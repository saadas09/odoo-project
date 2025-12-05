# Mock API Server for Hotel Reservation System

## Overview

This mock API server simulates the Booking.com and Airbnb APIs to allow testing and development of the hotel reservation synchronization features without requiring actual API credentials or hotel partnerships.

The server provides realistic endpoints that mirror the structure and behavior of the real Booking.com Connectivity API and Airbnb Host API.

## Features

- **Booking.com Mock Endpoints**: Simulates reservation retrieval and availability updates
- **Airbnb Mock Endpoints**: Simulates reservation retrieval and calendar management
- **Realistic Sample Data**: Includes 3 Booking.com and 3 Airbnb reservations with complete guest and booking information
- **Query Filtering**: Supports date range filtering for reservations
- **CORS Enabled**: Allows cross-origin requests for integration with web clients

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

Navigate to the mock_api directory and install required packages:

```bash
cd "C:\Program Files\Odoo 16.0.20230101\server\odoo\addons\hotel_reservation_system\mock_api"
pip install -r requirements.txt
```

Required packages:
- `fastapi==0.104.1` - Modern web framework for building APIs
- `uvicorn==0.24.0` - ASGI server for running FastAPI
- `pydantic==2.5.0` - Data validation using Python type annotations

## Running the Mock API Server

### Start the Server

From the mock_api directory, run:

```bash
uvicorn server:app --reload --port 8000
```

Or using Python directly:

```bash
python -m uvicorn server:app --reload --port 8000
```

The server will start on `http://localhost:8000`

### Server Output

When started successfully, you should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
======================================
 Mock API Server for Hotel Reservations
======================================
Available Endpoints:
  - GET  /booking/reservations
  - GET  /airbnb/reservations
  - GET  /booking/availability
  - GET  /airbnb/availability
  - POST /booking/update_availability
  - POST /airbnb/update_calendar
======================================
```

### Verify Server is Running

Open a browser and navigate to:
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## API Endpoints

### 1. Booking.com Reservations

**Endpoint**: `GET /booking/reservations`

**Description**: Retrieve reservations from Booking.com

**Query Parameters**:
- `check_in_from` (optional): Filter reservations with check-in after this date (YYYY-MM-DD)
- `check_in_to` (optional): Filter reservations with check-in before this date (YYYY-MM-DD)
- `status` (optional): Filter by reservation status (confirmed, cancelled, pending)

**Example Request**:
```bash
curl "http://localhost:8000/booking/reservations?check_in_from=2024-01-01&check_in_to=2024-12-31"
```

**Response Format**:
```json
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
    "status": "confirmed",
    "booking_date": "2024-01-20T10:30:00",
    "special_requests": "Late check-in requested"
  }
]
```

### 2. Airbnb Reservations

**Endpoint**: `GET /airbnb/reservations`

**Description**: Retrieve reservations from Airbnb

**Query Parameters**:
- `start_date_from` (optional): Filter reservations starting after this date (YYYY-MM-DD)
- `start_date_to` (optional): Filter reservations starting before this date (YYYY-MM-DD)
- `status` (optional): Filter by reservation status (accepted, cancelled, pending)

**Example Request**:
```bash
curl "http://localhost:8000/airbnb/reservations?start_date_from=2024-01-01"
```

**Response Format**:
```json
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
    "number_of_guests": 2,
    "nights": 3,
    "total_paid_amount": 420.00,
    "currency": "USD",
    "created_at": "2024-02-15T14:20:00",
    "guest_details": {
      "message": "Looking forward to our stay!"
    }
  }
]
```

### 3. Booking.com Availability

**Endpoint**: `GET /booking/availability`

**Description**: Get availability information for rooms

**Query Parameters**:
- `room_number` (optional): Filter by specific room
- `from_date` (optional): Start date for availability check
- `to_date` (optional): End date for availability check

**Example Request**:
```bash
curl "http://localhost:8000/booking/availability?room_number=101&from_date=2024-03-01"
```

### 4. Airbnb Availability

**Endpoint**: `GET /airbnb/availability`

**Description**: Get calendar availability for listings

**Query Parameters**:
- `listing_id` (optional): Filter by specific listing
- `start_date` (optional): Start date for calendar
- `end_date` (optional): End date for calendar

### 5. Update Booking.com Availability

**Endpoint**: `POST /booking/update_availability`

**Description**: Update availability for Booking.com rooms

**Request Body**:
```json
{
  "room_number": "101",
  "availability": [
    {
      "date": "2024-03-01",
      "available": true,
      "price": 150.00
    }
  ]
}
```

### 6. Update Airbnb Calendar

**Endpoint**: `POST /airbnb/update_calendar`

**Description**: Update calendar availability for Airbnb listings

**Request Body**:
```json
{
  "listing_id": "listing-101",
  "calendar": [
    {
      "date": "2024-03-01",
      "available": true,
      "price": 140.00
    }
  ]
}
```

## Sample Data

The mock API includes realistic sample data:

### Booking.com Reservations (3)
1. **John Smith** - Room 101 (Deluxe Suite)
   - Check-in: 2024-02-15, Check-out: 2024-02-18
   - Total: $450.00
   
2. **Emma Wilson** - Room 205 (Ocean View Room)
   - Check-in: 2024-03-20, Check-out: 2024-03-23
   - Total: $540.00
   
3. **Michael Brown** - Room 310 (Family Suite)
   - Check-in: 2024-04-05, Check-out: 2024-04-10
   - Total: $1,250.00

### Airbnb Reservations (3)
1. **Sarah Johnson** - Room 101 (Cozy Room with Ocean View)
   - Dates: 2024-03-10 to 2024-03-13
   - Total: $420.00
   
2. **David Lee** - Room 205 (Modern Studio Apartment)
   - Dates: 2024-04-15 to 2024-04-18
   - Total: $510.00
   
3. **Jennifer Martinez** - Room 310 (Spacious Family Suite)
   - Dates: 2024-05-01 to 2024-05-07
   - Total: $1,380.00

## Integration with Odoo

### Configure Odoo to Use Mock API

1. **Set Configuration Parameter**:
   - Navigate to: Settings > Technical > Parameters > System Parameters
   - Create new parameter:
     - Key: `hotel_reservation.mock_api_endpoint`
     - Value: `http://localhost:8000`

