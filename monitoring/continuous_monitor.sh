#!/bin/bash
# Continuous monitoring script for ZION 2.8.1

MONITOR_LOG="monitoring/continuous_monitor.log"
PID_FILE="monitoring/monitor.pid"

# Function to cleanup on exit
cleanup() {
    echo "Stopping continuous monitoring at $(date)" >> "$MONITOR_LOG"
    rm -f "$PID_FILE"
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Check if already running
if [ -f "$PID_FILE" ]; then
    echo "Monitoring already running (PID: $(cat $PID_FILE))"
    exit 1
fi

# Save PID
echo $$ > "$PID_FILE"

echo "Starting continuous monitoring at $(date)" >> "$MONITOR_LOG"

# Main monitoring loop
while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

    # Quick stats collection
    POOL_SHARES=$(sqlite3 zion_pool.db "SELECT COUNT(*) FROM shares;" 2>/dev/null || echo "0")
    VALID_SHARES=$(sqlite3 zion_pool.db "SELECT COUNT(*) FROM shares WHERE is_valid=1;" 2>/dev/null || echo "0")
    TOTAL_XP=$(sqlite3 consciousness_game.db "SELECT SUM(xp) FROM miner_consciousness;" 2>/dev/null || echo "0")
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}' 2>/dev/null || echo "0")

    # Log stats
    echo "$TIMESTAMP | Shares: $POOL_SHARES ($VALID_SHARES valid) | XP: $TOTAL_XP | CPU: ${CPU_USAGE}%" >> "$MONITOR_LOG"

    # Check for errors in logs
    if [ -f "pool.log" ]; then
        ERROR_COUNT=$(grep -c "ERROR\|Exception" pool.log 2>/dev/null || echo "0")
        if [ "$ERROR_COUNT" -gt 0 ]; then
            echo "$TIMESTAMP | ALERT: $ERROR_COUNT errors found in pool.log" >> "$MONITOR_LOG"
        fi
    fi

    sleep 30
done