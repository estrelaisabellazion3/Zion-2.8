# ZION 2.8.3 "Terra Nova" Testnet

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.8.3-blue.svg)](https://github.com/estrelaisabellazion3/Zion-2.8/releases)
[![Testnet](https://img.shields.io/badge/testnet-live-brightgreen.svg)](https://zionterranova.com)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)

> **Join the ZION Testnet - Mine, Test, and Build the Future of Humanitarian Blockchain**

ZION Testnet is a live testing environment for next-generation blockchain technology featuring **Cosmic Harmony** GPU mining, **WARP Engine** consensus, and a revolutionary **humanitarian tithe system** allocating 10% of mining rewards to verified charitable causes.

🌐 **Testnet RPC:** [zionterranova.com](https://zionterranova.com)  
⛏️ **Mining Pool:** pool.zionterranova.com:3333  
📊 **Dashboard:** [zionterranova.com/dashboard](https://zionterranova.com/dashboard)  
📖 **Documentation:** [docs/](./docs/)  
💬 **Support:** admin@zionterranova.com

---

## ⚠️ Testnet Notice

**This is a TESTNET environment for testing purposes only.**

- 🧪 Testnet coins have **NO REAL VALUE**
- 🔄 Network may be **RESET** without notice during testing
- 🐛 Bugs and issues are **EXPECTED** - please report them!
- 📝 All data is for **TESTING ONLY**

**Mainnet Launch:** TBA (after successful testnet validation)

---

## ✨ What You Can Do

### ⛏️ Mining
- Test **Cosmic Harmony** GPU mining algorithm
- Join the **mining pool** or solo mine
- Earn testnet ZION coins (for testing only)
- Benchmark your hardware performance

### 🔧 Development
- Build applications using **RPC API**
- Test wallet integrations
- Develop mining software
- Create blockchain explorers

### 🧪 Testing
- Stress test the network
- Report bugs and issues
- Suggest improvements
- Help validate consensus

### 📊 Monitoring
- Track network statistics
- Monitor mining pool performance
- View blockchain explorer data
- Analyze transaction throughput

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Linux, macOS, or Windows
- 2 GB RAM minimum
- 5 GB free disk space
- Internet connection

### Option 1: CLI Binary (Fastest)
```bash
# Download latest release
wget https://github.com/estrelaisabellazion3/Zion-2.8/releases/download/v2.8.3/zion-cli-2.8.3-linux-amd64.tar.gz

# Extract
tar -xzf zion-cli-2.8.3-linux-amd64.tar.gz
cd zion-cli-2.8.3

# Create wallet
./zion-cli wallet --create

# Check node status
./zion-cli node --status

# Start mining
./zion-cli mine --start
```

### Option 2: Docker (Recommended for Full Node)
```bash
# Clone repository
git clone https://github.com/estrelaisabellazion3/Zion-2.8.git
cd Zion-2.8

# Start node
docker-compose -f docker-compose.testnet.yml up -d

# Check status
curl http://localhost:8545/api/status
```

### Option 2: Binary Release
```bash
# Download latest release
wget https://github.com/estrelaisabellazion3/Zion-2.8/releases/download/v2.8.3/zion-cli-2.8.3-linux-amd64.tar.gz

# Extract and run
tar -xzf zion-cli-2.8.3-linux-amd64.tar.gz
chmod +x zion-cli
./zion-cli --help
```

### Option 3: From Source
```bash
# Clone and setup
git clone https://github.com/estrelaisabellazion3/Zion-2.8.git
cd Zion-2.8
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run node
python new_zion_blockchain.py
```

📚 **Detailed Instructions:** See [QUICK_START.md](./docs/2.8.3/QUICK_START.md)

---

## 🌐 Network Information

### Testnet (Current - LIVE)
- **Launch Date:** October 30, 2025
- **Network ID:** testnet-2.8.3
- **RPC Endpoint:** https://zionterranova.com
- **Dashboard:** https://zionterranova.com/dashboard
- **API Stats:** https://zionterranova.com/api/stats
- **Metrics:** https://zionterranova.com/metrics
- **Mining Pool:** pool.zionterranova.com:3333
- **Seed Nodes:** 91.98.122.165:8332
- **SSL Certificate:** Let's Encrypt (expires 2026-01-28)

### Mainnet (Planned)
- **Launch:** Q1 2026
- **Total Supply:** 21 billion ZION
- **Block Time:** ~2 minutes
- **Block Reward:** 50 ZION (decreasing)
- **Humanitarian Allocation:** 10% per block

---

## 📦 What's Inside

### Core Components

#### WARP Engine (`new_zion_blockchain.py`)
Full-featured blockchain node with:
- P2P networking and peer discovery
- RPC API server (port 8545)
- Transaction processing and validation
- Block creation and mining
- Consensus mechanism

#### Mining Pool (`src/core/zion_universal_pool_v2.py`)
Production-ready mining pool:
- Stratum protocol support
- Multi-algorithm handling
- Share validation and payouts
- Worker management
- Real-time statistics

#### Command-Line Interface (`cli_simple.py`)
User-friendly CLI tools:
- Wallet creation and management
- Transaction broadcasting
- Node status queries
- Mining controls

#### Cosmic Harmony Library (`build_zion/cosmic_harmony/`)
GPU-optimized mining algorithm:
- BLAKE3 hashing core
- Yescrypt memory-hard function
- Autolykos2 ASIC resistance
- Consciousness field calculations

---

## 🛠️ Technology Stack

### Backend
- **Python 3.13** - Core blockchain implementation
- **Flask** - RPC API server
- **asyncio** - High-performance networking
- **BLAKE3** - Cryptographic hashing
- **ecdsa** - Digital signatures

### Mining
- **C++17** - Cosmic Harmony algorithm
- **CUDA** - GPU acceleration (optional)
- **OpenCL** - Cross-platform GPU support

### Infrastructure
- **Docker** - Containerized deployment
- **Nginx** - Reverse proxy and SSL termination
- **Prometheus** - Metrics and monitoring
- **Grafana** - Dashboard visualization

### Security
- **Let's Encrypt** - SSL/TLS certificates
- **AES-256** - Data encryption
- **Multi-sig** - Wallet security
- **UFW** - Firewall management

---

## 📖 Documentation

### Getting Started
- [Quick Start Guide](./docs/2.8.3/QUICK_START.md) - Get running in 5 minutes
- [Mining Guide](./docs/2.8.3/MINING_GUIDE.md) - Complete mining tutorial
- [Docker Guide](./docs/DOCKER_QUICK_START.md) - Docker deployment

### Technical
- [RPC API Reference](./docs/2.8.3/RPC_API.md) - Complete API documentation
- [Architecture Overview](./docs/2.8.3/ARCHITECTURE.md) - System design deep-dive
- [Security Best Practices](./docs/SECURITY.md) - Secure your ZION

### Support
- [FAQ](./docs/2.8.3/FAQ.md) - Frequently Asked Questions
- [Troubleshooting](./docs/2.8.3/TROUBLESHOOTING.md) - Common issues

---

## 🎯 Roadmap

### ✅ Completed (v2.8.3 - October 2025)
- [x] WARP Engine consensus mechanism
- [x] Cosmic Harmony GPU mining algorithm
- [x] Multi-signature wallet system
- [x] Production-grade mining pool
- [x] RPC API with full documentation
- [x] Docker containerization
- [x] SSL/TLS security (HTTPS)
- [x] Binary releases (Linux)

### 🔄 In Progress (Q4 2025)
- [ ] Testnet public launch (Nov 15, 2025)
- [ ] Windows and macOS binaries
- [ ] Mobile wallet (iOS/Android)
- [ ] Hardware wallet integration
- [ ] Advanced monitoring dashboards

### 🔮 Planned (Q1-Q2 2026)
- [ ] Mainnet launch
- [ ] Smart contracts platform
- [ ] Zero-knowledge privacy features
- [ ] Cross-chain bridges (Ethereum, Solana)
- [ ] Decentralized exchange (DEX)
- [ ] Governance DAO

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute
- 🐛 **Bug Reports:** Found an issue? [Open an issue](https://github.com/estrelaisabellazion3/Zion-2.8/issues)
- 💡 **Feature Requests:** Have an idea? Share it with us!
- 🔧 **Code Contributions:** Submit a pull request
- 📖 **Documentation:** Improve our docs
- 🌍 **Translation:** Help translate ZION

### Development Setup
```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/Zion-2.8.git
cd Zion-2.8

# Create branch
git checkout -b feature/your-feature-name

# Setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/

# Submit PR
git push origin feature/your-feature-name
```

### Contribution Guidelines
- Follow PEP 8 style guide for Python code
- Write tests for new features
- Update documentation as needed
- Keep commits atomic and well-described
- Be respectful and constructive

---

## 💰 Mining

### Start Mining in 3 Steps

**1. Download Miner**
```bash
wget https://github.com/estrelaisabellazion3/Zion-2.8/releases/download/v2.8.3/zion-miner-2.8.3-linux-amd64.tar.gz
tar -xzf zion-miner-2.8.3-linux-amd64.tar.gz
```

**2. Configure Wallet**
```bash
./zion-cli wallet --create
# Save your wallet address!
```

**3. Start Mining**
```bash
./zion-miner --pool pool.zionterranova.com:3333 --wallet YOUR_WALLET_ADDRESS
```

📚 **Detailed Guide:** [MINING_GUIDE.md](./docs/2.8.3/MINING_GUIDE.md)

### Mining Rewards
- **Block Reward:** 50 ZION
- **Your Share:** 45 ZION (90%)
- **Humanitarian Fund:** 5 ZION (10%)
- **Block Time:** ~2 minutes
- **Difficulty:** Auto-adjusting

---

## 🔐 Security

### Security Features
- ✅ Multi-signature wallets (3-of-5 threshold)
- ✅ AES-256 encryption for private keys
- ✅ SSL/TLS for all network communication
- ✅ Regular security audits
- ✅ Open-source and peer-reviewed

### Reporting Security Issues
If you discover a security vulnerability, please email:
- **Security Team:** security@zionterranova.com
- **PGP Key:** [Download](https://zionterranova.com/pgp)

**Please do not** open public issues for security vulnerabilities.

### Bug Bounty Program
We offer rewards for responsibly disclosed security vulnerabilities:
- **Critical:** $1,000 - $5,000
- **High:** $500 - $1,000
- **Medium:** $100 - $500
- **Low:** $50 - $100

---

## 📊 System Requirements

### Minimum (Node)
- **CPU:** 2 cores
- **RAM:** 2 GB
- **Disk:** 10 GB SSD
- **Network:** 10 Mbps
- **OS:** Ubuntu 20.04+ / Debian 11+ / Windows 10+

### Recommended (Mining)
- **CPU:** 4+ cores
- **RAM:** 4 GB
- **Disk:** 20 GB SSD
- **GPU:** NVIDIA RTX 3060+ or AMD RX 6600+
- **Network:** 100 Mbps

### Optimal (Pool Operator)
- **CPU:** 8+ cores
- **RAM:** 16 GB
- **Disk:** 100 GB NVMe SSD
- **GPU:** Not required
- **Network:** 1 Gbps
- **Bandwidth:** Unlimited

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](./LICENSE) file for details.

### Third-Party Licenses
- BLAKE3: CC0-1.0 / Apache-2.0
- Python: PSF License
- Docker: Apache 2.0

---

## 🌟 Community

### Stay Connected
- **Website:** [zionterranova.com](https://zionterranova.com)
- **GitHub:** [estrelaisabellazion3/Zion-2.8](https://github.com/estrelaisabellazion3/Zion-2.8)
- **Email:** admin@zionterranova.com
- **Twitter:** [@ZionBlockchain](https://twitter.com/ZionBlockchain) (coming soon)
- **Discord:** [Join Server](https://discord.gg/zion) (coming soon)
- **Telegram:** [t.me/ZionBlockchain](https://t.me/ZionBlockchain) (coming soon)

### Core Team
- **Lead Developer:** Estrella Isabella Zion
- **Security Advisor:** TBA
- **Community Manager:** TBA

---

## 📈 Statistics

### Testnet Stats (Live - October 30, 2025)
- **Block Height:** 21
- **Total Transactions:** 21 (block creation)
- **Network Hashrate:** CPU mining active
- **Active Nodes:** 1 (zionterranova.com)
- **Total Supply:** 1,000 ZION (50 ZION/block reward)
- **Uptime:** 24+ hours
- **SSL Status:** ✅ Valid Let's Encrypt certificate

**Live Dashboard:** [zionterranova.com/dashboard](https://zionterranova.com/dashboard)
**API Stats:** [zionterranova.com/api/stats](https://zionterranova.com/api/stats)

---

## 🙏 Acknowledgments

Special thanks to:
- **Bitcoin Core** - For pioneering blockchain technology
- **Ethereum** - For smart contract inspiration
- **Monero** - For privacy features research
- **Ergo** - For Autolykos algorithm
- **The Open Source Community** - For making this possible

---

## ⚠️ Disclaimer

**ZION is experimental software in active development.**

- Testnet tokens have **no monetary value**
- Use at your own risk on mainnet
- Always backup your wallet
- Never invest more than you can afford to lose
- Consult local regulations before mining or trading

---

**Built with ❤️ for a better world through blockchain technology**

*ZION 2.8.3 "Terra Nova" - October 30, 2025*
