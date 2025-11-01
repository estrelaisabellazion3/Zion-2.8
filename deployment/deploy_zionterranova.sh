#!/usr/bin/env bash
set -euo pipefail

# Deploy ZION v2.8.4 stack to a remote host and obtain Let's Encrypt certs
# Usage:
#   TARGET=user@www.zionterranova.com EMAIL=you@example.com ./deployment/deploy_zionterranova.sh
# Optional:
#   BRANCH=v2.8.4 (defaults to current branch), REMOTE_DIR=/opt/zion/Zion-2.8

TARGET="${TARGET:-}"
EMAIL="${EMAIL:-${LETSENCRYPT_EMAIL:-}}"
DOMAIN="${DOMAIN:-zionterranova.com}"
BRANCH="${BRANCH:-}"
REMOTE_DIR="${REMOTE_DIR:-/opt/zion/Zion-2.8}"
COMPOSE_FILE="deployment/docker-compose.2.8.4-production.yml"

if [[ -z "${TARGET}" ]]; then
  echo "ERROR: Set TARGET=user@host (e.g., TARGET=ubuntu@www.zionterranova.com)"
  exit 1
fi

if [[ -z "${EMAIL}" ]]; then
  echo "ERROR: Set EMAIL=admin@example.com for Let's Encrypt registration"
  exit 1
fi

# Create remote directory and sync repository
ssh -o StrictHostKeyChecking=accept-new "$TARGET" "sudo mkdir -p $(dirname $REMOTE_DIR) && sudo chown -R \"$USER\" $(dirname $REMOTE_DIR)"

# Prefer rsync to keep local changes; fallback to tar if unavailable
if command -v rsync >/dev/null 2>&1; then
  rsync -az --delete --exclude ".git" ./ "$TARGET:$REMOTE_DIR/"
else
  echo "rsync not found locally, using tar | ssh"
  tar -czf - . --exclude .git | ssh "$TARGET" "mkdir -p $REMOTE_DIR && tar -xzf - -C $REMOTE_DIR"
fi

# Ensure Docker and Compose are available
ssh "$TARGET" "docker --version && docker compose version >/dev/null 2>&1 || (echo 'Docker Compose v2 required' && exit 1)"

# Open ports 80/443 if UFW exists (best-effort)
ssh "$TARGET" "if command -v ufw >/dev/null 2>&1; then sudo ufw allow 80/tcp || true; sudo ufw allow 443/tcp || true; fi"

# Build node image (uses Dockerfile.node COPY strategy)
ssh "$TARGET" "cd $REMOTE_DIR && docker compose -f $COMPOSE_FILE build zion-node"

# Start node + nginx (HTTP only) so ACME challenge works
ssh "$TARGET" "cd $REMOTE_DIR && docker compose -f $COMPOSE_FILE up -d zion-node nginx"

# Obtain/renew certificates using webroot
ssh "$TARGET" "cd $REMOTE_DIR && \
  docker compose -f $COMPOSE_FILE run --rm certbot certonly \
    --webroot -w /var/www/certbot \
    -d $DOMAIN -d www.$DOMAIN \
    --email $EMAIL --agree-tos --non-interactive ${LETSENCRYPT_STAGING:+--staging}"

# Reload nginx to pick up new certs
ssh "$TARGET" "docker exec zion-2.8.4-nginx nginx -s reload || true"

# Health checks
echo "Waiting for HTTPS to become available..."
sleep 3
set +e
ssh "$TARGET" "curl -fsS https://$DOMAIN/api/status >/dev/null" && echo "HTTPS /api/status OK" || echo "WARN: /api/status not reachable yet"
set -e

echo "Deployment completed. Visit: https://$DOMAIN"
