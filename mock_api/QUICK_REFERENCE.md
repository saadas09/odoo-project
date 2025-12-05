# Mock API Quick Reference Card

## 🚀 Quick Start Commands

### Install Dependencies
```powershell
# Option 1: Run batch file
install_dependencies.bat

# Option 2: Manual installation
pip install -r requirements.txt
```

### Start Server
```powershell
# Option 1: Run batch file
start_server.bat

# Option 2: Manual start
uvicorn server:app --reload --port 8000
```

### Verify Installation
```powershell
python verify_installation.py
```

## 📡 API Endpoints

Base URL: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/booking/reservations` | GET | Get Booking.com reservations |
| `/airbnb/reservations` | GET | Get Airbnb reservations |
| `/booking/availability` | GET | Get room availability |
| `/airbnb/availability` | GET | Get listing availability |
| `/booking/update_availability` | POST | Update room availability |
| `/airbnb/update_calendar` | POST | Update listing calendar |
| `/docs` | GET | Interactive API documentation |

## 🔧 Odoo Configuration

### Required System Parameter
- **Key**: `hotel_reservation.mock_api_endpoint`
- **Value**: `http://localhost:8000`
- **Location**: Settings > Technical > Parameters > System Parameters

### Required Rooms
Create in: Hotel > Configuration > Rooms

| Room Number | Name | Type |
|-------------|------|------|
| 101 | Deluxe Suite | Suite |
| 205 | Ocean View Room | Standard |
| 310 | Family Suite | Family |

## 🔄 Synchronization

### Manual Sync
1. Navigate to: **Hotel > Reservations**
2. Click: **"Sync Booking.com"** or **"Sync Airbnb"**
3. Check results in: **Hotel > Configuration > API Synchronization**

### Automatic Sync (CRON)
- **Frequency**: Every 1 hour
- **Location**: Settings > Technical > Automation > Scheduled Actions
- **Jobs**: 
  - "Sync Booking.com Reservations"
  - "Sync Airbnb Reservations"

## 📊 Sample Data

### Booking.com (3 reservations)
- John Smith (Room 101) - Feb 15-18
- Emma Wilson (Room 205) - Mar 20-23
- Michael Brown (Room 310) - Apr 5-10

### Airbnb (3 reservations)
- Sarah Johnson (Room 101) - Mar 10-13
- David Lee (Room 205) - Apr 15-18
- Jennifer Martinez (Room 310) - May 1-7

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Start mock API server |
| Room not found | Create rooms 101, 205, 310 |
| Already exists | Normal - delete reservations to re-test |
| Module error | Upgrade module, clear __pycache__ |

## 📝 Testing Checklist

- [ ] Dependencies installed
- [ ] Server starts without errors
- [ ] http://localhost:8000/docs loads
- [ ] System parameter configured
- [ ] Rooms 101, 205, 310 created
- [ ] Sync buttons visible
- [ ] Manual sync creates 6 reservations
- [ ] Sync logs show success

## 📚 Documentation

- **Complete Guide**: `README.md`
- **Setup Summary**: `SETUP_SUMMARY.md`
- **Module Structure**: `../STRUCTURE.md`

## 🔗 Quick Links

- API Docs: http://localhost:8000/docs
- Odoo Reservations: http://localhost:8069/web#action=hotel_reservation_system.action_hotel_reservation
- Odoo System Params: http://localhost:8069/web#menu_id=75&action=60

## 💡 Pro Tips

1. **Keep server running** while testing Odoo sync
2. **Check logs** after each sync operation
3. **Use interactive docs** at /docs to test endpoints
4. **Modify sample data** in server.py to add more reservations
5. **Clear duplicates** by deleting reservations before re-sync

---
**Version**: 1.0.0 | **Port**: 8000 | **Protocol**: HTTP
