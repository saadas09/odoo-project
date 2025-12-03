# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class TestHotelReservation(TransactionCase):
    
    def setUp(self):
        super(TestHotelReservation, self).setUp()
        
        # Create test room
        self.room = self.env['hotel.room'].create({
            'name': 'Test Room 101',
            'room_number': '101',
            'room_type': 'double',
            'price_per_night': 100.0,
            'capacity': 2,
            'status': 'available'
        })
        
        # Create test client
        self.client = self.env['hotel.client'].create({
            'name': 'Test Client',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'passport_number': 'AB123456'
        })
        
        # Test dates
        self.check_in = date.today() + timedelta(days=1)
        self.check_out = date.today() + timedelta(days=4)
    
    def test_01_room_creation(self):
        """Test room creation and constraints"""
        self.assertTrue(self.room)
        self.assertEqual(self.room.status, 'available')
        self.assertEqual(self.room.price_per_night, 100.0)
    
    def test_02_client_creation(self):
        """Test client creation and email validation"""
        self.assertTrue(self.client)
        self.assertEqual(self.client.email, 'test@example.com')
        
        # Test email uniqueness
        with self.assertRaises(Exception):
            self.env['hotel.client'].create({
                'name': 'Another Client',
                'email': 'test@example.com',  # Duplicate email
                'phone': '+9876543210'
            })
    
    def test_03_invalid_email_format(self):
        """Test email format validation"""
        with self.assertRaises(ValidationError):
            self.env['hotel.client'].create({
                'name': 'Invalid Email Client',
                'email': 'invalid-email',  # Invalid format
                'phone': '+1234567890'
            })
    
    def test_04_reservation_creation(self):
        """Test reservation creation"""
        reservation = self.env['hotel.reservation'].create({
            'client_id': self.client.id,
            'room_id': self.room.id,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'status': 'draft'
        })
        
        self.assertTrue(reservation)
        self.assertEqual(reservation.status, 'draft')
        self.assertEqual(reservation.nights, 3)
    
    def test_05_total_price_calculation(self):
        """Test automatic total price calculation"""
        reservation = self.env['hotel.reservation'].create({
            'client_id': self.client.id,
            'room_id': self.room.id,
            'check_in': self.check_in,
            'check_out': self.check_out
        })
        
        expected_price = 100.0 * 3  # 3 nights × 100/night
        self.assertEqual(reservation.total_price, expected_price)
    
    def test_06_invalid_dates(self):
        """Test date validation (check-out must be after check-in)"""
        with self.assertRaises(ValidationError):
            self.env['hotel.reservation'].create({
                'client_id': self.client.id,
                'room_id': self.room.id,
                'check_in': self.check_out,  # Invalid: check-in after check-out
                'check_out': self.check_in,
                'status': 'draft'
            })
    
    def test_07_overlapping_reservations(self):
        """Test prevention of overlapping reservations"""
        # Create first reservation
        reservation1 = self.env['hotel.reservation'].create({
            'client_id': self.client.id,
            'room_id': self.room.id,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'status': 'confirmed'
        })
        
        self.assertTrue(reservation1)
        
        # Try to create overlapping reservation (should fail)
        with self.assertRaises(ValidationError):
            self.env['hotel.reservation'].create({
                'client_id': self.client.id,
                'room_id': self.room.id,
                'check_in': self.check_in + timedelta(days=1),  # Overlaps with reservation1
                'check_out': self.check_out + timedelta(days=1),
                'status': 'confirmed'
            })
    
    def test_08_room_status_update_on_confirmation(self):
        """Test room status changes to occupied when reservation is confirmed"""
        # Create reservation in the current date range
        current_check_in = date.today()
        current_check_out = date.today() + timedelta(days=2)
        
        reservation = self.env['hotel.reservation'].create({
            'client_id': self.client.id,
            'room_id': self.room.id,
            'check_in': current_check_in,
            'check_out': current_check_out,
            'status': 'draft'
        })
        
        # Confirm reservation
        reservation.action_confirm()
        
        self.assertEqual(reservation.status, 'confirmed')
        self.assertEqual(self.room.status, 'occupied')
    
    def test_09_room_status_update_on_cancellation(self):
        """Test room status returns to available when reservation is cancelled"""
        # Create and confirm reservation
        current_check_in = date.today()
        current_check_out = date.today() + timedelta(days=2)
        
        reservation = self.env['hotel.reservation'].create({
            'client_id': self.client.id,
            'room_id': self.room.id,
            'check_in': current_check_in,
            'check_out': current_check_out,
            'status': 'draft'
        })
        
        reservation.action_confirm()
        self.assertEqual(self.room.status, 'occupied')
        
        # Cancel reservation
        reservation.action_cancel()
        
        self.assertEqual(reservation.status, 'cancelled')
        self.assertEqual(self.room.status, 'available')
    
    def test_10_check_room_availability(self):
        """Test room availability check method"""
        # Room should be available for future dates
        is_available = self.room.check_availability(self.check_in, self.check_out)
        self.assertTrue(is_available)
        
        # Create a reservation
        reservation = self.env['hotel.reservation'].create({
            'client_id': self.client.id,
            'room_id': self.room.id,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'status': 'confirmed'
        })
        
        # Room should not be available for overlapping dates
        is_available = self.room.check_availability(
            self.check_in + timedelta(days=1),
            self.check_out + timedelta(days=1)
        )
        self.assertFalse(is_available)
    
    def test_11_reservation_sequence(self):
        """Test reservation number auto-generation"""
        reservation1 = self.env['hotel.reservation'].create({
            'client_id': self.client.id,
            'room_id': self.room.id,
            'check_in': self.check_in,
            'check_out': self.check_out
        })
        
        reservation2 = self.env['hotel.reservation'].create({
            'client_id': self.client.id,
            'room_id': self.room.id,
            'check_in': self.check_in + timedelta(days=10),
            'check_out': self.check_out + timedelta(days=10)
        })
        
        # Both should have auto-generated names
        self.assertTrue(reservation1.name)
        self.assertTrue(reservation2.name)
        self.assertNotEqual(reservation1.name, reservation2.name)
    
    def test_12_room_maintenance_status(self):
        """Test that rooms in maintenance cannot be booked"""
        # Set room to maintenance
        self.room.status = 'maintenance'
        
        # Try to create reservation (should fail)
        with self.assertRaises(ValidationError):
            reservation = self.env['hotel.reservation'].create({
                'client_id': self.client.id,
                'room_id': self.room.id,
                'check_in': self.check_in,
                'check_out': self.check_out,
                'status': 'confirmed'
            })
    
    def test_13_multiple_non_overlapping_reservations(self):
        """Test that multiple non-overlapping reservations work correctly"""
        # Create first reservation
        reservation1 = self.env['hotel.reservation'].create({
            'client_id': self.client.id,
            'room_id': self.room.id,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'status': 'confirmed'
        })
        
        # Create second reservation (after the first one)
        reservation2 = self.env['hotel.reservation'].create({
            'client_id': self.client.id,
            'room_id': self.room.id,
            'check_in': self.check_out + timedelta(days=1),
            'check_out': self.check_out + timedelta(days=4),
            'status': 'confirmed'
        })
        
        self.assertTrue(reservation1)
        self.assertTrue(reservation2)
        self.assertEqual(reservation1.status, 'confirmed')
        self.assertEqual(reservation2.status, 'confirmed')
    
    def test_14_client_reservation_count(self):
        """Test client reservation count calculation"""
        initial_count = self.client.reservation_count
        
        # Create a reservation
        self.env['hotel.reservation'].create({
            'client_id': self.client.id,
            'room_id': self.room.id,
            'check_in': self.check_in,
            'check_out': self.check_out
        })
        
        # Refresh client
        self.client.invalidate_cache()
        
        self.assertEqual(self.client.reservation_count, initial_count + 1)
