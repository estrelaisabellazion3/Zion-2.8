#!/bin/bash

# 🌟 ZQAL SDK - Quick Development Setup
# Pro rychlý start vývoje ZQAL SDK

set -e

echo "🌟 ZQAL SDK Development Setup"
echo "================================"

# Kontrola Rust instalace
if ! command -v rustc &> /dev/null; then
    echo "❌ Rust není nainstalován. Instaluji..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
    echo "✅ Rust nainstalován"
else
    echo "✅ Rust je nainstalován: $(rustc --version)"
fi

# Kontrola Cargo
if ! command -v cargo &> /dev/null; then
    echo "❌ Cargo není dostupný"
    exit 1
else
    echo "✅ Cargo je dostupný: $(cargo --version)"
fi

# Přejít do zqal-sdk
cd "$(dirname "$0")/zqal-sdk"

echo ""
echo "🔧 Building ZQAL CLI (zqalc)..."
cd zqalc
cargo build --release

echo ""
echo "🧪 Testing current functionality..."
./target/release/zqalc --help

echo ""
echo "📝 Testing existing examples..."
cd ..
for f in examples/*.zqal; do
    echo "Testing $f..."
    ./zqalc/target/release/zqalc parse "$f"
done

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Prohlédnout si ZQAL_SDK_NEXT_STEPS_ROADMAP.md"
echo "2. Začít s ZQAL_SDK_PHASE_1_IMPLEMENTATION.md"
echo "3. Vytvořit feature branch: git checkout -b feature/extended-grammar"
echo ""
echo "🎯 Quick test:"
echo "  ./zqalc/target/release/zqalc parse examples/cosmic_harmony.zqal"
echo ""
echo "JAY RAM SITA HANUMAN! ✨"