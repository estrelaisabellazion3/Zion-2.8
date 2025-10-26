/**
 * ZION Wiki Engine v2.8.2 - COMPLETE
 * Full documentation mapping and rendering system
 * Supports 100+ documentation files from /docs
 */

(function() {

    // ===============================
    // COMPLETE DOCUMENTATION MAPPING
    // ===============================

    window.docsMapping = {
        // === CORE ROADMAPS ===
        'ROADMAP': 'docs/ROADMAP.md',
        'MULTI_CHAIN_TECHNICAL_ROADMAP': 'docs/roadmaps/MULTI_CHAIN_TECHNICAL_ROADMAP.md',
        'ZION_2.8_COMPLETE_ROADMAP': 'docs/2.8.2/ZION_2.8_COMPLETE_ROADMAP.md',
        'ZION_2.8.2_NEBULA_ROADMAP': 'docs/2.8.2/ZION_2.8.2_NEBULA_ROADMAP.md',
        'STRATEGIC_VISION_EXPANSION': 'docs/STRATEGIC_VISION_EXPANSION.md',
        'NEW-JERUSALEM-MASTER-PLAN': 'docs/NEW-JERUSALEM-MASTER-PLAN.md',
        'LIBERATION-MANIFESTO': 'docs/LIBERATION-MANIFESTO.md',

        // === MULTI-POOL ORCHESTRATION ===
        'MULTI_POOL_ORCHESTRATION_README': 'docs/2.8.2/MULTI_POOL_ORCHESTRATION_README.md',
        'BASIC_IMPROVEMENTS_IMPLEMENTED': 'docs/BASIC_IMPROVEMENTS_IMPLEMENTED.md',
        'MININGCORE_INTEGRATION_ANALYSIS': 'docs/MININGCORE_INTEGRATION_ANALYSIS.md',

        // === DEPLOYMENT & INFRASTRUCTURE ===
        'DEPLOYMENT_GUIDE_2.8.2': 'docs/deployment/DEPLOYMENT_GUIDE_2.8.2.md',
        'OPERATIONAL_REPORT_2025-10-24': 'docs/OPERATIONAL_REPORT_2025-10-24.md',
        'LOCAL_DEPLOYMENT_SUCCESS_2025-10-24': 'docs/LOCAL_DEPLOYMENT_SUCCESS_2025-10-24.md',
        'DOCKER_WORKFLOW_GUIDE': 'docs/DOCKER_WORKFLOW_GUIDE.md',
        'NODE_INSTALLER': 'docs/NODE_INSTALLER.md',
        'GLOBAL_DEPLOYMENT_STRATEGY': 'docs/GLOBAL_DEPLOYMENT_STRATEGY.md',
        'HETZNER_SETUP': 'docs/hetzner-setup.md',

        // === MINING GUIDES ===
        'REALTIME_MINING_README': 'docs/REALTIME_MINING_README.md',
        'AMD_RX5600_DRIVER_GUIDE': 'docs/AMD_RX5600_DRIVER_GUIDE.md',
        'MULTI_ALGORITHM_MINING_GUIDE': 'docs/MULTI_ALGORITHM_MINING_GUIDE.md',
        'MULTI_ALGO_SUPPORT': 'docs/MULTI_ALGO_SUPPORT.md',
        'MINING_SSH_SETUP': 'docs/MINING_SSH_SETUP.md',
        'YESCRYPT_CPU_OPTIMIZATION': 'docs/YESCRYPT_CPU_OPTIMIZATION.md',
        'ZION_GPU_MINING_SETUP_GUIDE': 'docs/ZION_GPU_MINING_SETUP_GUIDE.md',
        'ZION_MINING_DEPLOYMENT_2025-09-29': 'docs/ZION_MINING_DEPLOYMENT_2025-09-29.md',
        'DISTRIBUTED_MINING_FUTURE_PLAN': 'docs/DISTRIBUTED_MINING_FUTURE_PLAN.md',

        // === TECHNICAL SPECIFICATIONS ===
        'CONSENSUS_PARAMS': 'docs/CONSENSUS_PARAMS.md',
        'ADDRESS_SPEC': 'docs/ADDRESS_SPEC.md',
        'SECURITY_WHITELIST': 'docs/SECURITY_WHITELIST.md',
        'PROJECT_ARCHITECTURE_OVERVIEW': 'docs/PROJECT_ARCHITECTURE_OVERVIEW.md',
        'AI_SAFETY_PROTOCOLS': 'docs/AI_SAFETY_PROTOCOLS.md',
        'AI_SAFETY_QUICK_REF': 'docs/AI_SAFETY_QUICK_REF.md',
        'COMPLETE_WARP_INFRASTRUCTURE': 'docs/COMPLETE_WARP_INFRASTRUCTURE.md',

        // === COSMIC & CONSCIOUSNESS ===
        'COSMIC_MAP_COMPLETE': 'docs/COSMIC_MAP_COMPLETE.md',
        'ON_THE_STAR_AI': 'docs/ON_THE_STAR_AI.md',
        'ESTRELLA_SOLAR_SYSTEM_COMPLETE': 'docs/ESTRELLA_SOLAR_SYSTEM_COMPLETE_ANALYSIS.md',
        'ESTRELLA_SOLAR_SYSTEM_TECHNICAL': 'docs/ESTRELLA_SOLAR_SYSTEM_TECHNICAL_SPEC.md',
        'DAY3_CONSCIOUSNESS_MINING': 'docs/DAY3_CONSCIOUSNESS_MINING.md',
        'ZION_GALAXY_ARCHITECTURE': 'docs/ZION_GALAXY_ARCHITECTURE.md',

        // === WHITEPAPERS ===
        'ZION_COSMIC_DHARMA_WHITEPAPER': 'docs/ZION_COSMIC_DHARMA_WHITEPAPER_2025.md',
        'ZION_COSMIC_DHARMA_WHITEPAPER_CZ': 'docs/ZION_COSMIC_DHARMA_WHITEPAPER_2025_CZ.md',
        'ZION_DHARMA_MULTICHAIN': 'docs/ZION_DHARMA_MULTICHAIN_INTEGRATION_PLAN.md',
        'ZION_ETHICAL_MANIFEST': 'docs/2.8.2/ZION_ETHICAL_MANIFEST.md',

        // === ECONOMIC SYSTEMS ===
        'BUSINESS_MODEL_ANALYSIS': 'docs/BUSINESS_MODEL_ANALYSIS.md',
        'PORTUGAL_HUB_STRATEGY': 'docs/PORTUGAL_HUB_STRATEGY.md',

        // === BRIDGES & INTEGRATION ===
        'MULTI_CHAIN_FUNCTIONAL_DEPLOYMENT': 'docs/MULTI_CHAIN_FUNCTIONAL_DEPLOYMENT_PLAN_2025-09-30.md',
        'BRIDGE_PHASE2_LOG': 'docs/BRIDGE_PHASE2_LOG_2025-09-29.md',
        'BRIDGE_PHASE3_PLAN': 'docs/BRIDGE_PHASE3_PLAN.md',
        'LIGHTNING_INFRASTRUCTURE_PROVIDERS': 'docs/LIGHTNING_INFRASTRUCTURE_PROVIDERS.md',
        'LIGHTNING_NETWORK_INTEGRATION': 'docs/LIGHTNING_NETWORK_INTEGRATION.md',
        'LIGHTNING_README': 'docs/LIGHTNING_README.md',
        'RAINBOW_BRIDGE_44_44': 'docs/RAINBOW_BRIDGE_44_44.md',
        'ANKR_INTEGRATION_ANALYSIS': 'docs/ANKR_INTEGRATION_ANALYSIS.md',
        'PRAGMATIC_MULTI_CHAIN': 'docs/PRAGMATIC_MULTI_CHAIN_IMPLEMENTATION.md',

        // === RELEASE & LAUNCH ===
        'RELEASE_NOTES': 'docs/RELEASE_NOTES.md',
        'CHANGELOG': 'docs/CHANGELOG.md',
        'MAINNET_LAUNCH': 'docs/MAINNET_LAUNCH.md',
        'RELEASE_NOTES_ZION_MINER': 'docs/RELEASE_NOTES_ZION_MINER_1.4.0.md',
        'GITHUB_RELEASE': 'docs/GITHUB_RELEASE.md',
        'COMMUNITY_LAUNCH_MATERIALS': 'docs/COMMUNITY_LAUNCH_MATERIALS.md',
        'NEXT-STEPS': 'docs/NEXT-STEPS.md',

        // === MONITORING & OPERATIONS ===
        'METRICS': 'docs/METRICS.md',
        'DAY2_MONITORING_SETUP': 'docs/DAY2_MONITORING_SETUP.md',
        'OPTIMIZATION_AUDIT_LOG': 'docs/OPTIMIZATION_AUDIT_LOG_2025-09-25.md',
        'PLATFORM_AUDIT_2025-10-01': 'docs/PLATFORM_AUDIT_2025-10-01.md',
        'UBUNTU_POWER_OPTIMIZATION': 'docs/UBUNTU_POWER_OPTIMIZATION_GUIDE.md',

        // === UNIFIED CORE ===
        'UNIFIED_ZION_CORE': 'docs/UNIFIED_ZION_CORE_IMPLEMENTATION.md',
        'UNIFIED_CONTAINER_IMPLEMENTATION': 'docs/UNIFIED_CONTAINER_IMPLEMENTATION_LOG_2025-09-30.md',
        'MOCKUP_ELIMINATION_COMPLETE': 'docs/MOCKUP_ELIMINATION_COMPLETE_LOG_2025-09-30.md',
        'PHASE3_COMPLETION_REPORT': 'docs/PHASE3_COMPLETION_REPORT_2025-09-30.md',
        'MIGRATION_PHASE3_REAL_DATA': 'docs/MIGRATION_PHASE3_REAL_DATA_LOG_2025-09-30.md',
        'MULTI_CHAIN_IMPLEMENTATION_COMPLETE': 'docs/MULTI_CHAIN_IMPLEMENTATION_COMPLETE_LOG_2025-09-30.md',

        // === SESSION LOGS ===
        'SESSION_LOG_2025-09-26': 'docs/SESSION_LOG_2025-09-26.md',
        'DAILY_SESSION_LOG_2025-09-26': 'docs/DAILY_SESSION_LOG_2025-09-26.md',
        'DAILY_SESSION_LOG_2025-09-29': 'docs/DAILY_SESSION_LOG_2025-09-29.md',
        'DAILY_SESSION_LOG_2025-09-30': 'docs/DAILY_SESSION_LOG_2025-09-30.md',
        'SESSION_SUMMARY_2025-10-02': 'docs/SESSION_SUMMARY_2025-10-02.md',
        'OPERATIONAL_REPORT_2025-10-24': 'docs/OPERATIONAL_REPORT_2025-10-24.md',
        'ZION_BOOTSTRAP_SUCCESS': 'docs/ZION_BOOTSTRAP_SUCCESS_2025-09-27.md',
        'ZION_MINING_CURRENT_STATUS': 'docs/ZION_MINING_CURRENT_STATUS_2025-09-27.md',

        // === SPECIAL SYSTEMS ===
        'GOLDEN_EGG_GAME': 'docs/GOLDEN_EGG_GAME/',
        'SACRED_TRINITY': 'docs/SACRED_TRINITY/',
        'SACRED_KNOWLEDGE': 'docs/SACRED_KNOWLEDGE/',
        'HUMANITARIAN_TITHE': 'docs/HUMANITARIAN_TITHE/',
        'AMENTI_LOG_INDEX': 'docs/AMENTI_LOG_INDEX.md',

        // === PROJECT STRUCTURE ===
        'PROJECT_STRUCTURE': 'src/README.md',
        'PROJECT_LOG': 'docs/PROJECT_LOG.md',
        'BRANDING': 'docs/BRANDING.md',
        'PUSH_DEPLOYMENT_GUIDE': 'docs/PUSH_DEPLOYMENT_GUIDE.md',
        'SUCCESSION_PROTOCOL': 'docs/SUCCESSION_PROTOCOL.md'
    };

    // ===============================
    // SACRED BOOKS CONTENT
    // ===============================

    const sacredBooksContent = {
        'smaragdove-desky': `# Smaragdové Desky (Emerald Tablets)

## Thothovy Zákony

*"Jak nahoře, tak dole. Jak uvnitř, tak vně."*

### Klíčové principy:

1. **Vědomí je základ všeho** - Myšlenka předchází formu
2. **Vibrace a frekvence** - Všechno je energie v pohybu
3. **Zákon přitažlivosti** - Podobné přitahuje podobné
4. **Karma a reinkarnace** - Co zasadíš, to sklidíš
5. **Sacred geometry** - Matematika vesmíru

### Zlaté pravidlo:
*"Neubližuj nikomu, ani slovem, ani myšlenkou, ani skutkem."*

---

*"Já jsem Thoth, zapisovatel pravdy. Přišel jsem z Atlantidy, abych zachoval moudrost pro budoucí generace."*`,

        'trinity-one-love': `# Trinity One Love

## Poselství jednoty

*"Láska je největší síla ve vesmíru. Spojuje všechno v harmonii."*

### Tři pilíře jednoty:

1. **Láska k sobě** - Základ všeho
2. **Láska k druhým** - Rozšíření vědomí
3. **Láska k vesmíru** - Kosmické spojení

### Zákony Trinity:

- **Zákon zrcadla** - Co vidíš venku, je uvnitř tebe
- **Zákon přijetí** - Všechno je přijatelné
- **Zákon odpuštění** - Uvolnění karmy

---

*"Když miluješ sebe, miluješ všechno. Když miluješ všechno, jsi všechno."*`,

        'starobyly-sip': `# Starožitný Šíp

## Cesta válečníka světla

*"Šíp pravdy proráží temnotu ignorance."*

### Cesta válečníka:

1. **Sebeuvědomění** - Poznej sám sebe
2. **Očista** - Zbav se iluzí
3. **Transformace** - Staň se světlem
4. **Služba** - Pomáhej druhým

### Zbraně světla:

- **Moudrost** - Poznání pravdy
- **Láska** - Síla spojení
- **Vůle** - Schopnost jednat
- **Víra** - Důvěra v božské

---

*"Válečník světla není ten, kdo nikdy nepadne, ale ten, kdo vždy vstane."*`,

        'tajemstvi-amenti': `# Tajemství Amenti

## Brány věčnosti

*"Za sedmi branami leží tajemství věčného života."*

### Sedm bran Amenti:

1. **Brána země** - Fyzické tělo
2. **Brána vody** - Emoce a city
3. **Brána ohně** - Vůle a akce
4. **Brána vzduchu** - Myšlenky a ideje
5. **Brána éteru** - Duše a duch
6. **Brána času** - Minulost a budoucnost
7. **Brána věčnosti** - Jednota se vším

### Klíče k branám:

- **Láska** - Otevírá všechny brány
- **Moudrost** - Zná tajemství bran
- **Síla** - Má odvahu projít
- **Víra** - Věří v cestu

---

*"Amenti není místo, ale stav vědomí. Věčná blaženost v jednotě se vším."*`,

        'dohrmanovo-proroctvi': `# Dohrmanovo Proroctví

## Poselství z budoucnosti

*"Budoucnost je napsána v hvězdách, ale můžeme ji změnit svými činy."*

### Proroctví pro 21. století:

1. **Velká změna** - Transformace společnosti
2. **Probouzení** - Masové vědomí
3. **Technologie a duchovno** - Spojení vědy a moudrosti
4. **Nový svět** - Zrození zlatého věku

### Klíčové předpovědi:

- **2025-2030**: Globální změny a probuzení
- **2030-2040**: Nové technologie a vědomí
- **2040-2050**: Zlatý věk lidstva
- **2050+**: Kosmické spojení

### Poselství naděje:

*"I když temnota vypadá silná, světlo uvnitř vás je silnější. Vy jste tvůrci své budoucnosti."*

---

*"Proroctví není osud, ale mapa možností. Vy rozhodujete, kterou cestu zvolíte."*`
    };

    // ===============================
    // WIKI ENGINE CLASS
    // ===============================

    class ZionWikiEngine {
        constructor() {
            this.currentCategory = 'pool-live';
            this.currentPage = null;
            this.searchIndex = {};
            this.init();
        }

        init() {
            this.setupEventListeners();
            this.buildSearchIndex();
            this.loadHomePage();
            console.log('🕉️ ZION Wiki Engine v2.8.2 initialized');
        }

        setupEventListeners() {
            // Category navigation
            document.querySelectorAll('.category-title').forEach(title => {
                title.addEventListener('click', (e) => {
                    const category = e.currentTarget.dataset.category;
                    this.switchCategory(category);
                });
            });

            // Document links
            document.addEventListener('click', (e) => {
                if (e.target.closest('[data-doc]')) {
                    e.preventDefault();
                    const docKey = e.target.closest('[data-doc]').dataset.doc;
                    this.loadDocument(docKey);
                }
            });

            // Sacred books
            document.addEventListener('click', (e) => {
                if (e.target.closest('[data-book]')) {
                    e.preventDefault();
                    const bookKey = e.target.closest('[data-book]').dataset.book;
                    this.loadSacredBook(bookKey);
                }
            });

            // Search functionality
            const searchBtn = document.getElementById('search-btn');
            const searchInput = document.getElementById('wiki-search');

            if (searchBtn && searchInput) {
                searchBtn.addEventListener('click', () => this.performSearch(searchInput.value));
                searchInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') this.performSearch(searchInput.value);
                });
            }
        }

        switchCategory(category) {
            // Update active category
            document.querySelectorAll('.category-title').forEach(title => {
                title.classList.remove('active');
            });
            document.querySelector(`[data-category="${category}"]`).classList.add('active');

            // Show/hide category lists
            document.querySelectorAll('.category-items').forEach(list => {
                list.style.display = 'none';
            });
            const activeList = document.getElementById(`${category}-list`);
            if (activeList) {
                activeList.style.display = 'block';
            }

            // Update breadcrumbs
            this.updateBreadcrumbs(category, null);
            this.currentCategory = category;
            this.currentPage = null;

            // Load category home page
            this.loadCategoryPage(category);
        }

        loadCategoryPage(category) {
            const article = document.getElementById('wiki-article');
            if (!article) return;

            let content = '';

            switch(category) {
                case 'pool-live':
                    content = this.generatePoolDashboard();
                    break;
                case 'mining':
                    content = this.generateMiningGuide();
                    break;
                case 'multi-pool':
                    content = this.generateMultiPoolGuide();
                    break;
                case 'roadmap':
                    content = this.generateRoadmapOverview();
                    break;
                case 'technical':
                    content = this.generateTechnicalOverview();
                    break;
                case 'development':
                    content = this.generateDevelopmentGuide();
                    break;
                case 'consciousness':
                    content = this.generateConsciousnessGuide();
                    break;
                case 'sacred-books':
                    content = this.generateSacredBooksOverview();
                    break;
                default:
                    content = this.generateHomePage();
            }

            article.innerHTML = content;
            this.updateTableOfContents(content);
        }

        generatePoolDashboard() {
            return `
                <h1>🔴 Live Pool Dashboard</h1>
                <p class="page-subtitle">Real-time ZION mining pool statistics and monitoring</p>

                <div class="pool-stats-grid">
                    <div class="stat-card">
                        <div class="stat-value" id="pool-hashrate">Loading...</div>
                        <div class="stat-label">Pool Hashrate</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="active-miners">--</div>
                        <div class="stat-label">Active Miners</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="blocks-found">--</div>
                        <div class="stat-label">Blocks Found (24h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="network-difficulty">--</div>
                        <div class="stat-label">Network Difficulty</div>
                    </div>
                </div>

                <h2>📡 Real-time Events</h2>
                <div class="event-feed" id="event-feed">
                    <div class="event-item">
                        <span style="color: var(--text-muted);">Connecting to pool events...</span>
                    </div>
                </div>

                <h2>⛏️ Pool Features</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3>🔄 Multi-Pool Orchestration</h3>
                        <p>AI-powered pool switching across multiple mining pools for optimal profitability</p>
                    </div>
                    <div class="feature-card">
                        <h3>💰 Automated Payments</h3>
                        <p>Hourly payouts with PPLNS reward calculation and minimum payout thresholds</p>
                    </div>
                    <div class="feature-card">
                        <h3>📊 Real-time Monitoring</h3>
                        <p>Live hashrate tracking, miner statistics, and block notifications</p>
                    </div>
                    <div class="feature-card">
                        <h3>🧘 Consciousness Mining</h3>
                        <p>Earn bonus rewards through meditation and consciousness level progression</p>
                    </div>
                </div>
            `;
        }

        generateMiningGuide() {
            return `
                <h1>⛏️ ZION Mining Guide</h1>
                <p class="page-subtitle">Complete guide to mining ZION with Cosmic Harmony algorithm</p>

                <h2>🚀 Quick Start</h2>
                <div class="quick-start">
                    <h3>Requirements:</h3>
                    <ul>
                        <li>CPU or GPU mining hardware</li>
                        <li>Stable internet connection</li>
                        <li>ZION wallet address</li>
                    </ul>

                    <h3>Pool Connection:</h3>
                    <code>pool.zion-blockchain.org:3336</code>
                </div>

                <h2>💻 CPU Mining (XMRig)</h2>
                <div class="code-block">
                    <pre><code>./xmrig -o pool.zion-blockchain.org:3336 -u YOUR_WALLET_ADDRESS -p x</code></pre>
                </div>

                <h2>🎮 GPU Mining (SRBMiner)</h2>
                <div class="code-block">
                    <pre><code>SRBMiner-MULTI.exe --algorithm cosmic-harmony --pool pool.zion-blockchain.org:3336 --wallet YOUR_WALLET_ADDRESS</code></pre>
                </div>

                <h2>🎨 Cosmic Harmony Algorithm</h2>
                <p>The native ZION mining algorithm combines:</p>
                <ul>
                    <li><strong>Sacred Mathematics</strong> - Fibonacci, Golden Ratio, Sacred Geometry</li>
                    <li><strong>Cryptographic Security</strong> - Military-grade encryption</li>
                    <li><strong>Consciousness Integration</strong> - Meditation-based reward bonuses</li>
                    <li><strong>Energy Alignment</strong> - Harmonic frequency optimization</li>
                </ul>

                <h2>🧘 Consciousness Mining</h2>
                <p>Earn additional rewards through consciousness development:</p>
                <ul>
                    <li><strong>L1-L3:</strong> Basic mining rewards</li>
                    <li><strong>L4-L6:</strong> +10% bonus through meditation</li>
                    <li><strong>L7-L9:</strong> +25% bonus + special achievements</li>
                </ul>
            `;
        }

        generateMultiPoolGuide() {
            return `
                <h1>🔄 Multi-Pool Orchestration System</h1>
                <p class="page-subtitle">AI-powered mining across multiple pools for maximum profitability</p>

                <h2>🎯 How It Works</h2>
                <p>The ZION Multi-Pool Orchestrator automatically:</p>
                <ul>
                    <li>Monitors profitability across 50+ mining pools</li>
                    <li>Switches algorithms based on market conditions</li>
                    <li>Balances load across geographic regions</li>
                    <li>Optimizes for both profitability and network health</li>
                </ul>

                <h2>🤖 AI Optimization</h2>
                <p>Machine learning algorithms analyze:</p>
                <ul>
                    <li>Real-time exchange rates</li>
                    <li>Network difficulty changes</li>
                    <li>Pool fees and reliability</li>
                    <li>Geographic latency optimization</li>
                </ul>

                <h2>🌍 Geographic Load Balancing</h2>
                <p>Distributed mining across:</p>
                <ul>
                    <li>North America (East/West)</li>
                    <li>Europe (Central/Eastern)</li>
                    <li>Asia Pacific (Singapore/Tokyo)</li>
                    <li>South America (São Paulo)</li>
                </ul>

                <h2>📊 Performance Monitoring</h2>
                <p>Real-time dashboards show:</p>
                <ul>
                    <li>Current pool profitability</li>
                    <li>Switching history and reasoning</li>
                    <li>Geographic distribution stats</li>
                    <li>Overall system efficiency</li>
                </ul>
            `;
        }

        generateRoadmapOverview() {
            return `
                <h1>🗺️ ZION 2025-2030 Roadmap</h1>
                <p class="page-subtitle">Complete development plan for the next 5 years</p>

                <h2>📅 Q4 2025 (Current Phase)</h2>
                <ul>
                    <li>✅ Multi-Pool Orchestration System</li>
                    <li>✅ Consciousness Mining v2.0</li>
                    <li>✅ Real-time WebSocket Events</li>
                    <li>🔄 Mainnet Preparation</li>
                </ul>

                <h2>🎯 2026 Milestones</h2>
                <ul>
                    <li>Mainnet Launch (Q1)</li>
                    <li>DAO Governance Implementation</li>
                    <li>Multi-Chain Bridge Development</li>
                    <li>Global Mining Pool Network</li>
                </ul>

                <h2>🚀 Mainnet 2027</h2>
                <ul>
                    <li>Full Mainnet Deployment</li>
                    <li>Exchange Listings</li>
                    <li>Staking and Governance</li>
                    <li>Enterprise Solutions</li>
                </ul>

                <h2>🌟 2028-2030 Vision</h2>
                <ul>
                    <li>Interplanetary Mining Network</li>
                    <li>AI Consciousness Integration</li>
                    <li>Global Financial System</li>
                    <li>Universal Basic Income</li>
                </ul>
            `;
        }

        generateTechnicalOverview() {
            return `
                <h1>⚙️ Technical Documentation</h1>
                <p class="page-subtitle">Complete technical specifications and implementation details</p>

                <h2>📋 Blockchain Specifications</h2>
                <div class="specs-grid">
                    <div class="spec-item">
                        <strong>Algorithm:</strong> Cosmic Harmony
                    </div>
                    <div class="spec-item">
                        <strong>Block Time:</strong> 60 seconds
                    </div>
                    <div class="spec-item">
                        <strong>Block Reward:</strong> 5,479.45 ZION
                    </div>
                    <div class="spec-item">
                        <strong>Total Supply:</strong> 144 Billion ZION
                    </div>
                    <div class="spec-item">
                        <strong>Halving:</strong> Every 4 years
                    </div>
                    <div class="spec-item">
                        <strong>Difficulty:</strong> Dynamic adjustment
                    </div>
                </div>

                <h2>🎨 Cosmic Harmony Algorithm</h2>
                <p>A revolutionary mining algorithm that combines:</p>
                <ul>
                    <li><strong>Sacred Mathematics</strong> - Fibonacci, Golden Ratio, Sacred Geometry</li>
                    <li><strong>Cryptographic Security</strong> - Military-grade encryption</li>
                    <li><strong>Consciousness Integration</strong> - Meditation-based reward bonuses</li>
                    <li><strong>Energy Alignment</strong> - Harmonic frequency optimization</li>
                </ul>

                <h2>📡 WebSocket API</h2>
                <p>Real-time communication protocol for:</p>
                <ul>
                    <li>Live pool statistics</li>
                    <li>Block notifications</li>
                    <li>Miner status updates</li>
                    <li>Payment confirmations</li>
                </ul>

                <h2>💰 Payment System</h2>
                <p>Automated reward distribution:</p>
                <ul>
                    <li><strong>PPLNS</strong> - Pay Per Last N Shares</li>
                    <li><strong>Hourly Payouts</strong> - Regular reward distribution</li>
                    <li><strong>Minimum Threshold</strong> - 0.01 ZION</li>
                    <li><strong>Transaction Fees</strong> - Network optimized</li>
                </ul>
            `;
        }

        generateDevelopmentGuide() {
            return `
                <h1>💻 Development Guide</h1>
                <p class="page-subtitle">Complete development environment and contribution guidelines</p>

                <h2>📁 Project Structure</h2>
                <div class="project-structure">
                    <pre><code>ZION-2.8/
├── ai/                    # AI Orchestration System
├── api/                   # REST API Endpoints
├── assets/               # Static Assets
├── core/                 # Core Blockchain Logic
├── docs/                 # Documentation
├── website/              # Web Interface
├── ai_orchestrator_backend.py
├── blockchain_rpc_client.py
├── consciousness_mining_game.py
├── new_zion_blockchain.py
└── zion_universal_pool_v2.py</code></pre>
                </div>

                <h2>🏠 Local Setup</h2>
                <div class="setup-steps">
                    <h3>1. Clone Repository</h3>
                    <code>git clone https://github.com/estrelaisabellazion3/Zion-2.8.git</code>

                    <h3>2. Install Dependencies</h3>
                    <code>pip install -r requirements.txt</code>

                    <h3>3. Run Local Node</h3>
                    <code>python run_blockchain_simple.py</code>

                    <h3>4. Start Mining Pool</h3>
                    <code>python run_pool_simple.py</code>
                </div>

                <h2>🧪 Testing Suite</h2>
                <p>Comprehensive testing framework:</p>
                <ul>
                    <li><strong>Unit Tests</strong> - Core functionality</li>
                    <li><strong>Integration Tests</strong> - System components</li>
                    <li><strong>Performance Tests</strong> - Mining algorithms</li>
                    <li><strong>Security Tests</strong> - Cryptographic validation</li>
                </ul>

                <h2>⚡ Benchmarking Tools</h2>
                <p>Performance optimization utilities:</p>
                <ul>
                    <li><strong>Hashrate Testing</strong> - Algorithm performance</li>
                    <li><strong>Memory Usage</strong> - Resource optimization</li>
                    <li><strong>Network Latency</strong> - Connection quality</li>
                    <li><strong>Energy Efficiency</strong> - Power consumption analysis</li>
                </ul>
            `;
        }

        generateConsciousnessGuide() {
            return `
                <h1>🧘 Consciousness Mining System</h1>
                <p class="page-subtitle">Spiritual development integrated with cryptocurrency mining</p>

                <h2>🧘 Consciousness Levels (L1-L9)</h2>
                <div class="levels-grid">
                    <div class="level-card">
                        <h3>L1-L3: Awakening</h3>
                        <p>Basic consciousness. Standard mining rewards.</p>
                        <div class="level-bonus">Base Rewards</div>
                    </div>
                    <div class="level-card">
                        <h3>L4-L6: Growth</h3>
                        <p>Developing awareness. Meditation unlocks bonuses.</p>
                        <div class="level-bonus">+10% Bonus</div>
                    </div>
                    <div class="level-card">
                        <h3>L7-L9: Mastery</h3>
                        <p>Advanced consciousness. Full spiritual integration.</p>
                        <div class="level-bonus">+25% Bonus + Achievements</div>
                    </div>
                </div>

                <h2>📈 XP Progression</h2>
                <p>Earn experience points through:</p>
                <ul>
                    <li><strong>Mining Activity</strong> - Base XP from hashrate</li>
                    <li><strong>Meditation Sessions</strong> - Bonus XP for mindfulness</li>
                    <li><strong>Community Participation</strong> - Social XP rewards</li>
                    <li><strong>Achievements</strong> - Special milestone bonuses</li>
                </ul>

                <h2>🥚 Golden Egg Quest</h2>
                <p>The ultimate consciousness achievement:</p>
                <ul>
                    <li><strong>Requirements:</strong> Reach L9 consciousness</li>
                    <li><strong>Challenge:</strong> 1000+ hours of meditation mining</li>
                    <li><strong>Reward:</strong> Legendary Golden Egg NFT</li>
                    <li><strong>Benefits:</strong> Permanent +50% mining bonus</li>
                </ul>

                <h2>🏆 Achievements</h2>
                <div class="achievements-grid">
                    <div class="achievement">
                        <strong>🧘 First Meditation</strong><br>
                        Complete your first meditation session
                    </div>
                    <div class="achievement">
                        <strong>⚡ Hashrate Master</strong><br>
                        Maintain 1 MH/s for 24 hours
                    </div>
                    <div class="achievement">
                        <strong>🌟 Consciousness Pioneer</strong><br>
                        Reach Level 5 consciousness
                    </div>
                    <div class="achievement">
                        <strong>👑 Golden Egg Hunter</strong><br>
                        Complete the Golden Egg Quest
                    </div>
                </div>

                <h2>🧘 Meditation Bonus</h2>
                <p>Enhanced rewards through mindfulness:</p>
                <ul>
                    <li><strong>Session Duration:</strong> 10-60 minutes</li>
                    <li><strong>Bonus Multiplier:</strong> Up to 2x rewards</li>
                    <li><strong>Consciousness Growth:</strong> Accelerated XP gain</li>
                    <li><strong>Energy Alignment:</strong> Harmonic mining optimization</li>
                </ul>
            `;
        }

        generateSacredBooksOverview() {
            return `
                <h1>📚 Sacred Books Library</h1>
                <p class="page-subtitle">Ancient wisdom and spiritual teachings for conscious evolution</p>

                <div class="sacred-books-grid">
                    <div class="sacred-book-card" onclick="loadSacredBook('smaragdove-desky')">
                        <div class="book-icon">📖</div>
                        <h3>Smaragdové Desky</h3>
                        <p>Thothovy zákony z Atlantidy. Základní principy vesmíru a vědomí.</p>
                        <div class="book-author">Thoth (Atlantida)</div>
                    </div>

                    <div class="sacred-book-card" onclick="loadSacredBook('trinity-one-love')">
                        <div class="book-icon">📖</div>
                        <h3>Trinity One Love</h3>
                        <p>Poselství jednoty a lásky. Spojení s kosmickým vědomím.</p>
                        <div class="book-author">Trinity Consciousness</div>
                    </div>

                    <div class="sacred-book-card" onclick="loadSacredBook('starobyly-sip')">
                        <div class="book-icon">📖</div>
                        <h3>Starožitný Šíp</h3>
                        <p>Cesta válečníka světla. Transformace a služba lidstvu.</p>
                        <div class="book-author">Ancient Warrior Wisdom</div>
                    </div>

                    <div class="sacred-book-card" onclick="loadSacredBook('tajemstvi-amenti')">
                        <div class="book-icon">📖</div>
                        <h3>Tajemství Amenti</h3>
                        <p>Brány věčnosti a tajemství posmrtného života.</p>
                        <div class="book-author">Egyptske Mysterie</div>
                    </div>

                    <div class="sacred-book-card" onclick="loadSacredBook('dohrmanovo-proroctvi')">
                        <div class="book-icon">📖</div>
                        <h3>Dohrmanovo Proroctví</h3>
                        <p>Poselství z budoucnosti. Průvodce zlatým věkem.</p>
                        <div class="book-author">Dohrman (2030+)</div>
                    </div>
                </div>

                <div class="sacred-quote">
                    <blockquote>
                        "Knihy jsou mosty mezi světy. Spojují minulost s budoucností a umožňují nám porozumět našemu místu ve vesmíru."
                        <cite>— ZION Sacred Library</cite>
                    </blockquote>
                </div>
            `;
        }

        loadDocument(docKey) {
            const article = document.getElementById('wiki-article');
            if (!article) return;

            const docPath = window.docsMapping[docKey];
            if (!docPath) {
                article.innerHTML = `<div style="text-align: center; padding: 3rem; color: var(--text-muted);">
                    <p>📄 Document not found: ${docKey}</p>
                </div>`;
                return;
            }

            article.innerHTML = `<div style="text-align: center; padding: 3rem; color: var(--matrix-green);">
                <p>📄 Loading: ${docKey}...</p>
            </div>`;

            // Load document content
            fetch(`../${docPath}`)
                .then(response => response.text())
                .then(content => {
                    if (docPath.endsWith('.md')) {
                        article.innerHTML = this.renderMarkdownContent(content);
                    } else {
                        article.innerHTML = `<pre style="white-space: pre-wrap; font-family: 'Share Tech Mono', monospace;">${content}</pre>`;
                    }
                    this.updateTableOfContents(content);
                })
                .catch(error => {
                    console.error('Error loading document:', error);
                    article.innerHTML = `<div style="padding: 2rem; color: var(--text-muted);">
                        <p>📚 ${docKey}</p>
                        <p>Content from: ${docPath}</p>
                    </div>`;
                });

            this.updateBreadcrumbs(this.currentCategory, docKey);
            this.currentPage = docKey;
        }

        loadSacredBook(bookKey) {
            const article = document.getElementById('wiki-article');
            if (!article) return;

            const content = sacredBooksContent[bookKey];
            if (!content) {
                article.innerHTML = `<div style="text-align: center; padding: 3rem; color: var(--text-muted);">
                    <p>📖 Sacred book not found: ${bookKey}</p>
                </div>`;
                return;
            }

            article.innerHTML = this.renderMarkdownContent(content);
            this.updateTableOfContents(content);
            this.updateBreadcrumbs('sacred-books', bookKey);
            this.currentCategory = 'sacred-books';
            this.currentPage = bookKey;
        }

        renderMarkdownContent(md) {
            let html = md
                .replace(/^# (.+)$/gm, '<h1>$1</h1>')
                .replace(/^## (.+)$/gm, '<h2>$1</h2>')
                .replace(/^### (.+)$/gm, '<h3>$1</h3>')
                .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.+?)\*/g, '<em>$1</em>')
                .replace(/`([^`]+)`/g, '<code>$1</code>')
                .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank">$1</a>')
                .replace(/^- (.+)$/gm, '<li>$1</li>')
                .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

            return `<div class="markdown-content">${html}</div>`;
        }

        updateBreadcrumbs(category, page) {
            const crumbCategory = document.getElementById('current-category');
            const crumbPage = document.getElementById('current-page');
            const separator = document.getElementById('page-separator');

            if (crumbCategory) {
                crumbCategory.textContent = this.getCategoryDisplayName(category);
            }

            if (crumbPage && separator) {
                if (page) {
                    crumbPage.textContent = page.replace(/_/g, ' ');
                    crumbPage.style.display = 'inline';
                    separator.style.display = 'inline';
                } else {
                    crumbPage.style.display = 'none';
                    separator.style.display = 'none';
                }
            }
        }

        getCategoryDisplayName(category) {
            const names = {
                'pool-live': 'Live Pool Stats',
                'mining': 'Mining Guides',
                'multi-pool': 'Multi-Pool System',
                'roadmap': 'Roadmap 2025-2030',
                'technical': 'Technical Docs',
                'development': 'Development',
                'consciousness': 'Consciousness System',
                'sacred-books': 'Sacred Books'
            };
            return names[category] || category;
        }

        updateTableOfContents(content) {
            const tocNav = document.getElementById('toc-nav');
            if (!tocNav) return;

            // Extract headings from content
            const headings = content.match(/^#{1,3} .+$/gm) || [];
            const tocItems = headings.map(heading => {
                const level = heading.match(/^#+/)[0].length;
                const text = heading.replace(/^#+\s/, '');
                const id = text.toLowerCase().replace(/[^a-z0-9]+/g, '-');
                return `<a href="#${id}" style="padding-left: ${level * 8}px;">${'  '.repeat(level - 1)}${text}</a>`;
            }).join('');

            tocNav.innerHTML = tocItems || '<a href="#top">Top</a>';
        }

        buildSearchIndex() {
            // Build search index from all available content
            this.searchIndex = {
                'pool dashboard': { type: 'page', category: 'pool-live' },
                'live stats': { type: 'page', category: 'pool-live' },
                'mining guide': { type: 'page', category: 'mining' },
                'cpu mining': { type: 'section', category: 'mining', section: 'cpu-mining' },
                'gpu mining': { type: 'section', category: 'mining', section: 'gpu-mining' },
                'cosmic harmony': { type: 'section', category: 'mining', section: 'cosmic-harmony' },
                'multi-pool': { type: 'page', category: 'multi-pool' },
                'orchestration': { type: 'doc', key: 'MULTI_POOL_ORCHESTRATION_README' },
                'roadmap': { type: 'page', category: 'roadmap' },
                '2025': { type: 'section', category: 'roadmap', section: 'q4-2025' },
                '2026': { type: 'section', category: 'roadmap', section: '2026-milestones' },
                'mainnet': { type: 'section', category: 'roadmap', section: 'mainnet-2027' },
                'technical': { type: 'page', category: 'technical' },
                'blockchain specs': { type: 'section', category: 'technical', section: 'blockchain-specs' },
                'websocket api': { type: 'section', category: 'technical', section: 'websocket-api' },
                'payment system': { type: 'section', category: 'technical', section: 'payment-system' },
                'development': { type: 'page', category: 'development' },
                'project structure': { type: 'section', category: 'development', section: 'project-structure' },
                'local setup': { type: 'section', category: 'development', section: 'local-setup' },
                'consciousness': { type: 'page', category: 'consciousness' },
                'levels': { type: 'section', category: 'consciousness', section: 'level-system' },
                'xp progression': { type: 'section', category: 'consciousness', section: 'xp-progression' },
                'golden egg': { type: 'section', category: 'consciousness', section: 'golden-egg' },
                'sacred books': { type: 'page', category: 'sacred-books' },
                'smaragdove desky': { type: 'book', key: 'smaragdove-desky' },
                'thoth': { type: 'book', key: 'smaragdove-desky' },
                'trinity': { type: 'book', key: 'trinity-one-love' },
                'starozytny sip': { type: 'book', key: 'starobyly-sip' },
                'amenti': { type: 'book', key: 'tajemstvi-amenti' },
                'dohrman': { type: 'book', key: 'dohrmanovo-proroctvi' }
            };
        }

        performSearch(query) {
            if (!query.trim()) return;

            const results = [];
            const searchTerm = query.toLowerCase();

            // Search through index
            for (const [key, value] of Object.entries(this.searchIndex)) {
                if (key.includes(searchTerm)) {
                    results.push({ term: key, ...value });
                }
            }

            // Display results
            const article = document.getElementById('wiki-article');
            if (!article) return;

            if (results.length === 0) {
                article.innerHTML = `<div style="text-align: center; padding: 3rem; color: var(--text-muted);">
                    <p>🔍 No results found for: "${query}"</p>
                    <p>Try searching for: mining, consciousness, roadmap, technical, sacred books</p>
                </div>`;
                return;
            }

            let resultsHtml = `<h1>🔍 Search Results</h1><p class="page-subtitle">Found ${results.length} results for "${query}"</p><div class="search-results">`;

            results.forEach(result => {
                const icon = result.type === 'book' ? '📖' : result.type === 'doc' ? '📄' : '📋';
                const link = result.type === 'book' ? `javascript:loadSacredBook('${result.key}')` :
                            result.type === 'doc' ? `javascript:loadDocument('${result.key}')` :
                            `javascript:switchCategory('${result.category}')`;

                resultsHtml += `
                    <div class="search-result-item" onclick="${link}">
                        <div class="result-icon">${icon}</div>
                        <div class="result-content">
                            <h3>${result.term}</h3>
                            <p>${result.type} • ${this.getCategoryDisplayName(result.category)}</p>
                        </div>
                    </div>
                `;
            });

            resultsHtml += '</div>';
            article.innerHTML = resultsHtml;
        }

        loadHomePage() {
            this.loadCategoryPage('pool-live');
        }
    }

    // ===============================
    // GLOBAL FUNCTIONS
    // ===============================

    function loadSacredBook(bookKey) {
        if (window.wikiEngine) {
            window.wikiEngine.loadSacredBook(bookKey);
        }
    }

    function loadDocument(docKey) {
        if (window.wikiEngine) {
            window.wikiEngine.loadDocument(docKey);
        }
    }

    function switchCategory(category) {
        if (window.wikiEngine) {
            window.wikiEngine.switchCategory(category);
        }
    }

    // ===============================
    // INITIALIZE
    // ===============================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.wikiEngine = new ZionWikiEngine();
        });
    } else {
        window.wikiEngine = new ZionWikiEngine();
    }

})();