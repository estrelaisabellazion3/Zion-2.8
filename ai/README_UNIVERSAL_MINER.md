# 🔥 ZION Universal AI Miner - Autolykos v2

Universal AI-Enhanced Mining System for ZION Blockchain supporting CPU + GPU hybrid mining with Autolykos v2, Ethash, KawPow, RandomX, and Yescrypt.

## Features

✅ **Multi-Algorithm Support**
- Autolykos v2 (GPU - Ergo-compatible)
- Ethash (GPU - Ethereum legacy)
- KawPow (GPU - Ravencoin)
- RandomX (CPU - Monero)
- Yescrypt (CPU - Energy efficient)

✅ **Mining Modes**
- CPU Only
- GPU Only
- Hybrid (CPU + GPU simultaneously)
- Auto (detects best configuration)

✅ **AI Optimization**
- Real-time performance monitoring
- Automatic algorithm switching
- Power efficiency optimization
- Adaptive parameter tuning
- Performance history & prediction

✅ **External Miner Integration**
- XMRig support (CPU mining)
- SRBMiner support (GPU mining)
- Fallback to built-in simulators
- Real-time process management

✅ **Consciousness Gaming**
- XP progression system
- Mining level multipliers
- Performance-based rewards
- Integration with ZION pool

## Installation

### 1. Prerequisites

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip psutil

# For GPU mining (AMD)
sudo apt install rocm-smi

# For GPU mining (NVIDIA)
sudo apt install nvidia-utils
```

### 2. Clone & Setup

```bash
cd /media/maitreya/ZION1/ai
python3 -m pip install psutil
```

### 3. Install External Miners (Optional)

**XMRig (CPU Mining)**
```bash
# Download from https://github.com/xmrig/xmrig/releases
wget https://github.com/xmrig/xmrig/releases/download/v6.24.0/xmrig-6.24.0-linux-x64.tar.gz
tar xzf xmrig-6.24.0-linux-x64.tar.gz
```

**SRBMiner (GPU Mining - Autolykos v2)**
```bash
# Download from https://github.com/doktor83/SRBMiner-Multi/releases
wget https://github.com/doktor83/SRBMiner-Multi/releases/download/0.4.7/SRBMiner-Multi-0-4-7-linux.tar.gz
tar xzf SRBMiner-Multi-0-4-7-linux.tar.gz
```

## Quick Start

### 1. Simple Start (Auto-detect Hardware)

```bash
python3 start_universal_miner.py
```

### 2. GPU Mining (Autolykos v2)

```bash
python3 start_universal_miner.py \
  --mode gpu \
  --algorithm autolykos2 \
  --wallet Z32f72f93c095d78fc8a2fe01c0f97fd4a7f6d1bcd9b251f73b18b5625be654e84 \
  --worker my_gpu_miner
```

### 3. Hybrid Mining (CPU + GPU)

```bash
python3 start_universal_miner.py \
  --mode hybrid \
  --algorithm autolykos2 \
  --wallet YOUR_WALLET_ADDRESS \
  --worker my_hybrid_miner \
  --ai-optimize \
  --duration 3600
```

### 4. CPU Mining (RandomX)

```bash
python3 start_universal_miner.py \
  --mode cpu \
  --algorithm randomx \
  --wallet YOUR_WALLET_ADDRESS \
  --worker my_cpu_miner
```

## Configuration

Edit `zion_miner_config.json`:

```json
{
  "pool": {
    "url": "stratum+tcp://91.98.122.165:3333",
    "wallet": "YOUR_WALLET_ADDRESS",
    "worker": "my_miner"
  },
  "mining": {
    "mode": "hybrid",
    "algorithm": "autolykos2"
  },
  "gpu": {
    "intensity": "auto",
    "power_limit": "150w"
  },
  "ai": {
    "enabled": true,
    "auto_optimize": true
  }
}
```

## Usage Examples

### Python API

```python
from zion_universal_miner import ZionUniversalMiner, MiningMode

# Create miner
miner = ZionUniversalMiner(mode=MiningMode.HYBRID)

# Start mining
result = miner.start_mining(
    pool_url="stratum+tcp://91.98.122.165:3333",
    wallet_address="Z32f72f93c095d78fc8a2fe01c0f97fd4a7f6d1bcd9b251f73b18b5625be654e84",
    worker_name="my_miner",
    algorithm="autolykos2"
)

