/**
 * ZION BLOCKCHAIN - MATRIX RAIN EFFECT
 * Classic Matrix-style falling characters
 */

(function() {
    const canvas = document.getElementById('matrix-rain');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Matrix characters (mix of crypto symbols, numbers, and letters)
    const matrixChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789₿ΞΣΩλψφ🔺🔻⬡⬢⬣';
    const chars = matrixChars.split('');
    
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    
    // Array to store drop position for each column
    const drops = [];
    for (let i = 0; i < columns; i++) {
        drops[i] = Math.random() * -100; // Start at random heights
    }
    
    // Drawing function
    function draw() {
        // Semi-transparent black to create trail effect
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Matrix green text
        ctx.fillStyle = '#00ff41';
        ctx.font = fontSize + 'px monospace';
        
        // Loop over drops
        for (let i = 0; i < drops.length; i++) {
            // Random character
            const char = chars[Math.floor(Math.random() * chars.length)];
            
            // Draw character
            const x = i * fontSize;
            const y = drops[i] * fontSize;
            
            // Add glow effect to some characters
            if (Math.random() > 0.98) {
                ctx.shadowBlur = 10;
                ctx.shadowColor = '#00ff41';
            } else {
                ctx.shadowBlur = 0;
            }
            
            ctx.fillText(char, x, y);
            
            // Reset drop to top randomly
            if (y > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            
            // Move drop down
            drops[i]++;
        }
    }
    
    // Animate
    setInterval(draw, 50);
    
})();
