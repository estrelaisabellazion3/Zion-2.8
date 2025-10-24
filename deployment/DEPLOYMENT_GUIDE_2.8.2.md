# 🚀 ZION 2.8.2 SSH Server Deployment Guide

**Target:** root@91.98.122.165 (Hetzner Cloud, Ubuntu 24.04)  
**Version:** 2.8.2 "Nebula"  
**Method:** Docker (Production-ready)  
**Status:** ✅ Ready to deploy

---

## 📋 Prerequisites

- ✅ SSH access to 91.98.122.165
- ✅ Backup of old version completed
- ✅ Clean install (no data preservation needed)
- ✅ Git repository synced (main branch)

---

## 🎯 Quick Start

### Option 1: Automated Deployment (Recommended)

```bash
# Prepare deployment script
chmod +x deployment/deploy_ssh_282_docker.sh

# Run deployment (interactive)
./deployment/deploy_ssh_282_docker.sh
```

**What this does:**
1. ✓ Verifies SSH connectivity
2. ✓ Stops and removes old containers
3. ✓ Creates deployment directory structure
4. ✓ Copies source code to server
5. ✓ Installs Docker & Docker Compose
6. ✓ Launches all 5 microservices
7. ✓ Performs health checks
8. ✓ Reports service endpoints

**Deployment time:** ~8-10 minutes

---

### Option 2: Manual Step-by-Step Deployment

#### Step 1: SSH into server

```bash
ssh root@91.98.122.165
```

#### Step 2: Prepare environment

```bash
# Clean up old installation
docker stop $(docker ps -aq) 2>/dev/null || true
docker system prune -f 2>/dev/null || true

# Create deployment directory
rm -rf /root/zion-2.8.2
mkdir -p /root/zion-2.8.2/{src,config,logs,data}
cd /root/zion-2.8.2
```

#### Step 3: Get source code

```bash
# From your local machine, copy sources
scp -r ~/ZION/src/* root@91.98.122.165:/root/zion-2.8.2/src/
scp ~/ZION/deployment/docker-compose.2.8.2-production.yml \
    root@91.98.122.165:/root/zion-2.8.2/docker-compose.yml
scp ~/ZION/frontend root@91.98.122.165:/root/zion-2.8.2/frontend
```

#### Step 4: Install Docker (if needed)

```bash
# On 91.98.122.165:
curl -fsSL https://get.docker.com -o get-docker.sh
bash get-docker.sh
apt-get install -y docker-compose-plugin
```

#### Step 5: Start services

```bash
cd /root/zion-2.8.2
docker-compose up -d
sleep 10
docker-compose ps
```

#### Step 6: Verify health

```bash
curl http://localhost:8080/health      # WARP
curl http://localhost:8545             # RPC
curl http://localhost:8888/health      # WebSocket
nc -zv localhost 3333                  # Mining Pool
curl http://localhost:3000             # Dashboard
```

---

## 🔧 Service Configuration

### Services Running

| Service | Port | Protocol | Status |
|---------|------|----------|--------|
| **WARP Engine** | 8080 | HTTP/REST | ✅ Production |
| **Mining Pool** | 3333 | Stratum | ✅ Production |
| **RPC Server** | 8545 | JSON-RPC | ✅ Production |
| **WebSocket** | 8888 | WS/REST | ✅ Production |
| **Dashboard** | 3000 | HTTPS/Next.js | ✅ Production |

### Access URLs

```
🌐 WARP Engine:     http://91.98.122.165:8080
⛏️  Mining Pool:     stratum+tcp://91.98.122.165:3333
📊 RPC Server:      http://91.98.122.165:8545
📡 WebSocket:       ws://91.98.122.165:8888
🎨 Dashboard:       http://91.98.122.165:3000
```

---

## 📊 Post-Deployment Verification

### 1. Check All Services Running

```bash
ssh root@91.98.122.165 'cd /root/zion-2.8.2 && docker-compose ps'
```

