/**
 * Trial Junkie - Psychedelic Background Animation
 * Creates a trippy, drug-themed animated background with floating particles
 */

document.addEventListener('DOMContentLoaded', () => {
  // Create the background container
  const bgContainer = document.createElement('div');
  bgContainer.className = 'psychedelic-bg';
  document.body.prepend(bgContainer);
  
  // Create floating particles
  const particleCount = 30;
  
  // Define drug-themed colors
  const colors = [
    '#6f42c1', // Purple (Heroin Harry)
    '#0dcaf0', // Blue (Meth Mandy)
    '#20c997', // Green (Xanny Xan)
    '#dc3545', // Red (Cokehead Carl)
    '#ffc107', // Yellow (Acid Alice)
    '#ff00cc'  // Hot Pink (DMT Dave)
  ];
  
  for (let i = 0; i < particleCount; i++) {
    createParticle();
  }
  
  function createParticle() {
    const particle = document.createElement('div');
    particle.className = 'floating-particle';
    
    // Random properties
    const size = Math.random() * 10 + 5;
    const color = colors[Math.floor(Math.random() * colors.length)];
    const posX = Math.random() * 100;
    const posY = Math.random() * 100;
    const duration = Math.random() * 30 + 20;
    const delay = Math.random() * 10;
    
    // Apply styles
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.backgroundColor = color;
    particle.style.left = `${posX}vw`;
    particle.style.top = `${posY}vh`;
    particle.style.boxShadow = `0 0 ${size + 5}px ${color}`;
    particle.style.opacity = Math.random() * 0.5 + 0.1;
    particle.style.animationDuration = `${duration}s`;
    particle.style.animationDelay = `${delay}s`;
    
    // Add to container
    bgContainer.appendChild(particle);
  }
  
  // Create drug-themed effects for certain sections
  const heroicSections = document.querySelectorAll('.hero, .agent-section, .referral-section');
  
  heroicSections.forEach(section => {
    // Add subtle wavy animation to section backgrounds
    section.style.position = 'relative';
    section.style.overflow = 'hidden';
    
    const wave = document.createElement('div');
    wave.className = 'trippy-wave';
    section.appendChild(wave);
  });
  
  // Add hovering effects to agent cards
  const agentCards = document.querySelectorAll('.agent-card');
  
  agentCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      // Apply a more intense glow effect on hover
      const agentType = card.getAttribute('data-agent') || '';
      let glowColor;
      
      switch(agentType) {
        case 'heroin-harry':
          glowColor = '#ffc107';
          break;
        case 'meth-mandy':
          glowColor = '#0dcaf0';
          break;
        case 'xanny-xan':
          glowColor = '#20c997';
          break;
        case 'cokehead-carl':
          glowColor = '#dc3545';
          break;
        case 'shroomy-sal':
          glowColor = '#6f42c1';
          break;
        case 'crypto-craig':
          glowColor = '#20c997';
          break;
        default:
          glowColor = '#6f42c1';
      }
      
      card.style.boxShadow = `0 0 25px ${glowColor}`;
      
      // Create small particles around the card
      for (let i = 0; i < 5; i++) {
        const miniParticle = document.createElement('div');
        miniParticle.className = 'mini-particle';
        miniParticle.style.backgroundColor = glowColor;
        miniParticle.style.boxShadow = `0 0 5px ${glowColor}`;
        card.appendChild(miniParticle);
        
        // Remove after animation
        setTimeout(() => {
          if (miniParticle.parentNode === card) {
            card.removeChild(miniParticle);
          }
        }, 2000);
      }
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.boxShadow = '';
      
      // Remove any remaining particles
      const particles = card.querySelectorAll('.mini-particle');
      particles.forEach(p => p.remove());
    });
  });
  
  // Add trippy text effects to headers
  const drugHeaders = document.querySelectorAll('.drug-glow');
  
  drugHeaders.forEach(header => {
    // Create animated shadow effect
    header.style.position = 'relative';
    
    // Create a small amount of random character distortion on hover
    header.addEventListener('mouseenter', () => {
      const originalText = header.textContent;
      const distortInterval = setInterval(() => {
        if (header.matches(':hover')) {
          const text = header.textContent;
          const charIndex = Math.floor(Math.random() * text.length);
          const charArray = text.split('');
          
          // Only distort non-space characters
          if (charArray[charIndex] !== ' ') {
            const nextChar = String.fromCharCode(
              charArray[charIndex].charCodeAt(0) + 
              Math.floor(Math.random() * 5) - 2
            );
            
            charArray[charIndex] = nextChar;
            header.textContent = charArray.join('');
            
            // Reset character after short delay
            setTimeout(() => {
              const resetArray = header.textContent.split('');
              resetArray[charIndex] = originalText.split('')[charIndex];
              header.textContent = resetArray.join('');
            }, 100);
          }
        }
      }, 200);
      
      header.addEventListener('mouseleave', () => {
        clearInterval(distortInterval);
        header.textContent = originalText;
      });
    });
  });
});

// Add CSS for the animated elements
const style = document.createElement('style');
style.textContent = `
  .psychedelic-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -10;
    overflow: hidden;
  }
  
  .floating-particle {
    position: absolute;
    border-radius: 50%;
    animation: float-around 30s linear infinite;
    pointer-events: none;
  }
  
  @keyframes float-around {
    0% {
      transform: translate(0, 0) rotate(0deg);
    }
    25% {
      transform: translate(50px, -30px) rotate(90deg);
    }
    50% {
      transform: translate(0, -60px) rotate(180deg);
    }
    75% {
      transform: translate(-50px, -30px) rotate(270deg);
    }
    100% {
      transform: translate(0, 0) rotate(360deg);
    }
  }
  
  .trippy-wave {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 30%;
    background: linear-gradient(to top, 
                                rgba(111, 66, 193, 0.05), 
                                rgba(32, 201, 151, 0.03), 
                                rgba(255, 193, 7, 0.01), 
                                transparent);
    animation: wave 15s ease-in-out infinite;
    pointer-events: none;
    mix-blend-mode: screen;
  }
  
  @keyframes wave {
    0%, 100% {
      transform: translateY(0) scaleY(1);
    }
    50% {
      transform: translateY(-20px) scaleY(1.2);
    }
  }
  
  .mini-particle {
    position: absolute;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    animation: float-particle 2s ease-out;
    opacity: 0.7;
    pointer-events: none;
  }
  
  @keyframes float-particle {
    0% {
      transform: translate(0, 0) scale(0);
      opacity: 0.7;
    }
    50% {
      opacity: 0.5;
    }
    100% {
      transform: translate(
        calc(${Math.random() * 100 - 50}px), 
        calc(${Math.random() * 100 - 50}px)
      ) scale(1);
      opacity: 0;
    }
  }
`;

document.head.appendChild(style);