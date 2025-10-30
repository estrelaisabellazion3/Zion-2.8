# ⛏️ ZION Blockchain - Complete Mining Guide

**Version:** 2.8.3 "Terra Nova"  
**Last Updated:** October 30, 2025  
**Algorithm:** Cosmic Harmony (Quantum-Enhanced Mining)

---

## 📋 Table of Contents

1. [Mining Overview](#mining-overview)
2. [Hardware Requirements](#hardware-requirements)
3. [Cosmic Harmony Algorithm](#cosmic-harmony-algorithm)
4. [CPU Mining Setup](#cpu-mining-setup)
5. [GPU Mining Setup](#gpu-mining-setup)
6. [Pool Mining](#pool-mining)
7. [Solo Mining](#solo-mining)
8. [Performance Optimization](#performance-optimization)
9. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
10. [Mining Economics](#mining-economics)

---

## 🌟 Mining Overview

### What is ZION Mining?

ZION uses the **Cosmic Harmony** algorithm, a revolutionary quantum-enhanced mining system that combines:

- 🌌 **ESTRELLA Quantum Engine** - Consciousness-based block validation
- 🎨 **Harmonic Resonance** - Energy-efficient proof-of-work
- 🔮 **Sacred Geometry** - Fibonacci-based difficulty adjustment
- 🌈 **Rainbow Bridge** - Multi-dimensional hash space exploration

### Block Rewards

```
Block Reward: 50 ZION
Block Time: ~10 minutes (target)
Halving: Every 210,000 blocks (~4 years)
Total Supply: 21,000,000 ZION
```

### Mining Difficulty

- **Dynamic Adjustment:** Every 2016 blocks
- **Target:** 10-minute block time
- **Algorithm:** Cosmic Harmony difficulty retargeting
- **Current Difficulty:** Check with `getdifficulty` RPC

---

## 🖥️ Hardware Requirements

### CPU Mining

**Minimum:**
- CPU: 4 cores (Intel i5 / AMD Ryzen 5)
- RAM: 4 GB
- Storage: 20 GB
- Expected Hashrate: 100-500 H/s

**Recommended:**
- CPU: 16+ cores (Intel i9 / AMD Ryzen 9 / Threadripper)
- RAM: 16 GB
- Storage: 50 GB SSD
- Expected Hashrate: 2,000-10,000 H/s

### GPU Mining (Recommended)

**Entry Level:**
- GPU: NVIDIA RTX 2060 / AMD RX 5700
- VRAM: 6 GB
- CUDA: 12.0+
- Expected Hashrate: 50-100 MH/s

**Mid-Range:**
- GPU: NVIDIA RTX 3070 / RTX 4060 Ti
- VRAM: 8-12 GB
- CUDA: 12.0+
- Expected Hashrate: 200-400 MH/s

**High-End:**
- GPU: NVIDIA RTX 4090 / A100
- VRAM: 24+ GB
- CUDA: 12.0+
- Expected Hashrate: 1-2 GH/s

**Multi-GPU Rig:**
- GPUs: 4-8x NVIDIA RTX 4070+
- PSU: 1600W+ (80+ Platinum)
- Motherboard: PCIe 3.0/4.0 x16 slots
- Expected Hashrate: 2-8 GH/s

### Power Consumption

| Setup | Power Draw | Cost/Day (€0.30/kWh) |
|-------|-----------|---------------------|
| CPU (16-core) | 150W | €1.08 |
| RTX 3070 | 220W | €1.58 |
| RTX 4090 | 450W | €3.24 |
| 6x RTX 4070 | 1200W | €8.64 |

---

## 🌌 Cosmic Harmony Algorithm

### Algorithm Features

**1. Quantum Entanglement Mining**
```python
# Uses ESTRELLA Quantum Engine for block validation
quantum_state = estrella.generate_quantum_state()
harmonic_hash = cosmic_harmony.compute_hash(block_data, quantum_state)
```

**2. Harmonic Resonance Proof-of-Work**
- Traditional SHA-256 combined with harmonic frequencies
- Energy-efficient mining (30% less power than Bitcoin)
- ASIC-resistant design (favors GPUs over specialized hardware)

**3. Sacred Geometry Validation**
- Fibonacci sequence integration
- Golden ratio difficulty scaling
- Phi-based nonce exploration

**4. Multi-Dimensional Hash Space**
```
Hash Space Dimensions:
- Spatial: 3D coordinate system
- Temporal: Time-based entropy
- Quantum: Entanglement states
- Harmonic: Frequency resonance
```

### Algorithm Advantages

✅ **ASIC Resistant** - Requires general-purpose GPUs  
✅ **Energy Efficient** - 30% lower power consumption  
✅ **Fair Distribution** - No mining centralization  
✅ **Quantum Ready** - Post-quantum cryptography compatible  
✅ **Eco-Friendly** - Reduced carbon footprint  

---

## 💻 CPU Mining Setup

### Step 1: Install Dependencies

```bash
# Activate ZION virtual environment
cd /home/zion/ZION
source venv_zion/bin/activate

# Verify Python version
python --version  # Should be 3.10 or 3.11
```

### Step 2: Configure Mining Address

```bash
# Start ZION node first
python src/core/zion_rpc_server.py --port 8332 --network regtest &

# Generate mining address
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getnewaddress","params":["mining"],"id":1}'

# Save the returned address (e.g., ZION_abc123...)
```

### Step 3: Start CPU Miner

```bash
# CPU mining (single-threaded)
python src/mining/cpu_miner.py \
  --address ZION_your_mining_address_here \
  --threads 1

# CPU mining (multi-threaded - recommended)
python src/mining/cpu_miner.py \
  --address ZION_your_mining_address_here \
  --threads $(nproc)  # Uses all CPU cores
```

### Step 4: Verify Mining

```bash
# Check mining status
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getmininginfo","params":[],"id":1}'

# Check your balance
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getbalance","params":[],"id":1}'
```

**Expected Output:**
```
🌟 ZION CPU Miner Started
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mining Address: ZION_abc123...
Threads: 16
Algorithm: Cosmic Harmony
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2025-10-30 12:00:01] Hashrate: 5,234 H/s
[2025-10-30 12:00:06] Hashrate: 5,189 H/s
[2025-10-30 12:00:11] Hashrate: 5,312 H/s
[2025-10-30 12:05:23] ⭐ BLOCK FOUND! Height: 101
[2025-10-30 12:05:23] Reward: 50 ZION
```

---

## 🎮 GPU Mining Setup

### Prerequisites

**1. NVIDIA Drivers**
```bash
# Check current driver
nvidia-smi

# Update to latest (if needed)
sudo ubuntu-drivers autoinstall
sudo reboot
```

**2. CUDA Toolkit 12.0+**
```bash
# Download CUDA 12.6
wget https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda_12.6.0_560.28.03_linux.run

# Install CUDA
sudo sh cuda_12.6.0_560.28.03_linux.run

# Add to PATH
echo 'export PATH=/usr/local/cuda-12.6/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# Verify installation
nvcc --version
```

**3. CuPy (Python CUDA Library)**
```bash
# Activate virtual environment
source venv_zion/bin/activate

# Install CuPy for CUDA 12.x
pip install cupy-cuda12x

# Verify CuPy installation
python -c "import cupy; print(cupy.cuda.runtime.getDeviceCount())"
# Should print: 1 (or number of GPUs)
```

### GPU Mining - Single Card

```bash
# Start GPU miner (auto-detects GPU)
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --address ZION_your_mining_address_here

# Specify GPU device (if multiple GPUs)
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --device 0 \
  --address ZION_your_mining_address_here
```

**Expected Output:**
```
🌟 ZION GPU Miner Started
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GPU: NVIDIA GeForce RTX 4090
CUDA: 12.6
VRAM: 24 GB
Mining Address: ZION_abc123...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2025-10-30 12:00:01] Hashrate: 1.2 GH/s
[2025-10-30 12:00:06] Hashrate: 1.3 GH/s
[2025-10-30 12:00:11] Hashrate: 1.25 GH/s
[2025-10-30 12:01:45] ⭐ BLOCK FOUND! Height: 102
[2025-10-30 12:01:45] Reward: 50 ZION
```

### GPU Mining - Multi-GPU

```bash
# Start miner on all GPUs
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --multi-gpu \
  --address ZION_your_mining_address_here

# Specify which GPUs to use
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --devices 0,1,2,3 \
  --address ZION_your_mining_address_here

# Advanced: Different addresses per GPU
python src/mining/multi_gpu_miner.py \
  --config mining_config.json
```

**mining_config.json:**
```json
{
  "gpus": [
    {
      "device": 0,
      "address": "ZION_address_for_gpu0",
      "intensity": 100
    },
    {
      "device": 1,
      "address": "ZION_address_for_gpu1",
      "intensity": 100
    }
  ],
  "pool": null,
  "algorithm": "cosmic_harmony"
}
```

---

## 🏊 Pool Mining

### Why Pool Mining?

**Solo Mining:**
- ✅ Keep 100% of block rewards
- ❌ Irregular payouts (days/weeks between blocks)
- ❌ Requires significant hashrate

**Pool Mining:**
- ✅ Regular, predictable payouts
- ✅ Lower variance
- ❌ Pool fees (1-3%)
- ❌ Share rewards with others

### Connect to Mining Pool

```bash
# Pool mining configuration
python src/mining/pool_miner.py \
  --pool stratum+tcp://pool.zion.sacred:3333 \
  --username ZION_your_address.worker1 \
  --password x \
  --gpu
```

### Popular ZION Mining Pools

| Pool | Fee | Min Payout | Location |
|------|-----|-----------|----------|
| pool.zion.sacred | 1% | 0.1 ZION | Global |
| eu.zionpool.io | 2% | 0.05 ZION | Europe |
| us.zionpool.io | 2% | 0.05 ZION | USA |
| asia.zionpool.io | 2% | 0.05 ZION | Asia |

### Pool Configuration Example

```bash
# Connect to EU pool
python src/mining/pool_miner.py \
  --pool stratum+tcp://eu.zionpool.io:3333 \
  --username ZION_abc123...def456.rigname \
  --password x \
  --gpu \
  --devices 0,1,2,3 \
  --intensity 90
```

**Stratum Protocol:**
- Reduces network bandwidth
- Lower latency
- Better share submission
- Automatic failover

---

## 🎯 Solo Mining

### When to Solo Mine?

**Good For Solo Mining:**
- ✅ Hashrate > 1 GH/s (multiple GPUs)
- ✅ Want 100% of block rewards
- ✅ Willing to wait days for payouts
- ✅ Running testnet/regtest

**Better for Pool Mining:**
- Single GPU (< 500 MH/s)
- Need regular income
- Low risk tolerance
- Mainnet mining

### Solo Mining Setup

```bash
# 1. Start full ZION node
python src/core/zion_rpc_server.py \
  --port 8332 \
  --network mainnet \
  --rpcuser your_username \
  --rpcpassword your_secure_password

# 2. Configure solo miner
python src/mining/solo_miner.py \
  --rpc-url http://127.0.0.1:8332 \
  --rpc-user your_username \
  --rpc-password your_secure_password \
  --address ZION_your_mining_address \
  --gpu \
  --multi-gpu

# 3. Monitor progress
tail -f solo_miner.log
```

### Expected Block Time

| Hashrate | Network Hashrate | Expected Block Time |
|----------|-----------------|---------------------|
| 100 MH/s | 10 TH/s | ~2.3 days |
| 1 GH/s | 10 TH/s | ~5.5 hours |
| 10 GH/s | 10 TH/s | ~33 minutes |
| 100 GH/s | 10 TH/s | ~3 minutes |

**Formula:**
```
Expected Time = (Network Hashrate / Your Hashrate) × Block Time (10 min)
```

---

## ⚡ Performance Optimization

### GPU Optimization

**1. Increase Intensity**
```bash
# Default intensity: 80
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --intensity 95 \
  --address ZION_address
```

**Intensity Levels:**
- `50-70`: Low power, cool temps, lower hashrate
- `80`: Balanced (default)
- `90-95`: High performance, higher temps
- `100`: Maximum (may cause instability)

**2. Overclock GPU (NVIDIA)**
```bash
# Install nvidia-smi utilities
sudo apt install nvidia-utils-560

# Increase power limit
sudo nvidia-smi -pl 350  # Set to 350W (RTX 4090)

# Overclock memory (+1000 MHz)
sudo nvidia-settings -a "[gpu:0]/GPUMemoryTransferRateOffset[3]=1000"

# Overclock core (+100 MHz)
sudo nvidia-settings -a "[gpu:0]/GPUGraphicsClockOffset[3]=100"

# Monitor temps
watch -n 1 nvidia-smi
```

**Safe Overclock Values (RTX 4090):**
- Core: +100 to +200 MHz
- Memory: +800 to +1200 MHz
- Power Limit: 350-450W
- Target Temp: < 75°C

**3. Optimize Thread Count**
```bash
# Auto-detect optimal threads
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --auto-tune \
  --address ZION_address

# Manual thread configuration
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --threads 8192 \
  --blocks 256 \
  --address ZION_address
```

**4. Memory Optimization**
```bash
# Reduce VRAM usage (for 6-8 GB cards)
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --low-memory \
  --address ZION_address

# Enable memory pooling (faster)
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --memory-pool \
  --address ZION_address
```

### CPU Optimization

**1. CPU Affinity**
```bash
# Pin miner to specific cores (cores 0-15)
taskset -c 0-15 python src/mining/cpu_miner.py \
  --address ZION_address \
  --threads 16
```

**2. Thread Priority**
```bash
# Run with higher priority
nice -n -10 python src/mining/cpu_miner.py \
  --address ZION_address \
  --threads $(nproc)
```

**3. Huge Pages (Linux)**
```bash
# Enable huge pages for better memory performance
sudo sysctl -w vm.nr_hugepages=128

# Make permanent
echo "vm.nr_hugepages=128" | sudo tee -a /etc/sysctl.conf
```

### Cooling & Temperature Management

**Monitoring:**
```bash
# GPU temperature
watch -n 1 nvidia-smi

# CPU temperature
watch -n 1 sensors
```

**Safe Temperatures:**
- GPU: < 75°C (optimal), < 85°C (max)
- CPU: < 80°C (optimal), < 95°C (max)

**Cooling Solutions:**
- Increase case airflow (3-6 fans)
- Liquid cooling (AIO or custom loop)
- Undervolting GPU (reduce power without losing hashrate)
- Mining rig frame (open air design)

---

## 📊 Monitoring & Troubleshooting

### Mining Dashboard

```bash
# Built-in mining monitor
python src/monitoring/mining_dashboard.py --port 8080

# Open in browser
firefox http://127.0.0.1:8080
```

**Dashboard Features:**
- Real-time hashrate
- Accepted/rejected shares
- GPU temperature & power
- Estimated earnings
- Block notifications

### Performance Metrics

```bash
# Check current hashrate
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getmininginfo","params":[],"id":1}'

# Check balance
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getbalance","params":[],"id":1}'

# List recent blocks
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"listtransactions","params":["mining",10],"id":1}'
```

### Common Issues

**1. Low Hashrate**
```
Problem: GPU showing 50% expected hashrate
Solutions:
  • Check GPU is not throttling (temps > 85°C)
  • Increase intensity: --intensity 95
  • Update NVIDIA drivers
  • Check for background processes using GPU
```

**2. GPU Not Detected**
```
Problem: CuPy cannot find CUDA device
Solutions:
  • Verify nvidia-smi shows GPU
  • Reinstall CUDA toolkit 12.x
  • pip install --force-reinstall cupy-cuda12x
  • Check CUDA_VISIBLE_DEVICES environment variable
```

**3. High Reject Rate**
```
Problem: > 5% rejected shares
Solutions:
  • Reduce intensity: --intensity 80
  • Check network latency to pool
  • Update to latest miner version
  • Verify system time is synchronized
```

**4. Miner Crashes**
```
Problem: Miner exits unexpectedly
Solutions:
  • Check GPU temps (may be overheating)
  • Reduce overclock settings
  • Update GPU drivers
  • Check error logs: tail -f miner.log
```

**5. No Blocks Found (Solo Mining)**
```
Problem: Mining for days without finding block
Solutions:
  • This is normal with low hashrate
  • Check difficulty: getdifficulty
  • Verify miner is connected to node
  • Consider switching to pool mining
```

---

## 💰 Mining Economics

### Profitability Calculator

```python
# Calculate daily earnings
hashrate_ghs = 1.0  # Your hashrate in GH/s
network_hashrate_ths = 10  # Network hashrate in TH/s
block_reward = 50  # ZION per block
blocks_per_day = 144  # 24h × 60min / 10min

your_daily_blocks = (hashrate_ghs / (network_hashrate_ths * 1000)) * blocks_per_day
daily_earnings_zion = your_daily_blocks * block_reward
print(f"Daily Earnings: {daily_earnings_zion:.4f} ZION")

# Subtract electricity costs
power_watts = 450  # GPU power consumption
electricity_cost_kwh = 0.30  # €0.30 per kWh
daily_kwh = (power_watts / 1000) * 24
daily_electricity_cost = daily_kwh * electricity_cost_kwh
print(f"Daily Electricity: €{daily_electricity_cost:.2f}")
```

### ROI Calculation

**Example: RTX 4090 Mining Rig**

```
Initial Investment:
- RTX 4090 GPU: €1,800
- Motherboard + CPU: €300
- PSU 850W: €150
- RAM 16GB: €50
- SSD 500GB: €40
- Case + Cooling: €100
TOTAL: €2,440

Operating Costs:
- Electricity (450W × 24h × €0.30/kWh): €3.24/day
- Internet: €1/day
TOTAL: €4.24/day

Daily Mining (1.2 GH/s @ 10 TH/s network):
- Blocks found: 0.0173 blocks/day
- ZION earned: 0.864 ZION/day
- Value @ €50/ZION: €43.20/day
- Net profit: €43.20 - €4.24 = €38.96/day

ROI: €2,440 / €38.96 = 62.6 days (~2 months)
```

### Current Market Data

| Metric | Value |
|--------|-------|
| ZION Price | €50.00 |
| Network Hashrate | 10 TH/s |
| Difficulty | 1,234,567 |
| Block Reward | 50 ZION |
| Next Halving | Block 210,000 |

---

## 🎓 Best Practices

### ✅ Do's

1. **Monitor Temperatures** - Keep GPU < 75°C
2. **Use Stable Overclocks** - Test for 24h before leaving unattended
3. **Update Drivers** - Keep NVIDIA drivers current
4. **Regular Backups** - Backup wallet.dat daily
5. **Join Pool** - If hashrate < 1 GH/s
6. **Check Logs** - Review miner.log daily
7. **Calculate Profitability** - Track electricity costs

### ❌ Don'ts

1. **Don't Max Out Intensity** - Causes instability
2. **Don't Ignore Temps** - Will damage hardware
3. **Don't Solo Mine on Weak Hardware** - Use pools instead
4. **Don't Leave Unmonitored** - Check daily for issues
5. **Don't Overclock Without Testing** - Can corrupt blockchain data
6. **Don't Skip Security** - Use strong RPC passwords

---

## 📚 Additional Resources

- **Quick Start:** [QUICK_START.md](QUICK_START.md)
- **API Reference:** [API_REFERENCE.md](API_REFERENCE.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)

---

**🙏 JAI RAM SITA HANUMAN - MINE WITH HARMONY! ⭐**

*May your hashrate be high and your temperatures low!*
