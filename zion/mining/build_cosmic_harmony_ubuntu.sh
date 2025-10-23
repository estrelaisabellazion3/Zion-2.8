#!/bin/bash
# 🚀 Build ZION Cosmic Harmony Shared Library - Ubuntu Edition
# Complete automated build for Linux systems

set -e

echo "════════════════════════════════════════════════════════════"
echo "🔨 ZION Cosmic Harmony C++ Build System (Ubuntu/Linux)"
echo "════════════════════════════════════════════════════════════"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MINING_DIR="$SCRIPT_DIR/zion/mining"

echo "📍 Script location: $SCRIPT_DIR"
echo "📍 Mining directory: $MINING_DIR"
echo ""

# Check if we're in right directory
if [ ! -f "$MINING_DIR/zion-cosmic-harmony.cpp" ]; then
    echo "❌ Error: zion-cosmic-harmony.cpp not found in $MINING_DIR"
    echo "   Please run this script from the ZION project root"
    exit 1
fi

# ============================================================================
# Step 1: Check System Dependencies
# ============================================================================

echo "🔍 Checking system dependencies..."
echo ""

# Check compilers
if ! command -v g++ &> /dev/null; then
    echo "❌ g++ not found. Install with: sudo apt-get install build-essential"
    exit 1
fi
echo "✅ g++: $(g++ --version | head -1)"

if ! command -v gcc &> /dev/null; then
    echo "❌ gcc not found"
    exit 1
fi
echo "✅ gcc: $(gcc --version | head -1)"

# Check OpenSSL
if ! pkg-config --cflags --libs openssl >/dev/null 2>&1; then
    echo "❌ OpenSSL not found. Install with: sudo apt-get install libssl-dev"
    exit 1
fi
echo "✅ OpenSSL: $(openssl version)"

# Check CMake (optional)
if command -v cmake &> /dev/null; then
    echo "✅ CMake: $(cmake --version | head -1)"
else
    echo "⚠️  CMake not found (optional)"
fi

echo ""

# ============================================================================
# Step 2: Setup BLAKE3
# ============================================================================

echo "📦 Setting up BLAKE3..."
echo ""

BLAKE3_DIR="$MINING_DIR/external/blake3"
BLAKE3_LIB="$MINING_DIR/libblake3.a"

# Try to get BLAKE3 source
if [ ! -d "$BLAKE3_DIR" ]; then
    echo "🔹 Downloading BLAKE3 reference implementation..."
    
    # Try git first
    if git clone --depth 1 https://github.com/BLAKE3-team/BLAKE3.git "$BLAKE3_DIR" 2>/dev/null; then
        echo "✅ BLAKE3 downloaded from GitHub"
    else
        echo "⚠️  Could not clone BLAKE3 from GitHub"
        echo "   Will attempt to use system crypto only"
        BLAKE3_DIR=""
    fi
fi

# Build BLAKE3 if source exists
if [ -n "$BLAKE3_DIR" ] && [ -d "$BLAKE3_DIR/c" ]; then
    echo ""
    echo "🔨 Building BLAKE3 library..."
    
    cd "$BLAKE3_DIR/c"
    
    # Build BLAKE3 objects
    echo "   🔹 blake3.c"
    gcc -O3 -c blake3.c -o blake3.o
    
    echo "   🔹 blake3_dispatch.c"
    gcc -O3 -c blake3_dispatch.c -o blake3_dispatch.o
    
    echo "   🔹 blake3_portable.c"
    gcc -O3 -c blake3_portable.c -o blake3_portable.o
    
    # SIMD implementations (if supported)
    echo "   🔹 SIMD implementations..."
    gcc -O3 -msse2 -c blake3_sse2.c -o blake3_sse2.o 2>/dev/null || true
    gcc -O3 -msse4.1 -c blake3_sse41.c -o blake3_sse41.o 2>/dev/null || true
    gcc -O3 -mavx2 -c blake3_avx2.c -o blake3_avx2.o 2>/dev/null || true
    gcc -O3 -mavx512f -mavx512vl -c blake3_avx512.c -o blake3_avx512.o 2>/dev/null || true
    
    # Create static library
    echo "   🔗 Creating static library..."
    ar rcs libblake3.a blake3*.o
    
    # Copy to mining directory
    cp libblake3.a "$MINING_DIR/"
    echo "✅ BLAKE3 built successfully: $BLAKE3_LIB"
    
    cd "$SCRIPT_DIR"
else
    echo "⚠️  BLAKE3 source not available, will use system OpenSSL only"
fi

echo ""

# ============================================================================
# Step 3: Create Build Directory
# ============================================================================

echo "📁 Setting up build directory..."

BUILD_DIR="$MINING_DIR/build"
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

echo "✅ Build directory: $BUILD_DIR"
echo ""

# ============================================================================
# Step 4: Compiler Configuration
# ============================================================================

echo "🔧 Compiler configuration..."
echo ""

CXX=${CXX:-g++}
CC=${CC:-gcc}

# Detect CPU capabilities
CPU_FLAGS=""
if grep -q "avx2" /proc/cpuinfo 2>/dev/null; then
    CPU_FLAGS="-mavx2"
    echo "✅ CPU: AVX2 supported"
elif grep -q "sse4_1" /proc/cpuinfo 2>/dev/null; then
    CPU_FLAGS="-msse4.1"
    echo "✅ CPU: SSE4.1 supported"
elif grep -q "sse2" /proc/cpuinfo 2>/dev/null; then
    CPU_FLAGS="-msse2"
    echo "✅ CPU: SSE2 supported"
