#!/usr/bin/env python3
"""
2min mining test - start local pool and GPU miner, log stats every 10s
"""
import sys
import os
import time
import subprocess

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai', 'mining'))

# Ensure clean pool DB
os.system("rm -f zion_pool.db 2>/dev/null")

# Set core mode (pool uses direct state0<=target32 validation path)
os.environ['ZION_CH_CORE'] = '1'

print("=" * 80)
print("🌟 2-MINUTE GPU MINING TEST - Pool + Miner")
print("=" * 80)

# Start pool
print("\n1. Starting mining pool...")
pool_env = os.environ.copy()
pool_proc = subprocess.Popen(
    [sys.executable, "zion_universal_pool_v2.py"],
    env=pool_env,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
    bufsize=1
)

# Wait for pool to be ready (up to 20s)
ready = False
start_wait = time.time()
while time.time() - start_wait < 20:
    line = pool_proc.stdout.readline()
    if not line:
        time.sleep(0.2)
        continue
    l = line.strip()
    if l:
        print(f"[POOL] {l}")
    if "ZION Universal Mining Pool started on port" in l:
        ready = True
        break
    if "address already in use" in l.lower():
        print("[POOL] Port already in use - assuming pool already running")
        ready = True
        break
    if "error" in l.lower():
        # keep reading; minor errors may not be fatal
        pass
if not ready:
    print("⚠️ Pool readiness not confirmed, proceeding anyway...")

# Start miner
print("2. Starting GPU miner (2 minutes)...")
from ai.mining.cosmic_harmony_gpu_miner import ZionGPUMiner
miner = ZionGPUMiner()
if not miner.start_mining():
    print("❌ Failed to start miner")
    pool_proc.terminate()
    sys.exit(1)

# Run for 2 minutes
print("3. Mining for 2 minutes...")
start_time = time.time()
last_stats = time.time()

try:
    while time.time() - start_time < 120:  # 2 minutes
        elapsed = time.time() - start_time
        if time.time() - last_stats >= 10:
            stats = miner.get_stats()
            print(f"[{int(elapsed):3d}s] {stats['hashrate']} | Shares: {stats['shares']} | "
                  f"Hashes: {stats['total_hashes']:,} | GPU: {stats.get('gpu_temp_c')}°C | "
                  f"Kt: {stats.get('kernel_time_ms_last')}ms | RTT: {stats.get('submit_latency_ms_last')}ms")
            last_stats = time.time()
        time.sleep(1)
except KeyboardInterrupt:
    print("\n⏹️  Interrupted by user")

# Stop
print("\n4. Stopping mining...")
miner.stop_mining()
# Give a moment to flush
time.sleep(1)

# Final stats
final = miner.get_stats()
print("\n" + "=" * 80)
print("FINAL STATS:")
print(f"  Total hashes: {final['total_hashes']:,}")
print(f"  Hashrate: {final['hashrate']}")
print(f"  Shares found: {final['shares']}")
print(f"  Uptime: {final['uptime']:.1f}s")
print("=" * 80)

# Stop pool
try:
    pool_proc.terminate()
    pool_proc.wait(timeout=5)
except Exception:
    pass

print("\n✅ Test complete")
