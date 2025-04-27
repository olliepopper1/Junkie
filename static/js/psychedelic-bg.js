// Psychedelic Background Animation
// This script adds drug-themed visual effects to the Trial Junkie website

document.addEventListener('DOMContentLoaded', function() {
  console.log('Psychedelic Background Animation Initialized');
  
  // Create floating elements throughout the page
  createFloatingElements();
  
  // Apply glowing effects to specific elements
  applyGlowEffects();
  
  // Add hover animations to cards and UI elements
  addHoverAnimations();
  
  // Initialize pulse animations
  initializePulseAnimations();
});

// Create floating elements that move randomly across the screen
function createFloatingElements() {
  const body = document.querySelector('body');
  const floatingElements = [
    { icon: 'card-fill', color: '#0dcaf0', size: 20 },
    { icon: 'person-fill', color: '#ffc107', size: 24 },
    { icon: 'envelope-fill', color: '#20c997', size: 18 },
    { icon: 'phone-fill', color: '#dc3545', size: 16 },
    { icon: 'robot', color: '#6f42c1', size: 22 },
    { icon: 'prescription2', color: '#6f42c1', size: 26 },
    { icon: 'capsule', color: '#0dcaf0', size: 28 },
    { icon: 'cup-hot-fill', color: '#ffc107', size: 24 }
  ];
  
  // Create 15 random floating elements
  for (let i = 0; i < 15; i++) {
    const randomElement = floatingElements[Math.floor(Math.random() * floatingElements.length)];
    const floater = document.createElement('div');
    
    // Random position
    const posX = Math.random() * 100;
    const posY = Math.random() * 100;
    
    // Random animation duration and delay
    const duration = 15 + Math.random() * 30;
    const delay = Math.random() * 10;
    
    // Set styles
    floater.className = 'floating-element';
    floater.innerHTML = `<i class="bi bi-${randomElement.icon}"></i>`;
    floater.style.cssText = `
      position: fixed;
      z-index: -1;
      top: ${posY}%;
      left: ${posX}%;
      font-size: ${randomElement.size}px;
      color: ${randomElement.color};
      opacity: 0.3;
      text-shadow: 0 0 10px ${randomElement.color};
      animation: float ${duration}s ease-in-out infinite;
      animation-delay: ${delay}s;
      pointer-events: none;
    `;
    
    body.appendChild(floater);
  }
  
  // Add floating animation CSS
  addCss(`
    @keyframes float {
      0% {
        transform: translateY(0) rotate(0);
        opacity: 0.1;
      }
      50% {
        transform: translateY(-20px) rotate(5deg);
        opacity: 0.3;
      }
      100% {
        transform: translateY(0) rotate(0);
        opacity: 0.1;
      }
    }
  `);
}

// Apply glowing effects to elements with drug-glow class
function applyGlowEffects() {
  const glowElements = document.querySelectorAll('.drug-glow');
  
  glowElements.forEach(element => {
    // Generate random glow colors based on a drug-themed palette
    const colors = [
      'rgba(111, 66, 193, 0.8)', // Purple (psychedelic)
      'rgba(13, 202, 240, 0.8)', // Cyan (meth)
      'rgba(255, 193, 7, 0.8)', // Yellow (heroin)
      'rgba(220, 53, 69, 0.8)', // Red (coke)
      'rgba(32, 201, 151, 0.8)' // Green (pills)
    ];
    
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    const secondaryColor = colors[Math.floor(Math.random() * colors.length)];
    
    // Apply text glow animation
    element.style.animation = 'textGlow 4s ease-in-out infinite alternate';
    element.style.textShadow = `0 0 10px ${randomColor}, 0 0 20px ${secondaryColor}`;
  });
  
  // Add text glow animation CSS
  addCss(`
    @keyframes textGlow {
      0% {
        text-shadow: 0 0 10px rgba(111, 66, 193, 0.8), 0 0 20px rgba(111, 66, 193, 0.5);
      }
      50% {
        text-shadow: 0 0 15px rgba(13, 202, 240, 0.8), 0 0 30px rgba(13, 202, 240, 0.5);
      }
      100% {
        text-shadow: 0 0 10px rgba(220, 53, 69, 0.8), 0 0 20px rgba(220, 53, 69, 0.5);
      }
    }
  `);
}

