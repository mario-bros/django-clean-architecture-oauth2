#!/usr/bin/env python3
"""
Project Validator
Validates that all components are ready for demonstration
"""
import os
import sys
import requests
from pathlib import Path

class ProjectValidator:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.errors = []
        self.warnings = []
        
    def check_files(self):
        """Check that all required files exist"""
        print("📁 Checking required files...")
        
        required_files = [
            "manage.py",
            "requirements.txt",
            "oauth2_demo.py",
            "oauth2_setup_helper.py",
            "project_setup.sh",
            "SETUP_GUIDE.md",
            "ARCHITECTURE_GUIDE.md",
            "CLEAN_ARCHITECTURE_SUMMARY.md"
        ]
        
        for file in required_files:
            if os.path.exists(file):
                print(f"   ✅ {file}")
            else:
                print(f"   ❌ {file}")
                self.errors.append(f"Missing file: {file}")
        
        # Check src structure
        src_dirs = [
            "src/domain/entities",
            "src/application/use_cases",
            "src/infrastructure/repositories", 
            "src/presentation/views"
        ]
        
        for dir_path in src_dirs:
            if os.path.exists(dir_path):
                print(f"   ✅ {dir_path}/")
            else:
                print(f"   ❌ {dir_path}/")
                self.errors.append(f"Missing directory: {dir_path}")
    
    def check_server(self):
        """Check if Django server is running"""
        print("\n🌐 Checking Django server...")
        
        try:
            response = requests.get(f"{self.base_url}/admin/", timeout=5)
            if response.status_code in [200, 302]:
                print("   ✅ Server is running")
                return True
            else:
                print(f"   ❌ Server returned status {response.status_code}")
                self.warnings.append("Server is not responding correctly")
                return False
        except requests.exceptions.ConnectionError:
            print("   ⚠️  Server is not running")
            self.warnings.append("Server is not running - run 'python manage.py runserver'")
            return False
        except Exception as e:
            print(f"   ❌ Error checking server: {e}")
            self.errors.append(f"Server check error: {e}")
            return False
    
    def check_endpoints(self):
        """Check API endpoints"""
        print("\n🔗 Checking API endpoints...")
        
        endpoints = [
            "/api/protected-resource/",
            "/api/v2/protected-resource/",
            "/api/docs/",
            "/api/redoc/",
            "/api/schema/"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                if endpoint in ["/api/protected-resource/", "/api/v2/protected-resource/"]:
                    # These should return 401 (unauthorized)
                    if response.status_code == 401:
                        print(f"   ✅ {endpoint} (correctly protected)")
                    else:
                        print(f"   ⚠️  {endpoint} (status: {response.status_code})")
                        self.warnings.append(f"{endpoint} should return 401 Unauthorized")
                else:
                    # Documentation endpoints should return 200
                    if response.status_code == 200:
                        print(f"   ✅ {endpoint}")
                    else:
                        print(f"   ❌ {endpoint} (status: {response.status_code})")
                        self.errors.append(f"{endpoint} not accessible")
            except requests.exceptions.ConnectionError:
                print(f"   ⚠️  {endpoint} (server not running)")
            except Exception as e:
                print(f"   ❌ {endpoint} (error: {e})")
                self.errors.append(f"Error checking {endpoint}: {e}")
    
    def check_demo_script(self):
        """Check if demo script has been configured"""
        print("\n🎯 Checking demo script configuration...")
        
        try:
            with open("oauth2_demo.py", "r") as f:
                content = f.read()
                
            if "YOUR_CLIENT_ID_HERE" in content:
                print("   ⚠️  Client ID not configured")
                self.warnings.append("Update CLIENT_ID in oauth2_demo.py")
            else:
                print("   ✅ Client ID configured")
                
            if "YOUR_CLIENT_SECRET_HERE" in content:
                print("   ⚠️  Client Secret not configured")
                self.warnings.append("Update CLIENT_SECRET in oauth2_demo.py")
            else:
                print("   ✅ Client Secret configured")
                
        except FileNotFoundError:
            print("   ❌ oauth2_demo.py not found")
            self.errors.append("Demo script missing")
        except Exception as e:
            print(f"   ❌ Error checking demo script: {e}")
            self.errors.append(f"Demo script check error: {e}")
    
    def check_dependencies(self):
        """Check Python dependencies"""
        print("\n📦 Checking Python dependencies...")
        
        required_packages = [
            ("django", "django"),
            ("djangorestframework", "rest_framework"), 
            ("django-oauth-toolkit", "oauth2_provider"),
            ("drf-spectacular", "drf_spectacular"),
            ("requests", "requests")
        ]
        
        for package_name, import_name in required_packages:
            try:
                __import__(import_name)
                print(f"   ✅ {package_name}")
            except ImportError:
                print(f"   ❌ {package_name}")
                self.errors.append(f"Missing package: {package_name}")
    
    def generate_report(self):
        """Generate validation report"""
        print("\n" + "="*60)
        print("📋 PROJECT VALIDATION REPORT")
        print("="*60)
        
        if not self.errors and not self.warnings:
            print("🎉 ALL CHECKS PASSED!")
            print("✅ Your project bundle is ready!")
            print("\n🚀 To run the demo:")
            print("   1. Make sure server is running: python manage.py runserver")
            print("   2. Set up OAuth2 app: python oauth2_setup_helper.py")
            print("   3. Run demo: python oauth2_demo.py")
            return True
        
        if self.errors:
            print(f"❌ ERRORS FOUND ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.errors:
            print("\n❌ Please fix errors before proceeding")
            return False
        else:
            print("\n⚠️  You can proceed, but consider addressing warnings")
            return True
    
    def run_validation(self):
        """Run complete validation"""
        print("🔍 VALIDATING PROJECT BUNDLE")
        print("="*40)
        
        self.check_files()
        self.check_dependencies()
        server_running = self.check_server()
        
        if server_running:
            self.check_endpoints()
        
        self.check_demo_script()
        
        return self.generate_report()

if __name__ == "__main__":
    validator = ProjectValidator()
    success = validator.run_validation()
    
    if success:
        print("\n🎤 READY FOR DEMONSTRATION!")
        sys.exit(0)
    else:
        print("\n❌ NOT READY - Please fix issues above")
        sys.exit(1)
