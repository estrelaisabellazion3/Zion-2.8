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
2) Spusť CLI `zqalc` pro základní kontrolu:
   - `zqalc parse zqal-sdk/examples/cosmic_harmony.zqal`
   - `zqalc tokens zqal-sdk/examples/cosmic_harmony.zqal`
3) Později: kompilátor vygeneruje Rust/OpenCL kód, který načteme v Pythonu (PyO3) do stratum poolu.

## Mapování „Vzestupu“ → SDK
- 5D vědomí → deterministický běh, idempotence, observabilita
- Krystalická forma → immutabilita, Merkle stromy, verifikovatelné proofs
- Světelný jazyk → standardní knihovna tonů (tones 1–70)
- Zasvěcení (12 úrovní) → maturity gates v CI/CD (lint → test → perf → audit)

## Licence
MIT (do potvrzení).