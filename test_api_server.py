#!/usr/bin/env python3
"""
Simple WARP API Server Test
"""

import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime

class TestAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            health_data = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'uptime_seconds': 123,
                'blockchain_height': 42,
                'rpc_active': True,
                'p2p_active': True,
                'p2p_peers': 5,
                'active_pools': 2,
                'memory_usage_mb': 256.5,
                'cpu_usage_percent': 15.2,
                'consciousness_field': 0.95
            }
            
            self.wfile.write(json.dumps(health_data, indent=2).encode())
            
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status_data = {
                'blockchain_height': 42,
                'rpc_active': True,
                'p2p_active': True,
                'active_pools': 2,
                'system_health': 'HEALTHY',
                'memory_usage_mb': 256.5,
                'cpu_usage_percent': 15.2,
                'timestamp': datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(status_data, indent=2).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')
    
    def log_message(self, format, *args):
        return

def run_test_server():
    print("🧪 Starting Test API Server...")
    with HTTPServer(('localhost', 8081), TestAPIHandler) as httpd:
        print("✅ Test API Server running on http://localhost:8081")
        print("🌐 Available endpoints:")
        print("   GET /health - Health check")
        print("   GET /status - Full status")
        print("⏳ Server will run for 30 seconds...")
        httpd.timeout = 30
        httpd.serve_forever()

if __name__ == "__main__":
    run_test_server()