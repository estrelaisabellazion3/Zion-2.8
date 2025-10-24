#!/usr/bin/env python3
"""
Debug: Porovnání GPU vs Python wrapper hashu
- Vezme stejný header/nonce
- Spustí obě cesty
- Porovná byte-by-byte a hlásí kde se liší
"""

import sys
import os
import struct
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'zion', 'mining'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai', 'mining'))

from cosmic_harmony_wrapper import CosmicHarmonyHasher

print("=" * 80)
print("DEBUG: GPU vs Python Hash Comparison")
print("=" * 80)

# Python wrapper
print("\n1. Loading Python wrapper...")
py_hasher = CosmicHarmonyHasher(use_cpp=False)
print("   ✅ Python wrapper ready")

# Test data (80 bytes typical block header)
header = b"TEST_BLOCK_HEADER_123456789ABCDEFGHIJKLMNOP" + b"\x00" * 37
nonce = 0x12345678

print(f"\n2. Test input:")
print(f"   Header ({len(header)} bytes): {header[:32].hex()}...")
print(f"   Nonce: 0x{nonce:08x}")

# Python hash
py_hash = py_hasher.hash(header, nonce)
print(f"\n3. Python hash result ({len(py_hash)} bytes):")
print(f"   {py_hash.hex()}")

# Try GPU
print(f"\n4. GPU hash simulation:")
try:
    import pyopencl as cl
    
    # Simulate what GPU kernel does
    state = np.array([
        0x6A09E667,
        0xBB67AE85,
        0x3C6EF372,
        0xA54FF53A,
        0x510E527F,
        0x9B05688C,
        0x1F83D9AB,
        0x5BE0CD19,
    ], dtype=np.uint32)
    
    def rotl32(value, shift):
        value = value & 0xFFFFFFFF
        shift = shift & 31
        return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF
    
    def mix(a, b, c):
        return (rotl32((a ^ b) & 0xFFFFFFFF, 5) + (c & 0xFFFFFFFF)) & 0xFFFFFFFF
    
    # Prepare input
    padding = (-len(header)) % 4
    header_padded = header + (b"\x00" * padding)
    words = struct.unpack_from(f"<{len(header_padded) // 4}I", header_padded)
    
    # Stage 1: XOR header with state
    limit = min(len(words), 8)
    for i in range(limit):
        state[i] ^= words[i] & 0xFFFFFFFF
    
    state[0] ^= nonce & 0xFFFFFFFF
    state[1] ^= (nonce >> 16) & 0xFFFFFFFF
    
    # Stage 2: 12 rounds
    for _round in range(12):
        for i in range(8):
            state[i] = mix(state[i], state[(i + 1) % 8], state[(i + 2) % 8])
        for i in range(4):
            state[i], state[i + 4] = state[i + 4], state[i]
    
    # Stage 3: XOR mix
    xor_mix = 0
    for value in state:
        xor_mix ^= value
    for i in range(8):
        state[i] = (state[i] ^ xor_mix) & 0xFFFFFFFF
    
    # Stage 4: PHI multiply
    PHI = 0x9E3779B9
    for i in range(8):
        state[i] = (state[i] * PHI) & 0xFFFFFFFF
    
    gpu_hash = struct.pack('<8I', *state)
    
    print(f"   {gpu_hash.hex()}")
    
    # Compare
    print(f"\n5. Comparison:")
    if py_hash == gpu_hash:
        print(f"   ✅ HASHES MATCH!")
    else:
        print(f"   ❌ HASHES DIFFER")
        print(f"\n   Python:  {py_hash.hex()}")
        print(f"   GPU sim: {gpu_hash.hex()}")
        
        # Find first difference
        for i in range(min(len(py_hash), len(gpu_hash))):
            if py_hash[i] != gpu_hash[i]:
                print(f"\n   First difference at byte {i}:")
                print(f"     Python:  0x{py_hash[i]:02x}")
                print(f"     GPU sim: 0x{gpu_hash[i]:02x}")
                break
        
        # Compare as uint32 array
        py_u32 = struct.unpack('<8I', py_hash)
        gpu_u32 = struct.unpack('<8I', gpu_hash)
        print(f"\n   As uint32 array:")
        for i in range(8):
            match = "✅" if py_u32[i] == gpu_u32[i] else "❌"
            print(f"     [{i}] Python: 0x{py_u32[i]:08x} | GPU: 0x{gpu_u32[i]:08x} {match}")

except Exception as e:
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
