"""
ZION Blockchain v2.8 "Ad Astra Per Estrella" - Python-Native Multi-Chain Ecosystem

A high-performance blockchain implementation with integrated mining,
multi-chain bridges, Stratum protocol, and consciousness-aligned gaming.
"""

__version__ = "2.8.0"
__author__ = "Maitreya ZionNet"
__email__ = "maitreya@zionnet.org"

# Core components
from zion.core.blockchain import ZionBlockchain
from zion.mining.randomx_engine import RandomXEngine
from zion.rpc.server import ZionRPCServer

# Version compatibility check
import sys
if sys.version_info < (3, 9):
    raise RuntimeError("ZION requires Python 3.9 or later")

__all__ = [
    "ZionBlockchain",
    "RandomXEngine", 
    "ZionRPCServer",
    "__version__",
]