#!/bin/bash

# Setup script for Clean Architecture OAuth2 API with DRF-Spectacular
echo "🚀 Setting up Clean Architecture OAuth2 API with DRF-Spectacular..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser (optional - you'll be prompted)
echo "👤 Creating superuser (you can skip this by pressing Ctrl+C)..."
python manage.py createsuperuser || echo "Skipped superuser creation"

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run server: python manage.py runserver"
echo "3. Visit API docs:"
echo "   - Swagger UI: http://127.0.0.1:8000/api/docs/"
echo "   - ReDoc: http://127.0.0.1:8000/api/redoc/"
echo "   - Admin: http://127.0.0.1:8000/admin/"
echo "   - OAuth2: http://127.0.0.1:8000/o/"
echo ""
echo "🔐 OAuth2 Endpoints:"
echo "   - Original: http://127.0.0.1:8000/api/protected-resource/"
echo "   - Clean Architecture: http://127.0.0.1:8000/api/protected-resource/?resource_id=1"