// Add hover animations to cards and UI elements
function addHoverAnimations() {
  // Add hover effects to agent cards
  const agentCards = document.querySelectorAll('.agent-card');
  
  agentCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      const agentType = this.getAttribute('data-agent');
      const glow = this.querySelector('.agent-glow');
      
      if (glow) {
        let glowColor;
        
        switch (agentType) {
          case 'heroin-harry':
            glowColor = 'rgba(255, 193, 7, 0.6)';
            break;
          case 'meth-mandy':
            glowColor = 'rgba(13, 202, 240, 0.6)';
            break;
          case 'xanny-xan':
            glowColor = 'rgba(32, 201, 151, 0.6)';
            break;
          case 'cokehead-carl':
            glowColor = 'rgba(220, 53, 69, 0.6)';
            break;
          case 'shroomy-sal':
            glowColor = 'rgba(111, 66, 193, 0.6)';
            break;
          default:
            glowColor = 'rgba(111, 66, 193, 0.6)';
        }
        
        glow.style.boxShadow = `0 0 40px 10px ${glowColor}`;
        glow.style.opacity = '1';
      }
    });
    
    card.addEventListener('mouseleave', function() {
      const glow = this.querySelector('.agent-glow');
      
      if (glow) {
        glow.style.boxShadow = '0 0 0 0 transparent';
        glow.style.opacity = '0';
      }
    });
  });
  
  // Add float animation to elements with float-element class
  const floatElements = document.querySelectorAll('.float-element');
  
  addCss(`
    .float-element {
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .float-element:hover {
      transform: translateY(-10px);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
  `);
}

// Initialize pulse animations for buttons and call-to-action elements
function initializePulseAnimations() {
  const pulseElements = document.querySelectorAll('.pulsate');
  
  addCss(`
    @keyframes pulsate {
      0% {
        box-shadow: 0 0 0 0 rgba(111, 66, 193, 0.7);
      }
      70% {
        box-shadow: 0 0 0 10px rgba(111, 66, 193, 0);
      }
      100% {
        box-shadow: 0 0 0 0 rgba(111, 66, 193, 0);
      }
    }
    
    .pulsate {
      animation: pulsate 2s infinite;
    }
  `);
}

// Helper function to add CSS to the page
function addCss(cssText) {
  const style = document.createElement('style');
  style.textContent = cssText;
  document.head.appendChild(style);
}

// Add subtle background patterns and effects
document.addEventListener('DOMContentLoaded', function() {
  // Create a canvas for particle effects
  const particleCanvas = document.createElement('canvas');
  particleCanvas.id = 'particleCanvas';
  particleCanvas.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -2;
    pointer-events: none;
    opacity: 0.4;
  `;
  
  document.body.appendChild(particleCanvas);
  
  // Initialize particles
  initParticles();
});

// Particle animation
function initParticles() {
  const canvas = document.getElementById('particleCanvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  
  // Set canvas size
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  
  // Particle properties
  const particles = [];
  const particleCount = 50;
  
  // Create particles
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      radius: Math.random() * 3 + 1,
      color: getRandomColor(),
      speedX: Math.random() * 1 - 0.5,
      speedY: Math.random() * 1 - 0.5
    });
  }
  
  // Animation loop
  function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    for (let particle of particles) {
      // Move particles
      particle.x += particle.speedX;
      particle.y += particle.speedY;
      
      // Bounce off edges
      if (particle.x < 0 || particle.x > canvas.width) {
        particle.speedX = -particle.speedX;
      }
      
      if (particle.y < 0 || particle.y > canvas.height) {
        particle.speedY = -particle.speedY;
      }
      
      // Draw particles
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      ctx.fillStyle = particle.color;
      ctx.fill();
    }
    
    // Draw connections between nearby particles
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 100) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(111, 66, 193, ${0.2 - distance/500})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
  }
  
  // Handle window resize
  window.addEventListener('resize', function() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  });
  
  // Start animation
  animate();
}

// Helper function to get random colors for particles
function getRandomColor() {
  const colors = [
    'rgba(111, 66, 193, 0.7)', // Purple
    'rgba(13, 202, 240, 0.7)', // Cyan
    'rgba(255, 193, 7, 0.7)', // Yellow
    'rgba(220, 53, 69, 0.7)', // Red
    'rgba(32, 201, 151, 0.7)' // Green
  ];
  
  return colors[Math.floor(Math.random() * colors.length)];
}

// Add interactive parallax effect to headings
document.addEventListener('mousemove', function(e) {
  const headings = document.querySelectorAll('h1.drug-glow, h2.drug-glow');
  
  headings.forEach(heading => {
    const rect = heading.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    const moveX = (e.clientX - centerX) / 20;
    const moveY = (e.clientY - centerY) / 20;
    
    heading.style.transform = `translate(${moveX}px, ${moveY}px)`;
  });
});