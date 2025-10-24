#!/bin/bash
# ZION Docker Build Script
# Builds all Docker images for ZION 2.8.2 Nebula

set -e

echo "🏗️  Building ZION 2.8.2 Nebula Docker Images..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

print_status "Working directory: $PROJECT_ROOT"

# Build ZQAL SDK image
print_status "Building ZQAL SDK image..."
if docker build -f docker/Dockerfile.zqal-sdk -t zion/zqal-sdk:latest .; then
    print_success "ZQAL SDK image built successfully"
else
    print_error "Failed to build ZQAL SDK image"
    exit 1
fi

# Build ZION Node image
print_status "Building ZION Node image..."
if docker build -f docker/Dockerfile.zion-node -t zion/zion-node:latest .; then
    print_success "ZION Node image built successfully"
else
    print_error "Failed to build ZION Node image"
    exit 1
fi

# Build Mining Pool image
print_status "Building Mining Pool image..."
if docker build -f docker/Dockerfile.mining-pool -t zion/mining-pool:latest .; then
    print_success "Mining Pool image built successfully"
else
    print_error "Failed to build Mining Pool image"
    exit 1
fi

# Build Rainbow Bridge image
print_status "Building Rainbow Bridge image..."
if docker build -f docker/Dockerfile.rainbow-bridge -t zion/rainbow-bridge:latest .; then
    print_success "Rainbow Bridge image built successfully"
else
    print_error "Failed to build Rainbow Bridge image"
    exit 1
fi

print_success "All Docker images built successfully!"

# Show built images
print_status "Built images:"
docker images | grep zion/

# Instructions for running
echo ""
print_status "To start the ZION Nebula stack:"
echo "  cd docker"
echo "  docker-compose -f docker-compose.zqal.yml up -d"
echo ""
print_status "To view logs:"
echo "  docker-compose -f docker-compose.zqal.yml logs -f"
echo ""
print_status "To stop the stack:"
echo "  docker-compose -f docker-compose.zqal.yml down"
echo ""
print_status "Web monitor will be available at: http://localhost"
print_status "WebSocket server at: ws://localhost:8080"
print_status "Socket.IO server at: http://localhost:8081"