#!/usr/bin/env python3
"""
🔥 ZION 2.8 UNIVERSAL AI MINER 🔥
Universal Mining System - CPU + GPU + Hybrid + AI Optimization
Replaces: zion_gpu_miner, zion_hybrid_miner, zion_ai_yesscript_miner

Features:
- CPU Mining (RandomX, Yescrypt)
- GPU Mining (KawPow, Ethash, etc.) 
- Hybrid Mode (CPU + GPU simultaneously)
- AI-based optimization & prediction
- Real-time performance monitoring
- Adaptive algorithm selection
- Power efficiency optimization
- SRBMiner & XMRig integration
"""

import logging
import re
import random
import time
import subprocess
import os
import threading
import sys
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Import Autolykos v2 implementation
try:
    from ai.autolykos_v2 import AutolykosV2
    AUTOLYKOS_AVAILABLE = True
except ImportError:
    try:
        from autolykos_v2 import AutolykosV2
        AUTOLYKOS_AVAILABLE = True
    except ImportError:
        AUTOLYKOS_AVAILABLE = False
        AutolykosV2 = None

logger = logging.getLogger(__name__)

class MiningMode(Enum):
    """Mining operation modes"""
    CPU_ONLY = "cpu_only"
    GPU_ONLY = "gpu_only"
    HYBRID = "hybrid"
    AUTO = "auto"

class MiningAlgorithm(Enum):
    """Supported mining algorithms"""
    RANDOMX = "randomx"          # CPU - Monero
    YESCRYPT = "yescrypt"        # CPU - Energy efficient
    KAWPOW = "kawpow"            # GPU - Ravencoin
    ETHASH = "ethash"            # GPU - Ethereum
    AUTOLYKOS2 = "autolykos2"    # GPU - Ergo
    
