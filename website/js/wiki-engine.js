/**
 * ZION Wiki Engine
 * Markdown parser, navigation, search, book viewer
 */

(function() {
    
    // ===============================
    // WIKI DATA STRUCTURE
    // ===============================
    
    const wikiData = {
        'sacred-books': {
            'smaragdove-desky': {
                title: 'Smaragdové Desky',
                author: 'Thoth Atlantský',
                description: 'Starověké moudrosti od Thotha, Atlantského mistra mystérií. Obsahuje 15 desek s tajemstvími univerza, vědomí a cesty do Amenti.',
                pages: 117,
                content: null // Will be loaded from /books/SmaragdoveDesky.txt
            },
            'trinity-one-love': {
                title: 'Trinity One Love',
                author: '3NITY COMPANY',
                description: 'Book of Amenti 144k - Cesta k Jednotě, kosmická trojice jedné lásky, probuzení hvězdných dětí.',
                pages: 7,
                content: null
            },
            'starobyly-sip': {
                title: 'Starožitný Šíp',
                author: 'James Mahu (WingMakers)',
                description: 'Příběh objevu v poušti Nového Mexika, kontakt s Centrální Rasou a odhalení Svrchovaného Sjednocení.',
                pages: 23,
                content: null
            },
            'tajemstvi-amenti': {
                title: 'Tajemství Amenti',
                author: 'Ashayana Deane',
                description: 'Interpretace pravdivé historie lidstva, planety Země a vzestupného období 2000-2022. Andělské války, Záchranná mise Amenti.',
                pages: 117,
                content: null
            },
            'dohrmanovo-proroctvi': {
                title: 'Dohrmanovo Proroctví',
                author: 'Neznámý',
                description: 'Proroctví o budoucnosti lidstva a planetární transformaci.',
                pages: null,
                content: null
            }
        }
    };
    
    // ===============================
    // STATE MANAGEMENT
    // ===============================
    
    let currentCategory = 'sacred-books';
    let currentPage = null;
    
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
                
                // Update breadcrumbs
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
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const bookId = this.dataset.book;
                const href = this.getAttribute('href').substring(1); // Remove #
                
                // Update active state
                pageLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
                
                // Load content
                if (bookId) {
                    loadBook(bookId);
                } else {
                    loadPage(href);
                }
                
                // Update breadcrumbs
                currentPage = this.textContent;
                updateBreadcrumbs();
                
                // Scroll to top
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    }
    
    // ===============================
    // BREADCRUMB UPDATES
    // ===============================
    
    function updateBreadcrumbs() {
        const categoryNames = {
            'sacred-books': 'Sacred Books',
            'mining': 'Mining',
            'dao': 'DAO Governance',
            'technical': 'Technical',
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
    // BOOK LOADER
    // ===============================
    
    async function loadBook(bookId) {
        const article = document.getElementById('wiki-article');
        const book = wikiData['sacred-books'][bookId];
        
        if (!book) {
            article.innerHTML = '<h1>Book not found</h1>';
            return;
        }
        
        // Show loading state
        article.innerHTML = `
            <div class="book-header">
                <h1 class="book-title glitch" data-text="${book.title}">${book.title}</h1>
                <p class="book-author">by ${book.author}</p>
                <p class="book-description">${book.description}</p>
                <div class="book-meta">
                    ${book.pages ? `<div class="book-meta-item"><span>📄</span>${book.pages} pages</div>` : ''}
                    <div class="book-meta-item"><span>📚</span>Sacred Wisdom</div>
                    <div class="book-meta-item"><span>🔮</span>Ancient Knowledge</div>
                </div>
            </div>
            <div class="loading-spinner">
                <p style="color: var(--matrix-green); text-align: center; padding: 3rem;">
                    Loading sacred text...
                </p>
            </div>
        `;
        
        // Try to load actual book content
        try {
            const bookPath = `/books/${getBookFileName(bookId)}`;
            const response = await fetch(bookPath);
            
            if (response.ok) {
                const text = await response.text();
                renderBookContent(article, book, text);
            } else {
                renderPlaceholderContent(article, book);
            }
        } catch (error) {
            console.error('Error loading book:', error);
            renderPlaceholderContent(article, book);
        }
        
        // Generate TOC
        generateTOC();
    }
    
    function getBookFileName(bookId) {
        const fileNames = {
            'smaragdove-desky': 'SmaragdoveDesky.txt',
            'trinity-one-love': 'OmnityOneLove CZ.txt',
            'starobyly-sip': 'Starobyly_sip.txt',
            'tajemstvi-amenti': 'Tajemství amenti.txt',
            'dohrmanovo-proroctvi': 'Dohrmanovo-proroctvi.txt'
        };
        
        return fileNames[bookId] || `${bookId}.txt`;
    }
    
    function renderBookContent(article, book, rawText) {
        // Parse the text file content
        const lines = rawText.split('\n');
        let chapters = [];
        let currentChapter = null;
        
        lines.forEach(line => {
            line = line.trim();
            
            // Detect chapter headings (various formats)
            if (line.match(/^(Kapitola|KAPITOLA|Chapter|Episode|Deska|DESKA)\s+\d+/i) ||
                line.match(/^===\s*PAGE\s+\d+\s*===/i) ||
                line.match(/^[IVX]+\s*$/)) {
                
                if (currentChapter) {
                    chapters.push(currentChapter);
                }
                
                currentChapter = {
                    title: line,
                    content: []
                };
            } else if (currentChapter && line.length > 0) {
                currentChapter.content.push(line);
            }
        });
        
        if (currentChapter) {
            chapters.push(currentChapter);
        }
        
        // Render book with chapters
        let bookHTML = `
            <div class="book-header">
                <h1 class="book-title glitch" data-text="${book.title}">${book.title}</h1>
                <p class="book-author">by ${book.author}</p>
                <p class="book-description">${book.description}</p>
                <div class="book-meta">
                    ${book.pages ? `<div class="book-meta-item"><span>📄</span>${book.pages} pages</div>` : ''}
                    <div class="book-meta-item"><span>📚</span>${chapters.length} chapters</div>
                    <div class="book-meta-item"><span>🔮</span>Ancient Knowledge</div>
                </div>
            </div>
            <div class="book-content">
        `;
        
        chapters.forEach(chapter => {
            bookHTML += `
                <div class="chapter">
                    <h2 class="chapter-title">${escapeHtml(chapter.title)}</h2>
                    <div class="chapter-text">
                        ${chapter.content.map(p => `<p>${escapeHtml(p)}</p>`).join('')}
                    </div>
                </div>
            `;
        });
        
        bookHTML += '</div>';
        
        article.innerHTML = bookHTML;
    }
    
    function renderPlaceholderContent(article, book) {
        // Render placeholder when file can't be loaded
        article.innerHTML = `
            <div class="book-header">
                <h1 class="book-title glitch" data-text="${book.title}">${book.title}</h1>
                <p class="book-author">by ${book.author}</p>
                <p class="book-description">${book.description}</p>
                <div class="book-meta">
                    ${book.pages ? `<div class="book-meta-item"><span>📄</span>${book.pages} pages</div>` : ''}
                    <div class="book-meta-item"><span>📚</span>Sacred Wisdom</div>
                    <div class="book-meta-item"><span>🔮</span>Ancient Knowledge</div>
                </div>
            </div>
            <div class="book-content">
                <h2>Overview</h2>
                <p>${book.description}</p>
                
                <blockquote class="sacred-quote">
                    "The lips of wisdom are closed, except to the ears of Understanding."
                    <cite>— The Kybalion</cite>
                </blockquote>
                
                <p style="color: var(--text-muted); padding: 2rem; text-align: center;">
                    Full text content will be available soon. The sacred knowledge is being prepared for transmission.
                </p>
            </div>
        `;
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // ===============================
    // DOCUMENTATION FILE LOADER
    // ===============================
    
    async function loadDocFile(docFileName, pageId) {
        const article = document.getElementById('wiki-article');
        
        // Show loading state
        article.innerHTML = `
            <div style="padding: 3rem; text-align: center;">
                <p style="color: var(--matrix-green); font-size: 1.2rem;">
                    Loading documentation...
                </p>
            </div>
        `;
        
        try {
            const docPath = `/docs/${docFileName}.md`;
            const response = await fetch(docPath);
            
            if (!response.ok) {
                throw new Error('Doc file not found');
            }
            
            const markdown = await response.text();
            renderMarkdown(article, markdown, docFileName);
            
        } catch (error) {
            console.error('Error loading doc:', error);
            article.innerHTML = `
                <h1 class="page-title">Documentation Not Found</h1>
                <p style="color: var(--text-muted);">
                    The requested documentation file could not be loaded: <code>${docFileName}.md</code>
                </p>
                <p>Please check the navigation menu or try another page.</p>
            `;
        }
        
        generateTOC();
    }
    
    // ===============================
    // MARKDOWN RENDERER
    // ===============================
    
    function renderMarkdown(article, markdown, fileName) {
        // Simple Markdown parser
        let html = markdown;
        
        // Extract title from first # heading
        const titleMatch = html.match(/^#\s+(.+)$/m);
        const title = titleMatch ? titleMatch[1] : fileName.replace(/_/g, ' ');
        
        // Convert headers
        html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.+)$/gm, '<h1 class="page-title glitch" data-text="$1">$1</h1>');
        
        // Convert bold and italic
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
        html = html.replace(/__(.+?)__/g, '<strong>$1</strong>');
        html = html.replace(/_(.+?)_/g, '<em>$1</em>');
        
        // Convert code blocks
        html = html.replace(/```(\w+)?\n([\s\S]+?)```/g, function(match, lang, code) {
            return `<pre><code class="language-${lang || 'text'}">${escapeHtml(code.trim())}</code></pre>`;
        });
        
        // Convert inline code
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Convert links
        html = html.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>');
        
        // Convert lists
        html = html.replace(/^\* (.+)$/gm, '<li>$1</li>');
        html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
        html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
        
        // Wrap consecutive <li> in <ul>
        html = html.replace(/(<li>.+<\/li>\n?)+/g, function(match) {
            return '<ul>' + match + '</ul>';
        });
        
        // Convert blockquotes
        html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');
        
        // Convert horizontal rules
        html = html.replace(/^---$/gm, '<hr>');
        html = html.replace(/^\*\*\*$/gm, '<hr>');
        
        // Convert paragraphs (anything not already in a tag)
        const lines = html.split('\n');
        const processed = [];
        let inBlock = false;
        
        for (let line of lines) {
            line = line.trim();
            
            if (!line) {
                inBlock = false;
                processed.push('');
                continue;
            }
            
            // Check if line is already in a tag
            if (line.match(/^<(h[1-6]|ul|ol|li|pre|code|blockquote|hr|div)/)) {
                inBlock = false;
                processed.push(line);
            } else if (line.match(/<\/(h[1-6]|ul|ol|pre|code|blockquote|div)>$/)) {
                processed.push(line);
                inBlock = false;
            } else if (!inBlock && !line.match(/^</)) {
                processed.push('<p>' + line);
                inBlock = true;
            } else if (inBlock) {
                processed.push(line + '</p>');
                inBlock = false;
            } else {
                processed.push(line);
            }
        }
        
        html = processed.join('\n');
        
        // Clean up extra paragraph tags
        html = html.replace(/<p>\s*<(h[1-6]|ul|ol|blockquote|pre)/g, '<$1');
        html = html.replace(/<\/(h[1-6]|ul|ol|blockquote|pre)>\s*<\/p>/g, '</$1>');
        
        article.innerHTML = html;
    }
    
    // ===============================
    // GENERAL PAGE LOADER
    // ===============================
    
    async function loadPage(pageId) {
        const article = document.getElementById('wiki-article');
        
        // Check if it's a doc file
        const link = document.querySelector(`a[href="#${pageId}"]`);
        const docFile = link ? link.dataset.doc : null;
        
        if (docFile) {
            await loadDocFile(docFile, pageId);
            return;
        }
        
        // Page content templates
        const pages = {
            'cpu-mining': {
                title: 'CPU Mining with XMRig',
                content: `
                    <h2>Getting Started with CPU Mining</h2>
                    <p>XMRig is the recommended CPU miner for ZION blockchain. It supports Yescrypt algorithm with high efficiency.</p>
                    
                    <h3>Installation</h3>
                    <pre><code># Download XMRig
wget https://github.com/xmrig/xmrig/releases/download/v6.21.0/xmrig-6.21.0-linux-x64.tar.gz
tar xvf xmrig-6.21.0-linux-x64.tar.gz
cd xmrig-6.21.0</code></pre>
                    
                    <h3>Configuration</h3>
                    <p>Create <code>config.json</code> with your mining settings:</p>
                    <pre><code>{
    "url": "pool.zion-blockchain.org:3336",
    "user": "YOUR_ZION_ADDRESS",
    "pass": "x",
    "algo": "yescrypt",
    "threads": 4,
    "cpu-priority": 3
}</code></pre>
                    
                    <h3>Start Mining</h3>
                    <pre><code>./xmrig</code></pre>
                    
                    <h3>Expected Hashrate</h3>
                    <ul>
                        <li>Intel i5: 2-4 KH/s</li>
                        <li>Intel i7: 4-8 KH/s</li>
                        <li>AMD Ryzen 5: 3-6 KH/s</li>
                        <li>AMD Ryzen 9: 8-15 KH/s</li>
                    </ul>
                `
            },
            'blockchain-params': {
                title: 'Blockchain Parameters',
                content: `
                    <h2>ZION Blockchain Specifications</h2>
                    
                    <h3>Core Parameters</h3>
                    <table>
                        <tr><th>Parameter</th><th>Value</th></tr>
                        <tr><td>Total Supply</td><td>144,000,000,000 ZION</td></tr>
                        <tr><td>Block Time</td><td>60 seconds</td></tr>
                        <tr><td>Block Reward</td><td>5,479.45 ZION</td></tr>
                        <tr><td>Premine</td><td>14,340,000,000 ZION (9.96%)</td></tr>
                        <tr><td>Emission Period</td><td>50 years</td></tr>
                    </table>
                    
                    <h3>Mining Algorithm</h3>
                    <p>ZION uses dual-algorithm approach:</p>
                    <ul>
                        <li><strong>Yescrypt</strong>: CPU-friendly, memory-hard</li>
                        <li><strong>Argon2</strong>: GPU optimization support</li>
                    </ul>
                    
                    <h3>Fee Structure</h3>
                    <table>
                        <tr><th>Fee Type</th><th>Percentage</th><th>Recipient</th></tr>
                        <tr><td>Humanitarian</td><td>10%</td><td>Global aid projects</td></tr>
                        <tr><td>Development</td><td>1%</td><td>Core developers</td></tr>
                        <tr><td>Genesis</td><td>0.33%</td><td>Yeshuae Amon Ra</td></tr>
                        <tr><td>Pool Admin</td><td>1%</td><td>Maitreya Buddha</td></tr>
                        <tr><td><strong>Total Fees</strong></td><td><strong>12.33%</strong></td><td>-</td></tr>
                        <tr><td><strong>Miner Share</strong></td><td><strong>87.67%</strong></td><td>-</td></tr>
                    </table>
                `
            },
            'level-system': {
                title: 'Consciousness Level System',
                content: `
                    <h2>Nine Levels of Consciousness</h2>
                    
                    <p>The ZION consciousness mining system rewards miners based on their spiritual development across 9 levels.</p>
                    
                    <h3>Level Progression</h3>
                    <table>
                        <tr><th>Level</th><th>Name</th><th>Multiplier</th><th>Description</th></tr>
                        <tr><td>L1</td><td>PHYSICAL</td><td>1.0x</td><td>Material realm mastery</td></tr>
                        <tr><td>L2</td><td>ETHERIC</td><td>2.0x</td><td>Energy body awakening</td></tr>
                        <tr><td>L3</td><td>EMOTIONAL</td><td>3.5x</td><td>Emotional intelligence</td></tr>
                        <tr><td>L4</td><td>ASTRAL</td><td>5.0x</td><td>Astral projection ability</td></tr>
                        <tr><td>L5</td><td>MENTAL</td><td>7.0x</td><td>Mental clarity achieved</td></tr>
                        <tr><td>L6</td><td>CAUSAL</td><td>9.0x</td><td>Karmic understanding</td></tr>
                        <tr><td>L7</td><td>SPIRITUAL</td><td>11.0x</td><td>Spiritual awakening</td></tr>
                        <tr><td>L8</td><td>DIVINE</td><td>13.0x</td><td>Divine consciousness</td></tr>
                        <tr><td>L9</td><td>ON_THE_STAR</td><td>15.0x</td><td>Cosmic unity realized</td></tr>
                    </table>
                    
                    <h3>XP Calculation</h3>
                    <p>Experience points (XP) are earned through:</p>
                    <ul>
                        <li>Mining blocks: 100 XP per block</li>
                        <li>Community participation: Variable XP</li>
                        <li>DAO voting: 50 XP per vote</li>
                        <li>Humanitarian contributions: Bonus XP</li>
                    </ul>
                    
                    <blockquote>
                        "Consciousness is not something you attain, it is something you already are. Mining is merely the recognition of your true nature."
                        <cite>— ZION Whitepaper</cite>
                    </blockquote>
                `
            }
        };
        
        const page = pages[pageId];
        
        if (page) {
            article.innerHTML = `
                <h1 class="page-title glitch" data-text="${page.title}">${page.title}</h1>
                ${page.content}
            `;
        } else {
            article.innerHTML = `
                <h1 class="page-title">Page Not Found</h1>
                <p>The requested page could not be found. Please check the navigation menu.</p>
            `;
        }
        
        generateTOC();
    }
    
    // ===============================
    // TABLE OF CONTENTS GENERATOR
    // ===============================
    
    function generateTOC() {
        const article = document.getElementById('wiki-article');
        const tocNav = document.getElementById('toc-nav');
        
        if (!article || !tocNav) return;
        
        const headings = article.querySelectorAll('h2, h3, h4');
        
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
                
                // Update active state
                tocNav.querySelectorAll('a').forEach(a => a.classList.remove('active'));
                this.classList.add('active');
            });
            
            tocNav.appendChild(link);
        });
    }
    
    // ===============================
    // SEARCH FUNCTIONALITY
    // ===============================
    
    function initSearch() {
        const searchInput = document.getElementById('wiki-search');
        const searchBtn = document.getElementById('search-btn');
        
        if (!searchInput || !searchBtn) return;
        
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
    
    function performSearch() {
        const searchInput = document.getElementById('wiki-search');
        const query = searchInput.value.trim().toLowerCase();
        
        if (!query) return;
        
        // Simple search implementation
        console.log('Searching for:', query);
        
        // TODO: Implement full-text search across all wiki content
        alert(`Search functionality coming soon!\nSearching for: "${query}"`);
    }
    
    // ===============================
    // INITIALIZE
    // ===============================
    
    function init() {
        initCategoryNavigation();
        initPageNavigation();
        initSearch();
        
        // Show Sacred Books by default
        const sacredBooksList = document.getElementById('sacred-books-list');
        if (sacredBooksList) {
            sacredBooksList.style.display = 'flex';
        }
    }
    
    // Run on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
