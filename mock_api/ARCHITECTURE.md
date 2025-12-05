# Hotel Reservation System - Mock API Architecture

## System Overview

```
┌────────────────────────────────────────────────────────────────┐
│                     ODOO 16 WEB INTERFACE                      │
│  http://localhost:8069                                         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Rooms      │  │ Reservations │  │   Clients    │        │
│  │  Management  │  │  Management  │  │  Management  │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                          │                                      │
│                          │ [Sync Booking.com] [Sync Airbnb]   │
│                          ↓                                      │
└──────────────────────────┼──────────────────────────────────────┘
                           │
                           │ HTTP GET Requests
                           │
                           ↓
┌────────────────────────────────────────────────────────────────┐
│               MOCK API SERVER (FastAPI)                        │
│  http://localhost:8000                                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  ENDPOINTS                                             │    │
│  │  • GET  /booking/reservations                         │    │
│  │  • GET  /airbnb/reservations                          │    │
│  │  • GET  /booking/availability                         │    │
│  │  • GET  /airbnb/availability                          │    │
│  │  • POST /booking/update_availability                  │    │
│  │  • POST /airbnb/update_calendar                       │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  SAMPLE DATA (In-Memory)                              │    │
│  │  • 3 Booking.com Reservations                         │    │
│  │  • 3 Airbnb Reservations                              │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Data Flow - Synchronization Process

```
USER ACTION                  ODOO                    MOCK API
─────────────────────────────────────────────────────────────────

1. Click "Sync            → Trigger Action
   Booking.com"             
                             ↓
                          Call method:
                          sync_booking_
                          reservations()
                             ↓
                          HTTP GET
                          /booking/
                          reservations
                             │
                             ↓                     
                                              ← Return JSON
                                                [{reservation1},
                                                 {reservation2},
                                                 {reservation3}]
                             ↓
                          Parse JSON
                          For each 
                          reservation:
                             ↓
                          Find/Create
                          Client
                             ↓
                          Find Room by
                          room_number
                             ↓
                          Check for
                          Duplicate
                             ↓
                          Create New
                          Reservation
                             ↓
                          Log Sync
                          Operation
                             ↓
← Show Notification      Complete!
  "Sync started..."
```

## Module Architecture

```
hotel_reservation_system/
│
├── models/                    ← Business Logic
│   ├── hotel_room.py         → Room management
│   ├── hotel_client.py       → Client/Guest management
│   ├── hotel_reservation.py  → Reservation management
│   └── api_synchronization.py → API sync logic ★
│       ├── sync_booking_reservations()
│       ├── sync_airbnb_reservations()
│       ├── _create_or_update_reservation_from_booking()
│       └── _create_or_update_reservation_from_airbnb()
│
├── views/                     ← User Interface
│   ├── reservation_views.xml → Reservation UI + Sync Buttons ★
│   ├── room_views.xml        → Room UI
│   ├── client_views.xml      → Client UI
│   └── menus.xml             → Navigation
│
├── data/                      ← Configuration
│   └── scheduled_jobs.xml    → CRON Jobs ★
│       ├── ir_cron_sync_booking_reservations (every hour)
│       └── ir_cron_sync_airbnb_reservations (every hour)
│
└── mock_api/                  ← Testing Infrastructure ★
    ├── server.py             → FastAPI server
    ├── requirements.txt      → Dependencies
    ├── start_server.bat      → Windows startup script
    ├── install_dependencies.bat → Dependency installer
    ├── verify_installation.py → Test script
    ├── README.md             → Complete documentation
    ├── QUICK_REFERENCE.md    → Quick reference card
    └── ARCHITECTURE.md       → This file

★ = New/Modified for Mock API integration
```

## Database Schema

```
┌─────────────────────┐
│   hotel.client      │
│─────────────────────│
│ id (PK)             │
│ name                │◄─────┐
│ email (unique)      │      │
│ phone               │      │
│ address             │      │
└─────────────────────┘      │
                              │
                              │
┌─────────────────────┐      │
│   hotel.room        │      │
│─────────────────────│      │
│ id (PK)             │      │
│ room_number (unique)│◄─┐   │
│ name                │  │   │
│ room_type           │  │   │
│ price_per_night     │  │   │
│ max_occupancy       │  │   │
│ currency_id         │  │   │
└─────────────────────┘  │   │
                         │   │
                         │   │
