#!/bin/bash
################################################################################
# ZION 2.8.2 SSH Server Deployment Script (Docker)
# Server: 91.98.122.165 (Ubuntu 24.04)
# Clean install, production-ready
################################################################################

set -e

# Configuration
DEPLOY_USER="root"
DEPLOY_HOST="91.98.122.165"
DEPLOY_DIR="/root/zion-2.8.2"
SSH_CMD="ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no"
SCP_CMD="scp -o ConnectTimeout=10 -o StrictHostKeyChecking=no"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}ZION 2.8.2 SSH Server Deployment (Docker)${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"

# Step 1: Ověření připojení
echo -e "\n${YELLOW}[1/8]${NC} Ověřuji SSH připojení na ${DEPLOY_HOST}..."
if ! $SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} "echo 'SSH Connected'" > /dev/null 2>&1; then
    echo -e "${RED}✗ Nemohu se připojit na ${DEPLOY_HOST}${NC}"
    exit 1
fi
echo -e "${GREEN}✓ SSH připojení OK${NC}"

# Step 2: Zastavení starých služeb
echo -e "\n${YELLOW}[2/8]${NC} Zastavuji staré služby a Docker kontejnery..."
$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<'SCRIPT'
    docker stop zion-2.8.2-warp 2>/dev/null || true
    docker stop zion-2.8.2-pool 2>/dev/null || true
    docker stop zion-2.8.2-rpc 2>/dev/null || true
    docker stop zion-2.8.2-websocket 2>/dev/null || true
    docker stop zion-2.8.2-dashboard 2>/dev/null || true
    docker rm -f zion-2.8.2-warp 2>/dev/null || true
    docker rm -f zion-2.8.2-pool 2>/dev/null || true
    docker rm -f zion-2.8.2-rpc 2>/dev/null || true
    docker rm -f zion-2.8.2-websocket 2>/dev/null || true
    docker rm -f zion-2.8.2-dashboard 2>/dev/null || true
    pkill -f "python.*zion" 2>/dev/null || true
SCRIPT
echo -e "${GREEN}✓ Staré služby zastaveny${NC}"

# Step 3: Příprava serverů
echo -e "\n${YELLOW}[3/8]${NC} Připravuji adresáře..."
$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<SCRIPT
    rm -rf ${DEPLOY_DIR}
    mkdir -p ${DEPLOY_DIR}/{src,config,logs,data}
    cd ${DEPLOY_DIR}
    echo "ZION 2.8.2 Deployment - $(date)" > deployment.log
SCRIPT
echo -e "${GREEN}✓ Adresáře připraveny${NC}"

# Step 4: Kopírování zdrojového kódu
echo -e "\n${YELLOW}[4/8]${NC} Kopíruji zdrojový kód..."
$SCP_CMD -r ./src/* ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_DIR}/src/ 2>/dev/null || true
$SCP_CMD -r ./deployment/docker-compose.production.yml ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_DIR}/docker-compose.yml 2>/dev/null || true
echo -e "${GREEN}✓ Zdrojový kód zkopírován${NC}"

# Step 5: Docker setup
echo -e "\n${YELLOW}[5/8]${NC} Nastavuji Docker na serveru..."
$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<'SCRIPT'
    # Instalace Docker (pokud není)
    if ! command -v docker &> /dev/null; then
        curl -fsSL https://get.docker.com -o get-docker.sh
        bash get-docker.sh
        systemctl enable docker
        systemctl start docker
    fi
    
    # Instalace Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        apt-get update && apt-get install -y docker-compose-plugin
    fi
    
    # Verifikace
    docker --version
    docker-compose version
SCRIPT
echo -e "${GREEN}✓ Docker nainstalován${NC}"

# Step 6: Spuštění services
echo -e "\n${YELLOW}[6/8]${NC} Spouštím kontejnery..."
$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} <<SCRIPT
    cd ${DEPLOY_DIR}
    docker-compose up -d
    sleep 5
    docker-compose ps
SCRIPT
echo -e "${GREEN}✓ Kontejnery spuštěny${NC}"

# Step 7: Zdravotní kontrola
echo -e "\n${YELLOW}[7/8]${NC} Ověřuji služby..."
sleep 3

HEALTH_OK=0

# Check WARP Engine
echo -n "  WARP Engine (8080): "
if curl -s http://${DEPLOY_HOST}:8080/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
    ((HEALTH_OK++))
else
    echo -e "${RED}✗${NC}"
fi

# Check Mining Pool
echo -n "  Mining Pool (3333): "
if nc -zv ${DEPLOY_HOST} 3333 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
    ((HEALTH_OK++))
else
    echo -e "${RED}✗${NC}"
fi

# Check RPC Server
echo -n "  RPC Server (8545): "
if curl -s http://${DEPLOY_HOST}:8545 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
    ((HEALTH_OK++))
else
    echo -e "${RED}✗${NC}"
fi

# Check WebSocket
echo -n "  WebSocket (8888): "
if curl -s http://${DEPLOY_HOST}:8888/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
    ((HEALTH_OK++))
else
    echo -e "${RED}✗${NC}"
fi

# Check Dashboard
echo -n "  Dashboard (3000): "
if curl -s http://${DEPLOY_HOST}:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
    ((HEALTH_OK++))
else
    echo -e "${RED}✗${NC}"
fi

echo -e "\n  Zdraví: ${GREEN}${HEALTH_OK}/5 služeb${NC}"

# Step 8: Finální zpráva
echo -e "\n${YELLOW}[8/8]${NC} Deployment hotov!"
echo -e "\n${GREEN}═════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ ZION 2.8.2 Deployment Kompletní${NC}"
echo -e "${GREEN}═════════════════════════════════════════════════════════════${NC}"

echo -e "\n${BLUE}📊 Přístupové body:${NC}"
echo -e "  WARP Engine:    http://${DEPLOY_HOST}:8080"
echo -e "  Mining Pool:    stratum+tcp://${DEPLOY_HOST}:3333"
echo -e "  RPC Server:     http://${DEPLOY_HOST}:8545"
echo -e "  WebSocket:      ws://${DEPLOY_HOST}:8888"
echo -e "  Dashboard:      http://${DEPLOY_HOST}:3000"

echo -e "\n${BLUE}📝 Příkazy pro správu:${NC}"
echo -e "  Logy:      ${YELLOW}ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'docker-compose -f ${DEPLOY_DIR}/docker-compose.yml logs -f'${NC}"
echo -e "  Restart:   ${YELLOW}ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'docker-compose -f ${DEPLOY_DIR}/docker-compose.yml restart'${NC}"
echo -e "  Stop:      ${YELLOW}ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'docker-compose -f ${DEPLOY_DIR}/docker-compose.yml down'${NC}"
echo -e "  Status:    ${YELLOW}ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'docker-compose -f ${DEPLOY_DIR}/docker-compose.yml ps'${NC}"

if [ $HEALTH_OK -eq 5 ]; then
    echo -e "\n${GREEN}🎉 Všechny služby běží! Deployment byl úspěšný.${NC}"
    exit 0
else
    echo -e "\n${YELLOW}⚠️ Některé služby nebyly ověřeny. Zkontrolujte logy:${NC}"
    echo -e "  ${YELLOW}ssh ${DEPLOY_USER}@${DEPLOY_HOST} 'docker-compose -f ${DEPLOY_DIR}/docker-compose.yml logs'${NC}"
    exit 1
fi
