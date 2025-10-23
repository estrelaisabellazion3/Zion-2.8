#!/bin/bash
# ZION 2.8.1 - Complete Mining Library Build Script
# Compiles: Cosmic Harmony, Yescrypt, RandomX, and all mining components
# Platform: Linux (Ubuntu 20.04+)

set -e

echo "🚀 ZION 2.8.1 Mining Libraries - Complete Build"
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"
BUILD_DIR="$PROJECT_ROOT/build_zion"
LIB_DIR="$BUILD_DIR/lib"
BIN_DIR="$BUILD_DIR/bin"

echo -e "${YELLOW}Project Root: $PROJECT_ROOT${NC}"
echo -e "${YELLOW}Build Directory: $BUILD_DIR${NC}"

# Create build directories
mkdir -p "$BUILD_DIR" "$LIB_DIR" "$BIN_DIR"

# ============================================================================
# PHASE 1: System Dependencies Check
# ============================================================================
echo ""
echo -e "${GREEN}[PHASE 1] Checking System Dependencies${NC}"

check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ $1 found${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 NOT found${NC}"
        return 1
    fi
}

check_command "gcc" || exit 1
check_command "g++" || exit 1
check_command "cmake" || exit 1
check_command "make" || exit 1
check_command "python3" || exit 1
check_command "openssl" || exit 1

echo -e "${GREEN}✅ All dependencies found${NC}"

# ============================================================================
# PHASE 2: BLAKE3 Library Build
# ============================================================================
echo ""
echo -e "${GREEN}[PHASE 2] Building BLAKE3 Library${NC}"

BLAKE3_DIR="$BUILD_DIR/blake3"
if [ ! -d "$BLAKE3_DIR" ]; then
    echo "📦 Cloning BLAKE3 repository..."
    git clone --depth 1 https://github.com/BLAKE3-team/BLAKE3.git "$BLAKE3_DIR" 2>/dev/null || {
        echo -e "${YELLOW}⚠️ Failed to clone BLAKE3, skipping${NC}"
    }
fi

if [ -d "$BLAKE3_DIR/c" ]; then
    echo "🔨 Compiling BLAKE3..."
    cd "$BLAKE3_DIR/c"
    
    # Compile BLAKE3 sources
    gcc -O3 -fPIC -c blake3.c -o blake3.o
    gcc -O3 -fPIC -c blake3_dispatch.c -o blake3_dispatch.o
    gcc -O3 -fPIC -c blake3_portable.c -o blake3_portable.o
    
    # Try architecture-specific optimizations
    gcc -O3 -fPIC -msse2 -c blake3_sse2.c -o blake3_sse2.o 2>/dev/null || true
    gcc -O3 -fPIC -msse4.1 -c blake3_sse41.c -o blake3_sse41.o 2>/dev/null || true
    gcc -O3 -fPIC -mavx2 -c blake3_avx2.c -o blake3_avx2.o 2>/dev/null || true
    gcc -O3 -fPIC -mavx512f -c blake3_avx512.c -o blake3_avx512.o 2>/dev/null || true
    
    # Create static library
    ar rcs libblake3.a blake3*.o
    
    # Copy to build lib directory
    cp libblake3.a "$LIB_DIR/"
    cp blake3.h "$BUILD_DIR/include/" 2>/dev/null || mkdir -p "$BUILD_DIR/include" && cp blake3.h "$BUILD_DIR/include/"
    
    echo -e "${GREEN}✅ BLAKE3 compiled${NC}"
    cd "$SCRIPT_DIR"
fi

# ============================================================================
# PHASE 3: Cosmic Harmony C++ Library Build
# ============================================================================
echo ""
echo -e "${GREEN}[PHASE 3] Building Cosmic Harmony Library${NC}"

if [ -f "$PROJECT_ROOT/zion/mining/zion-cosmic-harmony.cpp" ]; then
    COSMIC_BUILD_DIR="$BUILD_DIR/cosmic_harmony"
    mkdir -p "$COSMIC_BUILD_DIR"
    cd "$COSMIC_BUILD_DIR"
    
    echo "🔨 Compiling Cosmic Harmony..."
    
    # Compiler flags
    CXX=${CXX:-g++}
    CXXFLAGS="-std=c++17 -O3 -fPIC -march=native -DNDEBUG"
    INCLUDES="-I$PROJECT_ROOT/zion/mining/include"
    LIBS="-lssl -lcrypto -lpthread"
    
    # Add BLAKE3 if available
    if [ -f "$LIB_DIR/libblake3.a" ]; then
        INCLUDES="$INCLUDES -I$BUILD_DIR/include"
        LIBS="$LIBS $LIB_DIR/libblake3.a"
    fi
    
    # Compile Cosmic Harmony
    $CXX $CXXFLAGS $INCLUDES -c "$PROJECT_ROOT/zion/mining/zion-cosmic-harmony.cpp" -o cosmic_harmony.o
    
    # Create C wrapper
    cat > cosmic_harmony_c_wrapper.cpp << 'WRAPEOF'
#include "zion-cosmic-harmony.h"
#include <cstring>

