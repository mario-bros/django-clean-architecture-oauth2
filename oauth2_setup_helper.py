#!/usr/bin/env python3
"""
Quick OAuth2 Setup Helper
This script helps you create OAuth2 applications via Django admin interface
"""
import webbrowser
import time

def main():
    print("🔧 OAuth2 Application Setup Helper")
    print("=" * 50)
    
    print("\n📋 Step-by-step OAuth2 setup:")
    print("1. Make sure Django server is running")
    print("2. Open Django admin in browser")
    print("3. Create OAuth2 application")
    print("4. Copy credentials to demo script")
    
    # Check if user wants to open browser
    response = input("\n🌐 Open Django admin in browser? (y/n): ").lower()
    if response == 'y':
        print("🚀 Opening Django admin...")
        webbrowser.open('http://127.0.0.1:8000/admin/')
        time.sleep(2)
        webbrowser.open('http://127.0.0.1:8000/admin/oauth2_provider/application/add/')
    
    print("\n📝 OAuth2 Application Settings:")
    print("   Name: Clean Architecture Demo Client")
    print("   Client type: Confidential")
    print("   Authorization grant type: Resource owner password-based")
    print("   Skip authorization: [Leave unchecked]")
    print("   Click SAVE")
    
    print("\n📋 After creating the application:")
    print("1. Copy the generated 'Client ID'")
    print("2. Copy the generated 'Client secret'")
    print("3. Update oauth2_demo.py:")
    print("   - Replace 'YOUR_CLIENT_ID_HERE' with actual Client ID")
    print("   - Replace 'YOUR_CLIENT_SECRET_HERE' with actual Client Secret")
    
    print("\n🎯 Then run the OAuth2 demo:")
    print("   python oauth2_demo.py")
    
    print("\n✅ Ready for demonstration!")

if __name__ == "__main__":
    main()
