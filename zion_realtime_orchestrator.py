#!/usr/bin/env python3
"""
ZION Real-Time Orchestrator
Integrates WebSocket server with existing ZION components for live monitoring
"""

import sys
import os
import time
import threading
import psutil
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import ZION components
from zion_websocket_server import ZIONWebSocketServer, ZIONSocketIOServer
from zion_monitoring_system import ZIONMonitoringSystem, get_monitoring_system
from seednodes import ZionNetworkConfig

class ZIONRealTimeOrchestrator:
    """Real-time orchestrator integrating all ZION components"""

    def __init__(self):
        self.websocket_server = None
        self.socketio_server = None
        self.monitoring_system = ZIONMonitoringSystem()
        self.monitoring_thread = None
        self.running = False

        # System monitoring
        self.start_time = time.time()

    def start_websocket_server(self):
        """Start WebSocket server"""
        try:
            self.websocket_server = ZIONWebSocketServer()
            ws_thread = threading.Thread(target=self._run_websocket_server, daemon=True)
            ws_thread.start()
            print("✅ WebSocket server started on ws://localhost:8080")
        except Exception as e:
            print(f"⚠️  WebSocket server failed: {e}")

    def start_socketio_server(self):
        """Start Socket.IO server as fallback"""
        try:
            self.socketio_server = ZIONSocketIOServer()
            sio_thread = threading.Thread(target=self._run_socketio_server, daemon=True)
            sio_thread.start()
            print("✅ Socket.IO server started on http://localhost:8081")
        except Exception as e:
            print(f"⚠️  Socket.IO server failed: {e}")

    def start_monitoring(self):
        """Start real-time monitoring"""
        self.monitoring_system.start()
        self.monitoring_thread = threading.Thread(target=self._metrics_broadcast_loop, daemon=True)
        self.monitoring_thread.start()
        print("✅ Real-time monitoring started")

    def _run_websocket_server(self):
        """Run WebSocket server in asyncio event loop"""
        import asyncio
        asyncio.run(self.websocket_server.start())

    def _run_socketio_server(self):
        """Run Socket.IO server"""
        self.socketio_server.run()

    def _metrics_broadcast_loop(self):
        """Broadcast metrics from monitoring system to WebSocket servers"""
        while self.running:
            try:
                # Get current metrics from monitoring system
                metrics = self.monitoring_system.get_current_metrics()

                # Update WebSocket servers with real metrics
                if self.websocket_server:
                    # System metrics
                    system = metrics['system']
                    self.websocket_server.update_system_metrics(
                        cpu_usage=system['cpu_percent'],
                        memory_usage=system['memory_percent'],
                        disk_usage=system['disk_percent'],
                        network_rx=metrics['network']['bytes_recv_per_second'],
                        network_tx=metrics['network']['bytes_sent_per_second'],
                        uptime=time.time() - self.start_time
                    )

                    # Mining metrics
                    mining = metrics['mining']
                    self.websocket_server.update_mining_metrics(
                        hashrate=mining['hashrate'],
                        shares_submitted=mining['shares_submitted'],
                        shares_accepted=mining['shares_accepted'],
                        shares_rejected=mining['shares_rejected'],
                        blocks_found=mining['blocks_found'],
                        difficulty=mining['current_difficulty'],
                        temperature=65.0,  # Placeholder - would come from actual hardware monitoring
                        power_consumption=200.0,  # Placeholder
                        efficiency=85.0  # Placeholder
                    )

                    # AI metrics (placeholder for now)
                    self.websocket_server.update_ai_metrics(
                        active_models=2,
                        predictions_made=100,
                        optimization_cycles=10,
                        consciousness_level=0.75,
                        rize_energy=0.80
                    )

                if self.socketio_server:
                    # Update Socket.IO server with same metrics
                    system = metrics['system']
                    self.socketio_server.update_system_metrics(
                        cpu_usage=system['cpu_percent'],
                        memory_usage=system['memory_percent'],
                        disk_usage=system['disk_percent'],
                        network_rx=metrics['network']['bytes_recv_per_second'],
                        network_tx=metrics['network']['bytes_sent_per_second'],
                        uptime=time.time() - self.start_time
                    )

                    mining = metrics['mining']
                    self.socketio_server.update_mining_metrics(
                        hashrate=mining['hashrate'],
                        shares_submitted=mining['shares_submitted'],
                        shares_accepted=mining['shares_accepted'],
                        shares_rejected=mining['shares_rejected'],
                        blocks_found=mining['blocks_found'],
                        difficulty=mining['current_difficulty'],
                        temperature=65.0,
                        power_consumption=200.0,
                        efficiency=85.0
                    )

                    self.socketio_server.update_ai_metrics(
                        active_models=2,
                        predictions_made=100,
                        optimization_cycles=10,
                        consciousness_level=0.75,
                        rize_energy=0.80
                    )

                time.sleep(1)  # Broadcast every second

            except Exception as e:
                print(f"⚠️  Metrics broadcast error: {e}")
                time.sleep(5)

    def stop(self):
        """Stop all services"""
        print("🛑 Stopping ZION Real-Time Orchestrator...")
        self.running = False

        if self.monitoring_system:
            self.monitoring_system.stop()

        if self.websocket_server:
            self.websocket_server.stop()

        print("✅ Real-Time Orchestrator stopped")

    def _update_mining_metrics(self):
        """Update mining metrics (placeholder for real mining integration)"""
        # This would integrate with actual mining pool/miner stats
        # For now, simulate some activity
        import random

        hashrate = 500000 + random.randint(-50000, 50000)  # ~500 KH/s ±50KH/s
        temperature = 45.0 + random.uniform(-5, 5)  # 45°C ±5°C
        power = 150.0 + random.uniform(-10, 10)  # 150W ±10W

        if self.websocket_server:
            self.websocket_server.update_mining_metrics(
                hashrate=hashrate,
                temperature=temperature,
                power_consumption=power,
                efficiency=85.0 + random.uniform(-5, 5)
            )

        if self.socketio_server:
            self.socketio_server.update_mining_metrics(
                hashrate=hashrate,
                temperature=temperature,
                power_consumption=power,
                efficiency=85.0 + random.uniform(-5, 5)
            )

    def _update_ai_metrics(self):
        """Update AI metrics (placeholder for real AI integration)"""
        # This would integrate with actual AI orchestrator stats
        import random

        consciousness = 0.6 + random.uniform(-0.1, 0.1)  # Base 0.6 ±0.1
        rize_energy = 0.7 + random.uniform(-0.1, 0.1)    # Base 0.7 ±0.1

        if self.websocket_server:
            self.websocket_server.update_ai_metrics(
                active_models=2 + random.randint(0, 2),
                consciousness_level=consciousness,
                rize_energy=rize_energy
            )

        if self.socketio_server:
            self.socketio_server.update_ai_metrics(
                active_models=2 + random.randint(0, 2),
                consciousness_level=consciousness,
                rize_energy=rize_energy
            )

    def start(self):
        """Start all real-time services"""
        print("🚀 Starting ZION Real-Time Orchestrator...")
        self.running = True

        # Start WebSocket server
        self.start_websocket_server()

        # Start Socket.IO server
        self.start_socketio_server()

        # Start monitoring
        self.start_monitoring()

        print("✅ ZION Real-Time Orchestrator started successfully")
        print("🌐 WebSocket: ws://localhost:8080")
        print("🌐 Socket.IO: http://localhost:8081")
        print("📊 Monitor: Open zion_websocket_monitor.html in browser")
        print("🛑 Press Ctrl+C to stop")

    def stop(self):
        """Stop all services"""
        print("🛑 Stopping ZION Real-Time Orchestrator...")
        self.running = False

        if self.websocket_server:
            self.websocket_server.stop()

        print("✅ Real-Time Orchestrator stopped")

def main():
    """Main entry point"""
    orchestrator = ZIONRealTimeOrchestrator()

    try:
        orchestrator.start()

        # Keep running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        orchestrator.stop()

if __name__ == "__main__":
    main()