# 💾 ZION Database Maintenance

Jednoduché nástroje pro údržbu ZION databází.

## 📊 Růst databází

### Projekce bez údržby:
```
Denní růst:    ~11 MB/den
Měsíční růst:  ~330 MB/měsíc
Roční růst:    ~4 GB/rok
```

### S 6-měsíční údržbou:
```
6 měsíců:      ~2 GB
Po VACUUM:     ~1.2 GB (-40%)
Roční:         ~2.5 GB (místo 4 GB)
```

## 🛠️ Nástroje

### 1. `database_maintenance.py`

**Analýza databází:**
```bash
python3 tools/database_maintenance.py --analyze
```

Výstup:
```
==========================================================================
🔍 ZION DATABASE ANALYSIS
==========================================================================

📄 zion_pool.db:
   Size: 0.65 MB
   Pages: 167 × 4096 bytes
   Wasted: 0.05 MB (12 free pages)
   Tables:
     - miners: 1 records
     - shares: 2,785 records
     - blocks: 5 records

📄 zion_unified_blockchain.db:
   Size: 0.03 MB
   Pages: 7 × 4096 bytes
   Wasted: 0.00 MB (0 free pages)
   Tables:
     - real_blocks: 16 records
     - real_transactions: 0 records

==========================================================================
📊 TOTAL: 0.68 MB (wasted: 0.05 MB)
💡 Potential savings: 0.05 MB (7.4%)
==========================================================================
```

**Optimalizace databází:**
```bash
python3 tools/database_maintenance.py --optimize
```

Co se děje:
1. ✅ Vytvoří backup každé databáze
2. ♻️ Spustí `VACUUM` (komprese + defragmentace)
3. 📊 Spustí `ANALYZE` (optimalizace dotazů)
4. 💾 Smaže backup pokud úspěšné
5. 📈 Zobrazí ušetřené místo

**Automatická údržba (1× za 6 měsíců):**
```bash
python3 tools/database_maintenance.py --auto
```

Spustí se pouze pokud:
- Uplynulo 6+ měsíců od poslední údržby
- NEBO použiješ `--force`

### 2. `db_maintenance_cron.sh`

Automatický cron job pro pravidelnou údržbu.

**Instalace:**
```bash
# Nastav práva
chmod +x tools/db_maintenance_cron.sh

# Přidej do crontab
crontab -e

# Vlož řádek (spustí se 1. den každého 6. měsíce v 3:00 ráno):
0 3 1 */6 * /root/zion/tools/db_maintenance_cron.sh
```

**Logy:**
```bash
# Uloženo v:
/root/zion/logs/db_maintenance_YYYYMMDD_HHMMSS.log

# Poslední log:
tail -f /root/zion/logs/db_maintenance_*.log | tail -1
```

## 📅 Plán údržby

### Doporučený harmonogram:

| Měsíc | Akce | Důvod |
|-------|------|-------|
| 1-5 | Žádná údržba | DB < 2 GB |
| 6 | VACUUM + ANALYZE | Prvních 6 měsíců |
| 7-11 | Žádná údržba | DB očištěna |
| 12 | VACUUM + ANALYZE | Roční údržba |

### Kdy spustit manuálně:

❗ **Okamžitě** pokud:
- DB > 5 GB
- Dotazy pomalé (> 1s)
- Místo na disku < 20%

⚠️ **Brzy** pokud:
- DB > 2 GB
- 6+ měsíců bez údržby
- Wasted space > 10%

✅ **Nemusíš** pokud:
- DB < 1 GB
- Poslední VACUUM < 3 měsíce
- Wasted space < 5%

## 🔍 Monitorování

### Kontrola velikosti:
```bash
cd /root/zion
du -sh *.db
```

### Kontrola fragmen tace:
```bash
python3 tools/database_maintenance.py --analyze
```

### Kontrola poslední údržby:
```bash
ls -lh /root/zion/.last_maintenance
```

## ⚙️ Pokročilé použití

### Manuální VACUUM:
```bash
sqlite3 zion_pool.db "VACUUM;"
```

### Jen analýza (bez úprav):
```bash
sqlite3 zion_pool.db "PRAGMA integrity_check;"
```

### Kontrola tabulek:
```bash
sqlite3 zion_pool.db ".tables"
```

### Export před údržbou:
```bash
sqlite3 zion_pool.db ".dump" > pool_backup.sql
```

## 📊 Výkon

### Typické časy VACUUM:

| Velikost DB | Čas VACUUM | Úspora |
|-------------|------------|--------|
| 100 MB | ~5 sekund | ~10 MB |
| 500 MB | ~20 sekund | ~50 MB |
| 1 GB | ~45 sekund | ~100 MB |
| 2 GB | ~90 sekund | ~200 MB |
| 5 GB | ~4 minuty | ~500 MB |

### Dopad na systém:

✅ **Bezpečné:**
- Read-only operace fungují během VACUUM
- Databáze je stále dostupná
- Backupy vytvořeny automaticky

⚠️ **Během VACUUM:**
- Write operace blokované
- Vyšší CPU usage (20-40%)
- Potřeba 2× velikosti DB na disku (dočasně)

## 🐛 Troubleshooting

### "Database is locked"
```bash
# Zastav unified systém
pkill -f zion_unified.py

# Spusť údržbu
python3 tools/database_maintenance.py --optimize

# Restartuj systém
python3 zion_unified.py &
```

### "Disk space full"
```bash
# VACUUM potřebuje 2× velikost DB
# Pokud DB = 2 GB, potřebuješ 4 GB volného místa

# Kontrola:
df -h

# Smaž staré logy:
find /root/zion/logs -mtime +30 -delete
```

### "Backup failed"
```bash
# Vytvoř backup manuálně:
cp zion_pool.db zion_pool.db.backup_$(date +%Y%m%d)

# Pak spusť údržbu
```

## 📝 Best Practices

### ✅ DĚLEJ:
- 🔄 Spusť údržbu každých 6 měsíců
- 💾 Kontroluj volné místo před VACUUM
- 📊 Analyzuj před optimalizací
- 🔍 Sleduj logy po údržbě

### ❌ NEDĚLEJ:
- ⛔ VACUUM na produkci za běhu (bez backupu)
- ⛔ Spouštět vícekrát týdně (zbytečné)
- ⛔ Mazat .last_maintenance soubor
- ⛔ Spouštět s < 2× volným místem

## 📚 Další informace

- SQLite VACUUM: https://www.sqlite.org/lang_vacuum.html
- PRAGMA commands: https://www.sqlite.org/pragma.html
- Database optimization: https://www.sqlite.org/optoverview.html

---

**Vytvořeno**: 10. října 2025  
**Verze**: 1.0  
**Status**: ✅ Production Ready
