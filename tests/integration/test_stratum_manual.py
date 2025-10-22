#!/usr/bin/env python3
"""
Minimal Stratum client test - ověří, jestli pool správně odpovídá
"""
import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)

try:
    print("Connecting to 127.0.0.1:3333 ...")
    sock.connect(("127.0.0.1", 3333))
    print("✅ Connected!")
    
    # Receive welcome
    print("Waiting for welcome message...")
    welcome = sock.recv(1024).decode('utf-8')
    print(f"Received: {welcome}")
    
    # Send login with valid ZION address format
    login = json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "login",
        "params": {
            "login": "Z" + "a" * 63,  # Valid 64-char ZION address
            "pass": "x",
            "agent": "XMRig/6.22.2"
        }
    }) + "\n"
    print(f"Sending login: {login}")
    sock.sendall(login.encode('utf-8'))
    
    # Receive response
    print("Waiting for login response...")
    response = sock.recv(1024).decode('utf-8')
    print(f"Received: {response}")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    sock.close()
