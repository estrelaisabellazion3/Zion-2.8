#!/bin/bash

# ZION Nebula Kubernetes Deployment Script
# Version: 2.8.2

set -e

echo "🚀 Deploying ZION Nebula 2.8.2 to Kubernetes..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if we're connected to a cluster
if ! kubectl cluster-info &> /dev/null; then
    print_error "Not connected to a Kubernetes cluster. Please configure kubectl."
    exit 1
fi

print_status "Connected to Kubernetes cluster: $(kubectl config current-context)"

# Create namespace
print_status "Creating namespace..."
kubectl apply -f k8s/namespace.yaml

# Deploy ConfigMaps and Secrets
print_status "Deploying configuration..."
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/monitoring-config.yaml

# Deploy PersistentVolumeClaims
print_status "Creating persistent storage..."
kubectl apply -f k8s/pvc.yaml

# Deploy database and cache
print_status "Deploying database and cache services..."
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/redis-service.yaml

# Wait for database to be ready
print_status "Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=zion-postgres -n zion-nebula --timeout=300s

# Deploy core services
print_status "Deploying ZION blockchain core services..."
kubectl apply -f k8s/zion-deployment.yaml
kubectl apply -f k8s/zion-service.yaml

# Deploy mining pool
print_status "Deploying mining pool..."
kubectl apply -f k8s/pool-deployment.yaml
kubectl apply -f k8s/pool-service.yaml

# Deploy real-time services
print_status "Deploying real-time services..."
kubectl apply -f k8s/websocket-deployment.yaml
kubectl apply -f k8s/websocket-service.yaml
kubectl apply -f k8s/dashboard-deployment.yaml
kubectl apply -f k8s/dashboard-service.yaml

# Deploy networking
print_status "Configuring networking..."
kubectl apply -f k8s/ingress.yaml

# Deploy autoscaling
print_status "Setting up autoscaling..."
kubectl apply -f k8s/hpa.yaml

# Wait for all deployments to be ready
print_status "Waiting for all services to be ready..."
kubectl wait --for=condition=ready pod -l app=zion-blockchain -n zion-nebula --timeout=300s
kubectl wait --for=condition=ready pod -l app=zion-pool -n zion-nebula --timeout=300s
kubectl wait --for=condition=ready pod -l app=zion-websocket -n zion-nebula --timeout=300s
kubectl wait --for=condition=ready pod -l app=zion-dashboard -n zion-nebula --timeout=300s

print_status "🎉 ZION Nebula 2.8.2 deployment completed successfully!"

# Show service endpoints
echo ""
print_status "Service Endpoints:"
echo "Dashboard: http://$(kubectl get svc zion-dashboard -n zion-nebula -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')"
echo "Mining Pool: $(kubectl get svc zion-pool -n zion-nebula -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'):3333"
echo "WebSocket: ws://zion-websocket.zion-nebula.svc.cluster.local:8080"

echo ""
print_status "To check deployment status: kubectl get all -n zion-nebula"
print_status "To view logs: kubectl logs -f deployment/zion-blockchain -n zion-nebula"