else
    echo "⚠️  CPU SIMD support not detected"
fi

CXXFLAGS="-std=c++17 -O3 -fPIC -DNDEBUG $CPU_FLAGS"
CCFLAGS="-O3 -fPIC -DNDEBUG $CPU_FLAGS"
INCLUDES="-I../include"
LIBS="-lssl -lcrypto -lpthread"

echo "CXX: $CXX"
echo "CXXFLAGS: $CXXFLAGS"
echo "INCLUDES: $INCLUDES"
echo "LIBS: $LIBS"
echo ""

# ============================================================================
# Step 5: Compile Cosmic Harmony
# ============================================================================

echo "🔨 Compiling Cosmic Harmony..."
echo ""

echo "   🔹 Cosmic Harmony (zion-cosmic-harmony.cpp)..."
if ! $CXX $CXXFLAGS $INCLUDES -c ../zion-cosmic-harmony.cpp -o cosmic_harmony.o; then
    echo "❌ Compilation failed!"
    echo ""
    echo "Common issues:"
    echo "   - Missing include files: check ../include/"
    echo "   - OpenSSL headers: sudo apt-get install libssl-dev"
    echo "   - C++17 support: upgrade compiler"
    exit 1
fi

echo "✅ Cosmic Harmony compiled"
echo ""

# ============================================================================
# Step 6: Create C Wrapper
# ============================================================================

echo "🔨 Creating C wrapper interface..."
echo ""

cat > cosmic_harmony_c_wrapper.cpp << 'WRAPPER_EOF'
#include "zion-cosmic-harmony.h"
#include <cstring>

extern "C" {

// C interface for Python ctypes binding

void cosmic_hash(const uint8_t* input, size_t input_len, uint32_t nonce, uint8_t* output) {
    if (input && output) {
        zion::CosmicHarmonyHasher::cosmic_hash(input, input_len, nonce, output);
    }
}

bool cosmic_harmony_initialize() {
    return zion::CosmicHarmonyHasher::initialize();
}

bool check_difficulty(const uint8_t* hash, uint64_t target_difficulty) {
    return zion::CosmicHarmonyHasher::check_difficulty(hash, target_difficulty);
}

} // extern "C"
WRAPPER_EOF

echo "   🔹 Compiling C wrapper..."
if ! $CXX $CXXFLAGS $INCLUDES -c cosmic_harmony_c_wrapper.cpp -o wrapper.o; then
    echo "❌ Wrapper compilation failed!"
    exit 1
fi

echo "✅ C wrapper compiled"
echo ""

# ============================================================================
# Step 7: Link Shared Library
# ============================================================================

echo "🔗 Linking shared library..."
echo ""

# Build link command
LINK_CMD="$CXX -shared $CXXFLAGS -o libcosmicharmony.so cosmic_harmony.o wrapper.o"

# Add BLAKE3 if available
if [ -f "../libblake3.a" ]; then
    LINK_CMD="$LINK_CMD ../libblake3.a"
    echo "   🔹 Including BLAKE3 library..."
fi

LINK_CMD="$LINK_CMD $LIBS"

echo "   Command: $LINK_CMD"
echo ""

if ! eval $LINK_CMD; then
    echo "❌ Linking failed!"
    exit 1
fi

echo "✅ Shared library created: libcosmicharmony.so"
echo ""

# ============================================================================
# Step 8: Verify Library
# ============================================================================

echo "🔍 Verifying library..."
echo ""

if [ ! -f "libcosmicharmony.so" ]; then
    echo "❌ libcosmicharmony.so not created!"
    exit 1
fi

echo "   📦 File info:"
file libcosmicharmony.so
echo ""

echo "   📚 Library dependencies:"
ldd libcosmicharmony.so | head -10
echo ""

echo "   🔧 Exported symbols:"
nm libcosmicharmony.so | grep "cosmic_" | head -5
echo ""

# ============================================================================
# Step 9: Copy to Final Location
# ============================================================================

echo "📦 Finalizing..."
echo ""

cp libcosmicharmony.so ../
echo "✅ Copied: ../libcosmicharmony.so"

# Make readable
chmod 644 libcosmicharmony.so ../libcosmicharmony.so

echo ""

# ============================================================================
# Step 10: Deployment Options
# ============================================================================

echo "📋 Next steps:"
echo ""
echo "1. Local use (recommended for development):"
echo "   Library is ready at: $MINING_DIR/libcosmicharmony.so"
echo ""
echo "2. System-wide installation:"
echo "   sudo cp $MINING_DIR/libcosmicharmony.so /usr/local/lib/"
echo "   sudo ldconfig"
echo ""
echo "3. Test the library:"
echo "   cd $SCRIPT_DIR"
echo "   python3 test_cosmic_harmony_quick.py"
echo ""
echo "4. Full integration test:"
echo "   python3 test_cosmic_harmony_integration.py"
echo ""

# ============================================================================
# Summary
# ============================================================================

echo "════════════════════════════════════════════════════════════"
echo "✅ BUILD COMPLETE!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📊 Results:"
echo "   ✅ BLAKE3 library: $([ -f ../libblake3.a ] && echo 'Built' || echo 'N/A')"
echo "   ✅ Cosmic Harmony: Compiled"
echo "   ✅ C wrapper: Compiled"
echo "   ✅ Shared library: $BUILD_DIR/libcosmicharmony.so"
echo ""
echo "🎯 Library size: $(ls -lh libcosmicharmony.so | awk '{print $5}')"
echo ""
