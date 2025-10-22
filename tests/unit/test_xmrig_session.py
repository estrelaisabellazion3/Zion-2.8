#!/usr/bin/env python3
"""
Continuous test of XMRig protocol login - pokus se přihlásit, počkat na job, ukončit
"""
import socket
import json
import time
import sys

def test_xmrig_session(host: str, port: int) -> bool:
    """Celá session: connect → login → wait for jobs → disconnect"""
    
    print(f"🔌 Connecting to {host}:{port}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    
    try:
        sock.connect((host, port))
        print("✅ Connected!")
        
        # 1. Poslat login
        login_request = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "login",
            "params": {
                "login": "ZION_CONTINUOUS_TEST",
                "pass": "x",
                "agent": "XMRig/6.22.2",
                "algo": ["rx/0"]
            }
        }
        
        print(f"📤 Sending login...")
        sock.sendall((json.dumps(login_request) + '\n').encode('utf-8'))
        
        # 2. Počkat na response bundle
        print("⏳ Waiting for login response...")
        sock.settimeout(5)
        response = sock.recv(8192).decode('utf-8')
        
        print(f"📥 Received ({len(response)} bytes)")
        
        # Parse všechny JSON zprávy
        job_id = None
        for raw in [line.strip() for line in response.splitlines() if line.strip()]:
            try:
                data = json.loads(raw)
                method = data.get('method')
                
                if 'result' in data and data['result']:
                    result = data['result']
                    print(f"✅ Login OK! ID: {result.get('id')}")
                    if 'job' in result:
                        job = result['job']
                        job_id = job.get('job_id')
                        print(f"   Job: {job_id}")
                        
                elif method == 'mining.set_difficulty':
                    diff = data.get('params', [])[0] if data.get('params') else 'N/A'
                    print(f"   Difficulty: {diff}")
                    
                elif method == 'job':
                    params = data.get('params', {})
                    jid = params.get('job_id', 'N/A')
                    print(f"   New job: {jid}")
                    job_id = jid
                    
            except json.JSONDecodeError:
                continue
        
        if not job_id:
            print("❌ No job received!")
            return False
            
        # 3. Čekat na další joby (periodic jobs)
        print("⏳ Waiting for periodic jobs (10s)...")
        sock.settimeout(15)
        
        for i in range(2):  # Čekat na 2 další joby
            try:
                data = sock.recv(4096).decode('utf-8')
                if data:
                    print(f"📨 Received more data ({len(data)} bytes)")
                    for line in data.splitlines():
                        if line.strip():
                            try:
                                msg = json.loads(line.strip())
                                if msg.get('method') == 'job':
                                    jid = msg.get('params', {}).get('job_id', 'N/A')
                                    print(f"   Periodic job: {jid}")
                            except:
                                pass
            except socket.timeout:
                print("⏱️  Timeout - no more jobs")
                break
                
        print("✅ Session complete!")
        return True
            
    except socket.timeout:
        print("❌ Timeout")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "91.98.122.165"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 3333
    
    print(f"🎯 Testing XMRig session: {host}:{port}")
    print("=" * 60)
    
    success = test_xmrig_session(host, port)
    
    if success:
        print("\n🎉 Test PASSED - Pool handshake works!")
        exit(0)
    else:
        print("\n❌ Test FAILED - Pool handshake broken")
        exit(1)
