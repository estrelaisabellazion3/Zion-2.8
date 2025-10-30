# 🚀 ZION Blockchain - Deployment Scripts

This directory contains production deployment scripts and configurations for ZION 2.8.3 blockchain.

## 📁 Files Overview

### Core Deployment
- **deploy.sh** - Master deployment script (runs all deployment steps)
- **test-deployment.sh** - Validates deployment after setup
- **generate-ssl-cert.sh** - Creates self-signed SSL certificate

### Service Configuration
- **zion-node.service** - Systemd service file for ZION node
- **nginx-zion.conf** - Nginx reverse proxy configuration
- **prometheus.yml** - Prometheus monitoring configuration

### Automation Scripts
- **backup.sh** - Automated daily backup script
- **security-hardening.sh** - Security configuration script

---

## 🚀 Quick Deployment

### Option 1: Automated Deployment (Recommended)

Run the master deployment script:

```bash
cd /home/zion/ZION/2.8.3/deployment
sudo chmod +x *.sh
sudo ./deploy.sh
```

This will:
1. Install system dependencies
2. Generate SSL certificate
3. Configure Nginx reverse proxy
4. Install systemd service
5. Setup automated backups
6. Apply security hardening
7. Start ZION node
8. Run health checks

### Option 2: Manual Step-by-Step Deployment

#### Step 1: Generate SSL Certificate
```bash
sudo ./generate-ssl-cert.sh
```

#### Step 2: Configure Nginx
```bash
sudo cp nginx-zion.conf /etc/nginx/sites-available/zion
sudo ln -s /etc/nginx/sites-available/zion /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Step 3: Install Systemd Service
```bash
sudo cp zion-node.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable zion-node
sudo systemctl start zion-node
```

#### Step 4: Setup Backups
```bash
chmod +x backup.sh
# Add to crontab (daily at 3 AM)
(crontab -l 2>/dev/null; echo "0 3 * * * /home/zion/ZION/2.8.3/deployment/backup.sh >> /var/log/zion_backup.log 2>&1") | crontab -
```

#### Step 5: Security Hardening
```bash
sudo ./security-hardening.sh
```

#### Step 6: Validate Deployment
```bash
sudo ./test-deployment.sh
```

---

## 🔐 SSL Certificate

### Self-Signed (Testing)
The deployment includes a self-signed certificate generator:
```bash
sudo ./generate-ssl-cert.sh
```

### Let's Encrypt (Production)
For production, use Let's Encrypt:
```bash
sudo certbot --nginx -d yourdomain.com
```

---

## 📊 Monitoring

### Prometheus Setup

1. Install Prometheus:
```bash
sudo apt install prometheus
```

2. Copy configuration:
```bash
sudo cp prometheus.yml /etc/prometheus/
```

3. Restart Prometheus:
```bash
sudo systemctl restart prometheus
```

4. Access: http://localhost:9090

### Grafana Setup

1. Install Grafana:
```bash
sudo apt install grafana
```

2. Start service:
```bash
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

3. Access: http://localhost:3000 (admin/admin)

4. Add Prometheus data source:
   - URL: http://localhost:9090
   - Import ZION dashboard

---

## 💾 Backups

### Manual Backup
```bash
./backup.sh
```

### Automated Backups
Configured via cron (daily at 3 AM):
```bash
crontab -l  # View scheduled backups
```

### Restore from Backup
```bash
# Stop ZION node
sudo systemctl stop zion-node

# Restore database
gunzip -c /home/zion/backups/zion/zion_regtest_YYYYMMDD_HHMMSS.db.gz > /home/zion/.zion/zion_regtest.db

# Start ZION node
sudo systemctl start zion-node
```

---

## 🛡️ Security

### Security Hardening Script
Applies all security best practices:
```bash
sudo ./security-hardening.sh
```

Includes:
- UFW firewall configuration
- fail2ban intrusion detection
- SSH hardening
- Automatic security updates
- Audit logging

### Firewall Rules
```bash
sudo ufw status verbose
```

### fail2ban Status
```bash
sudo fail2ban-client status
```

---

## 🔧 Service Management

### ZION Node Service

**Start:**
```bash
sudo systemctl start zion-node
```

**Stop:**
```bash
sudo systemctl stop zion-node
```

**Restart:**
```bash
sudo systemctl restart zion-node
```

**Status:**
```bash
sudo systemctl status zion-node
```

**Logs:**
```bash
sudo journalctl -u zion-node -f
```

### Nginx Service

**Reload config:**
```bash
sudo systemctl reload nginx
```

**Test config:**
```bash
sudo nginx -t
```

**Logs:**
```bash
sudo tail -f /var/log/nginx/zion_access.log
sudo tail -f /var/log/nginx/zion_error.log
```

---

## 📈 Testing & Validation

### Run Full Test Suite
```bash
sudo ./test-deployment.sh
```

### Manual Tests

**Test RPC:**
```bash
curl -X POST http://localhost:8332 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"getblockcount","params":[],"id":1}'
```

**Test HTTPS:**
```bash
curl -sk https://localhost/health
```

**Test Rate Limiting:**
```bash
for i in {1..150}; do
  curl -s https://localhost > /dev/null
done
# Should eventually get rate limited
```

---

## 🔍 Troubleshooting

### Service won't start
```bash
sudo journalctl -u zion-node -n 50
```

### Nginx errors
```bash
sudo nginx -t  # Test config
sudo tail -f /var/log/nginx/error.log
```

### Database locked
```bash
sudo systemctl stop zion-node
rm /home/zion/.zion/zion_regtest.db-journal
sudo systemctl start zion-node
```

### Firewall blocking
```bash
sudo ufw status
sudo ufw allow 443/tcp
```

---

## 📚 Additional Resources

- **Quick Start:** [../docs/QUICK_START.md](../docs/QUICK_START.md)
- **Deployment Guide:** [../docs/DEPLOYMENT_GUIDE.md](../docs/DEPLOYMENT_GUIDE.md)
- **Troubleshooting:** [../docs/TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md)
- **API Reference:** [../docs/API_REFERENCE.md](../docs/API_REFERENCE.md)

---

## ✅ Post-Deployment Checklist

- [ ] All tests passing (`./test-deployment.sh`)
- [ ] ZION node running (`systemctl status zion-node`)
- [ ] Nginx proxying HTTPS (`curl -sk https://localhost/health`)
- [ ] SSL certificate valid (`openssl x509 -in /etc/nginx/ssl/zion.crt -text`)
- [ ] Firewall configured (`ufw status`)
- [ ] Backups scheduled (`crontab -l`)
- [ ] fail2ban active (`fail2ban-client status`)
- [ ] Logs accessible (`journalctl -u zion-node`)
- [ ] Monitoring setup (Prometheus/Grafana)

---

**🙏 JAI RAM SITA HANUMAN - DEPLOY WITH CONFIDENCE! ⭐**

*Production deployment scripts for ZION 2.8.3 blockchain*
