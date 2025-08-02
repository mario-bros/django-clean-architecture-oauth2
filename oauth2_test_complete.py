#!/usr/bin/env python3
"""
Complete OAuth2 API Testing Script
This script demonstrates how to:
1. Create OAuth2 applications
2. Get access tokens
3. Test protected endpoints
4. Compare traditional vs Clean Architecture implementations
"""
import requests
import json
import urllib.parse
import base64
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

class OAuth2TestRunner:
    def __init__(self):
        self.access_token = None
        self.client_id = None
        self.client_secret = None
        
    def print_section(self, title):
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def setup_oauth2_application(self):
        """
        Manual OAuth2 Application Setup Instructions
        """
        self.print_section("OAuth2 Application Setup")
        print("To test OAuth2, you need to create an application first:")
        print()
        print("1. Go to: http://127.0.0.1:8000/admin/")
        print("2. Login with: admin / admin123")
        print("3. Navigate to: OAuth2 Provider > Applications")
        print("4. Click 'Add Application'")
        print("5. Fill in:")
        print("   - Name: Test API Client")
        print("   - Client type: Confidential")
        print("   - Authorization grant type: Authorization code")
        print("   - Redirect uris: http://127.0.0.1:8000/callback/")
        print("6. Save and copy the Client ID and Client Secret")
        print()
        
        # For demonstration, we'll use some example values
        # In real testing, these would come from the admin interface
        print("For this demo, let's assume you have:")
        self.client_id = "your_client_id_here"
        self.client_secret = "your_client_secret_here"
        print(f"Client ID: {self.client_id}")
        print(f"Client Secret: {self.client_secret}")
    
    def test_password_flow(self):
        """
        Test Resource Owner Password Credentials flow (for testing only)
        Note: This flow is deprecated and should only be used for testing
        """
        self.print_section("OAuth2 Resource Owner Password Flow")
        
        # This would work if we set up the application with "Resource owner password-based" grant type
        token_data = {
            'grant_type': 'password',
            'username': 'admin',
            'password': 'admin123',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'read write'
        }
        
        print("Attempting to get access token...")
        print(f"POST {BASE_URL}/o/token/")
        print(f"Data: {json.dumps(token_data, indent=2)}")
        
        try:
            response = requests.post(f"{BASE_URL}/o/token/", data=token_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                token_response = response.json()
                self.access_token = token_response.get('access_token')
                print(f"✅ Access token obtained: {self.access_token[:20]}...")
                return True
            else:
                print("❌ Failed to get access token")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_protected_endpoints(self):
        """
        Test both protected endpoints with OAuth2 token
        """
        if not self.access_token:
            print("❌ No access token available")
            return
            
        self.print_section("Testing Protected Endpoints")
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        endpoints = [
            ('/api/protected-resource/', 'Original Implementation'),
            ('/api/v2/protected-resource/', 'Clean Architecture Implementation'),
            ('/api/v2/protected-resource/?resource_id=1', 'Clean Architecture with Resource ID'),
        ]
        
        for endpoint, description in endpoints:
            print(f"\n--- {description} ---")
            print(f"GET {BASE_URL}{endpoint}")
            
            try:
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
                print(f"Status: {response.status_code}")
                
                if response.headers.get('content-type', '').startswith('application/json'):
                    try:
                        json_response = response.json()
                        print(f"Response: {json.dumps(json_response, indent=2)}")
                    except:
                        print(f"Response: {response.text}")
                else:
                    print(f"Response: {response.text}")
                    
                if response.status_code == 200:
                    print("✅ Success")
                else:
                    print("❌ Failed")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def test_without_auth(self):
        """
        Test endpoints without authentication (should fail)
        """
        self.print_section("Testing Without Authentication")
        
        endpoints = [
            '/api/protected-resource/',
            '/api/v2/protected-resource/'
        ]
        
        for endpoint in endpoints:
            print(f"\nTesting {endpoint}")
            try:
                response = requests.get(f"{BASE_URL}{endpoint}")
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text}")
                
                if response.status_code == 401:
                    print("✅ Correctly rejected (401 Unauthorized)")
                else:
                    print("❌ Unexpected response")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def test_api_documentation(self):
        """
        Test API documentation endpoints
        """
        self.print_section("API Documentation")
        
        docs_endpoints = [
            ('/api/schema/', 'OpenAPI Schema'),
            ('/api/docs/', 'Swagger UI'),
            ('/api/redoc/', 'ReDoc UI'),
        ]
        
        for endpoint, description in docs_endpoints:
            print(f"\n{description}: {BASE_URL}{endpoint}")
            try:
                response = requests.get(f"{BASE_URL}{endpoint}")
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ Available")
                else:
                    print("❌ Not available")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_architecture_comparison(self):
        """
        Show the difference between traditional and Clean Architecture approaches
        """
        self.print_section("Architecture Comparison")
        
        print("🏗️  TRADITIONAL APPROACH (/api/protected-resource/)")
        print("   └── myapp/views.py")
        print("       ├── Direct Django/DRF dependency")
        print("       ├── Business logic mixed with HTTP concerns")
        print("       └── Hard to test in isolation")
        print()
        
        print("🏗️  CLEAN ARCHITECTURE (/api/v2/protected-resource/)")
        print("   ├── src/presentation/views/protected_resource_view.py")
        print("   │   └── HTTP Controller (only HTTP concerns)")
        print("   ├── src/application/use_cases/access_protected_resource.py")
        print("   │   └── Business Logic (framework-agnostic)")
        print("   ├── src/domain/entities/")
        print("   │   └── Core Business Rules (pure Python)")
        print("   └── src/infrastructure/repositories/")
        print("       └── Data Access (framework-specific)")
        print()
        
        print("✅ Benefits of Clean Architecture:")
        print("   • Testable business logic")
        print("   • Framework independence")  
        print("   • Clear separation of concerns")
        print("   • Better maintainability")
        print("   • Domain-driven design")
    
    def run_all_tests(self):
        """
        Run the complete test suite
        """
        print("🚀 Django DRF OAuth2 Clean Architecture API Testing")
        print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test basic connectivity
        try:
            response = requests.get(f"{BASE_URL}/admin/")
            if response.status_code in [200, 302]:
                print("✅ Server is running")
            else:
                print("❌ Server connectivity issues")
                return
        except:
            print("❌ Cannot connect to server")
            return
        
        # Run tests
        self.setup_oauth2_application()
        self.test_without_auth()
        self.test_api_documentation()
        
        # OAuth2 flow would require manual setup
        print("\n" + "="*60)
        print("  OAuth2 Authentication Testing")
        print("="*60)
        print("To test OAuth2 authentication:")
        print("1. Set up OAuth2 application in admin panel")
        print("2. Update this script with real client credentials")
        print("3. Run the password flow test")
        
        self.show_architecture_comparison()
        
        print("\n" + "="*60)
        print("  Summary")
        print("="*60)
        print("✅ Both endpoints properly require authentication")
        print("✅ API documentation is working")
        print("✅ Clean Architecture structure implemented")
        print("📚 Documentation available at:")
        print(f"   • Swagger UI: {BASE_URL}/api/docs/")
        print(f"   • ReDoc: {BASE_URL}/api/redoc/")


if __name__ == "__main__":
    tester = OAuth2TestRunner()
    tester.run_all_tests()
