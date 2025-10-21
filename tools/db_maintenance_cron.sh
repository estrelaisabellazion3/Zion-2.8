#!/bin/bash
# ZION Database Maintenance Cron Job
# Přidej do crontab: crontab -e
# Řádek: 0 3 1 */6 * /root/zion/tools/db_maintenance_cron.sh

ZION_DIR="/root/zion"
LOG_DIR="$ZION_DIR/logs"
LOG_FILE="$LOG_DIR/db_maintenance_$(date +\%Y\%m\%d_\%H\%M\%S).log"

mkdir -p "$LOG_DIR"

echo "========================================" | tee -a "$LOG_FILE"
echo "ZION Database Maintenance" | tee -a "$LOG_FILE"
echo "Date: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

cd "$ZION_DIR"

# Run maintenance
python3 tools/database_maintenance.py --db-dir "$ZION_DIR" --auto --force 2>&1 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "Maintenance completed at: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# Keep only last 12 maintenance logs (1 year)
cd "$LOG_DIR"
ls -t db_maintenance_*.log | tail -n +13 | xargs -r rm

exit 0
