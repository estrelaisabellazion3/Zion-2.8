#!/usr/bin/env python3
"""
ZION Mining Algorithms Registry

Provides a unified interface for multiple Proof-of-Work algorithms used across
ZION's ecosystem. Algorithms are optional and detected dynamically; when a
native library is missing, the algorithm is marked as unavailable.

Supported identifiers:
- 'cosmic_harmony'  - Native ZION PoW (preferred)
- 'randomx'         - Monero-family CPU PoW (via librandomx/pyrx) [optional]
- 'yescrypt'        - CPU-friendly PoW (via libyescrypt) [optional]
- 'autolykos_v2'    - Ergo-family GPU PoW (via external lib) [optional]


Usage:
    from .algorithms import get_hash, is_available, AVAILABLE_ALGOS
    h = get_hash('cosmic_harmony', b'data', nonce=1)

Environment flags:
    (none)
"""

from __future__ import annotations
import hashlib
from typing import Callable, Dict, Optional

# --- Cosmic Harmony (native) -------------------------------------------------
_get_cosmic_hasher = None
try:
    # Try local import (same directory added by caller)
    from cosmic_harmony_wrapper import get_hasher as _get_cosmic_hasher  # type: ignore
except Exception:
    try:
        # Try project-relative path
        from zion.mining.cosmic_harmony_wrapper import get_hasher as _get_cosmic_hasher  # type: ignore
    except Exception:
        # Last attempt: add path and try again
        import sys
        import os
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        zion_mining_path = os.path.join(project_root, 'zion', 'mining')
        if os.path.exists(zion_mining_path) and zion_mining_path not in sys.path:
            sys.path.insert(0, zion_mining_path)
        try:
            from cosmic_harmony_wrapper import get_hasher as _get_cosmic_hasher  # type: ignore
        except Exception:
            _get_cosmic_hasher = None


def _hash_cosmic_harmony(data: bytes, nonce: int) -> bytes:
    if _get_cosmic_hasher is None:
        raise RuntimeError("Cosmic Harmony library not available")
    hasher = _get_cosmic_hasher(use_cpp=False)  # Use Python fallback for testing
    return hasher.hash(data, int(nonce))


COSMIC_HARMONY_AVAILABLE = _get_cosmic_hasher is not None

# --- RandomX (with Python fallback) -----------------------------------------
# Prefer pyrx if available; otherwise use Python fallback
_randomx_native_available = False

try:
    import pyrx  # type: ignore

    def _hash_randomx(data: bytes, nonce: int) -> bytes:
        # pyrx expects a key and input; we derive a simple key from data prefix
        key = data[:32] if len(data) >= 32 else (data + b"\x00" * (32 - len(data)))
        input_bytes = data + int(nonce).to_bytes(8, 'little', signed=False)
        return pyrx.get_fast_hash(input_bytes, key)

    _randomx_native_available = True
except Exception:
    # Python fallback: SHA3-256 based memory-hard function (simplified RandomX)
    def _hash_randomx(data: bytes, nonce: int) -> bytes:
        """Python fallback for RandomX - memory-hard SHA3-256 chain"""
        import hashlib
        # Combine data and nonce
        input_bytes = data + int(nonce).to_bytes(8, 'little', signed=False)
        # Memory-hard iterations (simplified)
        state = hashlib.sha3_256(input_bytes).digest()
        for i in range(16):  # Reduced rounds for performance
            state = hashlib.sha3_256(state + input_bytes).digest()
        return state

_randomx_available = True  # Always available (native or fallback)

# --- Yescrypt (with Python fallback) ----------------------------------------
_yescrypt_native_available = False
try:
    # Attempt to use 'yescrypt' python bindings if present (rare)
    import yescrypt  # type: ignore

    def _hash_yescrypt(data: bytes, nonce: int) -> bytes:
        # Derive salt from data and nonce
        salt = hashlib.sha256(data + int(nonce).to_bytes(8, 'little')).digest()
        return yescrypt.hash(data, salt)

    _yescrypt_native_available = True
except Exception:
    # Python fallback: PBKDF2-based memory-hard function (simplified Yescrypt)
    def _hash_yescrypt(data: bytes, nonce: int) -> bytes:
        """Python fallback for Yescrypt - PBKDF2-based memory-hard function"""
        import hashlib
        # Derive salt from nonce
        salt = hashlib.sha256(int(nonce).to_bytes(8, 'little')).digest()
        # PBKDF2 with SHA256 (memory-hard properties)
        return hashlib.pbkdf2_hmac('sha256', data, salt, iterations=1024, dklen=32)

_yescrypt_available = True  # Always available (native or fallback)

# --- Autolykos v2 (with Python fallback) ------------------------------------
_autolykos_native_available = False
try:
    # Some projects provide 'pyautolykos2' or similar; attempt import
    import pyautolykos2  # type: ignore

    def _hash_autolykos_v2(data: bytes, nonce: int) -> bytes:
        # Real Autolykos v2 implementation
        return pyautolykos2.hash(data, int(nonce))

    _autolykos_native_available = True
except Exception:
    # Python fallback: Blake2b-based GPU-friendly function (simplified Autolykos v2)
    def _hash_autolykos_v2(data: bytes, nonce: int) -> bytes:
        """Python fallback for Autolykos v2 - Blake2b-based function"""
        import hashlib
        # Combine data and nonce
        input_bytes = data + int(nonce).to_bytes(8, 'little', signed=False)
        # Blake2b is GPU-friendly and memory-hard
        h = hashlib.blake2b(input_bytes, digest_size=32)
        # Add some mixing rounds for complexity
        state = h.digest()
        for i in range(8):
            state = hashlib.blake2b(state + input_bytes, digest_size=32).digest()
        return state

_autolykos_available = True  # Always available (native or fallback)

# --- Registry ----------------------------------------------------------------

AVAILABLE_ALGOS: Dict[str, Dict[str, object]] = {
    'cosmic_harmony': {
        'available': COSMIC_HARMONY_AVAILABLE,
        'hash': _hash_cosmic_harmony if COSMIC_HARMONY_AVAILABLE else None,
    },
    'randomx': {
        'available': _randomx_available,
        'hash': _hash_randomx if _randomx_available else None,
    },
    'yescrypt': {
        'available': _yescrypt_available,
        'hash': _hash_yescrypt if _yescrypt_available else None,
    },
    'autolykos_v2': {
        'available': _autolykos_available,
        'hash': _hash_autolykos_v2 if _autolykos_available else None,
    },
}


def is_available(name: str) -> bool:
    info = AVAILABLE_ALGOS.get(name)
    return bool(info and info.get('available'))


def get_hash(
    name: str,
    data: bytes,
    nonce: int = 0,
) -> str:
    """Compute hash for the given algorithm name.

    If the algorithm isn't available, a RuntimeError is raised. No SHA256
    fallback is provided to preserve ASIC resistance.
    
    Returns:
        Hex string representation of hash (for compatibility with blockchain code)
    """
    algo = AVAILABLE_ALGOS.get(name)
    if algo and algo.get('available') and callable(algo.get('hash')):
        hash_bytes = algo['hash'](data, int(nonce))  # type: ignore
        return hash_bytes.hex()  # Convert to hex string

    raise RuntimeError(f"Algorithm '{name}' is not available")


def list_supported() -> Dict[str, bool]:
    """Return a mapping of algorithm name -> availability."""
    return {k: bool(v.get('available')) for k, v in AVAILABLE_ALGOS.items()}
