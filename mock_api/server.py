# -*- coding: utf-8 -*-
"""
Mock API Server for Booking.com and Airbnb
Simulates external booking platforms for testing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import random
import uvicorn

app = FastAPI(title="Hotel Mock API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data
BOOKING_RESERVATIONS = [
    {
        "reservation_id": "BK-2025-001",
        "guest": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@email.com",
            "phone": "+1234567890",
            "country": "USA"
        },
        "room": {
            "room_type": "double",
            "room_number": "101"
        },
        "dates": {
            "check_in": "2025-12-15",
            "check_out": "2025-12-20"
        },
        "pricing": {
            "total_price": 500.00,
            "currency": "USD",
            "price_per_night": 100.00
        },
        "status": "confirmed",
        "created_at": "2025-12-01T10:30:00Z",
        "platform": "booking.com"
    },
    {
        "reservation_id": "BK-2025-002",
        "guest": {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@email.com",
            "phone": "+1987654321",
            "country": "UK"
        },
        "room": {
            "room_type": "suite",
            "room_number": "205"
        },
        "dates": {
            "check_in": "2025-12-18",
            "check_out": "2025-12-22"
        },
        "pricing": {
            "total_price": 800.00,
            "currency": "USD",
            "price_per_night": 200.00
        },
        "status": "confirmed",
        "created_at": "2025-12-02T14:20:00Z",
        "platform": "booking.com"
    },
    {
        "reservation_id": "BK-2025-003",
        "guest": {
            "first_name": "Michael",
            "last_name": "Johnson",
            "email": "michael.j@email.com",
            "phone": "+1122334455",
            "country": "Canada"
        },
        "room": {
            "room_type": "single",
            "room_number": "310"
        },
        "dates": {
            "check_in": "2025-12-25",
            "check_out": "2025-12-28"
        },
        "pricing": {
            "total_price": 240.00,
            "currency": "USD",
            "price_per_night": 80.00
        },
        "status": "confirmed",
        "created_at": "2025-12-03T09:15:00Z",
        "platform": "booking.com"
    }
]

AIRBNB_RESERVATIONS = [
    {
        "confirmation_code": "HMAB123456",
        "guest": {
            "first_name": "Sarah",
            "last_name": "Williams",
            "email": "sarah.w@email.com",
            "phone": "+1555666777"
        },
        "listing": {
            "id": "12345",
            "name": "Luxury Double Room",
            "room_type": "double",
            "room_number": "101"
        },
        "check_in": "2025-12-10",
        "check_out": "2025-12-14",
        "guest_details": {
            "number_of_guests": 2,
            "number_of_adults": 2,
            "number_of_children": 0
        },
        "pricing": {
            "nights": 4,
            "nightly_price": 120.00,
            "total_price": 480.00,
            "currency": "USD",
            "service_fee": 48.00
        },
        "status": "accepted",
        "booked_at": "2025-11-28T16:45:00Z",
        "platform": "airbnb"
    },
    {
        "confirmation_code": "HMAB789012",
        "guest": {
            "first_name": "David",
            "last_name": "Brown",
            "email": "david.brown@email.com",
            "phone": "+1444555666"
        },
        "listing": {
            "id": "67890",
            "name": "Cozy Suite",
            "room_type": "suite",
            "room_number": "205"
        },
        "check_in": "2025-12-20",
        "check_out": "2025-12-25",
        "guest_details": {
            "number_of_guests": 3,
            "number_of_adults": 2,
            "number_of_children": 1
        },
        "pricing": {
            "nights": 5,
            "nightly_price": 180.00,
            "total_price": 900.00,
            "currency": "USD",
            "service_fee": 90.00
        },
        "status": "accepted",
        "booked_at": "2025-12-01T11:30:00Z",
        "platform": "airbnb"
    },
    {
        "confirmation_code": "HMAB345678",
        "guest": {
            "first_name": "Emma",
            "last_name": "Davis",
            "email": "emma.davis@email.com",
            "phone": "+1777888999"
        },
        "listing": {
            "id": "12345",
            "name": "Luxury Double Room",
            "room_type": "double",
            "room_number": "310"
        },
        "check_in": "2025-12-28",
        "check_out": "2025-12-31",
        "guest_details": {
            "number_of_guests": 2,
            "number_of_adults": 2,
            "number_of_children": 0
        },
        "pricing": {
            "nights": 3,
            "nightly_price": 150.00,
            "total_price": 450.00,
            "currency": "USD",
            "service_fee": 45.00
        },
        "status": "accepted",
        "booked_at": "2025-12-02T19:20:00Z",
        "platform": "airbnb"
    }
]


@app.get("/")
def root():
    """API Root"""
    return {
        "message": "Hotel Mock API Server",
        "version": "1.0.0",
        "endpoints": {
            "booking_reservations": "/booking/reservations",
            "airbnb_reservations": "/airbnb/reservations",
            "booking_availability": "/booking/availability",
            "airbnb_availability": "/airbnb/availability"
        }
    }


@app.get("/booking/reservations")
def get_booking_reservations(status: str = None, date_from: str = None, date_to: str = None):
    """
    Get Booking.com reservations
    
    Query Parameters:
    - status: Filter by status (confirmed, cancelled, pending)
    - date_from: Filter from date (YYYY-MM-DD)
    - date_to: Filter to date (YYYY-MM-DD)
    """
    reservations = BOOKING_RESERVATIONS.copy()
    
    # Filter by status
    if status:
        reservations = [r for r in reservations if r["status"] == status]
    
    # Filter by date range
    if date_from:
        reservations = [r for r in reservations if r["dates"]["check_in"] >= date_from]
    
    if date_to:
        reservations = [r for r in reservations if r["dates"]["check_out"] <= date_to]
    
    return {
        "success": True,
        "count": len(reservations),
        "reservations": reservations
    }


@app.get("/airbnb/reservations")
def get_airbnb_reservations(status: str = None, listing_id: str = None):
    """
    Get Airbnb reservations
    
    Query Parameters:
    - status: Filter by status (accepted, cancelled, pending)
    - listing_id: Filter by listing ID
    """
    reservations = AIRBNB_RESERVATIONS.copy()
    
    # Filter by status
    if status:
        reservations = [r for r in reservations if r["status"] == status]
    
    # Filter by listing ID
    if listing_id:
        reservations = [r for r in reservations if r["listing"]["id"] == listing_id]
    
    return {
        "success": True,
        "count": len(reservations),
        "reservations": reservations
    }


@app.get("/booking/availability")
def get_booking_availability(hotel_id: str = "default", date_from: str = None, date_to: str = None):
    """
    Get room availability from Booking.com
    
    Query Parameters:
    - hotel_id: Hotel ID
    - date_from: Start date (YYYY-MM-DD)
    - date_to: End date (YYYY-MM-DD)
    """
    if not date_from:
        date_from = datetime.now().strftime("%Y-%m-%d")
    if not date_to:
        date_to = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    availability = {
        "hotel_id": hotel_id,
        "date_from": date_from,
        "date_to": date_to,
        "rooms": [
            {
                "room_id": "101",
                "room_type": "single",
                "available": True,
                "price": 80.00,
                "currency": "USD"
            },
            {
                "room_id": "102",
                "room_type": "double",
                "available": True,
                "price": 120.00,
                "currency": "USD"
            },
            {
                "room_id": "201",
                "room_type": "suite",
                "available": False,
                "price": 200.00,
                "currency": "USD"
            }
        ]
    }
    
    return {
        "success": True,
        "availability": availability
    }


@app.get("/airbnb/availability")
def get_airbnb_availability(listing_id: str = "12345", month: int = None, year: int = None):
    """
    Get listing availability from Airbnb
    
    Query Parameters:
    - listing_id: Airbnb listing ID
    - month: Month (1-12)
    - year: Year (YYYY)
    """
    if not month:
        month = datetime.now().month
    if not year:
        year = datetime.now().year
    
    # Generate sample calendar
    days_in_month = 30
    calendar = []
    
    for day in range(1, days_in_month + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"
        is_available = random.choice([True, True, True, False])  # 75% available
        
        calendar.append({
            "date": date_str,
            "available": is_available,
            "price": 120.00 if is_available else None,
            "minimum_nights": 1,
            "maximum_nights": 30
        })
    
    return {
        "success": True,
        "listing_id": listing_id,
        "month": month,
        "year": year,
        "calendar": calendar
    }


@app.post("/booking/update_availability")
def update_booking_availability(room_id: str, date: str, available: bool):
    """Update room availability on Booking.com (mock)"""
    return {
        "success": True,
        "message": f"Availability updated for room {room_id} on {date}",
        "room_id": room_id,
        "date": date,
        "available": available
    }


@app.post("/airbnb/update_calendar")
def update_airbnb_calendar(listing_id: str, date: str, available: bool, price: float = None):
    """Update calendar on Airbnb (mock)"""
    return {
        "success": True,
        "message": f"Calendar updated for listing {listing_id} on {date}",
        "listing_id": listing_id,
        "date": date,
        "available": available,
        "price": price
    }


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Hotel Mock API Server")
    print("=" * 60)
    print("📍 Server running on: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    print("\n✅ Available Endpoints:")
    print("   - GET  /booking/reservations")
    print("   - GET  /airbnb/reservations")
    print("   - GET  /booking/availability")
    print("   - GET  /airbnb/availability")
    print("   - POST /booking/update_availability")
    print("   - POST /airbnb/update_calendar")
    print("\n" + "=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
