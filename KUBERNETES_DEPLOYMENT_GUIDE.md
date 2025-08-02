# Kubernetes & Skaffold Deployment Guide

This guide explains how to deploy the Django Clean Architecture OAuth2 API using Kubernetes and Skaffold.

## 📋 Prerequisites

### Required Tools
- **Docker**: Container runtime
- **kubectl**: Kubernetes command-line tool
- **Skaffold**: Kubernetes development workflow tool
- **Kubernetes Cluster**: Local (minikube, kind, Docker Desktop) or cloud-based

### Installation Commands

#### Install kubectl
```bash
# Windows (using winget)
winget install -e --id Kubernetes.kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

#### Install Skaffold
```bash
# Windows (using winget)
winget install -e --id GoogleLLC.Skaffold

# Linux
curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64
sudo install skaffold /usr/local/bin/
```

#### Setup Local Kubernetes Cluster
```bash
# Option 1: Docker Desktop (Recommended for Windows)
# Enable Kubernetes in Docker Desktop settings

# Option 2: minikube
minikube start --driver=docker

# Option 3: kind
kind create cluster --name django-clean-arch
```

## 🏗️ Project Structure

```
django-drf-oauth2/
├── k8s/                          # Kubernetes manifests
│   ├── namespace.yaml            # Namespace definition
│   ├── configmap.yaml           # Configuration and secrets
│   ├── deployment.yaml          # Application deployment
│   ├── service.yaml             # Service definitions
│   ├── ingress.yaml             # Ingress configuration
│   └── jobs.yaml                # Migration and static file jobs
├── .github/workflows/           # GitHub Actions CI/CD
│   └── ci-cd.yml               # Complete CI/CD pipeline
├── skaffold.yaml               # Skaffold configuration
├── deploy.sh                   # Deployment script
└── cleanup.sh                  # Cleanup script
```

## 🚀 Deployment Options

### 1. Development Deployment (Hot-Reload)
```bash
# Quick start
./deploy.sh development

# Or manually
skaffold dev --profile=development --port-forward
```

**Features:**
- Hot-reload on code changes
- Port forwarding to localhost:8000
- Development Docker image
- Real-time log streaming

### 2. Production Deployment
```bash
# Quick start
./deploy.sh production

# Or manually
skaffold run --profile=production
```

**Features:**
- Production-optimized Docker image
- Database migrations
- Static file collection
- Health checks and resource limits
- Multiple replicas for high availability

### 3. Test Profile
```bash
# Run tests in Kubernetes
./deploy.sh test

# Or manually
skaffold run --profile=test
```

## 🔧 Configuration

### Environment Variables (ConfigMap)
```yaml
DEBUG: "False"
ALLOWED_HOSTS: "django-clean-arch-service,localhost,127.0.0.1"
DATABASE_URL: "sqlite:///app/db.sqlite3"
CORS_ALLOWED_ORIGINS: "http://localhost:3000,http://localhost:8080"
OAUTH2_PROVIDER_ACCESS_TOKEN_EXPIRE_SECONDS: "3600"
OAUTH2_PROVIDER_REFRESH_TOKEN_EXPIRE_SECONDS: "86400"
```

### Secrets
```yaml
SECRET_KEY: # Base64 encoded Django secret key
```

**Update secrets before production deployment:**
```bash
# Generate new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Encode in base64
echo -n "your-secret-key-here" | base64

# Update k8s/configmap.yaml with the base64 value
```

## 🌐 Accessing the Application

### Development Mode
- **API**: http://localhost:8000
- **Admin**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/api/docs/
- **OAuth2**: http://localhost:8000/o/applications/

### Production Mode
- **NodePort**: http://localhost:30800
- **Ingress**: http://django-clean-arch.local (requires ingress controller)

### Add to hosts file for ingress:
```bash
# Add this line to /etc/hosts (Linux/Mac) or C:\Windows\System32\drivers\etc\hosts (Windows)
127.0.0.1 django-clean-arch.local
```

## 📊 Monitoring & Health Checks

### Check Application Status
```bash
# Check pods
kubectl get pods -n django-clean-arch

