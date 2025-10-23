# zqalc - ZQAL CLI

Minimal CLI pro kontrolu ZQAL souborů.

## Použití

```bash
# zobrazení nápovědy
zqalc --help

# základní kontrola souboru
zqalc parse ../examples/cosmic_harmony.zqal

# tokenová statistika
zqalc tokens ../examples/cosmic_harmony.zqal
```

Poznámka: Plnohodnotný parser (nom/pest) bude doplněn. Tato verze provádí:
- kontrolu přítomnosti `@algorithm` a `@kernel`
- jednoduchou kontrolu vyváženosti `{}`

## Build (volitelně)

```bash
cd zqal-sdk/zqalc
cargo build --release
./target/release/zqalc --help
```

## Další kroky
- Implementovat EBNF parser (nom)
- Validovat typy a rozhraní funkcí
- Přidat AST → Rust/OpenCL codegen