2. **Ensure Rooms Exist in Odoo**:
   The mock API references room numbers 101, 205, and 310. Create these rooms in Odoo:
   - Go to: Hotel > Configuration > Rooms
   - Create rooms with matching room numbers

### Manual Synchronization

From the Odoo interface:

1. Navigate to: **Hotel > Reservations**
2. Click the **"Sync Booking.com"** button in the tree view header
3. Click the **"Sync Airbnb"** button in the tree view header
4. Check the results in: **Hotel > Configuration > API Synchronization**

### Automatic Synchronization (CRON Jobs)

The module includes two scheduled jobs that run every hour:

1. **Sync Booking.com Reservations**
   - CRON ID: `ir_cron_sync_booking_reservations`
   - Interval: Every 1 hour
   - Calls: `api.synchronization.sync_booking_reservations()`

2. **Sync Airbnb Reservations**
   - CRON ID: `ir_cron_sync_airbnb_reservations`
   - Interval: Every 1 hour
   - Calls: `api.synchronization.sync_airbnb_reservations()`

To manage CRON jobs:
- Navigate to: Settings > Technical > Automation > Scheduled Actions
- Search for: "Sync Booking.com" or "Sync Airbnb"
- Enable/disable or modify the schedule as needed

### View Synchronization Logs

To check synchronization results:

1. Navigate to: **Hotel > Configuration > API Synchronization**
2. View the list of sync operations with:
   - Sync name and timestamp
   - Sync type (Booking.com or Airbnb)
   - Status (success/error/pending)
   - Error messages (if any)

## How Synchronization Works

### Data Flow

```
Mock API Server (Port 8000)
          ↓
    HTTP GET Request
          ↓
api_synchronization.py (sync_booking_reservations / sync_airbnb_reservations)
          ↓
   Parse JSON Response
          ↓
Find or Create Client (hotel.client)
          ↓
Find Room by Number (hotel.room)
          ↓
Check for Existing Reservation
          ↓
Create New Reservation (hotel.reservation)
```

### Process Details

1. **Fetch Reservations**: Odoo calls the mock API endpoint with date range filters
2. **Parse Response**: JSON data is parsed to extract guest and booking information
3. **Client Management**: 
   - Search for existing client by email
   - Create new client if not found (name, email, phone)
4. **Room Matching**: 
   - Search for room by room_number field
   - Log warning if room not found
5. **Duplicate Check**: 
   - Search for existing reservation with same client, room, and dates
   - Skip if duplicate found
6. **Create Reservation**: 
   - Create new reservation with status='confirmed'
   - Set num_adults and num_children from API data
7. **Logging**: 
   - Log sync operation to api.synchronization model
   - Log detailed info to Odoo server logs

### Field Mapping

#### Booking.com → Odoo
- `reservation_id` → Used for logging only (no external_id field in Odoo model)
- `guest_name` → `hotel.client.name`
- `guest_email` → `hotel.client.email`
- `guest_phone` → `hotel.client.phone`
- `room_number` → Matched against `hotel.room.room_number`
- `check_in` → `hotel.reservation.check_in`
- `check_out` → `hotel.reservation.check_out`
- `num_adults` → `hotel.reservation.num_adults`
- `num_children` → `hotel.reservation.num_children`