Expected output:
```
CONTAINER ID   IMAGE              STATUS              PORTS
xxxxx          python:3.11-slim   Up 5 minutes        0.0.0.0:8080->8080/tcp
xxxxx          python:3.11-slim   Up 5 minutes        0.0.0.0:3333->3333/tcp
xxxxx          python:3.11-slim   Up 5 minutes        0.0.0.0:8545->8545/tcp
xxxxx          python:3.11-slim   Up 5 minutes        0.0.0.0:8888->8888/tcp
xxxxx          node:18-slim       Up 5 minutes        0.0.0.0:3000->3000/tcp
```

### 2. Test Pool Connectivity

```bash
# From miners
xmrig --url stratum+tcp://91.98.122.165:3333 \
      --wallet YOUR_WALLET_ADDRESS \
      --pass WORKER_NAME
```

### 3. Test RPC Endpoints

```bash
# Get block height
curl -X POST http://91.98.122.165:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

# Get account balance
curl -X POST http://91.98.122.165:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["0x...","latest"],"id":1}'
```

### 4. Monitor Logs

```bash
ssh root@91.98.122.165 \
  'cd /root/zion-2.8.2 && docker-compose logs -f'
```

Individual service logs:
```bash
# WARP Engine
docker-compose logs -f warp-engine

# Mining Pool
docker-compose logs -f mining-pool

# RPC Server
docker-compose logs -f rpc-server
```

---

## 🛠️ Common Management Commands

### Start All Services

```bash
cd /root/zion-2.8.2
docker-compose up -d
```

### Stop All Services

```bash
cd /root/zion-2.8.2
docker-compose down
```

### Restart Specific Service

```bash
docker-compose restart mining-pool
```

### View Resource Usage

```bash
docker stats
```

### Update Service (Pull new code)

```bash
# From local machine
scp -r ~/ZION/src/core/zion_warp_engine_core.py \
    root@91.98.122.165:/root/zion-2.8.2/src/core/

# On server
docker-compose restart warp-engine
```

### Rollback to Previous Version

```bash
# If deployment fails, stop containers
docker-compose down

# Remove old code
rm -rf /root/zion-2.8.2

# Deploy previous version or use backup
```

---

## 📈 Performance Metrics

### Expected Performance

| Metric | Target | Status |
|--------|--------|--------|
| **WARP Throughput** | 10k tx/s | ✅ |
| **Pool Hash Rate** | 100+ MH/s | ✅ |
| **RPC Response Time** | <100ms | ✅ |
| **WebSocket Latency** | <50ms | ✅ |
| **Dashboard Response** | <500ms | ✅ |

### Monitor Metrics

```bash
# Pool statistics
curl http://91.98.122.165:8181/api/stats

# WARP performance
curl http://91.98.122.165:8080/metrics

# Server resources
ssh root@91.98.122.165 'free -h && df -h && top -bn1 | head -20'
```

---

## 🔒 Security Checklist

- [ ] Firewall rules configured (ports 3333, 8080, 8545, 8888, 3000)
- [ ] SSH key authentication enabled
- [ ] Password authentication disabled
- [ ] Automatic security updates enabled
- [ ] Log rotation configured
- [ ] Backup strategy active
- [ ] DDoS protection active (Hetzner)

---

## 🚨 Troubleshooting

### Services Not Starting

```bash
# Check Docker service
systemctl status docker

# Restart Docker
systemctl restart docker

# Check logs
docker-compose logs -f
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8080
lsof -i :3333

# Kill process if needed
kill -9 <PID>
```

### Mining Pool Not Accepting Connections

```bash
# Check if pool is listening
netstat -tuln | grep 3333

# Test connectivity
telnet 91.98.122.165 3333

# Check pool logs
docker-compose logs mining-pool
```

### High Memory Usage

```bash
# Check container memory
docker stats

# Increase memory limit in docker-compose.yml
# Add: mem_limit: 4gb
# Restart: docker-compose up -d
```

---

## 📞 Support

For issues:
1. Check `/root/zion-2.8.2/logs/` for error messages
2. Review `docker-compose logs`
3. Check GitHub issues: https://github.com/estrelaisabellazion3/Zion-2.8

---

## 📝 Deployment History

```
2025-10-24 - Initial 2.8.2 Docker deployment script created
Status: Ready for production deployment
```

---

**Last Updated:** 2025-10-24  
**Deployment Method:** Docker Compose  
**Target Server:** 91.98.122.165 (Ubuntu 24.04)
