# ZION Nebula Kubernetes Deployment

## Overview

This directory contains Kubernetes manifests for deploying ZION Nebula 2.8.2 in a production-ready, cloud-native environment.

## Architecture

The deployment includes the following components:

- **zion-postgres**: PostgreSQL database for persistent data storage
- **zion-redis**: Redis cache for session management and real-time data
- **zion-blockchain**: Core ZION blockchain node with RPC interface
- **zion-pool**: Mining pool with Stratum protocol support (auto-scaled)
- **zion-websocket**: Real-time WebSocket server for live monitoring
- **zion-dashboard**: Web dashboard with monitoring and management interface

## Prerequisites

- Kubernetes cluster (v1.19+)
- kubectl configured to access the cluster
- Docker registry access to `zion-nebula:latest` image
- NGINX Ingress Controller installed
- cert-manager (optional, for TLS certificates)
- Storage class configured for persistent volumes

## Quick Start

1. **Clone and navigate to the repository:**
   ```bash
   cd /path/to/zion-nebula
   ```

2. **Build and push Docker image:**
   ```bash
   # From the root directory
   cd docker
   ./build.sh
   docker push zion-nebula:latest
   ```

3. **Deploy to Kubernetes:**
   ```bash
   cd k8s
   chmod +x deploy.sh
   ./deploy.sh
   ```

4. **Verify deployment:**
   ```bash
   kubectl get all -n zion-nebula
   ```

## Configuration

### Environment Variables

Key configuration is managed through the `configmap.yaml`:

- `ZION_NETWORK`: Network identifier ("nebula")
- `ZION_P2P_PORT`: P2P network port (8333)
- `ZION_RPC_PORT`: RPC API port (8332)
- `POOL_PORT`: Mining pool port (3333)
- `WEBSOCKET_PORT`: WebSocket server port (8080)

### Secrets

Sensitive data is stored in `secret.yaml`:

- Database credentials
- Redis password
- JWT secrets
- Wallet seeds

### Scaling

The deployment includes HorizontalPodAutoscalers (HPA) for:

- **Mining Pool**: Scales 2-10 replicas based on CPU (70%) and memory (80%) usage
- **WebSocket Server**: Scales 2-5 replicas based on CPU (60%) usage

## Networking

### Services

- **zion-dashboard**: LoadBalancer service on port 80
- **zion-pool**: LoadBalancer service on port 3333 (Stratum)
- **zion-blockchain**: ClusterIP service for internal RPC access
- **zion-websocket**: ClusterIP service for WebSocket connections

### Ingress

The `ingress.yaml` provides external access with:

- SSL/TLS termination
- Path-based routing:
  - `/` → Dashboard
  - `/api` → Blockchain RPC
  - `/ws` → WebSocket server

## Monitoring

### Prometheus Configuration

Metrics collection is configured in `monitoring-config.yaml` with:

- Service discovery for all ZION components
- Alert rules for high CPU usage and service availability
- 15-30 second scrape intervals

### Health Checks

All deployments include:

- Liveness probes for container health
- Readiness probes for service availability
- Resource limits and requests

## Storage

### Persistent Volumes

- **zion-postgres-pvc**: 50GB for database storage
- **zion-blockchain-pvc**: 100GB for blockchain data
- **zion-models-pvc**: 20GB for AI models (future use)

## Troubleshooting

### Common Issues

1. **Pods not starting:**
   ```bash
   kubectl describe pod <pod-name> -n zion-nebula
   kubectl logs <pod-name> -n zion-nebula
   ```

2. **Service not accessible:**
   ```bash
   kubectl get svc -n zion-nebula
   kubectl describe ingress zion-ingress -n zion-nebula
   ```

3. **Storage issues:**
   ```bash
   kubectl get pvc -n zion-nebula
   kubectl describe pvc <pvc-name> -n zion-nebula
   ```

### Logs

View logs for specific components:

```bash
# Blockchain node
kubectl logs -f deployment/zion-blockchain -n zion-nebula

# Mining pool
kubectl logs -f deployment/zion-pool -n zion-nebula

# Dashboard
kubectl logs -f deployment/zion-dashboard -n zion-nebula
```

## Security Considerations

- Secrets are base64 encoded (consider using external secret management)
- Network policies should be added for production
- RBAC should be configured for access control
- TLS certificates are managed by cert-manager

## Scaling for Production

For production deployments:

1. **Increase replica counts** in deployments
2. **Configure resource limits** based on load testing
3. **Set up backup strategies** for persistent data
4. **Configure monitoring and alerting** with external systems
5. **Implement network policies** for security
6. **Set up log aggregation** and analysis

## Cleanup

To remove the entire deployment:

```bash
kubectl delete namespace zion-nebula
```

Or selectively:

```bash
kubectl delete -f k8s/ --ignore-not-found=true
```