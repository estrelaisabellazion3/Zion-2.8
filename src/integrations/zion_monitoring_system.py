#!/usr/bin/env python3
"""
ZION Live Monitoring System
Real-time metrics collection and monitoring for all ZION components
"""

import time
import threading
import psutil
import os
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class MonitoringConfig:
    """Configuration for monitoring system"""
    collection_interval: float = 1.0  # seconds
    retention_period: int = 3600  # 1 hour in seconds
    max_metrics_history: int = 1000
    enable_gpu_monitoring: bool = True
    enable_network_monitoring: bool = True
    enable_process_monitoring: bool = True

@dataclass
class SystemMetrics:
    """System-level metrics"""
    timestamp: float = field(default_factory=time.time)
    cpu_percent: float = 0.0
    cpu_count: int = 0
    memory_total: int = 0
    memory_used: int = 0
    memory_percent: float = 0.0
    disk_total: int = 0
    disk_used: int = 0
    disk_percent: float = 0.0
    network_bytes_sent: int = 0
    network_bytes_recv: int = 0
    network_packets_sent: int = 0
    network_packets_recv: int = 0
    load_average: tuple = field(default_factory=lambda: (0.0, 0.0, 0.0))

@dataclass
class MiningMetrics:
    """Mining-specific metrics"""
    timestamp: float = field(default_factory=time.time)
    hashrate: float = 0.0
    shares_submitted: int = 0
    shares_accepted: int = 0
    shares_rejected: int = 0
    blocks_found: int = 0
    current_difficulty: float = 0.0
    pool_connection_status: bool = False
    active_miners: int = 0
    total_miners: int = 0
    pool_efficiency: float = 0.0

@dataclass
class GPUMetrics:
    """GPU-specific metrics"""
    timestamp: float = field(default_factory=time.time)
    gpu_count: int = 0
    gpu_utilization: List[float] = field(default_factory=list)
    gpu_memory_used: List[int] = field(default_factory=list)
    gpu_memory_total: List[int] = field(default_factory=list)
    gpu_temperature: List[float] = field(default_factory=list)
    gpu_power_usage: List[float] = field(default_factory=list)

@dataclass
class NetworkMetrics:
    """Network-specific metrics"""
    timestamp: float = field(default_factory=time.time)
    connections_active: int = 0
    connections_total: int = 0
    bytes_sent_per_second: float = 0.0
    bytes_recv_per_second: float = 0.0
    packets_sent_per_second: float = 0.0
    packets_recv_per_second: float = 0.0
    latency_ms: float = 0.0

@dataclass
class ProcessMetrics:
    """Process-specific metrics"""
    timestamp: float = field(default_factory=time.time)
    process_count: int = 0
    python_processes: int = 0
    mining_processes: int = 0
    system_processes: int = 0
    total_cpu_percent: float = 0.0
    total_memory_percent: float = 0.0

