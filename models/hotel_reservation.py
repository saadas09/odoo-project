# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class HotelReservation(models.Model):
    _name = 'hotel.reservation'
    _description = 'Hotel Reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'check_in desc'

    name = fields.Char(
        string='Reservation Number',
        required=True,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('hotel.reservation') or 'New'
    )
    client_id = fields.Many2one(
        'hotel.client',
        string='Client',
        required=True,
        tracking=True
    )
    room_id = fields.Many2one(
        'hotel.room',
        string='Room',
        required=True,
        tracking=True
    )
    check_in = fields.Date(
        string='Check-in Date',
        required=True,
        tracking=True
    )
    check_out = fields.Date(
        string='Check-out Date',
        required=True,
        tracking=True
    )
    total_price = fields.Float(
        string='Total Price',
        compute='_compute_total_price',
        store=True,
        tracking=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='room_id.currency_id',
        store=True,
        readonly=True
    )
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True, tracking=True)
    
    nights = fields.Integer(
        string='Number of Nights',
        compute='_compute_nights',
        store=True
    )
    
    # Related fields for easy access
    client_name = fields.Char(related='client_id.name', string='Client Name', readonly=True)
    client_email = fields.Char(related='client_id.email', string='Client Email', readonly=True)
    room_number = fields.Char(related='room_id.room_number', string='Room Number', readonly=True)
    room_type = fields.Selection(related='room_id.room_type', string='Room Type', readonly=True)
    price_per_night = fields.Float(related='room_id.price_per_night', string='Price/Night', readonly=True)

    @api.depends('check_in', 'check_out')
    def _compute_nights(self):
        """Compute number of nights"""
        for reservation in self:
            if reservation.check_in and reservation.check_out:
                delta = reservation.check_out - reservation.check_in
                reservation.nights = delta.days
            else:
                reservation.nights = 0

    @api.depends('check_in', 'check_out', 'room_id', 'room_id.price_per_night')
    def _compute_total_price(self):
        """Automatically calculate total price"""
        for reservation in self:
            if reservation.check_in and reservation.check_out and reservation.room_id:
                try:
                    reservation.total_price = reservation.room_id.calculate_total_price(
                        reservation.check_in,
                        reservation.check_out
                    )
                except ValidationError:
                    reservation.total_price = 0.0
            else:
                reservation.total_price = 0.0

    @api.constrains('check_in', 'check_out')
    def _check_dates(self):
        """Validate check-in and check-out dates"""
        for reservation in self:
            if reservation.check_in and reservation.check_out:
                if reservation.check_out <= reservation.check_in:
                    raise ValidationError("Check-out date must be after check-in date")
                
                if reservation.check_in < fields.Date.today() and reservation.status == 'draft':
                    raise ValidationError("Check-in date cannot be in the past for new reservations")

    @api.constrains('room_id', 'check_in', 'check_out')
    def _check_room_availability(self):
        """Prevent overlapping reservations for the same room"""
        for reservation in self:
            if reservation.room_id and reservation.check_in and reservation.check_out and reservation.status != 'cancelled':
                # Check for overlapping reservations
                domain = [
                    ('room_id', '=', reservation.room_id.id),
                    ('id', '!=', reservation.id),
                    ('status', '!=', 'cancelled'),
                    '|',
                    '&', ('check_in', '<=', reservation.check_in), ('check_out', '>', reservation.check_in),
                    '&', ('check_in', '<', reservation.check_out), ('check_out', '>=', reservation.check_out),
                ]
                
                overlapping = self.search(domain, limit=1)
                
                if overlapping:
                    raise ValidationError(
                        f"Room {reservation.room_id.room_number} is not available for the selected dates. "
                        f"Conflict with reservation {overlapping.name}"
                    )

    @api.model_create_multi
    def create(self, vals_list):
        """Generate sequence number on creation"""
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('hotel.reservation') or 'New'
        
        reservations = super(HotelReservation, self).create(vals_list)
        
        # Update room status if reservation is confirmed
        for reservation in reservations:
            if reservation.status == 'confirmed':
                reservation._update_room_status()
        
        return reservations

    def write(self, vals):
        """Update room status when reservation status changes"""
        result = super(HotelReservation, self).write(vals)
        
        if 'status' in vals:
            for reservation in self:
                reservation._update_room_status()
        
        return result

    def _update_room_status(self):
        """Update room status based on reservation status"""
        self.ensure_one()
        
        if self.status == 'confirmed':
            # Check if today is within the reservation period
            today = fields.Date.today()
            if self.check_in <= today <= self.check_out:
                self.room_id.status = 'occupied'
        elif self.status == 'cancelled':
            # Check if there are other active reservations for this room
            active_reservations = self.search([
                ('room_id', '=', self.room_id.id),
                ('status', '=', 'confirmed'),
                ('check_in', '<=', fields.Date.today()),
                ('check_out', '>=', fields.Date.today()),
                ('id', '!=', self.id)
            ], limit=1)
            
            if not active_reservations:
                self.room_id.status = 'available'

    def action_confirm(self):
        """Confirm reservation"""
        for reservation in self:
            if reservation.status != 'draft':
                raise ValidationError("Only draft reservations can be confirmed")
            
            # Verify room availability
            if not reservation.room_id.check_availability(
                reservation.check_in,
                reservation.check_out,
                reservation.id
            ):
                raise ValidationError(
                    f"Room {reservation.room_id.room_number} is not available for the selected dates"
                )
            
            reservation.status = 'confirmed'
            reservation._update_room_status()

    def action_cancel(self):
        """Cancel reservation"""
        for reservation in self:
            reservation.status = 'cancelled'
            reservation._update_room_status()

    def action_set_to_draft(self):
        """Reset to draft"""
        for reservation in self:
            reservation.status = 'draft'
            reservation._update_room_status()
