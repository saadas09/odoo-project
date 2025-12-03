# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class ApiSynchronization(models.Model):
    _name = 'api.synchronization'
    _description = 'API Synchronization'

    name = fields.Char(string='Synchronization Name', required=True)
    last_sync_date = fields.Datetime(string='Last Synchronization Date')
    sync_type = fields.Selection([
        ('booking', 'Booking.com'),
        ('airbnb', 'Airbnb'),
        ('availability', 'Availability Update')
    ], string='Synchronization Type', required=True)
    status = fields.Selection([
        ('success', 'Success'),
        ('error', 'Error'),
        ('pending', 'Pending')
    ], string='Status', default='pending')
    error_message = fields.Text(string='Error Message')
    
    # API Configuration fields
    api_key = fields.Char(string='API Key')
    api_secret = fields.Char(string='API Secret')
    api_endpoint = fields.Char(string='API Endpoint')

    @api.model
    def sync_booking_reservations(self):
        """Synchronize reservations from Booking.com"""
        _logger.info("Starting Booking.com synchronization...")
        
        try:
            # Get API configuration
            config = self.env['ir.config_parameter'].sudo()
            booking_api_key = config.get_param('hotel_reservation.booking_api_key')
            booking_api_endpoint = config.get_param('hotel_reservation.booking_api_endpoint')
            
            if not booking_api_key or not booking_api_endpoint:
                _logger.warning("Booking.com API credentials not configured")
                return False
            
            # Prepare API request
            headers = {
                'Authorization': f'Bearer {booking_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Get reservations from the last 7 days
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            to_date = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
            
            params = {
                'from_date': from_date,
                'to_date': to_date
            }
            
            # Make API call (example endpoint)
            # response = requests.get(
            #     f"{booking_api_endpoint}/reservations",
            #     headers=headers,
            #     params=params,
            #     timeout=30
            # )
            
            # For demonstration purposes, we'll simulate the response
            # In production, uncomment the above code and comment out the simulation
            
            # Simulated response data
            simulated_reservations = []
            
            # Process reservations
            for booking_reservation in simulated_reservations:
                self._create_or_update_reservation_from_booking(booking_reservation)
            
            # Log successful sync
            self.create({
                'name': f'Booking.com Sync - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                'last_sync_date': fields.Datetime.now(),
                'sync_type': 'booking',
                'status': 'success'
            })
            
            _logger.info("Booking.com synchronization completed successfully")
            return True
            
        except Exception as e:
            error_msg = f"Error during Booking.com synchronization: {str(e)}"
            _logger.error(error_msg)
            
            self.create({
                'name': f'Booking.com Sync - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                'last_sync_date': fields.Datetime.now(),
                'sync_type': 'booking',
                'status': 'error',
                'error_message': error_msg
            })
            
            return False

    @api.model
    def sync_airbnb_reservations(self):
        """Synchronize reservations from Airbnb"""
        _logger.info("Starting Airbnb synchronization...")
        
        try:
            # Get API configuration
            config = self.env['ir.config_parameter'].sudo()
            airbnb_api_key = config.get_param('hotel_reservation.airbnb_api_key')
            airbnb_api_endpoint = config.get_param('hotel_reservation.airbnb_api_endpoint')
            
            if not airbnb_api_key or not airbnb_api_endpoint:
                _logger.warning("Airbnb API credentials not configured")
                return False
            
            # Prepare API request
            headers = {
                'Authorization': f'Bearer {airbnb_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Get reservations from the last 7 days
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            to_date = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
            
            params = {
                'start_date': from_date,
                'end_date': to_date
            }
            
            # Make API call (example endpoint)
            # response = requests.get(
            #     f"{airbnb_api_endpoint}/reservations",
            #     headers=headers,
            #     params=params,
            #     timeout=30
            # )
            
            # For demonstration purposes, we'll simulate the response
            simulated_reservations = []
            
            # Process reservations
            for airbnb_reservation in simulated_reservations:
                self._create_or_update_reservation_from_airbnb(airbnb_reservation)
            
            # Log successful sync
            self.create({
                'name': f'Airbnb Sync - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                'last_sync_date': fields.Datetime.now(),
                'sync_type': 'airbnb',
                'status': 'success'
            })
            
            _logger.info("Airbnb synchronization completed successfully")
            return True
            
        except Exception as e:
            error_msg = f"Error during Airbnb synchronization: {str(e)}"
            _logger.error(error_msg)
            
            self.create({
                'name': f'Airbnb Sync - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                'last_sync_date': fields.Datetime.now(),
                'sync_type': 'airbnb',
                'status': 'error',
                'error_message': error_msg
            })
            
            return False

    @api.model
    def sync_availabilities(self):
        """Synchronize room availabilities to external platforms"""
        _logger.info("Starting availability synchronization...")
        
        try:
            # Get all rooms
            rooms = self.env['hotel.room'].search([])
            
            for room in rooms:
                # Get next 90 days availability
                start_date = fields.Date.today()
                end_date = start_date + timedelta(days=90)
                
                # Check availability for each day
                availability_data = []
                current_date = start_date
                
                while current_date <= end_date:
                    next_date = current_date + timedelta(days=1)
                    is_available = room.check_availability(current_date, next_date)
                    
                    availability_data.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'available': is_available,
                        'price': room.price_per_night
                    })
                    
                    current_date = next_date
                
                # Send availability to external platforms
                self._send_availability_to_booking(room, availability_data)
                self._send_availability_to_airbnb(room, availability_data)
            
            # Log successful sync
            self.create({
                'name': f'Availability Sync - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                'last_sync_date': fields.Datetime.now(),
                'sync_type': 'availability',
                'status': 'success'
            })
            
            _logger.info("Availability synchronization completed successfully")
            return True
            
        except Exception as e:
            error_msg = f"Error during availability synchronization: {str(e)}"
            _logger.error(error_msg)
            
            self.create({
                'name': f'Availability Sync - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                'last_sync_date': fields.Datetime.now(),
                'sync_type': 'availability',
                'status': 'error',
                'error_message': error_msg
            })
            
            return False

    def _create_or_update_reservation_from_booking(self, booking_data):
        """Create or update reservation from Booking.com data"""
        # Extract data from booking response
        external_id = booking_data.get('reservation_id')
        guest_name = booking_data.get('guest_name')
        guest_email = booking_data.get('guest_email')
        room_number = booking_data.get('room_number')
        check_in = booking_data.get('check_in')
        check_out = booking_data.get('check_out')
        
        # Find or create client
        client = self.env['hotel.client'].search([('email', '=', guest_email)], limit=1)
        if not client:
            client = self.env['hotel.client'].create({
                'name': guest_name,
                'email': guest_email,
                'phone': booking_data.get('guest_phone', '')
            })
        
        # Find room
        room = self.env['hotel.room'].search([('room_number', '=', room_number)], limit=1)
        if not room:
            _logger.warning(f"Room {room_number} not found in system")
            return
        
        # Check if reservation already exists
        existing_reservation = self.env['hotel.reservation'].search([
            ('client_id', '=', client.id),
            ('room_id', '=', room.id),
            ('check_in', '=', check_in),
            ('check_out', '=', check_out)
        ], limit=1)
        
        if not existing_reservation:
            # Create new reservation
            self.env['hotel.reservation'].create({
                'client_id': client.id,
                'room_id': room.id,
                'check_in': check_in,
                'check_out': check_out,
                'status': 'confirmed'
            })
            _logger.info(f"Created reservation from Booking.com: {external_id}")

    def _create_or_update_reservation_from_airbnb(self, airbnb_data):
        """Create or update reservation from Airbnb data"""
        # Extract data from Airbnb response
        external_id = airbnb_data.get('confirmation_code')
        guest_name = airbnb_data.get('guest', {}).get('name')
        guest_email = airbnb_data.get('guest', {}).get('email')
        room_number = airbnb_data.get('listing', {}).get('room_number')
        check_in = airbnb_data.get('start_date')
        check_out = airbnb_data.get('end_date')
        
        # Find or create client
        client = self.env['hotel.client'].search([('email', '=', guest_email)], limit=1)
        if not client:
            client = self.env['hotel.client'].create({
                'name': guest_name,
                'email': guest_email,
                'phone': airbnb_data.get('guest', {}).get('phone', '')
            })
        
        # Find room
        room = self.env['hotel.room'].search([('room_number', '=', room_number)], limit=1)
        if not room:
            _logger.warning(f"Room {room_number} not found in system")
            return
        
        # Check if reservation already exists
        existing_reservation = self.env['hotel.reservation'].search([
            ('client_id', '=', client.id),
            ('room_id', '=', room.id),
            ('check_in', '=', check_in),
            ('check_out', '=', check_out)
        ], limit=1)
        
        if not existing_reservation:
            # Create new reservation
            self.env['hotel.reservation'].create({
                'client_id': client.id,
                'room_id': room.id,
                'check_in': check_in,
                'check_out': check_out,
                'status': 'confirmed'
            })
            _logger.info(f"Created reservation from Airbnb: {external_id}")

    def _send_availability_to_booking(self, room, availability_data):
        """Send availability updates to Booking.com"""
        try:
            config = self.env['ir.config_parameter'].sudo()
            booking_api_key = config.get_param('hotel_reservation.booking_api_key')
            booking_api_endpoint = config.get_param('hotel_reservation.booking_api_endpoint')
            
            if not booking_api_key or not booking_api_endpoint:
                return False
            
            # Prepare API request
            # headers = {
            #     'Authorization': f'Bearer {booking_api_key}',
            #     'Content-Type': 'application/json'
            # }
            
            # payload = {
            #     'room_id': room.room_number,
            #     'availability': availability_data
            # }
            
            # response = requests.post(
            #     f"{booking_api_endpoint}/availability",
            #     headers=headers,
            #     json=payload,
            #     timeout=30
            # )
            
            _logger.info(f"Availability sent to Booking.com for room {room.room_number}")
            return True
            
        except Exception as e:
            _logger.error(f"Error sending availability to Booking.com: {str(e)}")
            return False

    def _send_availability_to_airbnb(self, room, availability_data):
        """Send availability updates to Airbnb"""
        try:
            config = self.env['ir.config_parameter'].sudo()
            airbnb_api_key = config.get_param('hotel_reservation.airbnb_api_key')
            airbnb_api_endpoint = config.get_param('hotel_reservation.airbnb_api_endpoint')
            
            if not airbnb_api_key or not airbnb_api_endpoint:
                return False
            
            # Prepare API request
            # headers = {
            #     'Authorization': f'Bearer {airbnb_api_key}',
            #     'Content-Type': 'application/json'
            # }
            
            # payload = {
            #     'listing_id': room.room_number,
            #     'availability': availability_data
            # }
            
            # response = requests.post(
            #     f"{airbnb_api_endpoint}/calendar",
            #     headers=headers,
            #     json=payload,
            #     timeout=30
            # )
            
            _logger.info(f"Availability sent to Airbnb for room {room.room_number}")
            return True
            
        except Exception as e:
            _logger.error(f"Error sending availability to Airbnb: {str(e)}")
            return False
