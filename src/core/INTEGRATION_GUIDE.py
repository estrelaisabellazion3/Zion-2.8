#!/usr/bin/env python3
"""
ZION Pool Integration - Payment Processor + WebSocket Events
Integrace do zion_universal_pool_v2.py
"""

# ============================================
# PŘIDAT DO zion_universal_pool_v2.py
# ============================================

# 1. Import nových modulů (na začátek souboru):
"""
from payment_processor import PaymentProcessor, create_payment_tables
from websocket_events import PoolEventStreamer
"""

# 2. Do __init__ metody UniversalMiningPool:
"""
class UniversalMiningPool:
    def __init__(self, ...):
        # ... existující kód ...
        
        # Payment processor
        self.payment_processor = None
        if config.get('enable_auto_payments', True):
            self.payment_processor = PaymentProcessor(
                pool=self,
                blockchain_rpc=self.blockchain_rpc,
                db_path=self.db_path
            )
        
        # WebSocket event streamer
        self.event_streamer = None
        if config.get('enable_websocket', True):
            ws_port = config.get('websocket_port', 8765)
            self.event_streamer = PoolEventStreamer(port=ws_port)
"""

# 3. Do start() metody:
"""
async def start(self):
    # ... existující kód ...
    
    # Spustit payment processor
    if self.payment_processor:
        asyncio.create_task(self.payment_processor.start())
    
    # Spustit WebSocket streamer
    if self.event_streamer:
        await self.event_streamer.start()
"""

# 4. Přidat WebSocket události při důležitých akcích:

# V metodě když najdete blok:
"""
async def on_block_found(self, block):
    # ... existující kód ...
    
    # WebSocket event
    if self.event_streamer:
        await self.event_streamer.on_block_found({
            'height': block.height,
            'hash': block.hash,
            'reward': block.reward,
            'miner': block.miner,
            'algorithm': block.algorithm,
            'difficulty': block.difficulty
        })
"""

# Když přijmete validní share:
"""
async def process_share(self, ...):
    # ... existující validace ...
    
    if valid:
        # WebSocket event (jen občas, ne každý share)
        if self.event_streamer and share_count % 10 == 0:
            await self.event_streamer.on_share_submitted({
                'miner': miner_address,
                'difficulty': difficulty,
                'algorithm': algorithm,
                'valid': True
            })
"""

# Když miner připojen:
"""
async def handle_login(self, ...):
    # ... existující kód ...
    
    if self.event_streamer:
        await self.event_streamer.on_miner_connected({
            'address': wallet_address,
            'ip': addr[0],
            'algorithm': algorithm,
            'difficulty': difficulty
        })
"""

# 5. Aktualizovat requirements.txt:
"""
# Přidat:
websockets>=12.0
"""

# 6. Konfigurace v config (např. pro run_pool_production.py):
"""
POOL_CONFIG = {
    # ... existující konfigurace ...
    
    # Payment processor
    'enable_auto_payments': True,
    'payment_threshold': 10.0,  # ZION
    'payment_interval': 3600,   # 1 hodina
    
    # WebSocket events
    'enable_websocket': True,
    'websocket_port': 8765,
}
"""

# ============================================
# SIMPLE HTML CLIENT PRO TESTOVÁNÍ
# ============================================

HTML_CLIENT = """
<!DOCTYPE html>
<html>
<head>
    <title>ZION Pool Events - Live</title>
    <style>
        body { 
            font-family: Arial; 
            background: #1a1a1a; 
            color: #fff;
            padding: 20px;
        }
        .event { 
            margin: 10px 0; 
            padding: 10px; 
            background: #2a2a2a;
            border-left: 4px solid #4CAF50;
            border-radius: 4px;
        }
        .block_found { border-left-color: #FFD700; }
        .payment { border-left-color: #4CAF50; }
        .miner_connected { border-left-color: #2196F3; }
        .timestamp { color: #888; font-size: 0.9em; }
        #status { 
            padding: 10px; 
            background: #333; 
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .connected { color: #4CAF50; }
        .disconnected { color: #f44336; }
    </style>
</head>
<body>
    <h1>🌟 ZION Pool - Live Events</h1>
    <div id="status">Status: <span id="statusText" class="disconnected">Disconnected</span></div>
    <div id="events"></div>

    <script>
        const ws = new WebSocket('ws://localhost:8765');
        const eventsDiv = document.getElementById('events');
        const statusText = document.getElementById('statusText');

        ws.onopen = () => {
            statusText.textContent = 'Connected';
            statusText.className = 'connected';
            console.log('WebSocket connected');
        };

        ws.onclose = () => {
            statusText.textContent = 'Disconnected';
            statusText.className = 'disconnected';
            console.log('WebSocket disconnected');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('Event:', data);
            
            const eventDiv = document.createElement('div');
            eventDiv.className = 'event ' + data.type;
            
            let content = `<strong>${data.type.toUpperCase()}</strong><br>`;
            content += `<span class="timestamp">${data.timestamp}</span><br>`;
            
            if (data.type === 'block_found') {
                content += `Block #${data.data.height} found!<br>`;
                content += `Reward: ${data.data.reward} ZION<br>`;
                content += `Miner: ${data.data.miner}<br>`;
                content += `Algorithm: ${data.data.algorithm}`;
            } else if (data.type === 'payment') {
                content += `Payment sent: ${data.data.amount} ZION<br>`;
                content += `To: ${data.data.address}<br>`;
                content += `TX: ${data.data.tx_hash}`;
            } else if (data.type === 'miner_connected') {
                content += `Miner connected: ${data.data.address}<br>`;
                content += `IP: ${data.data.ip}<br>`;
                content += `Algorithm: ${data.data.algorithm}`;
            } else if (data.type === 'hashrate_update') {
                content += `Pool Hashrate: ${data.data.pool_hashrate} H/s<br>`;
                content += `Active Miners: ${data.data.active_miners}`;
            } else {
                content += JSON.stringify(data.data, null, 2);
            }
            
            eventDiv.innerHTML = content;
            eventsDiv.insertBefore(eventDiv, eventsDiv.firstChild);
            
            // Limit na 50 událostí
            while (eventsDiv.children.length > 50) {
                eventsDiv.removeChild(eventsDiv.lastChild);
            }
        };

        // Keep-alive ping každých 30s
        setInterval(() => {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send('ping');
            }
        }, 30000);
    </script>
</body>
</html>
"""

# Uložit HTML client
with open('/Users/yeshuae/Desktop/ZION/Zion-2.8-main/pool_events_live.html', 'w') as f:
    f.write(HTML_CLIENT)

print("✅ Integration guide created!")
print("📝 Next steps:")
print("1. pip install websockets")
print("2. Add imports to zion_universal_pool_v2.py")
print("3. Initialize payment_processor and event_streamer in __init__")
print("4. Add event calls when blocks found, payments sent, etc.")
print("5. Open pool_events_live.html in browser to see live events")