┌─────────────────────────────────────┐
│   hotel.reservation                 │
│─────────────────────────────────────│
│ id (PK)                             │
│ name (auto-generated: RES00001)     │
│ client_id (FK) ────────────────────┘
│ room_id (FK) ───────────────────────┘
│ check_in (date)                     │
│ check_out (date)                    │
│ num_adults                          │
│ num_children                        │
│ status (draft/confirmed/cancelled)  │
│ total_price (computed)              │
│ nights (computed)                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   api.synchronization               │
│─────────────────────────────────────│
│ id (PK)                             │
│ name (sync identifier)              │
│ last_sync_date                      │
│ sync_type (booking/airbnb/avail)    │
│ status (success/error/pending)      │
│ error_message                       │
└─────────────────────────────────────┘
```

## API Communication Flow

### Request: Booking.com Reservations

```
REQUEST:
GET http://localhost:8000/booking/reservations?check_in_from=2024-01-01

RESPONSE:
[
  {
    "reservation_id": "BK-2024-001",
    "guest_name": "John Smith",
    "guest_email": "john.smith@example.com",
    "guest_phone": "+1-555-0101",
    "room_number": "101",
    "room_type": "Deluxe Suite",
    "check_in": "2024-02-15",
    "check_out": "2024-02-18",
    "num_adults": 2,
    "num_children": 0,
    "total_price": 450.00,
    "currency": "USD",
    "status": "confirmed"
  }
]

ODOO PROCESSING:
1. Search for client by email: john.smith@example.com
2. If not found, create new client:
   - name: "John Smith"
   - email: "john.smith@example.com"
   - phone: "+1-555-0101"
3. Search for room by room_number: "101"
4. Check for existing reservation (same client, room, dates)
5. If not exists, create reservation:
   - client_id: <client.id>
   - room_id: <room.id>
   - check_in: 2024-02-15
   - check_out: 2024-02-18
   - num_adults: 2
   - status: "confirmed"
```

### Request: Airbnb Reservations

```
REQUEST:
GET http://localhost:8000/airbnb/reservations?start_date_from=2024-01-01

RESPONSE:
[
  {
    "confirmation_code": "HMABCDEF123",
    "status": "accepted",
    "guest": {
      "name": "Sarah Johnson",
      "email": "sarah.johnson@example.com",
      "phone": "+1-555-0201"
    },
    "listing": {
      "id": "listing-101",
      "name": "Cozy Room with Ocean View",
      "room_number": "101"
    },
    "start_date": "2024-03-10",
    "end_date": "2024-03-13",
    "number_of_guests": 2
  }
]

ODOO PROCESSING:
1. Extract guest info from nested object: guest.name, guest.email
2. Extract room info from nested object: listing.room_number
3. Follow same process as Booking.com
```

## CRON Job Architecture

```
ODOO CRON SCHEDULER
(Every hour)
    │
    ├─► Job 1: Sync Booking.com
    │   │
    │   ├─ Name: "Sync Booking.com Reservations"
    │   ├─ Model: api.synchronization
    │   ├─ Code: model.sync_booking_reservations()
    │   ├─ Interval: 1 hour
    │   ├─ Active: True
    │   │
    │   └─► Executes sync_booking_reservations()
    │       │
    │       ├─ Call mock API: /booking/reservations
    │       ├─ Process JSON response
    │       ├─ Create/Update records
    │       └─ Log result to api.synchronization
    │
    └─► Job 2: Sync Airbnb
        │
        ├─ Name: "Sync Airbnb Reservations"
        ├─ Model: api.synchronization
        ├─ Code: model.sync_airbnb_reservations()
        ├─ Interval: 1 hour
        ├─ Active: True
        │
        └─► Executes sync_airbnb_reservations()
            │
            ├─ Call mock API: /airbnb/reservations
            ├─ Process JSON response
            ├─ Create/Update records
            └─ Log result to api.synchronization
```

## Security & Error Handling

### Duplicate Prevention

```python
# Check if reservation already exists
existing = env['hotel.reservation'].search([
    ('client_id', '=', client.id),
    ('room_id', '=', room.id),
    ('check_in', '=', check_in),
    ('check_out', '=', check_out)
], limit=1)

