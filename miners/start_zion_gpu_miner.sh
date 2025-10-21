#!/bin/bash
# 🔥 ZION GPU Miner - SRBMiner Autolykos v2
# Quick launcher for GPU mining on ZION pool

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
POOL_URL="${POOL_URL:-91.98.122.165:3333}"
WALLET="${WALLET:-Z32f72f93c095d78fc8a2fe01c0f97fd4a7f6d1bcd9b251f73b18b5625be654e84}"
WORKER="${WORKER:-zion_gpu_miner}"
ALGORITHM="${ALGORITHM:-autolykos2}"

# SRBMiner paths to try
SRBMINER_PATHS=(
    "/media/maitreya/ZION1/miners/SRBMiner-Multi-2-4-9/SRBMiner-MULTI"
    "/media/maitreya/ZION1/mining/miners/SRBMiner-Multi-2-4-9/SRBMiner-MULTI"
    "./miners/SRBMiner-Multi-2-4-9/SRBMiner-MULTI"
    "SRBMiner-MULTI"
)

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║   🔥 ZION GPU MINER - Autolykos v2                   ║"
echo "║   SRBMiner Universal Mining                           ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Find SRBMiner
SRBMINER=""
for path in "${SRBMINER_PATHS[@]}"; do
    if [ -f "$path" ] && [ -x "$path" ]; then
        SRBMINER="$path"
        echo -e "${GREEN}✅ Found SRBMiner at: $SRBMINER${NC}"
        break
    fi
done

if [ -z "$SRBMINER" ]; then
    echo -e "${RED}❌ SRBMiner not found!${NC}"
    echo "Tried paths:"
    for path in "${SRBMINER_PATHS[@]}"; do
        echo "  - $path"
    done
    exit 1
fi

# Detect GPU
echo ""
echo -e "${BLUE}🎮 Detecting GPU devices...${NC}"
if command -v rocm-smi &> /dev/null; then
    echo -e "${GREEN}✅ AMD GPU detected${NC}"
    GPU_TYPE="AMD"
elif command -v nvidia-smi &> /dev/null; then
    echo -e "${GREEN}✅ NVIDIA GPU detected${NC}"
    GPU_TYPE="NVIDIA"
else
    echo -e "${YELLOW}⚠️  Could not detect GPU type${NC}"
    GPU_TYPE="AUTO"
fi

# Display configuration
echo ""
echo -e "${BLUE}⚙️  Mining Configuration:${NC}"
echo "  Pool: $POOL_URL"
echo "  Wallet: ${WALLET:0:30}..."
echo "  Worker: $WORKER"
echo "  Algorithm: $ALGORITHM"
echo "  GPU Type: $GPU_TYPE"

# Start mining
echo ""
echo -e "${GREEN}🚀 Starting SRBMiner...${NC}"
echo ""

# Build command
CMD="$SRBMINER"
CMD="$CMD --algorithm $ALGORITHM"
CMD="$CMD --pool stratum+tcp://$POOL_URL"
CMD="$CMD --wallet $WALLET"
CMD="$CMD --worker $WORKER"
CMD="$CMD --gpu-boost 3"
CMD="$CMD --intensity auto"
CMD="$CMD --api-enable"
CMD="$CMD --api-port 4444"

echo -e "${YELLOW}Command:${NC}"
echo "$CMD"
echo ""

# Execute
exec $CMD
