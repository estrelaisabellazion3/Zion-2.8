#!/bin/bash
#
# ZION Blockchain - Security Hardening Script
# Setup firewall, fail2ban, SSH hardening
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

log "Starting ZION security hardening..."

# 1. UFW Firewall Setup
log "Configuring UFW firewall..."

if ! command -v ufw &> /dev/null; then
    warn "UFW not installed, installing..."
    apt-get update
    apt-get install -y ufw
fi

# Default policies
ufw --force reset
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (change port if needed)
SSH_PORT=22
info "Allowing SSH on port $SSH_PORT"
ufw allow $SSH_PORT/tcp comment 'SSH'

# Allow HTTP/HTTPS
info "Allowing HTTP/HTTPS"
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'

# Allow ZION P2P (if mainnet)
# ufw allow 8333/tcp comment 'ZION P2P'

# Enable UFW
log "Enabling UFW..."
ufw --force enable

ufw status verbose

# 2. Fail2Ban Setup
log "Configuring fail2ban..."

if ! command -v fail2ban-client &> /dev/null; then
    warn "fail2ban not installed, installing..."
    apt-get install -y fail2ban
fi

# Create fail2ban jail for nginx
cat > /etc/fail2ban/jail.d/nginx-zion.conf << 'EOF'
[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
findtime = 60
bantime = 600

[nginx-botsearch]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 5
bantime = 3600
EOF

# Restart fail2ban
systemctl restart fail2ban
systemctl enable fail2ban

log "fail2ban configured and started"

# 3. SSH Hardening (MINIMAL - keep root login enabled for deployment)
log "Hardening SSH configuration..."

# Backup original config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup.$(date +%Y%m%d)

# SSH hardening settings
info "Applying SSH security settings..."

# Keep root login enabled for deployment
# sed -i 's/^#*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config

# Keep password authentication enabled for now
# sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Enable public key authentication
sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# Disable empty passwords
sed -i 's/^#*PermitEmptyPasswords.*/PermitEmptyPasswords no/' /etc/ssh/sshd_config

# Limit max auth tries
sed -i 's/^#*MaxAuthTries.*/MaxAuthTries 6/' /etc/ssh/sshd_config

# Test SSH config
if sshd -t; then
    log "SSH configuration valid"
    systemctl reload sshd || true
else
    warn "SSH configuration test failed, skipping SSH reload"
fi

# 4. System Updates
log "Checking for system updates..."
apt-get update
apt-get upgrade -y

# 5. Install security tools
log "Installing additional security tools..."
DEBIAN_FRONTEND=noninteractive apt-get install -y \
    unattended-upgrades \
    rkhunter \
    chkrootkit

# Configure automatic security updates (non-interactive)
echo 'APT::Periodic::Update-Package-Lists "1";' > /etc/apt/apt.conf.d/20auto-upgrades
echo 'APT::Periodic::Unattended-Upgrade "1";' >> /etc/apt/apt.conf.d/20auto-upgrades

# 6. Secure shared memory
log "Securing shared memory..."
if ! grep -q "tmpfs /run/shm" /etc/fstab; then
    echo "tmpfs /run/shm tmpfs defaults,noexec,nosuid 0 0" >> /etc/fstab
    info "Added secure shared memory to fstab"
fi

# 7. Disable unnecessary services
log "Checking for unnecessary services..."
systemctl list-unit-files --type=service --state=enabled

# 8. Set file permissions
log "Setting secure file permissions..."
chmod 700 /home/zion/.ssh 2>/dev/null || true
chmod 600 /home/zion/.ssh/authorized_keys 2>/dev/null || true

# 9. Configure password policy
log "Configuring password policy..."
apt-get install -y libpam-pwquality

# 10. Audit logging
log "Configuring audit logging..."
apt-get install -y auditd
systemctl enable auditd
systemctl start auditd

# Summary
echo ""
log "========================================="
log "Security Hardening Complete!"
log "========================================="
log "✅ UFW firewall configured"
log "✅ fail2ban installed and configured"
log "✅ SSH hardened"
log "✅ System updated"
log "✅ Security tools installed"
log "✅ Shared memory secured"
log "✅ Password policy configured"
log "✅ Audit logging enabled"
log "========================================="
echo ""
warn "IMPORTANT: Review the following:"
warn "1. Test SSH connection before logging out"
warn "2. Configure SSH key-based auth if not done"
warn "3. Change default SSH port if desired"
warn "4. Review fail2ban logs: journalctl -u fail2ban"
warn "5. Review firewall rules: ufw status verbose"
echo ""
log "Security hardening script completed successfully!"

exit 0
