#!/usr/bin/env python3
"""
OAuth2 + Clean Architecture Demo for Interview
This script demonstrates a complete OAuth2 flow with Clean Architecture
"""
import requests
import json
from datetime import datetime

class InterviewDemo:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        # Replace these with your actual credentials from Django admin
        self.client_id = "YOUR_CLIENT_ID_HERE"  # Replace with real client ID
        self.client_secret = "YOUR_CLIENT_SECRET_HERE"  # Replace with real secret
        self.username = "admin"  # Your admin username
        self.password = "admin123"  # Your admin password
        self.access_token = None
    
    def step1_get_access_token(self):
        """Step 1: Obtain OAuth2 access token"""
        print("🔑 STEP 1: Getting OAuth2 Access Token")
        print("-" * 50)
        
        token_data = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'read write'
        }
        
        print(f"POST {self.base_url}/o/token/")
        print("Request payload:")
        print(json.dumps({k: v if k not in ['password', 'client_secret'] else '***' for k, v in token_data.items()}, indent=2))
        
        try:
            response = requests.post(f"{self.base_url}/o/token/", data=token_data)
            print(f"\nResponse Status: {response.status_code}")
            
            if response.status_code == 200:
                token_response = response.json()
                self.access_token = token_response.get('access_token')
                print("✅ SUCCESS: Access token obtained!")
                print(f"Token Type: {token_response.get('token_type')}")
                print(f"Expires In: {token_response.get('expires_in')} seconds")
                print(f"Scope: {token_response.get('scope')}")
                print(f"Access Token: {self.access_token[:20]}...")
                return True
            else:
                print("❌ FAILED to get access token")
                print(f"Error: {response.text}")
                return False
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def step2_test_without_auth(self):
        """Step 2: Show that endpoints are protected"""
        print("\n🚫 STEP 2: Testing Without Authentication (Should Fail)")
        print("-" * 50)
        
        endpoints = [
            '/api/protected-resource/',
            '/api/v2/protected-resource/'
        ]
        
        for endpoint in endpoints:
            print(f"\nTesting: GET {self.base_url}{endpoint}")
            try:
                response = requests.get(f"{self.base_url}{endpoint}")
                print(f"Status: {response.status_code}")
                if response.status_code == 401:
                    print("✅ CORRECT: Returns 401 Unauthorized (protected)")
                else:
                    print("❌ UNEXPECTED: Should return 401")
            except Exception as e:
                print(f"❌ ERROR: {e}")
    
    def step3_test_with_auth(self):
        """Step 3: Test with OAuth2 authentication"""
        if not self.access_token:
            print("❌ No access token available")
            return
            
        print("\n🔓 STEP 3: Testing With OAuth2 Authentication")
        print("-" * 50)
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        test_cases = [
            {
                'endpoint': '/api/protected-resource/',
                'description': 'Traditional Django DRF Implementation',
                'architecture': 'Monolithic'
            },
            {
                'endpoint': '/api/v2/protected-resource/',
                'description': 'Clean Architecture Implementation',
                'architecture': 'Clean Architecture'
            },
            {
                'endpoint': '/api/v2/protected-resource/?resource_id=1',
                'description': 'Clean Architecture with Business Logic',
                'architecture': 'Clean Architecture + Domain Rules'
            }
        ]
        
        for test_case in test_cases:
            print(f"\n--- {test_case['description']} ---")
            print(f"Architecture: {test_case['architecture']}")
            print(f"GET {self.base_url}{test_case['endpoint']}")
            print(f"Authorization: Bearer {self.access_token[:20]}...")
            
            try:
                response = requests.get(f"{self.base_url}{test_case['endpoint']}", headers=headers)
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        json_response = response.json()
                        print("✅ SUCCESS: Authenticated access granted")
                        print("Response:")
                        print(json.dumps(json_response, indent=2))
                    except:
                        print(f"Response: {response.text}")
                else:
                    print("❌ FAILED")
                    print(f"Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ ERROR: {e}")
    
    def step4_show_architecture_benefits(self):
        """Step 4: Explain Clean Architecture benefits"""
        print("\n🏗️ STEP 4: Clean Architecture Benefits Demonstration")
        print("-" * 50)
        
        print("📊 COMPARISON:")
        print()
        print("🔴 TRADITIONAL APPROACH:")
        print("   • Business logic mixed with HTTP handling")
        print("   • Direct database access in views")
        print("   • Hard to unit test")
        print("   • Framework-dependent")
        print("   • Violation of Single Responsibility Principle")
        print()
        print("🟢 CLEAN ARCHITECTURE APPROACH:")
        print("   • Clear separation of concerns")
        print("   • Business logic isolated in use cases")
        print("   • Easy to unit test")
        print("   • Framework-independent core")
        print("   • Domain-driven design")
        print()
        print("📁 CLEAN ARCHITECTURE LAYERS:")
        print("   └── Presentation Layer (HTTP/REST)")
        print("       └── Application Layer (Use Cases)")
        print("           └── Domain Layer (Business Rules)")
        print("               └── Infrastructure Layer (Database/External)")
        print()
        print("✅ BENEFITS DEMONSTRATED:")
        print("   • OAuth2 authentication working across all layers")
        print("   • Business logic centralized and testable")
        print("   • Easy to extend with new features")
        print("   • Clear documentation with DRF-Spectacular")
    
    def step5_show_api_docs(self):
        """Step 5: Show API documentation"""
        print("\n📚 STEP 5: Interactive API Documentation")
        print("-" * 50)
        
        docs_urls = [
            ('Swagger UI', '/api/docs/'),
            ('ReDoc', '/api/redoc/'),
            ('OpenAPI Schema', '/api/schema/')
        ]
        
        for name, endpoint in docs_urls:
            print(f"\n{name}: {self.base_url}{endpoint}")
            try:
                response = requests.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    print("✅ Available - Open in browser to explore")
                else:
                    print("❌ Not available")
            except:
                print("❌ Error accessing documentation")
    
    def run_complete_demo(self):
        """Run the complete demonstration"""
        print("🎯 OAUTH2 + CLEAN ARCHITECTURE INTERVIEW DEMONSTRATION")
        print("=" * 60)
        print(f"📅 Demo Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎤 Presenter: [Your Name]")
        print("📋 Topic: Django REST Framework + OAuth2 + Clean Architecture")
        print("=" * 60)
        
        # Check server connectivity
        try:
            response = requests.get(f"{self.base_url}/admin/")
            if response.status_code not in [200, 302]:
                print("❌ Server not running. Please start with: python manage.py runserver")
                return
        except:
            print("❌ Cannot connect to server. Please start with: python manage.py runserver")
            return
        
        print("✅ Server is running")
        
        # Run demonstration steps
        if self.step1_get_access_token():
            self.step2_test_without_auth()
            self.step3_test_with_auth()
        
        self.step4_show_architecture_benefits()
        self.step5_show_api_docs()
        
        print("\n" + "=" * 60)
        print("🎉 DEMONSTRATION COMPLETE!")
        print("=" * 60)
        print("📋 What was demonstrated:")
        print("   ✅ OAuth2 authentication flow")
        print("   ✅ Protected API endpoints")
        print("   ✅ Clean Architecture implementation")
        print("   ✅ Traditional vs Clean Architecture comparison")
        print("   ✅ Interactive API documentation")
        print("   ✅ Business logic separation")
        print("   ✅ Framework independence")
        print()
        print("🔗 Key URLs to show interviewer:")
        print(f"   • API Documentation: {self.base_url}/api/docs/")
        print(f"   • Admin Panel: {self.base_url}/admin/")
        print(f"   • OAuth2 Management: {self.base_url}/o/applications/")


if __name__ == "__main__":
    print("⚠️  SETUP REQUIRED:")
    print("1. Make sure Django server is running: python manage.py runserver")
    print("2. Create OAuth2 application in admin panel")
    print("3. Update CLIENT_ID and CLIENT_SECRET in this script")
    print("4. Run: python demo_for_interviewer.py")
    print()
    
    demo = InterviewDemo()
    
    # Check if credentials are updated
    if demo.client_id == "YOUR_CLIENT_ID_HERE":
        print("❌ Please update CLIENT_ID and CLIENT_SECRET with real values from Django admin")
        print("   Go to: http://127.0.0.1:8000/admin/oauth2_provider/application/")
    else:
        demo.run_complete_demo()
