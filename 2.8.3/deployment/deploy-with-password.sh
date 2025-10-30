#!/bin/bash
# Temporary deployment script with password authentication

set -e

DEPLOY_USER="root"
DEPLOY_HOST="91.98.122.165"
DEPLOY_DIR="/opt/zion-2.8.3"
LOCAL_ZION_DIR="/home/zion/ZION"
LOCAL_DEPLOY_DIR="/home/zion/ZION/2.8.3/deployment"

# SSH with password (temporary)
export SSHPASS='x3nityOne144'
SSH_CMD="sshpass -e ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no"
SCP_CMD="sshpass -e scp -o ConnectTimeout=10 -o StrictHostKeyChecking=no -r"

echo "Testing SSH connection with password..."
$SSH_CMD ${DEPLOY_USER}@${DEPLOY_HOST} "echo 'SSH OK!' && hostname"

if [ $? -eq 0 ]; then
    echo "✓ SSH connection successful!"
    echo "Now running main deployment script..."
    
    # Update the main script to use password auth temporarily
    sed -i 's|SSH_CMD="ssh -i $SSH_KEY|SSH_CMD="sshpass -e ssh|g' deploy-ssh-production.sh
    sed -i 's|SCP_CMD="scp -i $SSH_KEY|SCP_CMD="sshpass -e scp|g' deploy-ssh-production.sh
    
    export SSHPASS='x3nityOne144'
    ./deploy-ssh-production.sh
else
    echo "✗ SSH connection failed"
    exit 1
fi
