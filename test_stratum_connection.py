#!/usr/bin/env python3
"""Test Stratum connection to pool"""
import socket
import json
import time

HOST = "91.98.122.165"
PORT = 3333

print(f"🔌 Connecting to {HOST}:{PORT}...")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((HOST, PORT))
    print(f"✅ Connected!")
    
    # Send mining.subscribe request
    request = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "mining.subscribe",
        "params": ["xmrig-test/2.8.1", None]
    }
    
    sock.sendall((json.dumps(request) + "\n").encode())
    print(f"📤 Sent: {request['method']}")
    
    # Wait for response
    response = sock.recv(1024).decode()
    print(f"📥 Received: {response[:100]}...")
    
    # Send mining.authorize
    auth_request = {
        "id": 2,
        "jsonrpc": "2.0",
        "method": "mining.authorize",
        "params": ["ZION_TEST_WALLET", "x"]
    }
    
    sock.sendall((json.dumps(auth_request) + "\n").encode())
    print(f"📤 Sent: {auth_request['method']}")
    
    # Wait for response
    response = sock.recv(1024).decode()
    print(f"📥 Received: {response[:100]}...")
    
    print("\n✅ Stratum protocol working!")
    
    sock.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
