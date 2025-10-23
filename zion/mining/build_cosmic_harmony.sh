#!/bin/bash
# Build ZION Cosmic Harmony shared library for Python wrapper
# Compiles C++ implementation as .so/.dylib for use in Universal AI Miner

set -e

echo "🔨 Building ZION Cosmic Harmony Shared Library"
echo "=============================================="

# Detect OS
OS=$(uname -s)
ARCH=$(uname -m)

echo "OS: $OS"
echo "Architecture: $ARCH"
echo ""

# Compiler settings
CXX=${CXX:-g++}
CXXFLAGS="-std=c++17 -O3 -fPIC -DNDEBUG"
INCLUDES="-I./include -I../../../external/blake3/c"
LIBS="-lcrypto -lssl"

# Platform-specific settings
if [[ "$OS" == "Darwin" ]]; then
    # macOS
    OUTPUT="libcosmicharmony.dylib"
    LDFLAGS="-dynamiclib -undefined dynamic_lookup"
    echo "Platform: macOS"
elif [[ "$OS" == "Linux" ]]; then
    # Linux
    OUTPUT="libcosmicharmony.so"
    LDFLAGS="-shared"
    echo "Platform: Linux"
else
    echo "⚠️  Unsupported OS: $OS"
    exit 1
fi

# Create build directory
mkdir -p build
cd build

echo ""
echo "📦 Compiling Cosmic Harmony C++ sources..."
echo "Compiler: $CXX"
echo "Flags: $CXXFLAGS"
echo ""

# Compile BLAKE3 C implementation
echo "🔹 Compiling BLAKE3..."
$CXX $CXXFLAGS -c ../../../external/blake3/c/blake3.c -o blake3.o 2>&1 || {
    echo "⚠️ BLAKE3 not found, will use system crypto"
}

# Compile Cosmic Harmony
echo "🔹 Compiling Cosmic Harmony..."
$CXX $CXXFLAGS $INCLUDES -c ../zion-cosmic-harmony.cpp -o cosmic_harmony.o

# Create wrapper C interface (for easier Python ctypes binding)
cat > cosmic_harmony_c_wrapper.cpp << 'EOF'
#include "zion-cosmic-harmony.h"
#include <cstring>

extern "C" {

// C interface for Python ctypes
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
EOF

echo "🔹 Compiling C wrapper..."
$CXX $CXXFLAGS $INCLUDES -c cosmic_harmony_c_wrapper.cpp -o wrapper.o

# Link shared library
echo "🔗 Linking shared library..."
if [ -f blake3.o ]; then
    $CXX $LDFLAGS $CXXFLAGS -o $OUTPUT cosmic_harmony.o wrapper.o blake3.o $LIBS
else
    $CXX $LDFLAGS $CXXFLAGS -o $OUTPUT cosmic_harmony.o wrapper.o $LIBS
fi

# Copy to parent directory for easy access
cp $OUTPUT ../

echo ""
echo "✅ Build complete!"
echo "📚 Library: build/$OUTPUT"
echo "📚 Copied to: $OUTPUT"
echo ""

# Test if library is valid
if [[ "$OS" == "Darwin" ]]; then
    echo "🔍 Library info:"
    otool -L $OUTPUT | grep -v ":" || true
elif [[ "$OS" == "Linux" ]]; then
    echo "🔍 Library info:"
    ldd $OUTPUT | head -5 || true
fi

echo ""
echo "🎯 Next steps:"
echo "   1. Test: python3 cosmic_harmony_wrapper.py"
echo "   2. Integrate: Import in zion_universal_miner.py"
echo ""
