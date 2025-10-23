#!/usr/bin/env python3
"""
ZION Cosmic Harmony Algorithm - Python Wrapper
Wraps C++ optimized implementation for use in Universal AI Miner

Architecture:
- Blake3 → Keccak-256 → SHA3-512 → Golden Ratio Matrix → Cosmic Fusion
- 5-stage hash process with PHI constants
- OpenSSL + BLAKE3 optimizations
"""

import os
import sys
import ctypes
import hashlib
import logging
from typing import Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import blake3 (pure Python fallback available)
try:
    import blake3
    BLAKE3_AVAILABLE = True
except ImportError:
    BLAKE3_AVAILABLE = False
    logger.warning("⚠️ blake3 module not available, using fallback implementation")

# Golden Ratio constant
PHI = 1.618033988749895
PHI_UINT32 = 0x9E3779B9  # Golden ratio in uint32
PHI_UINT64 = 0x9E3779B97F4A7C15  # Golden ratio in uint64


class CosmicHarmonyHasher:
    """
    Python wrapper for ZION Cosmic Harmony algorithm
    
    Provides two modes:
    1. C++ library mode (fast, uses compiled .so/.dylib)
    2. Pure Python mode (slower fallback, ~10-50x slower)
    """
    
    def __init__(self, use_cpp: bool = True):
        """
        Initialize Cosmic Harmony hasher
        
        Args:
            use_cpp: Try to load C++ library for performance
        """
        self.cpp_lib = None
        self.use_cpp = use_cpp
        
        if use_cpp:
            self._try_load_cpp_library()
        
        if self.cpp_lib:
            logger.info("✅ Cosmic Harmony: Using C++ optimized implementation")
        else:
            logger.info("⚙️ Cosmic Harmony: Using Python fallback implementation")
    
    def _try_load_cpp_library(self):
        """Try to load compiled C++ Cosmic Harmony library"""
        # Possible library paths
        lib_names = [
            'libcosmicharmony.so',      # Linux
            'libcosmicharmony.dylib',   # macOS
            'cosmicharmony.dll',        # Windows
        ]
        
        search_paths = [
            Path(__file__).parent,                                    # Same directory
            Path(__file__).parent / 'build',                         # Build directory
            Path(__file__).parent.parent.parent / 'build' / 'lib',  # Project build
        ]
        
        for search_path in search_paths:
            for lib_name in lib_names:
                lib_path = search_path / lib_name
                if lib_path.exists():
                    try:
                        self.cpp_lib = ctypes.CDLL(str(lib_path))
                        self._setup_cpp_functions()
                        logger.info(f"📚 Loaded C++ library: {lib_path}")
                        return
                    except Exception as e:
                        logger.debug(f"Failed to load {lib_path}: {e}")
        
        logger.debug("C++ library not found, using Python fallback")
    
    def _setup_cpp_functions(self):
        """Setup C++ function signatures"""
        if not self.cpp_lib:
            return
        
        try:
            # cosmic_hash function: (input, input_len, nonce, output)
            self.cpp_lib.cosmic_hash.argtypes = [
                ctypes.POINTER(ctypes.c_uint8),  # input
                ctypes.c_size_t,                  # input_len
                ctypes.c_uint32,                  # nonce
                ctypes.POINTER(ctypes.c_uint8)    # output (32 bytes)
            ]
            self.cpp_lib.cosmic_hash.restype = None
            
            # Initialize function
            if hasattr(self.cpp_lib, 'cosmic_harmony_initialize'):
                self.cpp_lib.cosmic_harmony_initialize.argtypes = []
                self.cpp_lib.cosmic_harmony_initialize.restype = ctypes.c_bool
                self.cpp_lib.cosmic_harmony_initialize()
                
        except Exception as e:
            logger.warning(f"Failed to setup C++ functions: {e}")
            self.cpp_lib = None
    
    def hash(self, input_data: bytes, nonce: int = 0) -> bytes:
        """
        Compute Cosmic Harmony hash
        
        Args:
            input_data: Block header or data to hash
            nonce: Mining nonce
            
        Returns:
            32-byte hash result
        """
        if self.cpp_lib:
            return self._hash_cpp(input_data, nonce)
        else:
            return self._hash_python(input_data, nonce)
    
    def _hash_cpp(self, input_data: bytes, nonce: int) -> bytes:
        """Hash using C++ library (fast)"""
        try:
            input_array = (ctypes.c_uint8 * len(input_data)).from_buffer_copy(input_data)
            output_array = (ctypes.c_uint8 * 32)()
            
            self.cpp_lib.cosmic_hash(
                input_array,
                len(input_data),
                ctypes.c_uint32(nonce),
                output_array
            )
            
            return bytes(output_array)
            
        except Exception as e:
            logger.error(f"C++ hash failed: {e}, falling back to Python")
            return self._hash_python(input_data, nonce)
    
    def _hash_python(self, input_data: bytes, nonce: int) -> bytes:
        """
        Hash using pure Python (slower fallback)
        
        Implements simplified Cosmic Harmony:
        1. Blake3 foundation
        2. Keccak-256 (via SHA3-256) galactic matrix
        3. SHA3-512 stellar harmony
        4. Golden ratio transformations
        5. Final Blake3 fusion
        """
        # Prepare input with nonce
        nonce_bytes = nonce.to_bytes(4, byteorder='little')
        nonce_input = input_data + nonce_bytes
        
        # Stage 1: Blake3 - Quantum Foundation
        if BLAKE3_AVAILABLE:
            blake3_hash = blake3.blake3(nonce_input).digest()
        else:
            # Fallback: SHA256 (not as good but works)
            blake3_hash = hashlib.sha256(nonce_input).digest()
        
        # Stage 2: Galactic Matrix Operations (Keccak-256 via SHA3-256)
        keccak_input = self._galactic_matrix_ops(blake3_hash)
        keccak_hash = hashlib.sha3_256(keccak_input).digest()
        
        # Stage 3: Stellar Harmony Processing (SHA3-512)
        stellar_input = self._stellar_harmony_process(keccak_hash)
        sha3_hash = hashlib.sha3_512(stellar_input).digest()
        
        # Stage 4: Golden Ratio Matrix Transformation
        golden_matrix = self._golden_matrix_transform(sha3_hash)
        
        # Stage 5: Compute Harmony Factor
        harmony_factor: int = 0
        for i in range(8):
            v = int(golden_matrix[i])  # ensure Python int, avoid numpy.uint64 to_bytes issues
            harmony_factor ^= (v >> 32) & 0xFFFFFFFF
            harmony_factor ^= v & 0xFFFFFFFF
        
        # Apply cosmic resonance
        harmony_factor = int((harmony_factor * PHI_UINT32) ^ int(nonce)) & 0xFFFFFFFF
        harmony_bytes = int(harmony_factor).to_bytes(4, byteorder='little')
        
        # Final: Cosmic Fusion
        fusion_input = (
            blake3_hash +      # 32 bytes
            keccak_hash +      # 32 bytes
            sha3_hash +        # 64 bytes
            golden_matrix.tobytes() +  # 64 bytes
            harmony_bytes +    # 4 bytes
            nonce_bytes        # 4 bytes
        )
        
        if BLAKE3_AVAILABLE:
            final_hash = blake3.blake3(fusion_input).digest()
        else:
            final_hash = hashlib.sha256(fusion_input).digest()
        
        return final_hash
    
    def _galactic_matrix_ops(self, input_hash: bytes) -> bytes:
        """Galactic matrix operations with golden ratio mixing"""
        temp = bytearray(input_hash)
        
        # Apply galactic matrix operations (4 rounds)
        for round_num in range(4):
            # Golden ratio mixing
            for i in range(len(temp)):
                phi_byte = (PHI_UINT64 >> (i % 64)) & 0xFF
                temp[i] ^= phi_byte
                temp[i] = ((temp[i] << 3) | (temp[i] >> 5)) & 0xFF
            
            # Galactic rotation
            carry = temp[0]
            temp[:-1] = temp[1:]
            temp[-1] = carry
        
        return bytes(temp)
    
    def _stellar_harmony_process(self, input_hash: bytes) -> bytes:
        """Stellar harmony processing with wave functions"""
        stellar_input = bytearray(input_hash)
        
        # Extend to 64 bytes with stellar field harmonics
        for i in range(32, 64):
            stellar_input.append(
                input_hash[i - 32] ^ ((PHI_UINT64 >> ((i * 8) % 64)) & 0xFF)
            )
        
        # Apply stellar wave functions (3 waves)
        for wave in range(3):
            for i in range(64):
                harmonic = stellar_input[i]
                harmonic ^= (harmonic << 1) | (harmonic >> 7)
                harmonic ^= (PHI_UINT32 >> ((wave * 8 + i) % 32)) & 0xFF
                stellar_input[i] = harmonic & 0xFF
        
        return bytes(stellar_input)
    
    def _golden_matrix_transform(self, input_hash: bytes) -> 'numpy.ndarray':
        """Golden ratio matrix transformation"""
        try:
            import numpy as np
            matrix = np.zeros(8, dtype=np.uint64)
        except ImportError:
            # Fallback without numpy
            matrix = [0] * 8
        
        # Initialize with PHI-based values
        for i in range(8):
            matrix[i] = (PHI_UINT64 * (i + 1)) & 0xFFFFFFFFFFFFFFFF
        
        # Transform matrix using input bytes (8 rounds)
        for round_num in range(8):
            for i in range(8):
                # Build input chunk from hash
                input_chunk = 0
                for j in range(8):
                    idx = (round_num * 8 + j) % len(input_hash)
                    input_chunk |= (input_hash[idx] << (j * 8))
                
                # Golden ratio transformation
                matrix[i] ^= input_chunk
                matrix[i] = ((matrix[i] * PHI_UINT64) ^ (matrix[i] >> 32)) & 0xFFFFFFFFFFFFFFFF
                matrix[i] = (matrix[i] + PHI_UINT64) & 0xFFFFFFFFFFFFFFFF
                
                # Matrix mixing
                if i > 0:
                    matrix[i] ^= matrix[i - 1]
            
            # Matrix rotation
            temp = matrix[0]
            matrix[:-1] = matrix[1:]
            matrix[-1] = temp
        
        try:
            import numpy as np
            return np.array(matrix, dtype=np.uint64)
        except ImportError:
            # Return as simple object with tobytes method
            class SimpleArray:
                def __init__(self, data):
                    self.data = data
                def tobytes(self):
                    return b''.join(x.to_bytes(8, 'little') for x in self.data)
            return SimpleArray(matrix)
    
    def check_difficulty(self, hash_result: bytes, target_difficulty: int) -> bool:
        """
        Check if hash meets difficulty target
        
        Args:
            hash_result: 32-byte hash
            target_difficulty: Number of leading zero bits required
            
        Returns:
            True if hash meets difficulty
        """
        # Calculate hash difficulty (number of leading zero bits)
        hash_difficulty = 0
        
        for byte_idx in range(31, -1, -1):
            byte_val = hash_result[byte_idx]
            if byte_val == 0:
                hash_difficulty += 8
            else:
                # Count leading zeros in this byte
                mask = 0x80
                while (byte_val & mask) == 0 and mask != 0:
                    hash_difficulty += 1
                    mask >>= 1
                break
        
        return hash_difficulty >= target_difficulty

    def check_target32(self, hash_result: bytes, target32: int) -> bool:
        """
        Check if first 4 bytes (little-endian) of hash_result are <= 32-bit target.
        This matches the GPU miner's placeholder/state[0] semantics used during bring-up.
        """
        if not hash_result or len(hash_result) < 4:
            return False
        state0 = int.from_bytes(hash_result[:4], 'little', signed=False)
        return state0 <= int(target32)


