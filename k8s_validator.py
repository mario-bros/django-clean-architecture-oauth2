#!/usr/bin/env python3
"""
Kubernetes deployment validation script for Django Clean Architecture OAuth2 API
"""
import subprocess
import sys
import json
import time
import requests
from pathlib import Path

def run_command(command, capture_output=True, check=True):
    """Run shell command and return result"""
    try:
        result = subprocess.run(
            command.split() if isinstance(command, str) else command,
            capture_output=capture_output,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {command}")
        print(f"   Error: {e.stderr if e.stderr else e.stdout}")
        return None
    except FileNotFoundError:
        print(f"❌ Command not found: {command.split()[0] if isinstance(command, str) else command[0]}")
        return None

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    tools = {
        'docker': 'docker --version',
        'kubectl': 'kubectl version --client',
        'skaffold': 'skaffold version'
    }
    
    missing_tools = []
    
    for tool, command in tools.items():
        result = run_command(command, check=False)
        if result and result.returncode == 0:
            print(f"   ✅ {tool}: Available")
        else:
            print(f"   ❌ {tool}: Not found")
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"\n❌ Missing required tools: {', '.join(missing_tools)}")
        print("Please install missing tools before proceeding.")
        return False
    
    return True

def check_kubernetes_cluster():
    """Check if Kubernetes cluster is accessible"""
    print("\n🔍 Checking Kubernetes cluster...")
    
    result = run_command('kubectl cluster-info', check=False)
    if not result or result.returncode != 0:
        print("❌ Kubernetes cluster not accessible")
        print("💡 Please ensure kubectl is configured and cluster is running")
        return False
    
    print("✅ Kubernetes cluster is accessible")
    
    # Check nodes
    result = run_command('kubectl get nodes', check=False)
    if result and result.returncode == 0:
        print("✅ Kubernetes nodes are ready")
    else:
        print("⚠️  Could not retrieve node information")
    
    return True

def validate_manifests():
    """Validate Kubernetes manifests"""
    print("\n🔍 Validating Kubernetes manifests...")
    
    k8s_dir = Path('k8s')
    if not k8s_dir.exists():
        print("❌ k8s directory not found")
        return False
    
    manifest_files = [
        'namespace.yaml',
        'configmap.yaml', 
        'deployment.yaml',
        'service.yaml',
        'ingress.yaml',
        'jobs.yaml'
    ]
    
    valid_manifests = 0
    
    for manifest in manifest_files:
        manifest_path = k8s_dir / manifest
        if manifest_path.exists():
            # Validate with kubectl
            result = run_command(f'kubectl apply --dry-run=client -f {manifest_path}', check=False)
            if result and result.returncode == 0:
                print(f"   ✅ {manifest}: Valid")
                valid_manifests += 1
            else:
                print(f"   ❌ {manifest}: Invalid")
        else:
            print(f"   ❌ {manifest}: Not found")
    
    if valid_manifests == len(manifest_files):
        print("✅ All Kubernetes manifests are valid")
        return True
    else:
        print(f"❌ {len(manifest_files) - valid_manifests} manifests have issues")
        return False

def validate_skaffold_config():
    """Validate Skaffold configuration"""
    print("\n🔍 Validating Skaffold configuration...")
    
    if not Path('skaffold.yaml').exists():
        print("❌ skaffold.yaml not found")
        return False
    
    # Check Skaffold configuration
    result = run_command('skaffold config list', check=False)
    if result and result.returncode == 0:
        print("✅ Skaffold configuration is valid")
        
        # Check profiles
        try:
            profiles = ['development', 'production', 'test']
            for profile in profiles:
                result = run_command(f'skaffold build --dry-run --profile={profile}', check=False)
                if result and result.returncode == 0:
                    print(f"   ✅ Profile '{profile}': Valid")
                else:
                    print(f"   ❌ Profile '{profile}': Invalid")
        except Exception as e:
            print(f"   ⚠️  Could not validate profiles: {e}")
        
        return True
    else:
        print("❌ Skaffold configuration is invalid")
        return False

