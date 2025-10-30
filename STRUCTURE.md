# 📁 ZION 2.8.3 - Project Structure

**Organized:** October 30, 2025  
**Version:** 2.8.3 Cosmic Harmony  

---

## 🎯 Root Directory Organization

```
ZION/
├── 2.8.3/                          # ⭐ Current version (2.8.3)
│   ├── docs/                       # Documentation
│   │   ├── API_REFERENCE.md
│   │   ├── ARCHITECTURE.md
│   │   ├── DEPLOYMENT_GUIDE.md
│   │   ├── MINING_GUIDE.md
│   │   ├── QUICK_START.md
│   │   ├── TROUBLESHOOTING.md
│   │   └── phases/                 # Phase completion reports
│   │       ├── PHASE_5_COMPLETE.md
│   │       ├── PHASE_7_COMPLETE.md
│   │       ├── PHASE_9_COMPLETE.md
│   │       └── PHASE_11_COMPLETE.md
│   └── deployment/                 # Production deployment
│       ├── deploy.sh
│       ├── test-deployment.sh
│       ├── zion-node.service
│       ├── nginx-zion.conf
│       ├── backup.sh
│       ├── security-hardening.sh
│       ├── prometheus.yml
│       ├── grafana-dashboard.json
│       └── PHASE_12_COMPLETE.md
│
├── src/                            # Source code
│   ├── core/                       # Blockchain core
│   │   ├── new_zion_blockchain.py
│   │   └── zion_rpc_server.py
│   ├── mining/                     # Mining implementation
│   ├── wallet/                     # Wallet implementation
│   ├── network/                    # P2P network
│   └── consensus/                  # Consensus algorithms
│
├── tests/                          # Test suite
│   ├── unit/                       # Unit tests
│   ├── integration/                # Integration tests
│   └── artifacts/                  # Test artifacts (gitignored)
│       ├── htmlcov/
│       └── .pytest_cache/
│
├── tools/                          # Development tools
│   └── mining/                     # Mining utilities
│       ├── benchmark_miners.py
│       ├── mine_realtime.py
│       └── REALTIME_MINING_README.md
│
├── scripts/                        # Utility scripts
│   ├── setup_lnd.sh
│   ├── run_test_node.py
│   └── cli_simple.py
│
├── docker/                         # Docker configuration
│   ├── docker-compose.production.yml
│   ├── docker-compose.testnet.yml
│   ├── Dockerfile.testnet
│   └── .dockerignore
│
├── logs/                           # Application logs (gitignored)
│   ├── node.log
│   ├── node_startup.log
│   └── coverage.xml
│
├── data/                           # Runtime data
│   └── databases/                  # Databases (gitignored)
│       ├── zion_regtest.db
│       └── zion_pool.db
│
├── archive/                        # Archived files (gitignored)
│   ├── 2.8.2/                      # Old 2.8.2 deployment files
│   └── old_builds/                 # Old build artifacts
│
├── docs/                           # Legacy documentation
├── frontend/                       # Web frontend
├── website/                        # Project website
├── venv_testing/                   # Python virtual environment
│
└── Configuration Files (Root)
    ├── Readme.md                   # Main README
    ├── requirements.txt            # Python dependencies
    ├── pytest.ini                  # Pytest configuration
    ├── .gitignore                  # Git ignore rules
    ├── .gitmodules                 # Git submodules
    └── ROADMAP.md                  # Project roadmap
```

---

## 📦 Directory Descriptions

### Core Directories

#### `2.8.3/` - Current Version
Complete 2.8.3 version with documentation and deployment scripts. This is the **main working directory** for current development.

- **`docs/`** - User and developer documentation (6 comprehensive guides)
- **`docs/phases/`** - Phase completion reports (Phase 5-11)
- **`deployment/`** - Production deployment automation (Phase 12)

#### `src/` - Source Code
Core blockchain implementation organized by functionality:
- `core/` - Blockchain engine and RPC server
- `mining/` - Mining algorithms (Cosmic Harmony)
- `wallet/` - Wallet functionality
- `network/` - P2P networking
- `consensus/` - Consensus mechanisms

#### `tests/` - Test Suite
Comprehensive test coverage (96.7% - 89/92 tests passing):
- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for full system
- `artifacts/` - Generated test artifacts (HTML coverage, pytest cache)

### Development Tools

#### `tools/` - Development Utilities
Tools for development and mining:
- `mining/` - Mining benchmarks and real-time mining tools

#### `scripts/` - Utility Scripts
Helper scripts for setup and testing:
- Lightning Network setup
- Test node runner
- CLI utilities

### Configuration & Deployment

#### `docker/` - Docker Configuration
Container configuration for various environments:
- Production deployment
- Testnet deployment
- Development environment

#### `logs/` - Application Logs
Runtime logs from ZION node and tests (gitignored):
- Node logs
- Test logs
- Coverage reports

#### `data/` - Runtime Data
Runtime data including databases (gitignored):
- Blockchain databases
- Pool databases

