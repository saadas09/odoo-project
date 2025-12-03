# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class HotelClient(models.Model):
    _name = 'hotel.client'
    _description = 'Hotel Client'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Client Name',
        required=True,
        tracking=True
    )
    email = fields.Char(
        string='Email',
        required=True,
        tracking=True
    )
    phone = fields.Char(
        string='Phone',
        tracking=True
    )
    passport_number = fields.Char(
        string='Passport Number',
        tracking=True
    )
    
    reservation_ids = fields.One2many(
        'hotel.reservation',
        'client_id',
        string='Reservations'
    )
    reservation_count = fields.Integer(
        string='Reservation Count',
        compute='_compute_reservation_count'
    )
    
    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'Email must be unique!'),
    ]

    @api.depends('reservation_ids')
    def _compute_reservation_count(self):
        for client in self:
            client.reservation_count = len(client.reservation_ids)

    @api.constrains('email')
    def _check_email_format(self):
        """Validate email format"""
        for client in self:
            if client.email:
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, client.email):
                    raise ValidationError("Invalid email format")

    @api.constrains('phone')
    def _check_phone_format(self):
        """Validate phone format"""
        for client in self:
            if client.phone:
                phone_pattern = r'^[\d\s\+\-\(\)]+$'
                if not re.match(phone_pattern, client.phone):
                    raise ValidationError("Invalid phone format")