extern "C" {

void cosmic_hash(const uint8_t* input, size_t input_len, uint32_t nonce, uint8_t* output) {
    zion::CosmicHarmonyHasher::cosmic_hash(input, input_len, nonce, output);
}

bool cosmic_harmony_initialize() {
    return zion::CosmicHarmonyHasher::initialize();
}

bool check_difficulty(const uint8_t* hash, uint64_t target_difficulty) {
    return zion::CosmicHarmonyHasher::check_difficulty(hash, target_difficulty);
}

}
WRAPEOF
    
    $CXX $CXXFLAGS $INCLUDES -c cosmic_harmony_c_wrapper.cpp -o wrapper.o
    
    # Link shared library
    $CXX -shared $CXXFLAGS -o libcosmicharmony.so cosmic_harmony.o wrapper.o $LIBS
    
    # Copy to lib directory
    cp libcosmicharmony.so "$LIB_DIR/"
    
    echo -e "${GREEN}✅ Cosmic Harmony compiled${NC}"
    cd "$SCRIPT_DIR"
else
    echo -e "${YELLOW}⚠️ Cosmic Harmony source not found${NC}"
fi

# ============================================================================
# PHASE 4: Yescrypt Library Build (if C extension exists)
# ============================================================================
echo ""
echo -e "${GREEN}[PHASE 4] Building Yescrypt Library${NC}"

if [ -f "$PROJECT_ROOT/zion/mining/yescrypt.c" ] || [ -f "$PROJECT_ROOT/zion/mining/yescrypt_fast.c" ]; then
    YESCRYPT_BUILD_DIR="$BUILD_DIR/yescrypt"
    mkdir -p "$YESCRYPT_BUILD_DIR"
    cd "$YESCRYPT_BUILD_DIR"
    
    echo "🔨 Compiling Yescrypt..."
    
    # Find yescrypt sources
    YESCRYPT_SRC=""
    for src in "$PROJECT_ROOT/zion/mining/yescrypt"*.c; do
        if [ -f "$src" ]; then
            YESCRYPT_SRC="$YESCRYPT_SRC $src"
        fi
    done
    
    if [ -n "$YESCRYPT_SRC" ]; then
        gcc -O3 -fPIC -pthread -march=native $YESCRYPT_SRC -c -o yescrypt.o
        gcc -shared -o libyescrypt.so yescrypt.o
        cp libyescrypt.so "$LIB_DIR/"
        echo -e "${GREEN}✅ Yescrypt compiled${NC}"
    fi
    
    cd "$SCRIPT_DIR"
else
    echo -e "${YELLOW}⚠️ Yescrypt source not found${NC}"
fi

# ============================================================================
# PHASE 5: RandomX Library Build (if available)
# ============================================================================
echo ""
echo -e "${GREEN}[PHASE 5] Building RandomX Library${NC}"

if [ -d "$PROJECT_ROOT/zion/mining/randomx" ] || [ -f "$PROJECT_ROOT/zion/mining/randomx.cpp" ]; then
    echo "📦 RandomX library build skipped (using system/Python version)"
else
    echo -e "${YELLOW}⚠️ RandomX source not found${NC}"
fi

# ============================================================================
# PHASE 6: Copy Headers
# ============================================================================
echo ""
echo -e "${GREEN}[PHASE 6] Setting up Headers${NC}"

mkdir -p "$BUILD_DIR/include"
cp "$PROJECT_ROOT/zion/mining/include/"*.h "$BUILD_DIR/include/" 2>/dev/null || true

echo -e "${GREEN}✅ Headers installed${NC}"

# ============================================================================
# PHASE 7: Summary and Verification
# ============================================================================
echo ""
echo -e "${GREEN}[PHASE 7] Build Summary${NC}"

echo ""
echo "📦 Generated Libraries:"
ls -lh "$LIB_DIR/" 2>/dev/null || echo "  (No libraries built)"

echo ""
echo "📚 Installed Headers:"
ls -lh "$BUILD_DIR/include/" 2>/dev/null || echo "  (No headers installed)"

# ============================================================================
# PHASE 8: Copy to Mining Directory for Python
# ============================================================================
echo ""
echo -e "${GREEN}[PHASE 8] Installing Python Wrappers${NC}"

# Copy compiled libraries to mining directory for Python to find
if [ -d "$LIB_DIR" ]; then
    find "$LIB_DIR" -name "*.so" -exec cp {} "$PROJECT_ROOT/zion/mining/" \;
    echo -e "${GREEN}✅ Libraries copied to zion/mining/${NC}"
fi

# ============================================================================
# FINAL: Test Python Integration
# ============================================================================
echo ""
echo -e "${GREEN}[FINAL] Testing Python Integration${NC}"

cd "$PROJECT_ROOT"

python3 << 'PYTHONEOF'
import sys
import os

print("\n📋 Python Library Check:")
print("=" * 50)

# Check Cosmic Harmony
try:
    sys.path.insert(0, 'zion/mining')
    from cosmic_harmony_wrapper import get_hasher
    hasher = get_hasher()
    test_hash = hasher.hash(b"test")
    print(f"✅ Cosmic Harmony: {type(hasher).__name__}")
except Exception as e:
    print(f"⚠️ Cosmic Harmony: {str(e)[:50]}")

# Check other modules
for module_name in ['yescrypt_fast', 'randomx_engine']:
    try:
        mod = __import__(module_name)
        print(f"✅ {module_name}: Available")
    except ImportError:
        print(f"⚠️ {module_name}: Not available")

print("=" * 50)
PYTHONEOF

echo ""
echo -e "${GREEN}✅ BUILD COMPLETE!${NC}"
echo ""
echo "📝 Next steps:"
echo "  1. Test mining: python3 test_cosmic_harmony_mining.py"
echo "  2. Integration test: python3 test_cosmic_harmony_integration.py"
echo "  3. Start pool: python3 zion_universal_pool_v2.py"
echo "  4. Start miner: python3 ai/zion_universal_miner.py --algorithm cosmic_harmony"
echo ""
