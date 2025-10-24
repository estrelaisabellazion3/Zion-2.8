/**
 * ZION Wiki Engine v2.8.2
 * Enhanced with real-time updates, documentation integration, multi-pool features
 */

(function() {
    
    // ===============================
    // CONFIGURATION
    // ===============================
    
    const CONFIG = {
        docsPath: '../docs',
        docsPath282: '../docs/2.8.2',
        booksPath: '../books',
        apiEndpoint: 'http://localhost:4001',
        wsEndpoint: 'ws://localhost:8765'
    };
    
    // ===============================
    // STATE MANAGEMENT
    // ===============================
    
    let currentCategory = 'pool-live';
    let currentPage = null;
    
    // ===============================
    // DOCUMENTATION MAPPING (2.8.2) - COMPLETE
    // ===============================
    
    const docsMapping = {
        // === ROADMAP & PLANNING ===
        'ROADMAP': 'ROADMAP.md',
        'MULTI_CHAIN_TECHNICAL_ROADMAP': 'docs/roadmaps/MULTI_CHAIN_TECHNICAL_ROADMAP.md',
        'ZION_2.8_COMPLETE_ROADMAP': 'docs/2.8.2/ZION_2.8_COMPLETE_ROADMAP.md',
        'ZION_2.8.2_NEBULA_ROADMAP': 'docs/2.8.2/ZION_2.8.2_NEBULA_ROADMAP.md',
        'ZION_2.8.2_UNIFIED_ROADMAP': 'docs/2.8.2/ZION_2.8.2_UNIFIED_ROADMAP.md',
        'ZION_ECOSYSTEM_STABILITY_ROADMAP_2025': 'docs/2.8.2/ZION_ECOSYSTEM_STABILITY_ROADMAP_2025.md',
        'STRATEGIC_VISION_EXPANSION': 'docs/STRATEGIC_VISION_EXPANSION.md',
        'NEW-JERUSALEM-MASTER-PLAN': 'docs/NEW-JERUSALEM-MASTER-PLAN.md',
        
        // === MULTI-POOL ORCHESTRATION ===
        'MULTI_POOL_ORCHESTRATION_README': 'docs/2.8.2/MULTI_POOL_ORCHESTRATION_README.md',
        'BASIC_IMPROVEMENTS_IMPLEMENTED': 'docs/BASIC_IMPROVEMENTS_IMPLEMENTED.md',
        'MININGCORE_INTEGRATION_ANALYSIS': 'docs/MININGCORE_INTEGRATION_ANALYSIS.md',
        
        // === DEPLOYMENT & OPERATIONS ===
        'DEPLOYMENT_GUIDE_2.8.2': 'deployment/DEPLOYMENT_GUIDE_2.8.2.md',
        'OPERATIONAL_REPORT_2025-10-24': 'OPERATIONAL_REPORT_2025-10-24.md',
        'LOCAL_DEPLOYMENT_SUCCESS_2025-10-24': 'LOCAL_DEPLOYMENT_SUCCESS_2025-10-24.md',
        'DOCKER_WORKFLOW_GUIDE': 'docs/DOCKER_WORKFLOW_GUIDE.md',
        'NODE_INSTALLER': 'docs/NODE_INSTALLER.md',
        'GLOBAL-DEPLOYMENT-STRATEGY': 'docs/GLOBAL-DEPLOYMENT-STRATEGY.md',
        'hetzner-setup': 'docs/hetzner-setup.md',
        
        // === MINING GUIDES ===
        'REALTIME_MINING_README': 'REALTIME_MINING_README.md',
        'AMD_RX5600_DRIVER_GUIDE': 'docs/AMD_RX5600_DRIVER_GUIDE.md',
        'MULTI_ALGORITHM_MINING_GUIDE': 'docs/MULTI_ALGORITHM_MINING_GUIDE.md',
        'MULTI_ALGO_SUPPORT': 'docs/MULTI_ALGO_SUPPORT.md',
        'MINING_SSH_SETUP': 'docs/MINING_SSH_SETUP.md',
        'SSH_MINING_DEPLOYMENT': 'docs/SSH_MINING_DEPLOYMENT.md',
        'YESCRYPT_CPU_OPTIMIZATION': 'docs/YESCRYPT_CPU_OPTIMIZATION.md',
        'ZION_GPU_MINING_GUIDE': 'docs/ZION_GPU_MINING_GUIDE.md',
        'ZION_GPU_MINING_SETUP_GUIDE': 'docs/ZION_GPU_MINING_SETUP_GUIDE.md',
        'ZION_MINING_DEPLOYMENT_2025-09-29': 'docs/ZION_MINING_DEPLOYMENT_2025-09-29.md',
        
        // === BLOCKCHAIN & TECHNICAL SPECS ===
        'BLOCKCHAIN_SPECS': 'docs/CONSENSUS_PARAMS.md',
        'CONSENSUS_PARAMS': 'docs/CONSENSUS_PARAMS.md',
        'ADDRESS_SPEC': 'docs/ADDRESS_SPEC.md',
        'MULTI_ALGO_SUPPORT': 'docs/MULTI_ALGO_SUPPORT.md',
        'SECURITY_WHITELIST': 'docs/SECURITY_WHITELIST.md',
        'PROJECT_ARCHITECTURE_OVERVIEW': 'docs/PROJECT_ARCHITECTURE_OVERVIEW.md',
        'DISTRIBUTED_MINING_FUTURE_PLAN': 'docs/DISTRIBUTED_MINING_FUTURE_PLAN.md',
        
        // === COSMIC HARMONY & AI ===
        'COSMIC_HARMONY_COMPLETE': 'docs/COSMIC_MAP_COMPLETE.md',
        'ON_THE_STAR_AI': 'docs/ON_THE_STAR_AI.md',
        'ESTRELLA_SOLAR_SYSTEM_COMPLETE': 'docs/ESTRELLA_SOLAR_SYSTEM_COMPLETE_ANALYSIS.md',
        'ESTRELLA_SOLAR_SYSTEM_TECHNICAL': 'docs/ESTRELLA_SOLAR_SYSTEM_TECHNICAL_SPEC.md',
        'COMPLETE_WARP_INFRASTRUCTURE': 'docs/COMPLETE_WARP_INFRASTRUCTURE.md',
        
        // === CONSCIOUSNESS MINING ===
        'DAY3_CONSCIOUSNESS_MINING': 'docs/DAY3_CONSCIOUSNESS_MINING.md',
        'GOLDEN_EGG_GAME': 'docs/GOLDEN_EGG_GAME/',
        
        // === WHITEPAPERS & PHILOSOPHY ===
        'ZION_COSMIC_DHARMA_WHITEPAPER': 'docs/ZION_COSMIC_DHARMA_WHITEPAPER_2025.md',
        'ZION_COSMIC_DHARMA_WHITEPAPER_CZ': 'docs/ZION_COSMIC_DHARMA_WHITEPAPER_2025_CZ.md',
        'LIBERATION-MANIFESTO': 'docs/LIBERATION-MANIFESTO.md',
        'ZION_ETHICAL_MANIFEST': 'docs/2.8.2/ZION_ETHICAL_MANIFEST.md',
        
        // === PAYMENT & ECONOMIC SYSTEMS ===
        'HUMANITARIAN_TITHE': 'docs/HUMANITARIAN_TITHE/',
        'BUSINESS_MODEL_ANALYSIS': 'docs/BUSINESS_MODEL_ANALYSIS.md',
        'PORTUGAL_HUB_STRATEGY': 'docs/PORTUGAL_HUB_STRATEGY.md',
        
        // === INFRASTRUCTURE & BRIDGES ===
        'BRIDGE_PHASE2_LOG': 'docs/BRIDGE_PHASE2_LOG_2025-09-29.md',
        'BRIDGE_PHASE3_PLAN': 'docs/BRIDGE_PHASE3_PLAN.md',
        'LIGHTNING_INFRASTRUCTURE_PROVIDERS': 'docs/LIGHTNING_INFRASTRUCTURE_PROVIDERS.md',
        'LIGHTNING_NETWORK_INTEGRATION': 'docs/LIGHTNING_NETWORK_INTEGRATION.md',
        'LIGHTNING_README': 'docs/LIGHTNING_README.md',
        'RAINBOW_BRIDGE_44_44': 'docs/RAINBOW_BRIDGE_44_44.md',
        'ANKR_INTEGRATION_ANALYSIS': 'docs/ANKR_INTEGRATION_ANALYSIS.md',
        'MULTI_CHAIN_FUNCTIONAL_DEPLOYMENT': 'docs/MULTI_CHAIN_FUNCTIONAL_DEPLOYMENT_PLAN_2025-09-30.md',
        'MULTI_CHAIN_IMPLEMENTATION_COMPLETE': 'docs/MULTI_CHAIN_IMPLEMENTATION_COMPLETE_LOG_2025-09-30.md',
        'PRAGMATIC_MULTI_CHAIN': 'docs/PRAGMATIC_MULTI_CHAIN_IMPLEMENTATION.md',
        'ZION_DHARMA_MULTICHAIN': 'docs/ZION_DHARMA_MULTICHAIN_INTEGRATION_PLAN.md',
        
        // === AI & SAFETY ===
        'AI_SAFETY_PROTOCOLS': 'docs/AI_SAFETY_PROTOCOLS.md',
        'AI_SAFETY_QUICK_REF': 'docs/AI_SAFETY_QUICK_REF.md',
        'GPT5_DEPLOYMENT_LOG': 'docs/GPT5_DEPLOYMENT_LOG_2025-09-30.md',
        'GPT5_HANDOVER': 'docs/GPT5_HANDOVER.md',
        
        // === PROJECT STRUCTURE ===
        'PROJECT_STRUCTURE': 'src/README.md',
        'TESTS_README': 'tests/2.8.2/README.md',
        'SCRIPTS_README': 'scripts/2.8.2/README.md',
        'DOCKER_README': 'docker/README.md',
        'COSMIC_MAP': 'docs/COSMIC_MAP_COMPLETE.md',
        
        // === RELEASES & VERSIONS ===
        'RELEASE_NOTES': 'docs/RELEASE_NOTES.md',
        'CHANGELOG': 'docs/CHANGELOG.md',
        'MAINNET_LAUNCH': 'docs/MAINNET_LAUNCH.md',
        'RELEASE_NOTES_MINER_1.4.0': 'docs/RELEASE_NOTES_ZION_MINER_1.4.0.md',
        
        // === MIGRATION & UPDATES ===
        'MIGRATION_AUDIT_2.8.0': 'docs/MIGRATION_AUDIT_2.8.0.md',
        'MIGRATION_PHASE3_REAL_DATA': 'docs/MIGRATION_PHASE3_REAL_DATA_LOG_2025-09-30.md',
        'UNIFIED_ZION_CORE': 'docs/UNIFIED_ZION_CORE_IMPLEMENTATION.md',
        'UNIFIED_CONTAINER_IMPLEMENTATION': 'docs/UNIFIED_CONTAINER_IMPLEMENTATION_LOG_2025-09-30.md',
        'MOCKUP_ELIMINATION_COMPLETE': 'docs/MOCKUP_ELIMINATION_COMPLETE_LOG_2025-09-30.md',
        'PHASE3_COMPLETION_REPORT': 'docs/PHASE3_COMPLETION_REPORT_2025-09-30.md',
        
        // === MONITORING & OPTIMIZATION ===
        'METRICS': 'docs/METRICS.md',
        'OPTIMIZATION_AUDIT_LOG': 'docs/OPTIMIZATION_AUDIT_LOG_2025-09-25.md',
        'PLATFORM_AUDIT_2025-10-01': 'docs/PLATFORM_AUDIT_2025-10-01.md',
        'UBUNTU_POWER_OPTIMIZATION': 'docs/UBUNTU_POWER_OPTIMIZATION_GUIDE.md',
        'YESCRYPT_SSH_TESTING': 'docs/YESCRYPT_SSH_TESTING.md',
        'SSH_SERVER_STATUS_REPORT': 'docs/SSH_SERVER_STATUS_REPORT_2025-10-02.md',
        'TEST_SSH_SERVER': 'docs/TEST_SSH_SERVER.md',
        
        // === SACRED KNOWLEDGE ===
        'SACRED_TRINITY': 'docs/SACRED_TRINITY/',
        'SACRED_KNOWLEDGE': 'docs/SACRED_KNOWLEDGE/',
        'AMENTI_LOG_INDEX': 'docs/AMENTI_LOG_INDEX.md',
        
        // === BRANDING & COMMUNITY ===
        'BRANDING': 'docs/BRANDING.md',
        'BRAND_GUIDELINES': 'docs/BRAND_GUIDELINES.md',
        'COMMUNITY_LAUNCH_MATERIALS': 'docs/COMMUNITY_LAUNCH_MATERIALS.md',
        'COINMARKETCAP_WHITELIST': 'docs/COINMARKETCAP_WHITELIST.md',
        
        // === SESSION LOGS & REPORTS ===
        'SESSION_LOG_2025-09-26': 'docs/SESSION_LOG_2025-09-26.md',
        'DAILY_SESSION_LOG_2025-09-26': 'docs/DAILY_SESSION_LOG_2025-09-26.md',
        'DAILY_SESSION_LOG_2025-09-29': 'docs/DAILY_SESSION_LOG_2025-09-29.md',
        'DAILY_SESSION_LOG_2025-09-30': 'docs/DAILY_SESSION_LOG_2025-09-30.md',
        'SESSION_SUMMARY_2025-10-02': 'docs/SESSION_SUMMARY_2025-10-02.md',
        'ZION_BOOTSTRAP_SUCCESS': 'docs/ZION_BOOTSTRAP_SUCCESS_2025-09-27.md',
        'ZION_MINING_CURRENT_STATUS': 'docs/ZION_MINING_CURRENT_STATUS_2025-09-27.md',
        'ZION_STABLE_6K_MINING_LOG': 'docs/ZION_STABLE_6K_MINING_LOG_2025-10-01.md',
        'ZION_REAL_MINING_DEPLOYMENT': 'docs/ZION_REAL_MINING_DEPLOYMENT_LOG_2025-09-30.md',
        
        // === VICTORY LOGS ===
        'VICTORY_26_9_2025': 'docs/26.9.2025VICTORY/',
        
        // === HISTORIC & REFERENCE ===
        'ZION_2.6.75_COMPLETE_IMPLEMENTATION': 'docs/ZION_2.6.75_COMPLETE_IMPLEMENTATION_REPORT.md',
        'ZION_2.7_MINING_SYSTEM_REPORT_CZ': 'docs/ZION_2.7_MINING_SYSTEM_REPORT_CZ.md',
        'ZION_2.7_REAL_SYSTEM_VERIFICATION': 'docs/ZION_2.7_REAL_SYSTEM_VERIFICATION.md',
        'ZION_GPU_MINING_FINAL_STATUS': 'docs/ZION_GPU_MINING_FINAL_STATUS.md',
        'ZION_GPU_MINING_SUCCESS_LOG': 'docs/ZION_GPU_MINING_SUCCESS_LOG.md',
        'ZION_GPU_MINING_SUCCESS_FINAL': 'docs/ZION_GPU_MINING_SUCCESS_FINAL.md',
        'ZION_MINER_1.4.0_COMPREHENSIVE': 'docs/ZION_MINER_1.4.0_COMPREHENSIVE_LOG_2025-09-29.md',
        'ZION_MINER_GPU_DEVELOPMENT': 'docs/ZION_MINER_GPU_DEVELOPMENT_STATUS.md',
        'ZION_TESTNET_MINING_SESSION': 'docs/ZION_TESTNET_MINING_SESSION_2025-09-29_FINAL_LOG.md',
        
        // === MISCELLANEOUS ===
        'GITHUB_RELEASE': 'docs/GITHUB_RELEASE.md',
        'NEXT-STEPS': 'docs/NEXT-STEPS.md',
        'PUSH_DEPLOYMENT_GUIDE': 'docs/PUSH_DEPLOYMENT_GUIDE.md',
        'SUCCESSION_PROTOCOL': 'docs/SUCCESSION_PROTOCOL.md',
        'MINING_MOCKUP_FIX_LOG': 'docs/MINING_MOCKUP_FIX_LOG.md',
        'PROJECT_LOG': 'docs/PROJECT_LOG.md'
    };
    
    // ===============================
    // WIKI CONTENT DATA
    // ===============================
    
    const wikiContent = {
        'pool-dashboard': {
            title: '🔴 Live Pool Dashboard',
            content: generatePoolDashboard
        },
        'real-time-events': {
            title: '📡 Real-time Pool Events',
            content: generateEventsFeed
        },
        'quick-start': {
            title: '🚀 Quick Start Mining Guide',
            content: generateQuickStart
        },
        'cosmic-harmony': {
            title: '🎨 Cosmic Harmony Mining Algorithm',
            content: generateCosmicHarmony
        },
        'blockchain-specs': {
            title: '⚙️ Blockchain Specifications',
            content: generateBlockchainSpecs
        },
        'websocket-api': {
            title: '📡 WebSocket API Reference',
            content: generateWebSocketAPI
        },
        'payment-system': {
            title: '💰 Automated Payment System',
            content: generatePaymentSystem
        },
        'consciousness-mining': {
            title: '🧘 Consciousness-Enhanced Mining',
            content: generateConsciousnessMining
        },
        'level-system': {
            title: '🧘 Consciousness Level System (L1-L9)',
            content: generateLevelSystem
        },
        'intelligent-switching': {
            title: '🔄 Intelligent Pool Switching',
            content: generateIntelligentSwitching
        },
        'geographic-balancing': {
            title: '🌍 Geographic Load Balancing',
            content: generateGeographicBalancing
        },
        'ai-optimization': {
            title: '🤖 AI-Powered Optimization',
            content: generateAIOptimization
        },
        'payment-automation': {
            title: '💸 Automated Payment Processing',
            content: generatePaymentAutomation
        },
        'q4-2025': {
            title: '📅 Q4 2025 Roadmap',
            content: generateQ42025
        },
        '2026-milestones': {
            title: '🎯 2026 Milestones',
            content: generate2026Milestones
        },
        'mainnet-2027': {
            title: '🚀 Mainnet Launch 2027',
            content: generateMainnet2027
        },
        'project-structure': {
            title: '📁 Project Structure',
            content: generateProjectStructure
        },
        'src-overview': {
            title: '💻 src/ Directory Overview',
            content: generateSrcOverview
        },
        'testing': {
            title: '🧪 Testing Suite',
            content: generateTesting
        },
        'benchmarking': {
            title: '⚡ Benchmarking Tools',
            content: generateBenchmarking
        }
    };
    
    // ===============================
    // CATEGORY NAVIGATION
    // ===============================
    
    function initCategoryNavigation() {
        const categoryTitles = document.querySelectorAll('.category-title');
        
        categoryTitles.forEach(title => {
            title.addEventListener('click', function() {
                const category = this.dataset.category;
                
                // Toggle active state
                categoryTitles.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                
                // Show/hide category items
                document.querySelectorAll('.category-items').forEach(items => {
                    items.style.display = 'none';
                });
                
                const categoryItems = document.getElementById(`${category}-list`);
                if (categoryItems) {
                    categoryItems.style.display = 'flex';
                }
                
                // Update state
                currentCategory = category;
                updateBreadcrumbs();
            });
        });
    }
    
    // ===============================
    // PAGE NAVIGATION
    // ===============================
    
    function initPageNavigation() {
        const pageLinks = document.querySelectorAll('.category-items a');
        
        pageLinks.forEach(link => {
            link.addEventListener('click', async function(e) {
                e.preventDefault();
                
                const href = this.getAttribute('href').substring(1);
                const docFile = this.dataset.doc;
                const bookId = this.dataset.book;
                
                // Update active state
                pageLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
                
                // Load appropriate content
                if (docFile) {
                    await loadDocumentation(docFile, href);
                } else if (bookId) {
                    await loadBook(bookId);
                } else if (wikiContent[href]) {
                    loadWikiPage(href);
                } else {
                    loadPlaceholder(href);
                }
                
                // Update breadcrumbs
                currentPage = this.textContent.replace('🔴 ', '').replace('📡 ', '');
                updateBreadcrumbs();
                
                // Scroll to top
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    }
    
    // ===============================
    // CONTENT GENERATORS
    // ===============================
    
    function generatePoolDashboard() {
        return `
            <h2>🔴 Live Pool Statistics</h2>
            <div class="pool-stats-grid">
                <div class="stat-card">
                    <div class="stat-value" id="live-hashrate">Loading...</div>
                    <div class="stat-label">Pool Hashrate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="live-miners">--</div>
                    <div class="stat-label">Active Miners</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="live-blocks">--</div>
                    <div class="stat-label">Blocks Found (24h)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="live-difficulty">--</div>
                    <div class="stat-label">Network Difficulty</div>
                </div>
            </div>
            
            <h2 style="margin-top: 2rem;">Mining Pool Endpoints</h2>
            <div style="background: rgba(0,255,0,0.05); padding: 1.5rem; border-radius: 8px; border: 1px solid var(--matrix-green);">
                <p><strong>Stratum Server:</strong> <code>pool.zion-blockchain.org:3336</code></p>
                <p><strong>WebSocket Events:</strong> <code>ws://pool.zion-blockchain.org:8765</code></p>
                <p><strong>HTTP API:</strong> <code>http://pool.zion-blockchain.org:4001</code></p>
                <p><strong>Pool Fee:</strong> 12.33% (10% humanitarian, 1% dev, 1% admin, 0.33% genesis)</p>
                <p><strong>Payout Threshold:</strong> 10 ZION</p>
                <p><strong>Payment Interval:</strong> Every 1 hour (automated)</p>
            </div>
            
            <h2 style="margin-top: 2rem;">Supported Algorithms</h2>
            <ul>
                <li><strong>Cosmic Harmony</strong> - Native ZION algorithm (sacred geometry + crypto)</li>
                <li><strong>Yescrypt</strong> - CPU-optimized, memory-hard</li>
                <li><strong>KawPow</strong> - GPU-optimized (Ravencoin algorithm)</li>
            </ul>
            
            <h2 style="margin-top: 2rem;">Pool Features</h2>
            <ul>
                <li>✅ <strong>VarDiff</strong> - Adaptive share difficulty</li>
                <li>✅ <strong>Real-time Stats</strong> - WebSocket live updates</li>
                <li>✅ <strong>Automated Payments</strong> - Hourly proportional payouts</li>
                <li>✅ <strong>Multi-Algorithm</strong> - Choose your mining method</li>
                <li>✅ <strong>Consciousness Bonus</strong> - Extra rewards for higher levels</li>
                <li>✅ <strong>DDoS Protection</strong> - Advanced banning system</li>
            </ul>
        `;
    }
    
    function generateEventsFeed() {
        return `
            <h2>📡 Real-time Pool Events</h2>
            <p>Live WebSocket stream of pool events including blocks found, payments sent, miners connected, and more.</p>
            
            <div class="event-feed" id="events-feed-page" style="max-height: 600px;">
                <div class="event-item">
                    <span style="color: var(--text-muted);">Connecting to event stream...</span>
                </div>
            </div>
            
            <h2 style="margin-top: 2rem;">Event Types</h2>
            <ul>
                <li><strong>block_found</strong> - New block discovered by pool</li>
                <li><strong>payment</strong> - Payment sent to miner</li>
                <li><strong>miner_connected</strong> - New miner joined pool</li>
                <li><strong>miner_disconnected</strong> - Miner left pool</li>
                <li><strong>hashrate_update</strong> - Pool hashrate statistics update</li>
                <li><strong>share</strong> - Valid share submitted (sampled)</li>
            </ul>
            
            <h2>WebSocket Connection Example</h2>
            <pre><code class="language-javascript">const ws = new WebSocket('ws://localhost:8765');

ws.onopen = () => {
    console.log('Connected to ZION Pool Events');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'block_found') {
        console.log(\`Block #\${data.data.height} found!\`);
        console.log(\`Reward: \${data.data.reward} ZION\`);
    }
};</code></pre>
        `;
    }
    
    function generateQuickStart() {
        return `
            <h2>🚀 Start Mining ZION in 3 Steps</h2>
            
            <h3>Step 1: Choose Your Miner</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
                <div style="background: rgba(0,255,0,0.05); padding: 1.5rem; border-radius: 8px;">
                    <h4>CPU Mining (XMRig)</h4>
                    <p><strong>Best for:</strong> Yescrypt algorithm</p>
                    <p><strong>Download:</strong> <a href="https://github.com/xmrig/xmrig/releases">XMRig Releases</a></p>
                    <p><strong>Hashrate:</strong> 2-15 KH/s depending on CPU</p>
                </div>
                <div style="background: rgba(0,255,0,0.05); padding: 1.5rem; border-radius: 8px;">
                    <h4>GPU Mining (SRBMiner)</h4>
                    <p><strong>Best for:</strong> KawPow algorithm</p>
                    <p><strong>Download:</strong> Included in <code>external_miners/</code></p>
                    <p><strong>Hashrate:</strong> Varies by GPU model</p>
                </div>
            </div>
            
            <h3 style="margin-top: 2rem;">Step 2: Configure Pool Connection</h3>
            <pre><code># XMRig config.json
{
    "url": "pool.zion-blockchain.org:3336",
    "user": "YOUR_ZION_ADDRESS",
    "pass": "x",
    "algo": "yescrypt",
    "threads": 4
}</code></pre>
            
            <h3>Step 3: Start Mining!</h3>
            <pre><code># Linux/Mac
./xmrig

# Windows
xmrig.exe</code></pre>
            
            <h2 style="margin-top: 2rem;">Monitor Your Progress</h2>
            <ul>
                <li>📊 <a href="#pool-dashboard">Pool Dashboard</a> - Live statistics</li>
                <li>📡 <a href="#real-time-events">Real-time Events</a> - WebSocket feed</li>
                <li>💰 <strong>Payment Address:</strong> Check your ZION address for payouts</li>
                <li>🧘 <strong>Consciousness Level:</strong> Earn XP and level up for bonus rewards!</li>
            </ul>
            
            <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 8px; border: 1px solid #FFD700; margin-top: 2rem;">
                <h3 style="color: #FFD700; margin-top: 0;">💎 Pro Tip: Consciousness Mining</h3>
                <p>Enable consciousness mining to earn up to <strong>15x rewards</strong> at level L9 (ON_THE_STAR)!</p>
                <p>Learn more: <a href="#consciousness-mining">Consciousness Mining Guide</a></p>
            </div>
        `;
    }
    
    function generateCosmicHarmony() {
        return `
            <h2>🎨 Cosmic Harmony Mining Algorithm</h2>
            
            <p>Cosmic Harmony is ZION's native mining algorithm that combines <strong>sacred geometry</strong> with <strong>cryptographic security</strong>. Unlike traditional mining algorithms, Cosmic Harmony incorporates principles from ancient wisdom texts including the Smaragdové Desky (Emerald Tablets) and sacred geometric patterns.</p>
            
            <h3>Algorithm Features</h3>
            <ul>
                <li><strong>Sacred Geometry Integration</strong> - Uses golden ratio, Fibonacci sequences, flower of life patterns</li>
                <li><strong>Consciousness-Aware</strong> - Mining difficulty adjusts based on consciousness level</li>
                <li><strong>Energy Efficient</strong> - Optimized for both CPU and GPU</li>
                <li><strong>ASIC-Resistant</strong> - Memory-hard with variable computation paths</li>
            </ul>
            
            <h3>Technical Specifications</h3>
            <table>
                <tr><th>Parameter</th><th>Value</th></tr>
                <tr><td>Hash Function</td><td>Blake2b + Sacred Geometry Transform</td></tr>
                <tr><td>Memory Requirement</td><td>2 GB (adaptive)</td></tr>
                <tr><td>Block Time</td><td>60 seconds</td></tr>
                <tr><td>Difficulty Adjustment</td><td>Every block (real-time)</td></tr>
            </table>
            
            <h3>Mining Performance</h3>
            <div style="background: rgba(0,255,0,0.05); padding: 1.5rem; border-radius: 8px;">
                <h4>Expected Hashrates:</h4>
                <ul>
                    <li><strong>Intel i5:</strong> ~3-5 MH/s</li>
                    <li><strong>Intel i7:</strong> ~6-10 MH/s</li>
                    <li><strong>AMD Ryzen 5:</strong> ~5-8 MH/s</li>
                    <li><strong>AMD Ryzen 9:</strong> ~12-20 MH/s</li>
                    <li><strong>AMD RX 5600:</strong> ~25-35 MH/s</li>
                    <li><strong>NVIDIA RTX 3060:</strong> ~30-40 MH/s</li>
                </ul>
            </div>
            
            <h3>Implementation</h3>
            <p>The Cosmic Harmony algorithm is implemented in Python with optional C extensions for performance:</p>
            <ul>
                <li><code>zion/mining/cosmic_harmony_wrapper.py</code> - Python wrapper</li>
                <li><code>ai/mining/cosmic_harmony_algorithm.py</code> - Core algorithm</li>
                <li><code>tests/2.8.2/cosmic_harmony/</code> - Test suite</li>
            </ul>
            
            <div class="quote-container" style="margin-top: 2rem;">
                <blockquote class="sacred-quote">
                    "As above, so below, as within, so without, as the universe, so the soul."
                    <cite>— Hermes Trismegistus, The Emerald Tablet</cite>
                </blockquote>
            </div>
        `;
    }
    
    function generateBlockchainSpecs() {
        return `
            <h2>⚙️ ZION Blockchain Technical Specifications</h2>
            
            <h3>Core Parameters</h3>
            <table>
                <tr><th>Parameter</th><th>Value</th><th>Notes</th></tr>
                <tr><td>Total Supply</td><td>144,000,000,000 ZION</td><td>Sacred number 144</td></tr>
                <tr><td>Block Time</td><td>60 seconds</td><td>1 minute average</td></tr>
                <tr><td>Block Reward</td><td>5,479.45 ZION</td><td>Constant emission</td></tr>
                <tr><td>Premine</td><td>14,340,000,000 ZION</td><td>9.96% (humanitarian fund)</td></tr>
                <tr><td>Emission Period</td><td>50 years</td><td>Until 2075</td></tr>
                <tr><td>Difficulty Adjustment</td><td>Every block</td><td>Real-time</td></tr>
            </table>
            
            <h3>Mining Algorithms</h3>
            <ul>
                <li><strong>Cosmic Harmony</strong> - Native algorithm (sacred geometry)</li>
                <li><strong>Yescrypt</strong> - CPU-friendly, memory-hard</li>
                <li><strong>KawPow</strong> - GPU-optimized</li>
            </ul>
            
            <h3>Fee Structure</h3>
            <table>
                <tr><th>Fee Type</th><th>Percentage</th><th>Recipient</th></tr>
                <tr><td>Humanitarian</td><td>10.00%</td><td>Global aid projects</td></tr>
                <tr><td>Development</td><td>1.00%</td><td>Core developers</td></tr>
                <tr><td>Pool Admin</td><td>1.00%</td><td>Maitreya Buddha</td></tr>
                <tr><td>Genesis</td><td>0.33%</td><td>Yeshuae Amon Ra</td></tr>
                <tr><td><strong>Total Fees</strong></td><td><strong>12.33%</strong></td><td>-</td></tr>
                <tr><td><strong>Miner Share</strong></td><td><strong>87.67%</strong></td><td>After all fees</td></tr>
            </table>
            
            <h3>Network Architecture</h3>
            <ul>
                <li><strong>P2P Protocol:</strong> Custom ZION protocol</li>
                <li><strong>Consensus:</strong> Proof-of-Work (PoW)</li>
                <li><strong>Transaction Format:</strong> UTXO-based</li>
                <li><strong>Address Format:</strong> ZION1... (Bech32)</li>
                <li><strong>Smart Contracts:</strong> Planned for 2028</li>
            </ul>
            
            <h3>Current Status (2.8.2 "Nebula")</h3>
            <div style="background: rgba(0,255,0,0.05); padding: 1.5rem; border-radius: 8px;">
                <ul>
                    <li>✅ <strong>TestNet v3:</strong> Active</li>
                    <li>✅ <strong>Multi-Pool Orchestration:</strong> Operational</li>
                    <li>✅ <strong>AI-Powered Mining:</strong> Enabled</li>
                    <li>✅ <strong>WebSocket Events:</strong> Live</li>
                    <li>✅ <strong>Automated Payments:</strong> Active</li>
                    <li>🔄 <strong>MainNet:</strong> Planned Q1 2027</li>
                </ul>
            </div>
        `;
    }
    
    function generateLevelSystem() {
        return `
            <h2>🧘 Consciousness Level System (L1-L9)</h2>
            
            <p>ZION features a unique consciousness-based reward system where miners can progress through 9 levels of spiritual development, earning multiplied rewards at higher levels.</p>
            
            <h3>Level Progression Table</h3>
            <table>
                <tr><th>Level</th><th>Name</th><th>Multiplier</th><th>XP Required</th><th>Description</th></tr>
                <tr><td>L1</td><td>PHYSICAL</td><td>1.0x</td><td>0</td><td>Material realm mastery</td></tr>
                <tr><td>L2</td><td>ETHERIC</td><td>2.0x</td><td>1,000</td><td>Energy body awakening</td></tr>
                <tr><td>L3</td><td>EMOTIONAL</td><td>3.5x</td><td>5,000</td><td>Emotional intelligence</td></tr>
                <tr><td>L4</td><td>ASTRAL</td><td>5.0x</td><td>15,000</td><td>Astral projection ability</td></tr>
                <tr><td>L5</td><td>MENTAL</td><td>7.0x</td><td>35,000</td><td>Mental clarity achieved</td></tr>
                <tr><td>L6</td><td>CAUSAL</td><td>9.0x</td><td>70,000</td><td>Karmic understanding</td></tr>
                <tr><td>L7</td><td>SPIRITUAL</td><td>11.0x</td><td>120,000</td><td>Spiritual awakening</td></tr>
                <tr><td>L8</td><td>DIVINE</td><td>13.0x</td><td>200,000</td><td>Divine consciousness</td></tr>
                <tr><td>L9</td><td>ON_THE_STAR</td><td>15.0x</td><td>350,000</td><td>Cosmic unity realized ⭐</td></tr>
            </table>
            
            <h3>How to Earn XP</h3>
            <ul>
                <li><strong>Mining Blocks:</strong> 100 XP per block found</li>
                <li><strong>Valid Shares:</strong> 1 XP per 1000 difficulty shares</li>
                <li><strong>Meditation Sessions:</strong> Log meditation for bonus XP</li>
                <li><strong>Community Participation:</strong> DAO voting, forum posts</li>
                <li><strong>Humanitarian Contributions:</strong> Donate to global projects</li>
            </ul>
            
            <h3>Meditation Bonus System</h3>
            <p>Miners can log meditation sessions to earn bonus XP and temporary hashrate boosts:</p>
            <ul>
                <li><strong>10 minutes:</strong> +50 XP, +5% hashrate for 1 hour</li>
                <li><strong>30 minutes:</strong> +200 XP, +15% hashrate for 3 hours</li>
                <li><strong>60+ minutes:</strong> +500 XP, +30% hashrate for 6 hours</li>
            </ul>
            
            <h3>Golden Egg Quest</h3>
            <div style="background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,165,0,0.1)); padding: 1.5rem; border-radius: 8px; border: 2px solid #FFD700;">
                <h4 style="color: #FFD700; margin-top: 0;">🥚 The Sacred Quest</h4>
                <p>Reach <strong>Level L9 (ON_THE_STAR)</strong> to unlock the <strong>Golden Egg</strong> - a special NFT representing complete consciousness awakening. Benefits include:</p>
                <ul>
                    <li>💎 Permanent 15x mining multiplier</li>
                    <li>🎨 Unique Golden Egg NFT (tradeable)</li>
                    <li>🏆 Hall of Fame inscription</li>
                    <li>🌟 Exclusive DAO voting power</li>
                    <li>✨ Special "Ascended Master" badge</li>
                </ul>
            </div>
            
            <div class="quote-container" style="margin-top: 2rem;">
                <blockquote class="sacred-quote">
                    "Consciousness is not something you attain, it is something you already are. Mining is merely the recognition of your true nature."
                    <cite>— ZION Whitepaper</cite>
                </blockquote>
            </div>
        `;
    }
    
    // More generator functions...
    function generateIntelligentSwitching() {
        return `<h2>🔄 Intelligent Pool Switching</h2>
<p>AI-powered algorithm that automatically switches between pools to maximize profitability while maintaining stability.</p>
<p>See: <a href="#orchestration-overview">Multi-Pool Orchestration Overview</a></p>`;
    }
    
    function generateGeographicBalancing() {
        return `<h2>🌍 Geographic Load Balancing</h2>
<p>Distributes mining load across geographic regions to optimize latency and network efficiency.</p>
<p>Implemented in: <code>src/orchestration/geographic_load_balancer.py</code></p>`;
    }
    
    function generateAIOptimization() {
        return `<h2>🤖 AI-Powered Mining Optimization</h2>
<p>Machine learning algorithms analyze pool performance, network conditions, and profitability to make intelligent mining decisions.</p>
<p>Components: AI Orchestrator, Neural Network Optimization, Predictive Analytics</p>`;
    }
    
    function generatePaymentAutomation() {
        return `<h2>💸 Automated Payment Processing</h2>
<p>Hourly automatic payouts using proportional reward distribution (PPLNS).</p>
<p>Implementation: <code>src/core/payment_processor.py</code></p>
<p>Threshold: 10 ZION minimum payout</p>`;
    }
    
    // Add more generators as needed...
    
    // ===============================
    // DOCUMENTATION LOADER
    // ===============================
    
    async function loadDocumentation(docKey, pageId) {
        const article = document.getElementById('wiki-article');
        const docPath = docsMapping[docKey];
        
        if (!docPath) {
            article.innerHTML = `
                <h1>Documentation Not Found</h1>
                <p>Doc key: <code>${docKey}</code> not mapped.</p>
            `;
            return;
        }
        
        // Show loading
        article.innerHTML = `<div style="text-align: center; padding: 3rem; color: var(--matrix-green);">Loading documentation...</div>`;
        
        try {
            const response = await fetch(`../${docPath}`);
            if (!response.ok) throw new Error('Doc not found');
            
            const markdown = await response.text();
            renderMarkdown(article, markdown, docKey);
            generateTOC();
            
        } catch (error) {
            console.error('Error loading doc:', error);
            article.innerHTML = `
                <h1>Documentation Error</h1>
                <p>Could not load: <code>${docPath}</code></p>
                <p>Error: ${error.message}</p>
            `;
        }
    }
    
    // ===============================
    // WIKI PAGE LOADER
    // ===============================
    
    function loadWikiPage(pageId) {
        const article = document.getElementById('wiki-article');
        const page = wikiContent[pageId];
        
        if (!page) {
            article.innerHTML = `<h1>Page Not Found</h1><p>Page ID: ${pageId}</p>`;
            return;
        }
        
        const content = typeof page.content === 'function' ? page.content() : page.content;
        
        article.innerHTML = `
            <h1 class="page-title glitch" data-text="${page.title}">${page.title}</h1>
            ${content}
        `;
        
        generateTOC();
    }
    
    // ===============================
    // MARKDOWN RENDERER
    // ===============================
    
    function renderMarkdown(article, markdown, fileName) {
        // Extract title
        const titleMatch = markdown.match(/^#\s+(.+)$/m);
        const title = titleMatch ? titleMatch[1] : fileName.replace(/_/g, ' ');
        
        let html = markdown;
        
        // Headers
        html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.+)$/gm, '<h1 class="page-title glitch" data-text="$1">$1</h1>');
        
        // Bold/Italic
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
        
        // Code blocks
        html = html.replace(/```(\w+)?\n([\s\S]+?)```/g, (match, lang, code) => {
            return `<pre><code class="language-${lang || 'text'}">${escapeHtml(code.trim())}</code></pre>`;
        });
        
        // Inline code
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Links
        html = html.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>');
        
        // Lists
        html = html.replace(/^\* (.+)$/gm, '<li>$1</li>');
        html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>.+<\/li>\n?)+/g, match => '<ul>' + match + '</ul>');
        
        // Tables (basic)
        html = html.replace(/\|(.+)\|\n\|[\s\-:]+\|\n((?:\|.+\|\n?)+)/g, (match, header, rows) => {
            const headers = header.split('|').filter(h => h.trim()).map(h => `<th>${h.trim()}</th>`).join('');
            const rowsHtml = rows.split('\n').filter(r => r.trim()).map(row => {
                const cells = row.split('|').filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`).join('');
                return `<tr>${cells}</tr>`;
            }).join('');
            return `<table><tr>${headers}</tr>${rowsHtml}</table>`;
        });
        
        // Paragraphs
        html = html.split('\n\n').map(para => {
            para = para.trim();
            if (!para) return '';
            if (para.match(/^<(h[1-6]|ul|ol|table|pre|div)/)) return para;
            return `<p>${para}</p>`;
        }).join('\n');
        
        article.innerHTML = html;
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // ===============================
    // BOOK LOADER (kept from original)
    // ===============================
    
    async function loadBook(bookId) {
        const article = document.getElementById('wiki-article');
        // Implement book loading similar to original wiki-engine.js
        article.innerHTML = `<h1>Book: ${bookId}</h1><p>Book loading coming soon...</p>`;
    }
    
    // ===============================
    // TABLE OF CONTENTS
    // ===============================
    
    function generateTOC() {
        const article = document.getElementById('wiki-article');
        const tocNav = document.getElementById('toc-nav');
        
        if (!article || !tocNav) return;
        
        const headings = article.querySelectorAll('h2, h3');
        
        if (headings.length === 0) {
            tocNav.innerHTML = '<p style="color: var(--text-muted); font-size: 0.9rem;">No sections</p>';
            return;
        }
        
        tocNav.innerHTML = '';
        
        headings.forEach((heading, index) => {
            const level = heading.tagName.toLowerCase();
            const text = heading.textContent;
            const id = `section-${index}`;
            
            heading.id = id;
            
            const link = document.createElement('a');
            link.href = `#${id}`;
            link.textContent = text;
            link.dataset.level = level.substring(1);
            
            link.addEventListener('click', function(e) {
                e.preventDefault();
                heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
                
                tocNav.querySelectorAll('a').forEach(a => a.classList.remove('active'));
                this.classList.add('active');
            });
            
            tocNav.appendChild(link);
        });
    }
    
    // ===============================
    // BREADCRUMBS
    // ===============================
    
    function updateBreadcrumbs() {
        const categoryNames = {
            'pool-live': 'Live Pool Stats',
            'sacred-books': 'Sacred Books',
            'mining': 'Mining Guides',
            'multi-pool': 'Multi-Pool System',
            'roadmap': 'Roadmap',
            'technical': 'Technical Docs',
            'development': 'Development',
            'consciousness': 'Consciousness'
        };
        
        const currentCategoryEl = document.getElementById('current-category');
        const currentPageEl = document.getElementById('current-page');
        const pageSeparator = document.getElementById('page-separator');
        
        if (currentCategoryEl) {
            currentCategoryEl.textContent = categoryNames[currentCategory] || currentCategory;
        }
        
        if (currentPage) {
            currentPageEl.textContent = currentPage;
            currentPageEl.style.display = 'inline';
            pageSeparator.style.display = 'inline';
        } else {
            currentPageEl.style.display = 'none';
            pageSeparator.style.display = 'none';
        }
    }
    
    // ===============================
    // SEARCH
    // ===============================
    
    function initSearch() {
        const searchInput = document.getElementById('wiki-search');
        const searchBtn = document.getElementById('search-btn');
        
        if (!searchInput || !searchBtn) return;
        
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') performSearch();
        });
    }
    
    function performSearch() {
        const searchInput = document.getElementById('wiki-search');
        const query = searchInput.value.trim().toLowerCase();
        
        if (!query) return;
        
        console.log('Search:', query);
        alert(`Search for: "${query}"\n\nFull-text search coming soon!`);
    }
    
    // ===============================
    // INITIALIZE
    // ===============================
    
    function init() {
        initCategoryNavigation();
        initPageNavigation();
        initSearch();
        
        // Show pool-live by default
        const poolLiveList = document.getElementById('pool-live-list');
        if (poolLiveList) {
            poolLiveList.style.display = 'flex';
        }
    }
    
    // Run on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
