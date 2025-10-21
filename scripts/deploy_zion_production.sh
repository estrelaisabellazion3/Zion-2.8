#!/bin/bash
# ZION Production Deployment Script
# Deploy to SSH server with full blockchain and mining pool

SERVER="91.98.122.165"
USER="root"

echo "🚀 ZION Production Deployment to $SERVER"
echo "========================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Test connection
echo "Testing SSH connection..."
if ! ssh -o ConnectTimeout=10 $USER@$SERVER "echo 'SSH OK'" > /dev/null 2>&1; then
    print_error "SSH connection failed"
    exit 1
fi
print_status "SSH connection OK"

# Stop existing processes
echo "Stopping existing processes..."
ssh $USER@$SERVER "pkill -9 -f python; pkill -9 -f zion; sleep 3" 2>/dev/null || true
print_status "Processes stopped"

# Upload files
echo "Uploading ZION files..."
scp new_zion_blockchain.py \
    zion_universal_pool_v2.py \
    seednodes.py \
    requirements.txt \
    zion_p2p_network.py \
    zion_rpc_server.py \
    crypto_utils.py \
    $USER@$SERVER:/root/ > /dev/null 2>&1
print_status "Files uploaded"

# Install dependencies
echo "Installing dependencies..."
ssh $USER@$SERVER "pip3 install --break-system-packages -r requirements.txt" > /dev/null 2>&1
print_status "Dependencies installed"

# Clean old databases
echo "Cleaning old data..."
ssh $USER@$SERVER "rm -f *.db *.log; mkdir -p logs data" > /dev/null 2>&1
print_status "Data cleaned"

# Start blockchain
echo "Starting ZION blockchain..."
ssh $USER@$SERVER "cd /root && nohup python3 new_zion_blockchain.py > logs/blockchain.log 2>&1 &"
sleep 5

# Check if blockchain started
if ssh $USER@$SERVER "ps aux | grep new_zion_blockchain | grep -v grep" > /dev/null 2>&1; then
    print_status "Blockchain started successfully"
else
    print_error "Blockchain failed to start"
    ssh $USER@$SERVER "cat logs/blockchain.log" 2>/dev/null || true
    exit 1
fi

# Start mining pool
echo "Starting ZION mining pool..."
ssh $USER@$SERVER "cd /root && nohup python3 zion_universal_pool_v2.py > logs/pool.log 2>&1 &"
sleep 5

# Check if pool started
if ssh $USER@$SERVER "ps aux | grep zion_universal_pool | grep -v grep" > /dev/null 2>&1; then
    print_status "Mining pool started successfully"
else
    print_error "Mining pool failed to start"
    ssh $USER@$SERVER "cat logs/pool.log" 2>/dev/null || true
    exit 1
fi

# Get server info
echo ""
echo "🌐 Server Information:"
echo "======================"
ssh $USER@$SERVER "echo 'Blockchain RPC: http://$SERVER:8333'; echo 'Pool Stratum: $SERVER:3335'; echo 'Pool API: http://$SERVER:3336/api/stats'"

echo ""
print_status "🎉 ZION Production Deployment Complete!"
print_status "Blockchain and mining pool are running on $SERVER"
echo ""
echo "📋 Next steps:"
echo "1. Test blockchain: curl http://$SERVER:8333/api/status"
echo "2. Test pool: curl http://$SERVER:3336/api/stats"
echo "3. Connect miner: xmrig -o $SERVER:3335 -u YOUR_ZION_ADDRESS -p x"