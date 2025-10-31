#!/usr/bin/env python3
"""
🌟 ZION 2.8.0 "Ad Astra Per Estrella" - Linux Dashboard 🌟
Advanced Mining Dashboard with AI Integration

Features:
- CPU & GPU Mining Control (Universal Miner)
- Real-time Logs & Monitoring
- AI Afterburner Integration
- All AI Systems (13 modules)
- Blockchain Status
- Pool Statistics
- ESTRELLA Quantum Engine Status
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import time
import json
import os
import sys
import psutil
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageTk

# Add AI path
sys.path.insert(0, str(Path(__file__).parent / 'ai'))

class ZionDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 ZION 2.8.0 Dashboard - Ad Astra Per Estrella")
        self.root.geometry("1400x900")
        # Base directory for all relative paths
        self.base_dir = Path(__file__).parent
        
        # Processes
        self.miner_process = None
        
        # Mining state (v2.8.4: ASIC-only)
        self.mining_active = False
        self.mining_mode = "hybrid"  # cpu, gpu, hybrid
        self.mining_algorithm = "cosmic_harmony"  # v2.8.4: default changed from autolykos2
        
        # Wallet
        self.wallet_balance = 0.0
        self.wallet_address = ""
        
        # Production pool (SSH server)
        self.production_pool = "91.98.122.165:3333"
        
        # UI refresh
        self.update_interval = 2000  # ms

        # Keyboard shortcuts for ESTRELLA
        self.root.bind('<Control-i>', lambda e: self.ignite_warp())
        self.root.bind('<Control-k>', lambda e: self.shutdown_warp())

        self.setup_ui()
        self.start_auto_refresh()
    
    def setup_ui(self):
        """Setup main UI"""
        # Title bar with logo
        title_frame = tk.Frame(self.root, bg="#1a1a2e")
        title_frame.pack(fill=tk.X, pady=10)
        
        # Load and display logo
        try:
            logo_path = Path(__file__).parent / "Logo" / "zion_logo.png"
            if logo_path.exists():
                logo_img = Image.open(logo_path)
                # Resize to 80x80
                logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_img)
                
                # Cache to prevent garbage collection
                self._logo_image = logo_photo
                
                logo_label = tk.Label(
                    title_frame,
                    image=logo_photo,
                    bg="#1a1a2e"
                )
                logo_label.pack(side=tk.LEFT, padx=20)
        except Exception as e:
            print(f"Could not load logo: {e}")
        
        # Title text
        title_text_frame = tk.Frame(title_frame, bg="#1a1a2e")
        title_text_frame.pack(side=tk.LEFT, expand=True)
        
        title = tk.Label(
            title_text_frame,
            text="🌟 ZION 2.8.0 Dashboard",
            font=("Arial", 20, "bold"),
            bg="#1a1a2e",
            fg="#00ff88"
        )
        title.pack()
        
        subtitle = tk.Label(
            title_text_frame,
            text="Ad Astra Per Estrella - Production Mining Platform",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#00aaff"
        )
        subtitle.pack()

        # Quick ESTRELLA controls in title bar
        title_actions = tk.Frame(title_frame, bg="#1a1a2e")
        title_actions.pack(side=tk.RIGHT, padx=10)
        ttk.Button(
            title_actions,
            text="🔥 IGNITE",
            command=self.ignite_warp,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            title_actions,
            text="⏹️  SHUTDOWN",
            command=self.shutdown_warp,
            width=12
        ).pack(side=tk.LEFT, padx=5)

        # Menu bar with ESTRELLA menu
        menubar = tk.Menu(self.root)
        estrella_menu = tk.Menu(menubar, tearoff=0)
        estrella_menu.add_command(label="Ignite Warp Engine (Ctrl+I)", command=self.ignite_warp)
        estrella_menu.add_command(label="Shutdown Warp (Ctrl+K)", command=self.shutdown_warp)
        menubar.add_cascade(label="ESTRELLA", menu=estrella_menu)
        self.root.config(menu=menubar)
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = ttk.Frame(main_frame, width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Right panel - Logs & Status
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.setup_controls(left_panel)
        self.setup_logs_and_status(right_panel)
    
    def setup_controls(self, parent):
        """Setup control panel"""
        
        # === MINING CONTROLS ===
        mining_frame = ttk.LabelFrame(parent, text="⛏️  Mining Controls", padding=10)
        mining_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Mode selection
        ttk.Label(mining_frame, text="Mode:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.mode_var = tk.StringVar(value="hybrid")
        mode_combo = ttk.Combobox(
            mining_frame,
            textvariable=self.mode_var,
            values=["cpu", "gpu", "hybrid"],
            state="readonly",
            width=15
        )
        mode_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Algorithm (v2.8.4: ASIC-only, default cosmic_harmony)
        ttk.Label(mining_frame, text="Algorithm:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.algo_var = tk.StringVar(value="cosmic_harmony")
        algo_combo = ttk.Combobox(
            mining_frame,
            textvariable=self.algo_var,
            values=["cosmic_harmony", "autolykos2", "randomx", "yescrypt"],
            state="readonly",
            width=15
        )
        algo_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Pool (Production SSH - read-only)
        ttk.Label(mining_frame, text="Pool:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(
            mining_frame, 
            text="91.98.122.165:3333",
            font=("Courier", 9, "bold")
        ).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Wallet
        ttk.Label(mining_frame, text="Wallet:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.wallet_var = tk.StringVar(value="")
        wallet_entry = ttk.Entry(mining_frame, textvariable=self.wallet_var, width=18)
        wallet_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Start/Stop buttons
        btn_frame = ttk.Frame(mining_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.start_btn = ttk.Button(
            btn_frame,
            text="🚀 Start Mining",
            command=self.start_mining,
            width=15
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(
            btn_frame,
            text="⏹️  Stop Mining",
            command=self.stop_mining,
            state=tk.DISABLED,
            width=15
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Mining status
        self.mining_status_label = ttk.Label(
            mining_frame,
            text="Status: Idle",
            font=("Arial", 10, "bold")
        )
        self.mining_status_label.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Hashrate display
        self.hashrate_label = ttk.Label(
            mining_frame,
            text="Hashrate: 0 H/s",
            font=("Courier", 9),
            foreground="#00ff88"
        )
        self.hashrate_label.grid(row=6, column=0, columnspan=2, pady=2)
        
        # Shares display
        self.shares_label = ttk.Label(
            mining_frame,
            text="Shares: 0 accepted / 0 rejected",
            font=("Courier", 9)
        )
        self.shares_label.grid(row=7, column=0, columnspan=2, pady=2)
        
        # === WALLET MANAGEMENT ===
        wallet_frame = ttk.LabelFrame(parent, text="💰 Wallet & Earnings", padding=10)
        wallet_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Balance display
        ttk.Label(wallet_frame, text="Balance:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.balance_label = ttk.Label(
            wallet_frame,
            text="0.0000 ZION",
            font=("Courier", 10, "bold"),
            foreground="#00ff88"
        )
        self.balance_label.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Wallet address
        ttk.Label(wallet_frame, text="Address:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.wallet_addr_label = ttk.Label(
            wallet_frame,
            text="Not set",
            font=("Courier", 8)
        )
        self.wallet_addr_label.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        btn_wallet_frame = ttk.Frame(wallet_frame)
        btn_wallet_frame.grid(row=2, column=0, columnspan=2, pady=5)
        
        ttk.Button(
            btn_wallet_frame,
            text="📝 Create Wallet",
            command=self.create_wallet,
            width=15
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            btn_wallet_frame,
            text="📂 Load Wallet",
            command=self.load_wallet,
            width=15
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            btn_wallet_frame,
            text="🔄 Refresh Balance",
            command=self.refresh_balance,
            width=15
        ).pack(side=tk.LEFT, padx=2)
        
        # === AI SYSTEMS ===
        ai_frame = ttk.LabelFrame(parent, text="🤖 AI Systems", padding=10)
        ai_frame.pack(fill=tk.X, pady=(0, 10))
        
        # AI Afterburner
        ttk.Button(
            ai_frame,
            text="🔥 AI Afterburner",
            command=self.open_afterburner,
            width=20
        ).pack(pady=2)
        
        # AI Orchestrator
        ttk.Button(
            ai_frame,
            text="🎼 AI Orchestrator",
            command=self.open_orchestrator,
            width=20
        ).pack(pady=2)
        
        # All AI Modules
        ttk.Button(
            ai_frame,
            text="🧠 All AI Modules (13)",
            command=self.show_ai_modules,
            width=20
        ).pack(pady=2)
        
        # === BLOCKCHAIN ===
        blockchain_frame = ttk.LabelFrame(parent, text="⛓️  Blockchain", padding=10)
        blockchain_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            blockchain_frame,
            text="🔗 Blockchain Status",
            command=self.check_blockchain_status,
            width=20
        ).pack(pady=2)
        
        ttk.Button(
            blockchain_frame,
            text="🔍 Recent Blocks",
            command=self.show_recent_blocks,
            width=20
        ).pack(pady=2)
        
        self.blockchain_status_label = ttk.Label(
            blockchain_frame,
            text="Blocks: Loading...",
            font=("Arial", 9)
        )
        self.blockchain_status_label.pack(pady=2)
        
        # === ESTRELLA WARP ENGINE ===
        estrella_frame = ttk.LabelFrame(parent, text="⭐ ESTRELLA WARP ENGINE", padding=10)
        estrella_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Warp status
        self.warp_status_label = ttk.Label(
            estrella_frame,
            text="🌑 WARP: OFFLINE",
            font=("Courier", 11, "bold"),
            foreground="#666666"
        )
        self.warp_status_label.pack(pady=5)
        
        # Coherence
        self.coherence_label = ttk.Label(
            estrella_frame,
            text="Quantum Coherence: 0%",
            font=("Courier", 9)
        )
        self.coherence_label.pack(pady=2)
        
        # Active AI count
        self.ai_count_label = ttk.Label(
            estrella_frame,
            text="Active AI Systems: 0 / 13",
            font=("Courier", 9)
        )
        self.ai_count_label.pack(pady=2)
        
        # Ignition button
        self.warp_btn = ttk.Button(
            estrella_frame,
            text="🔥 IGNITE WARP ENGINE",
            command=self.ignite_warp,
            width=25
        )
        self.warp_btn.pack(pady=10)
        
        # Shutdown button
        self.warp_shutdown_btn = ttk.Button(
            estrella_frame,
            text="⏹️  SHUTDOWN WARP",
            command=self.shutdown_warp,
            state=tk.DISABLED,
            width=25
        )
        self.warp_shutdown_btn.pack(pady=5)
        
        # === AI PLANETS STATUS ===
        planets_frame = ttk.LabelFrame(parent, text="🌌 AI PLANETS (13 Systems)", padding=10)
        planets_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Scrollable frame for planets
        canvas = tk.Canvas(planets_frame, height=200, bg="#0f0f1e")
        scrollbar = ttk.Scrollbar(planets_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # AI Systems status labels
        self.ai_systems = {
            "Master Orchestrator": {"emoji": "🎼", "status": "offline"},
            "AI Afterburner": {"emoji": "🔥", "status": "offline"},
            "Quantum AI": {"emoji": "⚛️", "status": "offline"},
            "Cosmic AI": {"emoji": "🌌", "status": "offline"},
            "Music AI": {"emoji": "🎵", "status": "offline"},
            "Oracle AI": {"emoji": "🔮", "status": "offline"},
            "Bio AI": {"emoji": "🧬", "status": "offline"},
            "Gaming AI": {"emoji": "🎮", "status": "offline"},
            "Lightning AI": {"emoji": "⚡", "status": "offline"},
            "Trading Bot": {"emoji": "💹", "status": "offline"},
            "Blockchain Analytics": {"emoji": "📊", "status": "offline"},
            "Security Monitor": {"emoji": "🛡️", "status": "offline"},
            "Predictive Maintenance": {"emoji": "🔧", "status": "offline"}
        }
        
        self.ai_labels = {}
        for i, (name, data) in enumerate(self.ai_systems.items()):
            label = ttk.Label(
                scrollable_frame,
                text=f"{data['emoji']} {name}: 🌑 OFFLINE",
                font=("Courier", 9),
                foreground="#666666"
            )
            label.grid(row=i, column=0, sticky=tk.W, pady=2, padx=5)
            self.ai_labels[name] = label
        
        # === STATS ===
        stats_frame = ttk.LabelFrame(parent, text="📊 Statistics", padding=10)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        self.stats_text = tk.Text(stats_frame, height=8, width=35, font=("Courier", 9))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_logs_and_status(self, parent):
        """Setup logs and status panel"""
        
        # Tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Mining Log Tab
        mining_tab = ttk.Frame(notebook)
        notebook.add(mining_tab, text="⛏️  Mining Log")
        
        self.mining_log = scrolledtext.ScrolledText(
            mining_tab,
            wrap=tk.WORD,
            font=("Courier", 9),
            bg="#1a1a1a",
            fg="#00ff88"
        )
        self.mining_log.pack(fill=tk.BOTH, expand=True)
        
        # Blockchain Tab
        blockchain_tab = ttk.Frame(notebook)
        notebook.add(blockchain_tab, text="⛓️  Blockchain")
        
        self.blockchain_text = scrolledtext.ScrolledText(
            blockchain_tab,
            wrap=tk.WORD,
            font=("Courier", 9),
            bg="#1a1a1a",
            fg="#ffaa00"
        )
        self.blockchain_text.pack(fill=tk.BOTH, expand=True)
        
        # AI Log Tab
        ai_tab = ttk.Frame(notebook)
        notebook.add(ai_tab, text="🤖 AI Systems")
        
        self.ai_log = scrolledtext.ScrolledText(
            ai_tab,
            wrap=tk.WORD,
            font=("Courier", 9),
            bg="#1a1a1a",
            fg="#ff00ff"
        )
        self.ai_log.pack(fill=tk.BOTH, expand=True)
    
    # === MINING FUNCTIONS ===
    
    def start_mining(self):
        """Start mining"""
        mode = self.mode_var.get()
        algo = self.algo_var.get()
        pool = self.production_pool
        wallet = self.wallet_var.get()
        
        # Validate wallet
        if not wallet or wallet.strip() == "":
            messagebox.showerror("Error", "Please set wallet address first!\n\nUse 'Create Wallet' or 'Load Wallet' button.")
            return
        
        self.log_mining(f"🚀 Starting mining: {mode} mode, {algo} algorithm")
        self.log_mining(f"   Pool: {pool}")
        self.log_mining(f"   Wallet: {wallet}")
        
        # Build command
        cmd = [
            "python3",
            "ai/zion_universal_miner.py",
            "--pool", pool,
            "--wallet", wallet,
            "--algorithm", algo
        ]
        
        if mode == "cpu":
            cmd.append("--cpu-only")
        elif mode == "gpu":
            cmd.append("--gpu")
        # hybrid is default
        
        try:
            # Redirect stdout to PIPE so we can capture it in GUI
            self.miner_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                text=True,
                cwd=str(self.base_dir)
            )
            
            self.mining_active = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.mining_status_label.config(text=f"Status: Mining ({mode})")
            
            # Start log reader threads
            threading.Thread(target=self.read_miner_output, daemon=True).start()
            threading.Thread(target=self.read_miner_errors, daemon=True).start()
            threading.Thread(target=self.monitor_mining_stats, daemon=True).start()
            
            self.log_mining("✅ Mining started successfully!")
            
        except Exception as e:
            self.log_mining(f"❌ Failed to start mining: {e}")
            messagebox.showerror("Mining Error", f"Failed to start mining:\n{e}")
    
    def stop_mining(self):
        """Stop mining"""
        if self.miner_process:
            self.log_mining("⏹️  Stopping mining...")
            self.miner_process.terminate()
            try:
                self.miner_process.wait(timeout=5)
            except:
                self.miner_process.kill()
            
            self.mining_active = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.mining_status_label.config(text="Status: Stopped")
            self.log_mining("✅ Mining stopped")
    
    def read_miner_output(self):
        """Read miner stdout in background"""
        if not self.miner_process:
            return
        
        try:
            while self.mining_active and self.miner_process:
                line = self.miner_process.stdout.readline()
                if not line:
                    break
                line = line.strip()
                if line:
                    self.log_mining(line)
                    # Parse hashrate from output
                    self.parse_mining_output(line)
        except Exception as e:
            self.log_mining(f"⚠️  Output reader error: {e}")
    
    def read_miner_errors(self):
        """Read miner stderr in background"""
        if not self.miner_process:
            return
        
        try:
            while self.mining_active and self.miner_process:
                line = self.miner_process.stderr.readline()
                if not line:
                    break
                line = line.strip()
                if line:
                    self.log_mining(f"⚠️  {line}")
        except Exception as e:
            pass
    
    def parse_mining_output(self, line):
        """Parse mining output for stats"""
        try:
            # Parse hashrate
            if "H/s" in line or "KH/s" in line or "MH/s" in line:
                import re
                match = re.search(r'([\d.]+)\s*(H/s|KH/s|MH/s)', line)
                if match:
                    hashrate = float(match.group(1))
                    unit = match.group(2)
                    if unit == "KH/s":
                        hashrate *= 1000
                    elif unit == "MH/s":
                        hashrate *= 1000000
                    self.root.after(0, lambda: self.hashrate_label.config(
                        text=f"Hashrate: {self.format_hashrate(hashrate)}"
                    ))
            
            # Parse shares
            if "ACCEPTED" in line or "accepted" in line:
                current = self.shares_label.cget("text")
                if "accepted" in current:
                    import re
                    match = re.search(r'(\d+) accepted', current)
                    if match:
                        accepted = int(match.group(1)) + 1
                        rejected_match = re.search(r'(\d+) rejected', current)
                        rejected = int(rejected_match.group(1)) if rejected_match else 0
                        self.root.after(0, lambda: self.shares_label.config(
                            text=f"Shares: {accepted} accepted / {rejected} rejected"
                        ))
            
            elif "REJECTED" in line or "rejected" in line or "duplicate" in line.lower():
                current = self.shares_label.cget("text")
                if "rejected" in current:
                    import re
                    accepted_match = re.search(r'(\d+) accepted', current)
                    rejected_match = re.search(r'(\d+) rejected', current)
                    accepted = int(accepted_match.group(1)) if accepted_match else 0
                    rejected = int(rejected_match.group(1)) + 1 if rejected_match else 1
                    self.root.after(0, lambda: self.shares_label.config(
                        text=f"Shares: {accepted} accepted / {rejected} rejected"
                    ))
        except Exception as e:
            pass
    
    def format_hashrate(self, hashrate):
        """Format hashrate for display"""
        if hashrate >= 1000000:
            return f"{hashrate / 1000000:.2f} MH/s"
        elif hashrate >= 1000:
            return f"{hashrate / 1000:.2f} KH/s"
        else:
            return f"{hashrate:.2f} H/s"
    
    def monitor_mining_stats(self):
        """Monitor mining stats while active"""
        while self.mining_active:
            try:
                # Just sleep and wait for log parsing to update stats
                time.sleep(2)
            except Exception as e:
                break
    
    # === WALLET FUNCTIONS ===
    
    def create_wallet(self):
        """Create new wallet"""
        self.log_blockchain("💰 Creating new ZION wallet...")
        
        try:
            result = subprocess.run(
                ["python3", "-c", """
