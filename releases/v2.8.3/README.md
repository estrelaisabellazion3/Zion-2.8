# ZION 2.8.3 Testnet - CLI Release

**Version:** 2.8.3 "Terra Nova"  
**Release Date:** October 29, 2025  
**Platform:** Linux x86_64  

## 📦 What's Included

### zion-cli
Command-line interface for ZION blockchain:
- Wallet management (create, check balance)
- Node information (status, peers)
- Mining controls (start, stop, hashrate)

**Size:** 7.8 MB (standalone executable)

## 🚀 Quick Start

### Installation
```bash
# Download and extract
wget https://github.com/estrelaisabellazion3/Zion-2.8/releases/download/v2.8.3/zion-cli-2.8.3-linux-amd64.tar.gz
tar -xzf zion-cli-2.8.3-linux-amd64.tar.gz

# Make executable
chmod +x zion-cli

# Test
./zion-cli --version
```

### Usage Examples

**Create Wallet:**
```bash
./zion-cli wallet --create
```

**Check Node Status:**
```bash
./zion-cli node --status
```

**Check Mining Hashrate:**
```bash
./zion-cli mine --hashrate
```

**Get Help:**
```bash
./zion-cli --help
./zion-cli wallet --help
./zion-cli node --help
./zion-cli mine --help
```

## 🌐 Network Information

**Testnet Launch:** November 15, 2025  
**RPC Endpoint:** https://api.zionterranova.com  
**Mining Pool:** pool.zionterranova.com:3333  
**Explorer:** https://explorer.zionterranova.com  

**Seed Nodes:**
- 91.98.122.165:8333 (Europe - Primary)

## 📝 System Requirements

**Minimum:**
- OS: Linux (Ubuntu 20.04+, Debian 11+, Fedora 36+)
- Architecture: x86_64 (amd64)
- RAM: 512 MB
- Disk: 50 MB

**Tested On:**
- ✅ Ubuntu 22.04 LTS
- ✅ Ubuntu 25.04
- ⏳ Debian 12 (pending)
- ⏳ Fedora 40 (pending)

## 🔐 Security

**Standalone Binary:**
- No external dependencies required
- Built with PyInstaller 6.16.0
- Python 3.13.3 embedded

**Verification:**
```bash
# SHA256 checksum
sha256sum zion-cli
# Expected: (will be added after final release)
```

**Source Code:**
- GitHub: https://github.com/estrelaisabellazion3/Zion-2.8
- License: MIT
- Reproducible builds: Coming soon

## 📚 Documentation

**Full Documentation:**
- [Quick Start Guide](../../docs/QUICK_START.md) - 5-minute setup
- [Mining Guide](../../docs/MINING_GUIDE.md) - Complete mining tutorial
- [RPC API Reference](../../docs/RPC_API.md) - API documentation
- [Architecture](../../docs/ARCHITECTURE.md) - Technical overview

**Community:**
- GitHub Issues: https://github.com/estrelaisabellazion3/Zion-2.8/issues
- Email: admin@zionterranova.com
- Website: https://zionterranova.com

## 🆘 Troubleshooting

**Binary won't execute:**
```bash
# Check permissions
chmod +x zion-cli

# Check architecture
file zion-cli
# Should show: ELF 64-bit LSB executable, x86-64
```

**"Command not found":**
```bash
# Use relative path
./zion-cli --help

# Or add to PATH
sudo mv zion-cli /usr/local/bin/
```

**Node connection failed:**
- Testnet launches November 15, 2025
- Check firewall rules (port 8333)
- Verify network connectivity

## 🔄 Updates

**Auto-Update:** Not available (manual download required)

**Check for Updates:**
```bash
# Current version
./zion-cli --version

# Latest release
curl -s https://api.github.com/repos/estrelaisabellazion3/Zion-2.8/releases/latest | grep tag_name
```

## 📋 Version History

**v2.8.3 (October 29, 2025)**
- Initial CLI binary release
- Wallet management commands
- Node status queries
- Mining control interface
- Linux x86_64 support

**Coming Soon:**
- Windows executable (.exe)
- macOS binary (arm64/x86_64)
- Full node binary (zion-node)
- GPU miner binary (zion-miner)

## 🎯 Roadmap

**Phase 3.2 (Current):**
- [x] CLI binary (Linux)
- [ ] Node binary (zion-node)
- [ ] Miner binary (zion-miner)
- [ ] Windows builds
- [ ] macOS builds

**Phase 3.3 (November 6-7):**
- [ ] Docker images
- [ ] docker-compose setup
- [ ] Multi-arch support

**Phase 4-6 (November 5-15):**
- [ ] Complete documentation
- [ ] Integration testing
- [ ] Security audit
- [ ] Public testnet launch

## ⚖️ License

MIT License - See [LICENSE](../../LICENSE) for details

---

**ZION 2.8.3 "Terra Nova" Testnet**  
*Building the future of humanitarian blockchain*

**Support:** admin@zionterranova.com  
**Website:** https://zionterranova.com  
**GitHub:** https://github.com/estrelaisabellazion3/Zion-2.8
