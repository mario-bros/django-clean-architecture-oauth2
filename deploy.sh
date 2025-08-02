#!/bin/bash
set -e

echo "🚀 Deploying Django Clean Architecture with Skaffold"
echo "=================================================="

# Check prerequisites
command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl is required but not installed. Aborting." >&2; exit 1; }
command -v skaffold >/dev/null 2>&1 || { echo "❌ skaffold is required but not installed. Aborting." >&2; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ docker is required but not installed. Aborting." >&2; exit 1; }

# Set default profile
PROFILE=${1:-development}

echo "📋 Using profile: $PROFILE"

# Check if kubectl is configured
if ! kubectl cluster-info >/dev/null 2>&1; then
    echo "❌ kubectl is not configured or cluster is not accessible"
    echo "💡 Please configure kubectl to connect to your Kubernetes cluster"
    exit 1
fi

echo "✅ Kubernetes cluster is accessible"

# Validate Skaffold configuration
echo "🔍 Validating Skaffold configuration..."
if ! skaffold config list >/dev/null 2>&1; then
    echo "❌ Skaffold configuration validation failed"
    exit 1
fi

echo "✅ Skaffold configuration is valid"

# Clean up previous deployments (optional)
if [ "$PROFILE" = "production" ]; then
    echo "🧹 Cleaning up previous production deployment..."
    kubectl delete job django-migrate django-collectstatic -n django-clean-arch --ignore-not-found=true
fi

# Deploy based on profile
case $PROFILE in
    development)
        echo "🏗️  Starting development deployment..."
        echo "💡 For hot-reload development, use: skaffold dev --profile=development --port-forward"
        echo "💡 For one-time deployment, continuing with skaffold run..."
        skaffold run --profile=development
        echo "✅ Development deployment completed"
        echo "📋 Application should be available at:"
        echo "   - Port forward manually: kubectl port-forward svc/django-clean-arch-service 8000:80 -n django-clean-arch"
        ;;
    production)
        echo "🏗️  Starting production deployment..."
        skaffold run --profile=production
        echo "✅ Production deployment completed"
        echo "📋 Application should be available at:"
        echo "   - NodePort: http://localhost:30800"
        echo "   - Ingress: http://django-clean-arch.local (if ingress controller is installed)"
        ;;
    test)
        echo "🧪 Running tests in Kubernetes..."
        skaffold run --profile=test
        ;;
    *)
        echo "❌ Unknown profile: $PROFILE"
        echo "Available profiles: development, production, test"
        exit 1
        ;;
esac

echo "🎉 Deployment completed successfully!"