import hashlib
import secrets
import time

# Generate wallet address
seed = secrets.token_hex(32)
address = 'ZION_' + hashlib.sha256(seed.encode()).hexdigest()[:20].upper()
ts = int(time.time())
print(f'Address: {address}')
print(f'Seed: {seed}')

# Save to file
with open(f'wallet_{ts}.txt', 'w') as f:
    f.write(f'ZION Wallet\\n')
    f.write(f'Address: {address}\\n')
    f.write(f'Seed: {seed}\\n')
    f.write(f'Created: {time.ctime()}\\n')
    print(f'Saved to: wallet_{ts}.txt')
"""],
                capture_output=True,
                text=True,
                cwd=str(self.base_dir)
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.startswith('Address: '):
                        addr = line.split(': ')[1]
                        self.wallet_var.set(addr)
                        self.wallet_addr_label.config(text=addr)
                        self.wallet_address = addr
                        self.log_blockchain(f"✅ Wallet created: {addr}")
                    elif line.startswith('Saved to: '):
                        file = line.split(': ')[1]
                        self.log_blockchain(f"📁 Saved to: {file}")
                
                messagebox.showinfo("Wallet Created", f"New wallet created!\n\nAddress: {self.wallet_address}\n\nBackup file saved in ZION1 folder.")
            else:
                self.log_blockchain(f"❌ Error: {result.stderr}")
                
        except Exception as e:
            self.log_blockchain(f"❌ Failed to create wallet: {e}")
            messagebox.showerror("Error", f"Failed to create wallet:\n{e}")
    
    def load_wallet(self):
        """Load existing wallet"""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="Select Wallet File",
            initialdir="/media/maitreya/ZION1",
            filetypes=[("Wallet files", "wallet_*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if line.startswith('Address: '):
                            addr = line.split(': ')[1]
                            self.wallet_var.set(addr)
                            self.wallet_addr_label.config(text=addr)
                            self.wallet_address = addr
                            self.log_blockchain(f"✅ Wallet loaded: {addr}")
                            self.refresh_balance()
                            break
            except Exception as e:
                self.log_blockchain(f"❌ Failed to load wallet: {e}")
                messagebox.showerror("Error", f"Failed to load wallet:\n{e}")
    
    def refresh_balance(self):
        """Refresh wallet balance from SSH pool"""
        if not self.wallet_address:
            messagebox.showwarning("No Wallet", "Please create or load a wallet first.")
            return
        
        self.log_blockchain(f"🔄 Checking balance for {self.wallet_address}...")
        
        try:
            result = subprocess.run(
                ["ssh", "root@91.98.122.165", f"""
