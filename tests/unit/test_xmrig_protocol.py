#!/usr/bin/env python3
"""Test XMrig protocol (ne Stratum!)"""
import socket
import json

HOST = "91.98.122.165"
PORT = 3333

print(f"🔌 Connecting to {HOST}:{PORT} (XMrig protocol)...")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((HOST, PORT))
    print(f"✅ Connected!")
    
    # Send login (XMrig protocol, not Stratum)
    login_msg = {
        "id": "1",
        "method": "login",
        "params": {
            "login": "ZION_XMRIG_TEST",
            "pass": "x",
            "agent": "xmrig/6.22.2"
        }
    }
    
    sock.sendall((json.dumps(login_msg) + "\n").encode())
    print(f"📤 Sent XMrig login...")
    
    # Wait for response
    response = sock.recv(1024).decode()
    print(f"📥 Response: {response[:200]}...")
    
    print("\n✅ XMrig protocol working!")
    sock.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
