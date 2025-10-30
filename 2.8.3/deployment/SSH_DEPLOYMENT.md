# 🚀 ZION 2.8.3 SSH Production Deployment

Quick guide for deploying ZION 2.8.3 to production server **zionterranova.com** (91.98.122.165).

## 📋 Prerequisites

- **SSH Access**: Root access to 91.98.122.165 configured
- **Local Setup**: ZION 2.8.3 source code in `/home/zion/ZION`
- **Server**: Ubuntu 24.04 LTS on target server

## 🚀 Quick Deploy

```bash
cd /home/zion/ZION/2.8.3/deployment
./deploy-ssh-production.sh
```

That's it! The script will:

1. ✅ Validate pre-deployment requirements
2. ✅ Stop old services (including 2.8.2 if present)
3. ✅ Prepare server directories
4. ✅ Transfer source code via SCP
5. ✅ Install system dependencies
6. ✅ Setup Python virtual environment
7. ✅ Generate SSL certificates
8. ✅ Configure Nginx reverse proxy
9. ✅ Install systemd service
10. ✅ Configure automated backups (daily 3 AM)
11. ✅ Apply security hardening (UFW, fail2ban)
12. ✅ Start ZION node & validate

## 🌐 After Deployment

**Access Points:**
- Website: https://zionterranova.com
- Website (IP): https://91.98.122.165
- RPC: http://localhost:8332 (server-side only)

**Management:**
```bash
# SSH to server
ssh root@91.98.122.165

# View logs
ssh root@91.98.122.165 'journalctl -u zion-node -f'

# Service control
ssh root@91.98.122.165 'systemctl status|stop|start|restart zion-node'

# Check health
curl -sk https://91.98.122.165/health
```

## 📊 What Gets Deployed

**Directory Structure on Server:**
```
/opt/zion-2.8.3/
├── src/                  # Source code
├── deployment/           # Deployment scripts
├── data/                 # Blockchain data
│   ├── regtest/
│   ├── testnet/
│   └── mainnet/
├── logs/                 # Application logs
│   ├── node/
│   ├── nginx/
│   └── system/
├── backups/              # Automated backups
└── venv/                 # Python virtual environment
```

**Services Installed:**
- ✅ ZION Blockchain Node (systemd service)
- ✅ Nginx Reverse Proxy (SSL/TLS enabled)
- ✅ Automated Daily Backups (cron @ 3 AM)
- ✅ UFW Firewall (ports 80, 443, 22, 8332)
- ✅ Fail2Ban (SSH protection)
- ✅ Prometheus Monitoring (optional)

**Security Features:**
- ✅ SSL/TLS encryption (self-signed or Let's Encrypt)
- ✅ Firewall rules (UFW)
- ✅ SSH hardening
- ✅ Rate limiting (Nginx)
- ✅ Intrusion prevention (Fail2Ban)
- ✅ Automatic security updates

## 🔧 Troubleshooting

**If deployment fails:**

1. Check SSH connection:
   ```bash
   ssh root@91.98.122.165 echo "Connected"
   ```

2. Check server logs:
   ```bash
   ssh root@91.98.122.165 'journalctl -u zion-node -n 50'
   ```

3. Verify Nginx:
   ```bash
   ssh root@91.98.122.165 'nginx -t'
   ```

4. Check firewall:
   ```bash
   ssh root@91.98.122.165 'ufw status'
   ```

**Common Issues:**

- **SSH timeout**: Check server is running and SSH key is configured
- **Port conflicts**: Old services may be running - stop them first
- **Permission denied**: Ensure root SSH access is enabled
- **Nginx config error**: Check domain/SSL certificate settings

## 📝 Manual Verification

After deployment completes:

```bash
# Test HTTPS endpoint
curl -sk https://91.98.122.165/health

# Test RPC (from server)
ssh root@91.98.122.165 'curl http://localhost:8332'

# Check service status
ssh root@91.98.122.165 'systemctl status zion-node'

# View recent logs
ssh root@91.98.122.165 'journalctl -u zion-node -n 100'

# Monitor in real-time
ssh root@91.98.122.165 'htop'
```

## 🔄 Updating Deployment

To update to a newer version:

```bash
# Stop old service
ssh root@91.98.122.165 'systemctl stop zion-node'

# Run new deployment
./deploy-ssh-production.sh

# The script will automatically:
# - Stop old services
# - Update code
# - Restart with new version
```

## 📦 Rollback

If you need to rollback:

```bash
# Stop current version
ssh root@91.98.122.165 'systemctl stop zion-node'

# Deploy previous version
cd /home/zion/ZION/deployment
./deploy_ssh_282_docker.sh  # For 2.8.2
```

## 🙏 Support

For issues or questions:
- Check logs: `journalctl -u zion-node -f`
- Review docs: `/opt/zion-2.8.3/deployment/README.md`
- GitHub: https://github.com/estrelaisabellazion3/Zion-2.8

---

**JAI RAM SITA HANUMAN** ⭐

ZION 2.8.3 "Terra Nova" - Production Ready
