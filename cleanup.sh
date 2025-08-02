#!/bin/bash
set -e

echo "🧹 Cleaning up Django Clean Architecture Kubernetes resources"
echo "============================================================"

NAMESPACE="django-clean-arch"

# Check if kubectl is available
command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl is required but not installed. Aborting." >&2; exit 1; }

# Check if namespace exists
if kubectl get namespace $NAMESPACE >/dev/null 2>&1; then
    echo "🔍 Found namespace: $NAMESPACE"
    
    # Delete all resources in the namespace
    echo "🗑️  Deleting all resources in namespace $NAMESPACE..."
    
    # Delete deployments
    kubectl delete deployment --all -n $NAMESPACE --ignore-not-found=true
    
    # Delete services
    kubectl delete service --all -n $NAMESPACE --ignore-not-found=true
    
    # Delete ingress
    kubectl delete ingress --all -n $NAMESPACE --ignore-not-found=true
    
    # Delete jobs
    kubectl delete job --all -n $NAMESPACE --ignore-not-found=true
    
    # Delete configmaps and secrets
    kubectl delete configmap --all -n $NAMESPACE --ignore-not-found=true
    kubectl delete secret --all -n $NAMESPACE --ignore-not-found=true
    
    # Wait a moment for resources to be cleaned up
    echo "⏳ Waiting for resources to be cleaned up..."
    sleep 5
    
    # Delete the namespace
    echo "🗑️  Deleting namespace $NAMESPACE..."
    kubectl delete namespace $NAMESPACE --ignore-not-found=true
    
    echo "✅ Cleanup completed successfully"
else
    echo "ℹ️  Namespace $NAMESPACE not found - nothing to clean up"
fi

# Clean up Docker images (optional)
read -p "🐳 Do you want to clean up Docker images as well? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Cleaning up Docker images..."
    docker rmi django-clean-arch:latest django-clean-arch:dev django-clean-arch:prod --force 2>/dev/null || true
    docker image prune -f
    echo "✅ Docker cleanup completed"
fi

echo "🎉 All cleanup tasks completed!"
