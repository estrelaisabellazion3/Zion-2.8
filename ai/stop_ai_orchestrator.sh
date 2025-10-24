#!/bin/bash

# ZION AI Orchestrator Stop Script
# Gracefully stops all AI components

set -e

echo "🛑 Stopping ZION AI Orchestrator..."

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

# Function to stop AI component
stop_ai_component() {
    local component_name=$1
    local pid_file="$LOG_DIR/${component_name}.pid"

    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 $pid 2>/dev/null; then
            print_info "Stopping $component_name (PID: $pid)..."
            kill -TERM $pid

            # Wait for graceful shutdown
            local count=0
            while kill -0 $pid 2>/dev/null && [ $count -lt 10 ]; do
                sleep 1
                ((count++))
            done

            if kill -0 $pid 2>/dev/null; then
                print_warning "$component_name didn't stop gracefully, force killing..."
                kill -KILL $pid
                sleep 1
            fi

            if kill -0 $pid 2>/dev/null; then
                print_error "Failed to stop $component_name"
            else
                print_status "$component_name stopped successfully"
                rm -f "$pid_file"
            fi
        else
            print_warning "$component_name PID $pid not running, cleaning up"
            rm -f "$pid_file"
        fi
    else
        print_info "$component_name not running (no PID file)"
    fi
}

# Stop AI components in reverse order
print_info "Stopping AI components..."

# 1. Stop Master AI Orchestrator first
stop_ai_component "ai_orchestrator"

# 2. Stop AI Warp Engine
stop_ai_component "warp_engine"

# 3. Stop AI Pool Orchestrator
stop_ai_component "pool_orchestrator"

# 4. Stop Consciousness Mining AI
stop_ai_component "consciousness_ai"

# Check for any remaining Python processes related to AI
print_info "Checking for any remaining AI processes..."
ai_processes=$(pgrep -f "python.*ai_" || true)

if [ -n "$ai_processes" ]; then
    print_warning "Found remaining AI processes: $ai_processes"
    print_info "Force stopping remaining processes..."
    echo "$ai_processes" | xargs kill -KILL 2>/dev/null || true
fi

# Clean up PID files
print_info "Cleaning up PID files..."
rm -f "$LOG_DIR"/*.pid

# Check Redis (don't stop if other services might be using it)
if pgrep -x "redis-server" > /dev/null; then
    print_info "Redis server is still running (may be used by other services)"
fi

print_status "🎉 AI Orchestrator stopped successfully"

# Show final status
running_processes=$(pgrep -f "python.*ai_" | wc -l)
if [ $running_processes -eq 0 ]; then
    print_status "All AI components stopped"
else
    print_warning "$running_processes AI processes still running"
fi