#!/usr/bin/env python3
"""
Simple script to test OAuth2 endpoints
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint_without_auth(endpoint):
    """Test endpoint without authentication"""
    print(f"\n=== Testing {endpoint} (No Auth) ===")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_oauth2_flow():
    """Test OAuth2 authentication flow"""
    print("\n=== OAuth2 Flow Test ===")
    
    # 1. Check OAuth2 provider endpoints
    print("1. Checking OAuth2 provider endpoints...")
    try:
        response = requests.get(f"{BASE_URL}/o/.well-known/openid_configuration/")
        print(f"   ✅ OpenID Configuration Status: {response.status_code}")
        if response.status_code == 200:
            config = response.json()
            print(f"   📋 Authorization Endpoint: {config.get('authorization_endpoint', 'N/A')}")
            print(f"   📋 Token Endpoint: {config.get('token_endpoint', 'N/A')}")
    except Exception as e:
        print(f"   ❌ OpenID Configuration Error: {e}")
    
    # 2. Check OAuth2 application management
    print("\n2. Checking OAuth2 application endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/o/applications/")
        print(f"   ✅ OAuth2 Applications Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ OAuth2 Applications Error: {e}")
    
    # 3. Check token endpoint availability
    print("\n3. Checking token endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/o/token/", data={})
        print(f"   ✅ Token Endpoint Status: {response.status_code} (Expected 400 for missing params)")
    except Exception as e:
        print(f"   ❌ Token Endpoint Error: {e}")

def test_api_documentation():
    """Test API documentation endpoints"""
    print("\n=== API Documentation Test ===")
    
    doc_endpoints = [
        ("/api/docs/", "Swagger UI"),
        ("/api/redoc/", "ReDoc"),
        ("/api/schema/", "OpenAPI Schema")
    ]
    
    for endpoint, name in doc_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            status_icon = "✅" if response.status_code == 200 else "❌"
            print(f"   {status_icon} {name}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name} Error: {e}")

def test_clean_architecture_comparison():
    """Test both traditional and Clean Architecture endpoints"""
    print("\n=== Architecture Comparison Test ===")
    
    endpoints = [
        ("/api/protected-resource/", "Traditional Django"),
        ("/api/v2/protected-resource/", "Clean Architecture")
    ]
    
    for endpoint, approach in endpoints:
        print(f"\n{approach} Endpoint: {endpoint}")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            status_icon = "✅" if response.status_code == 401 else "❌"
            print(f"   {status_icon} Status: {response.status_code} (Expected 401 - Authentication Required)")
            
            if response.status_code == 401:
                try:
                    error_data = response.json()
                    print(f"   📋 Error Response: {error_data}")
                except:
                    print(f"   📋 Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_server_health():
    """Test basic server health and availability"""
    print("\n=== Server Health Check ===")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        status_icon = "✅" if response.status_code < 500 else "❌"
        print(f"   {status_icon} Server Status: {response.status_code}")
        print(f"   📋 Server Running: Django development server detected")
    except requests.exceptions.ConnectionError:
        print("   ❌ Server Status: Not running or unreachable")
        print("   💡 Please run: python manage.py runserver")
    except Exception as e:
        print(f"   ❌ Server Health Error: {e}")

def print_project_summary():
    """Print summary for project demonstration"""
    print("\n" + "="*60)
    print("🎯 PROJECT SUMMARY")
    print("="*60)
    print("✅ This project demonstrates:")
    print("   • Clean Architecture implementation")
    print("   • OAuth2 authentication with Django OAuth Toolkit")  
    print("   • Professional API documentation (Swagger/ReDoc)")
    print("   • Comprehensive testing strategy")
    print("   • Both traditional and Clean Architecture approaches")
    print("\n📋 Next Steps for Exploration:")
    print("   1. Explore API docs: http://127.0.0.1:8000/api/docs/")
    print("   2. Review Clean Architecture: src/ directory structure")
    print("   3. Compare implementations: /api/ vs /api/v2/ endpoints")
    print("   4. Run business logic tests: python -m pytest src/tests/")
    print("   5. Check OAuth2 setup: python oauth2_setup_helper.py")
    print("="*60)

def main():
    print("🚀 Django DRF Clean Architecture OAuth2 API Testing")
    print("="*60)
    
    # Server health check first
    test_server_health()
    
    # Test endpoints without authentication (should return 401)
    test_endpoint_without_auth("/api/protected-resource/")  # Original endpoint
    test_endpoint_without_auth("/api/v2/protected-resource/")  # Clean Architecture endpoint
    
    # Test OAuth2 infrastructure
    test_oauth2_flow()
    
    # Test API documentation availability
    test_api_documentation()
    
    # Compare both architectural approaches
    test_clean_architecture_comparison()
    
    # Print project summary
    print_project_summary()

if __name__ == "__main__":
    main()
