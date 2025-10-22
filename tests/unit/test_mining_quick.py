#!/usr/bin/env python3
"""
Quick mining sanity test: start CPU RandomX against production pool for ~20s
"""
import time
import hashlib
import secrets
from ai.zion_universal_miner import ZionUniversalMiner, MiningMode

def gen_wallet():
    seed = secrets.token_hex(32)
    return 'ZION_' + hashlib.sha256(seed.encode()).hexdigest()[:20].upper()

if __name__ == "__main__":
    wallet = gen_wallet()
    pool = "91.98.122.165:3333"
    print(f"Wallet: {wallet}")
    miner = ZionUniversalMiner(mode=MiningMode.CPU_ONLY)
    res = miner.start_mining(pool_url=pool, wallet_address=wallet, algorithm="randomx")
    print(res)
    time.sleep(20)
    print(miner.get_status())
    print("Stopping...")
    print(miner.stop_mining())