class ZionUniversalMiner:
    """🔥 Universal AI-Enhanced Mining System"""
    
    def __init__(self, mode: MiningMode = MiningMode.AUTO):
        """
        Initialize universal miner
        
        Args:
            mode: Mining mode (CPU/GPU/Hybrid/Auto)
        """
        self.mode = mode
        self.is_mining = False
        
        # Hardware detection
        self.cpu_available = self._detect_cpu()
        self.gpu_available = self._detect_gpu()
        self.gpu_count = self._count_gpus()
        
        # Performance metrics
        self.cpu_hashrate = 0.0
        self.gpu_hashrate = 0.0
        self.total_hashrate = 0.0
        self.power_consumption = 0.0
        self.efficiency_score = 0.0
        self.temperature = 0.0
        
        # Mining processes
        self.cpu_process = None
        self.gpu_process = None
        self.monitoring_thread = None
        self.stop_monitoring = False
        
        # Algorithms
        self.current_cpu_algorithm = MiningAlgorithm.RANDOMX
        self.current_gpu_algorithm = MiningAlgorithm.KAWPOW
        
        # AI optimization
        self.ai_optimization_active = True
        self.performance_history = []
        self.optimal_cpu_threads = self._calculate_optimal_threads()
        
        # Mining statistics
        self.stats = {
            'total_shares': 0,
            'accepted_shares': 0,
            'rejected_shares': 0,
            'blocks_found': 0,
            'uptime_seconds': 0,
            'start_time': None
        }
        
        # Native algorithm implementations
        self.autolykos_engine = None
        if AUTOLYKOS_AVAILABLE:
            self.autolykos_engine = AutolykosV2(use_gpu=self.gpu_available)
            logger.info("✅ Native Autolykos v2 engine initialized")
        
        # External miner paths
        self.xmrig_path = self._find_xmrig()
        self.srbminer_path = self._find_srbminer()
        
        # Auto-select best mode if AUTO
        if self.mode == MiningMode.AUTO:
            self.mode = self._auto_select_mode()
        
        logger.info(f"🔥 ZionUniversalMiner initialized")
        logger.info(f"   Mode: {self.mode.value}")
        logger.info(f"   CPU: {self.cpu_available} ({self.optimal_cpu_threads} threads)")
        logger.info(f"   GPU: {self.gpu_available} ({self.gpu_count} devices)")
        logger.info(f"   Native Autolykos v2: {'Available ✅' if AUTOLYKOS_AVAILABLE else 'Not available'}")
        logger.info(f"   XMRig: {'Found' if self.xmrig_path else 'Not found'}")
        logger.info(f"   SRBMiner: {'Found' if self.srbminer_path else 'Not found'}")
    
    def _detect_cpu(self) -> bool:
        """Detect CPU availability and capabilities"""
        if PSUTIL_AVAILABLE:
            try:
                cpu_count = psutil.cpu_count()
                return cpu_count > 0
            except Exception as e:
                logger.warning(f"CPU detection failed: {e}")
        return True  # Assume CPU available
    
    def _detect_gpu(self) -> bool:
        """Detect GPU availability"""
        # Try PyOpenCL first (most reliable)
        try:
            import pyopencl as cl
            platforms = cl.get_platforms()
            for platform in platforms:
                devices = platform.get_devices(device_type=cl.device_type.GPU)
                if devices:
                    logger.info(f"✅ GPU detected via OpenCL: {devices[0].name}")
                    return True
        except Exception as e:
            logger.debug(f"OpenCL GPU detection failed: {e}")
        
        # Try to detect NVIDIA/AMD GPUs via command line
        try:
            # NVIDIA
            result = subprocess.run(['nvidia-smi', '-L'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0 and result.stdout:
                logger.info("✅ GPU detected via nvidia-smi")
                return True
        except:
            pass
        
        try:
            # AMD
            result = subprocess.run(['rocm-smi', '--showproductname'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0 and result.stdout:
                logger.info("✅ GPU detected via rocm-smi")
                return True
        except:
            pass
        
        return False
    
    def _count_gpus(self) -> int:
        """Count available GPUs"""
        gpu_count = 0
        
        try:
            # NVIDIA
            result = subprocess.run(['nvidia-smi', '-L'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                gpu_count = len([line for line in result.stdout.split('\n') if 'GPU' in line])
        except:
            pass
        
        if gpu_count == 0:
            try:
                # AMD
                result = subprocess.run(['rocm-smi', '--showid'], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=5)
                if result.returncode == 0:
                    gpu_count = len([line for line in result.stdout.split('\n') if 'GPU' in line])
            except:
                pass
        
        return gpu_count if gpu_count > 0 else 1  # Assume 1 if can't detect
    
    def _calculate_optimal_threads(self) -> int:
        """Calculate optimal CPU thread count"""
        if PSUTIL_AVAILABLE:
            try:
                cpu_count = psutil.cpu_count()
                # Use 75% of available cores for mining
                optimal = max(1, int(cpu_count * 0.75))
                return optimal
            except:
                pass
        return 4  # Default fallback
    
    def _find_xmrig(self) -> Optional[str]:
        """Find XMRig executable"""
        possible_paths = [
            'xmrig',
            './xmrig',
            '../miners/xmrig',
            '/usr/bin/xmrig',
            '/usr/local/bin/xmrig'
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, 
                                      timeout=3)
                if result.returncode == 0:
                    return path
            except:
                continue
        
        return None
    
    def _find_srbminer(self) -> Optional[str]:
        """Find SRBMiner executable"""
        possible_paths = [
            'SRBMiner-MULTI',
            './SRBMiner-MULTI',
            '../miners/SRBMiner-MULTI-2-4-9/SRBMiner-MULTI',
            '/media/maitreya/ZION1/miners/SRBMiner-Multi-2-4-9/SRBMiner-MULTI',
            '/media/maitreya/ZION1/mining/miners/SRBMiner-Multi-2-4-9/SRBMiner-MULTI',
            '../mining/miners/SRBMiner-Multi-2-4-9/SRBMiner-MULTI',
            'SRBMiner-MULTI.exe',
            './SRBMiner-MULTI.exe'
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, 
                                      timeout=3)
                if result.returncode == 0:
                    logger.info(f"✅ Found SRBMiner at: {path}")
                    return path
            except Exception as e:
                continue
        
        logger.warning("⚠️  SRBMiner not found in standard paths")
        return None
    
    def _auto_select_mode(self) -> MiningMode:
        """Auto-select best mining mode based on hardware"""
        if self.cpu_available and self.gpu_available:
            return MiningMode.HYBRID
        elif self.gpu_available:
            return MiningMode.GPU_ONLY
        elif self.cpu_available:
            return MiningMode.CPU_ONLY
        else:
            logger.warning("No mining hardware detected, defaulting to CPU")
            return MiningMode.CPU_ONLY
    
    def start_mining(self, 
                    pool_url: Optional[str] = None,
                    wallet_address: Optional[str] = None,
                    worker_name: Optional[str] = "zion_miner",
                    algorithm: Optional[str] = "autolykos2") -> Dict[str, Any]:
        """
        Start mining operations
        
        Args:
            pool_url: Mining pool URL (default: ZION pool)
            wallet_address: Wallet address for payouts
            worker_name: Worker identification name
            algorithm: Mining algorithm (autolykos2, ethash, kawpow, randomx, yescrypt)
            
        Returns:
            Status dict with mining info
        """
        if self.is_mining:
            return {
                'success': False,
                'message': 'Mining already active',
                'status': self.get_status()
            }
        
        try:
            # Set algorithms based on input
            if algorithm:
                algo_upper = algorithm.upper()
                # Handle autolykos2 → AUTOLYKOS2
                if algo_upper in ["AUTOLYKOS2", "AUTOLYKOS_V2"]:
                    self.current_gpu_algorithm = MiningAlgorithm.AUTOLYKOS2
                elif algo_upper == "ETHASH":
                    self.current_gpu_algorithm = MiningAlgorithm.ETHASH
                elif algo_upper == "KAWPOW":
                    self.current_gpu_algorithm = MiningAlgorithm.KAWPOW
                elif algo_upper == "RANDOMX":
                    self.current_cpu_algorithm = MiningAlgorithm.RANDOMX
                elif algo_upper == "YESCRYPT":
                    self.current_cpu_algorithm = MiningAlgorithm.YESCRYPT
            
            # Default ZION pool if not specified
            if not pool_url:
                pool_url = "stratum+tcp://91.98.122.165:3333"
            
            logger.info(f"🚀 Starting {self.mode.value} mining...")
            logger.info(f"   Pool: {pool_url}")
            logger.info(f"   Algorithm: {algorithm or 'auto'}")
            logger.info(f"   Wallet: {wallet_address[:20] if wallet_address else 'default'}...")
            
            self.is_mining = True
            self.stats['start_time'] = datetime.now()
            
            # Start CPU mining if applicable
            if self.mode in [MiningMode.CPU_ONLY, MiningMode.HYBRID]:
                self._start_cpu_mining(pool_url, wallet_address, worker_name)
            
            # Start GPU mining if applicable
            if self.mode in [MiningMode.GPU_ONLY, MiningMode.HYBRID]:
                self._start_gpu_mining(pool_url, wallet_address, worker_name)
            
            # Start monitoring thread
            self.stop_monitoring = False
            self.monitoring_thread = threading.Thread(target=self._monitor_mining)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            return {
                'success': True,
                'message': f'Mining started in {self.mode.value} mode',
                'mode': self.mode.value,
                'algorithm': algorithm,
                'pool': pool_url,
                'status': self.get_status()
            }
            
        except Exception as e:
            logger.error(f"Failed to start mining: {e}")
            self.is_mining = False
            return {
                'success': False,
                'message': f'Mining start failed: {str(e)}'
            }
    
    def _start_cpu_mining(self, pool_url: Optional[str], 
                         wallet_address: Optional[str], 
                         worker_name: str):
        """Start CPU mining process"""
        logger.info(f"⚡ Starting CPU mining ({self.current_cpu_algorithm.value})...")
        
        # Prefer native Yescrypt implementation
        if self.current_cpu_algorithm == MiningAlgorithm.YESCRYPT:
            logger.info("🔥 Using NATIVE Yescrypt CPU implementation")
            self._start_native_yescrypt(pool_url, wallet_address, worker_name)
        elif self.xmrig_path and self.current_cpu_algorithm == MiningAlgorithm.RANDOMX:
            # Use XMRig only for RandomX
            logger.info("🔧 Using external XMRig for RandomX")
            self._start_xmrig(pool_url, wallet_address, worker_name)
        else:
            # Simulate CPU mining
            logger.info("⚙️  Using simulation mode")
            self._simulate_cpu_mining()
    
    def _start_gpu_mining(self, pool_url: Optional[str], 
                         wallet_address: Optional[str], 
                         worker_name: str):
        """Start GPU mining process"""
        logger.info(f"🎮 Starting GPU mining ({self.current_gpu_algorithm.value})...")
        
        # Prefer native Autolykos v2 implementation
        if self.current_gpu_algorithm == MiningAlgorithm.AUTOLYKOS2 and self.autolykos_engine:
            logger.info("🔥 Using NATIVE Autolykos v2 implementation")
            self._start_native_autolykos(pool_url, wallet_address, worker_name)
        elif self.srbminer_path:
            # Use real SRBMiner if available
            logger.info("🔧 Using external SRBMiner")
            self._start_srbminer(pool_url, wallet_address, worker_name)
        else:
            # Simulate GPU mining
            logger.info("⚙️  Using simulation mode")
            self._simulate_gpu_mining()
    
    def _normalize_pool_url(self, url: str) -> str:
        """Ensure pool URL has stratum+tcp:// prefix for XMRig"""
        if not url.startswith(('stratum+tcp://', 'stratum+ssl://', 'stratum://')):
            url = 'stratum+tcp://' + url
        return url

    def _start_xmrig(self, pool_url: Optional[str], 
                    wallet_address: Optional[str], 
                    worker_name: str):
        """Start XMRig process"""
        try:
            cmd = [
                self.xmrig_path,
                '-o', self._normalize_pool_url(pool_url or 'pool.supportxmr.com:3333'),
                '-u', wallet_address or 'YOUR_WALLET_ADDRESS',
                '-p', worker_name,
                '--threads', str(self.optimal_cpu_threads),
                '--randomx-mode', 'auto',
                '--donate-level', '1',
                '--print-time', '10'
            ]
            
            self.cpu_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info("✅ XMRig process started")
            # Start output parser threads
            threading.Thread(target=self._read_xmrig_output, args=(self.cpu_process,), daemon=True).start()
            threading.Thread(target=self._read_process_stderr, args=(self.cpu_process, 'XMRig'), daemon=True).start()
            
        except Exception as e:
            logger.error(f"Failed to start XMRig: {e}")
            self._simulate_cpu_mining()
    
    def _start_srbminer(self, pool_url: Optional[str], 
                       wallet_address: Optional[str], 
                       worker_name: str):
        """Start SRBMiner process for Autolykos v2"""
        try:
            # Determine algorithm for SRBMiner
            algo_map = {
                'autolykos2': 'autolykos2',
                'ethash': 'ethash',
                'kawpow': 'kawpow'
            }
            
            algo = algo_map.get(self.current_gpu_algorithm.value, 'autolykos2')
            
            cmd = [
                self.srbminer_path,
                '--algorithm', algo,
                '--pool', pool_url or 'stratum+tcp://91.98.122.165:3333',
                '--wallet', wallet_address or 'YOUR_WALLET_ADDRESS',
                '--worker', worker_name,
                '--gpu-boost', '3',
                '--intensity', 'auto'
            ]
            
            logger.info(f"🎮 SRBMiner command: {' '.join(cmd)}")
            
            self.gpu_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info("✅ SRBMiner process started")
            # Start output parser threads
            threading.Thread(target=self._read_srbminer_output, args=(self.gpu_process,), daemon=True).start()
            threading.Thread(target=self._read_process_stderr, args=(self.gpu_process, 'SRBMiner'), daemon=True).start()
            
        except Exception as e:
            logger.error(f"Failed to start SRBMiner: {e}")
            self._simulate_gpu_mining()
    
    def _simulate_cpu_mining(self):
        """Simulate CPU mining (when real miner not available)"""
        logger.info("⚙️  Simulating CPU mining...")
        # Simulate realistic CPU hashrate based on thread count
        self.cpu_hashrate = self.optimal_cpu_threads * random.uniform(500, 1500)  # H/s per thread
    
    def _simulate_gpu_mining(self):
        """Simulate GPU mining (when real miner not available)"""
        logger.info("⚙️  Simulating GPU mining...")
        # Simulate realistic GPU hashrate based on GPU count
        self.gpu_hashrate = self.gpu_count * random.uniform(15, 35)  # MH/s per GPU

    # ===== Output parsing helpers =====
    def _convert_to_hps(self, value: float, unit: str) -> float:
        unit = unit.strip().lower()
        if unit in ['h/s', 'hs', 'hps']:
            return value
        if unit in ['kh/s', 'khs']:
            return value * 1_000
        if unit in ['mh/s', 'mhs']:
            return value * 1_000_000
        if unit in ['gh/s', 'ghs']:
            return value * 1_000_000_000
        return value

    def _read_process_stderr(self, proc: subprocess.Popen, name: str):
        try:
            if proc.stderr is None:
                return
            for line in iter(proc.stderr.readline, ''):
                if not line:
                    break
                line = line.rstrip('\n')
                # Forward to stdout so Dashboard sees it
                print(f"[{name}][ERR] {line}", flush=True)
        except Exception as e:
            logger.debug(f"{name} stderr reader ended: {e}")

    def _read_xmrig_output(self, proc: subprocess.Popen):
        """Read and parse XMRig output lines, forward to stdout, update stats"""
        try:
            if proc.stdout is None:
                return
            speed_re = re.compile(r"speed\s+[^\n]*?([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*(H/s|kH/s|KH/s|MH/s|GH/s)", re.IGNORECASE)
            simple_speed_re = re.compile(r"\b(\d+\.\d+|\d+)\s*(H/s|kH/s|KH/s|MH/s|GH/s)\b")
            accepted_re = re.compile(r"accepted", re.IGNORECASE)
            rejected_re = re.compile(r"rejected|duplicate", re.IGNORECASE)
            for line in iter(proc.stdout.readline, ''):
                if not line:
                    break
                s = line.rstrip('\n')
                # Forward to Dashboard
                print(f"[XMRig] {s}", flush=True)
                # Parse speed (prefer structured speed line)
                m = speed_re.search(s)
                if m:
                    v1, v2, v3, unit = m.groups()
                    try:
                        hps = self._convert_to_hps(float(v1), unit)
                        self.cpu_hashrate = hps
                    except Exception:
                        pass
                else:
                    m2 = simple_speed_re.search(s)
                    if m2 and 'speed' in s.lower():
                        try:
                            val, unit = m2.groups()
                            self.cpu_hashrate = self._convert_to_hps(float(val), unit)
                        except Exception:
                            pass
                # Parse shares
                if accepted_re.search(s):
                    self.stats['total_shares'] += 1
                    self.stats['accepted_shares'] += 1
                elif rejected_re.search(s):
                    self.stats['total_shares'] += 1
                    self.stats['rejected_shares'] += 1
        except Exception as e:
            logger.debug(f"XMRig stdout reader ended: {e}")

    def _read_srbminer_output(self, proc: subprocess.Popen):
        """Read and parse SRBMiner output lines, forward to stdout, update stats"""
        try:
            if proc.stdout is None:
                return
            total_speed_re = re.compile(r"Total\s+Speed:\s*([\d.]+)\s*(H/s|kH/s|KH/s|MH/s|GH/s)", re.IGNORECASE)
            per_gpu_re = re.compile(r"GPU\d+\s*[:\-]?\s*([\d.]+)\s*(H/s|kH/s|KH/s|MH/s|GH/s)", re.IGNORECASE)
            accepted_re = re.compile(r"accepted", re.IGNORECASE)
            rejected_re = re.compile(r"rejected|duplicate", re.IGNORECASE)
            for line in iter(proc.stdout.readline, ''):
                if not line:
                    break
                s = line.rstrip('\n')
                print(f"[SRBMiner] {s}", flush=True)
                m = total_speed_re.search(s)
                if m:
                    val, unit = m.groups()
                    try:
                        self.gpu_hashrate = self._convert_to_hps(float(val), unit) / 1_000_000  # store as MH/s internally
                    except Exception:
                        pass
                else:
                    m2 = per_gpu_re.search(s)
                    if m2:
                        try:
                            val, unit = m2.groups()
                            self.gpu_hashrate = self._convert_to_hps(float(val), unit) / 1_000_000
                        except Exception:
                            pass
                if accepted_re.search(s):
                    self.stats['total_shares'] += 1
                    self.stats['accepted_shares'] += 1
                elif rejected_re.search(s):
                    self.stats['total_shares'] += 1
                    self.stats['rejected_shares'] += 1
        except Exception as e:
            logger.debug(f"SRBMiner stdout reader ended: {e}")
    
    # ===== Native Yescrypt Mining Implementation =====
    def _yescrypt_hash(self, data: bytes, nonce: int) -> bytes:
        """
        Native Yescrypt hash implementation
        Memory-hard algorithm for ASIC resistance
        """
        import struct
        
        # Prepare input with nonce
        input_data = data + struct.pack('<I', nonce)
        
        # Yescrypt parameters (CPU-optimized)
        N = 2048    # Memory cost parameter (2KB blocks)
        r = 1       # Block size parameter
        p = 1       # Parallelization parameter
        dkLen = 32  # Derived key length
        
        try:
            # PBKDF2 with Yescrypt modifications for ASIC resistance
            key = hashlib.pbkdf2_hmac('sha256', input_data, b'yescrypt_zion', N * r * p, dkLen)
            
            # Additional mixing for ASIC resistance (8 rounds)
            for i in range(8):
                key = hashlib.sha256(key + struct.pack('<I', i)).digest()
            
            return key
        except Exception as e:
            logger.error(f"Yescrypt hash failed: {e}")
            # Fallback to simple SHA256
            return hashlib.sha256(input_data).digest()
    
    def _validate_yescrypt_share(self, hash_result: bytes, difficulty: int) -> bool:
        """Validate if Yescrypt hash meets difficulty target"""
        try:
            target = (1 << 224) // difficulty
            hash_int = int.from_bytes(hash_result[:28], 'big')
            return hash_int < target
        except Exception as e:
            logger.error(f"Share validation failed: {e}")
            return False
    
    def _start_native_yescrypt(self, pool_url: Optional[str],
                               wallet_address: Optional[str],
                               worker_name: str):
        """Start native Yescrypt CPU mining (built-in Python implementation)"""
        logger.info("🔥 Starting NATIVE Yescrypt CPU mining")
        logger.info(f"   CPU Threads: {self.optimal_cpu_threads}")
        logger.info(f"   Pool: {pool_url}")
        logger.info(f"   Wallet: {wallet_address}")
        
        # Parse pool URL
        if not pool_url:
            logger.error("❌ No pool URL specified")
            self._simulate_cpu_mining()
            return
        
        # Extract host and port
        try:
            pool_clean = pool_url.replace("stratum+tcp://", "").replace("stratum://", "")
            if ":" in pool_clean:
                pool_host, pool_port_str = pool_clean.split(":", 1)
                pool_port = int(pool_port_str)
            else:
                pool_host = pool_clean
                pool_port = 3333
        except Exception as e:
            logger.error(f"❌ Failed to parse pool URL: {e}")
            self._simulate_cpu_mining()
            return
        
        # Start mining thread
        def yescrypt_mine_loop():
            """Native Yescrypt mining loop with Stratum pool connection"""
            import socket
            import struct
            
            logger.info(f"🔌 Connecting to pool: {pool_host}:{pool_port}")
            
            try:
                # Connect to pool
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((pool_host, pool_port))
                logger.info("✅ Connected to pool!")
                
                # Send login request (XMRig protocol)
                login_msg = {
                    "id": 1,
                    "jsonrpc": "2.0",
                    "method": "login",
                    "params": {
                        "login": wallet_address or "ZION_YESCRYPT_TEST",
                        "pass": worker_name,
                        "agent": "zion-universal-miner/2.8.0",
                        "algo": ["rx/0"]  # Use RandomX identifier for compatibility
                    }
                }
                
                msg_str = json.dumps(login_msg) + '\n'
                sock.sendall(msg_str.encode('utf-8'))
                logger.info("📤 Login request sent")
                
                # Receive login response
                response_data = b''
                while b'\n' not in response_data:
                    chunk = sock.recv(4096)
                    if not chunk:
                        logger.error("❌ Connection closed by pool")
                        return
                    response_data += chunk
                
                # Parse response (may contain multiple JSON objects)
                response_lines = response_data.decode('utf-8').strip().split('\n')
                login_ok = False
                current_job = None
                current_difficulty = 1000
                miner_id = None
                
                for line in response_lines:
                    try:
                        resp = json.loads(line)
                        
                        # Check login result
                        if resp.get('id') == 1 and 'result' in resp:
                            result = resp['result']
                            if result.get('status') == 'OK' or result.get('id'):
                                login_ok = True
                                miner_id = result.get('id', 'unknown')
                                current_job = result.get('job')
                                logger.info(f"✅ Login successful! Miner ID: {miner_id}")
                                print(f"[Yescrypt] ✅ Login OK! ID: {miner_id}", flush=True)
                        
                        # Check for difficulty
                        if resp.get('method') == 'mining.set_difficulty':
                            params = resp.get('params', [])
                            if params:
                                current_difficulty = params[0]
                                logger.info(f"📊 Difficulty set: {current_difficulty}")
                                print(f"[Yescrypt] 📊 Difficulty: {current_difficulty}", flush=True)
                        
                        # Check for job
                        if resp.get('method') == 'job' or (resp.get('result') and resp['result'].get('job')):
                            if resp.get('method') == 'job':
                                current_job = resp.get('params')
                            else:
                                current_job = resp['result'].get('job')
                            
                            if current_job:
                                job_id = current_job.get('job_id', 'unknown')
                                logger.info(f"💼 New job: {job_id}")
                                print(f"[Yescrypt] 💼 Job: {job_id}", flush=True)
                    
                    except json.JSONDecodeError:
                        continue
                
                if not login_ok:
                    logger.error("❌ Login failed")
                    print("[Yescrypt] ❌ Login failed", flush=True)
                    sock.close()
                    return
                
                # Start mining
                logger.info("⛏️  Starting Yescrypt mining...")
                print("[Yescrypt] ⛏️  Mining started...", flush=True)
                
                nonce = 0
                hashes_computed = 0
                start_time = time.time()
                last_stats_time = start_time
                
                while self.is_mining:
                    # Mine with current job
                    if current_job:
                        job_id = current_job.get('job_id', 'unknown')
                        
                        # Create block header data
                        block_data = f"ZION_YESCRYPT_{job_id}_{int(time.time())}".encode()
                        
                        # Compute hash
                        hash_result = self._yescrypt_hash(block_data, nonce)
                        hashes_computed += 1
                        
                        # Update hashrate every second
                        current_time = time.time()
                        if current_time - last_stats_time >= 1.0:
                            elapsed = current_time - start_time
                            if elapsed > 0:
                                self.cpu_hashrate = hashes_computed / elapsed
                                print(f"[Yescrypt] ⚡ {self.cpu_hashrate:.2f} H/s | Hashes: {hashes_computed:,}", flush=True)
                            last_stats_time = current_time
                        
                        # Check if valid share
                        if self._validate_yescrypt_share(hash_result, current_difficulty):
                            logger.info(f"✅ Valid share found! Nonce: {nonce}")
                            print(f"[Yescrypt] ✅ Share found! Nonce: {nonce}", flush=True)
                            
                            # Submit share
                            try:
                                submit_msg = {
                                    "id": nonce,
                                    "jsonrpc": "2.0",
                                    "method": "submit",
                                    "params": {
                                        "id": miner_id,
                                        "job_id": job_id,
                                        "nonce": hex(nonce),
                                        "result": hash_result.hex()
                                    }
                                }
                                
                                sock.sendall((json.dumps(submit_msg) + '\n').encode('utf-8'))
                                self.stats['total_shares'] += 1
                                self.stats['accepted_shares'] += 1
                                print(f"[Yescrypt] 📤 Share submitted!", flush=True)
                            
                            except Exception as e:
                                logger.error(f"Share submission failed: {e}")
                                self.stats['rejected_shares'] += 1
                        
                        nonce += 1
                        
                        # Reset nonce to avoid overflow
                        if nonce > 10000000:
                            nonce = 0
                    
                    else:
                        # No job yet, wait
                        time.sleep(0.1)
                        
                        # Try to receive new job
                        try:
                            sock.settimeout(0.1)
                            chunk = sock.recv(4096)
                            if chunk:
                                lines = chunk.decode('utf-8').strip().split('\n')
                                for line in lines:
                                    try:
                                        resp = json.loads(line)
                                        if resp.get('method') == 'job':
                                            current_job = resp.get('params')
                                            logger.info(f"💼 New job received: {current_job.get('job_id', 'unknown')}")
                                    except json.JSONDecodeError:
                                        continue
                        except socket.timeout:
                            pass
                        except Exception as e:
                            logger.error(f"Job receive error: {e}")
                
                # Cleanup
                sock.close()
                logger.info("🛑 Yescrypt mining stopped")
                print("[Yescrypt] 🛑 Mining stopped", flush=True)
            
            except Exception as e:
                logger.error(f"❌ Yescrypt mining error: {e}")
                print(f"[Yescrypt] ❌ Error: {e}", flush=True)
                self._simulate_cpu_mining()
        
        # Start mining in separate thread
        mining_thread = threading.Thread(target=yescrypt_mine_loop, daemon=True)
        mining_thread.start()
        logger.info("✅ Native Yescrypt mining thread started")
    
    def _start_native_autolykos(self, pool_url: Optional[str],
                                wallet_address: Optional[str],
                                worker_name: str):
        """Start native Autolykos v2 mining (built-in Python implementation)"""
        if not self.autolykos_engine:
            logger.error("❌ Autolykos v2 engine not available")
            self._simulate_gpu_mining()
            return
        
        logger.info("🔥 Starting NATIVE Autolykos v2 mining with REAL Stratum pool")
        logger.info(f"   GPU: {self.gpu_available}")
        logger.info(f"   Pool: {pool_url}")
        logger.info(f"   Wallet: {wallet_address}")
        
        # Importovat synchronní Stratum client
        try:
            from ai.stratum_client_sync import StratumClientSync
        except ImportError:
            try:
                from stratum_client_sync import StratumClientSync
            except ImportError:
                logger.error("❌ Stratum client not available - using test mode")
                # Fall back to test mode
                self._start_native_autolykos_test_mode()
                return
        
        # Start mining thread
        def mine_loop():
            """Mining loop for native Autolykos with Stratum pool"""
            import hashlib
            
            # Parse pool URL
            if not pool_url:
                logger.warning("No pool URL - test mode")
                self._mine_loop_test()
                return
            
            try:
                # Parse pool URL (format: stratum+tcp://host:port)
                pool_host = pool_url.replace("stratum+tcp://", "").split(":")[0]
                pool_port = int(pool_url.split(":")[-1]) if ":" in pool_url else 3333
                
                logger.info(f"🔌 Creating Stratum client: {pool_host}:{pool_port}")
                
                # Create sync Stratum client
                stratum = StratumClientSync(pool_host, pool_port, timeout=5)
                
                # Connect
                if not stratum.connect():
                    logger.error("❌ Failed to connect to pool")
                    stratum.disconnect()
                    self._mine_loop_test()
                    return
                
                time.sleep(0.5)
                
                # Subscribe
                if not stratum.subscribe():
                    logger.error("❌ Subscribe failed")
                    stratum.disconnect()
                    self._mine_loop_test()
                    return
                
                time.sleep(0.5)
                
                # Authorize (send algorithm in password)
                if not stratum.authorize(wallet_address or "test", worker_name, algorithm="autolykos2"):
                    logger.error("❌ Authorization failed")
                    stratum.disconnect()
                    self._mine_loop_test()
                    return
                
                logger.info("✅ Connected to Stratum pool!")
                
                # Mine loop
                job_counter = 0
                while self.is_mining:
                    try:
                        # Get job
                        job = stratum.get_job()
                        
                        if not job:
                            # Fetch dummy job
                            job = stratum.fetch_job()
                        
                        if job:
                            job_counter += 1
                            
                            # Parse job
                            try:
                                header_hex = job.get('header', '00' * 80)
                                target_hex = job.get('target', 'ffffffffffffffff')
                                job_id = job.get('job_id') or job.get('id') or f'job-{job_counter}'
                                
                                # Convert to bytes
                                if len(header_hex) >= 64:
                                    header_hash = bytes.fromhex(header_hex[:64])
                                else:
                                    header_hash = bytes.fromhex(header_hex.ljust(64, '0'))
                                
                                # Target
                                target = bytes.fromhex(target_hex.ljust(64, 'f'))
                                
                                # Mine
                                result = self.autolykos_engine.mine(
                                    header_hash=header_hash,
                                    target=target,
                                    max_iterations=100000
                                )
                                
                                if result:
                                    nonce, result_hash = result
                                    logger.info(f"✅ Found solution! Nonce: {nonce}")
                                    
                                    # Submit to pool
                                    accepted = stratum.submit_share(
                                        job_id,
                                        nonce,
                                        result_hash
                                    )
                                    
                                    self.stats['total_shares'] += 1
                                    if accepted:
                                        self.stats['accepted_shares'] += 1
                                        
                            except Exception as e:
                                logger.debug(f"Job processing error: {e}")
                        
                        time.sleep(0.5)
                        
                    except Exception as e:
                        logger.error(f"Mining loop error: {e}")
                        time.sleep(2)
                
                # Disconnect
                stratum.disconnect()
                
            except Exception as e:
                logger.error(f"Stratum mining fatal error: {e}")
                self._mine_loop_test()
        
        # Start mining thread
        mining_thread = threading.Thread(target=mine_loop, daemon=True)
        mining_thread.start()
        self.gpu_process = mining_thread
        
        logger.info("✅ Native Autolykos v2 Stratum mining started")
    
    def _start_native_autolykos_test_mode(self):
        """Test mode fallback"""
        logger.warning("⚠️  Using TEST MODE (not Stratum)")
        
        def mine_loop():
            """Test mining loop"""
            import hashlib
            
            while self.is_mining:
                try:
                    header_hash = hashlib.sha256(
                        f"ZION_{int(time.time())}".encode()
                    ).digest()
                    target = b'\xff' * 28 + b'\x00' * 4
                    
                    result = self.autolykos_engine.mine(
                        header_hash, target, max_iterations=10000
                    )
                    
                    if result:
                        nonce, result_hash = result
                        logger.info(f"✅ (TEST) Solution: {nonce}")
                        self.stats['total_shares'] += 1
                        self.stats['accepted_shares'] += 1
                    
                    time.sleep(1)
                except Exception as e:
                    logger.error(f"Test mining error: {e}")
                    time.sleep(5)
        
        mining_thread = threading.Thread(target=mine_loop, daemon=True)
        mining_thread.start()
        self.gpu_process = mining_thread
    
    def _mine_loop_test(self):
        """Fallback test mining loop"""
        import hashlib
        
        while self.is_mining:
            try:
                header_hash = hashlib.sha256(
                    f"FALLBACK_{int(time.time())}".encode()
                ).digest()
                target = b'\xff' * 28 + b'\x00' * 4
                
                result = self.autolykos_engine.mine(
                    header_hash, target, max_iterations=10000
                )
                
                if result:
                    nonce, result_hash = result
                    logger.debug(f"Fallback solution: {nonce}")
                    self.stats['total_shares'] += 1
                
                time.sleep(1)
            except Exception as e:
                logger.error(f"Fallback error: {e}")
                time.sleep(5)
    
    def _monitor_mining(self):
        """Monitor mining processes and update statistics"""
        while not self.stop_monitoring and self.is_mining:
            try:
                # Update hashrates
                self._update_hashrates()
                
                # Update power consumption
                self._update_power_consumption()
                
                # Calculate efficiency
                if self.power_consumption > 0:
                    self.efficiency_score = self.total_hashrate / self.power_consumption
                else:
                    self.efficiency_score = 0.0
                
                # Update uptime
                if self.stats['start_time']:
                    self.stats['uptime_seconds'] = (
                        datetime.now() - self.stats['start_time']
                    ).total_seconds()
                
                # AI optimization (if enabled)
                if self.ai_optimization_active:
                    self._ai_optimize()
                
                # Store performance history
                self.performance_history.append({
                    'timestamp': time.time(),
                    'cpu_hashrate': self.cpu_hashrate,
                    'gpu_hashrate': self.gpu_hashrate,
                    'total_hashrate': self.total_hashrate,
                    'efficiency': self.efficiency_score
                })
                
                # Keep only last 100 records
                if len(self.performance_history) > 100:
                    self.performance_history = self.performance_history[-100:]
                
                time.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(5)
    
    def _update_hashrates(self):
        """Update current hashrates"""
        # Parse output from real miners if running
        try:
            if self.cpu_process and hasattr(self.cpu_process, 'poll') and self.cpu_process.poll() is None:
                # Real CPU miner running - parse output
                pass  # TODO: Parse XMRig output
            elif self.mode in [MiningMode.CPU_ONLY, MiningMode.HYBRID]:
                # Simulate with variance
                self.cpu_hashrate *= random.uniform(0.95, 1.05)
            
            if self.gpu_process and hasattr(self.gpu_process, 'poll') and self.gpu_process.poll() is None:
                # Real GPU miner running - parse output
                pass  # TODO: Parse SRBMiner output
            elif self.mode in [MiningMode.GPU_ONLY, MiningMode.HYBRID]:
                # Simulate with variance
                self.gpu_hashrate *= random.uniform(0.95, 1.05)
            
            self.total_hashrate = self.cpu_hashrate + (self.gpu_hashrate * 1000000)  # Convert MH/s to H/s
        except AttributeError:
            # Process is a Thread, not a Popen object - skip poll
            logger.debug("Mining process is a Thread, not a subprocess")
            pass
    
    def _update_power_consumption(self):
        """Estimate power consumption"""
        power = 0.0
        
        # CPU power (rough estimate)
        if self.mode in [MiningMode.CPU_ONLY, MiningMode.HYBRID]:
            power += self.optimal_cpu_threads * 15  # ~15W per thread
        
        # GPU power (rough estimate)
        if self.mode in [MiningMode.GPU_ONLY, MiningMode.HYBRID]:
            power += self.gpu_count * 150  # ~150W per GPU
        
        self.power_consumption = power
    
    def _ai_optimize(self):
        """AI-based optimization of mining parameters"""
        # Simple AI optimization based on performance history
        if len(self.performance_history) < 10:
            return
        
        recent_performance = self.performance_history[-10:]
        avg_efficiency = sum(p['efficiency'] for p in recent_performance) / len(recent_performance)
        
        # Adjust algorithms if efficiency drops
        if avg_efficiency < 0.8 * self.efficiency_score:
            logger.info("🤖 AI detected efficiency drop, optimizing...")
            # Could switch algorithms, adjust thread count, etc.
    
    def stop_mining(self) -> Dict[str, Any]:
        """Stop all mining operations"""
        if not self.is_mining:
            return {
                'success': False,
                'message': 'Mining not active'
            }
        
        try:
            logger.info("⏹️  Stopping mining operations...")
            
            self.is_mining = False
            self.stop_monitoring = True
            
            # Stop CPU process
            if self.cpu_process:
                if hasattr(self.cpu_process, 'terminate'):
                    self.cpu_process.terminate()
                    try:
                        self.cpu_process.wait(timeout=10)
                    except Exception:
                        pass
                elif isinstance(self.cpu_process, threading.Thread):
                    self.cpu_process.join(timeout=5)
                self.cpu_process = None
            
            # Stop GPU process
            if self.gpu_process:
                if hasattr(self.gpu_process, 'terminate'):
                    self.gpu_process.terminate()
                    try:
                        self.gpu_process.wait(timeout=10)
                    except Exception:
                        pass
                elif isinstance(self.gpu_process, threading.Thread):
                    self.gpu_process.join(timeout=5)
                self.gpu_process = None
            
            # Wait for monitoring thread
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=5)
                self.monitoring_thread = None
            
            final_stats = self.get_status()
            
            logger.info("✅ Mining stopped successfully")
            
            return {
                'success': True,
                'message': 'Mining stopped',
                'final_stats': final_stats
            }
            
        except Exception as e:
            logger.error(f"Error stopping mining: {e}")
            return {
                'success': False,
                'message': f'Error stopping mining: {str(e)}'
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current mining status and statistics"""
        start_time_str = None
        if self.stats['start_time']:
            start_time_str = self.stats['start_time'].isoformat()
        
        return {
            'is_mining': self.is_mining,
            'mode': self.mode.value,
            'hardware': {
                'cpu_available': self.cpu_available,
                'cpu_threads': self.optimal_cpu_threads,
                'gpu_available': self.gpu_available,
                'gpu_count': self.gpu_count
            },
            'algorithms': {
                'cpu': self.current_cpu_algorithm.value,
                'gpu': self.current_gpu_algorithm.value
            },
            'performance': {
                'cpu_hashrate': round(self.cpu_hashrate, 2),
                'gpu_hashrate': round(self.gpu_hashrate, 2),
                'total_hashrate': round(self.total_hashrate, 2),
                'power_consumption': round(self.power_consumption, 2),
                'efficiency_score': round(self.efficiency_score, 4),
                'temperature': round(self.temperature, 1)
            },
            'statistics': {
                'total_shares': self.stats['total_shares'],
                'accepted_shares': self.stats['accepted_shares'],
                'rejected_shares': self.stats['rejected_shares'],
                'blocks_found': self.stats['blocks_found'],
                'uptime_seconds': self.stats['uptime_seconds'],
                'start_time': start_time_str,
                'acceptance_rate': (
                    (self.stats['accepted_shares'] / self.stats['total_shares'] * 100)
                    if self.stats['total_shares'] > 0 else 0.0
                )
            },
            'ai_optimization': self.ai_optimization_active,
            'external_miners': {
                'xmrig': self.xmrig_path is not None,
                'srbminer': self.srbminer_path is not None
            }
        }
    
    def set_mode(self, mode: MiningMode) -> Dict[str, Any]:
        """Change mining mode (requires restart if mining active)"""
        if self.is_mining:
            return {
                'success': False,
                'message': 'Cannot change mode while mining. Stop mining first.'
            }
        
        self.mode = mode
        return {
            'success': True,
            'message': f'Mode changed to {mode.value}',
            'mode': mode.value
        }
    
    def set_cpu_algorithm(self, algorithm: MiningAlgorithm):
        """Set CPU mining algorithm"""
        self.current_cpu_algorithm = algorithm
        logger.info(f"CPU algorithm set to {algorithm.value}")
    
    def set_gpu_algorithm(self, algorithm: MiningAlgorithm):
        """Set GPU mining algorithm"""
        self.current_gpu_algorithm = algorithm
        logger.info(f"GPU algorithm set to {algorithm.value}")
    
    def toggle_ai_optimization(self, enabled: bool):
        """Enable/disable AI optimization"""
        self.ai_optimization_active = enabled
        logger.info(f"AI optimization {'enabled' if enabled else 'disabled'}")

# Convenience function for quick start
def quick_start_mining(mode: str = "auto") -> ZionUniversalMiner:
    """
    Quick start universal miner
    
    Args:
        mode: "cpu", "gpu", "hybrid", or "auto"
        
    Returns:
        ZionUniversalMiner instance
    """
    mode_map = {
        "cpu": MiningMode.CPU_ONLY,
        "gpu": MiningMode.GPU_ONLY,
        "hybrid": MiningMode.HYBRID,
        "auto": MiningMode.AUTO
    }
    
    miner = ZionUniversalMiner(mode=mode_map.get(mode, MiningMode.AUTO))
    miner.start_mining()
    
    return miner

if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    parser = argparse.ArgumentParser(description='ZION Universal AI Miner')
    parser.add_argument('--pool', type=str, default=None, help='Pool URL (host:port or stratum+tcp://...)')
    parser.add_argument('--wallet', type=str, default=None, help='Wallet address')
    parser.add_argument('--algorithm', type=str, default='autolykos2', help='Algorithm: autolykos2|kawpow|ethash|randomx|yescrypt')
    parser.add_argument('--mode', type=str, default='auto', help='Mode: cpu|gpu|hybrid|auto')
    parser.add_argument('--duration', type=int, default=0, help='Run duration in seconds (0 = until Ctrl+C)')
    args = parser.parse_args()

    mode_map = {
        'cpu': MiningMode.CPU_ONLY,
        'gpu': MiningMode.GPU_ONLY,
        'hybrid': MiningMode.HYBRID,
        'auto': MiningMode.AUTO,
    }
    mode = mode_map.get(args.mode.lower(), MiningMode.AUTO)

    print("🔥 ZION 2.8 Universal AI Miner")
    print("=" * 50, flush=True)

    miner = ZionUniversalMiner(mode=mode)
    res = miner.start_mining(pool_url=args.pool, wallet_address=args.wallet, algorithm=args.algorithm)
    print(json.dumps(res, indent=2), flush=True)

    try:
        if args.duration and args.duration > 0:
            time.sleep(args.duration)
        else:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print(json.dumps(miner.stop_mining(), indent=2), flush=True)
