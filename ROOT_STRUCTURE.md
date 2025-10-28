# 📁 ZION 2.8.2 Nebula - Root Structure

## �� Root-Level Documentation
- **Readme.md** - Main project documentation (ZION 2.8.2 Nebula overview)
- **ROADMAP.md** - 2025-2027 strategic roadmap
- **REALTIME_MINING_README.md** - Professional GPU mining guide

## 🔧 Configuration Files
- `requirements.txt` - Python dependencies
- `requirements-pool-switcher.txt` - Pool switcher dependencies
- `zion_gpu_mining_config.json` - GPU mining configuration
- `zion_gpu_mining_config.py` - GPU mining config helper
- `setup_lnd.sh` - Lightning Network Daemon setup
- `docker-compose.*.yml` - Docker orchestration files
- `.env.production`, `.env.example` - Environment configuration

## 📦 Source Code Structure
```
src/                      # Core blockchain implementation
├── core/                 # Blockchain engine, pool, RPC
├── integrations/         # Cross-chain bridges, governance
├── mining/               # Mining algorithms
└── ...

ai/                       # AI/ML components
├── mining/               # Real-time metrics, optimizers
├── orchestration/        # Multi-pool management
└── ...

api/                      # API servers and services
website/                  # Frontend (Next.js, Vue)
```

## 🧪 Testing Infrastructure
```
tests/2.8.2/
├── test_complete_suite.py       # Full integration tests
├── run_complete_tests.py        # Test runner
├── cosmic_harmony/              # Algorithm tests
├── mining/                      # Mining component tests
├── integration/                 # Integration tests
└── pool/                        # Pool tests
```

## 📊 Reports & Data
```
reports/                  # Benchmark and test reports
├── benchmark_report_*.json/.txt
├── cosmic_harmony_test_report_*.json
├── mining_validation_report_*.json
└── ...

.artifacts/               # Runtime data (logs, databases)
.web-temp/               # Temporary web assets
```

## 🎯 Top-Level Scripts
- `mine_realtime.py` - Professional mining launcher (CLI)
- `benchmark_miners.py` - GPU vs CPU benchmark framework
- `build_all_libraries.sh` - Build automation script

## 📖 Documentation by Category
```
docs/2.8.2/              # Version 2.8.2 specific docs
├── LND_SETUP_README.md
├── AMD_RX5600_DRIVER_GUIDE.md
├── OPERATIONAL_REPORT_2025-10-24.md
├── PROJECT_SUMMARY_2025.md
├── DOCUMENTATION_MAP.md
└── ...

docs/WHITEPAPER_2025/    # Complete 12-part whitepaper
docs/SACRED_TRINITY/     # Governance documentation
```

## 🗂️ Archived/Temporary
```
.web-temp/               # Temporary HTML dashboards
.artifacts/              # Log files, database files
local_data/, local_logs/ # Local development data
```

---

**Total Codebase:**
- ~290+ Python files
- ~100,000+ lines of code
- 6+ algorithms
- 14+ features
- 100% test coverage

**Last Updated:** October 28, 2025
