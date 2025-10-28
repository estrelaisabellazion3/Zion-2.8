# 🚀 ZION 2.8.2 Nebula - Complete Deployment Guide

**Version:** 2.8.2 Nebula  
**Date:** October 28, 2025  
**Status:** ✅ Production Ready

---

## Table of Contents

1. [Quick Start (5 minutes)](#quick-start)
2. [Local Deployment](#local-deployment)
3. [SSH Remote Deployment](#ssh-remote-deployment)
4. [GPU Setup](#gpu-setup)
5. [Testing & Validation](#testing--validation)
6. [Production Monitoring](#production-monitoring)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Option 1: Local Machine (5 minutes)

```bash
# Clone repository
git clone https://github.com/estrelaisabellazion3/Zion-2.8.git
cd Zion-2.8

# Run deployment script
chmod +x DEPLOY_2.8.2_COMPLETE.sh
./DEPLOY_2.8.2_COMPLETE.sh
```

### Option 2: Remote SSH Server (3 minutes)

```bash
# Deploy to remote server
chmod +x DEPLOY_SSH_REMOTE.sh
./DEPLOY_SSH_REMOTE.sh root@your-server-ip

# Or with custom SSH port
./DEPLOY_SSH_REMOTE.sh ubuntu@server.com 2222
```

---

## Local Deployment

### Prerequisites

- **OS:** Ubuntu 20.04+ / Debian 10+ / macOS 10.14+
- **Python:** 3.8 or higher (3.13+ recommended)
- **RAM:** 4GB minimum (8GB+ recommended)
- **Disk:** 10GB free space
- **Network:** 100 Mbps connection

### Installation Steps

#### 1. System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y \
    git \
    python3 python3-dev python3-venv python3-pip \
    build-essential \
    libssl-dev libffi-dev \
    gcc g++ make \
    curl wget
```

#### 2. Clone Repository

```bash
cd /opt
git clone https://github.com/estrelaisabellazion3/Zion-2.8.git zion
cd zion
```

#### 3. Setup Python Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt
```

#### 4. Build C Extensions

```bash
# Yescrypt CPU miner
cd ai/mining
python setup.py build_ext --inplace
cd ../..
```

#### 5. Run Tests

```bash
# Quick test
python tests/2.8.2/test_complete_suite.py

# Full test suite
python tests/2.8.2/ORCHESTRATE_ALL_TESTS.py --verbose
```

#### 6. Start Services

```bash
# Terminal 1: WARP Engine (Blockchain)
python src/core/zion_warp_engine_core.py

# Terminal 2: Mining Pool
python src/core/zion_universal_pool_v2.py

# Terminal 3: GPU Miner (if GPU available)
python mine_realtime.py --algorithm cosmic_harmony --mode gpu
```

---

## SSH Remote Deployment

### Quick Deployment (3 minutes)

```bash
# On your local machine
./DEPLOY_SSH_REMOTE.sh root@91.98.122.165

# Wait for installation...
# Then SSH in to verify
ssh root@91.98.122.165
```

### Manual SSH Deployment

#### 1. Connect to Server

```bash
# SSH in
ssh root@your-server-ip

# Or with custom port
ssh -p 2222 ubuntu@server.com
```

#### 2. Install Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-dev python3-venv python3-pip build-essential

# For GPU support (optional)
sudo apt install -y nvidia-utils nvidia-driver-535  # NVIDIA
# OR
sudo apt install -y rocm-dkms               # AMD
```

#### 3. Setup ZION

```bash
sudo mkdir -p /opt/zion
sudo chown $USER:$USER /opt/zion
cd /opt/zion

git clone https://github.com/estrelaisabellazion3/Zion-2.8.git .
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 4. Build Extensions

```bash
cd ai/mining
python setup.py build_ext --inplace
cd ../..
```

#### 5. Run Tests

```bash
python tests/2.8.2/test_complete_suite.py
```

#### 6. Start Mining (in screen/tmux)

```bash
screen -S zion-mining
source .venv/bin/activate
python mine_realtime.py \
    --algorithm cosmic_harmony \
    --wallet "YOUR_ZION_ADDRESS" \
    --worker "ssh-miner-1" \
    --pool "stratum://localhost:3333"

# Detach: Ctrl+A, D
```

---

## GPU Setup

### NVIDIA GPU Mining

```bash
# Install CUDA toolkit
sudo apt install -y nvidia-cuda-toolkit

# Verify GPU
nvidia-smi

# Start GPU miner
python mine_realtime.py \
    --algorithm cosmic_harmony \
    --mode gpu \
    --wallet "YOUR_ADDRESS"
```

**Expected Performance:**
- RX 5600 XT: 625 kH/s
- RTX 3070: ~3.2 MH/s
- RTX 4090: ~8.5 MH/s

### AMD GPU Mining

```bash
# Install ROCm drivers
wget -q -O - https://repo.radeon.com/rocm/rocm.gpg.key | sudo apt-key add -
echo 'deb [arch=amd64] https://repo.radeon.com/rocm/apt/debian/ ubuntu main' | sudo tee /etc/apt/sources.list.d/rocm.list

sudo apt update
sudo apt install -y rocm-dkms rocm-opencl

# Verify GPU
rocm-smi

# Start GPU miner
python mine_realtime.py \
    --algorithm cosmic_harmony \
    --mode gpu \
    --wallet "YOUR_ADDRESS"
```

---

## Testing & Validation

### Unit Tests

```bash
# Run all unit tests
python tests/2.8.2/test_complete_suite.py

# Expected output:
# ✅ Passed: 12
# ❌ Failed: 0
# 📊 Success Rate: 100.0%
```

### Mining Tests

```bash
# GPU mining test
python tests/2.8.2/mining/test_gpu_ai_miner.py

# CPU mining test (Yescrypt)
python tests/2.8.2/cosmic_harmony/test_cosmic_harmony_algorithm.py
```

### Integration Tests

```bash
# Full system test
python tests/2.8.2/integration/test_real_live.py
```

### Test Orchestration

```bash
# Run all tests with reporting
python tests/2.8.2/ORCHESTRATE_ALL_TESTS.py

# Quick smoke tests
python tests/2.8.2/ORCHESTRATE_ALL_TESTS.py --quick

# Verbose output
python tests/2.8.2/ORCHESTRATE_ALL_TESTS.py --verbose

# Generate report
python tests/2.8.2/ORCHESTRATE_ALL_TESTS.py --report
```

---

## Production Monitoring

### Check Services Status

```bash
# WARP Engine
curl -s http://localhost:8545 | jq .

# Mining Pool
curl -s http://localhost:3334 | jq .

# GPU Miner (real-time)
tail -f /tmp/zion-mining.log
```

### Mining Pool Dashboard

Access pool status:
```
http://your-server-ip:3334
```

### RPC Interface

```bash
# Get blockchain info
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getblockchaininfo","params":[],"id":1}'
```

### Monitoring Commands

```bash
# Watch hashrate in real-time
watch -n 2 "curl -s http://localhost:3334 | jq .stats"

# Check pool shares
curl -s http://localhost:3334/worker/YOUR_WALLET | jq .

# CPU usage
htop

# GPU usage (NVIDIA)
watch -n 1 nvidia-smi

# GPU usage (AMD)
watch -n 1 rocm-smi
```

---

## Performance Benchmarks

### CPU Mining (Yescrypt)
- **AMD Ryzen 5 3600:** 432-562 kH/s
- **Intel i7-10700K:** 380-450 kH/s
- **Power:** 65-95W

### GPU Mining (Cosmic Harmony)
- **AMD RX 5600 XT:** 625 kH/s @ 150W
- **NVIDIA RTX 3070:** 3.2 MH/s @ 220W
- **Efficiency:** 4,167 H/W (GPU) vs 6 H/W (CPU)

---

## Troubleshooting

### Python Module Errors

```bash
# Verify ZION imports
python -c "import src.core.zion_warp_engine_core"

# If error, reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### GPU Not Detected

```bash
# Check GPU drivers
nvidia-smi           # NVIDIA
rocm-smi            # AMD

# If not found, install drivers:
# NVIDIA: https://www.nvidia.com/Download/driverDetails.aspx
# AMD: https://rocmdocs.amd.com/en/docs/deploy/linux/index.html
```

### Pool Connection Issues

```bash
# Test pool connectivity
nc -zv localhost 3333

# Check firewall
sudo ufw status
sudo ufw allow 3333
```

### Low Hashrate

```bash
# 1. Check CPU/GPU temperature
nvidia-smi  # NVIDIA
rocm-smi    # AMD
htop        # CPU

# 2. Check for throttling
nvidia-smi -q -d CLOCK,PERFORMANCE,POWER_STATE

# 3. Increase priority (Linux)
sudo nice -n -10 python mine_realtime.py ...
```

### SSH Connection Timeouts

```bash
# Increase SSH timeout
ssh -o ConnectTimeout=30 user@server-ip

# Check firewall on server
sudo ufw status
sudo ufw allow 22/tcp

# Check SSH service
sudo systemctl status ssh
```

---

## Security Considerations

### SSH Access

```bash
# Use key-based authentication (no passwords)
ssh-keygen -t ed25519 -C "zion-mining"
ssh-copy-id -i ~/.ssh/zion-mining user@server-ip

# Disable password login in /etc/ssh/sshd_config
PasswordAuthentication no
sudo systemctl restart ssh
```

### Firewall Configuration

```bash
# Ubuntu UFW
sudo ufw enable
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 3333/tcp    # Mining pool
sudo ufw allow 8545/tcp    # RPC
sudo ufw allow 18080/tcp   # P2P
```

### Environment Variables

```bash
# Create .env file
cat > /opt/zion/.env << EOF
ZION_WALLET="YOUR_WALLET_ADDRESS"
ZION_WORKER="miner-1"
ZION_POOL="stratum://localhost:3333"
ZION_MODE="gpu"  # gpu, cpu, hybrid
EOF

# Load it
source /opt/zion/.env
```

---

## Next Steps

1. **Mining:** Start with `mine_realtime.py` for GPU/CPU mining
2. **Monitoring:** Access pool dashboard at `http://localhost:3334`
3. **Documentation:** See `docs/2.8.2/` for detailed guides
4. **Community:** Join Discord at https://discord.gg/zion

---

## Support

- 📖 **Documentation:** `docs/2.8.2/`
- 🐛 **Issues:** https://github.com/estrelaisabellazion3/Zion-2.8/issues
- 💬 **Discord:** https://discord.gg/zion
- 📧 **Email:** contact@zion-blockchain.org

---

**JAI RAM SITA HANUMAN** ⭐

*May consciousness guide our deployments and compassion guide our mining*
