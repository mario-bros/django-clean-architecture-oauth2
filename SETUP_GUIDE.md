# Interview Demo Bundle

This directory contains a complete Django REST Framework implementation with OAuth2 authentication and Clean Architecture principles - perfect for technical interviews.

## 🚀 Quick Start for Interview

1. **Run setup script:**
   ```bash
   chmod +x interview_setup.sh
   ./interview_setup.sh
   ```

2. **Create OAuth2 application:**
   ```bash
   python oauth2_setup_helper.py
   ```

3. **Update credentials in demo script and run:**
   ```bash
   python demo_for_interviewer.py
   ```

## 📁 File Structure

```
django-drf-oauth2/
├── demo_for_interviewer.py     # Main interview demonstration script
├── oauth2_setup_helper.py      # OAuth2 application setup assistant
├── interview_setup.sh          # Automated environment setup
├── oauth2_test_complete.py     # Comprehensive testing script
├── INTERVIEW_PRESENTATION_GUIDE.md  # Presentation talking points
├── CLEAN_ARCHITECTURE_SUMMARY.md   # Architecture documentation
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management
├── src/                        # Clean Architecture implementation
│   ├── domain/                 # Business entities and rules
│   ├── application/            # Use cases and business logic
│   ├── infrastructure/         # Data access and external services
│   └── presentation/           # HTTP controllers and views
├── myapp/                      # Traditional Django implementation
└── mydrfproject/              # Django project settings
```

## 🎯 What This Demonstrates

- **OAuth2 Authentication**: Industry-standard token-based security
- **Clean Architecture**: Layered architecture with clear separation of concerns
- **API Documentation**: Interactive Swagger UI and ReDoc
- **Modern Django**: Django 4.2 with REST Framework
- **Professional Structure**: Enterprise-ready code organization

## 🔗 Key URLs

- **API Documentation**: http://127.0.0.1:8000/api/docs/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Traditional API**: http://127.0.0.1:8000/api/protected-resource/
- **Clean Architecture API**: http://127.0.0.1:8000/api/v2/protected-resource/

## 🎤 Interview Flow (15 minutes)

1. **Setup Demo** (2 min): Show project structure and run demo
2. **API Documentation** (3 min): Interactive Swagger UI exploration
3. **OAuth2 Flow** (4 min): Live authentication demonstration
4. **Architecture Comparison** (4 min): Traditional vs Clean Architecture
5. **Q&A** (2 min): Technical questions and discussion

## 📚 Additional Resources

- `CLEAN_ARCHITECTURE_SUMMARY.md` - Detailed architecture explanation
- `INTERVIEW_PRESENTATION_GUIDE.md` - Talking points and expected questions
- Server logs available in `server.log` when running

---

**Ready to impress your interviewer with modern Django development skills!** 🚀
