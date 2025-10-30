#!/bin/bash
#
# ZION Blockchain - Complete Production Deployment Script
# Automates full deployment process
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] INFO:${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    error "Please run as root (use sudo)"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZION_DIR="/home/zion/ZION"

log "========================================="
log "ZION BLOCKCHAIN - PRODUCTION DEPLOYMENT"
log "========================================="
echo ""

# 1. Pre-deployment checks
log "Step 1/9: Pre-deployment validation..."

if [ ! -d "$ZION_DIR" ]; then
    error "ZION directory not found: $ZION_DIR"
    exit 1
fi

if [ ! -f "$ZION_DIR/venv_testing/bin/python" ]; then
    error "Python virtual environment not found"
    exit 1
fi

info "✓ ZION directory found"
info "✓ Virtual environment found"

# 2. Install system dependencies
log "Step 2/9: Installing system dependencies..."

apt-get update
apt-get install -y \
    nginx \
    sqlite3 \
    ufw \
    fail2ban \
    certbot \
    python3-certbot-nginx

info "✓ System dependencies installed"

# 3. Generate SSL certificate
log "Step 3/9: Generating SSL certificate..."

if [ ! -f "/etc/nginx/ssl/zion.crt" ]; then
    bash "$SCRIPT_DIR/generate-ssl-cert.sh"
else
    warn "SSL certificate already exists, skipping generation"
fi

info "✓ SSL certificate ready"

# 4. Configure Nginx
log "Step 4/9: Configuring Nginx..."

# Backup existing config
if [ -f "/etc/nginx/sites-enabled/default" ]; then
    mv /etc/nginx/sites-enabled/default /etc/nginx/sites-enabled/default.backup
fi

# Copy ZION nginx config
cp "$SCRIPT_DIR/nginx-zion.conf" /etc/nginx/sites-available/zion
ln -sf /etc/nginx/sites-available/zion /etc/nginx/sites-enabled/zion

# Test nginx config
if nginx -t; then
    info "✓ Nginx configuration valid"
    systemctl reload nginx
    systemctl enable nginx
else
    error "Nginx configuration invalid"
    exit 1
fi

info "✓ Nginx configured"

# 5. Install systemd service
log "Step 5/9: Installing systemd service..."

cp "$SCRIPT_DIR/zion-node.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable zion-node

info "✓ Systemd service installed"

# 6. Setup backup automation
log "Step 6/9: Configuring automated backups..."

# Make backup script executable
chmod +x "$SCRIPT_DIR/backup.sh"

# Add to crontab for zion user
CRON_ENTRY="0 3 * * * $SCRIPT_DIR/backup.sh >> /var/log/zion_backup.log 2>&1"

# Check if cron entry already exists
if ! sudo -u zion crontab -l 2>/dev/null | grep -q "backup.sh"; then
    (sudo -u zion crontab -l 2>/dev/null; echo "$CRON_ENTRY") | sudo -u zion crontab -
    info "✓ Backup cron job added (daily at 3 AM)"
else
    warn "Backup cron job already exists"
fi

info "✓ Automated backups configured"

# 7. Security hardening
log "Step 7/9: Applying security hardening..."

bash "$SCRIPT_DIR/security-hardening.sh"

info "✓ Security hardening complete"

# 8. Start ZION node
log "Step 8/9: Starting ZION node..."

systemctl start zion-node

# Wait for node to start
sleep 5

if systemctl is-active --quiet zion-node; then
    info "✓ ZION node started successfully"
else
    error "ZION node failed to start"
    journalctl -u zion-node -n 50
    exit 1
fi

# 9. Health check
log "Step 9/9: Running health checks..."

# Check if RPC is responding
sleep 2
if curl -s http://localhost:8332 > /dev/null; then
    info "✓ RPC server responding"
else
    warn "RPC server not responding yet (may need more time)"
fi

# Check if Nginx is proxying
if curl -sk https://localhost/health | grep -q "OK"; then
    info "✓ Nginx reverse proxy working"
else
    warn "Nginx health check failed"
fi

# Summary
echo ""
log "========================================="
log "DEPLOYMENT COMPLETE!"
log "========================================="
echo ""
log "Services Status:"
systemctl status zion-node --no-pager | head -5
systemctl status nginx --no-pager | head -5
echo ""
log "Access Points:"
info "HTTP:  http://localhost (redirects to HTTPS)"
info "HTTPS: https://localhost"
info "RPC:   http://localhost:8332 (internal)"
echo ""
log "Logs:"
info "Node:   journalctl -u zion-node -f"
info "Nginx:  tail -f /var/log/nginx/zion_*.log"
info "Backup: tail -f /var/log/zion_backup.log"
echo ""
log "Next Steps:"
warn "1. Test RPC: curl -sk https://localhost -d '{\"jsonrpc\":\"2.0\",\"method\":\"getblockcount\",\"params\":[],\"id\":1}'"
warn "2. Review logs: journalctl -u zion-node"
warn "3. Check firewall: ufw status"
warn "4. Monitor backups: ls -lh /home/zion/backups/zion/"
echo ""
log "========================================="
log "JAI RAM SITA HANUMAN - DEPLOYMENT SUCCESS!"
log "========================================="

exit 0
