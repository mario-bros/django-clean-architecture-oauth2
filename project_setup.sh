#!/bin/bash
echo "🎯 Setting up OAuth2 + Clean Architecture Demo for Interview"
echo "=========================================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the Django project root directory"
    echo "   Expected: manage.py file should be present"
    exit 1
fi

echo "📍 Current directory: $(pwd)"
echo "✅ Found Django project"

# Check Python and dependencies
echo ""
echo "🔍 Checking Python environment..."
python3 --version
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo ""
echo "🗄️ Running database migrations..."
python manage.py migrate

# Check if server is already running
echo ""
echo "🔍 Checking if server is already running..."
if curl -s http://127.0.0.1:8000/admin/ > /dev/null 2>&1; then
    echo "✅ Server is already running"
    SERVER_RUNNING=true
else
    echo "🚀 Starting Django server..."
    python manage.py runserver > server.log 2>&1 &
    SERVER_PID=$!
    echo "✅ Server started with PID: $SERVER_PID"
    
    # Wait for server to start
    echo "⏳ Waiting for server to start..."
    sleep 5
    
    # Check if server started successfully
    if curl -s http://127.0.0.1:8000/admin/ > /dev/null 2>&1; then
        echo "✅ Server is now running"
        SERVER_RUNNING=true
    else
        echo "❌ Server failed to start. Check server.log for details"
        SERVER_RUNNING=false
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps for interview demo:"
echo "1. Open browser: http://127.0.0.1:8000/admin/"
echo "2. Login with admin credentials (username: admin, password: admin123)"
echo "3. Go to: DJANGO OAUTH TOOLKIT > Applications > Add Application"
echo "4. Create application with these settings:"
echo "   - Name: Interview Demo Client"
echo "   - Client type: Confidential"
echo "   - Authorization grant type: Resource owner password-based"
echo "   - Click SAVE"
echo "5. Copy the generated Client ID and Client Secret"
echo "6. Update demo_for_interviewer.py with your real credentials:"
echo "   - Replace 'YOUR_CLIENT_ID_HERE' with actual Client ID"
echo "   - Replace 'YOUR_CLIENT_SECRET_HERE' with actual Client Secret"
echo "7. Run: python demo_for_interviewer.py"
echo ""
echo "🔗 Key URLs to show interviewer:"
echo "   • Swagger UI: http://127.0.0.1:8000/api/docs/"
echo "   • ReDoc: http://127.0.0.1:8000/api/redoc/"
echo "   • Admin Panel: http://127.0.0.1:8000/admin/"
echo "   • OAuth2 Apps: http://127.0.0.1:8000/admin/oauth2_provider/application/"
echo ""

if [ "$SERVER_RUNNING" = true ] && [ -n "$SERVER_PID" ]; then
    echo "📝 To stop server later: kill $SERVER_PID"
    echo "📋 Server log: tail -f server.log"
fi

echo ""
echo "🎤 Interview Demo Tips:"
echo "   • Show the API documentation first (Swagger UI)"
echo "   • Demonstrate authentication flow with real tokens"
echo "   • Compare traditional vs Clean Architecture endpoints"
echo "   • Explain the layered architecture structure"
echo "   • Highlight testing and maintainability benefits"
echo ""
echo "✅ Ready for interview demonstration!"
