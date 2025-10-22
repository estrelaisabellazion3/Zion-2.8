# 🤖 AI Modules & Algorithms

Organizovaná AI infrastruktura ZION s minerem, analýtikou a trading boty

---

## 📂 Struktura

```
ai/
├── mining/              # ⛏️ Mining algorithms & Stratum
├── analytics/           # 📊 Blockchain & predictive analytics
├── trading/             # 💹 Trading & market analysis
├── core/                # 🧠 Core AI orchestration
├── [ostatní AI]         # 🌟 Cosmic, quantum, gaming, music, etc.
```

---

## ⛏️ Mining Module (`ai/mining/`)

**Těžební algoritmy a Stratum integrace**

### Miners
- `zion_universal_miner.py` - Multi-algorithm CPU/GPU miner
- `start_universal_miner.py` - Launch script
- `zion_yescrypt_optimized.py` - Optimized Yescrypt CPU
- `zion_yescrypt_real.py` - Native Yescrypt implementation

### Stratum Protocol
- `stratum_client.py` - Stratum v1 async client
- `stratum_client_sync.py` - Stratum v1 sync client
- `pool_stratum_bridge.py` - Bridge to pool infrastructure

### Usage
```python
from ai.mining.zion_universal_miner import UniversalMiner

miner = UniversalMiner(algorithm='randomx', wallet='ZION_ADDRESS')
miner.start()
```

---

## 📊 Analytics Module (`ai/analytics/`)

**Blockchain analýza a prediktivní údržba**

- `zion_blockchain_analytics.py` - On-chain analytics
- `zion_predictive_maintenance.py` - System health prediction
- `zion_security_monitor.py` - Security threat monitoring

### Usage
```python
from ai.analytics.zion_blockchain_analytics import BlockchainAnalytics

analyzer = BlockchainAnalytics()
stats = analyzer.get_chain_stats()
```

---

## 💹 Trading Module (`ai/trading/`)

**Trading boti a market analysis**

- `zion_trading_bot.py` - Automated trading bot

### Features
- Real-time price monitoring
- Technical analysis
- Automated buy/sell signals
- Risk management

---

## 🧠 Core AI Module (`ai/core/`)

**Centrální AI orchestration**

- `zion_ai_master_orchestrator.py` - Main AI orchestrator
- `quantum_enhanced_ai_integration.py` - Quantum computing integration

### Orchestration
- Load balancing
- System health
- Resource allocation
- Performance optimization

---

## 🌟 Specialty AI Modules

Ostatní AI implementace:

- `zion_cosmic_ai.py` - Cosmic consciousness simulation
- `zion_quantum_ai.py` - Quantum algorithm exploration
- `zion_oracle_ai.py` - Prediction oracle
- `zion_gaming_ai.py` - Gaming AI
- `zion_music_ai.py` - Music generation
- `zion_lightning_ai.py` - Lightning network AI
- `zion_bio_ai.py` - Bio-inspired algorithms
- `zion_cosmic_image_analyzer.py` - Image analysis
- `zion_afterburner.py` - Performance tuning

---

## 🚀 Quick Start

### Setup
```bash
cd ai/mining
pip install -r ../../requirements.txt
```

### Start Mining
```bash
python3 zion_universal_miner.py \
    --algorithm randomx \
    --pool 127.0.0.1:3333 \
    --wallet YOUR_ADDRESS
```

### Start Analytics
```bash
python3 ../analytics/zion_blockchain_analytics.py
```

### Start Trading
```bash
python3 ../trading/zion_trading_bot.py
```

---

## 📊 Algorithm Support

**Supported in Universal Miner:**
- RandomX (CPU)
- Autolykos v2 (GPU)
- Yescrypt (CPU)
- KawPow (GPU)

---

## 🔗 Integration Points

```
Pool <---> Stratum Client <---> Universal Miner
             ↓
        Analytics Monitor
             ↓
        Master Orchestrator
             ↓
        [Trading/Gaming/AI]
```

---

## ⚙️ Configuration

### Default Config
```yaml
algorithm: auto
difficulty: auto-adjust
reconnect: 30s
timeout: 60s
threads: auto
```

### Custom Config
```python
config = {
    'algorithm': 'yescrypt',
    'threads': 8,
    'difficulty': 1024,
    'pool': '91.98.122.165:3333'
}
```

---

## 📈 Performance Metrics

Monitorované metriky:
- Hashrate (H/s)
- Share acceptance rate
- Pool connection status
- Temperature (GPU)
- Power consumption
- Uptime

---

## 🐛 Debugging

### Enable Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Status
```bash
python3 -m ai.mining.zion_universal_miner --status
```

### Performance Test
```bash
python3 -m ai.mining.zion_universal_miner --benchmark
```

---

## 📚 Documentation

- Mining: `ai/mining/README.md`
- Analytics: `ai/analytics/README.md`
- Trading: `ai/trading/README.md`

---

**Status**: ✅ Organized  
**Last Updated**: 23. září 2025  
**Version**: ZION 2.8.1 "Estrella"
