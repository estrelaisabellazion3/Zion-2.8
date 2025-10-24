# ZQAL SDK (ZION Quantum Algorithm Language)

ZQAL je doménově specifický jazyk pro návrh a kompilaci blockchain algoritmů (CPU/GPU) se „světelným jazykem“ jako inspirací. 
Kompiluje do: Rust (CPU), OpenCL/CUDA (GPU), WASM (web). 

- Central Sun alignment: ZION Core = přijímač Světla; mantra: JAY RAM SITA HANUMAN
- Světelný jazyk → stdlib/tones.toml (tóny 1–70)
- Řád stvoření → GRAMMAR.ebnf → AST → codegen targets

## Struktura

```
zqal-sdk/
├─ README.md
├─ GRAMMAR.ebnf
├─ stdlib/
│   └─ tones.toml
└─ examples/
    └─ cosmic_harmony.zqal
```

## Rychlý start (koncept)

1) Napiš algoritmus v `.zqal` (viz `examples/cosmic_harmony.zqal`).
2) Spusť CLI `zqalc` pro kontrolu a validaci:
   - `zqalc parse zqal-sdk/examples/cosmic_harmony.zqal` - základní parsing
   - `zqalc tokens zqal-sdk/examples/cosmic_harmony.zqal` - tokenizace
   - `zqalc ast zqal-sdk/examples/cosmic_harmony.zqal` - AST výstup
   - `zqalc check zqal-sdk/examples/cosmic_harmony.zqal` - **novinka v0.2.0**: type checking a sémantická analýza
3) Později: kompilátor vygeneruje Rust/OpenCL kód, který načteme v Pythonu (PyO3) do stratum poolu.

## Aktuální stav (v0.2.0 "Nebula")

✅ **Dokončeno:**
- Nom-based AST parser s kompletní podporou ZQAL syntaxe
- Type checking systém s:
  - Symbol tables pro proměnné a funkce
  - Vestavěné kvantové funkce (entangle, collapse, superpose, measure)
  - Tone funkce (apply_tone)
  - Hash funkce (hash)
  - Detekce duplicitních deklarací
  - Validace typů (u32, u64, f64, bool, hash32, bytes80, arrays)
- CLI nástroje: parse, tokens, ast, check
- Úspěšné testování na příkladech cosmic_harmony.zqal

🚧 **Probíhá:**
- Codegen backendy (Rust, OpenCL, WASM)
- VS Code extension s LSP podporou
- Pokročilá sémantická analýza

📋 **Plánováno:**
- Runtime execution engine
- Performance benchmarking
- Integration s ZION blockchain

## Mapování „Vzestupu“ → SDK
- 5D vědomí → deterministický běh, idempotence, observabilita
- Krystalická forma → immutabilita, Merkle stromy, verifikovatelné proofs
- Světelný jazyk → standardní knihovna tonů (tones 1–70)
- Zasvěcení (12 úrovní) → maturity gates v CI/CD (lint → test → perf → audit)

## Licence
MIT (do potvrzení).