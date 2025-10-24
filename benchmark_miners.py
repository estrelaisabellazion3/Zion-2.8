#!/usr/bin/env python3
"""
⚡ ZION Mining Benchmark Suite
Porovnání výkonu různých minerů s našim AI minerem

Benchmarks:
1. SRBMiner-MULTI (external, optimized)
2. ZION AI GPU Miner (Cosmic Harmony)
3. ZION Universal Miner

Metriky:
- Hashrate (H/s, MH/s)
- GPU utilization
- Power efficiency (H/W)
- Share acceptance rate
- Latency
- Stability
"""

import subprocess
import time
import json
import psutil
import os
import signal
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MinerBenchmark:
    """Benchmark framework pro mining"""
    
    def __init__(self, duration: int = 60):
        """
        Args:
            duration: Benchmark duration in seconds
        """
        self.duration = duration
        self.results: Dict[str, Dict] = {}
        self.pool_host = "127.0.0.1"
        self.pool_port = 3333
        self.output_dir = Path("benchmark_results")
        self.output_dir.mkdir(exist_ok=True)
    
    def monitor_system_power(self, duration: float = 1.0) -> Dict:
        """Monitor system power consumption (estimate from CPU/GPU usage)"""
        cpu_percent = psutil.cpu_percent(interval=duration)
        
        # Estimate power (rough approximation)
        # AMD Ryzen 5 3600: ~65W TDP
        # AMD RX 5600 XT: ~150W TDP
        cpu_power = (cpu_percent / 100) * 65  # Watts
        
        # GPU power - try to read from sensors if available
        gpu_power = 0
        try:
            # Try reading AMD GPU power (requires proper drivers)
            with open('/sys/class/drm/card0/device/hwmon/hwmon0/power1_average', 'r') as f:
                gpu_power = int(f.read().strip()) / 1_000_000  # Convert µW to W
        except:
            # Fallback to estimate based on typical usage
            gpu_power = 150 * 0.8  # Assume 80% utilization
        
        return {
            'cpu_power_w': cpu_power,
            'gpu_power_w': gpu_power,
            'total_power_w': cpu_power + gpu_power,
            'cpu_usage_pct': cpu_percent
        }
        
    def benchmark_cosmic_harmony_gpu(self) -> Dict:
        """Benchmark Cosmic Harmony GPU miner"""
        logger.info("🔥 Benchmarking Cosmic Harmony GPU Miner...")
        
        cmd = [
            "python3",
            "ai/mining/cosmic_harmony_gpu_miner.py"
        ]
        
        env = os.environ.copy()
        env['RUSTICL_ENABLE'] = 'radeonsi'
        
        start_time = time.time()
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            preexec_fn=os.setsid  # Create process group for clean kill
        )
        
        # Collect metrics with timestamps
        hashrates = []
        hashrate_times = []
        shares = {'total': 0, 'accepted': 0, 'rejected': 0}
        gpu_temps = []
        power_samples = []
        
        try:
            # Monitor for duration
            while time.time() - start_time < self.duration:
                line = process.stdout.readline()
                if not line:
                    break
                
                current_time = time.time() - start_time
                
                # Parse hashrate
                if 'H/s' in line:
                    try:
                        # Extract: "⛏️  451168 H/s"
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if 'H/s' in part and i > 0:
                                hashrate = int(parts[i-1].replace(',', ''))
                                hashrates.append(hashrate)
                                hashrate_times.append(current_time)
                    except:
                        pass
                
                # Parse shares
                if 'Share accepted' in line or '✅' in line:
                    shares['accepted'] += 1
                    shares['total'] += 1
                elif 'Share rejected' in line or '❌' in line and 'Share' in line:
                    shares['rejected'] += 1
                    shares['total'] += 1
                
                # Parse GPU temp
                if 'GPU' in line and '°C' in line:
                    try:
                        temp_str = line.split('°C')[0].split()[-1]
                        gpu_temps.append(float(temp_str))
                    except:
                        pass
                
                # Sample power every 2 seconds
                if int(current_time) % 2 == 0 and len(power_samples) < int(current_time / 2):
                    power = self.monitor_system_power(duration=0.1)
                    power_samples.append(power)
        
        finally:
            # Clean kill entire process group
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            except:
                process.terminate()
            
            try:
                process.wait(timeout=5)
            except:
                process.kill()
        
        elapsed = time.time() - start_time
        
        # Calculate metrics
        avg_hashrate = sum(hashrates) / len(hashrates) if hashrates else 0
        avg_temp = sum(gpu_temps) / len(gpu_temps) if gpu_temps else 0
        acceptance_rate = (
            shares['accepted'] / shares['total'] * 100 
            if shares['total'] > 0 else 0
        )
        
        # Power efficiency
        avg_power = sum(p['total_power_w'] for p in power_samples) / len(power_samples) if power_samples else 0
        efficiency = avg_hashrate / avg_power if avg_power > 0 else 0  # H/W
        
        return {
            'name': 'ZION Cosmic Harmony GPU',
            'algorithm': 'cosmic_harmony',
            'duration': elapsed,
            'avg_hashrate': avg_hashrate,
            'hashrate_mhs': avg_hashrate / 1_000_000,
            'peak_hashrate': max(hashrates) if hashrates else 0,
            'min_hashrate': min(hashrates) if hashrates else 0,
            'shares_total': shares['total'],
            'shares_accepted': shares['accepted'],
            'shares_rejected': shares['rejected'],
            'acceptance_rate': acceptance_rate,
            'avg_gpu_temp': avg_temp,
            'avg_power_w': avg_power,
            'efficiency_h_per_w': efficiency,
            'hashrate_samples': len(hashrates),
            'raw_hashrates': hashrates,
            'hashrate_times': hashrate_times,
            'power_samples': power_samples
        }
    
    def benchmark_universal_miner_cpu(self) -> Dict:
        """Benchmark Universal Miner CPU (RandomX)"""
        logger.info("🖥️  Benchmarking Universal Miner CPU (RandomX)...")
        
        cmd = [
            "python3",
            "ai/zion_universal_miner.py",
            "--mode", "cpu",
            "--pool", f"{self.pool_host}:{self.pool_port}",
            "--wallet", "ZION_BENCH_CPU",
            "--algorithm", "randomx",
            "--duration", str(self.duration)
        ]
        
        start_time = time.time()
        hashrates = []
        hashrate_times = []
        power_samples = []
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            preexec_fn=os.setsid
        )
        
        try:
            while time.time() - start_time < self.duration + 10:
                line = process.stdout.readline()
                if not line:
                    if process.poll() is not None:
                        break
                    continue
                
                current_time = time.time() - start_time
                
                # Parse JSON status updates
                if '"cpu_hashrate":' in line or '"total_hashrate":' in line:
                    try:
                        # Try to extract hashrate
                        if '"cpu_hashrate":' in line:
                            hr_str = line.split('"cpu_hashrate":')[1].split(',')[0].strip()
                            hashrate = float(hr_str)
                            if hashrate > 0:
                                hashrates.append(hashrate)
                                hashrate_times.append(current_time)
                    except:
                        pass
                
                # Sample power
                if int(current_time) % 2 == 0 and len(power_samples) < int(current_time / 2):
                    power = self.monitor_system_power(duration=0.1)
                    power_samples.append(power)
        
        finally:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            except:
                process.terminate()
            try:
                process.wait(timeout=5)
            except:
                process.kill()
        
        elapsed = time.time() - start_time
        
        # Calculate metrics
        avg_hashrate = sum(hashrates) / len(hashrates) if hashrates else 0
        avg_power = sum(p['cpu_power_w'] for p in power_samples) / len(power_samples) if power_samples else 0
        efficiency = avg_hashrate / avg_power if avg_power > 0 else 0
        
        return {
            'name': 'ZION Universal Miner CPU',
            'algorithm': 'randomx',
            'duration': elapsed,
            'avg_hashrate': avg_hashrate,
            'hashrate_mhs': avg_hashrate / 1_000_000,
            'peak_hashrate': max(hashrates) if hashrates else 0,
            'min_hashrate': min(hashrates) if hashrates else 0,
            'shares_total': 0,  # Will be updated if available
            'shares_accepted': 0,
            'shares_rejected': 0,
            'acceptance_rate': 0,
            'avg_power_w': avg_power,
            'efficiency_h_per_w': efficiency,
            'hashrate_samples': len(hashrates),
            'raw_hashrates': hashrates,
            'hashrate_times': hashrate_times,
            'power_samples': power_samples
        }
    
    def run_all_benchmarks(self) -> Dict[str, Dict]:
        """Run all benchmarks"""
        logger.info("=" * 80)
        logger.info("🚀 ZION Mining Benchmark Suite")
        logger.info(f"⏱️  Duration: {self.duration}s per miner")
        logger.info("=" * 80)
        
        # 1. Cosmic Harmony GPU
        self.results['cosmic_harmony_gpu'] = self.benchmark_cosmic_harmony_gpu()
        time.sleep(5)  # Cool down
        
        # 2. Universal Miner CPU
        self.results['universal_cpu'] = self.benchmark_universal_miner_cpu()
        time.sleep(5)  # Cool down
        
        return self.results
    
    def plot_performance_graphs(self):
        """Generate performance graphs"""
        logger.info("📊 Generating performance graphs...")
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('ZION Mining Benchmark Results', fontsize=16, fontweight='bold')
        
        # 1. Hashrate over time comparison
        ax1 = axes[0, 0]
        for key, result in self.results.items():
            if 'hashrate_times' in result and result['hashrate_times']:
                times = result['hashrate_times']
                hashrates = [h / 1000 for h in result['raw_hashrates'][:len(times)]]  # Convert to kH/s
                ax1.plot(times, hashrates, label=result['name'], linewidth=2, marker='o', markersize=3)
        
        ax1.set_xlabel('Time (seconds)', fontsize=12)
        ax1.set_ylabel('Hashrate (kH/s)', fontsize=12)
        ax1.set_title('Hashrate Over Time', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Average hashrate comparison (bar chart)
        ax2 = axes[0, 1]
        names = [r['name'] for r in self.results.values()]
        avg_hashrates = [r['avg_hashrate'] / 1000 for r in self.results.values()]  # kH/s
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
        
        bars = ax2.bar(range(len(names)), avg_hashrates, color=colors[:len(names)])
        ax2.set_xticks(range(len(names)))
        ax2.set_xticklabels([n.replace('ZION ', '') for n in names], rotation=45, ha='right')
        ax2.set_ylabel('Average Hashrate (kH/s)', fontsize=12)
        ax2.set_title('Average Hashrate Comparison', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, (bar, val) in enumerate(zip(bars, avg_hashrates)):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(avg_hashrates)*0.01,
                    f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # 3. Power efficiency comparison
        ax3 = axes[1, 0]
        efficiencies = []
        eff_names = []
        for key, result in self.results.items():
            if 'efficiency_h_per_w' in result and result['efficiency_h_per_w'] > 0:
                efficiencies.append(result['efficiency_h_per_w'])
                eff_names.append(result['name'].replace('ZION ', ''))
        
        if efficiencies:
            bars = ax3.bar(range(len(eff_names)), efficiencies, color=colors[:len(eff_names)])
            ax3.set_xticks(range(len(eff_names)))
            ax3.set_xticklabels(eff_names, rotation=45, ha='right')
            ax3.set_ylabel('Efficiency (H/W)', fontsize=12)
            ax3.set_title('Power Efficiency', fontsize=14, fontweight='bold')
            ax3.grid(True, alpha=0.3, axis='y')
            
            for bar, val in zip(bars, efficiencies):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(efficiencies)*0.01,
                        f'{val:.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # 4. Share acceptance rate
        ax4 = axes[1, 1]
        acceptance_rates = []
        acc_names = []
        for key, result in self.results.items():
            if result.get('shares_total', 0) > 0:
                acceptance_rates.append(result['acceptance_rate'])
                acc_names.append(result['name'].replace('ZION ', ''))
        
        if acceptance_rates:
            bars = ax4.bar(range(len(acc_names)), acceptance_rates, color=colors[:len(acc_names)])
            ax4.set_xticks(range(len(acc_names)))
            ax4.set_xticklabels(acc_names, rotation=45, ha='right')
            ax4.set_ylabel('Acceptance Rate (%)', fontsize=12)
            ax4.set_title('Share Acceptance Rate', fontsize=14, fontweight='bold')
            ax4.set_ylim([0, 105])
            ax4.grid(True, alpha=0.3, axis='y')
            ax4.axhline(y=100, color='g', linestyle='--', alpha=0.5, label='100% Target')
            
            for bar, val in zip(bars, acceptance_rates):
                ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                        f'{val:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        
        # Save figure
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        graph_file = self.output_dir / f"benchmark_graph_{timestamp}.png"
        plt.savefig(graph_file, dpi=150, bbox_inches='tight')
        logger.info(f"📊 Graphs saved to: {graph_file}")
        
        return str(graph_file)
    
    def generate_report(self) -> str:
        """Generate benchmark report"""
        report = []
        report.append("\n" + "=" * 80)
        report.append("📊 ZION MINING BENCHMARK REPORT")
        report.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        
        for key, result in self.results.items():
            report.append(f"\n🔹 {result['name']}")
            report.append(f"   Algorithm: {result['algorithm']}")
            report.append(f"   Duration: {result['duration']:.1f}s")
            report.append(f"   ⚡ Avg Hashrate: {result['avg_hashrate']:,.0f} H/s ({result['hashrate_mhs']:.3f} MH/s)")
            
            if 'peak_hashrate' in result:
                report.append(f"   📈 Peak: {result['peak_hashrate']:,.0f} H/s")
                report.append(f"   📉 Min: {result['min_hashrate']:,.0f} H/s")
            
            report.append(f"   📦 Shares: {result['shares_total']} (✅ {result['shares_accepted']}, ❌ {result['shares_rejected']})")
            report.append(f"   ✓ Acceptance: {result['acceptance_rate']:.1f}%")
            
            if 'avg_gpu_temp' in result and result['avg_gpu_temp'] > 0:
                report.append(f"   🌡️  Avg GPU Temp: {result['avg_gpu_temp']:.1f}°C")
            
            if 'avg_power_w' in result and result['avg_power_w'] > 0:
                report.append(f"   ⚡ Avg Power: {result['avg_power_w']:.1f}W")
                report.append(f"   🎯 Efficiency: {result['efficiency_h_per_w']:,.0f} H/W")
            
            if 'hashrate_samples' in result:
                report.append(f"   📊 Samples: {result['hashrate_samples']}")
            
            report.append("")
        
        report.append("=" * 80)
        
        # Performance comparison
        if len(self.results) > 1:
            report.append("\n📊 Performance Comparison:")
            sorted_results = sorted(
                self.results.values(), 
                key=lambda x: x['avg_hashrate'], 
                reverse=True
            )
            
            baseline = sorted_results[0]['avg_hashrate']
            for i, result in enumerate(sorted_results, 1):
                relative = (result['avg_hashrate'] / baseline * 100) if baseline > 0 else 0
                report.append(f"   {i}. {result['name']}: {relative:.1f}% of best")
            
            report.append("")
        
        # Efficiency comparison
        eff_results = [r for r in self.results.values() if r.get('efficiency_h_per_w', 0) > 0]
        if len(eff_results) > 1:
            report.append("\n⚡ Power Efficiency Comparison:")
            sorted_eff = sorted(eff_results, key=lambda x: x['efficiency_h_per_w'], reverse=True)
            for i, result in enumerate(sorted_eff, 1):
                report.append(f"   {i}. {result['name']}: {result['efficiency_h_per_w']:,.0f} H/W")
            report.append("")
        
        report.append("💡 Optimization Recommendations:")
        
        for result in self.results.values():
            if result['acceptance_rate'] < 95 and result['shares_total'] > 0:
                report.append(f"   ⚠️  {result['name']}: Low acceptance rate ({result['acceptance_rate']:.1f}%)")
            
            if 'avg_gpu_temp' in result and result['avg_gpu_temp'] > 70:
                report.append(f"   🌡️  {result['name']}: High GPU temp ({result['avg_gpu_temp']:.1f}°C)")
            
            if 'efficiency_h_per_w' in result and result['efficiency_h_per_w'] > 0:
                # Compare against theoretical optimum
                if result['algorithm'] == 'cosmic_harmony' and result['efficiency_h_per_w'] < 3000:
                    report.append(f"   🎯 {result['name']}: Room for efficiency improvement")
        
        report.append("")
        report.append("=" * 80)
        
        return '\n'.join(report)
    
    def save_report(self, filename: str = None):
        """Save benchmark report to file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.output_dir / f"benchmark_report_{timestamp}.txt"
        else:
            filename = self.output_dir / filename
        
        report = self.generate_report()
        
        with open(filename, 'w') as f:
            f.write(report)
        
        logger.info(f"📝 Report saved to: {filename}")
        
        # Also save JSON
        json_file = str(filename).replace('.txt', '.json')
        
        # Prepare JSON (remove non-serializable data)
        json_data = {}
        for key, result in self.results.items():
            json_data[key] = {k: v for k, v in result.items() 
                            if not isinstance(v, (list)) or len(str(v)) < 10000}
        
        with open(json_file, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        logger.info(f"📊 JSON data saved to: {json_file}")
        
        return str(filename)


if __name__ == "__main__":
    import sys
    
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    
    print("🚀 Starting ZION Mining Benchmark Suite...")
    print(f"⏱️  Test duration: {duration}s per miner")
    print()
    
    benchmark = MinerBenchmark(duration=duration)
    benchmark.run_all_benchmarks()
    
    # Print report
    print(benchmark.generate_report())
    
    # Save to file
    benchmark.save_report()
    
    # Generate graphs
    try:
        graph_file = benchmark.plot_performance_graphs()
        print(f"\n📊 Performance graphs saved to: {graph_file}")
    except Exception as e:
        logger.error(f"Failed to generate graphs: {e}")
        import traceback
        traceback.print_exc()
