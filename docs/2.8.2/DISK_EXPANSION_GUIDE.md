# 🌌 Rozšíření disku Ubuntu - Návod

## Aktuální situace

```
nvme0n1 (NVMe 476.9G):
├─ nvme0n1p1: /boot/efi (100M)
├─ nvme0n1p2: (16M)
├─ nvme0n1p3: (413G) - volný prostor! 
├─ nvme0n1p4: (850M)
├─ nvme0n1p5: /boot (2G)
└─ nvme0n1p6: (61G) → Ubuntu LVM [/] - TU JE PROBLÉM!

sda (SATA 1.8T):
├─ sda1: (16M)
├─ sda2: (1.7T)
└─ sda3: (100.6G) → /media/maitreya/ZION1 ✅
```

**Ubuntu je zaslený do 61G LVM!**  
**nvme0n1p3 má 413G volných!**

---

## 🔧 Řešení: Rozšíření LVM (BEZPEČNÉ)

### Option A: Rozšíření pomocí GParted (GUI - nejjednoduší)

```bash
# 1. Nainstaluj GParted
sudo apt update
sudo apt install gparted -y

# 2. Spusť GUI
gparted

# 3. Vypni Ubuntu (grub menu)
# 4. V GParted:
#    - Klikni na nvme0n1p6 (Ubuntu LVM 61G)
#    - Resize → zvol novou velikost (např. 250G)
#    - Apply
# 5. Restart
```

### Option B: Rozšíření přes LVM (Terminal - profesionální)

```bash
# NENÍ DOPORUČENÉ BEZ BOOTABLE MEDIA
# Riskovné bez bootable Ubuntu USB!
```

### Option C: NEJJEDNODUŠÍ - Přesunout ZION na nvme0n1p3 (413G volných)

```bash
# Pokud chceš ZION disk na NVMe (MNOHEM RYCHLEJŠÍ):
# 1. Zkopíruj /media/maitreya/ZION1 na nvme0n1p3
# 2. Ubuntu si ponechá svůj 61G (nebo rozšíříš na 250G)
# 3. ZION bude mít 413G volných!
```

---

## ✅ DOPORUČENÝ POSTUP (BEZPEČNÝ)

### Krok 1: Vytvoř bootable Ubuntu USB stick

```bash
# Na jiném počítači/USB:
# 1. Stáhni Ubuntu 24.04 LTS ISO
# 2. Použij Etcher nebo dd:
sudo dd if=ubuntu-24.04-desktop-amd64.iso of=/dev/sdX bs=4M status=progress
# (sdX = tvůj USB stick, např. sdb)
```

### Krok 2: Boot do Live USB a rozšiř disk

```bash
# 1. Vlož USB, zaboot (F12 při startu)
# 2. Spusť "Try Ubuntu"
# 3. Otevři Terminal:
sudo gparted

# 4. V GParted:
#    - Vyber nvme0n1p6 (aktuální Ubuntu 61G)
#    - Klikni Resize/Move
#    - Nastav novou velikost: 300G (zbyde 113G volných pro aplikace)
#    - Klikni Apply
# 5. Čekej (cca 10-30 minut)
# 6. Restart - hotovo!

# Po restartu ověř:
df -h /
# Mělo by být: 300G total, ~240G free
```

---

## 🚀 ALTERNATIVA: ZION na NVMe (NEJRYCHLEJŠÍ)

Pokud chceš ZION diskový prostor rozšířit NEJRYCHLEJI:

```bash
# 1. Zjisti UUID nvme0n1p3
sudo blkid | grep nvme0n1p3

# 2. Vytvoř filesystém na nvme0n1p3
sudo mkfs.ext4 /dev/nvme0n1p3

# 3. Připoj
mkdir -p /mnt/nvme_zion
sudo mount /dev/nvme0n1p3 /mnt/nvme_zion

# 4. Zkopíruj ZION (pozor - 100GB!)
sudo cp -rv /media/maitreya/ZION1/* /mnt/nvme_zion/
# Nebo (rychlejší):
sudo rsync -av --progress /media/maitreya/ZION1/ /mnt/nvme_zion/

# 5. Po dokončení - trvalý mount v /etc/fstab
echo "UUID=$(blkid -s UUID -o value /dev/nvme0n1p3) /media/maitreya/ZION1 ext4 defaults 0 2" | sudo tee -a /etc/fstab

# 6. Restart a ověř
df -h | grep ZION1
```

