#!/usr/bin/env python3
"""Quick test of pool login"""
import socket
import json
import time

host = "91.98.122.165"
port = 3333

print(f"🔌 Connecting to {host}:{port}...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((host, port))
    print("✅ Connected!")
    
    # Send login
    login_msg = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "login",
        "params": {
            "login": "ZionQuickTest2025",
            "pass": "x",
            "agent": "quick-test/1.0"
        }
    }
    
    print(f"📤 Sending: {json.dumps(login_msg)}")
    sock.sendall((json.dumps(login_msg) + '\n').encode('utf-8'))
    
    # Receive response
    print("📥 Waiting for response...")
    data = sock.recv(4096)
    print(f"✅ Received {len(data)} bytes:")
    print(data.decode('utf-8', errors='replace'))
    
    sock.close()
    print("✅ Test complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
