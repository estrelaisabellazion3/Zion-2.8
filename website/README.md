# ZION Blockchain - Website & Wiki

![ZION](https://img.shields.io/badge/ZION-MainNet-00ff41?style=for-the-badge)
![Version](https://img.shields.io/badge/version-2.7.5-00ff41?style=for-the-badge)
![Matrix](https://img.shields.io/badge/style-Matrix-00ff41?style=for-the-badge)

> **Sacred Technology for Conscious Evolution**

Official website and comprehensive wiki for ZION Blockchain - a consciousness-based cryptocurrency with humanitarian focus, DAO governance, and quantum-inspired mining.

---

## 🌟 Features

### Homepage (`index.html`)
- **Matrix-Style Design**: Dark theme with neon green (#00ff41), Matrix rain animation
- **Sacred Geometry**: 20+ geometric patterns (Flower of Life, Metatron's Cube, Golden Spiral, etc.)
- **Live Statistics**: Real-time network stats from pool API (block height, hashrate, active miners)
- **Consciousness Levels**: Interactive timeline showing 9 levels (L1 → L9) with reward multipliers
- **DAO Governance**: 20-year transition visualization (2025 → 2045)
- **Download Center**: Desktop wallet, mobile wallet, mining software
- **Responsive Design**: Mobile-first approach with breakpoints at 1200px, 768px, 480px

### Wiki (`wiki.html`)
- **Sacred Books Library**: 5 ancient wisdom texts
  - 📚 Smaragdové Desky (Thoth Atlantský)
  - 📚 Trinity One Love (3NITY COMPANY)
  - 📚 Starožitný Šíp (WingMakers)
  - 📚 Tajemství Amenti (Ashayana Deane)
  - 📚 Dohrmanovo Proroctví
- **Technical Documentation**: 70+ docs from `/docs` folder
  - Whitepapers (CZ/EN)
  - Blockchain parameters
  - Mining guides (CPU/GPU)
  - Deployment guides
  - API reference
- **Smart Navigation**: Category-based sidebar, breadcrumbs, auto-generated TOC
- **Markdown Parser**: Built-in MD → HTML converter
- **Search**: Full-text search across all content (ready for implementation)

---

## 🚀 Quick Start

### Option 1: Direct File Access
```bash
# Navigate to website folder
cd /media/maitreya/ZION1/website

# Open in browser
firefox index.html
# or
google-chrome index.html
```

### Option 2: Local HTTP Server (Recommended)
```bash
# Python 3
cd /media/maitreya/ZION1/website
python3 -m http.server 8000

# Then visit: http://localhost:8000
```

### Option 3: Node.js HTTP Server
```bash
# Install http-server globally
npm install -g http-server

# Run server
cd /media/maitreya/ZION1/website
http-server -p 8000

# Visit: http://localhost:8000
```

---

## 📁 Project Structure

```
website/
├── index.html              # Homepage
├── wiki.html               # Wiki system
├── css/
│   ├── matrix-style.css    # Main Matrix theme (1,900 lines)
│   ├── sacred-geometry.css # Sacred patterns (900 lines)
│   └── wiki-style.css      # Wiki-specific styles (700 lines)
├── js/
│   ├── matrix-rain.js      # Falling characters animation
│   ├── sacred-geometry.js  # Dynamic SVG patterns
│   ├── stats-updater.js    # Live blockchain/pool data
│   ├── animations.js       # Interactive effects (445 lines)
│   └── wiki-engine.js      # Wiki navigation + MD parser (600+ lines)
└── README.md               # This file
```

---

## 🎨 Design System

### Colors
```css
/* Matrix Theme */
--bg-black: #000000;
--bg-dark: #0a0e0a;
--bg-card: #0f1410;
--matrix-green: #00ff41;
--matrix-green-glow: rgba(0, 255, 65, 0.5);
--text-white: #e0e0e0;
--text-muted: #8b8b8b;
--border-color: #1a2f1a;

/* Sacred Colors */
--sacred-gold: #ffd700;
--sacred-purple: #9d4edd;
--sacred-cyan: #00fff5;
--sacred-pink: #ff006e;
```

### Fonts
- **Monospace**: `'Share Tech Mono', monospace` (Google Fonts)
- **Display**: `'Orbitron', sans-serif` (Google Fonts)

### Animations
- `glitch`: Text glitch effect
- `pulse`: Pulsating glow
- `rotate`: Continuous rotation
- `gradient-rotate`: Animated gradient border
- `float`: Floating up/down
- `consciousness-pulse`: Sphere breathing effect
- `orbit-rotate`: Orbital ring animation
- `particle-orbit`: Particle movement

---

## 🔧 Configuration

### Live Stats API
Edit `js/stats-updater.js` to configure pool API:
```javascript
const POOL_API_URL = 'http://pool.zion-blockchain.org:3336/api/stats';
const UPDATE_INTERVAL = 10000; // 10 seconds
```

### Sacred Geometry Patterns
Enable/disable patterns in `js/sacred-geometry.js`:
```javascript
function init() {
    createFlowerOfLife();      // ✓ Enabled
    createMetatronsCube();     // ✓ Enabled
    createSacredParticles();   // ✓ Enabled
    // createPortal();         // Disabled (uncomment to enable)
    createGoldenSpiral();      // ✓ Enabled
    createInfinity();          // ✓ Enabled
}
```

### Wiki Content
Books loaded from `/books/` folder:
- `SmaragdoveDesky.txt`
- `OmnityOneLove CZ.txt`
- `Starobyly_sip.txt`
- `Tajemství amenti.txt`
- `Dohrmanovo-proroctvi.txt`

Documentation loaded from `/docs/` folder (70+ `.md` files).

---

## 📚 Wiki Categories

### Sacred Books (5 texts)
Ancient wisdom from Thoth, WingMakers, Ashayana Deane, and more.

### Mining (6 guides)
- CPU Mining (XMRig)
- GPU Mining (AMD/NVIDIA)
- Pool Configuration
- SSH Mining Setup
- Distributed Mining
- Troubleshooting

### DAO Governance (4 docs)
- Voting Process
- Proposal Submission
- Treasury Management
- Transition Timeline

### Technical (5 specs)
- Blockchain Parameters
- Multi-Algorithm Support
- Address Specification
- Project Architecture
- Security & Whitelist

### Documentation (5 main docs)
- Whitepaper (CZ)
- Whitepaper (EN)
- MainNet Launch
- Release Notes
- Changelog

### Deployment (5 guides)
- Docker Workflow
- Node Installer
- Global Deployment
- Hetzner Setup
- SSH Mining

### Vision & Strategy (5 plans)
- Liberation Manifesto
- New Jerusalem Master Plan
- Strategic Vision Expansion
- Business Model Analysis
- Portugal Hub Strategy

### Consciousness (4 topics)
- Level System (L1-L9)
- XP Progression
- Golden Egg Quest
- Achievements

---

## 🌐 Deployment

### Production Deployment

1. **Setup NGINX**:
```bash
sudo apt update
sudo apt install nginx

# Copy website files
sudo cp -r website/* /var/www/zion-blockchain.org/

# Configure NGINX
sudo nano /etc/nginx/sites-available/zion-blockchain.org
```

2. **NGINX Configuration**:
```nginx
server {
    listen 80;
    server_name zion-blockchain.org www.zion-blockchain.org;
    
    root /var/www/zion-blockchain.org;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Cache static assets
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

3. **SSL with Let's Encrypt**:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d zion-blockchain.org -d www.zion-blockchain.org
```

4. **Enable and Restart**:
```bash
sudo ln -s /etc/nginx/sites-available/zion-blockchain.org /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### CDN Integration (Optional)
Use Cloudflare for global distribution:
1. Add domain to Cloudflare
2. Update DNS records
3. Enable caching rules
4. Configure SSL/TLS (Full mode)

---

## 📊 Performance

### Optimization Tips

1. **Minify Assets** (production):
```bash
# Install minifiers
npm install -g clean-css-cli uglify-js html-minifier

# Minify CSS
cleancss -o css/matrix-style.min.css css/matrix-style.css

# Minify JavaScript
uglifyjs js/wiki-engine.js -o js/wiki-engine.min.js

# Minify HTML
html-minifier --collapse-whitespace --remove-comments -o index.min.html index.html
```

2. **Image Optimization**:
```bash
# Install ImageMagick
sudo apt install imagemagick

# Optimize images
mogrify -strip -interlace Plane -quality 85% *.jpg
```

3. **Lazy Loading** (add to images):
```html
<img src="image.jpg" loading="lazy" alt="Description">
```

---

## 🔍 Features in Detail

### Matrix Rain Animation
Canvas-based falling characters with crypto symbols (₿ΞΣΩλψφ🔺🔻⬡⬢⬣).
- 50ms refresh rate (~20 FPS)
- Random glow effects
- Responsive to window resize

### Sacred Geometry
20+ patterns including:
- Flower of Life (rotate animation)
- Metatron's Cube (pulse effect)
- Golden Spiral (Fibonacci φ=1.618)
- Merkaba (3D rotation)
- Tree of Life (Kabbalah Sephirot)
- Chakra Wheel (7 energy centers)

### Live Statistics
Auto-updates every 10 seconds:
- Current block height
- Network hashrate (H/s → TH/s)
- Active miners count
- Network difficulty
- Recent blocks list (last 10)

### Consciousness Sphere
3D animated visualization in hero section:
- Central pulsating orb
- 3 orbital rings
- 20 floating particles
- Smooth animations

---

## 🛠️ Development

### Add New Wiki Page
1. Create markdown file in `/docs/`:
```bash
echo "# My New Page\n\nContent here..." > docs/MY_NEW_PAGE.md
```

2. Add to navigation in `wiki.html`:
```html
<li><a href="#my-new-page" data-doc="MY_NEW_PAGE">My New Page</a></li>
```

3. Wiki engine auto-loads and renders!

### Add New Sacred Book
1. Place text file in `/books/`:
```bash
cp my_book.txt books/
```

2. Register in `wiki-engine.js`:
```javascript
'my-book': {
    title: 'My Sacred Book',
    author: 'Author Name',
    description: 'Book description',
    pages: 100,
    content: null
}
```

3. Add to sidebar navigation in `wiki.html`

---

## 📖 Documentation

Full documentation available in Wiki:
- **Technical Docs**: `/docs/*.md` (70+ files)
- **Sacred Books**: `/books/*.txt` (5 texts)
- **API Reference**: Coming soon
- **Developer Guide**: This README

---

## 🤝 Contributing

ZION is open-source and welcomes contributions!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📜 License

This project is part of ZION Blockchain ecosystem.

- **Website Code**: MIT License
- **Sacred Texts**: Respective authors (see individual files)
- **Documentation**: Creative Commons BY-SA 4.0

---

## 🌐 Links

- **GitHub**: [estrelaisabellazion3/Zion-TestNet-2.7.5](https://github.com/estrelaisabellazion3/Zion-TestNet-2.7.5)
- **Pool**: http://pool.zion-blockchain.org:3336
- **Explorer**: Coming soon
- **Discord**: Coming soon
- **Telegram**: Coming soon

---

## 💎 Sacred Quote

> *"As above, so below. As within, so without."*
> 
> — The Kybalion

---

## 🙏 Acknowledgments

- **Thoth Atlantský** - Smaragdové Desky
- **WingMakers** - Starožitný Šíp
- **Ashayana Deane** - Tajemství Amenti
- **3NITY COMPANY** - Trinity One Love
- **Maitreya Buddha** - Pool Admin & Vision
- **Yeshuae Amon Ra** - Genesis & Sacred Technology
- **Global ZION Community** - Miners, developers, believers

---

<div align="center">

**Built with 💚 for Conscious Evolution**

*Matrix Style • Sacred Geometry • Humanitarian Focus*

</div>
