# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Room Name',
        required=True,
        tracking=True
    )
    room_number = fields.Char(
        string='Room Number',
        required=True,
        tracking=True
    )
    room_type = fields.Selection([
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite')
    ], string='Room Type', required=True, default='single', tracking=True)
    
    price_per_night = fields.Float(
        string='Price per Night',
        required=True,
        tracking=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        required=True
    )
    capacity = fields.Integer(
        string='Capacity',
        required=True,
        default=1
    )
    status = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance')
    ], string='Status', required=True, default='available', tracking=True)
    
    reservation_ids = fields.One2many(
        'hotel.reservation',
        'room_id',
        string='Reservations'
    )
    
    _sql_constraints = [
        ('room_number_unique', 'UNIQUE(room_number)', 'Room number must be unique!')
    ]

    @api.model
    def calculate_total_price(self, check_in, check_out):
        """Calculate total price based on number of nights"""
        if not check_in or not check_out:
            return 0.0
        
        delta = check_out - check_in
        nights = delta.days
        
        if nights <= 0:
            raise ValidationError("Check-out date must be after check-in date")
        
        return self.price_per_night * nights

    def check_availability(self, check_in, check_out, reservation_id=None):
        """Check if room is available for given dates"""
        if self.status != 'available':
            return False
        
        # Check for overlapping reservations
        domain = [
            ('room_id', '=', self.id),
            ('status', '!=', 'cancelled'),
            '|',
            '&', ('check_in', '<=', check_in), ('check_out', '>', check_in),
            '&', ('check_in', '<', check_out), ('check_out', '>=', check_out),
        ]
        
        if reservation_id:
            domain.append(('id', '!=', reservation_id))
        
        overlapping = self.env['hotel.reservation'].search(domain, limit=1)
        
        return not bool(overlapping)
