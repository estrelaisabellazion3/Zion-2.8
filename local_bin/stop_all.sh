#!/bin/bash
PROJECT_DIR="/home/zion/ZION"
echo "Stopping ZION 2.8.2 services..."
if [ -f "$PROJECT_DIR/.pids_local" ]; then
    while read pid; do
        kill $pid 2>/dev/null || true
    done < "$PROJECT_DIR/.pids_local"
    rm "$PROJECT_DIR/.pids_local"
    echo "✓ All services stopped"
else
    pkill -f "python3.*new_zion\|python3.*pool\|python3.*warp\|python3.*rpc" 2>/dev/null || true
    echo "✓ Services killed"
fi
