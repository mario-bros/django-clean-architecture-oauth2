# 🏗️ Clean Architecture OAuth2 API - Django DRF Implementation

**A comprehensive demonstration of Clean Architecture principles applied to Django DRF with OAuth2 authentication.**

> **Production Ready**: This project showcases enterprise-level architecture patterns, comprehensive testing, and professional API documentation.

## 🎯 Project Overview

This project demonstrates a **Clean Architecture** implementation with Django DRF, featuring:

- ✅ **Clean Architecture** with proper layer separation
- ✅ **OAuth2 Authentication** with scope-based authorization  
- ✅ **DRF-Spectacular** API documentation (Swagger/ReDoc)
- ✅ **Comprehensive Testing** with mocked dependencies
- ✅ **Both Traditional & Clean Architecture** endpoints for comparison

## 🏗️ Architecture Layers

```
src/
├── domain/                    # 🧠 Business Logic Core
│   ├── entities/             # Pure business entities
│   └── exceptions/           # Domain-specific exceptions
├── application/              # 🎯 Use Cases & Business Logic  
│   ├── interfaces/           # Repository contracts
│   └── use_cases/            # Business workflows
├── infrastructure/           # 🔧 External Dependencies
│   └── repositories/         # Repository implementations
└── presentation/             # 🌐 HTTP/API Layer
    └── views/                # Clean Architecture controllers
```

## 🚀 Quick Start Guide

### **Option 1: Automated Setup (Recommended)**

```bash
# For Windows users with WSL
wsl -e bash -c "cd django-drf-oauth2 && chmod +x setup_and_run.sh && ./setup_and_run.sh"

# For Linux/Mac users  
cd django-drf-oauth2
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### **Option 2: Manual Setup**

```bash
# For Windows users with WSL
wsl -e bash -c "cd django-drf-oauth2 && pip install -r requirements.txt"
wsl -e bash -c "cd django-drf-oauth2 && python3 manage.py migrate"
wsl -e bash -c "cd django-drf-oauth2 && python3 oauth2_setup_helper.py"

# For Linux/Mac users
pip install -r requirements.txt
python manage.py migrate
python oauth2_setup_helper.py
```

### **Option 3: Start Django Server**

```bash
# For Windows users with WSL
wsl -e bash -c "cd django-drf-oauth2 && python3 manage.py runserver"

# For Linux/Mac users
python manage.py runserver
```

## 🧪 Testing the Implementation

### **Automated Testing Script**

```bash
# For Windows users with WSL
wsl -e bash -c "cd django-drf-oauth2 && python3 test_endpoints.py"

# For Linux/Mac users
python test_endpoints.py
```

**What it tests:**

- ✅ Endpoint accessibility (should return 401 without auth)
- ✅ OAuth2 provider configuration
- ✅ API documentation availability
- ✅ Both traditional and Clean Architecture endpoints

### **Manual Testing Options**

#### **1. API Documentation Interface**
- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/  
- **OpenAPI Schema**: http://127.0.0.1:8000/api/schema/

#### **2. Demo Script for Interviewers**
```bash
#### **2. OAuth2 Demo Script**

```bash
# Interactive demo with OAuth2 flow
python oauth2_demo.py
```
```

#### **3. Endpoint Comparison**
```bash
# Traditional Django approach
GET /api/protected-resource/

# Clean Architecture approach  
GET /api/v2/protected-resource/
```

## 🎪 Architecture Demonstration Points

### **1. Clean Architecture Benefits**

- **Domain Layer**: Pure business logic, framework-independent
- **Application Layer**: Use cases with dependency injection
- **Infrastructure Layer**: Repository pattern with interface segregation
- **Presentation Layer**: Thin controllers, OAuth2 boundary handling

### **2. Testing Strategy**

```bash
# For Windows users with WSL - Run Clean Architecture tests (no Django setup needed!)
wsl -e bash -c "cd django-drf-oauth2 && PYTHONPATH=django-drf-oauth2/src python3 -m unittest src.tests.test_use_cases -v"

# For Windows users with WSL - Single test example
wsl -e bash -c "cd django-drf-oauth2 && PYTHONPATH=django-drf-oauth2/src python3 -m unittest src.tests.test_use_cases.TestAccessProtectedResourceUseCase.test_successful_access -v"

