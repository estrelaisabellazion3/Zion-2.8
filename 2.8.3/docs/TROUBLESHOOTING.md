# 🔧 ZION Blockchain - Troubleshooting Guide

**Version:** 2.8.3 "Terra Nova"  
**Last Updated:** October 30, 2025

---

## 📋 Table of Contents

1. [Installation Issues](#installation-issues)
2. [Node Startup Problems](#node-startup-problems)
3. [RPC Connection Errors](#rpc-connection-errors)
4. [Mining Problems](#mining-problems)
5. [Wallet Issues](#wallet-issues)
6. [Network Problems](#network-problems)
7. [Performance Issues](#performance-issues)
8. [Database Errors](#database-errors)
9. [GPU Mining Troubleshooting](#gpu-mining-troubleshooting)
10. [Common Error Codes](#common-error-codes)

---

## 🚨 Installation Issues

### Problem: `pip install -r requirements.txt` fails

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solutions:**

1. **Check Python version:**
```bash
python --version
# Should be 3.10 or 3.11 (NOT 3.12)
```

2. **Upgrade pip:**
```bash
pip install --upgrade pip setuptools wheel
```

3. **Install dependencies one by one:**
```bash
pip install requests
pip install flask
pip install cryptography
# ... etc
```

4. **Use specific Python version:**
```bash
python3.11 -m venv venv_zion
source venv_zion/bin/activate
pip install -r requirements.txt
```

---

### Problem: Virtual environment not activating

**Symptoms:**
```
bash: venv_zion/bin/activate: No such file or directory
```

**Solutions:**

1. **Create virtual environment first:**
```bash
python3.11 -m venv venv_zion
```

2. **Check you're in correct directory:**
```bash
pwd
# Should be /home/zion/ZION or your project root
ls -la venv_zion/
```

3. **Use full path:**
```bash
source /home/zion/ZION/venv_zion/bin/activate
```

---

## 🌟 Node Startup Problems

### Problem: Port 8332 already in use

**Symptoms:**
```
OSError: [Errno 98] Address already in use
```

**Solutions:**

1. **Find process using port:**
```bash
lsof -ti:8332
# Shows process ID
```

2. **Kill the process:**
```bash
lsof -ti:8332 | xargs -r kill -9
```

3. **Use different port:**
```bash
python src/core/zion_rpc_server.py --port 8333
```

---

### Problem: Database locked error

**Symptoms:**
```
sqlite3.OperationalError: database is locked
```

**Solutions:**

1. **Close all ZION processes:**
```bash
pkill -f zion_rpc_server
sleep 2
```

2. **Remove lock file:**
```bash
rm -f zion_regtest.db-journal
```

3. **Check file permissions:**
```bash
chmod 644 zion_regtest.db
```

4. **Backup and recreate database:**
```bash
mv zion_regtest.db zion_regtest.db.backup
python src/core/zion_rpc_server.py
```

---

### Problem: Module not found errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'crypto_utils'
```

**Solutions:**

1. **Add project to PYTHONPATH:**
```bash
export PYTHONPATH="/home/zion/ZION:$PYTHONPATH"
```

2. **Run from project root:**
```bash
cd /home/zion/ZION
python src/core/zion_rpc_server.py
```

3. **Install missing packages:**
```bash
pip install -r requirements.txt
```

---

## 🔌 RPC Connection Errors

### Problem: Connection refused

**Symptoms:**
```
requests.exceptions.ConnectionError: Connection refused
```

**Solutions:**

1. **Check node is running:**
```bash
ps aux | grep zion_rpc_server
```

2. **Verify port:**
```bash
netstat -tuln | grep 8332
# Should show: 0.0.0.0:8332
```

3. **Test with localhost:**
```bash
curl http://127.0.0.1:8332
# Should return HTML or JSON
```

4. **Check firewall:**
```bash
sudo ufw status
sudo ufw allow 8332/tcp
```

---

### Problem: JSON-RPC error -32601 (Method not found)

**Symptoms:**
```json
{
  "error": {
    "code": -32601,
    "message": "Method not found"
  }
}
```

**Solutions:**

1. **Check method name spelling:**
```bash
# Correct:
{"method": "getblockcount"}

# Wrong:
{"method": "getBlockCount"}  # Capital letters
{"method": "get_block_count"}  # Underscores
```

2. **List available methods:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"help","params":[],"id":1}'
```

---

### Problem: Rate limit exceeded (-32)

**Symptoms:**
```json
{
  "error": {
    "code": -32,
    "message": "Rate limit exceeded"
  }
}
```

**Solutions:**

1. **Wait 60 seconds** (rate limit window)

2. **Reduce request frequency:**
```python
import time

for i in range(100):
    make_rpc_request()
    time.sleep(0.1)  # 100ms delay
```

3. **Batch requests:**
```bash
# Instead of multiple sendtoaddress calls, use sendmany
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"sendmany",
    "params":["", {"ZION_addr1": 10, "ZION_addr2": 20}],
    "id":1
  }'
```

---

## ⛏️ Mining Problems

### Problem: Low hashrate on GPU

**Symptoms:**
- Expected: 1 GH/s
- Actual: 100 MH/s (10x lower)

**Solutions:**

1. **Check GPU is being used:**
```bash
nvidia-smi
# Look for python process using GPU
```

2. **Increase intensity:**
```bash
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --intensity 95 \
  --address ZION_addr
```

3. **Check GPU temperature:**
```bash
nvidia-smi
# If temp > 85°C, GPU is throttling
```

4. **Update NVIDIA drivers:**
```bash
sudo ubuntu-drivers autoinstall
sudo reboot
```

5. **Check CUDA version:**
```bash
nvcc --version
# Should be 12.x
```

---

### Problem: GPU not detected

**Symptoms:**
```
RuntimeError: No CUDA-capable device is detected
```

**Solutions:**

1. **Verify GPU is visible:**
```bash
nvidia-smi
# Should show your GPU
```

2. **Check CuPy installation:**
```bash
python -c "import cupy; print(cupy.cuda.runtime.getDeviceCount())"
# Should print > 0
```

3. **Reinstall CuPy:**
```bash
pip uninstall cupy-cuda12x
pip install cupy-cuda12x
```

4. **Check CUDA environment:**
```bash
echo $CUDA_HOME
# Should be /usr/local/cuda-12.x

export PATH=/usr/local/cuda-12.6/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH
```

---

### Problem: Miner crashes after few minutes

**Symptoms:**
```
Segmentation fault (core dumped)
```

**Solutions:**

1. **Reduce overclock:**
```bash
# Reset GPU to default clocks
sudo nvidia-smi -pm 1  # Persistence mode
sudo nvidia-smi -rgc  # Reset graphics clock
sudo nvidia-smi -rmc  # Reset memory clock
```

2. **Lower intensity:**
```bash
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --intensity 80 \
  --address ZION_addr
```

3. **Check temps and power:**
```bash
watch -n 1 nvidia-smi
# Temp should be < 85°C
# Power should be < rated TDP
```

4. **Enable low-memory mode:**
```bash
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --low-memory \
  --address ZION_addr
```

---

### Problem: High reject rate (> 5%)

**Symptoms:**
```
Accepted: 450 (90%)
Rejected: 50 (10%)  ← Too high!
```

**Solutions:**

1. **Check network latency:**
```bash
ping pool.zion.sacred
# Should be < 50ms
```

2. **Reduce intensity:**
```bash
--intensity 80  # Down from 95
```

3. **Use closer pool:**
```bash
# If in Europe, use EU pool
--pool stratum+tcp://eu.zionpool.io:3333
```

4. **Sync system time:**
```bash
sudo apt install ntpdate
sudo ntpdate pool.ntp.org
```

---

## 💰 Wallet Issues

### Problem: Address validation fails

**Symptoms:**
```json
{
  "error": {
    "code": -1,
    "message": "Invalid address"
  }
}
```

**Solutions:**

1. **Check address format:**
```bash
# Valid formats:
ZION_abc123def456...  (ZION_ + 40+ hex chars)
0x1234567890abcdef... (Plain 64/66 hex)

# Invalid:
zion_abc123...  (lowercase prefix)
ZION_xyz...     (non-hex characters)
```

2. **Validate address:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"validateaddress",
    "params":["ZION_your_address_here"],
    "id":1
  }'
```

---

### Problem: Insufficient funds (-6)

**Symptoms:**
```json
{
  "error": {
    "code": -6,
    "message": "Insufficient funds"
  }
}
```

**Solutions:**

1. **Check balance:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getbalance","params":["*"],"id":1}'
```

2. **Wait for confirmations:**
```bash
# Mining rewards require 100 confirmations
# Check transaction confirmations:
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"gettransaction",
    "params":["txid_here"],
    "id":1
  }'
```

3. **List unspent outputs:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"listunspent","params":[],"id":1}'
```

---

### Problem: Balance shows 0 after mining

**Symptoms:**
- Mined 10 blocks
- Balance still shows 0

**Solutions:**

1. **Check confirmations required:**
```bash
# Mining rewards need 100 confirmations
# If you mined block 50, need to reach block 150
```

2. **Generate more blocks:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"generate","params":[100],"id":1}'
```

3. **Check transaction list:**
```bash
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"listtransactions","params":["*",100],"id":1}'
```

---

## 🌐 Network Problems

### Problem: Cannot connect to peers

**Symptoms:**
```
getpeerinfo returns empty array
```

**Solutions:**

1. **Check network mode:**
```bash
# In regtest mode, there are no peers
# For peer connections, use testnet or mainnet
python src/core/zion_rpc_server.py --network testnet
```

2. **Add seed nodes:**
```bash
# Edit seednodes.py
SEED_NODES = [
    "seed1.zion.sacred:8333",
    "seed2.zion.sacred:8333"
]
```

3. **Check firewall:**
```bash
sudo ufw allow 8333/tcp
sudo ufw status
```

---

## ⚡ Performance Issues

### Problem: Slow RPC responses (> 1 second)

**Symptoms:**
```
getblock taking 2-3 seconds
```

**Solutions:**

1. **Add database indexes:**
```sql
CREATE INDEX IF NOT EXISTS idx_blocks_height ON blocks(height);
CREATE INDEX IF NOT EXISTS idx_blocks_hash ON blocks(hash);
CREATE INDEX IF NOT EXISTS idx_tx_block ON transactions(block_hash);
```

2. **Vacuum database:**
```bash
sqlite3 zion_regtest.db "VACUUM;"
```

3. **Use SSD storage:**
```bash
# Move database to SSD
mv zion_regtest.db /mnt/ssd/
ln -s /mnt/ssd/zion_regtest.db .
```

4. **Increase SQLite cache:**
```python
# In zion_rpc_server.py
conn.execute("PRAGMA cache_size = -64000")  # 64MB cache
```

---

### Problem: High memory usage (> 4 GB)

**Symptoms:**
```
python process using 8 GB RAM
```

**Solutions:**

1. **Clear transaction pool:**
```python
blockchain.mempool.clear()
```

2. **Limit UTXO cache:**
```python
blockchain.utxo_cache = {}  # Clear cache
```

3. **Restart node periodically:**
```bash
# Add to crontab
0 3 * * * /path/to/restart_node.sh
```

4. **Use memory profiler:**
```bash
pip install memory_profiler
python -m memory_profiler src/core/zion_rpc_server.py
```

---

## 🗄️ Database Errors

### Problem: Database corruption

**Symptoms:**
```
sqlite3.DatabaseError: database disk image is malformed
```

**Solutions:**

1. **Attempt recovery:**
```bash
sqlite3 zion_regtest.db ".recover" | sqlite3 zion_recovered.db
mv zion_regtest.db zion_corrupt.db
mv zion_recovered.db zion_regtest.db
```

2. **Restore from backup:**
```bash
cp backups/zion_regtest_20251030.db zion_regtest.db
```

3. **Rebuild blockchain:**
```bash
rm zion_regtest.db
python src/core/zion_rpc_server.py
# Will create new genesis block
```

---

### Problem: Foreign key constraint failed

**Symptoms:**
```
sqlite3.IntegrityError: FOREIGN KEY constraint failed
```

**Solutions:**

1. **Disable foreign keys temporarily:**
```sql
PRAGMA foreign_keys = OFF;
-- Fix data
PRAGMA foreign_keys = ON;
```

2. **Check data consistency:**
```sql
-- Find orphaned transactions
SELECT txid FROM transactions 
WHERE block_hash NOT IN (SELECT hash FROM blocks);
```

3. **Re-import blockchain:**
```bash
python scripts/reindex_blockchain.py
```

---

## 🎮 GPU Mining Troubleshooting

### Problem: Out of memory error

**Symptoms:**
```
cupy.cuda.memory.OutOfMemoryError: Out of memory
```

**Solutions:**

1. **Enable low-memory mode:**
```bash
python src/mining/cosmic_harmony_miner.py \
  --gpu \
  --low-memory \
  --address ZION_addr
```

2. **Reduce batch size:**
```bash
--threads 4096 --blocks 128  # Down from 8192/256
```

3. **Close other GPU applications:**
```bash
# Check what's using GPU
nvidia-smi
# Kill unnecessary processes
```

4. **Use smaller GPU:**
```bash
# If you have multiple GPUs, use one with more free VRAM
--device 1
```

---

### Problem: GPU temperature too high (> 90°C)

**Symptoms:**
```
nvidia-smi shows 92°C
Mining crashes
```

**Solutions:**

1. **Reduce intensity:**
```bash
--intensity 70  # Down from 95
```

2. **Lower power limit:**
```bash
sudo nvidia-smi -pl 250  # Reduce to 250W
```

3. **Improve cooling:**
```bash
# Set fan to 80%
sudo nvidia-settings -a "[gpu:0]/GPUFanControlState=1"
sudo nvidia-settings -a "[fan:0]/GPUTargetFanSpeed=80"
```

4. **Undervolt GPU:**
```bash
# Use MSI Afterburner or nvidia-smi
sudo nvidia-smi -lgc 1800  # Lock core to 1800MHz
```

---

## 📋 Common Error Codes

### JSON-RPC Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| `-32700` | Parse error | Check JSON syntax |
| `-32600` | Invalid request | Verify JSON-RPC format |
| `-32601` | Method not found | Check method name spelling |
| `-32602` | Invalid params | Verify parameter types |
| `-32603` | Internal error | Check server logs |
| `-1` | Invalid address | Validate address format |
| `-3` | Invalid amount | Amount must be > 0 |
| `-5` | Resource not found | Block/TX doesn't exist |
| `-6` | Insufficient funds | Not enough balance |
| `-8` | Invalid parameter | Check param range/format |
| `-32` | Rate limit exceeded | Wait 60 seconds |

---

### HTTP Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| `404` | Not found | Check URL/endpoint |
| `429` | Too many requests | Rate limit - wait |
| `500` | Internal server error | Check server logs |
| `503` | Service unavailable | Node may be syncing |

---

## 🆘 Getting Help

### Debug Information to Collect

When reporting issues, include:

```bash
# 1. System info
uname -a
lsb_release -a

# 2. Python version
python --version

# 3. ZION version
cat VERSION

# 4. Node status
curl -X POST http://127.0.0.1:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getblockchaininfo","params":[],"id":1}'

# 5. GPU info (if mining)
nvidia-smi

# 6. Recent logs
tail -100 zion.log

# 7. Error message (full stack trace)
```

### Support Resources

- **Documentation:** [2.8.3/docs/](../docs/)
- **GitHub Issues:** https://github.com/estrelaisabellazion3/Zion-2.8/issues
- **Community Forum:** https://github.com/estrelaisabellazion3/Zion-2.8/discussions

### Diagnostic Tools

```bash
# Run diagnostic script
python scripts/diagnostics.py

# Test suite
pytest tests/integration/ -v

# Network test
python scripts/test_network.py

# Mining test
python scripts/test_mining.py --gpu --duration 60
```

---

## 💡 Best Practices

### Preventing Issues

1. ✅ **Keep backups** - Daily database backups
2. ✅ **Monitor logs** - Check for errors daily
3. ✅ **Update regularly** - Keep software current
4. ✅ **Test changes** - Use regtest before mainnet
5. ✅ **Monitor resources** - CPU, RAM, disk space
6. ✅ **Secure node** - Firewall, strong passwords
7. ✅ **Document config** - Keep notes on changes

### Performance Tips

1. ⚡ Use SSD storage
2. ⚡ Add database indexes
3. ⚡ Enable connection pooling
4. ⚡ Cache frequently accessed data
5. ⚡ Optimize SQL queries
6. ⚡ Use faster JSON library (ujson)
7. ⚡ Enable gzip compression

---

**🙏 JAI RAM SITA HANUMAN - SOLVE ALL PROBLEMS! ⭐**

*Comprehensive troubleshooting for ZION 2.8.3 blockchain*
