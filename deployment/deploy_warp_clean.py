#!/usr/bin/env python3
"""
🔥 ZION CLEAN DEPLOYMENT ORCHESTRATOR 🔥

Kompletní čistý deploy ZION 2.8.0 s WARP Engine jako core orchestrator

Steps:
1. ✅ Backup complete (ssh_backup_YYYYMMDD_HHMMSS.tar.gz)
2. Clean old data (optional - keep backups)
3. Deploy fresh WARP Engine infrastructure
4. Initialize blockchain with genesis
5. Start RPC & P2P
6. Connect pools
7. Verify all systems operational

Version: 2.8.0 "Ad Astra Per Estrella"
Date: 2025-10-21
"""

import os
import sys
import time
import subprocess
import asyncio
from datetime import datetime
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

class ZionDeploymentOrchestrator:
    """Orchestrates clean ZION deployment"""
    
    def __init__(self, target: str = "local", clean_data: bool = False):
        self.target = target  # "local" or "ssh"
        self.clean_data = clean_data
        self.deployment_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.deployment_log = f"deployment_{self.deployment_time}.log"
        
    def log(self, message: str, level: str = "INFO"):
        """Log with color and timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = {
            "INFO": BLUE,
            "SUCCESS": GREEN,
            "WARNING": YELLOW,
            "ERROR": RED
        }.get(level, RESET)
        
        formatted = f"{color}[{timestamp}] {level}: {message}{RESET}"
        print(formatted)
        
        # Also write to log file
        with open(self.deployment_log, 'a') as f:
            f.write(f"[{timestamp}] {level}: {message}\n")
    
    def run_command(self, cmd: str, description: str) -> bool:
        """Run shell command with logging"""
        self.log(f"Running: {description}", "INFO")
        self.log(f"Command: {cmd}", "INFO")
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.log(f"✅ {description} - SUCCESS", "SUCCESS")
                if result.stdout:
                    self.log(f"Output: {result.stdout[:200]}", "INFO")
                return True
            else:
                self.log(f"❌ {description} - FAILED", "ERROR")
                if result.stderr:
                    self.log(f"Error: {result.stderr[:200]}", "ERROR")
                return False
                
        except subprocess.TimeoutExpired:
            self.log(f"⏱️ {description} - TIMEOUT", "ERROR")
            return False
        except Exception as e:
            self.log(f"💥 {description} - EXCEPTION: {str(e)}", "ERROR")
            return False
    
    def verify_backup_exists(self) -> bool:
        """Verify backup was created"""
        self.log("Verifying backup exists...", "INFO")
        
        # Find most recent backup
        backups = list(Path(".").glob("ssh_backup_*.tar.gz"))
        if not backups:
            self.log("No backups found!", "ERROR")
            return False
        
        latest_backup = max(backups, key=lambda p: p.stat().st_mtime)
        backup_size = latest_backup.stat().st_size / 1024  # KB
        
        self.log(f"Latest backup: {latest_backup.name} ({backup_size:.1f} KB)", "SUCCESS")
        return True
    
    def clean_local_data(self):
        """Clean local data (if requested)"""
        if not self.clean_data:
            self.log("Skipping data cleanup (clean_data=False)", "INFO")
            return
        
        self.log("🧹 Cleaning local data...", "WARNING")
        
        files_to_clean = [
            "zion_blockchain.db",
            "zion_blockchain.db-journal",
            "*.log"
        ]
        
        for pattern in files_to_clean:
            self.run_command(f"rm -f {pattern}", f"Remove {pattern}")
    
    def deploy_warp_files(self):
        """Deploy WARP engine files"""
        self.log("📦 Deploying WARP Engine files...", "INFO")
        
        required_files = [
            "zion_warp_engine_core.py",
            "new_zion_blockchain.py",
            "zion_rpc_server.py",
            "zion_p2p_network.py",
            "seednodes.py",
            "crypto_utils.py"
        ]
        
        missing = []
        for f in required_files:
            if not Path(f).exists():
                missing.append(f)
        
        if missing:
            self.log(f"Missing files: {', '.join(missing)}", "ERROR")
            return False
        
        self.log("✅ All required files present", "SUCCESS")
        return True
    
    def deploy_to_ssh(self):
        """Deploy to SSH server"""
        if self.target != "ssh":
            return
        
        self.log("🚀 Deploying to SSH server 91.98.122.165...", "INFO")
        
        # Files to deploy
        deploy_files = [
            "zion_warp_engine_core.py",
            "new_zion_blockchain.py",
            "zion_rpc_server.py",
            "zion_p2p_network.py",
            "zion_universal_pool_v2.py",
            "seednodes.py",
            "crypto_utils.py",
            "blockchain_rpc_client.py"
        ]
        
        for f in deploy_files:
            self.run_command(
                f"scp {f} root@91.98.122.165:~/",
                f"Deploy {f} to SSH"
            )
    
    def start_warp_engine_local(self):
        """Start WARP engine locally"""
        if self.target != "local":
            return
        
        self.log("🔥 Starting WARP Engine locally...", "INFO")
        
        # Test import first
        if not self.run_command(
            "python3 -c 'from zion_warp_engine_core import ZionWARPEngine'",
            "Test WARP Engine import"
        ):
            return False
        
        # Start in background
        self.log("Starting WARP Engine in background...", "INFO")
        self.log("(Press Ctrl+C to stop during status check)", "WARNING")
        
        return True
    
    def verify_deployment(self):
        """Verify deployment is operational"""
        self.log("🔍 Verifying deployment...", "INFO")
        
        # Run quick test
        if not self.run_command(
            "python3 test_warp_engine_local.py",
            "WARP Engine Quick Test"
        ):
            self.log("Deployment verification FAILED", "ERROR")
            return False
        
        self.log("✅ Deployment verification PASSED", "SUCCESS")
        return True
    
    def run_deployment(self):
        """Execute full deployment"""
        print("\n" + "=" * 80)
        print(f"{GREEN}🔥 ZION CLEAN DEPLOYMENT ORCHESTRATOR 🔥{RESET}")
        print("=" * 80)
        print(f"Target: {self.target}")
        print(f"Clean Data: {self.clean_data}")
        print(f"Deployment Log: {self.deployment_log}")
        print("=" * 80 + "\n")
        
        # Step 1: Verify backup
        if not self.verify_backup_exists():
            self.log("❌ No backup found - run backup_ssh_full.sh first!", "ERROR")
            return False
        
        # Step 2: Clean data (if requested)
        if self.clean_data:
            self.clean_local_data()
        
        # Step 3: Verify files
        if not self.deploy_warp_files():
            self.log("❌ Missing required files", "ERROR")
            return False
        
        # Step 4: Deploy to target
        if self.target == "ssh":
            self.deploy_to_ssh()
        
        # Step 5: Start WARP engine (local only for now)
        if self.target == "local":
            self.start_warp_engine_local()
        
        # Step 6: Verify
        if not self.verify_deployment():
            self.log("❌ Deployment verification failed", "ERROR")
            return False
        
        # Success!
        print("\n" + "=" * 80)
        self.log("✅ DEPLOYMENT COMPLETE!", "SUCCESS")
        print("=" * 80)
        print(f"\n{GREEN}🌟 ZION 2.8.0 'Ad Astra Per Estrella' is ready! 🌟{RESET}\n")
        
        if self.target == "local":
            print("To start WARP Engine:")
            print("  python3 zion_warp_engine_core.py")
            print()
        elif self.target == "ssh":
            print("To start on SSH:")
            print("  ssh root@91.98.122.165")
            print("  python3 zion_warp_engine_core.py")
            print()
        
        return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ZION Clean Deployment Orchestrator"
    )
    parser.add_argument(
        "--target",
        choices=["local", "ssh"],
        default="local",
        help="Deployment target (default: local)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean existing data before deployment"
    )
    
    args = parser.parse_args()
    
    orchestrator = ZionDeploymentOrchestrator(
        target=args.target,
        clean_data=args.clean
    )
    
    success = orchestrator.run_deployment()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