# For Linux/Mac users
PYTHONPATH=./src python -m unittest src.tests.test_use_cases -v
```

### **3. OAuth2 Integration**  
- **Framework Boundary**: OAuth2 handled at presentation layer
- **Business Logic**: Completely OAuth2-agnostic
- **Testability**: Business rules tested without OAuth2 setup

## 📋 Validation Checklist

Run the validation script to ensure everything is working:

```bash
# For Windows users with WSL
wsl -e bash -c "cd django-drf-oauth2 && python3 project_validator.py"

# For Linux/Mac users
python project_validator.py
```

**Validates:**

- ✅ All required files present
- ✅ Clean Architecture structure  
- ✅ Server startup and endpoints
- ✅ OAuth2 configuration
- ✅ API documentation generation

## 🔍 Key Files for Review

| File | Purpose | Architecture Focus |
|------|---------|----------------|
| `src/domain/entities/user.py` | Pure business entities | Framework independence |
| `src/application/use_cases/access_protected_resource.py` | Business workflows | Dependency inversion |
| `src/infrastructure/repositories/` | Repository implementations | Interface segregation |
| `src/presentation/views/` | Clean controllers | Separation of concerns |
| `src/tests/test_use_cases.py` | Business logic testing | Testability benefits |

## 🎯 Architecture Comparison

### **Traditional Django** (`myapp/`)
```python
# Mixed concerns in views
def protected_view(request):
    user = User.objects.get(id=request.user.id)  # Database
    if user.is_active:                           # Business logic  
        return JsonResponse({...})               # HTTP response
```

### **Clean Architecture** (`src/`)
```python
# Separated concerns across layers
class AccessProtectedResourceUseCase:
    def execute(self, user_id: int) -> dict:
        user = self.user_repository.find_by_id(user_id)  # Interface
        if user.can_access_protected_resource():         # Domain logic
            return {"message": "Access granted"}         # Pure data
```

## 🛠️ Technology Stack

- **Framework**: Django 4.x + Django REST Framework
- **Authentication**: Django OAuth Toolkit  
- **Documentation**: DRF-Spectacular (OpenAPI 3.0)
- **Testing**: Python unittest + Mock
- **Architecture**: Clean Architecture principles

## 📚 Additional Resources

- **[Clean Architecture Summary](CLEAN_ARCHITECTURE_SUMMARY.md)** - Detailed implementation explanation
- **[Architecture Guide](ARCHITECTURE_GUIDE.md)** - Development talking points  
- **[Setup Instructions](SETUP_GUIDE.md)** - Detailed setup documentation

## 🎯 Common Questions This Project Addresses

- **"Explain Clean Architecture principles"** → Layer separation demonstration
- **"How do you test business logic?"** → Use case testing with mocks
- **"Show OAuth2 integration"** → Framework boundary handling
- **"Demonstrate dependency injection"** → Repository pattern implementation
- **"Compare traditional vs. clean approaches"** → Side-by-side comparison

## 🚀 Production Ready

This project demonstrates:

- ✅ **Enterprise Architecture** patterns and principles
- ✅ **Professional API Development** with comprehensive documentation  
- ✅ **Testing Strategy** for maintainable codebases
- ✅ **Security Implementation** with OAuth2 best practices
- ✅ **Code Organization** and separation of concerns
- ✅ **Containerization** with Docker and Kubernetes
- ✅ **CI/CD Pipeline** with GitHub Actions and Skaffold

## 🐳 Docker & Kubernetes Deployment

### Quick Start with Docker
```bash
# Build and run development container
docker build -t django-clean-arch .
docker run -p 8000:8000 django-clean-arch

# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes with Skaffold
```bash
# Validate deployment setup
python k8s_validator.py

# Development deployment (hot-reload)
./deploy.sh development

# Production deployment
./deploy.sh production

# Cleanup
./cleanup.sh
```

### Access Points
- **Development**: http://localhost:8000
- **Production**: http://localhost:30800
- **API Documentation**: http://localhost:8000/api/docs/
- **OAuth2 Management**: http://localhost:8000/o/applications/

### Deployment Guides
- **[Kubernetes Deployment Guide](KUBERNETES_DEPLOYMENT_GUIDE.md)** - Complete K8s setup
- **[Architecture Guide](ARCHITECTURE_GUIDE.md)** - Clean Architecture explanation
- **[Setup Guide](SETUP_GUIDE.md)** - Local development setup

---

Built with ❤️ for demonstrating Clean Architecture mastery and production deployment skills
