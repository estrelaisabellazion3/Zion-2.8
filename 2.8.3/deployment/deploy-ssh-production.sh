#!/bin/bash
################################################################################
# ZION 2.8.3 "Terra Nova" - Production SSH Deployment
# Target: zionterranova.com (91.98.122.165)
# Ubuntu 24.04 LTS | Production-Ready | Phase 12 Complete
################################################################################

set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

DEPLOY_USER="root"
DEPLOY_HOST="91.98.122.165"
DEPLOY_DOMAIN="zionterranova.com"
DEPLOY_DIR="/opt/zion-2.8.3"
ZION_VERSION="2.8.3"

# Local paths
LOCAL_ZION_DIR="/home/zion/ZION"
LOCAL_DEPLOY_DIR="/home/zion/ZION/2.8.3/deployment"

# SSH configuration (using password with sshpass)
SSH_CMD="sshpass -e ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no"
SCP_CMD="sshpass -e scp -o ConnectTimeout=10 -o StrictHostKeyChecking=no -r"

# ============================================================================
# COLORS
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# ============================================================================
# LOGGING FUNCTIONS
# ============================================================================

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

step() {
    echo -e "\n${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}\n"
}

# ============================================================================
# DEPLOYMENT BANNER
# ============================================================================

echo -e "${MAGENTA}"
cat << "EOF"
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║         ███████╗██╗ ██████╗ ███╗   ██╗                        ║
║         ╚══███╔╝██║██╔═══██╗████╗  ██║                        ║
║           ███╔╝ ██║██║   ██║██╔██╗ ██║                        ║
║          ███╔╝  ██║██║   ██║██║╚██╗██║                        ║
║         ███████╗██║╚██████╔╝██║ ╚████║                        ║
║         ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝                        ║
║                                                                ║
║                  BLOCKCHAIN 2.8.3 "Terra Nova"                ║
║                  Production SSH Deployment                     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

log "Target Server: ${DEPLOY_HOST} (${DEPLOY_DOMAIN})"
log "ZION Version: ${ZION_VERSION}"
log "Deployment Directory: ${DEPLOY_DIR}"
echo ""

# ============================================================================
# STEP 1: PRE-DEPLOYMENT CHECKS
# ============================================================================

step "Step 1/12: Pre-Deployment Validation"

# Check local files exist
info "Checking local files..."
if [ ! -d "$LOCAL_ZION_DIR" ]; then
    error "Local ZION directory not found: $LOCAL_ZION_DIR"
    exit 1
fi

if [ ! -d "$LOCAL_DEPLOY_DIR" ]; then
    error "Deployment scripts not found: $LOCAL_DEPLOY_DIR"
    exit 1
fi

log "✓ Local files validated"

# Test SSH connection
info "Testing SSH connection to ${DEPLOY_HOST}..."
if ! $SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} "echo 'SSH Connected'" > /dev/null 2>&1; then
    error "Cannot connect to ${DEPLOY_HOST}"
    error "Please check:"
    error "  1. SSH key is configured"
    error "  2. Server is reachable"
    error "  3. User has proper permissions"
    exit 1
fi

log "✓ SSH connection established"

# Check server OS
info "Checking server operating system..."
SERVER_OS=$($SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} "lsb_release -d" 2>/dev/null || echo "Unknown")
log "✓ Server OS: $SERVER_OS"

# ============================================================================
# STEP 2: STOP OLD SERVICES
# ============================================================================

step "Step 2/12: Stopping Old Services"

$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<'REMOTE_SCRIPT'
    # Stop systemd service if exists
    if systemctl list-units --all | grep -q "zion-node"; then
        echo "Stopping zion-node service..."
        systemctl stop zion-node || true
        systemctl disable zion-node || true
    fi
    
    # Stop any running ZION processes
    echo "Stopping ZION processes..."
    pkill -f "python.*zion" || true
    pkill -f "new_zion_blockchain" || true
    
    # Stop old Docker containers (if any from 2.8.2)
    if command -v docker &> /dev/null; then
        echo "Stopping old Docker containers..."
        docker stop zion-2.8.2-warp 2>/dev/null || true
        docker stop zion-2.8.2-pool 2>/dev/null || true
        docker stop zion-2.8.2-rpc 2>/dev/null || true
        docker rm -f zion-2.8.2-warp 2>/dev/null || true
        docker rm -f zion-2.8.2-pool 2>/dev/null || true
        docker rm -f zion-2.8.2-rpc 2>/dev/null || true
    fi
    
    echo "Old services stopped"
