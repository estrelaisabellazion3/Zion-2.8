/**
 * ZION BLOCKCHAIN - INTERACTIVE ANIMATIONS
 * Hero visuals, scroll effects, and interactive elements
 */

(function() {
    
    // ===============================
    // HERO CONSCIOUSNESS SPHERE
    // ===============================
    
    function initConsciousnessSphere() {
        const hero = document.querySelector('.hero');
        if (!hero) return;
        
        // Create consciousness sphere container
        const sphereContainer = document.createElement('div');
        sphereContainer.className = 'consciousness-sphere';
        sphereContainer.style.cssText = `
            position: absolute;
            top: 50%;
            right: 10%;
            transform: translate(0, -50%);
            width: 400px;
            height: 400px;
            pointer-events: none;
            z-index: 1;
        `;
        
        // Central orb
        const centralOrb = document.createElement('div');
        centralOrb.className = 'central-orb';
        centralOrb.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 150px;
            height: 150px;
            background: radial-gradient(circle at 30% 30%, 
                rgba(0, 255, 65, 0.8), 
                rgba(0, 255, 65, 0.4), 
                rgba(0, 255, 65, 0));
            border-radius: 50%;
            box-shadow: 
                0 0 30px rgba(0, 255, 65, 0.6),
                0 0 60px rgba(0, 255, 65, 0.4),
                inset 0 0 30px rgba(0, 255, 65, 0.3);
            animation: consciousness-pulse 3s ease-in-out infinite;
        `;
        
        // Orbit rings (3 rings)
        for (let i = 0; i < 3; i++) {
            const ring = document.createElement('div');
            ring.className = 'orbit-ring';
            const size = 200 + (i * 60);
            const delay = i * 0.5;
            
            ring.style.cssText = `
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: ${size}px;
                height: ${size}px;
                border: 2px solid rgba(0, 255, 65, ${0.3 - i * 0.08});
                border-radius: 50%;
                animation: orbit-rotate ${10 + i * 3}s linear infinite;
                animation-delay: ${delay}s;
            `;
            
            sphereContainer.appendChild(ring);
        }
        
        // Consciousness particles (20 particles)
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'consciousness-particle';
            
            const angle = (i / 20) * 360;
            const distance = 120 + Math.random() * 80;
            const x = Math.cos(angle * Math.PI / 180) * distance;
            const y = Math.sin(angle * Math.PI / 180) * distance;
            const delay = Math.random() * 5;
            const duration = 3 + Math.random() * 2;
            
            particle.style.cssText = `
                position: absolute;
                top: calc(50% + ${y}px);
                left: calc(50% + ${x}px);
                width: 4px;
                height: 4px;
                background: var(--matrix-green);
                border-radius: 50%;
                box-shadow: 0 0 10px var(--matrix-green);
                animation: particle-orbit ${duration}s ease-in-out infinite;
                animation-delay: ${delay}s;
                opacity: 0.6;
            `;
            
            sphereContainer.appendChild(particle);
        }
        
        sphereContainer.appendChild(centralOrb);
        hero.appendChild(sphereContainer);
        
        // Add animations to stylesheet
        if (!document.querySelector('#consciousness-animations')) {
            const style = document.createElement('style');
            style.id = 'consciousness-animations';
            style.textContent = `
                @keyframes consciousness-pulse {
                    0%, 100% {
                        transform: translate(-50%, -50%) scale(1);
                        opacity: 0.8;
                    }
                    50% {
                        transform: translate(-50%, -50%) scale(1.1);
                        opacity: 1;
                    }
                }
                
                @keyframes orbit-rotate {
                    0% {
                        transform: translate(-50%, -50%) rotate(0deg);
                    }
                    100% {
                        transform: translate(-50%, -50%) rotate(360deg);
                    }
                }
                
                @keyframes particle-orbit {
                    0%, 100% {
                        transform: translate(-50%, -50%) scale(1);
                        opacity: 0.4;
                    }
                    50% {
                        transform: translate(-50%, -50%) scale(1.5);
                        opacity: 0.8;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    // ===============================
    // SCROLL EFFECTS
    // ===============================
    
    function initScrollEffects() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);
        
        // Observe feature cards
        document.querySelectorAll('.feature-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        });
        
        // Observe consciousness levels
        document.querySelectorAll('.consciousness-level').forEach(level => {
            level.style.opacity = '0';
            level.style.transform = 'translateX(-30px)';
            level.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(level);
        });
        
        // Observe stat cards
        document.querySelectorAll('.stat-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'scale(0.9)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        });
        
        // Add animate-in class styles
        if (!document.querySelector('#scroll-animations')) {
            const style = document.createElement('style');
            style.id = 'scroll-animations';
            style.textContent = `
                .animate-in {
                    opacity: 1 !important;
                    transform: translateY(0) translateX(0) scale(1) !important;
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    // ===============================
    // SMOOTH SCROLLING
    // ===============================
    
    function initSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;
                
                e.preventDefault();
                const target = document.querySelector(href);
                
                if (target) {
                    const offsetTop = target.offsetTop - 80; // Account for fixed header
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    // ===============================
    // BUTTON RIPPLE EFFECT
    // ===============================
    
    function initButtonRipples() {
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    position: absolute;
                    width: ${size}px;
                    height: ${size}px;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.5);
                    top: ${y}px;
                    left: ${x}px;
                    pointer-events: none;
                    animation: ripple-animation 0.6s ease-out;
                `;
                
                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        });
        
        // Add ripple animation
        if (!document.querySelector('#ripple-animation')) {
            const style = document.createElement('style');
            style.id = 'ripple-animation';
            style.textContent = `
                @keyframes ripple-animation {
                    0% {
                        transform: scale(0);
                        opacity: 1;
                    }
                    100% {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    // ===============================
    // CARD TILT EFFECT
    // ===============================
    
    function initCardTilt() {
        const cards = document.querySelectorAll('.feature-card, .consciousness-level, .download-card');
        
        cards.forEach(card => {
            card.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 20;
                const rotateY = (centerX - x) / 20;
                
                this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
            });
        });
    }
    
    // ===============================
    // CONSCIOUSNESS LEVEL PROGRESS
    // ===============================
    
    function animateConsciousnessProgress() {
        const levels = document.querySelectorAll('.consciousness-level');
        
        levels.forEach((level, index) => {
            const progressBar = level.querySelector('.progress-bar');
            if (!progressBar) return;
            
            // Calculate progress based on level (L1=11%, L3=33%, L5=55%, L7=77%, L9=100%)
            const progress = ((index + 1) * 2 - 1) / 9 * 100;
            
            setTimeout(() => {
                progressBar.style.width = progress + '%';
            }, 300 + (index * 100));
        });
    }
    
    // ===============================
    // HEADER SCROLL EFFECT
    // ===============================
    
    function initHeaderScroll() {
        const header = document.querySelector('.header');
        if (!header) return;
        
        let lastScroll = 0;
        
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            // Add shadow when scrolled
            if (currentScroll > 50) {
                header.style.boxShadow = '0 4px 20px rgba(0, 255, 65, 0.2)';
                header.style.background = 'rgba(10, 14, 10, 0.95)';
            } else {
                header.style.boxShadow = 'none';
                header.style.background = 'var(--bg-dark)';
            }
            
            lastScroll = currentScroll;
        });
    }
    
    // ===============================
    // TYPING EFFECT
    // ===============================
    
    function initTypingEffect() {
        const tagline = document.querySelector('.hero-tagline');
        if (!tagline) return;
        
        const text = tagline.textContent;
        tagline.textContent = '';
        tagline.style.borderRight = '2px solid var(--matrix-green)';
        
        let index = 0;
        
        function type() {
            if (index < text.length) {
                tagline.textContent += text.charAt(index);
                index++;
                setTimeout(type, 50);
            } else {
                // Blinking cursor effect
                setInterval(() => {
                    tagline.style.borderRight = 
                        tagline.style.borderRight === '2px solid var(--matrix-green)' 
                        ? '2px solid transparent' 
                        : '2px solid var(--matrix-green)';
                }, 500);
            }
        }
        
        // Start typing after small delay
        setTimeout(type, 500);
    }
    
    // ===============================
    // COUNTER ANIMATION
    // ===============================
    
    function animateCounters() {
        const counters = document.querySelectorAll('.stat-value');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = parseInt(counter.textContent.replace(/,/g, '')) || 0;
                    
                    animateCounter(counter, 0, target, 2000);
                    observer.unobserve(counter);
                }
            });
        }, { threshold: 0.5 });
        
        counters.forEach(counter => observer.observe(counter));
    }
    
    function animateCounter(element, start, end, duration) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= end) {
                element.textContent = end.toLocaleString();
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current).toLocaleString();
            }
        }, 16);
    }
    
    // ===============================
    // INITIALIZE ALL
    // ===============================
    
    function init() {
        initConsciousnessSphere();
        initScrollEffects();
        initSmoothScrolling();
        initButtonRipples();
        initCardTilt();
        initHeaderScroll();
        // initTypingEffect(); // Commented out - can be enabled if desired
        animateCounters();
        
        // Animate consciousness progress when visible
        const consciousnessSection = document.querySelector('#consciousness');
        if (consciousnessSection) {
            const observer = new IntersectionObserver((entries) => {
                if (entries[0].isIntersecting) {
                    animateConsciousnessProgress();
                    observer.disconnect();
                }
            }, { threshold: 0.3 });
            
            observer.observe(consciousnessSection);
        }
    }
    
    // Run on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
