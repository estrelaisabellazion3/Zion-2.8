# ZION Source Code Structure

Production source code for ZION Blockchain v2.8.2 "Nebula"

## 📁 Directory Structure

### `core/`
Blockchain core components:
- `new_zion_blockchain.py` - Main blockchain implementation
- `blockchain_rpc_client.py` - RPC client interface
- `crypto_utils.py` - Cryptographic utilities
- `security_validators.py` - Security validation
- `zion_p2p_network.py` - P2P networking
- `zion_rpc_server.py` - RPC server
- `zion_universal_pool_v2.py` - Universal mining pool
- `zion_warp_engine_core.py` - WARP Engine orchestrator
- `Dashboard.py` - Monitoring dashboard

### `orchestration/`
Multi-pool and AI orchestration:
- `ai_orchestrator_backend.py` - AI orchestration backend
- `multi_pool_orchestrator.py` - Multi-pool coordinator
- `multi_pool_master_orchestrator.py` - Master orchestrator
- `geographic_load_balancer.py` - Geographic load balancing
- `intelligent_pool_switcher.py` - Smart pool switching
- `zion_realtime_orchestrator.py` - Real-time orchestration
- `zion_websocket_server.py` - WebSocket server

### `bridges/`
Cross-chain bridges:
- `solana_bridge_anchor.py` - Solana Anchor bridge
- `stellar_bridge_humanitarian.py` - Stellar humanitarian bridge
- `warp_bridge_production.py` - WARP production bridge
- `warp_bridge_poc.py` - WARP proof-of-concept
- `zion_path_payments.py` - Stellar path payments
- `zion_stellar_asset.py` - Stellar asset management

### `mining/`
Consciousness mining:
- `consciousness_mining_game.py` - Consciousness mining game mechanics

### `integrations/`
External integrations:
- `fiat_ramp_integration.py` - Fiat on/off ramps
- `lightning_rainbow_config.py` - Lightning Network config
- `estrella_solar_system.py` - Estrella Solar System integration
- `zion_monitoring_system.py` - System monitoring
- `zion_round_table_ai_integration.py` - Round Table AI
- `zion_round_table_council.py` - Round Table Council

## 🚀 Usage

Import from src modules:
```python
from src.core import new_zion_blockchain
from src.orchestration import ai_orchestrator_backend
from src.bridges import solana_bridge_anchor
```

## 📝 Notes

All production code has been organized into logical modules for better maintainability and clarity.
