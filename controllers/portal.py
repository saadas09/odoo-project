# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class HotelReservationPortal(http.Controller):

    @http.route('/hotel/reservation/form', type='http', auth='public', website=True)
    def hotel_reservation_form(self, **kwargs):
        """Display hotel reservation form"""
        # Get available rooms
        rooms = request.env['hotel.room'].sudo().search([
            ('status', '=', 'available')
        ])
        
        values = {
            'rooms': rooms,
            'check_in': kwargs.get('check_in', ''),
            'check_out': kwargs.get('check_out', ''),
            'error': kwargs.get('error', ''),
            'success': kwargs.get('success', ''),
        }
        
        return request.render('hotel_reservation_system.hotel_reservation_form_template', values)

    @http.route('/hotel/reservation/check_availability', type='json', auth='public', methods=['POST'])
    def check_availability(self, check_in, check_out, **kwargs):
        """Check room availability via AJAX"""
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            
            if check_out_date <= check_in_date:
                return {
                    'success': False,
                    'message': 'Check-out date must be after check-in date'
                }
            
            # Find available rooms
            all_rooms = request.env['hotel.room'].sudo().search([])
            available_rooms = []
            
            for room in all_rooms:
                if room.check_availability(check_in_date, check_out_date):
                    nights = (check_out_date - check_in_date).days
                    total_price = room.price_per_night * nights
                    
                    available_rooms.append({
                        'id': room.id,
                        'name': room.name,
                        'room_number': room.room_number,
                        'room_type': room.room_type,
                        'price_per_night': room.price_per_night,
                        'total_price': total_price,
                        'capacity': room.capacity,
                        'nights': nights
                    })
            
            return {
                'success': True,
                'rooms': available_rooms
            }
            
        except Exception as e:
            _logger.error(f"Error checking availability: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }

    @http.route('/hotel/reservation/submit', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def submit_reservation(self, **post):
        """Submit reservation form"""
        try:
            # Extract form data
            room_id = int(post.get('room_id'))
            client_name = post.get('client_name')
            client_email = post.get('client_email')
            client_phone = post.get('client_phone')
            passport_number = post.get('passport_number', '')
            check_in = post.get('check_in')
            check_out = post.get('check_out')
            
            # Validate required fields
            if not all([room_id, client_name, client_email, check_in, check_out]):
                return request.redirect('/hotel/reservation/form?error=Missing required fields')
            
            # Convert dates
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            
            # Find or create client
            Client = request.env['hotel.client'].sudo()
            client = Client.search([('email', '=', client_email)], limit=1)
            
            if not client:
                client = Client.create({
                    'name': client_name,
                    'email': client_email,
                    'phone': client_phone,
                    'passport_number': passport_number
                })
            else:
                # Update client info if needed
                client.write({
                    'name': client_name,
                    'phone': client_phone,
                    'passport_number': passport_number
                })
            
            # Get room
            room = request.env['hotel.room'].sudo().browse(room_id)
            
            if not room.exists():
                return request.redirect('/hotel/reservation/form?error=Room not found')
            
            # Check availability
            if not room.check_availability(check_in_date, check_out_date):
                return request.redirect('/hotel/reservation/form?error=Room not available for selected dates')
            
            # Create reservation
            reservation = request.env['hotel.reservation'].sudo().create({
                'client_id': client.id,
                'room_id': room.id,
                'check_in': check_in_date,
                'check_out': check_out_date,
                'status': 'draft'
            })
            
            # Redirect to confirmation page
            return request.redirect(f'/hotel/reservation/confirmation/{reservation.id}')
            
        except Exception as e:
            _logger.error(f"Error submitting reservation: {str(e)}")
            return request.redirect(f'/hotel/reservation/form?error={str(e)}')

    @http.route('/hotel/reservation/confirmation/<int:reservation_id>', type='http', auth='public', website=True)
    def reservation_confirmation(self, reservation_id, **kwargs):
        """Display reservation confirmation"""
        reservation = request.env['hotel.reservation'].sudo().browse(reservation_id)
        
        if not reservation.exists():
            return request.redirect('/hotel/reservation/form?error=Reservation not found')
        
        values = {
            'reservation': reservation
        }
        
        return request.render('hotel_reservation_system.hotel_reservation_confirmation_template', values)

    @http.route('/hotel/rooms', type='http', auth='public', website=True)
    def list_rooms(self, **kwargs):
        """List all available rooms"""
        rooms = request.env['hotel.room'].sudo().search([
            ('status', '=', 'available')
        ])
        
        values = {
            'rooms': rooms
        }
        
        return request.render('hotel_reservation_system.hotel_rooms_list_template', values)
