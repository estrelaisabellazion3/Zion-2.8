#!/bin/bash
PROJECT_DIR="/home/zion/ZION"
VENV_DIR="$PROJECT_DIR/.venv_local"

source "$VENV_DIR/bin/activate"
export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"
export ZION_ENV="local"
export ZION_LOG_LEVEL="info"

# Create PID file
echo "" > "$PROJECT_DIR/.pids_local"

echo "🚀 Starting ZION 2.8.2 Local Services..."

# Start Blockchain
echo "[1/4] Starting Blockchain..."
cd "$PROJECT_DIR"
python3 src/core/new_zion_blockchain.py > "$PROJECT_DIR/local_logs/blockchain.log" 2>&1 &
echo $! >> "$PROJECT_DIR/.pids_local"
sleep 2

# Start Mining Pool
echo "[2/4] Starting Mining Pool (Port 3333)..."
python3 src/core/zion_universal_pool_v2.py > "$PROJECT_DIR/local_logs/pool.log" 2>&1 &
echo $! >> "$PROJECT_DIR/.pids_local"
sleep 2

# Start WARP Engine
echo "[3/4] Starting WARP Engine (Port 8080)..."
python3 src/core/zion_warp_engine_core.py > "$PROJECT_DIR/local_logs/warp.log" 2>&1 &
echo $! >> "$PROJECT_DIR/.pids_local"
sleep 2

# Start RPC Server
echo "[4/4] Starting RPC Server (Port 8545)..."
python3 src/core/zion_rpc_server.py > "$PROJECT_DIR/local_logs/rpc.log" 2>&1 &
echo $! >> "$PROJECT_DIR/.pids_local"
sleep 2

echo ""
echo "✅ All services started!"
echo ""
echo "📊 Service Status:"
ps aux | grep python3 | grep -E "new_zion|pool|warp|rpc" | grep -v grep && echo "✓ All running" || echo "⚠ Check logs"

echo ""
echo "📝 View logs:"
echo "  tail -f $PROJECT_DIR/local_logs/blockchain.log"
echo "  tail -f $PROJECT_DIR/local_logs/pool.log"
echo "  tail -f $PROJECT_DIR/local_logs/warp.log"
echo "  tail -f $PROJECT_DIR/local_logs/rpc.log"

echo ""
echo "🛑 Stop all: bash $PROJECT_DIR/local_bin/stop_all.sh"
