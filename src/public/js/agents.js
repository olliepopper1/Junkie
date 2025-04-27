/**
 * Trial Junkie - Agent Profiles Animation
 * Adds drug-themed animations to agent profile cards and modals
 */

document.addEventListener('DOMContentLoaded', () => {
  // Add data-agent attributes to all agent cards
  const agentCards = document.querySelectorAll('.agent-card');
  const agentNames = [
    'heroin-harry',
    'meth-mandy',
    'xanny-xan',
    'cokehead-carl',
    'shroomy-sal',
    'crypto-craig'
  ];
  
  // Match cards with agent names based on order
  agentCards.forEach((card, index) => {
    if (index < agentNames.length) {
      card.setAttribute('data-agent', agentNames[index]);
    }
  });
  
  // Add floating animation to agent cards
  agentCards.forEach(card => {
    // Random floating animation parameters
    const duration = 3 + Math.random() * 2; // 3-5 seconds
    const delay = Math.random() * 2; // 0-2 second delay
    
    card.style.animation = `float ${duration}s ease-in-out ${delay}s infinite`;
  });
  
  // Modal enhancements
  const agentModals = document.querySelectorAll('.modal');
  
  agentModals.forEach(modal => {
    // Extract agent type from modal ID
    const modalId = modal.id;
    const agentType = modalId.replace('Modal', '');
    
    modal.addEventListener('show.bs.modal', () => {
      // Add drug-themed effects based on agent type
      const portrait = modal.querySelector('.agent-portrait');
      const quote = modal.querySelector('.agent-quote');
      
      if (portrait) {
        // Different glow colors based on agent
        let glowColor;
        switch(agentType) {
          case 'heroinHarry':
            glowColor = '#ffc107';
            addSlowPulseEffect(portrait, quote);
            break;
          case 'methMandy':
            glowColor = '#0dcaf0';
            addJitterEffect(portrait, quote);
            break;
          case 'xannyXan':
            glowColor = '#20c997';
            addRelaxedEffect(portrait, quote);
            break;
          case 'cokeheadCarl':
            glowColor = '#dc3545';
            addHyperEffect(portrait, quote);
            break;
          case 'shroomySal':
            glowColor = '#6f42c1';
            addTripEffect(portrait, quote);
            break;
          case 'cryptoCraig':
            glowColor = '#20c997';
            addParanoidEffect(portrait, quote);
            break;
          default:
            glowColor = '#6f42c1';
        }
        
        // Apply glow effect
        portrait.style.boxShadow = `0 0 20px ${glowColor}`;
      }
    });
    
    modal.addEventListener('hidden.bs.modal', () => {
      // Remove effects when modal closes
      const portrait = modal.querySelector('.agent-portrait');
      if (portrait) {
        portrait.style.animation = '';
        portrait.style.transform = '';
      }
      
      const quote = modal.querySelector('.agent-quote');
      if (quote) {
        quote.style.animation = '';
      }
    });
  });
  
  // Agent-specific animations
  function addSlowPulseEffect(portrait, quote) {
    // Heroin Harry - slow, dreamy pulsing
    portrait.style.animation = 'heroinPulse 8s ease-in-out infinite';
    addAnimationStyles(`
      @keyframes heroinPulse {
        0%, 100% { transform: scale(1); filter: blur(0px); }
        50% { transform: scale(1.05); filter: blur(1px); }
      }
    `);
    
    if (quote) {
      quote.style.animation = 'slowFade 8s ease-in-out infinite';
      addAnimationStyles(`
        @keyframes slowFade {
          0%, 100% { opacity: 0.7; }
          50% { opacity: 1; }
        }
      `);
    }
  }
  
  function addJitterEffect(portrait, quote) {
    // Meth Mandy - fast jittery movements
    portrait.style.animation = 'methJitter 0.5s linear infinite';
    addAnimationStyles(`
      @keyframes methJitter {
        0% { transform: translate(0, 0); }
        25% { transform: translate(-2px, 1px); }
        50% { transform: translate(2px, -1px); }
        75% { transform: translate(-1px, -1px); }
        100% { transform: translate(0, 0); }
      }
    `);
    
    if (quote) {
      quote.style.animation = 'fastFade 1s linear infinite';
      addAnimationStyles(`
        @keyframes fastFade {
          0%, 100% { opacity: 0.9; }
          50% { opacity: 1; }
        }
      `);
    }
  }
  
  function addRelaxedEffect(portrait, quote) {
    // Xanny Xan - extremely slow, relaxed movements
    portrait.style.animation = 'xannyFloat 12s ease-in-out infinite';
    addAnimationStyles(`
      @keyframes xannyFloat {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(5px) rotate(2deg); }
      }
    `);
    
    if (quote) {
      quote.style.animation = 'xannyBlur 12s ease-in-out infinite';
      addAnimationStyles(`
        @keyframes xannyBlur {
          0%, 100% { filter: blur(0px); }
          50% { filter: blur(1px); }
        }
      `);
    }
  }
  
  function addHyperEffect(portrait, quote) {
    // Cokehead Carl - rapid, energetic movements
    portrait.style.animation = 'cokeShake 0.3s linear infinite';
    addAnimationStyles(`
      @keyframes cokeShake {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        25% { transform: translate(3px, -3px) rotate(1deg); }
        50% { transform: translate(-3px, 3px) rotate(-1deg); }
        75% { transform: translate(3px, 3px) rotate(0deg); }
      }
    `);
    
    if (quote) {
      quote.style.animation = 'hyperPulse 0.5s linear infinite';
      addAnimationStyles(`
        @keyframes hyperPulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.02); }
        }
      `);
    }
  }
  
  function addTripEffect(portrait, quote) {
    // Shroomy Sal - psychedelic warping
    portrait.style.animation = 'shroomWarp 10s ease-in-out infinite';
    addAnimationStyles(`
      @keyframes shroomWarp {
        0%, 100% { transform: scale(1) rotate(0deg); border-radius: 50%; }
        25% { transform: scale(1.05) rotate(2deg); border-radius: 45%; }
        50% { transform: scale(1.02) rotate(-2deg); border-radius: 52%; }
        75% { transform: scale(1.03) rotate(1deg); border-radius: 48%; }
      }
    `);
    
    if (quote) {
      quote.style.animation = 'colorShift 10s linear infinite';
      addAnimationStyles(`
        @keyframes colorShift {
          0% { text-shadow: 0 0 5px #6f42c1; }
          33% { text-shadow: 0 0 5px #20c997; }
          66% { text-shadow: 0 0 5px #ffc107; }
          100% { text-shadow: 0 0 5px #6f42c1; }
        }
      `);
    }
  }
  
  function addParanoidEffect(portrait, quote) {
    // Crypto Craig - suspicious, paranoid movements
    portrait.style.animation = 'paranoidLook 5s ease-in-out infinite';
    addAnimationStyles(`
      @keyframes paranoidLook {
        0%, 100% { transform: translateX(0) rotate(0deg); }
        20% { transform: translateX(-5px) rotate(-2deg); }
        25% { transform: translateX(-5px) rotate(-2deg); }
        45% { transform: translateX(5px) rotate(2deg); }
        50% { transform: translateX(5px) rotate(2deg); }
        70% { transform: translateX(-3px) rotate(-1deg); }
        75% { transform: translateX(-3px) rotate(-1deg); }
      }
    `);
    
    if (quote) {
      quote.style.animation = 'cryptoShadow 5s ease-in-out infinite';
      addAnimationStyles(`
        @keyframes cryptoShadow {
          0%, 100% { box-shadow: 0 0 10px rgba(32, 201, 151, 0.3); }
          50% { box-shadow: 0 0 15px rgba(32, 201, 151, 0.5); }
        }
      `);
    }
  }
  
  // Helper to add animation styles
  function addAnimationStyles(styleText) {
    // Check if style already exists
    let styleElement = document.getElementById('agent-animations');
    
    if (!styleElement) {
      styleElement = document.createElement('style');
      styleElement.id = 'agent-animations';
      document.head.appendChild(styleElement);
    }
    
    // Append new styles
    styleElement.textContent += styleText;
  }
  
  // Add trippy effect to agent section background
  const agentSection = document.querySelector('.py-5');
  if (agentSection) {
    const trippyBg = document.createElement('div');
    trippyBg.className = 'trippy-background';
    agentSection.prepend(trippyBg);
    
    // Add styles
    addAnimationStyles(`
      .trippy-background {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at 50% 50%, rgba(111, 66, 193, 0.1), transparent 70%);
        pointer-events: none;
        z-index: -1;
        animation: pulse-bg 15s ease-in-out infinite;
      }
      
      @keyframes pulse-bg {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.2); }
      }
    `);
  }
  
  // Add psychedelic-bg.js effects if it's not already loaded
  if (!document.querySelector('script[src*="psychedelic-bg.js"]')) {
    const script = document.createElement('script');
    script.src = '/js/psychedelic-bg.js';
    document.body.appendChild(script);
  }
});