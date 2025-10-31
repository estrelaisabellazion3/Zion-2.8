#!/usr/bin/env python3
"""
Quick test for v2.8.4 RPC getalgorithms endpoint
Tests unified blockchain migration and ASIC-resistant algo support
"""

import json
import urllib.request
import urllib.error

RPC_URL = "http://localhost:8545"

def rpc_call(method, params=None):
    """Make RPC call"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or []
    }
    
    req = urllib.request.Request(
        RPC_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print(f"❌ Connection error: {e}")
        print(f"   Make sure ZION node is running on {RPC_URL}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_algorithms_endpoint():
    """Test new getalgorithms RPC method (v2.8.4)"""
    print("🧪 Testing v2.8.4 RPC getalgorithms endpoint...\n")
    
    response = rpc_call("getalgorithms")
    
    if not response:
        return False
    
    if 'error' in response and response['error']:
        print(f"❌ RPC Error: {response['error']}")
        return False
    
    result = response.get('result', {})
    
    print("✅ RPC getalgorithms response:")
    print(json.dumps(result, indent=2))
    print()
    
    # Validate response structure
    assert 'supported' in result, "Missing 'supported' field"
    assert 'default' in result, "Missing 'default' field"
    assert 'asic_resistant' in result, "Missing 'asic_resistant' field"
    
    # Validate ASIC-resistant policy
    assert result['asic_resistant'] is True, "ASIC-resistant should be True"
    assert result['default'] == 'cosmic_harmony', "Default should be cosmic_harmony"
    
    supported = result['supported']
    assert 'cosmic_harmony' in supported, "cosmic_harmony should be in supported list"
    
    # SHA256 should NOT be supported (ASIC resistance)
    if 'sha256' in supported and supported['sha256']:
        print("⚠️  WARNING: SHA256 is listed as supported (violates ASIC-resistant policy)")
        return False
    
    print("✅ All validations passed!")
    print(f"   Default algorithm: {result['default']}")
    print(f"   Active algorithm: {result.get('active', 'N/A')}")
    print(f"   ASIC-resistant: {result['asic_resistant']}")
    print(f"   Supported algorithms: {list(supported.keys())}")
    
    return True

def test_blockchain_info():
    """Test basic blockchain info (compatibility check)"""
    print("\n🧪 Testing blockchain compatibility...\n")
    
    response = rpc_call("getblockcount")
    
    if not response:
        return False
    
    if 'error' in response and response['error']:
        print(f"❌ RPC Error: {response['error']}")
        return False
    
    block_count = response.get('result', 0)
    print(f"✅ Blockchain accessible: {block_count} blocks")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("ZION v2.8.4 - RPC Algorithm Endpoint Test")
    print("=" * 60)
    print()
    
    # Test basic connectivity
    if not test_blockchain_info():
        print("\n❌ Basic RPC connectivity failed")
        print("   Start node with: python3 src/core/new_zion_blockchain.py")
        exit(1)
    
    # Test new algorithms endpoint
    if not test_algorithms_endpoint():
        print("\n❌ Algorithms endpoint test failed")
        exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! v2.8.4 RPC migration successful")
    print("=" * 60)
