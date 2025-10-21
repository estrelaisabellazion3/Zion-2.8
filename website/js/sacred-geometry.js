/**
 * ZION BLOCKCHAIN - SACRED GEOMETRY ANIMATIONS
 * Dynamic sacred geometry rendering
 */

(function() {
    const bg = document.querySelector('.sacred-geometry-bg');
    if (!bg) return;
    
    // Create Flower of Life pattern
    function createFlowerOfLife() {
        const container = document.createElement('div');
        container.className = 'flower-of-life';
        container.style.top = '10%';
        container.style.left = '80%';
        
        // Create SVG
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('width', '400');
        svg.setAttribute('height', '400');
        svg.setAttribute('viewBox', '0 0 400 400');
        
        // Central circle
        const centerX = 200;
        const centerY = 200;
        const radius = 50;
        
        // Draw 7 circles in flower pattern
        const angles = [0, 60, 120, 180, 240, 300];
        
        // Center circle
        const centerCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        centerCircle.setAttribute('cx', centerX);
        centerCircle.setAttribute('cy', centerY);
        centerCircle.setAttribute('r', radius);
        centerCircle.setAttribute('fill', 'none');
        centerCircle.setAttribute('stroke', '#00ff41');
        centerCircle.setAttribute('stroke-width', '2');
        centerCircle.setAttribute('opacity', '0.3');
        svg.appendChild(centerCircle);
        
        // Surrounding circles
        angles.forEach(angle => {
            const rad = (angle * Math.PI) / 180;
            const x = centerX + radius * Math.cos(rad);
            const y = centerY + radius * Math.sin(rad);
            
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', x);
            circle.setAttribute('cy', y);
            circle.setAttribute('r', radius);
            circle.setAttribute('fill', 'none');
            circle.setAttribute('stroke', '#00ff41');
            circle.setAttribute('stroke-width', '2');
            circle.setAttribute('opacity', '0.3');
            svg.appendChild(circle);
        });
        
        container.appendChild(svg);
        bg.appendChild(container);
    }
    
    // Create Metatron's Cube
    function createMetatronsCube() {
        const container = document.createElement('div');
        container.className = 'metatrons-cube';
        container.style.top = '60%';
        container.style.left = '10%';
        
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('width', '500');
        svg.setAttribute('height', '500');
        svg.setAttribute('viewBox', '0 0 500 500');
        
        const centerX = 250;
        const centerY = 250;
        const radius = 100;
        
        // Create 13 circles (Metatron's Cube)
        const points = [
            {x: 0, y: 0}, // Center
            {x: 0, y: -radius},
            {x: radius * Math.cos(Math.PI/6), y: -radius * Math.sin(Math.PI/6)},
            {x: radius, y: 0},
            {x: radius * Math.cos(Math.PI/6), y: radius * Math.sin(Math.PI/6)},
            {x: 0, y: radius},
            {x: -radius * Math.cos(Math.PI/6), y: radius * Math.sin(Math.PI/6)},
            {x: -radius, y: 0},
            {x: -radius * Math.cos(Math.PI/6), y: -radius * Math.sin(Math.PI/6)},
        ];
        
        // Draw circles
        points.forEach(point => {
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', centerX + point.x);
            circle.setAttribute('cy', centerY + point.y);
            circle.setAttribute('r', '30');
            circle.setAttribute('fill', 'none');
            circle.setAttribute('stroke', '#9d4edd');
            circle.setAttribute('stroke-width', '2');
            circle.setAttribute('opacity', '0.4');
            svg.appendChild(circle);
        });
        
        // Draw connecting lines
        points.forEach((p1, i) => {
            points.forEach((p2, j) => {
                if (i < j) {
                    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                    line.setAttribute('x1', centerX + p1.x);
                    line.setAttribute('y1', centerY + p1.y);
                    line.setAttribute('x2', centerX + p2.x);
                    line.setAttribute('y2', centerY + p2.y);
                    line.setAttribute('stroke', '#00fff5');
                    line.setAttribute('stroke-width', '1');
                    line.setAttribute('opacity', '0.2');
                    svg.appendChild(line);
                }
            });
        });
        
        container.appendChild(svg);
        bg.appendChild(container);
    }
    
    // Create floating particles
    function createSacredParticles() {
        const particlesContainer = document.createElement('div');
        particlesContainer.className = 'sacred-particles';
        
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 10 + 's';
            particle.style.animationDuration = (10 + Math.random() * 10) + 's';
            
            // Random color
            const colors = ['#00ff41', '#00fff5', '#9d4edd', '#ffd700'];
            particle.style.background = colors[Math.floor(Math.random() * colors.length)];
            
            particlesContainer.appendChild(particle);
        }
        
        bg.appendChild(particlesContainer);
    }
    
    // Create portal effect
    function createPortal() {
        const portal = document.createElement('div');
        portal.className = 'portal';
        portal.style.top = '30%';
        portal.style.left = '50%';
        portal.style.transform = 'translateX(-50%)';
        bg.appendChild(portal);
    }
    
    // Create golden spiral
    function createGoldenSpiral() {
        const container = document.createElement('div');
        container.className = 'golden-spiral';
        container.style.top = '70%';
        container.style.right = '10%';
        
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('width', '400');
        svg.setAttribute('height', '400');
        svg.setAttribute('viewBox', '0 0 400 400');
        
        // Golden ratio φ = 1.618
        const phi = 1.618;
        let size = 5;
        let x = 200;
        let y = 200;
        
        for (let i = 0; i < 10; i++) {
            const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            rect.setAttribute('x', x);
            rect.setAttribute('y', y);
            rect.setAttribute('width', size);
            rect.setAttribute('height', size * phi);
            rect.setAttribute('fill', 'none');
            rect.setAttribute('stroke', '#ffd700');
            rect.setAttribute('stroke-width', '1');
            rect.setAttribute('opacity', '0.3');
            svg.appendChild(rect);
            
            // Rotate and scale for next iteration
            const newSize = size * phi;
            x -= newSize;
            y -= newSize * phi;
            size = newSize;
        }
        
        container.appendChild(svg);
        bg.appendChild(container);
    }
    
    // Create infinity symbol
    function createInfinity() {
        const container = document.createElement('div');
        container.className = 'infinity';
        container.style.top = '50%';
        container.style.left = '20%';
        
        const loop1 = document.createElement('div');
        loop1.className = 'infinity-loop';
        
        const loop2 = document.createElement('div');
        loop2.className = 'infinity-loop';
        
        container.appendChild(loop1);
        container.appendChild(loop2);
        bg.appendChild(container);
    }
    
    // Initialize all sacred geometry
    function init() {
        createFlowerOfLife();
        createMetatronsCube();
        createSacredParticles();
        createPortal();
        createGoldenSpiral();
        createInfinity();
    }
    
    // Run on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