#### Airbnb → Odoo
- `confirmation_code` → Used for logging only
- `guest.name` → `hotel.client.name`
- `guest.email` → `hotel.client.email`
- `guest.phone` → `hotel.client.phone`
- `listing.room_number` → Matched against `hotel.room.room_number`
- `start_date` → `hotel.reservation.check_in`
- `end_date` → `hotel.reservation.check_out`
- `number_of_guests` → `hotel.reservation.num_adults`
- `0` → `hotel.reservation.num_children` (default)

## Testing the Integration

### Step-by-Step Test

1. **Start Mock API Server**:
   ```bash
   cd "C:\Program Files\Odoo 16.0.20230101\server\odoo\addons\hotel_reservation_system\mock_api"
   uvicorn server:app --reload --port 8000
   ```

2. **Verify API is Running**:
   - Open browser: http://localhost:8000/docs
   - Test GET endpoint: http://localhost:8000/booking/reservations

3. **Configure Odoo**:
   - Settings > Technical > System Parameters
   - Create parameter: `hotel_reservation.mock_api_endpoint` = `http://localhost:8000`

4. **Create Required Rooms** (if not exists):
   - Hotel > Configuration > Rooms
   - Create: Room 101, 205, 310 with appropriate types and prices

5. **Run Manual Sync**:
   - Hotel > Reservations
   - Click "Sync Booking.com" button
   - Click "Sync Airbnb" button

6. **Verify Results**:
   - Check reservations list for new entries
   - Check clients list for new guests
   - View sync logs: Hotel > Configuration > API Synchronization

### Expected Results

After successful synchronization:
- **6 new reservations** created (3 Booking.com + 3 Airbnb)
- **6 new clients** created (if they didn't exist)
- **2 sync log entries** with status='success'
- Odoo server logs show detailed sync information

### Troubleshooting

#### Issue: "Mock API returned status code 404"
- **Cause**: Mock API server not running or wrong endpoint
- **Solution**: Verify server is running on port 8000, check system parameter value

#### Issue: "Room 101 not found in system"
- **Cause**: Referenced rooms don't exist in Odoo
- **Solution**: Create rooms 101, 205, and 310 in Hotel > Configuration > Rooms

#### Issue: "Reservation already exists, skipping"
- **Cause**: Duplicate prevention - reservation with same client, room, and dates exists
- **Solution**: This is normal behavior. Delete existing reservations to re-sync

#### Issue: Connection timeout
- **Cause**: Network issue or firewall blocking localhost connections
- **Solution**: Check Windows Firewall settings, verify port 8000 is accessible

## Customization

### Adding More Sample Data

Edit `server.py` and add entries to `BOOKING_RESERVATIONS` or `AIRBNB_RESERVATIONS` lists:

```python
BOOKING_RESERVATIONS.append({
    "reservation_id": "BK-2024-004",
    "guest_name": "Your Name",
    "guest_email": "your.email@example.com",
    # ... other fields
})
```

### Changing Server Port

To run on a different port:

```bash
uvicorn server:app --reload --port 9000
```

Update Odoo system parameter to: `http://localhost:9000`

### Adding Authentication

Modify `server.py` to add API key authentication:

```python
from fastapi import Header, HTTPException

async def verify_token(x_api_key: str = Header(...)):
    if x_api_key != "your-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@app.get("/booking/reservations", dependencies=[Depends(verify_token)])
async def get_booking_reservations(...):
    # endpoint code
```

## Production Considerations

**⚠️ IMPORTANT**: This mock API is for **DEVELOPMENT AND TESTING ONLY**.

For production deployment with real Booking.com and Airbnb APIs:

1. Replace mock endpoints with real API endpoints
2. Implement proper authentication (OAuth 2.0, API keys)
3. Add rate limiting and error handling
4. Implement webhook receivers for real-time updates
5. Add data validation and sanitization
6. Implement proper logging and monitoring
7. Use environment variables for sensitive configuration
8. Consider using a production ASGI server like Gunicorn with Uvicorn workers

### Real API Documentation

- **Booking.com Connectivity API**: https://connect.booking.com/
- **Airbnb Host API**: https://www.airbnb.com/help/article/2934

## Support

For issues or questions about the mock API:

1. Check Odoo server logs: `C:\Program Files\Odoo 16.0.20230101\server\odoo.log`
2. Check FastAPI console output for errors
3. Review sync logs in Odoo: Hotel > Configuration > API Synchronization

## License

This mock API server is part of the Hotel Reservation System module for Odoo 16.