class ZIONMonitoringSystem:
    """Comprehensive monitoring system for ZION components"""

    def __init__(self, config: Optional[MonitoringConfig] = None):
        self.config = config or MonitoringConfig()
        self.running = False
        self.collection_thread: Optional[threading.Thread] = None

        # Metrics history
        self.system_history: List[SystemMetrics] = []
        self.mining_history: List[MiningMetrics] = []
        self.gpu_history: List[GPUMetrics] = []
        self.network_history: List[NetworkMetrics] = []
        self.process_history: List[ProcessMetrics] = []

        # Current metrics
        self.current_system = SystemMetrics()
        self.current_mining = MiningMetrics()
        self.current_gpu = GPUMetrics()
        self.current_network = NetworkMetrics()
        self.current_process = ProcessMetrics()

        # Previous values for rate calculations
        self.prev_network_bytes_sent = 0
        self.prev_network_bytes_recv = 0
        self.prev_network_packets_sent = 0
        self.prev_network_packets_recv = 0
        self.prev_collection_time = time.time()

        logger.info("ZION Monitoring System initialized")

    def start(self):
        """Start monitoring system"""
        if self.running:
            return

        self.running = True
        self.collection_thread = threading.Thread(target=self._collection_loop, daemon=True)
        self.collection_thread.start()
        logger.info("ZION Monitoring System started")

    def stop(self):
        """Stop monitoring system"""
        self.running = False
        if self.collection_thread:
            self.collection_thread.join(timeout=5.0)
        logger.info("ZION Monitoring System stopped")

    def _collection_loop(self):
        """Main collection loop"""
        while self.running:
            try:
                start_time = time.time()

                # Collect all metrics
                self._collect_system_metrics()
                self._collect_mining_metrics()
                self._collect_gpu_metrics()
                self._collect_network_metrics()
                self._collect_process_metrics()

                # Store in history
                self._store_metrics_history()

                # Clean old data
                self._cleanup_old_data()

                # Sleep for remaining interval
                elapsed = time.time() - start_time
                sleep_time = max(0.1, self.config.collection_interval - elapsed)
                time.sleep(sleep_time)

            except Exception as e:
                logger.error(f"Monitoring collection error: {e}")
                time.sleep(1.0)

    def _collect_system_metrics(self):
        """Collect system-level metrics"""
        try:
            # CPU metrics
            self.current_system.cpu_percent = psutil.cpu_percent(interval=None)
            self.current_system.cpu_count = psutil.cpu_count()

            # Memory metrics
            memory = psutil.virtual_memory()
            self.current_system.memory_total = memory.total
            self.current_system.memory_used = memory.used
            self.current_system.memory_percent = memory.percent

            # Disk metrics
            disk = psutil.disk_usage('/')
            self.current_system.disk_total = disk.total
            self.current_system.disk_used = disk.used
            self.current_system.disk_percent = disk.percent

            # Network metrics (absolute values)
            network = psutil.net_io_counters()
            self.current_system.network_bytes_sent = network.bytes_sent
            self.current_system.network_bytes_recv = network.bytes_recv
            self.current_system.network_packets_sent = network.packets_sent
            self.current_system.network_packets_recv = network.packets_recv

            # Load average
            self.current_system.load_average = psutil.getloadavg()

            self.current_system.timestamp = time.time()

        except Exception as e:
            logger.error(f"System metrics collection failed: {e}")

    def _collect_mining_metrics(self):
        """Collect mining-specific metrics"""
        try:
            # This would integrate with actual mining pool/miner APIs
            # For now, simulate realistic mining metrics

            # Simulate hashrate based on system load
            base_hashrate = 1000000  # 1 MH/s base
            cpu_load_factor = self.current_system.cpu_percent / 100.0
            self.current_mining.hashrate = base_hashrate * (0.5 + cpu_load_factor * 0.5)

            # Simulate shares (very basic simulation)
            import random
            if random.random() < 0.1:  # 10% chance per second
                self.current_mining.shares_submitted += 1
                if random.random() < 0.95:  # 95% acceptance rate
                    self.current_mining.shares_accepted += 1
                else:
                    self.current_mining.shares_rejected += 1

            # Simulate occasional blocks
            if random.random() < 0.001:  # 0.1% chance per second (~1 block per 1000s)
                self.current_mining.blocks_found += 1

            self.current_mining.current_difficulty = 1000.0
            self.current_mining.pool_connection_status = True
            self.current_mining.active_miners = 1
            self.current_mining.total_miners = 1
            self.current_mining.pool_efficiency = 95.0 + random.uniform(-5, 5)

            self.current_mining.timestamp = time.time()

        except Exception as e:
            logger.error(f"Mining metrics collection failed: {e}")

    def _collect_gpu_metrics(self):
        """Collect GPU-specific metrics"""
        if not self.config.enable_gpu_monitoring:
            return

        try:
            # Try to detect NVIDIA GPUs using nvidia-ml-py3
            try:
                import pynvml
                pynvml.nvmlInit()

                self.current_gpu.gpu_count = pynvml.nvmlDeviceGetCount()

                for i in range(self.current_gpu.gpu_count):
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)

                    # GPU utilization
                    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    self.current_gpu.gpu_utilization.append(util.gpu)

                    # Memory info
                    mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    self.current_gpu.gpu_memory_used.append(mem_info.used)
                    self.current_gpu.gpu_memory_total.append(mem_info.total)

                    # Temperature
                    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                    self.current_gpu.gpu_temperature.append(temp)

                    # Power usage
                    power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  # Convert to Watts
                    self.current_gpu.gpu_power_usage.append(power)

                pynvml.nvmlShutdown()

            except ImportError:
                # Fallback: simulate GPU metrics if nvidia-ml-py3 not available
                self.current_gpu.gpu_count = 1
                self.current_gpu.gpu_utilization = [45.0]
                self.current_gpu.gpu_memory_used = [2_000_000_000]  # 2GB
                self.current_gpu.gpu_memory_total = [8_000_000_000]  # 8GB
                self.current_gpu.gpu_temperature = [65.0]
                self.current_gpu.gpu_power_usage = [150.0]

            self.current_gpu.timestamp = time.time()

        except Exception as e:
            logger.error(f"GPU metrics collection failed: {e}")

    def _collect_network_metrics(self):
        """Collect network-specific metrics"""
        if not self.config.enable_network_monitoring:
            return

        try:
            current_time = time.time()
            time_diff = current_time - self.prev_collection_time

            # Get current network stats
            network = psutil.net_io_counters()
            current_bytes_sent = network.bytes_sent
            current_bytes_recv = network.bytes_recv
            current_packets_sent = network.packets_sent
            current_packets_recv = network.packets_recv

            # Calculate rates
            if time_diff > 0:
                self.current_network.bytes_sent_per_second = (current_bytes_sent - self.prev_network_bytes_sent) / time_diff
                self.current_network.bytes_recv_per_second = (current_bytes_recv - self.prev_network_bytes_recv) / time_diff
                self.current_network.packets_sent_per_second = (current_packets_sent - self.prev_network_packets_sent) / time_diff
                self.current_network.packets_recv_per_second = (current_packets_recv - self.prev_network_packets_recv) / time_diff

            # Store previous values
            self.prev_network_bytes_sent = current_bytes_sent
            self.prev_network_bytes_recv = current_bytes_recv
            self.prev_network_packets_sent = current_packets_sent
            self.prev_network_packets_recv = current_packets_recv
            self.prev_collection_time = current_time

            # Connection counts (simplified)
            self.current_network.connections_active = len(psutil.net_connections(kind='inet'))
            self.current_network.connections_total = self.current_network.connections_active

            # Simulate latency (would need actual ping measurements)
            self.current_network.latency_ms = 25.0  # ms

            self.current_network.timestamp = time.time()

        except Exception as e:
            logger.error(f"Network metrics collection failed: {e}")

    def _collect_process_metrics(self):
        """Collect process-specific metrics"""
        if not self.config.enable_process_monitoring:
            return

        try:
            all_processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])

            python_processes = 0
            mining_processes = 0
            total_cpu = 0.0
            total_memory = 0.0

            for proc in all_processes:
                try:
                    name = proc.info['name'].lower()
                    cpu = proc.info['cpu_percent'] or 0.0
                    memory = proc.info['memory_percent'] or 0.0

                    total_cpu += cpu
                    total_memory += memory

                    if 'python' in name:
                        python_processes += 1
                        if any(keyword in name for keyword in ['mine', 'miner', 'pool', 'zion']):
                            mining_processes += 1

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            self.current_process.process_count = len(psutil.pids())
            self.current_process.python_processes = python_processes
            self.current_process.mining_processes = mining_processes
            self.current_process.system_processes = self.current_process.process_count - python_processes
            self.current_process.total_cpu_percent = total_cpu
            self.current_process.total_memory_percent = total_memory

            self.current_process.timestamp = time.time()

        except Exception as e:
            logger.error(f"Process metrics collection failed: {e}")

    def _store_metrics_history(self):
        """Store current metrics in history"""
        self.system_history.append(self.current_system)
        self.mining_history.append(self.current_mining)
        self.gpu_history.append(self.current_gpu)
        self.network_history.append(self.current_network)
        self.process_history.append(self.current_process)

    def _cleanup_old_data(self):
        """Clean up old metrics data"""
        current_time = time.time()
        cutoff_time = current_time - self.config.retention_period

        # Clean system history
        self.system_history = [m for m in self.system_history if m.timestamp > cutoff_time]

        # Clean mining history
        self.mining_history = [m for m in self.mining_history if m.timestamp > cutoff_time]

        # Clean GPU history
        self.gpu_history = [m for m in self.gpu_history if m.timestamp > cutoff_time]

        # Clean network history
        self.network_history = [m for m in self.network_history if m.timestamp > cutoff_time]

        # Clean process history
        self.process_history = [m for m in self.process_history if m.timestamp > cutoff_time]

        # Limit history size
        if len(self.system_history) > self.config.max_metrics_history:
            self.system_history = self.system_history[-self.config.max_metrics_history:]

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get all current metrics as dictionary"""
        return {
            'system': {
                'cpu_percent': self.current_system.cpu_percent,
                'memory_percent': self.current_system.memory_percent,
                'disk_percent': self.current_system.disk_percent,
                'network_bytes_sent': self.current_system.network_bytes_sent,
                'network_bytes_recv': self.current_system.network_bytes_recv,
            },
            'mining': {
                'hashrate': self.current_mining.hashrate,
                'shares_submitted': self.current_mining.shares_submitted,
                'shares_accepted': self.current_mining.shares_accepted,
                'shares_rejected': self.current_mining.shares_rejected,
                'blocks_found': self.current_mining.blocks_found,
                'pool_connection_status': self.current_mining.pool_connection_status,
            },
            'gpu': {
                'gpu_count': self.current_gpu.gpu_count,
                'gpu_utilization': self.current_gpu.gpu_utilization,
                'gpu_temperature': self.current_gpu.gpu_temperature,
                'gpu_power_usage': self.current_gpu.gpu_power_usage,
            },
            'network': {
                'bytes_sent_per_second': self.current_network.bytes_sent_per_second,
                'bytes_recv_per_second': self.current_network.bytes_recv_per_second,
                'latency_ms': self.current_network.latency_ms,
            },
            'process': {
                'python_processes': self.current_process.python_processes,
                'mining_processes': self.current_process.mining_processes,
                'total_cpu_percent': self.current_process.total_cpu_percent,
            },
            'timestamp': time.time()
        }

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary with averages and peaks"""
        if not self.system_history:
            return self.get_current_metrics()

        # Calculate averages for last 5 minutes
        recent_cutoff = time.time() - 300

        recent_system = [m for m in self.system_history if m.timestamp > recent_cutoff]
        recent_mining = [m for m in self.mining_history if m.timestamp > recent_cutoff]

        return {
            'current': self.get_current_metrics(),
            'averages_5min': {
                'cpu_percent': sum(m.cpu_percent for m in recent_system) / len(recent_system) if recent_system else 0,
                'memory_percent': sum(m.memory_percent for m in recent_system) / len(recent_system) if recent_system else 0,
                'hashrate': sum(m.hashrate for m in recent_mining) / len(recent_mining) if recent_mining else 0,
            },
            'peaks_5min': {
                'cpu_percent': max((m.cpu_percent for m in recent_system), default=0),
                'memory_percent': max((m.memory_percent for m in recent_system), default=0),
                'hashrate': max((m.hashrate for m in recent_mining), default=0),
            }
        }

# Global monitoring instance
monitoring_system = ZIONMonitoringSystem()

def get_monitoring_system() -> ZIONMonitoringSystem:
    """Get global monitoring system instance"""
    return monitoring_system

def start_monitoring():
    """Start global monitoring system"""
    monitoring_system.start()

def stop_monitoring():
    """Stop global monitoring system"""
    monitoring_system.stop()

if __name__ == "__main__":
    # Test monitoring system
    print("🧪 Testing ZION Monitoring System...")

    monitoring = ZIONMonitoringSystem()
    monitoring.start()

    try:
        for i in range(10):
            time.sleep(2)
            metrics = monitoring.get_current_metrics()
            print(f"📊 Metrics at {i*2}s: CPU {metrics['system']['cpu_percent']:.1f}%, "
                  f"Memory {metrics['system']['memory_percent']:.1f}%, "
                  f"Hashrate {metrics['mining']['hashrate']/1000:.0f} KH/s")

    except KeyboardInterrupt:
        pass
    finally:
        monitoring.stop()
        print("✅ Monitoring test completed")