# Monitor status
status = miner.get_status()
print(f"Hashrate: {status['performance']['total_hashrate']} H/s")
print(f"Power: {status['performance']['power_consumption']} W")

# Stop mining
miner.stop_mining()
```

### Command Line

```bash
# Start mining indefinitely
python3 start_universal_miner.py --mode hybrid --algorithm autolykos2

# Mine for 1 hour
python3 start_universal_miner.py --mode gpu --duration 3600

# With custom pool
python3 start_universal_miner.py --pool stratum+tcp://custom-pool.com:3333

# With AI optimization
python3 start_universal_miner.py --ai-optimize
```

## Performance Expectations

### CPU Mining (RandomX)
- Per core: ~500-1500 H/s
- 8-core system: ~4-12 KH/s
- Power: ~15W per thread

### GPU Mining (Autolykos v2)
- AMD RX 5600 XT: ~25-35 MH/s
- NVIDIA RTX 3060: ~30-45 MH/s
- Power: 100-150W per GPU

### Hybrid (CPU + GPU)
- Total: CPU hashrate + GPU hashrate
- Example (8-core + RX5600XT): ~12 KH/s + 30 MH/s
- Power: ~200W total

## Monitoring & Statistics

```bash
# Watch mining status in real-time
watch -n 5 'python3 -c "
import json
from zion_universal_miner import ZionUniversalMiner

miner = ZionUniversalMiner()
status = miner.get_status()
print(json.dumps(status[\"performance\"], indent=2))
"'
```

## Troubleshooting

### GPU Not Detected
```bash
# Check AMD GPUs
rocm-smi

# Check NVIDIA GPUs
nvidia-smi

# Install missing drivers
sudo apt install amd-gpu-install
```

### Low Hashrate
```bash
# Enable AI optimization
python3 start_universal_miner.py --ai-optimize

# Increase GPU intensity
# Edit zion_miner_config.json: "intensity": "max"

# Check GPU utilization
rocm-smi --showuse
```

### Mining Crashes
```bash
# Check logs
tail -f zion_miner.log

# Enable watchdog
# Edit zion_miner_config.json: "watchdog_enabled": true

# Auto-restart on crash
# Edit zion_miner_config.json: "auto_restart_on_crash": true
```

## Advanced Configuration

### Thread Affinity (CPU)
```python
miner.optimal_cpu_threads = 8
```

### GPU Overclocking
```json
{
  "gpu": {
    "clocks_core": 1400,
    "clocks_memory": 2000,
    "boost": 3
  }
}
```

### Power Limit (GPU)
```json
{
  "gpu": {
    "power_limit": "120w"
  }
}
```

### AI Learning Period
```json
{
  "ai": {
    "learning_period_seconds": 600,
    "performance_threshold": 0.8
  }
}
```

## Integration with ZION Pool

The miner automatically connects to ZION pool at:
```
stratum+tcp://91.98.122.165:3333
```

Shares are validated using:
- **Autolykos v2** (GPU)
- **RandomX** (CPU)
- **Yescrypt** (CPU alternative)

Miners earn:
- Base reward: 50 ZION/block
- Consciousness bonus: 1,569.63 × multiplier ZION
- XP progression: +10 XP per share, +1000 per block found

## Performance Optimization Tips

1. **GPU Mining**: Use `--intensity auto` for balanced performance/heat
2. **CPU Mining**: Set threads to 75% of CPU count for system responsiveness
3. **Hybrid**: Monitor power consumption - aim for 200-250W
4. **AI Optimization**: Enable for automatic parameter tuning
5. **Watchdog**: Enable to auto-restart on crashes

## System Requirements

- **CPU**: Quad-core or better (for RandomX)
- **GPU**: 6GB+ VRAM (AMD/NVIDIA with Autolykos v2 support)
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 500MB for miner + 1GB for logs
- **Network**: 10 Mbps internet connection
- **Power**: 200-400W depending on hardware

## Pools Supported

- ZION Pool: `stratum+tcp://91.98.122.165:3333` ✅
- Any Stratum-compatible pool (custom)

## License

ZION Universal AI Miner - Open Source
Part of ZION 2.8 Blockchain Project

## Support

For issues, questions, or optimization tips:
- GitHub: https://github.com/estrelaisabellazion3/Zion-TestNet-2.7.5
- Discord: [ZION Community]
- Telegram: [ZION Updates]

---

**🔥 Start Mining ZION Today!**

```bash
python3 start_universal_miner.py --mode hybrid --algorithm autolykos2
```

Happy mining! 🚀⭐