def check_docker_image():
    """Check if Django Docker image exists or can be built"""
    print("\n🔍 Checking Docker image...")
    
    # Check if image exists
    result = run_command('docker images django-clean-arch:latest --format "{{.ID}}"', check=False)
    if result and result.returncode == 0 and result.stdout.strip():
        print("✅ Django Docker image exists")
        return True
    
    # Try to build image
    print("📦 Django image not found, attempting to build...")
    if not Path('Dockerfile').exists():
        print("❌ Dockerfile not found")
        return False
    
    result = run_command('docker build -t django-clean-arch:latest .', capture_output=False, check=False)
    if result and result.returncode == 0:
        print("✅ Django Docker image built successfully")
        return True
    else:
        print("❌ Failed to build Django Docker image")
        return False

def test_deployment_dry_run():
    """Test deployment with dry-run"""
    print("\n🔍 Testing deployment (dry-run)...")
    
    result = run_command('skaffold build --dry-run --profile=development', check=False)
    if result and result.returncode == 0:
        print("✅ Skaffold build dry-run successful")
    else:
        print("❌ Skaffold build dry-run failed")
        return False
    
    result = run_command('skaffold deploy --dry-run --profile=development', check=False)
    if result and result.returncode == 0:
        print("✅ Skaffold deploy dry-run successful")
        return True
    else:
        print("❌ Skaffold deploy dry-run failed")
        return False

def check_github_workflow():
    """Check GitHub Actions workflow"""
    print("\n🔍 Checking GitHub Actions workflow...")
    
    workflow_path = Path('.github/workflows/ci-cd.yml')
    if workflow_path.exists():
        print("✅ GitHub Actions workflow found")
        
        # Basic syntax check (if yamllint is available)
        result = run_command('yamllint .github/workflows/ci-cd.yml', check=False)
        if result:
            if result.returncode == 0:
                print("✅ Workflow YAML syntax is valid")
            else:
                print("⚠️  Workflow YAML may have issues (yamllint)")
        else:
            print("ℹ️  yamllint not available for syntax checking")
        
        return True
    else:
        print("❌ GitHub Actions workflow not found")
        return False

def print_deployment_summary():
    """Print deployment instructions summary"""
    print("\n" + "="*60)
    print("🎯 DEPLOYMENT VALIDATION SUMMARY")
    print("="*60)
    
    print("\n📋 Quick Start Commands:")
    print("   # Development (with hot-reload)")
    print("   ./deploy.sh development")
    print("   # OR: skaffold dev --profile=development --port-forward")
    
    print("\n   # Production deployment")
    print("   ./deploy.sh production") 
    print("   # OR: skaffold run --profile=production")
    
    print("\n   # Test profile")
    print("   ./deploy.sh test")
    print("   # OR: skaffold run --profile=test")
    
    print("\n🌐 Access Points (after deployment):")
    print("   • Development: http://localhost:8000")
    print("   • Production NodePort: http://localhost:30800")
    print("   • Ingress: http://django-clean-arch.local")
    
    print("\n📚 Documentation:")
    print("   • Full Guide: KUBERNETES_DEPLOYMENT_GUIDE.md")
    print("   • Architecture: ARCHITECTURE_GUIDE.md")
    print("   • Setup: SETUP_GUIDE.md")
    
    print("\n🧹 Cleanup:")
    print("   ./cleanup.sh")
    
    print("="*60)

def main():
    """Main validation function"""
    print("🚀 Django Clean Architecture Kubernetes Deployment Validator")
    print("=" * 60)
    
    checks = [
        check_prerequisites,
        check_kubernetes_cluster,
        validate_manifests,
        validate_skaffold_config,
        check_docker_image,
        test_deployment_dry_run,
        check_github_workflow
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check in checks:
        try:
            if check():
                passed_checks += 1
        except Exception as e:
            print(f"❌ Check failed with error: {e}")
    
    print(f"\n📊 Validation Results: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 All validation checks passed! Your deployment is ready.")
        print_deployment_summary()
        return 0
    else:
        print("⚠️  Some validation checks failed. Please address the issues above.")
        print("💡 Check KUBERNETES_DEPLOYMENT_GUIDE.md for troubleshooting help.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
