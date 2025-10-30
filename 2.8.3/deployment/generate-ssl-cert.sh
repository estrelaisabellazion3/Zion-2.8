#!/bin/bash
#
# ZION Blockchain - SSL Certificate Generator
# Creates self-signed certificate for testing/development
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

SSL_DIR="/etc/nginx/ssl"
CERT_FILE="$SSL_DIR/zion.crt"
KEY_FILE="$SSL_DIR/zion.key"
DAYS_VALID=365

log "Creating SSL certificate directory..."
mkdir -p "$SSL_DIR"

log "Generating self-signed SSL certificate..."

# Generate certificate
openssl req -x509 -nodes -days $DAYS_VALID -newkey rsa:4096 \
    -keyout "$KEY_FILE" \
    -out "$CERT_FILE" \
    -subj "/C=CZ/ST=Prague/L=Prague/O=ZION Blockchain/OU=IT/CN=zion.local" \
    -addext "subjectAltName=DNS:zion.local,DNS:localhost,IP:127.0.0.1"

# Set permissions
chmod 600 "$KEY_FILE"
chmod 644 "$CERT_FILE"

log "SSL certificate created successfully!"
echo ""
log "Certificate: $CERT_FILE"
log "Private Key: $KEY_FILE"
log "Valid for: $DAYS_VALID days"
echo ""
warn "This is a SELF-SIGNED certificate for TESTING only!"
warn "For production, use Let's Encrypt or a commercial CA."
echo ""
log "To view certificate details:"
echo "  openssl x509 -in $CERT_FILE -text -noout"
echo ""

exit 0