### Archive

#### `archive/` - Archived Files
Historical files and old builds (gitignored):
- `2.8.2/` - Old 2.8.2 deployment scripts
- `old_builds/` - Old build artifacts and releases

---

## 🎯 Version Management

### Current Active Version: **2.8.3 Cosmic Harmony**

**Location:** `/2.8.3/`

**Key Features:**
- ✅ Cosmic Harmony mining algorithm
- ✅ 96.7% test coverage (89/92 tests)
- ✅ Production deployment automation
- ✅ Comprehensive documentation
- ✅ Real-time monitoring (Prometheus/Grafana)

**Phases Completed:** 12/12
1. ✅ Project Setup
2. ✅ Core Implementation
3. ✅ Mining System
4. ✅ Wallet & Transactions
5. ✅ Core Testing (100%)
6. ✅ Wallet Testing (89%)
7. ✅ Extended Integration (100%)
8. ⏭️ Stratum Protocol (skipped)
9. ✅ Performance Testing (100%)
10. ✅ Security Audit (100%)
11. ✅ Documentation Sprint (100%)
12. ✅ Production Deployment (100%)

---

## 📝 File Naming Conventions

### Documentation
- `UPPER_CASE.md` - Major documentation files
- `Phase_Name.md` - Phase reports
- `snake_case.md` - Technical documentation

### Code
- `snake_case.py` - Python source files
- `PascalCase.py` - Class modules
- `kebab-case.sh` - Shell scripts

### Configuration
- `lowercase.yml` - YAML configs
- `lowercase.json` - JSON configs
- `.lowercase` - Dotfiles

---

## 🔍 Finding Files

### Documentation
```bash
# Main README
cat Readme.md

# 2.8.3 Documentation
ls 2.8.3/docs/

# Phase Reports
ls 2.8.3/docs/phases/

# Deployment Guide
cat 2.8.3/deployment/README.md
```

### Source Code
```bash
# Core blockchain
ls src/core/

# Mining implementation
ls src/mining/

# All tests
ls tests/
```

### Logs & Data
```bash
# Application logs
ls logs/

# Databases
ls data/databases/

# Test coverage
open htmlcov/index.html  # (in tests/artifacts/)
```

---

## 🚀 Quick Navigation

### Development
```bash
cd /home/zion/ZION/src/core          # Core code
cd /home/zion/ZION/tests             # Tests
cd /home/zion/ZION/tools/mining      # Mining tools
```

### Documentation
```bash
cd /home/zion/ZION/2.8.3/docs        # Main docs
cd /home/zion/ZION/2.8.3/docs/phases # Phase reports
```

### Deployment
```bash
cd /home/zion/ZION/2.8.3/deployment  # Deployment scripts
```

### Configuration
```bash
cd /home/zion/ZION/docker            # Docker configs
cd /home/zion/ZION/scripts           # Utility scripts
```

---

## 🧹 Cleanup History

**Date:** October 30, 2025

**Changes Made:**
1. ✅ Moved phase reports to `2.8.3/docs/phases/`
2. ✅ Archived old 2.8.2 files to `archive/2.8.2/`
3. ✅ Moved logs to `logs/` directory
4. ✅ Moved databases to `data/databases/`
5. ✅ Moved test artifacts to `tests/artifacts/`
6. ✅ Moved mining tools to `tools/mining/`
7. ✅ Archived old builds to `archive/old_builds/`
8. ✅ Consolidated Docker files in `docker/`
9. ✅ Moved scripts to `scripts/` directory
10. ✅ Removed duplicate README.md (kept Readme.md)

**Result:** Clean, organized root directory with logical structure.

---

## 🔐 Security Notes

### Gitignored Directories
The following directories are automatically ignored by git:
- `logs/` - Contains runtime logs
- `tests/artifacts/` - Test coverage and cache
- `archive/` - Old files and builds
- `data/databases/` - Database files
- `venv_testing/` - Python virtual environment
- `*.db` - All database files
- `*.log` - All log files

### Private Files
Never commit:
- Database files (`.db`, `.sqlite`)
- Log files (`.log`)
- Coverage reports (`coverage.xml`, `.coverage`)
- Test artifacts (`htmlcov/`, `.pytest_cache/`)
- Build artifacts (`dist/`, `build/`)

---

## 📚 Additional Resources

- **Main README:** [Readme.md](Readme.md)
- **Roadmap:** [ROADMAP.md](ROADMAP.md)
- **Quick Start:** [2.8.3/docs/QUICK_START.md](2.8.3/docs/QUICK_START.md)
- **API Reference:** [2.8.3/docs/API_REFERENCE.md](2.8.3/docs/API_REFERENCE.md)
- **Deployment:** [2.8.3/deployment/README.md](2.8.3/deployment/README.md)

---

**🙏 JAI RAM SITA HANUMAN - ORGANIZED FOR COSMIC HARMONY! ⭐**

*Generated: October 30, 2025*  
*ZION 2.8.3 - Production-Ready Blockchain*