if existing:
    logger.info("Reservation already exists, skipping")
    return False
```

### Room Availability Validation

```python
# In hotel.reservation model
@api.constrains('check_in', 'check_out', 'room_id')
def _check_room_availability(self):
    """Prevent double bookings"""
    conflicting = self.search([
        ('room_id', '=', self.room_id.id),
        ('id', '!=', self.id),
        ('status', '!=', 'cancelled'),
        ('check_in', '<', self.check_out),
        ('check_out', '>', self.check_in)
    ])
    
    if conflicting:
        raise ValidationError("Room not available!")
```

### Error Logging

```python
try:
    # Sync operations
    ...
    self.create({
        'status': 'success',
        'error_message': f'Synced {count} reservations'
    })
except Exception as e:
    logger.error(f"Sync failed: {str(e)}")
    self.create({
        'status': 'error',
        'error_message': str(e)
    })
```

## Testing Strategy

```
┌─────────────────────────────────────────┐
│ LEVEL 1: Component Testing              │
├─────────────────────────────────────────┤
│ 1. Mock API Server                      │
│    □ Dependencies installed             │
│    □ Server starts                      │
│    □ Endpoints respond                  │
│    □ Returns valid JSON                 │
│                                          │
│ 2. Odoo Module                          │
│    □ Module installs                    │
│    □ Views load                         │
│    □ Models create records              │
│    □ Buttons visible                    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ LEVEL 2: Integration Testing            │
├─────────────────────────────────────────┤
│ 1. Configuration                        │
│    □ System parameter set               │
│    □ Rooms created                      │
│    □ CRON jobs active                   │
│                                          │
│ 2. Manual Sync                          │
│    □ Button triggers action             │
│    □ API call succeeds                  │
│    □ JSON parsed correctly              │
│    □ Records created                    │
│    □ Sync logged                        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ LEVEL 3: End-to-End Testing             │
├─────────────────────────────────────────┤
│ 1. Full Workflow                        │
│    □ Start mock API                     │
│    □ Configure Odoo                     │
│    □ Run sync                           │
│    □ Verify 6 reservations              │
│    □ Verify 6 clients                   │
│    □ Check sync logs                    │
│    □ Test duplicate prevention          │
│    □ Verify CRON execution              │
└─────────────────────────────────────────┘
```

## Performance Considerations

### Mock API
- **Response Time**: < 10ms (in-memory data)
- **Concurrent Requests**: Supports multiple simultaneous requests
- **Data Size**: 3 reservations per platform = ~5KB JSON

### Odoo Sync
- **Processing Time**: ~1-2 seconds for 6 reservations
- **Database Queries**: 
  - 1 search per client (by email)
  - 1 search per room (by room_number)
  - 1 search per reservation (duplicate check)
  - 1 insert per new record
- **Total Queries**: ~18 queries for 6 reservations

### CRON Impact
- **Frequency**: Every 1 hour
- **Execution Time**: ~2-3 seconds
- **System Load**: Negligible (runs in background)

## Scaling to Production

### From Mock to Real APIs

```
MOCK API                    REAL API
────────────────────────────────────────────

http://localhost:8000   →  https://api.booking.com
                           https://api.airbnb.com

No authentication       →  OAuth 2.0 / API Keys
                           
In-memory data          →  Live database
                           
Instant response        →  Rate limits apply
                           
Static sample data      →  Real-time updates
                           
No webhooks             →  Webhook receivers
                           
Development only        →  Production-ready
```

### Production Checklist

- [ ] Replace mock endpoints with real API URLs
- [ ] Implement OAuth 2.0 authentication
- [ ] Add rate limiting handling
- [ ] Implement webhook receivers for real-time updates
- [ ] Add data validation and sanitization
- [ ] Set up monitoring and alerting
- [ ] Implement proper error recovery
- [ ] Add request/response logging
- [ ] Configure SSL/TLS certificates
- [ ] Set up backup and disaster recovery
- [ ] Implement API key rotation
- [ ] Add performance monitoring
- [ ] Set up load balancing (if needed)

---

**Architecture Version**: 1.0.0  
**Last Updated**: 2024  
**Module Version**: 16.0.1.0.0
