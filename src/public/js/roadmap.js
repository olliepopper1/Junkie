/**
 * Trial Junkie - Roadmap Page
 * Adds interactive elements and animations to the roadmap timeline
 */

document.addEventListener('DOMContentLoaded', () => {
  // Add scroll animations to roadmap phases
  const roadmapPhases = document.querySelectorAll('.roadmap-phase');
  
  // Intersection Observer for scroll animations
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
        
        // Add staggered animation to features
        const features = entry.target.querySelectorAll('.feature-item');
        features.forEach((feature, index) => {
          setTimeout(() => {
            feature.classList.add('animate-in');
          }, 100 * index);
        });
      }
    });
  }, {
    threshold: 0.2
  });
  
  // Observe roadmap phases
  roadmapPhases.forEach(phase => {
    observer.observe(phase);
  });
  
  // Add animation styles
  const style = document.createElement('style');
  style.textContent = `
    .roadmap-phase {
      opacity: 0;
      transform: translateY(20px);
      transition: opacity 0.5s ease-out, transform 0.5s ease-out;
    }
    
    .roadmap-phase.animate-in {
      opacity: 1;
      transform: translateY(0);
    }
    
    .feature-item {
      opacity: 0;
      transform: translateX(-10px);
      transition: opacity 0.3s ease-out, transform 0.3s ease-out;
    }
    
    .feature-item.animate-in {
      opacity: 1;
      transform: translateX(0);
    }
    
    /* Enhance the phase dots with animations */
    .phase-dot {
      transition: transform 0.3s ease-out;
    }
    
    .roadmap-phase:hover .phase-dot {
      transform: translateX(-60%) scale(1.2);
    }
    
    /* Add interaction to feature vote items */
    .feature-vote-item {
      transition: background-color 0.3s ease;
    }
    
    .feature-vote-item:hover {
      background-color: rgba(111, 66, 193, 0.1);
    }
    
    /* Make agent previews interactive */
    .agent-preview {
      transition: transform 0.3s ease;
    }
    
    .agent-preview:hover {
      transform: scale(1.1);
    }
  `;
  document.head.appendChild(style);
  
  // Add voting functionality
  const voteButtons = document.querySelectorAll('.feature-vote-item .btn');
  
  voteButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const voteItem = e.target.closest('.feature-vote-item');
      const progressBar = voteItem.querySelector('.progress-bar');
      const progressText = voteItem.querySelector('small:first-child');
      
      // Get current votes
      let votes = parseInt(progressText.textContent);
      
      // Increment votes
      votes++;
      
      // Update progress
      progressText.textContent = `${votes} votes`;
      progressBar.style.width = `${votes}%`;
      
      // Disable button
      button.disabled = true;
      button.textContent = 'Voted';
      button.classList.remove('btn-primary');
      button.classList.add('btn-success');
      
      // Add particle effects
      addParticleEffects(button);
    });
  });
  
  // Add trippy effects to the lab preview
  const labPreview = document.querySelector('.lab-preview');
  if (labPreview) {
    labPreview.addEventListener('mouseenter', () => {
      labPreview.classList.add('lab-glow');
    });
    
    labPreview.addEventListener('mouseleave', () => {
      labPreview.classList.remove('lab-glow');
    });
    
    // Add lab glow styles
    const labStyle = document.createElement('style');
    labStyle.textContent = `
      .lab-glow {
        filter: drop-shadow(0 0 10px #6f42c1);
        transition: filter 0.5s ease;
      }
    `;
    document.head.appendChild(labStyle);
  }
  
  // Helper function to add particle effects
  function addParticleEffects(element) {
    for (let i = 0; i < 5; i++) {
      const particle = document.createElement('div');
      particle.className = 'vote-particle';
      
      // Random properties
      const size = Math.random() * 8 + 4;
      const angle = Math.random() * Math.PI * 2;
      const distance = Math.random() * 50 + 20;
      const duration = Math.random() * 1 + 1;
      
      // Calculate end position
      const x = Math.cos(angle) * distance;
      const y = Math.sin(angle) * distance;
      
      // Apply styles
      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;
      particle.style.backgroundColor = '#6f42c1';
      particle.style.position = 'absolute';
      particle.style.borderRadius = '50%';
      particle.style.left = '50%';
      particle.style.top = '50%';
      particle.style.transform = 'translate(-50%, -50%)';
      particle.style.zIndex = '10';
      
      // Add to button
      element.style.position = 'relative';
      element.style.overflow = 'visible';
      element.appendChild(particle);
      
      // Animate
      particle.animate([
        {
          transform: 'translate(-50%, -50%)',
          opacity: 1
        },
        {
          transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`,
          opacity: 0
        }
      ], {
        duration: duration * 1000,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
        fill: 'forwards'
      });
      
      // Clean up after animation
      setTimeout(() => {
        if (particle.parentNode) {
          particle.parentNode.removeChild(particle);
        }
      }, duration * 1000);
    }
  }
  
  // Add scroll tracking for the roadmap line
  window.addEventListener('scroll', () => {
    const timeline = document.querySelector('.roadmap-timeline');
    if (!timeline) return;
    
    const timelineTop = timeline.getBoundingClientRect().top;
    const timelineHeight = timeline.offsetHeight;
    const windowHeight = window.innerHeight;
    
    // Calculate how far down the timeline we've scrolled (0 to 1)
    let scrollProgress = 0;
    
    if (timelineTop < windowHeight && timelineTop + timelineHeight > 0) {
      // Timeline is visible
      scrollProgress = Math.min(1, Math.max(0, 
        (windowHeight - timelineTop) / (windowHeight + timelineHeight)
      ));
    }
    
    // Apply a gradient to the timeline based on scroll progress
    const line = document.querySelector('.roadmap-timeline::before');
    if (line) {
      line.style.background = `linear-gradient(
        to bottom,
        var(--primary-purple) 0%,
        var(--primary-purple) ${scrollProgress * 20}%,
        var(--secondary-green) ${scrollProgress * 20}%,
        var(--secondary-green) ${scrollProgress * 40}%,
        var(--info-blue) ${scrollProgress * 40}%,
        var(--info-blue) ${scrollProgress * 60}%,
        var(--warning-yellow) ${scrollProgress * 60}%,
        var(--warning-yellow) ${scrollProgress * 80}%,
        var(--danger-red) ${scrollProgress * 80}%,
        var(--danger-red) 100%
      )`;
    }
  });
  
  // Add psychedelic background effects if not already loaded
  if (!document.querySelector('script[src*="psychedelic-bg.js"]')) {
    const script = document.createElement('script');
    script.src = '/js/psychedelic-bg.js';
    document.body.appendChild(script);
  }
});