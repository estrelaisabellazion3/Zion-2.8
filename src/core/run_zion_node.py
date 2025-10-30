#!/usr/bin/env python3
"""
ZION Production Node Launcher
Jednoduchý launcher bez složitých importů
"""

import os
import sys

# Nastavení PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Spuštění standalone RPC serveru
os.chdir(current_dir)
os.execv(sys.executable, [sys.executable, os.path.join(current_dir, 'standalone_rpc_server.py')] + sys.argv[1:])
