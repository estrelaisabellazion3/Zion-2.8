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
        'GLOBAL-DEPLOYMENT-STRATEGY': 'docs/GLOBAL-DEPLOYMENT-STRATEGY.md',
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
    // CATEGORY ORGANIZATION
    // ===============================
    
    const CATEGORIES = {
        'roadmap': {
            title: '🗺️ Roadmaps',
            docs: ['ROADMAP', 'MULTI_CHAIN_TECHNICAL_ROADMAP', 'STRATEGIC_VISION_EXPANSION', 'NEW-JERUSALEM-MASTER-PLAN', 'LIBERATION-MANIFESTO']
        },
        'mining': {
            title: '⛏️ Mining',
            docs: ['REALTIME_MINING_README', 'MULTI_ALGORITHM_MINING_GUIDE', 'AMD_RX5600_DRIVER_GUIDE', 'ZION_GPU_MINING_SETUP_GUIDE', 'YESCRYPT_CPU_OPTIMIZATION']
        },
        'deployment': {
            title: '🚀 Deployment',
            docs: ['DEPLOYMENT_GUIDE_2.8.2', 'DOCKER_WORKFLOW_GUIDE', 'LOCAL_DEPLOYMENT_SUCCESS_2025-10-24', 'GLOBAL-DEPLOYMENT-STRATEGY', 'NODE_INSTALLER']
        },
        'technical': {
            title: '⚙️ Technical',
            docs: ['CONSENSUS_PARAMS', 'ADDRESS_SPEC', 'PROJECT_ARCHITECTURE_OVERVIEW', 'UNIFIED_ZION_CORE', 'COMPLETE_WARP_INFRASTRUCTURE']
        },
        'multi-pool': {
            title: '🔄 Multi-Pool',
            docs: ['MULTI_POOL_ORCHESTRATION_README', 'BASIC_IMPROVEMENTS_IMPLEMENTED', 'MININGCORE_INTEGRATION_ANALYSIS']
        },
        'cosmos': {
            title: '✨ Cosmos',
            docs: ['COSMIC_MAP_COMPLETE', 'ESTRELLA_SOLAR_SYSTEM_COMPLETE', 'ON_THE_STAR_AI', 'DAY3_CONSCIOUSNESS_MINING', 'ZION_GALAXY_ARCHITECTURE']
        },
        'whitepaper': {
            title: '📖 Whitepapers',
            docs: ['ZION_COSMIC_DHARMA_WHITEPAPER', 'ZION_DHARMA_MULTICHAIN', 'ZION_ETHICAL_MANIFEST']
        },
        'bridges': {
            title: '🌉 Bridges',
            docs: ['MULTI_CHAIN_FUNCTIONAL_DEPLOYMENT', 'LIGHTNING_NETWORK_INTEGRATION', 'RAINBOW_BRIDGE_44_44', 'PRAGMATIC_MULTI_CHAIN']
        },
        'release': {
            title: '🎯 Release',
            docs: ['MAINNET_LAUNCH', 'RELEASE_NOTES', 'CHANGELOG', 'COMMUNITY_LAUNCH_MATERIALS']
        },
        'monitoring': {
            title: '📊 Monitoring',
            docs: ['METRICS', 'PLATFORM_AUDIT_2025-10-01', 'OPERATIONAL_REPORT_2025-10-24']
        },
        'sacred': {
            title: '✨ Sacred',
            docs: ['COSMIC_MAP_COMPLETE', 'SACRED_TRINITY', 'SACRED_KNOWLEDGE', 'AMENTI_LOG_INDEX']
        },
        'sessions': {
            title: '📋 Sessions',
            docs: ['SESSION_LOG_2025-09-26', 'DAILY_SESSION_LOG_2025-09-29', 'SESSION_SUMMARY_2025-10-02', 'OPERATIONAL_REPORT_2025-10-24']
        }
    };
    
    // ===============================
    // INITIALIZATION
    // ===============================
    
    function initializeWiki() {
        console.log('🚀 ZION Wiki Engine v2.8.2 Initialized');
        console.log('📚 Loaded', Object.keys(window.docsMapping).length, 'documentation files');
        
        setupCategoryLinks();
        setupDocumentLinks();
        setupSearch();
    }
    
    // ===============================
    // CATEGORY SETUP
    // ===============================
    
    function setupCategoryLinks() {
        document.addEventListener('click', function(e) {
            const title = e.target.closest('.category-title');
            if (!title) return;
            
            e.preventDefault();
            const categoryKey = title.dataset.category;
            if (!categoryKey) return;
            
            // Toggle list visibility
            const list = document.getElementById(categoryKey + '-list');
            if (list) {
                const isVisible = list.style.display !== 'none';
                list.style.display = isVisible ? 'none' : 'flex';
                title.classList.toggle('active');
            }
        });
    }
    
    // ===============================
    // DOCUMENT SETUP
    // ===============================
    
    function setupDocumentLinks() {
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a[data-doc]');
            if (!link) return;
            
            e.preventDefault();
            const docKey = link.dataset.doc;
            loadDocument(docKey);
        });
    }
    
    // ===============================
    // DOCUMENT LOADER
    // ===============================
    
    async function loadDocument(docKey) {
        const path = window.docsMapping[docKey];
        if (!path) {
            console.error('Document not found:', docKey);
            return;
        }
        
        const article = document.getElementById('wiki-article');
        if (!article) return;
        
        // Show loading
        article.innerHTML = `
            <div style="text-align: center; padding: 3rem; color: var(--matrix-green);">
                <p>📄 Loading: ${docKey}...</p>
            </div>
        `;
        
        try {
            const response = await fetch(`../${path}`);
            if (response.ok) {
                const content = await response.text();
                if (path.endsWith('.md')) {
                    renderMarkdown(article, content, docKey);
                } else {
                    article.textContent = content;
                }
            } else {
                renderPlaceholder(article, docKey, path);
            }
        } catch (error) {
            console.error('Error loading document:', error);
            renderPlaceholder(article, docKey, path);
        }
    }
    
    // ===============================
    // MARKDOWN RENDERER
    // ===============================
    
    function renderMarkdown(article, markdown, title) {
        let html = markdown
            .split('\n')
            .map((line, idx) => {
                // Headers
                if (line.startsWith('### ')) return `<h3>${escapeHtml(line.slice(4))}</h3>`;
                if (line.startsWith('## ')) return `<h2>${escapeHtml(line.slice(3))}</h2>`;
                if (line.startsWith('# ')) return `<h1 class="page-title">${escapeHtml(line.slice(2))}</h1>`;
                
                // Code blocks
                if (line.startsWith('```')) return `<pre><code>`;
                if (line === '```') return `</code></pre>`;
                
                // Bold and italic
                line = line
                    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\*(.+?)\*/g, '<em>$1</em>')
                    .replace(/`([^`]+)`/g, '<code class="inline">$1</code>');
                
                // Links
                line = line.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank">$1</a>');
                
                // Lists
                if (line.startsWith('* ')) return `<li>${escapeHtml(line.slice(2))}</li>`;
                if (line.startsWith('- ')) return `<li>${escapeHtml(line.slice(2))}</li>`;
                
                // Empty lines
                if (line.trim() === '') return '<br>';
                
                return `<p>${escapeHtml(line)}</p>`;
            })
            .join('\n');
        
        article.innerHTML = html;
    }
    
    function renderPlaceholder(article, docKey, path) {
        article.innerHTML = `
            <h1 class="page-title">${docKey}</h1>
            <div style="padding: 2rem; color: var(--text-muted);">
                <p>📄 Documentation file</p>
                <p style="font-family: monospace; font-size: 0.9rem;">Path: ${path}</p>
                <p style="font-size: 0.9rem; margin-top: 1rem;">
                    Content loading from repository...
                </p>
            </div>
        `;
    }
    
    // ===============================
    // SEARCH
    // ===============================
    
    function setupSearch() {
        const searchInput = document.getElementById('wiki-search');
        const searchBtn = document.getElementById('search-btn');
        
        if (!searchInput || !searchBtn) return;
        
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') performSearch();
        });
    }
    
    function performSearch() {
        const query = document.getElementById('wiki-search')?.value.toLowerCase();
        if (!query) return;
        
        console.log('🔍 Searching:', query);
        
        // Find matching docs
        const matches = [];
        
        Object.entries(window.docsMapping).forEach(([key, path]) => {
            if (key.toLowerCase().includes(query) || path.toLowerCase().includes(query)) {
                matches.push({ key, path });
            }
        });
        
        if (matches.length > 0) {
            loadDocument(matches[0].key);
            console.log(`✅ Found ${matches.length} match(es)`);
        } else {
            alert(`❌ No documents found for: "${query}"`);
        }
    }
    
    // ===============================
    // UTILITIES
    // ===============================
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // ===============================
    // INITIALIZE ON LOAD
    // ===============================
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeWiki);
    } else {
        initializeWiki();
    }
    
})();