REMOTE_SCRIPT

log "✓ Old services stopped"

# ============================================================================
# STEP 3: PREPARE SERVER DIRECTORIES
# ============================================================================

step "Step 3/12: Preparing Server Directories"

$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<REMOTE_SCRIPT
    # Create deployment directory structure
    echo "Creating directory structure at ${DEPLOY_DIR}..."
    mkdir -p ${DEPLOY_DIR}/{src,deployment,data,logs,backups}
    mkdir -p ${DEPLOY_DIR}/data/{regtest,testnet,mainnet}
    mkdir -p ${DEPLOY_DIR}/logs/{node,nginx,system}
    
    # Set proper permissions
    chmod 755 ${DEPLOY_DIR}
    
    # Create deployment marker
    echo "ZION ${ZION_VERSION} Deployment - \$(date)" > ${DEPLOY_DIR}/deployment.log
    
    echo "Directories prepared"
REMOTE_SCRIPT

log "✓ Server directories prepared"

# ============================================================================
# STEP 4: TRANSFER SOURCE CODE
# ============================================================================

step "Step 4/12: Transferring Source Code"

info "Copying source code to server..."

# Transfer main source files
$SCP_CMD ${LOCAL_ZION_DIR}/src/* ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_DIR}/src/ 2>/dev/null || true

# Transfer main Python files
for file in new_zion_blockchain.py crypto_utils.py blockchain_rpc_client.py; do
    if [ -f "${LOCAL_ZION_DIR}/${file}" ]; then
        $SCP_CMD ${LOCAL_ZION_DIR}/${file} ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_DIR}/src/
    fi
done

# Transfer deployment scripts
$SCP_CMD ${LOCAL_DEPLOY_DIR}/* ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_DIR}/deployment/

# Transfer requirements.txt
if [ -f "${LOCAL_ZION_DIR}/requirements.txt" ]; then
    $SCP_CMD ${LOCAL_ZION_DIR}/requirements.txt ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_DIR}/
fi

log "✓ Source code transferred"

# ============================================================================
# STEP 5: INSTALL SYSTEM DEPENDENCIES
# ============================================================================

step "Step 5/12: Installing System Dependencies"

$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<'REMOTE_SCRIPT'
    echo "Updating package lists..."
    apt-get update -qq
    
    echo "Installing system dependencies..."
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        nginx \
        sqlite3 \
        ufw \
        fail2ban \
        curl \
        wget \
        git \
        htop \
        net-tools \
        lsof \
        certbot \
        python3-certbot-nginx
    
    echo "System dependencies installed"
REMOTE_SCRIPT

log "✓ System dependencies installed"

# ============================================================================
# STEP 6: SETUP PYTHON ENVIRONMENT
# ============================================================================

step "Step 6/12: Setting Up Python Environment"

$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<REMOTE_SCRIPT
    cd ${DEPLOY_DIR}
    
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "Upgrading pip..."
    pip install --upgrade pip
    
    echo "Installing Python dependencies..."
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt
    else
        # Install core dependencies
        pip install fastapi uvicorn requests websockets sqlite3
    fi
    
    echo "Python environment ready"
REMOTE_SCRIPT

log "✓ Python environment configured"

# ============================================================================
# STEP 7: GENERATE SSL CERTIFICATE
# ============================================================================

step "Step 7/12: Generating SSL Certificate"

$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<REMOTE_SCRIPT
    cd ${DEPLOY_DIR}/deployment
    
    # Make scripts executable
    chmod +x *.sh
    
    # Generate self-signed SSL certificate
    if [ ! -f /etc/nginx/ssl/zion.crt ]; then
        echo "Generating SSL certificate..."
        bash generate-ssl-cert.sh
    else
        echo "SSL certificate already exists"
    fi
REMOTE_SCRIPT

log "✓ SSL certificate ready"

# ============================================================================
# STEP 8: CONFIGURE NGINX
# ============================================================================

step "Step 8/12: Configuring Nginx Reverse Proxy"

$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<REMOTE_SCRIPT
    cd ${DEPLOY_DIR}/deployment
    
    echo "Backing up existing Nginx config..."
    if [ -f /etc/nginx/sites-enabled/default ]; then
        mv /etc/nginx/sites-enabled/default /etc/nginx/sites-enabled/default.backup 2>/dev/null || true
    fi
    
    echo "Installing ZION Nginx configuration..."
    cp nginx-zion.conf /etc/nginx/sites-available/zion
    ln -sf /etc/nginx/sites-available/zion /etc/nginx/sites-enabled/zion
    
    echo "Testing Nginx configuration..."
    if nginx -t; then
        echo "Nginx config valid - reloading..."
        systemctl enable nginx
        systemctl reload nginx
    else
        echo "ERROR: Nginx configuration invalid!"
        exit 1
    fi
REMOTE_SCRIPT

log "✓ Nginx configured"

# ============================================================================
# STEP 9: INSTALL SYSTEMD SERVICE
# ============================================================================

step "Step 9/12: Installing Systemd Service"

$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<REMOTE_SCRIPT
    cd ${DEPLOY_DIR}/deployment
    
    echo "Installing systemd service..."
    cp zion-node.service /etc/systemd/system/
    
    echo "Reloading systemd daemon..."
    systemctl daemon-reload
    
    echo "Enabling zion-node service..."
    systemctl enable zion-node
    
    echo "Systemd service installed"
REMOTE_SCRIPT

log "✓ Systemd service installed"

# ============================================================================
# STEP 10: CONFIGURE AUTOMATED BACKUPS
# ============================================================================

step "Step 10/12: Configuring Automated Backups"

$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<REMOTE_SCRIPT
    cd ${DEPLOY_DIR}/deployment
    
    echo "Setting up backup automation..."
    chmod +x backup.sh
    
    # Add cron job for daily backups at 3 AM
    CRON_ENTRY="0 3 * * * ${DEPLOY_DIR}/deployment/backup.sh >> /var/log/zion_backup.log 2>&1"
    
    # Check if cron entry already exists
    if ! crontab -l 2>/dev/null | grep -q "backup.sh"; then
        (crontab -l 2>/dev/null; echo "\$CRON_ENTRY") | crontab -
        echo "Backup cron job added (daily at 3 AM)"
    else
        echo "Backup cron job already exists"
    fi
    
    # Create initial backup
    mkdir -p ${DEPLOY_DIR}/backups
    
    echo "Backup automation configured"
REMOTE_SCRIPT

log "✓ Automated backups configured"

# ============================================================================
# STEP 11: APPLY SECURITY HARDENING
# ============================================================================

step "Step 11/12: Applying Security Hardening"

$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<REMOTE_SCRIPT
    cd ${DEPLOY_DIR}/deployment
    
    echo "Applying security hardening..."
    bash security-hardening.sh
    
    echo "Security hardening complete"
REMOTE_SCRIPT

log "✓ Security hardening applied"

# ============================================================================
# STEP 12: START ZION NODE
# ============================================================================

step "Step 12/12: Starting ZION Node"

$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<'REMOTE_SCRIPT'
    echo "Starting ZION node service..."
    systemctl start zion-node
    
    echo "Waiting for node to start..."
    sleep 5
    
    # Check service status
    if systemctl is-active --quiet zion-node; then
        echo "✓ ZION node started successfully"
    else
        echo "✗ ZION node failed to start"
        journalctl -u zion-node -n 20
        exit 1
    fi
REMOTE_SCRIPT

log "✓ ZION node started"

# ============================================================================
# HEALTH CHECKS
# ============================================================================

step "Health Checks & Validation"

sleep 3

info "Running health checks..."

HEALTH_OK=0
HEALTH_TOTAL=5

# Check 1: Systemd service
echo -n "  Systemd Service: "
if $SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} "systemctl is-active --quiet zion-node"; then
    echo -e "${GREEN}✓ Running${NC}"
    ((HEALTH_OK++))
else
    echo -e "${RED}✗ Not Running${NC}"
fi

# Check 2: RPC Server (local)
echo -n "  RPC Server (8332): "
if $SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} "curl -s http://localhost:8332 > /dev/null 2>&1"; then
    echo -e "${GREEN}✓ Responding${NC}"
    ((HEALTH_OK++))
else
    echo -e "${YELLOW}⚠ Not Responding${NC}"
fi

# Check 3: Nginx
echo -n "  Nginx Reverse Proxy: "
if $SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} "systemctl is-active --quiet nginx"; then
    echo -e "${GREEN}✓ Running${NC}"
    ((HEALTH_OK++))
else
    echo -e "${RED}✗ Not Running${NC}"
fi

# Check 4: SSL/HTTPS
echo -n "  HTTPS Endpoint: "
if curl -sk https://${DEPLOY_HOST}/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Accessible${NC}"
    ((HEALTH_OK++))
else
    echo -e "${YELLOW}⚠ Not Accessible${NC}"
fi

# Check 5: Firewall
echo -n "  Firewall (UFW): "
if $SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} "ufw status | grep -q 'Status: active'"; then
    echo -e "${GREEN}✓ Active${NC}"
    ((HEALTH_OK++))
else
    echo -e "${YELLOW}⚠ Inactive${NC}"
fi

echo ""
log "Health Score: ${HEALTH_OK}/${HEALTH_TOTAL} checks passed"

# ============================================================================
# DEPLOYMENT SUMMARY
# ============================================================================

echo ""
echo -e "${MAGENTA}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║                                                                ║${NC}"
echo -e "${MAGENTA}║         ✅ ZION 2.8.3 DEPLOYMENT COMPLETE! ✅                  ║${NC}"
echo -e "${MAGENTA}║                                                                ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

log "📊 Deployment Information:"
echo ""
info "  Server:        ${DEPLOY_HOST}"
info "  Domain:        ${DEPLOY_DOMAIN}"
info "  Version:       ZION ${ZION_VERSION} 'Terra Nova'"
info "  Deploy Dir:    ${DEPLOY_DIR}"
info "  Health:        ${HEALTH_OK}/${HEALTH_TOTAL} ✓"
echo ""

log "🌐 Access Points:"
echo ""
info "  Website:       https://${DEPLOY_DOMAIN}"
info "  Website (IP):  https://${DEPLOY_HOST}"
info "  RPC Internal:  http://localhost:8332 (server-side only)"
info "  HTTPS:         Port 443 (SSL/TLS enabled)"
info "  HTTP:          Port 80 (redirects to HTTPS)"
echo ""

log "📝 Management Commands:"
echo ""
info "  SSH Connect:   ssh ${DEPLOY_USER}@${DEPLOY_HOST}"
info "  View Logs:     ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'journalctl -u zion-node -f'"
info "  Service Stop:  ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'systemctl stop zion-node'"
info "  Service Start: ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'systemctl start zion-node'"
info "  Service Status:ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'systemctl status zion-node'"
info "  Nginx Logs:    ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'tail -f /var/log/nginx/zion_*.log'"
echo ""

log "🔍 Verification Steps:"
echo ""
warn "  1. Test HTTPS:     curl -sk https://${DEPLOY_HOST}/health"
warn "  2. Check RPC:      ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'curl http://localhost:8332'"
warn "  3. View Logs:      ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'journalctl -u zion-node -n 50'"
warn "  4. Check Firewall: ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'ufw status'"
warn "  5. Monitor:        ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'htop'"
echo ""

log "📦 Services Installed:"
echo ""
info "  ✓ ZION Blockchain Node (systemd)"
info "  ✓ Nginx Reverse Proxy (SSL/TLS)"
info "  ✓ Automated Daily Backups (3 AM)"
info "  ✓ UFW Firewall"
info "  ✓ Fail2Ban Security"
info "  ✓ Prometheus Monitoring (optional)"
echo ""

if [ $HEALTH_OK -eq $HEALTH_TOTAL ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  🎉 ALL SYSTEMS OPERATIONAL - DEPLOYMENT SUCCESSFUL! 🎉        ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    log "🙏 JAI RAM SITA HANUMAN - TERRA NOVA LIVE! ⭐"
    echo ""
    exit 0
else
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  ⚠️  DEPLOYMENT COMPLETE WITH WARNINGS  ⚠️                     ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    warn "Some health checks failed. Please review:"
    warn "  ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'journalctl -u zion-node -n 100'"
    echo ""
    exit 0
fi
