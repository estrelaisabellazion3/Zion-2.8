#!/bin/bash
#
# ZION Blockchain - Deployment Test Script
# Validates production deployment
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((TESTS_PASSED++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((TESTS_FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "========================================="
echo "ZION DEPLOYMENT VALIDATION TESTS"
echo "========================================="
echo ""

# Test 1: Systemd service
echo "Testing systemd service..."
if systemctl is-active --quiet zion-node; then
    pass "ZION node service is running"
else
    fail "ZION node service is not running"
fi

if systemctl is-enabled --quiet zion-node; then
    pass "ZION node service is enabled"
else
    fail "ZION node service is not enabled"
fi

# Test 2: RPC Server
echo ""
echo "Testing RPC server..."
if curl -s http://localhost:8332 > /dev/null 2>&1; then
    pass "RPC server is responding on port 8332"
    
    # Test RPC method
    RESPONSE=$(curl -s -X POST http://localhost:8332 \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","method":"getblockcount","params":[],"id":1}')
    
    if echo "$RESPONSE" | grep -q '"result"'; then
        pass "RPC getblockcount method working"
    else
        fail "RPC getblockcount method failed"
    fi
else
    fail "RPC server is not responding"
fi

# Test 3: Nginx
echo ""
echo "Testing Nginx..."
if systemctl is-active --quiet nginx; then
    pass "Nginx is running"
else
    fail "Nginx is not running"
fi

if curl -sk https://localhost/health 2>&1 | grep -q "OK"; then
    pass "Nginx HTTPS health check passed"
else
    fail "Nginx HTTPS health check failed"
fi

# Test HTTP → HTTPS redirect
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)
if [ "$HTTP_CODE" = "301" ]; then
    pass "HTTP → HTTPS redirect working"
else
    fail "HTTP → HTTPS redirect not working (got $HTTP_CODE)"
fi

# Test 4: SSL Certificate
echo ""
echo "Testing SSL certificate..."
if [ -f "/etc/nginx/ssl/zion.crt" ]; then
    pass "SSL certificate exists"
    
    # Check expiry
    EXPIRY=$(openssl x509 -in /etc/nginx/ssl/zion.crt -noout -enddate | cut -d= -f2)
    pass "SSL expires: $EXPIRY"
else
    fail "SSL certificate not found"
fi

# Test 5: Firewall
echo ""
echo "Testing firewall..."
if command -v ufw &> /dev/null; then
    if ufw status | grep -q "Status: active"; then
        pass "UFW firewall is active"
        
        if ufw status | grep -q "443/tcp.*ALLOW"; then
            pass "HTTPS port is allowed"
        else
            warn "HTTPS port may not be allowed in firewall"
        fi
    else
        warn "UFW firewall is not active"
    fi
else
    warn "UFW not installed"
fi

# Test 6: Fail2ban
echo ""
echo "Testing fail2ban..."
if systemctl is-active --quiet fail2ban; then
    pass "fail2ban is running"
else
    warn "fail2ban is not running"
fi

# Test 7: Backup configuration
echo ""
echo "Testing backup configuration..."
if [ -x "/home/zion/ZION/2.8.3/deployment/backup.sh" ]; then
    pass "Backup script is executable"
else
    fail "Backup script is not executable"
fi

if sudo -u zion crontab -l 2>/dev/null | grep -q "backup.sh"; then
    pass "Backup cron job is configured"
else
    fail "Backup cron job is not configured"
fi

if [ -d "/home/zion/backups" ]; then
    pass "Backup directory exists"
else
    warn "Backup directory not found"
fi

# Test 8: Database
echo ""
echo "Testing database..."
if [ -f "/home/zion/.zion/zion_regtest.db" ]; then
    pass "Database file exists"
    
    # Check size
    DB_SIZE=$(du -h /home/zion/.zion/zion_regtest.db | cut -f1)
    pass "Database size: $DB_SIZE"
else
    fail "Database file not found"
fi

# Test 9: Logs
echo ""
echo "Testing logs..."
if journalctl -u zion-node --since "1 minute ago" > /dev/null 2>&1; then
    pass "Systemd journal accessible"
else
    fail "Systemd journal not accessible"
fi

if [ -f "/var/log/nginx/zion_access.log" ]; then
    pass "Nginx access log exists"
else
    warn "Nginx access log not found"
fi

# Test 10: Performance
echo ""
echo "Testing performance..."

START_TIME=$(date +%s%N)
curl -s -X POST http://localhost:8332 \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"getblockcount","params":[],"id":1}' > /dev/null
END_TIME=$(date +%s%N)

RESPONSE_TIME=$(( (END_TIME - START_TIME) / 1000000 ))

if [ $RESPONSE_TIME -lt 100 ]; then
    pass "RPC response time: ${RESPONSE_TIME}ms (excellent)"
elif [ $RESPONSE_TIME -lt 200 ]; then
    pass "RPC response time: ${RESPONSE_TIME}ms (good)"
else
    warn "RPC response time: ${RESPONSE_TIME}ms (acceptable)"
fi

# Summary
echo ""
echo "========================================="
echo "TEST SUMMARY"
echo "========================================="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    echo ""
    echo "Deployment is production-ready! 🚀"
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED!${NC}"
    echo ""
    echo "Please review failed tests above."
    exit 1
fi
