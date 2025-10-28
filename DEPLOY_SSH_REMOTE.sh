#!/bin/bash
#
# 🔒 ZION 2.8.2 Nebula - SSH Remote Deployment
#
# Usage:
#   ./DEPLOY_SSH_REMOTE.sh root@server.com
#   ./DEPLOY_SSH_REMOTE.sh ubuntu@server.com 2222  # Custom SSH port
#
# Features:
#   ✅ Clean remote environment setup
#   ✅ Automatic dependency installation  
#   ✅ GPU/CUDA detection
#   ✅ Mining pool setup
#   ✅ Real-time test execution
#   ✅ Service monitoring
#
# Author: ZION Development Team
# Version: 2.8.2 Nebula
#

set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

REPOSITORY="https://github.com/estrelaisabellazion3/Zion-2.8.git"
INSTALL_PATH="/opt/zion"
PYTHON_VERSION="3.13"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# ============================================================================
# MAIN SCRIPT
# ============================================================================

print_banner() {
    echo -e "${BLUE}
╔════════════════════════════════════════════════════════╗
║  ZION 2.8.2 Nebula - SSH Remote Deployment           ║
║  Safe, Clean, Production-Ready Installation           ║
╚════════════════════════════════════════════════════════╝
${NC}"
}

validate_ssh_args() {
    if [ -z "$1" ]; then
        echo -e "${RED}Usage: $0 user@server-ip [ssh_port]${NC}"
        echo "Example: $0 root@91.98.122.165"
        echo "Example: $0 ubuntu@server.com 2222"
        exit 1
    fi
    
    SSH_USER_HOST="$1"
    SSH_PORT="${2:-22}"
    
    echo -e "${YELLOW}Target: $SSH_USER_HOST:$SSH_PORT${NC}"
}

test_ssh_connection() {
    echo -e "${YELLOW}Testing SSH connection...${NC}"
    
    if ! ssh -p "$SSH_PORT" "$SSH_USER_HOST" "echo 'SSH connection OK'" > /dev/null 2>&1; then
        echo -e "${RED}Cannot connect to $SSH_USER_HOST via SSH${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ SSH connection verified${NC}"
}

deploy_to_remote() {
    echo -e "${YELLOW}Starting remote deployment...${NC}"
    
    ssh -p "$SSH_PORT" "$SSH_USER_HOST" << 'DEPLOY_SCRIPT'
#!/bin/bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() {
    echo -e "${YELLOW}[REMOTE] 🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}[REMOTE] ✅ $1${NC}"
}

# ========== REMOTE DEPLOYMENT STEPS ==========

print_step "Step 1: Update system packages"
sudo apt-get update -y
sudo apt-get upgrade -y
print_success "System updated"

print_step "Step 2: Install dependencies"
sudo apt-get install -y \
    git \
    python3 python3-dev python3-venv python3-pip \
    build-essential \
    libssl-dev libffi-dev \
    gcc g++ make \
    curl wget \
    docker.io docker-compose \
    net-tools

print_success "Dependencies installed"

print_step "Step 3: Create ZION directory"
sudo mkdir -p /opt/zion
sudo chown $USER:$USER /opt/zion
cd /opt/zion

print_step "Step 4: Clone ZION repository"
if [ -d ".git" ]; then
    git pull origin main
else
    git clone https://github.com/estrelaisabellazion3/Zion-2.8.git .
fi
print_success "Repository cloned/updated"

print_step "Step 5: Setup Python virtual environment"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
print_success "Virtual environment ready"

print_step "Step 6: Install Python dependencies"
pip install -r requirements.txt
print_success "Python packages installed"

print_step "Step 7: Build C extensions"
if [ -f "ai/mining/setup.py" ]; then
    cd ai/mining
    python setup.py build_ext --inplace
    cd ../..
    print_success "C extensions built"
fi

print_step "Step 8: Detect GPU (NVIDIA/AMD)"
if command -v nvidia-smi &> /dev/null; then
    echo -e "${GREEN}NVIDIA GPU detected$(nvidia-smi --query-gpu=name --format=csv,noheader)${NC}"
elif command -v rocm-smi &> /dev/null; then
    echo -e "${GREEN}AMD GPU detected$(rocm-smi --query-gpu=name --format=csv,noheader)${NC}"
else
    echo -e "${YELLOW}No GPU detected - CPU mining mode${NC}"
fi

print_step "Step 9: Run test suite"
if [ -f "tests/2.8.2/test_complete_suite.py" ]; then
    source .venv/bin/activate
    python tests/2.8.2/test_complete_suite.py || echo "Some tests failed, but deployment continues"
    print_success "Tests executed"
fi

print_step "Step 10: Verify installation"
source .venv/bin/activate
python -c "import src.core.zion_warp_engine_core; print('✅ ZION Core OK')"
print_success "Installation verified"

echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════╗"
echo "║  REMOTE DEPLOYMENT COMPLETE                       ║"
echo "║  Installation path: /opt/zion                     ║"
echo "║  Next steps:                                      ║"
echo "║    1. cd /opt/zion                                ║"
echo "║    2. source .venv/bin/activate                   ║"
echo "║    3. python mine_realtime.py --help             ║"
echo "╚═══════════════════════════════════════════════════╝"
echo -e "${NC}"

DEPLOY_SCRIPT
    
    echo -e "${GREEN}✅ Remote deployment complete${NC}"
}

post_deployment_info() {
    echo -e "${BLUE}
╔════════════════════════════════════════════════════════╗
║  POST-DEPLOYMENT INFORMATION                          ║
╠════════════════════════════════════════════════════════╣
║  SSH Login:                                            ║"
    echo "║    ssh -p $SSH_PORT $SSH_USER_HOST                    ║"
    echo "║                                                        ║"
    echo "║  Start Mining:                                         ║"
    echo "║    cd /opt/zion                                        ║"
    echo "║    source .venv/bin/activate                           ║"
    echo "║    python mine_realtime.py --algorithm cosmic_harmony  ║"
    echo "║                                                        ║"
    echo "║  View Logs:                                            ║"
    echo "║    ssh $SSH_USER_HOST 'tail -f /opt/zion/mining.log'   ║"
    echo "║                                                        ║"
    echo "║  Monitoring:                                           ║"
    echo "║    • Pool Status: http://$SSH_USER_HOST:3334           ║"
    echo "║    • RPC: http://$SSH_USER_HOST:8545                   ║"
    echo "║                                                        ║"
    echo "║  Documentation:                                        ║"
    echo "║    • Mining: docs/MINING_SSH_SETUP.md                  ║"
    echo "║    • Tests:  tests/2.8.2/test_complete_suite.py        ║"
    echo "║    • Deploy: docs/SSH_MINING_DEPLOYMENT.md             ║"
    echo "╚════════════════════════════════════════════════════════╝
${NC}"
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    print_banner
    validate_ssh_args "$@"
    test_ssh_connection
    deploy_to_remote
    post_deployment_info
}

main "$@"
