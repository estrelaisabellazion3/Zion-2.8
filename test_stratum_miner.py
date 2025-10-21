#!/usr/bin/env python3
"""
ZION Test Stratum Miner - Simple Python client to validate pool implementation
Updated: Standard port 3333 (not 3335)
"""

import socket
import json
import time

POOL_HOST = "localhost"
POOL_PORT = 3333
WALLET = "ZION_SACRED_B0FA7E2A234D8C2F08545F02295C98"

def send_message(sock, message):
    """Send JSON message to pool"""
    data = json.dumps(message) + "\n"
    print(f"📤 Sending: {data.strip()}")
    sock.sendall(data.encode())

def receive_message(sock):
    """Receive JSON message from pool"""
    data = b""
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
        if b"\n" in data:
            break
    
    if data:
        response = data.decode().strip()
        print(f"📥 Received: {response}")
        
        # Handle multiple JSON messages separated by newlines
        lines = response.split('\n')
        results = []
        for line in lines:
            if line.strip():
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parse error: {e}")
        
        return results[0] if len(results) == 1 else results
    return None

def main():
    print("=" * 80)
    print("🔥 ZION Stratum Test Miner")
    print("=" * 80)
    print(f"Pool: {POOL_HOST}:{POOL_PORT}")
    print(f"Wallet: {WALLET}")
    print("=" * 80)
    
    try:
        # Connect to pool
        print(f"\n🔌 Connecting to {POOL_HOST}:{POOL_PORT}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((POOL_HOST, POOL_PORT))
        print("✅ Connected!")
        
        # Step 1: Subscribe
        print("\n📝 Step 1: mining.subscribe")
        subscribe_msg = {
            "id": 1,
            "method": "mining.subscribe",
            "params": ["TestMiner/1.0"]
        }
        send_message(sock, subscribe_msg)
        response = receive_message(sock)
        
        if response and response.get('result'):
            print(f"✅ Subscribe successful!")
            print(f"   Extranonce1: {response['result'][1]}")
            print(f"   Extranonce2_size: {response['result'][2]}")
        
        # Step 2: Authorize
        print("\n🔐 Step 2: mining.authorize")
        authorize_msg = {
            "id": 2,
            "method": "mining.authorize",
            "params": [WALLET, "randomx"]
        }
        send_message(sock, authorize_msg)
        
        # Receive authorize response and job
        responses = receive_message(sock)
        if not isinstance(responses, list):
            responses = [responses]
        
        for response in responses:
            if response:
                if response.get('id') == 2:
                    if response.get('result'):
                        print(f"✅ Authorization successful!")
                    else:
                        print(f"❌ Authorization failed: {response.get('error')}")
                elif response.get('method') == 'mining.set_difficulty':
                    difficulty = response['params'][0]
                    print(f"⚙️  Difficulty set to: {difficulty}")
                elif response.get('method') == 'mining.notify':
                    job_id = response['params'][0]
                    print(f"💼 Received job: {job_id}")
        
        # Step 3: Submit fake share (testing)
        print("\n📊 Step 3: Submit test share")
        submit_msg = {
            "id": 3,
            "method": "mining.submit",
            "params": [
                WALLET,
                "zion_kp_000001",  # job_id
                "00000000",  # extranonce2
                "00000001",  # ntime
                "abcd1234"   # nonce (fake)
            ]
        }
        send_message(sock, submit_msg)
        response = receive_message(sock)
        
        if response:
            if response.get('result'):
                print(f"✅ Share accepted!")
            else:
                print(f"❌ Share rejected: {response.get('error')}")
        
        # Keep alive for a bit
        print("\n⏰ Waiting for more messages...")
        time.sleep(5)
        
        sock.close()
        print("\n✅ Test completed successfully!")
        
    except socket.timeout:
        print(f"❌ Connection timeout")
    except ConnectionRefusedError:
        print(f"❌ Connection refused - pool not running?")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