# Convenience functions
_global_hasher = None

def get_hasher(use_cpp: bool = True) -> CosmicHarmonyHasher:
    """Get global Cosmic Harmony hasher instance"""
    global _global_hasher
    if _global_hasher is None:
        _global_hasher = CosmicHarmonyHasher(use_cpp=use_cpp)
    return _global_hasher

def cosmic_hash(input_data: bytes, nonce: int = 0) -> bytes:
    """Quick hash function using global hasher"""
    return get_hasher().hash(input_data, nonce)

def check_hash_difficulty(hash_result: bytes, difficulty: int) -> bool:
    """Quick difficulty check using global hasher"""
    return get_hasher().check_difficulty(hash_result, difficulty)


# Test/benchmark code
if __name__ == "__main__":
    import time
    
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("🌟 ZION Cosmic Harmony Algorithm Test")
    print("=" * 60)
    
    # Test both implementations
    for use_cpp in [True, False]:
        mode = "C++" if use_cpp else "Python"
        print(f"\n{mode} Implementation:")
        print("-" * 60)
        
        hasher = CosmicHarmonyHasher(use_cpp=use_cpp)
        
        # Test hash
        test_data = b"ZION_TEST_BLOCK_HEADER_" + b"0" * 57  # 80 bytes
        test_nonce = 12345
        
        result = hasher.hash(test_data, test_nonce)
        print(f"Input:  {test_data[:20]}... ({len(test_data)} bytes)")
        print(f"Nonce:  {test_nonce}")
        print(f"Hash:   {result.hex()}")
        
        # Benchmark
        iterations = 1000 if use_cpp else 100
        start_time = time.time()
        
        for i in range(iterations):
            _ = hasher.hash(test_data, i)
        
        elapsed = time.time() - start_time
        hashrate = iterations / elapsed
        
        print(f"\nBenchmark ({iterations} hashes):")
        print(f"  Time:     {elapsed:.3f}s")
        print(f"  Hashrate: {hashrate:.2f} H/s")
        
        # Difficulty test
        difficulty = 8
        meets = hasher.check_difficulty(result, difficulty)
        print(f"\nDifficulty check (target={difficulty} bits): {meets}")
    
    print("\n" + "=" * 60)
    print("✅ Cosmic Harmony algorithm test complete!")
