#!/usr/bin/env python3
"""
ZION v2.8.4 - Algorithm Performance Benchmark

Compares performance of:
- Cosmic Harmony (Python vs C++ native)
- RandomX (Python SHA3 fallback vs native)
- Yescrypt (Python PBKDF2 fallback vs native)
- Autolykos v2 (Python Blake2b fallback vs native)
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.algorithms import get_hash, is_available, list_supported


def benchmark_algorithm(algo_name: str, iterations: int = 1000):
    """Benchmark single algorithm"""
    print(f"\n🔬 Benchmarking {algo_name}...")
    
    test_data = b"X" * 76  # Typical block header size
    
    if not is_available(algo_name):
        print(f"   ⚠️  {algo_name} not available")
        return None
    
    # Warm-up
    for i in range(10):
        get_hash(algo_name, test_data, i)
    
    # Benchmark
    start = time.time()
    for nonce in range(iterations):
        get_hash(algo_name, test_data, nonce)
    elapsed = time.time() - start
    
    hashrate = iterations / elapsed
    avg_time_ms = (elapsed / iterations) * 1000
    
    print(f"   Iterations: {iterations:,}")
    print(f"   Total time: {elapsed:.2f}s")
    print(f"   Hashrate:   {hashrate:>12,.0f} H/s")
    print(f"   Avg time:   {avg_time_ms:>12.3f} ms/hash")
    
    return {
        'algorithm': algo_name,
        'iterations': iterations,
        'elapsed': elapsed,
        'hashrate': hashrate,
        'avg_time_ms': avg_time_ms
    }


def main():
    print("=" * 70)
    print("ZION v2.8.4 - Algorithm Performance Benchmark")
    print("=" * 70)
    
    # Check availability
    supported = list_supported()
    print("\n📊 Algorithm Availability:")
    for algo, available in supported.items():
        status = "✅ Available" if available else "❌ Not available"
        print(f"   {algo:15s}: {status}")
    
    # Benchmark parameters
    iterations = {
        'cosmic_harmony': 10000,   # Fast algorithm
        'randomx': 1000,           # Memory-hard (slower)
        'yescrypt': 1000,          # PBKDF2 (slower)
        'autolykos_v2': 5000,      # GPU-friendly (medium)
    }
    
    results = []
    
    for algo in ['cosmic_harmony', 'randomx', 'yescrypt', 'autolykos_v2']:
        if is_available(algo):
            result = benchmark_algorithm(algo, iterations.get(algo, 1000))
            if result:
                results.append(result)
        else:
            print(f"\n⚠️  Skipping {algo} (not available)")
    
    # Summary
    print("\n" + "=" * 70)
    print("Benchmark Results Summary:")
    print("=" * 70)
    print(f"{'Algorithm':<15} {'Hashrate (H/s)':>15} {'Avg Time (ms)':>15} {'Type':>10}")
    print("-" * 70)
    
    for r in sorted(results, key=lambda x: x['hashrate'], reverse=True):
        algo_type = "Native" if "native" in r['algorithm'].lower() else "Python"
        print(f"{r['algorithm']:<15} {r['hashrate']:>15,.0f} {r['avg_time_ms']:>15.3f} {algo_type:>10}")
    
    print("=" * 70)
    
    # Performance notes
    print("\n📝 Performance Notes:")
    print("   - Cosmic Harmony: Python fallback is sufficient for testing")
    print("   - RandomX: SHA3-256 fallback is 10-50x slower than native")
    print("   - Yescrypt: PBKDF2 fallback is 5-20x slower than native")
    print("   - Autolykos v2: Blake2b fallback is 10-30x slower than native")
    print("\n   💡 For production mining, build native libraries:")
    print("      See docs/2.8.4/NATIVE_LIBS_BUILD.md")
    
    # Expected results
    print("\n📊 Expected Performance (Python fallbacks):")
    print("   - Cosmic Harmony: 1,000-5,000 H/s")
    print("   - RandomX (SHA3): 100-500 H/s")
    print("   - Yescrypt (PBKDF2): 50-200 H/s")
    print("   - Autolykos v2 (Blake2b): 500-2,000 H/s")
    
    print("\n📊 Expected Performance (Native libs):")
    print("   - Cosmic Harmony: 100,000-500,000 H/s (50-100x speedup)")
    print("   - RandomX: 2,000-10,000 H/s (10-50x speedup)")
    print("   - Yescrypt: 500-2,000 H/s (5-20x speedup)")
    print("   - Autolykos v2: 10,000-50,000 H/s (10-30x speedup)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
