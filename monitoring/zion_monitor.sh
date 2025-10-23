#!/bin/bash
# ZION 2.8.1 Monitoring Script

echo "=== ZION 2.8.1 SYSTEM MONITORING ==="
echo "Timestamp: $(date)"
echo

# Process monitoring
echo "=== PROCESSES ==="
ps aux | grep -E "(zion|pool|warp|mining)" | grep -v grep || echo "No ZION processes found"
echo

# Pool statistics
echo "=== POOL STATISTICS ==="
if [ -f "zion_pool.db" ]; then
    echo "Total shares: $(sqlite3 zion_pool.db "SELECT COUNT(*) FROM shares;")"
    echo "Valid shares: $(sqlite3 zion_pool.db "SELECT COUNT(*) FROM shares WHERE is_valid=1;")"
    echo "Invalid shares: $(sqlite3 zion_pool.db "SELECT COUNT(*) FROM shares WHERE is_valid=0;")"
    echo "Active miners: $(sqlite3 zion_pool.db "SELECT COUNT(DISTINCT address) FROM miners WHERE last_share_time > strftime('%s', 'now', '-300');")"
else
    echo "Pool database not found"
fi
echo

# Consciousness game statistics
echo "=== CONSCIOUSNESS GAME ==="
if [ -f "consciousness_game.db" ]; then
    echo "Total miners: $(sqlite3 consciousness_game.db "SELECT COUNT(*) FROM miner_consciousness;")"
    echo "Total XP: $(sqlite3 consciousness_game.db "SELECT SUM(xp) FROM miner_consciousness;")"
    echo "Average level: $(sqlite3 consciousness_game.db "SELECT AVG(level) FROM miner_consciousness;")"
else
    echo "Consciousness database not found"
fi
echo

# System resources
echo "=== SYSTEM RESOURCES ==="
echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}')"
echo "Memory Usage: $(free | grep Mem | awk '{printf "%.2f%%", $3/$2 * 100.0}')"
echo "Disk Usage: $(df / | tail -1 | awk '{print $5}')"
echo

# Network connections
echo "=== NETWORK ==="
echo "Active connections: $(netstat -tuln 2>/dev/null | grep LISTEN | wc -l)"
echo "Pool connections: $(netstat -tuln 2>/dev/null | grep :3333 | wc -l)"
echo

echo "=== END MONITORING ==="