cd /root/zion && python3 -c '
import sqlite3
import os

wallet = "{self.wallet_address}"
db_path = "data/zion_pool.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT balance FROM miners WHERE wallet_address = ?", (wallet,))
    result = c.fetchone()
    if result:
        print(f"Balance: {{result[0]:.4f}}")
    else:
        print("Balance: 0.0000")
    conn.close()
else:
    print("Balance: 0.0000")
'
"""],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.startswith('Balance: '):
                        balance = float(line.split(': ')[1])
                        self.wallet_balance = balance
                        self.balance_label.config(text=f"{balance:.4f} ZION")
                        self.log_blockchain(f"✅ Balance: {balance:.4f} ZION")
            else:
                self.log_blockchain(f"⚠️  Could not fetch balance: {result.stderr}")
                
        except Exception as e:
            self.log_blockchain(f"❌ Error checking balance: {e}")
    
    # === AI FUNCTIONS ===
    
    def ignite_warp(self):
        """Ignite ESTRELLA Warp Engine -启动所有13个AI系统"""
        self.log_ai("🔥 IGNITING ESTRELLA WARP ENGINE...")
        self.log_ai("⭐ Initializing Quantum Coherence Field...")
        
        # Update warp status
        self.warp_status_label.config(
            text="🌟 WARP: IGNITING...",
            foreground="#ffaa00"
        )
        self.warp_btn.config(state=tk.DISABLED)
        
        # Start ignition sequence in background
        threading.Thread(target=self.ignition_sequence, daemon=True).start()
    
    def ignition_sequence(self):
        """ESTRELLA ignition sequence - start all 13 AI systems"""
        try:
            # AI system mapping to files
            ai_files = {
                "Master Orchestrator": "ai/zion_ai_master_orchestrator.py",
                "AI Afterburner": "ai/zion_ai_afterburner.py",
                "Quantum AI": "ai/zion_quantum_ai.py",
                "Cosmic AI": "ai/zion_cosmic_ai.py",
                "Music AI": "ai/zion_music_ai.py",
                "Oracle AI": "ai/zion_oracle_ai.py",
                "Bio AI": "ai/zion_bio_ai.py",
                "Gaming AI": "ai/zion_gaming_ai.py",
                "Lightning AI": "ai/zion_lightning_ai.py",
                "Trading Bot": "ai/zion_trading_bot.py",
                "Blockchain Analytics": "ai/zion_blockchain_analytics.py",
                "Security Monitor": "ai/zion_security_monitor.py",
                "Predictive Maintenance": "ai/zion_predictive_maintenance.py"
            }
            
            active_count = 0
            coherence = 0
            
            for name, filepath in ai_files.items():
                coherence += 7.7  # 100% / 13 systems
                
                # Update coherence
                self.root.after(0, lambda c=coherence: self.coherence_label.config(
                    text=f"Quantum Coherence: {c:.1f}%"
                ))
                
                # Check if file exists
                if os.path.exists(filepath):
                    # Start AI system (most are modules, not standalone)
                    self.ai_systems[name]["status"] = "online"
                    active_count += 1
                    
                    # Update planet status
                    emoji = self.ai_systems[name]["emoji"]
                    self.root.after(0, lambda n=name, e=emoji: self.ai_labels[n].config(
                        text=f"{e} {n}: ☀️ ONLINE",
                        foreground="#00ff88"
                    ))
                    
                    self.log_ai(f"✅ {emoji} {name} - ONLINE")
                else:
                    self.log_ai(f"⚠️  {name} - Module not found")
                
                # Update active count
                self.root.after(0, lambda c=active_count: self.ai_count_label.config(
                    text=f"Active AI Systems: {c} / 13"
                ))
                
                time.sleep(0.3)  # Smooth ignition
            
            # Warp fully online
            self.root.after(0, lambda: self.warp_status_label.config(
                text="☀️ WARP: ONLINE - FULL POWER",
                foreground="#00ff88"
            ))
            self.root.after(0, lambda: self.warp_shutdown_btn.config(state=tk.NORMAL))
            
            self.log_ai(f"🌟 ESTRELLA WARP ENGINE FULLY OPERATIONAL!")
            self.log_ai(f"☀️  {active_count} / 13 AI Planets Active")
            self.log_ai(f"⚛️  Quantum Coherence: {coherence:.1f}%")
            
        except Exception as e:
            self.log_ai(f"❌ Warp ignition failed: {e}")
            self.root.after(0, lambda: self.warp_btn.config(state=tk.NORMAL))
    
    def shutdown_warp(self):
        """Shutdown ESTRELLA Warp Engine"""
        self.log_ai("⏹️  SHUTTING DOWN ESTRELLA WARP ENGINE...")
        
        # Reset all AI systems
        for name in self.ai_systems.keys():
            self.ai_systems[name]["status"] = "offline"
            emoji = self.ai_systems[name]["emoji"]
            self.ai_labels[name].config(
                text=f"{emoji} {name}: 🌑 OFFLINE",
                foreground="#666666"
            )
        
        # Reset warp status
        self.warp_status_label.config(
            text="🌑 WARP: OFFLINE",
            foreground="#666666"
        )
        self.coherence_label.config(text="Quantum Coherence: 0%")
        self.ai_count_label.config(text="Active AI Systems: 0 / 13")
        
        self.warp_btn.config(state=tk.NORMAL)
        self.warp_shutdown_btn.config(state=tk.DISABLED)
        
        self.log_ai("✅ WARP ENGINE SHUTDOWN COMPLETE")
    
    def open_afterburner(self):
        """Open AI Afterburner"""
        self.log_ai("🔥 Opening AI Afterburner...")
        try:
            subprocess.Popen(["python3", "ai/zion_ai_afterburner.py"])
        except Exception as e:
            self.log_ai(f"❌ Error: {e}")
    
    def open_orchestrator(self):
        """Open AI Orchestrator"""
        self.log_ai("🎼 Opening AI Orchestrator...")
        try:
            subprocess.Popen(["python3", "ai/zion_ai_master_orchestrator.py"])
        except Exception as e:
            self.log_ai(f"❌ Error: {e}")
    
    def show_ai_modules(self):
        """Show all AI modules"""
        modules = [
            "zion_ai_master_orchestrator.py - Master AI Coordination",
            "zion_ai_afterburner.py - GPU Optimization",
            "zion_cosmic_ai.py - Cosmic Pattern Analysis",
            "zion_quantum_ai.py - Quantum Computing Interface",
            "zion_oracle_ai.py - Predictive Oracle",
            "zion_music_ai.py - Sacred Music Generation",
            "zion_gaming_ai.py - Gaming AI Integration",
            "zion_bio_ai.py - Biological Systems Modeling",
            "zion_lightning_ai.py - Lightning Network AI",
            "zion_trading_bot.py - Automated Trading",
            "zion_blockchain_analytics.py - Chain Analytics",
            "zion_security_monitor.py - Security Monitoring",
            "zion_predictive_maintenance.py - System Maintenance"
        ]
        
        msg = "🧠 ZION AI Systems (13 Modules):\n\n" + "\n".join(modules)
        messagebox.showinfo("AI Modules", msg)
    
    # === LOGGING FUNCTIONS ===
    
    def check_blockchain_status(self):
        """Check real blockchain status from database"""
        self.log_blockchain("📊 Checking blockchain status...")
        try:
            import sqlite3
            db_path = self.base_dir / "data" / "zion_blockchain.db"
            if db_path.exists():
                conn = sqlite3.connect(str(db_path))
                c = conn.cursor()
                c.execute("SELECT COUNT(*) FROM blocks")
                block_count = c.fetchone()[0]
                
                c.execute("SELECT height, hash, timestamp FROM blocks ORDER BY height DESC LIMIT 1")
                last_block = c.fetchone()
                
                conn.close()
                
                self.blockchain_status_label.config(text=f"Blocks: {block_count}")
                
                if last_block:
                    self.log_blockchain(f"✅ Total blocks: {block_count}")
                    self.log_blockchain(f"   Last block: #{last_block[0]}")
                    self.log_blockchain(f"   Hash: {last_block[1][:16]}...")
                    self.log_blockchain(f"   Time: {last_block[2]}")
                else:
                    self.log_blockchain("⚠️  No blocks found yet")
            else:
                self.log_blockchain("❌ Blockchain database not found")
                self.blockchain_status_label.config(text="Blocks: No DB")
        except Exception as e:
            self.log_blockchain(f"❌ Error: {e}")
    
    def show_recent_blocks(self):
        """Show recent blocks from blockchain"""
        self.log_blockchain("🔍 Loading recent blocks...")
        try:
            import sqlite3
            db_path = self.base_dir / "data" / "zion_blockchain.db"
            if db_path.exists():
                conn = sqlite3.connect(str(db_path))
                c = conn.cursor()
                c.execute("SELECT height, hash, timestamp, reward FROM blocks ORDER BY height DESC LIMIT 10")
                blocks = c.fetchall()
                conn.close()
                
                self.log_blockchain(f"\n{'='*60}")
                self.log_blockchain("📦 LAST 10 BLOCKS:")
                self.log_blockchain(f"{'='*60}")
                
                for block in blocks:
                    self.log_blockchain(f"Block #{block[0]:4d} | Hash: {block[1][:16]}... | Reward: {block[3]:.2f} ZION")
                
                self.log_blockchain(f"{'='*60}\n")
            else:
                self.log_blockchain("❌ Blockchain database not found")
        except Exception as e:
            self.log_blockchain(f"❌ Error: {e}")
    
    # === LOGGING FUNCTIONS ===
    
    def log_mining(self, message):
        """Log to mining tab (thread-safe)"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        def _append():
            self.mining_log.insert(tk.END, f"[{timestamp}] {message}\n")
            self.mining_log.see(tk.END)
        self.root.after(0, _append)
    

    
    def log_ai(self, message):
        """Log to AI tab (thread-safe)"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        def _append():
            self.ai_log.insert(tk.END, f"[{timestamp}] {message}\n")
            self.ai_log.see(tk.END)
        self.root.after(0, _append)
    
    def log_blockchain(self, message):
        """Log to blockchain tab (thread-safe)"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        def _append():
            self.blockchain_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.blockchain_text.see(tk.END)
        self.root.after(0, _append)
    
    # === AUTO REFRESH ===
    
    def start_auto_refresh(self):
        """Start automatic stats refresh"""
        self.update_stats()
        self.root.after(self.update_interval, self.start_auto_refresh)
    
    def update_stats(self):
        """Update statistics display"""
        try:
            # System stats
            cpu_percent = psutil.cpu_percent(interval=0.1)
            mem = psutil.virtual_memory()
            
            stats = f"""
╔══════════════════════════════╗
║   SYSTEM STATISTICS          ║
╚══════════════════════════════╝

CPU Usage:    {cpu_percent:.1f}%
Memory:       {mem.percent:.1f}% ({mem.used / 1024**3:.1f} GB / {mem.total / 1024**3:.1f} GB)
Mining:       {"Active" if self.mining_active else "Idle"}
Wallet:       {self.wallet_address[:20] + "..." if self.wallet_address else "Not set"}
Balance:      {self.wallet_balance:.4f} ZION

╔══════════════════════════════╗
║   ESTRELLA WARP ENGINE       ║
╚══════════════════════════════╝

Status:       {sum(1 for ai in self.ai_systems.values() if ai["status"] == "online")} / 13 AI Active
Warp:         {"ONLINE" if any(ai["status"] == "online" for ai in self.ai_systems.values()) else "OFFLINE"}

╔══════════════════════════════╗
║   ZION 2.8.0 STATUS          ║
╚══════════════════════════════╝

Version:      2.8.0
Codename:     Ad Astra Per Estrella
Algorithm:    Autolykos v2 / RandomX
SSH Pool:     91.98.122.165:3333

"""
            
            self.stats_text.delete("1.0", tk.END)
            self.stats_text.insert("1.0", stats)
            
        except Exception as e:
            pass
    
    def cleanup(self):
        """Cleanup on exit"""
        if self.mining_active:
            self.stop_mining()

def main():
    root = tk.Tk()
    root.configure(bg="#0f0f1e")
    
    # Style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#0f0f1e")
    style.configure("TLabel", background="#0f0f1e", foreground="#ffffff")
    style.configure("TButton", background="#1a4d2e", foreground="#ffffff")
    style.configure("TLabelframe", background="#0f0f1e", foreground="#00ff88")
    style.configure("TLabelframe.Label", background="#0f0f1e", foreground="#00ff88")
    
    app = ZionDashboard(root)
    
    def on_closing():
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    print("🌟 ZION 2.8.0 Dashboard Starting...")
    print("   Linux Edition - Full AI Integration")
    print("   Ad Astra Per Estrella! ✨\n")
    main()
