/**
 * Psychedelic Background Animation for Trial Junkie
 * Creates a trippy visual effect in the background
 */

// Animation settings
const settings = {
  particleCount: 100,
  particleSizeMin: 2,
  particleSizeMax: 6,
  colorPalette: [
    'rgba(111, 66, 193, 0.8)',  // Primary purple
    'rgba(163, 112, 247, 0.8)',  // Secondary purple
    'rgba(210, 194, 255, 0.8)',  // Light purple
    'rgba(77, 43, 137, 0.8)'     // Dark purple
  ],
  speedFactor: 0.5,
  blurFactor: 2,
  connectParticles: true,
  connectDistance: 150,
  pulseEffect: true,
  responsivenessThreshold: 768  // Reduce particle count on mobile
};

// Initialize canvas elements and animation
document.addEventListener('DOMContentLoaded', function() {
  console.log('Psychedelic Background Animation Initialized');
  
  // Only create animation on pages with the bg-canvas element
  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  let particles = [];
  let animationFrameId;
  let width, height;
  
  // Set canvas to full window size
  function resizeCanvas() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    
    // Adjust particle count for mobile
    const isMobile = width < settings.responsivenessThreshold;
    const particleCount = isMobile ? Math.floor(settings.particleCount / 2) : settings.particleCount;
    
    // Reinitialize particles
    initParticles(particleCount);
  }
  
  // Create particles
  function initParticles(count) {
    particles = [];
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * (settings.particleSizeMax - settings.particleSizeMin) + settings.particleSizeMin,
        color: settings.colorPalette[Math.floor(Math.random() * settings.colorPalette.length)],
        vx: (Math.random() - 0.5) * settings.speedFactor,
        vy: (Math.random() - 0.5) * settings.speedFactor,
        pulse: 0,
        pulseDirection: Math.random() > 0.5 ? 1 : -1
      });
    }
  }
  
  // Animation loop
  function animate() {
    ctx.clearRect(0, 0, width, height);
    
    // Draw connections between particles
    if (settings.connectParticles) {
      ctx.beginPath();
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < settings.connectDistance) {
            const opacity = 1 - (distance / settings.connectDistance);
            ctx.strokeStyle = `rgba(111, 66, 193, ${opacity * 0.3})`;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }
    }
    
    // Update and draw particles
    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      
      // Update position
      p.x += p.vx;
      p.y += p.vy;
      
      // Pulse effect (subtle size change)
      if (settings.pulseEffect) {
        p.pulse += 0.01 * p.pulseDirection;
        if (p.pulse > 1 || p.pulse < -1) p.pulseDirection *= -1;
      }
      
      // Wrap around screen edges
      if (p.x < -50) p.x = width + 50;
      if (p.x > width + 50) p.x = -50;
      if (p.y < -50) p.y = height + 50;
      if (p.y > height + 50) p.y = -50;
      
      // Draw particle
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius * (1 + p.pulse * 0.2), 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      
      // Apply glow effect
      const blur = settings.blurFactor + Math.abs(p.pulse) * 2;
      ctx.shadowColor = p.color;
      ctx.shadowBlur = blur;
      ctx.shadowOffsetX = 0;
      ctx.shadowOffsetY = 0;
      
      ctx.fill();
      ctx.closePath();
    }
    
    animationFrameId = requestAnimationFrame(animate);
  }
  
  // Initialize and start animation
  resizeCanvas();
  animate();
  
  // Handle window resize
  window.addEventListener('resize', resizeCanvas);
  
  // Cleanup on page unload
  window.addEventListener('beforeunload', function() {
    cancelAnimationFrame(animationFrameId);
    window.removeEventListener('resize', resizeCanvas);
  });
});