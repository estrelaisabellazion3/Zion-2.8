#!/bin/bash

# ZION AI Orchestrator Startup Script
# Launches all AI components for ZION Nebula 2.8.2

set -e

echo "🤖 Starting ZION AI Orchestrator..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
AI_DIR="$PROJECT_ROOT/ai"
LOG_DIR="$PROJECT_ROOT/logs"

# Create log directory
mkdir -p "$LOG_DIR"

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

print_info() {
    echo -e "${BLUE}[AI]${NC} $1"
}

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Redis is running
if ! pgrep -x "redis-server" > /dev/null; then
    print_warning "Redis server is not running. Starting Redis..."
    if command -v redis-server &> /dev/null; then
        redis-server --daemonize yes
        sleep 2
        print_status "Redis server started"
    else
        print_error "Redis server is not installed. Please install Redis first."
        exit 1
    fi
fi

# Install AI dependencies if needed
print_info "Checking AI dependencies..."
if [ ! -f "$AI_DIR/requirements-ai.txt" ]; then
    print_error "AI requirements file not found: $AI_DIR/requirements-ai.txt"
    exit 1
fi

# Check if virtual environment exists
VENV_DIR="$AI_DIR/venv"
if [ ! -d "$VENV_DIR" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install/update dependencies
print_info "Installing AI dependencies..."
pip install --quiet -r "$AI_DIR/requirements-ai.txt"

# Function to start AI component
start_ai_component() {
    local component_name=$1
    local script_name=$2
    local log_file="$LOG_DIR/${component_name}.log"

    print_info "Starting $component_name..."

    if [ -f "$AI_DIR/$script_name" ]; then
        # Start component in background
        nohup python3 "$AI_DIR/$script_name" >> "$log_file" 2>&1 &
        local pid=$!

        # Wait a moment and check if process is still running
        sleep 2
        if kill -0 $pid 2>/dev/null; then
            print_status "$component_name started successfully (PID: $pid)"
            echo $pid > "$LOG_DIR/${component_name}.pid"
        else
            print_error "$component_name failed to start. Check logs: $log_file"
            return 1
        fi
    else
        print_error "Script not found: $AI_DIR/$script_name"
        return 1
    fi
}

# Start AI components in order
print_info "Launching AI components..."

# 1. Start Consciousness Mining AI
start_ai_component "consciousness_ai" "consciousness_mining_ai.py"

# 2. Start AI Pool Orchestrator
start_ai_component "pool_orchestrator" "ai_pool_orchestrator.py"

# 3. Start AI Warp Engine
start_ai_component "warp_engine" "ai_warp_engine.py"

# 4. Start Master AI Orchestrator
start_ai_component "ai_orchestrator" "ai_orchestrator.py"

# Wait for all components to initialize
print_info "Waiting for AI components to initialize..."
sleep 5

# Check if all components are running
running_components=0
total_components=4

for component in consciousness_ai pool_orchestrator warp_engine ai_orchestrator; do
    if [ -f "$LOG_DIR/${component}.pid" ]; then
        pid=$(cat "$LOG_DIR/${component}.pid")
        if kill -0 $pid 2>/dev/null; then
            ((running_components++))
        fi
    fi
done

if [ $running_components -eq $total_components ]; then
    print_status "🎉 All AI components started successfully!"
    print_status "AI Orchestrator is now running with $running_components active components"
    print_info "Monitor logs in: $LOG_DIR"
    print_info "To stop AI components, run: $SCRIPT_DIR/stop_ai.sh"
else
    print_warning "Only $running_components out of $total_components AI components started successfully"
    print_info "Check logs in: $LOG_DIR for details"
fi

# Keep script running to show status
print_info "AI Orchestrator is running. Press Ctrl+C to stop..."

# Status monitoring loop
while true; do
    sleep 30

    # Check component health
    healthy_components=0
    for component in consciousness_ai pool_orchestrator warp_engine ai_orchestrator; do
        if [ -f "$LOG_DIR/${component}.pid" ]; then
            pid=$(cat "$LOG_DIR/${component}.pid")
            if kill -0 $pid 2>/dev/null; then
                ((healthy_components++))
            fi
        fi
    done

    if [ $healthy_components -lt $total_components ]; then
        print_warning "Component health check: $healthy_components/$total_components healthy"
    fi
done