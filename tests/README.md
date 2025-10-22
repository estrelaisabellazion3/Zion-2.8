# 🧪 ZION Test Suite

Kompletní testovací infrastruktura pro ZION 2.8.1 "Estrella"

---

## 📂 Struktura

```
tests/
├── unit/                    # Jednotkové testy (komponenty)
├── integration/             # Integrační testy (vzájemné vazby)
└── mining/                  # Mining testy (pool + stratum)
```

---

## 🔬 Unit Testy (`tests/unit/`)

Testují jednotlivé komponenty izolovaně:

- `test_mining_blocks.py` - Testování vytváření bloků
- `test_mining_quick.py` - Rychlý test mining algoritmu
- `test_native_yescrypt.py` - Native Yescrypt implementace
- `test_xmrig_login.py` - xmrig login proces
- `test_xmrig_protocol.py` - xmrig protokol
- `test_xmrig_session.py` - xmrig session management

### Spuštění
```bash
cd tests/unit
python3 test_mining_blocks.py
python3 test_native_yescrypt.py
```

---

## 🔗 Integrační Testy (`tests/integration/`)

Testují interakci mezi komponentami:

- `test_estrella.py` - Základní Estrella test
- `test_estrella_complete.py` - Kompletní Estrella test
- `test_estrella_solar_system.py` - Solar system integrační test
- `test_stratum_connection.py` - Stratum server test
- `test_stratum_manual.py` - Manuální Stratum test
- `test_stratum_miner.py` - Stratum miner test
- `test_warp_engine_local.py` - WARP engine local test

### Spuštění
```bash
cd tests/integration
python3 test_estrella_complete.py
python3 test_stratum_connection.py
```

---

## ⛏️ Mining Testy (`tests/mining/`)

Testují mining pool a algoritmy:

- `quick_pool_test.py` - Rychlý pool test
- `real_mining_no_sim.py` - Reálný mining bez simulace

### Spuštění
```bash
cd tests/mining
python3 quick_pool_test.py
python3 real_mining_no_sim.py
```

---

## 🚀 Spuštění všech testů

```bash
# Všechny unit testy
pytest tests/unit/

# Všechny integrační testy
pytest tests/integration/

# Všechny mining testy
pytest tests/mining/

# Všechny testy
pytest tests/
```

---

## 📊 Test Coverage

- **Unit**: 6 testů (komponenty)
- **Integration**: 7 testů (systém)
- **Mining**: 2 testy (pool)
- **Total**: 15 testů

---

## ⚙️ Konfigurace

Všechny testy očekávají:
- Python 3.8+
- Blockchain running na http://localhost:8332
- Pool running na localhost:3333
- RPC client configured

---

**Status**: ✅ Organized  
**Last Updated**: 23. září 2025
