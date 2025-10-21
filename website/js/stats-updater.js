/**
 * ZION BLOCKCHAIN - LIVE STATS UPDATER
 * Real-time network statistics from pool API
 */

(function() {
    const POOL_API_URL = 'http://pool.zion-blockchain.org:3336/api/stats';
    const UPDATE_INTERVAL = 10000; // 10 seconds
    
    // Stats elements
    const elements = {
        currentHeight: document.getElementById('current-height'),
        networkHashrate: document.getElementById('network-hashrate'),
        activeMiners: document.getElementById('active-miners'),
        statBlocks: document.getElementById('stat-blocks'),
        statMiners: document.getElementById('stat-miners'),
        statConsciousness: document.getElementById('stat-consciousness'),
        statDifficulty: document.getElementById('stat-difficulty'),
        statHashrateTotal: document.getElementById('stat-hashrate-total'),
        blocksList: document.getElementById('blocks-list')
    };
    
    // Format large numbers
    function formatNumber(num) {
        if (num >= 1000000000) {
            return (num / 1000000000).toFixed(2) + 'B';
        } else if (num >= 1000000) {
            return (num / 1000000).toFixed(2) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(2) + 'K';
        }
        return num.toFixed(0);
    }
    
    // Format hashrate
    function formatHashrate(hashrate) {
        if (hashrate >= 1000000000000) {
            return (hashrate / 1000000000000).toFixed(2) + ' TH/s';
        } else if (hashrate >= 1000000000) {
            return (hashrate / 1000000000).toFixed(2) + ' GH/s';
        } else if (hashrate >= 1000000) {
            return (hashrate / 1000000).toFixed(2) + ' MH/s';
        } else if (hashrate >= 1000) {
            return (hashrate / 1000).toFixed(2) + ' KH/s';
        }
        return hashrate.toFixed(2) + ' H/s';
    }
    
    // Format consciousness level
    function formatConsciousness(level) {
        const levels = {
            1: 'PHYSICAL',
            2: 'ETHERIC',
            3: 'EMOTIONAL',
            4: 'ASTRAL',
            5: 'MENTAL',
            6: 'CAUSAL',
            7: 'SPIRITUAL',
            8: 'DIVINE',
            9: 'ON_THE_STAR'
        };
        return levels[Math.floor(level)] || 'UNKNOWN';
    }
    
    // Fetch and update stats
    async function updateStats() {
        try {
            const response = await fetch(POOL_API_URL);
            if (!response.ok) {
                throw new Error('Failed to fetch stats');
            }
            
            const data = await response.json();
            
            // Update hero stats
            if (elements.currentHeight) {
                animateNumber(elements.currentHeight, data.network?.height || 0);
            }
            
            if (elements.networkHashrate) {
                elements.networkHashrate.textContent = formatHashrate(data.network?.hashrate || 0);
            }
            
            if (elements.activeMiners) {
                animateNumber(elements.activeMiners, data.pool?.miners || 0);
            }
            
            // Update detailed stats
            if (elements.statBlocks) {
                animateNumber(elements.statBlocks, data.network?.height || 0);
            }
            
            if (elements.statMiners) {
                animateNumber(elements.statMiners, data.pool?.miners || 0);
            }
            
            if (elements.statConsciousness) {
                const avgLevel = data.pool?.avg_consciousness_level || 1.0;
                elements.statConsciousness.textContent = formatConsciousness(avgLevel);
            }
            
            if (elements.statDifficulty) {
                elements.statDifficulty.textContent = formatNumber(data.network?.difficulty || 0);
            }
            
            if (elements.statHashrateTotal) {
                elements.statHashrateTotal.textContent = formatHashrate(data.network?.hashrate || 0);
            }
            
            // Update recent blocks
            if (elements.blocksList && data.blocks) {
                updateRecentBlocks(data.blocks);
            }
            
        } catch (error) {
            console.error('Error updating stats:', error);
            // Use fallback/demo data
            useFallbackData();
        }
    }
    
    // Animate number changes
    function animateNumber(element, targetValue) {
        const currentValue = parseInt(element.textContent.replace(/,/g, '')) || 0;
        const difference = targetValue - currentValue;
        const duration = 1000; // 1 second
        const steps = 60;
        const stepValue = difference / steps;
        const stepDuration = duration / steps;
        
        let current = currentValue;
        let step = 0;
        
        const interval = setInterval(() => {
            step++;
            current += stepValue;
            
            if (step >= steps) {
                element.textContent = targetValue.toLocaleString();
                clearInterval(interval);
            } else {
                element.textContent = Math.floor(current).toLocaleString();
            }
        }, stepDuration);
    }
    
    // Update recent blocks list
    function updateRecentBlocks(blocks) {
        if (!elements.blocksList) return;
        
        elements.blocksList.innerHTML = '';
        
        const recentBlocks = blocks.slice(0, 10); // Last 10 blocks
        
        recentBlocks.forEach(block => {
            const blockItem = document.createElement('div');
            blockItem.className = 'block-item';
            blockItem.style.cssText = `
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0.75rem;
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                margin-bottom: 0.5rem;
                transition: all 0.3s ease;
            `;
            
            blockItem.innerHTML = `
                <div>
                    <span style="color: var(--matrix-green); font-weight: bold;">Block #${block.height}</span>
                    <span style="color: var(--text-muted); margin-left: 1rem;">${formatTime(block.timestamp)}</span>
                </div>
                <div>
                    <span style="color: var(--text-white);">${block.reward?.toFixed(2) || '5479.45'} ZION</span>
                    <span style="color: var(--text-muted); margin-left: 1rem;">by ${block.miner?.substring(0, 10) || 'Anonymous'}...</span>
                </div>
            `;
            
            blockItem.addEventListener('mouseenter', function() {
                this.style.background = 'var(--bg-card-hover)';
                this.style.borderColor = 'var(--matrix-green)';
                this.style.transform = 'translateX(5px)';
            });
            
            blockItem.addEventListener('mouseleave', function() {
                this.style.background = 'var(--bg-card)';
                this.style.borderColor = 'var(--border-color)';
                this.style.transform = 'translateX(0)';
            });
            
            elements.blocksList.appendChild(blockItem);
        });
    }
    
    // Format timestamp
    function formatTime(timestamp) {
        const now = Date.now();
        const diff = now - timestamp;
        const seconds = Math.floor(diff / 1000);
        
        if (seconds < 60) {
            return seconds + 's ago';
        } else if (seconds < 3600) {
            return Math.floor(seconds / 60) + 'm ago';
        } else if (seconds < 86400) {
            return Math.floor(seconds / 3600) + 'h ago';
        } else {
            return Math.floor(seconds / 86400) + 'd ago';
        }
    }
    
    // Use fallback demo data when API unavailable
    function useFallbackData() {
        const demoData = {
            network: {
                height: 12547,
                hashrate: 2850000000, // 2.85 GH/s
                difficulty: 1250000
            },
            pool: {
                miners: 127,
                avg_consciousness_level: 3.2
            },
            blocks: generateDemoBlocks()
        };
        
        // Update with demo data
        if (elements.currentHeight) {
            animateNumber(elements.currentHeight, demoData.network.height);
        }
        
        if (elements.networkHashrate) {
            elements.networkHashrate.textContent = formatHashrate(demoData.network.hashrate);
        }
        
        if (elements.activeMiners) {
            animateNumber(elements.activeMiners, demoData.pool.miners);
        }
        
        if (elements.statBlocks) {
            animateNumber(elements.statBlocks, demoData.network.height);
        }
        
        if (elements.statMiners) {
            animateNumber(elements.statMiners, demoData.pool.miners);
        }
        
        if (elements.statConsciousness) {
            elements.statConsciousness.textContent = formatConsciousness(demoData.pool.avg_consciousness_level);
        }
        
        if (elements.statDifficulty) {
            elements.statDifficulty.textContent = formatNumber(demoData.network.difficulty);
        }
        
        if (elements.statHashrateTotal) {
            elements.statHashrateTotal.textContent = formatHashrate(demoData.network.hashrate);
        }
        
        if (elements.blocksList) {
            updateRecentBlocks(demoData.blocks);
        }
    }
    
    // Generate demo blocks
    function generateDemoBlocks() {
        const blocks = [];
        const now = Date.now();
        
        for (let i = 0; i < 10; i++) {
            blocks.push({
                height: 12547 - i,
                timestamp: now - (i * 60000), // 1 minute apart
                reward: 5479.45,
                miner: 'ZION' + Math.random().toString(36).substring(2, 15).toUpperCase()
            });
        }
        
        return blocks;
    }
    
    // Initialize
    function init() {
        // Initial update
        updateStats();
        
        // Set up periodic updates
        setInterval(updateStats, UPDATE_INTERVAL);
    }
    
    // Run on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
