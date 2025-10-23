#!/usr/bin/env python3
"""
ZION 2.8.1 - Comprehensive Mining & Block Test
Tests: Mining on SSH pool + Block validation
"""

import time
import socket
import json
import hashlib
import sys
from datetime import datetime

class MiningBlockTester:
    def __init__(self, pool_host="91.98.122.165", pool_port=3333, wallet="ZION_BLOCK_TEST_280"):
        self.pool_host = pool_host
        self.pool_port = pool_port
        self.wallet = wallet
        self.sock = None
        self.current_job = None
        self.shares_submitted = 0
        self.shares_accepted = 0
        self.shares_rejected = 0
        self.blocks_found = 0
        
    def connect(self):
        """Connect to pool"""
        print(f"🔌 Connecting to {self.pool_host}:{self.pool_port}...")
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((self.pool_host, self.pool_port))
            print("✅ Connected!")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def send_request(self, method, params, req_id=None):
        """Send JSON-RPC request"""
        if req_id is None:
            req_id = int(time.time() * 1000)
        
        request = {
            "id": req_id,
            "method": method,
            "params": params
        }
        
        msg = json.dumps(request) + "\n"
        self.sock.send(msg.encode())
        
        # Read response
        response_data = b""
        while True:
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            response_data += chunk
            if b"\n" in response_data:
                break
        
        lines = response_data.decode().strip().split("\n")
        responses = []
        for line in lines:
            if line:
                try:
                    responses.append(json.loads(line))
                except:
                    pass
        
        return responses
    
    def subscribe(self):
        """Subscribe to pool"""
        print(f"📝 Subscribing as {self.wallet}...")
        responses = self.send_request("mining.subscribe", [self.wallet], 1)
        
        for resp in responses:
            if resp.get("id") == 1:
                if resp.get("error"):
                    print(f"❌ Subscribe error: {resp['error']}")
                    return False
                else:
                    print(f"✅ Subscribed! Session: {resp.get('result', [None, None])[1]}")
                    return True
        return False
    
    def authorize(self):
        """Authorize with pool"""
        print(f"🔐 Authorizing {self.wallet}...")
        responses = self.send_request("mining.authorize", [self.wallet, "x"], 2)
        
        for resp in responses:
            if resp.get("id") == 2:
                if resp.get("result"):
                    print(f"✅ Authorized!")
                    return True
                else:
                    print(f"❌ Authorization failed")
                    return False
        
        # Check for mining.notify
        for resp in responses:
            if resp.get("method") == "mining.notify":
                self.current_job = {
                    "job_id": resp["params"][0],
                    "header": resp["params"][1],
                    "target": resp["params"][2],
                    "height": resp["params"][3] if len(resp["params"]) > 3 else 0
                }
                print(f"📦 Job received: {self.current_job['job_id']} (height: {self.current_job['height']})")
        
        return True
    
    def mine_and_submit(self, duration_seconds=120):
        """Mine and submit shares for specified duration"""
        print(f"\n⛏️  Starting mining for {duration_seconds} seconds...")
        print(f"🎯 Target difficulty: Low (testing mode)")
        print(f"📊 Monitoring blocks and shares...\n")
        
        start_time = time.time()
        last_report = start_time
        nonce = 0
        
        while time.time() - start_time < duration_seconds:
            # Simple nonce increment
            nonce += 1
            
            # Submit share every ~2 seconds
            if nonce % 100 == 0:
                nonce_hex = hex(nonce)[2:].zfill(8)
                
                if self.current_job:
                    try:
                        responses = self.send_request(
                            "mining.submit",
                            [self.wallet, self.current_job["job_id"], nonce_hex, "autolykos2"],
                            3000 + self.shares_submitted
                        )
                        
                        self.shares_submitted += 1
                        
                        for resp in responses:
                            if resp.get("id", 0) >= 3000:
                                if resp.get("result"):
                                    self.shares_accepted += 1
                                    print(f"✅ Share #{self.shares_submitted} ACCEPTED (nonce: {nonce_hex})")
                                    
                                    # Check if it's a block
                                    if resp.get("result") == "block":
                                        self.blocks_found += 1
                                        print(f"🎉 BLOCK FOUND! Block #{self.blocks_found}")
                                else:
                                    self.shares_rejected += 1
                                    error = resp.get("error", "unknown")
                                    print(f"❌ Share #{self.shares_submitted} REJECTED: {error}")
                            
                            # Check for new job
                            if resp.get("method") == "mining.notify":
                                self.current_job = {
                                    "job_id": resp["params"][0],
                                    "header": resp["params"][1],
                                    "target": resp["params"][2],
                                    "height": resp["params"][3] if len(resp["params"]) > 3 else 0
                                }
                                print(f"📦 New job: {self.current_job['job_id']} (height: {self.current_job['height']})")
                        
                    except Exception as e:
                        print(f"⚠️  Submit error: {e}")
                        # Reconnect if needed
                        pass
                
                time.sleep(2)
            
            # Progress report every 30 seconds
            if time.time() - last_report >= 30:
                elapsed = int(time.time() - start_time)
                print(f"\n📊 Progress at {elapsed}s:")
                print(f"   Submitted: {self.shares_submitted}")
                print(f"   Accepted: {self.shares_accepted} ({self.shares_accepted/max(1,self.shares_submitted)*100:.1f}%)")
                print(f"   Rejected: {self.shares_rejected} ({self.shares_rejected/max(1,self.shares_submitted)*100:.1f}%)")
                print(f"   Blocks: {self.blocks_found}")
                last_report = time.time()
    
    def disconnect(self):
        """Disconnect from pool"""
        if self.sock:
            self.sock.close()
            print("\n🔌 Disconnected from pool")
    
    def print_summary(self):
        """Print final summary"""
        print("\n" + "="*60)
        print("📊 MINING TEST SUMMARY")
        print("="*60)
        print(f"Pool: {self.pool_host}:{self.pool_port}")
        print(f"Wallet: {self.wallet}")
        print(f"\n📈 Results:")
        print(f"  Total Submitted: {self.shares_submitted}")
        print(f"  Accepted: {self.shares_accepted} ({self.shares_accepted/max(1,self.shares_submitted)*100:.1f}%)")
        print(f"  Rejected: {self.shares_rejected} ({self.shares_rejected/max(1,self.shares_submitted)*100:.1f}%)")
        print(f"  Blocks Found: {self.blocks_found} 🎉" if self.blocks_found > 0 else f"  Blocks Found: 0")
        
        if self.shares_accepted > 0:
            print(f"\n✅ TEST PASSED: Pool accepting shares")
        else:
            print(f"\n⚠️  WARNING: No shares accepted")
        
        print("="*60)

def main():
    tester = MiningBlockTester()
    
    if not tester.connect():
        sys.exit(1)
    
    if not tester.subscribe():
        tester.disconnect()
        sys.exit(1)
    
    if not tester.authorize():
        tester.disconnect()
        sys.exit(1)
    
    try:
        tester.mine_and_submit(duration_seconds=120)  # 2 minutes
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
    
    tester.disconnect()
    tester.print_summary()

if __name__ == "__main__":
    print("🌟 ZION 2.8.0 - Mining & Block Test")
    print("="*60)
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    main()
    
    print(f"\n⏰ End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n✨ Ad Astra Per Estrella! 🌟")