# Check services
kubectl get services -n django-clean-arch

# Check logs
kubectl logs -f deployment/django-clean-arch -n django-clean-arch

# Check health
kubectl exec -it deployment/django-clean-arch -n django-clean-arch -- python manage.py check --deploy
```

### Resource Usage
```bash
# Check resource usage
kubectl top pods -n django-clean-arch

# Describe deployment
kubectl describe deployment django-clean-arch -n django-clean-arch
```

## 🔄 CI/CD Pipeline

The project includes a complete GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:

1. **Test Stage**: Runs unit tests, integration tests, and Django system checks
2. **Security Stage**: Performs security scans with safety and bandit
3. **Build Stage**: Builds Docker images for development and production
4. **Deploy Stage**: Validates Skaffold configuration and prepares for deployment
5. **Documentation Stage**: Generates API documentation and validates endpoints
6. **Release Stage**: Creates GitHub releases with artifacts

### Trigger CI/CD
```bash
# Push to main/master for production pipeline
git push origin main

# Push to develop for development pipeline
git push origin develop

# Create pull request for full validation
gh pr create --title "Feature update" --body "Description"
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Image Pull Errors
```bash
# Check if image exists locally
docker images | grep django-clean-arch

# Rebuild image
docker build -t django-clean-arch:latest .
```

#### 2. Pod Not Starting
```bash
# Check pod status
kubectl describe pod <pod-name> -n django-clean-arch

# Check logs
kubectl logs <pod-name> -n django-clean-arch --previous
```

#### 3. Service Not Accessible
```bash
# Check service endpoints
kubectl get endpoints -n django-clean-arch

# Port forward directly to pod
kubectl port-forward pod/<pod-name> 8000:8000 -n django-clean-arch
```

#### 4. Database Issues
```bash
# Run migrations manually
kubectl exec -it deployment/django-clean-arch -n django-clean-arch -- python manage.py migrate

# Check database
kubectl exec -it deployment/django-clean-arch -n django-clean-arch -- python manage.py dbshell
```

### Skaffold Debugging
```bash
# Validate configuration
skaffold config list

# Check schema
skaffold schema get

# Debug build
skaffold build --dry-run

# Debug deployment
skaffold deploy --dry-run
```

## 🧹 Cleanup

### Quick Cleanup
```bash
./cleanup.sh
```

### Manual Cleanup
```bash
# Delete namespace and all resources
kubectl delete namespace django-clean-arch

# Clean up Docker images
docker rmi django-clean-arch:latest django-clean-arch:dev django-clean-arch:prod
docker image prune -f
```

## 📈 Scaling

### Horizontal Pod Autoscaler
```bash
# Create HPA
kubectl autoscale deployment django-clean-arch --cpu-percent=70 --min=2 --max=10 -n django-clean-arch

# Check HPA status
kubectl get hpa -n django-clean-arch
```

### Manual Scaling
```bash
# Scale replicas
kubectl scale deployment django-clean-arch --replicas=5 -n django-clean-arch
```

## 🔐 Security Considerations

1. **Update SECRET_KEY** before production deployment
2. **Use external database** for production (PostgreSQL recommended)
3. **Configure HTTPS** with proper TLS certificates
4. **Set up RBAC** for cluster access control
5. **Use image scanning** in CI/CD pipeline
6. **Configure network policies** for pod communication
7. **Set resource limits** to prevent resource exhaustion

## 📚 Additional Resources

- [Skaffold Documentation](https://skaffold.dev/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Django OAuth Toolkit](https://django-oauth-toolkit.readthedocs.io/)
- [Clean Architecture Guide](./ARCHITECTURE_GUIDE.md)
