"""
Mock API Installation Verification Script

This script verifies that the mock API server is correctly configured and working.
"""

import sys
import requests
from datetime import datetime

def test_dependencies():
    """Test that required packages are installed"""
    print("Testing dependencies...")
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("  ✓ All dependencies installed")
        return True
    except ImportError as e:
        print(f"  ✗ Missing dependency: {e}")
        print("\nPlease run: pip install -r requirements.txt")
        return False

def test_server_running():
    """Test that the server is running"""
    print("\nTesting server connection...")
    try:
        response = requests.get("http://localhost:8000/booking/reservations", timeout=5)
        if response.status_code == 200:
            print("  ✓ Server is running and responding")
            return True
        else:
            print(f"  ✗ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("  ✗ Cannot connect to server")
        print("\nPlease start the server with: uvicorn server:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_booking_endpoint():
    """Test Booking.com endpoint"""
    print("\nTesting Booking.com endpoint...")
    try:
        response = requests.get("http://localhost:8000/booking/reservations", timeout=5)
        data = response.json()
        print(f"  ✓ Retrieved {len(data)} Booking.com reservations")
        if len(data) > 0:
            print(f"    - First reservation: {data[0]['guest_name']} (Room {data[0]['room_number']})")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_airbnb_endpoint():
    """Test Airbnb endpoint"""
    print("\nTesting Airbnb endpoint...")
    try:
        response = requests.get("http://localhost:8000/airbnb/reservations", timeout=5)
        data = response.json()
        print(f"  ✓ Retrieved {len(data)} Airbnb reservations")
        if len(data) > 0:
            print(f"    - First reservation: {data[0]['guest']['name']} (Room {data[0]['listing']['room_number']})")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_docs_endpoint():
    """Test API documentation endpoint"""
    print("\nTesting API documentation...")
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("  ✓ API documentation available at http://localhost:8000/docs")
            return True
        else:
            print(f"  ✗ Documentation returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    print("=" * 60)
    print(" Mock API Server - Installation Verification")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Test 1: Dependencies
    if not test_dependencies():
        all_passed = False
        print("\n❌ Verification failed: Missing dependencies")
        sys.exit(1)
    
    # Test 2: Server running
    if not test_server_running():
        all_passed = False
        print("\n❌ Verification failed: Server not running")
        sys.exit(1)
    
    # Test 3: Booking.com endpoint
    if not test_booking_endpoint():
        all_passed = False
    
    # Test 4: Airbnb endpoint
    if not test_airbnb_endpoint():
        all_passed = False
    
    # Test 5: Documentation
    if not test_docs_endpoint():
        all_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print(" ✅ ALL TESTS PASSED")
        print("=" * 60)
        print("\nYour mock API server is working correctly!")
        print("\nNext steps:")
        print("1. Configure Odoo system parameter:")
        print("   hotel_reservation.mock_api_endpoint = http://localhost:8000")
        print("2. Create rooms 101, 205, 310 in Odoo")
        print("3. Test synchronization from Odoo interface")
    else:
        print(" ❌ SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease fix the issues above and run this script again.")
    
    print()

if __name__ == "__main__":
    main()
