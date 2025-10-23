#!/usr/bin/env python3
"""
Test WARP Engine API Server
"""

import requests
import time
import subprocess
import signal
import sys

def test_warp_api():
    """Test WARP Engine API endpoints"""

    print("🚀 Starting WARP Engine for API testing...")

    # Start WARP Engine in background
    process = subprocess.Popen(
        ['python3', 'zion_warp_engine_core.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    try:
        # Wait for engine to start
        print("⏳ Waiting for WARP Engine to initialize...")
        time.sleep(15)  # Increased wait time

        # Test health endpoint
        print("\n🩺 Testing /health endpoint...")
        try:
            response = requests.get('http://localhost:8080/health', timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                print("✅ Health endpoint working!")
                print(f"   Status: {health_data.get('status')}")
                print(f"   Uptime: {health_data.get('uptime_seconds', 0):.0f}s")
                print(f"   Blockchain Height: {health_data.get('blockchain_height')}")
                print(f"   RPC Active: {health_data.get('rpc_active')}")
                print(f"   P2P Active: {health_data.get('p2p_active')}")
            else:
                print(f"❌ Health endpoint returned status {response.status_code}")
        except Exception as e:
            print(f"❌ Health endpoint failed: {e}")

        # Test status endpoint
        print("\n📊 Testing /status endpoint...")
        try:
            response = requests.get('http://localhost:8080/status', timeout=5)
            if response.status_code == 200:
                status_data = response.json()
                print("✅ Status endpoint working!")
                print(f"   System Health: {status_data.get('system_health')}")
                print(f"   Memory Usage: {status_data.get('memory_usage_mb', 0):.1f} MB")
                print(f"   CPU Usage: {status_data.get('cpu_usage_percent', 0):.1f}%")
            else:
                print(f"❌ Status endpoint returned status {response.status_code}")
        except Exception as e:
            print(f"❌ Status endpoint failed: {e}")

        # Test invalid endpoint
        print("\n❓ Testing invalid endpoint...")
        try:
            response = requests.get('http://localhost:8080/invalid', timeout=5)
            if response.status_code == 404:
                print("✅ 404 handling working correctly")
            else:
                print(f"⚠️  Unexpected status for invalid endpoint: {response.status_code}")
        except Exception as e:
            print(f"❌ Invalid endpoint test failed: {e}")

    finally:
        # Clean shutdown
        print("\n🛑 Stopping WARP Engine...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

        print("✅ Test complete")

if __name__ == "__main__":
    test_warp_api()