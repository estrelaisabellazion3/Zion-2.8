# ZION 2.8.2 Nebula - Docker Setup

This directory contains Docker configuration for deploying ZION 2.8.2 Nebula in containerized environments.

## Architecture

The ZION Nebula stack consists of the following services:

- **zqal-sdk**: ZQAL SDK with real-time WebSocket monitoring and AI orchestration
- **zion-node**: ZION blockchain node with RPC and P2P interfaces
- **mining-pool**: Stratum mining pool with Cosmic Harmony algorithm support
- **rainbow-bridge**: Lightning Network and cross-chain bridge services
- **web-monitor**: Nginx web server serving the real-time monitoring dashboard

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 10GB+ disk space

### Build Images

```bash
# Make build script executable
chmod +x docker/build.sh

# Build all images
./docker/build.sh
```

### Start Services

```bash
# Start the complete stack
docker-compose -f docker/docker-compose.zqal.yml up -d

# View logs
docker-compose -f docker/docker-compose.zqal.yml logs -f

# Check status
docker-compose -f docker/docker-compose.zqal.yml ps
```

### Access Services

- **Web Monitor**: http://localhost
- **WebSocket Server**: ws://localhost:8080
- **Socket.IO Server**: http://localhost:8081
- **ZION RPC**: http://localhost:18089
- **Mining Pool Stratum**: stratum+tcp://localhost:3333
- **Mining Pool API**: http://localhost:3334

## Development Setup

For development with live code reloading:

```bash
# Start with development overrides
docker-compose -f docker/docker-compose.zqal.yml -f docker/docker-compose.override.yml up -d

# View real-time logs
docker-compose -f docker/docker-compose.zqal.yml logs -f zqal-sdk
```

## Configuration

### Environment Variables

Copy `docker/.env` and modify as needed:

```bash
cp docker/.env docker/.env.local
# Edit docker/.env.local with your settings
```

Key configuration options:

- `ZION_RPC_TOKEN`: RPC authentication token
- `ZION_NETWORK`: Network type (mainnet/testnet)
- `MINING_DIFFICULTY`: Mining difficulty level
- `LOG_LEVEL`: Logging verbosity
- `MONITORING_ENABLED`: Enable real-time monitoring

### Resource Limits

Default resource limits can be adjusted in `docker-compose.zqal.yml`:

```yaml
services:
  zqal-sdk:
    deploy:
      resources:
        limits:
          memory: 2GB
          cpus: '2.0'
```

## Monitoring

### Real-time Dashboard

Open http://localhost in your browser to access the real-time monitoring dashboard showing:

- Mining metrics (hashrate, shares, blocks found)
- AI metrics (consciousness level, RIZE energy)
- System metrics (CPU, memory, network usage)
- Live event log

### WebSocket API

Connect to WebSocket endpoints for programmatic access:

```javascript
// WebSocket connection
const ws = new WebSocket('ws://localhost:8080');

// Subscribe to metrics
ws.onopen = () => {
    ws.send(JSON.stringify({
        type: 'subscribe',
        channels: ['mining_metrics', 'ai_metrics', 'system_metrics']
    }));
};

// Handle messages
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

### Health Checks

Check service health:

```bash
# Individual services
docker-compose -f docker/docker-compose.zqal.yml exec zqal-sdk python -c "print('OK')"
docker-compose -f docker/docker-compose.zqal.yml exec zion-node curl -f http://localhost:18089/health

# All services
docker-compose -f docker/docker-compose.zqal.yml ps
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports in `docker-compose.zqal.yml` if needed
2. **Memory issues**: Increase Docker memory limit or reduce service resource limits
3. **Build failures**: Ensure all dependencies are available and try `docker system prune`

### Logs and Debugging

```bash
# View all logs
docker-compose -f docker/docker-compose.zqal.yml logs

# View specific service logs
docker-compose -f docker/docker-compose.zqal.yml logs zqal-sdk

# Follow logs in real-time
docker-compose -f docker/docker-compose.zqal.yml logs -f

# Enter container for debugging
docker-compose -f docker/docker-compose.zqal.yml exec zqal-sdk bash
```

### Reset and Clean

```bash
# Stop and remove all containers
docker-compose -f docker/docker-compose.zqal.yml down

# Remove volumes (WARNING: deletes all data)
docker-compose -f docker/docker-compose.zqal.yml down -v

# Clean up unused images
docker image prune -f
```

## Production Deployment

For production deployment:

1. Use external databases instead of SQLite
2. Configure SSL/TLS certificates
3. Set up proper logging and monitoring
4. Configure firewall rules
5. Use Docker secrets for sensitive data
6. Set up backup and recovery procedures

### Example Production Compose

```yaml
version: '3.8'
services:
  zqal-sdk:
    image: zion/zqal-sdk:latest
    environment:
      - LOG_LEVEL=WARNING
      - MONITORING_ENABLED=true
    secrets:
      - rpc_token
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 4GB
          cpus: '4.0'

secrets:
  rpc_token:
    file: /path/to/rpc_token.txt
```

## Security Considerations

- Change default passwords and tokens
- Use Docker secrets for sensitive data
- Regularly update base images
- Monitor container logs for security events
- Implement proper network segmentation
- Use TLS for external communications

## Contributing

When making changes to Docker configuration:

1. Test builds locally: `./docker/build.sh`
2. Test deployment: `docker-compose -f docker/docker-compose.zqal.yml up -d`
3. Update documentation if needed
4. Ensure backward compatibility

## Support

For issues and questions:

- Check logs: `docker-compose -f docker/docker-compose.zqal.yml logs`
- View container status: `docker-compose -f docker/docker-compose.zqal.yml ps`
- Check resource usage: `docker stats`