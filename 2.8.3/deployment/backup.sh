#!/bin/bash
#
# ZION Blockchain - Automated Backup Script
# Daily backup of blockchain database and wallet
#

set -e

# Configuration
BACKUP_DIR="/home/zion/backups/zion"
DATA_DIR="/home/zion/.zion"
DB_FILE="zion_regtest.db"
WALLET_FILE="wallet.dat"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

log "Starting ZION blockchain backup..."

# Check if database exists
if [ ! -f "$DATA_DIR/$DB_FILE" ]; then
    error "Database file not found: $DATA_DIR/$DB_FILE"
    exit 1
fi

# Backup database
log "Backing up database..."
if command -v sqlite3 &> /dev/null; then
    # Use SQLite backup command (hot backup)
    sqlite3 "$DATA_DIR/$DB_FILE" ".backup '$BACKUP_DIR/${DB_FILE}_${DATE}.db'"
    
    if [ $? -eq 0 ]; then
        log "Database backup successful"
    else
        error "Database backup failed"
        exit 1
    fi
else
    # Fallback to simple copy
    warn "sqlite3 not found, using cp (not recommended for active database)"
    cp "$DATA_DIR/$DB_FILE" "$BACKUP_DIR/${DB_FILE}_${DATE}.db"
fi

# Compress backup
log "Compressing backup..."
gzip "$BACKUP_DIR/${DB_FILE}_${DATE}.db"

if [ $? -eq 0 ]; then
    log "Compression successful: ${DB_FILE}_${DATE}.db.gz"
else
    error "Compression failed"
    exit 1
fi

# Backup wallet (if exists)
if [ -f "$DATA_DIR/$WALLET_FILE" ]; then
    log "Backing up wallet..."
    cp "$DATA_DIR/$WALLET_FILE" "$BACKUP_DIR/${WALLET_FILE}_${DATE}"
    
    # Encrypt wallet backup (recommended)
    if command -v gpg &> /dev/null; then
        log "Encrypting wallet backup..."
        # Note: You should set up GPG key first
        # gpg -c "$BACKUP_DIR/${WALLET_FILE}_${DATE}"
        # rm "$BACKUP_DIR/${WALLET_FILE}_${DATE}"
        log "Wallet backup complete (unencrypted - consider setting up GPG)"
    fi
else
    warn "Wallet file not found, skipping wallet backup"
fi

# Calculate backup size
BACKUP_SIZE=$(du -h "$BACKUP_DIR/${DB_FILE}_${DATE}.db.gz" | cut -f1)
log "Backup size: $BACKUP_SIZE"

# Clean up old backups
log "Cleaning up old backups (older than $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "*.gz" -type f -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "wallet.dat_*" -type f -mtime +$RETENTION_DAYS -delete

REMAINING=$(ls -1 "$BACKUP_DIR" | wc -l)
log "Backup cleanup complete. Remaining backups: $REMAINING"

# Backup summary
echo ""
log "========================================="
log "ZION Backup Summary"
log "========================================="
log "Backup file: ${DB_FILE}_${DATE}.db.gz"
log "Backup size: $BACKUP_SIZE"
log "Location: $BACKUP_DIR"
log "Retention: $RETENTION_DAYS days"
log "Status: SUCCESS"
log "========================================="

exit 0
