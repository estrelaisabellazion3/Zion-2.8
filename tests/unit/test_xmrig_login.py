#!/usr/bin/env python3
"""
Test XMRig protocol login - simulace XMRig klienta
"""
import socket
import json
import time
import argparse

def test_xmrig_login(host: str, port: int) -> bool:
    """Test přihlášení pomocí XMRig protokolu"""

    print(f"🔌 Connecting to {host}:{port}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    
    try:
        sock.connect((host, port))
        print("✅ Connected!")

        # Počkat chvíli (pool by měl poslat welcome, ale podle Node.js pool to NEPOSÍLÁ)
        time.sleep(1)

        # Poslat XMRig login request
        login_request = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "login",
            "params": {
                "login": "ZION_TEST_WALLET_1234567890ABCDEF01234567",
                "pass": "x",
                "agent": "XMRig/6.22.2",
                "algo": ["rx/0"]
            }
        }

        print(f"📤 Sending login: {json.dumps(login_request)}")
        sock.sendall((json.dumps(login_request) + '\n').encode('utf-8'))

        # Počkat na odpověď
        print("⏳ Waiting for response...")
        sock.settimeout(5)
        response = sock.recv(4096).decode('utf-8')

        print(f"📥 Received: {response}")

        # Parse all JSON messages in the chunk
        success = False
        for raw in [line.strip() for line in response.splitlines() if line.strip()]:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as decode_error:
                print(f"❌ JSON decode error for chunk: {raw} -> {decode_error}")
                continue

            method = data.get('method')
            if method and not data.get('result'):
                print(f"ℹ️  Notice: method={method}, params={data.get('params')}")

            if 'result' in data and data['result']:
                result = data['result']
                print("✅ Login successful!")
                print(f"   ID: {result.get('id', 'N/A')}")
                print(f"   Status: {result.get('status', 'N/A')}")
                if 'job' in result:
                    job = result['job']
                    print(f"   Job ID: {job.get('job_id', 'N/A')}")
                    print(f"   Blob: {job.get('blob', 'N/A')[:40]}...")
                success = True
                break

        if success:
            return True

        print("❌ Login failed: žádná result zpráva")
        return False

    except socket.timeout:
        print("❌ Timeout waiting for response")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test XMRig login handshake")
    parser.add_argument("host", nargs="?", default="127.0.0.1", help="Pool host")
    parser.add_argument("port", nargs="?", type=int, default=3333, help="Pool port")
    args = parser.parse_args()

    success = test_xmrig_login(args.host, args.port)
    exit(0 if success else 1)
