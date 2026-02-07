#!/usr/bin/env python3
"""
Simple test script to verify Django backend is working.
Run this to test your backend before starting the frontend.
"""

import requests
import time

def test_backend():
    """Test the Django backend endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Django Backend...")
    print("=" * 50)
    
    # Test 1: Health check
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Health check passed")
            print(f"   📊 Response: {response.json()}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to backend - is Django running?")
        return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 2: Test API endpoint
    try:
        print("\n2. Testing API endpoint...")
        response = requests.get(f"{base_url}/api/test/", timeout=5)
        if response.status_code == 200:
            print("   ✅ API test passed")
            print(f"   📊 Response: {response.json()}")
        else:
            print(f"   ❌ API test failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ API test error: {e}")
        return False
    
    # Test 3: Events API
    try:
        print("\n3. Testing Events API...")
        response = requests.get(f"{base_url}/api/events/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Events API working")
            print(f"   📊 Response: {response.json()}")
        else:
            print(f"   ⚠️  Events API returned: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Events API error: {e}")
    
    # Test 4: Admin interface
    try:
        print("\n4. Testing Admin interface...")
        response = requests.get(f"{base_url}/admin/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Admin interface accessible")
        else:
            print(f"   ⚠️  Admin interface returned: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Admin test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Backend testing completed!")
    return True

def check_django_running():
    """Check if Django is running on the expected port"""
    try:
        response = requests.get("http://localhost:8000/health/", timeout=2)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    print("🚀 Django Backend Test Script")
    print("Make sure Django is running on http://localhost:8000")
    print()
    
    # Check if Django is running
    if not check_django_running():
        print("❌ Django backend is not running!")
        print("Please start Django first:")
        print("   cd myticket")
        print("   python manage.py runserver")
        print()
        input("Press Enter after starting Django...")
    
    # Run tests
    test_backend()