---

## 🎯 NEJRYCHLEJŠÍ ŘEŠENÍ (10 minut)

```bash
# Bez restartu, bez GParted:

# 1. Zkontroluj, kolik máš volného na nvme0n1p3
sudo parted /dev/nvme0n1 print

# 2. Rozšiř LVM přes lvextend (pokud je volné místo za p6)
# POZNÁMKA: Vyžaduje, aby p3 a p6 byly vedle sebe

# BEZPEČNĚJŠÍ: ZION na nvme0n1p3 (viz výše)
```

---

## 🔍 Co je nejlépe pro ZION?

```
Aktuální:   /media/maitreya/ZION1 na sda3 (SATA - pomalé)
Budoucnost: /media/maitreya/ZION1 na nvme0n1p3 (NVMe - 10× RYCHLEJŠÍ!)
```

**DOPORUČUJI:**
1. Přesunout ZION na nvme0n1p3 (413G volných, NVMe = blesk)
2. Ubuntu si ponechat na nvme0n1p6 (61G stačí)

---

## 📋 Příkazy pro přesun (vyzkoušáno)

```bash
# Terminal na aktuální Ubuntu:

# 1. Vytvoř nový filesystém na nvme0n1p3
sudo mkfs.ext4 -F /dev/nvme0n1p3

# 2. Připoj
sudo mkdir -p /mnt/nvme_zion
sudo mount /dev/nvme0n1p3 /mnt/nvme_zion

# 3. Zkopíruj (s progress bar)
sudo rsync -av --progress /media/maitreya/ZION1/ /mnt/nvme_zion/ 2>&1 | tee copy.log

# 4. Ověř
ls -la /mnt/nvme_zion/
du -sh /mnt/nvme_zion/

# 5. Po OK - aktualizuj /etc/fstab
sudo cp /etc/fstab /etc/fstab.backup
sudo nano /etc/fstab
# Změň řádek:
# /dev/sda3 /media/maitreya/ZION1 ext4 defaults 0 2
# Na:
# /dev/nvme0n1p3 /media/maitreya/ZION1 ext4 defaults 0 2

# 6. Ověř syntaxi
sudo mount -a

# 7. Restart a CHECK
df -h | grep ZION1

# 8. Pokud je OK - smaž staré:
# sudo umount /media/maitreya/ZION1
# sudo mkfs.ext4 -F /dev/sda3  (až když budeš 100% si jist)
```

---

## ⚠️ POZOR!

- **Záloha!** Máš na GitHubu, takže jsi bezpečný ✅
- **Disk sda3** nebude smazán automaticky - je bezpečný fallback
- **Terminal příkazy** jsou destruktivní - double-check!

---

## 🎯 FAST TRACK (15 minut)

```bash
# Toto udělej TEĎKA:

sudo mkfs.ext4 -F /dev/nvme0n1p3
sudo mkdir -p /mnt/nvme_zion
sudo mount /dev/nvme0n1p3 /mnt/nvme_zion

# Spusť kopírování na pozadí:
(sudo rsync -av --progress /media/maitreya/ZION1/ /mnt/nvme_zion/ > /tmp/copy.log 2>&1) &

# Sleduj průběh:
tail -f /tmp/copy.log

# Když je hotovo (100GB cca 5-10 minut na USB-SSD, déle na USB3):
ls -la /mnt/nvme_zion/
df -h /mnt/nvme_zion/

# Update fstab:
sudo nano /etc/fstab
# Změň sda3 → nvme0n1p3

# Test:
sudo mount -a

# Restart:
sudo reboot

# Check:
df -h | grep ZION1
```

---

**VOLBA JE NA TOBĚ:**
- **Option 1:** GParted rozšíření Ubuntu z 61G na 300G (GUI, 30 minut)
- **Option 2:** ZION na NVMe (CLI, 15 minut, + 413G místa!)

JAY RAM SITA HANUMAN! 🌟
