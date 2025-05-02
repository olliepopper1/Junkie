/**
 * Trial Junkie - Referrals Page
 * Handles referral code generation, copying, and statistics display
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const getRefCodeBtn = document.getElementById('get-referral-btn');
  const loadReferralsBtn = document.getElementById('load-referrals-btn');
  const discordIdInput = document.getElementById('discord-id-input');
  const referralCodeSection = document.getElementById('referral-code-section');
  const referralStatsSection = document.getElementById('referral-stats-section');
  const referralCodeDisplay = document.getElementById('referral-code');
  const copyCodeBtn = document.getElementById('copy-code-btn');
  const shareDropdown = document.getElementById('shareDropdown');
  const customShareBtn = document.getElementById('share-custom');
  const copyCustomMessageBtn = document.getElementById('copy-custom-message');
  const customMessageArea = document.getElementById('custom-message');
  const successModal = new bootstrap.Modal(document.getElementById('successModal'));
  const successMessage = document.getElementById('success-message');
  const yourRankRow = document.getElementById('your-rank-row');
  
  // Stats elements
  const totalReferrals = document.getElementById('total-referrals');
  const totalEarnings = document.getElementById('total-earnings');
  const availableBalance = document.getElementById('available-balance');
  const withdrawBtn = document.getElementById('withdraw-btn');
  const yourReferrals = document.getElementById('your-referrals');
  const yourEarnings = document.getElementById('your-earnings');
  
  // Get referral code from the server
  async function fetchReferralCode() {
    try {
      const response = await fetch('/api/referral-code');
      const data = await response.json();
      
      if (data.success) {
        return data.code;
      } else {
        console.error("Error fetching referral code:", data.message);
        return null;
      }
    } catch (error) {
      console.error("Error fetching referral code:", error);
      return null;
    }
  }
  
  // Get referral stats from the server
  async function fetchReferralStats() {
    try {
      const response = await fetch('/api/referral-stats');
      const data = await response.json();
      
      if (data.success) {
        return {
          referrals: data.total_referrals || 0,
          totalEarned: data.total_earned?.toFixed(2) || "0.00",
          paid: data.total_paid?.toFixed(2) || "0.00",
          available: data.available_balance?.toFixed(2) || "0.00",
          active_users: data.active_users || 0,
          tier: data.tier || "Standard",
          next_tier_progress: data.next_tier_progress || 0,
          next_tier_target: data.next_tier_target || 15
        };
      } else {
        console.error("Error fetching referral stats:", data.message);
        return {
          referrals: 0,
          totalEarned: "0.00",
          paid: "0.00",
          available: "0.00",
          active_users: 0,
          tier: "Standard",
          next_tier_progress: 0,
          next_tier_target: 15
        };
      }
    } catch (error) {
      console.error("Error fetching referral stats:", error);
      return {
        referrals: 0,
        totalEarned: "0.00",
        paid: "0.00",
        available: "0.00",
        active_users: 0,
        tier: "Standard",
        next_tier_progress: 0,
        next_tier_target: 15
      };
    }
  }
  
  // Update UI with referral stats
  function updateReferralStats(stats) {
    if (totalReferrals) totalReferrals.textContent = stats.referrals;
    if (totalEarnings) totalEarnings.textContent = `$${stats.totalEarned}`;
    if (availableBalance) availableBalance.textContent = `$${stats.available}`;
    if (yourReferrals) yourReferrals.textContent = stats.referrals;
    if (yourEarnings) yourEarnings.textContent = `$${stats.totalEarned}`;
    
    // Enable withdraw button if available balance > $0
    if (withdrawBtn && parseFloat(stats.available) > 0) {
      withdrawBtn.disabled = false;
    }
    
    // Determine dealer status based on referrals
    let status = 'Starter';
    let statusClass = 'bg-primary';
    
    if (stats.referrals >= 100) {
      status = 'Kingpin';
      statusClass = 'bg-danger';
    } else if (stats.referrals >= 26) {
      status = 'Distributor';
      statusClass = 'bg-warning text-dark';
    }
    
    // Update your status on the leaderboard
    const yourStatus = document.getElementById('your-status');
    if (yourStatus) {
      yourStatus.innerHTML = `<span class="badge ${statusClass}">${status}</span>`;
    }
    
    // Show your rank on the leaderboard
    if (yourRankRow) {
      yourRankRow.classList.remove('d-none');
      
      // Calculate mock rank
      let rank = 0;
      if (stats.referrals < 10) rank = Math.floor(Math.random() * 20) + 30;
      else if (stats.referrals < 50) rank = Math.floor(Math.random() * 15) + 10;
      else if (stats.referrals < 100) rank = Math.floor(Math.random() * 5) + 6;
      else rank = Math.floor(Math.random() * 3) + 3;
      
      // Update rank
      const yourRank = document.getElementById('your-rank');
      if (yourRank) yourRank.textContent = rank;
      
      // Update member since date
      const memberSince = document.getElementById('member-since');
      if (memberSince) {
        const date = new Date();
        memberSince.textContent = `Since ${date.toLocaleString('default', { month: 'short' })} ${date.getFullYear()}`;
      }
    }
  }
  
  // UI Event Handlers
  if (getRefCodeBtn) {
    getRefCodeBtn.addEventListener('click', async () => {
      // Don't need Discord ID input anymore since we'll get the code from the server
      // Disable the button while processing
      getRefCodeBtn.disabled = true;
      getRefCodeBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
      
      try {
        // Fetch the referral code from the server
        const code = await fetchReferralCode();
        if (!code) {
          console.error("Failed to get referral code");
          getRefCodeBtn.disabled = false;
          getRefCodeBtn.textContent = 'Get Referral Code';
          return;
        }
        
        // Display the referral code
        referralCodeDisplay.textContent = code;
        
        // Show the referral code section with a fade-in effect
        referralCodeSection.classList.remove('d-none');
        referralCodeSection.style.opacity = '0';
        setTimeout(() => {
          referralCodeSection.style.transition = 'opacity 0.5s ease-in-out';
          referralCodeSection.style.opacity = '1';
        }, 50);
        
        // Scroll to the referral code section
        referralCodeSection.scrollIntoView({ behavior: 'smooth' });
        
        // Load stats too
        const stats = await fetchReferralStats();
        updateReferralStats(stats);
        
        // Show the stats section
        referralStatsSection.classList.remove('d-none');
        
        // Add pill-themed effects
        document.querySelectorAll('.card').forEach(card => {
          card.classList.add('glow-effect');
        });
      } catch (error) {
        console.error("Error getting referral information:", error);
      } finally {
        // Re-enable button
        getRefCodeBtn.disabled = false;
        getRefCodeBtn.textContent = 'Get Referral Code';
      }
    });
  }
  
  if (loadReferralsBtn) {
    loadReferralsBtn.addEventListener('click', async () => {
      // Disable the button while processing
      loadReferralsBtn.disabled = true;
      loadReferralsBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
      
      try {
        // Fetch the referral code from the server
        const code = await fetchReferralCode();
        if (!code) {
          console.error("Failed to get referral code");
          loadReferralsBtn.disabled = false;
          loadReferralsBtn.textContent = 'Load My Referrals';
          return;
        }
        
        // Display the referral code
        referralCodeDisplay.textContent = code;
        
        // Show the referral code section
        referralCodeSection.classList.remove('d-none');
        
        // Load stats from server
        const stats = await fetchReferralStats();
        updateReferralStats(stats);
        
        // Show the stats section
        referralStatsSection.classList.remove('d-none');
        
        // Add pill-themed effects
        document.querySelectorAll('.card').forEach(card => {
          card.classList.add('glow-effect');
        });
      } catch (error) {
        console.error("Error loading referral information:", error);
      } finally {
        // Re-enable button
        loadReferralsBtn.disabled = false;
        loadReferralsBtn.textContent = 'Load My Referrals';
      }
    });
  }
  
  // Copy referral code button
  if (copyCodeBtn) {
    copyCodeBtn.addEventListener('click', () => {
      const code = referralCodeDisplay.textContent;
      navigator.clipboard.writeText(code).then(() => {
        // Show success message
        successMessage.textContent = 'Referral code copied to clipboard!';
        successModal.show();
        
        // Add particle effects to the button
        const button = copyCodeBtn;
        for (let i = 0; i < 5; i++) {
          const particle = document.createElement('div');
          particle.className = 'mini-particle';
          button.appendChild(particle);
          
          // Random color from our drug theme
          const colors = ['#6f42c1', '#20c997', '#ffc107', '#dc3545'];
          const color = colors[Math.floor(Math.random() * colors.length)];
          
          particle.style.backgroundColor = color;
          particle.style.boxShadow = `0 0 5px ${color}`;
          
          // Remove after animation completes
          setTimeout(() => {
            if (particle.parentNode === button) {
              button.removeChild(particle);
            }
          }, 2000);
        }
      });
    });
  }
  
  // Share dropdown handlers
  const shareButtons = document.querySelectorAll('#shareDropdown .dropdown-item');
  shareButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      
      const platform = button.id.replace('share-', '');
      const code = referralCodeDisplay.textContent;
      
      let shareUrl = '';
      let shareText = encodeURIComponent(`Get your digital fix with Trial Junkie! Use my referral code ${code} to start generating free trials.`);
      
      switch (platform) {
        case 'discord':
          // For Discord, we just copy a formatted message
          navigator.clipboard.writeText(`Get your digital fix with Trial Junkie! Use my referral code **${code}** to start generating free trials. Join at https://discord.gg/trialjunkie`);
          successMessage.textContent = 'Discord message copied to clipboard!';
          successModal.show();
          break;
        case 'twitter':
          shareUrl = `https://twitter.com/intent/tweet?text=${shareText}`;
          window.open(shareUrl, '_blank');
          break;
        case 'telegram':
          shareUrl = `https://t.me/share/url?url=https://trialjunkie.com&text=${shareText}`;
          window.open(shareUrl, '_blank');
          break;
        case 'custom':
          // Show custom message modal
          const customModal = new bootstrap.Modal(document.getElementById('customShareModal'));
          customModal.show();
          
          // Replace placeholder with actual code
          const text = customMessageArea.value;
          customMessageArea.value = text.replace('{CODE}', code);
          break;
      }
    });
  });
  
  // Custom message copy button
  if (copyCustomMessageBtn) {
    copyCustomMessageBtn.addEventListener('click', () => {
      const text = customMessageArea.value;
      navigator.clipboard.writeText(text).then(() => {
        // Hide the custom modal
        bootstrap.Modal.getInstance(document.getElementById('customShareModal')).hide();
        
        // Show success message
        successMessage.textContent = 'Custom message copied to clipboard!';
        successModal.show();
      });
    });
  }
  
  // Add psychedelic background effects
  const referralCodeContainer = document.querySelector('.ref-card-glow');
  if (referralCodeContainer) {
    // Add floating particles
    for (let i = 0; i < 5; i++) {
      const particle = document.createElement('div');
      particle.className = 'floating-particle';
      
      // Random properties
      const size = Math.random() * 10 + 5;
      const posX = Math.random() * 100;
      const posY = Math.random() * 100;
      const color = '#6f42c1';
      
      // Apply styles
      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;
      particle.style.left = `${posX}%`;
      particle.style.top = `${posY}%`;
      particle.style.backgroundColor = color;
      particle.style.boxShadow = `0 0 ${size}px ${color}`;
      particle.style.opacity = '0.5';
      particle.style.position = 'absolute';
      particle.style.borderRadius = '50%';
      particle.style.animation = `float ${5 + Math.random() * 5}s ease-in-out infinite alternate`;
      
      referralCodeContainer.appendChild(particle);
    }
  }
  
  // Add keyframes for particle animation if they don't exist yet
  if (!document.getElementById('referral-animations')) {
    const styleElement = document.createElement('style');
    styleElement.id = 'referral-animations';
    styleElement.textContent = `
      @keyframes float {
        0% {
          transform: translateY(0) translateX(0);
        }
        50% {
          transform: translateY(-20px) translateX(10px);
        }
        100% {
          transform: translateY(0) translateX(0);
        }
      }
      
      .mini-particle {
        position: absolute;
        width: 5px;
        height: 5px;
        border-radius: 50%;
        animation: mini-float 2s ease-out forwards;
        opacity: 0.7;
        pointer-events: none;
      }
      
      @keyframes mini-float {
        0% {
          transform: translate(0, 0) scale(0);
          opacity: 0.7;
        }
        100% {
          transform: translate(
            calc(${Math.random() * 100 - 50}px), 
            calc(${Math.random() * 100 - 50}px)
          ) scale(1);
          opacity: 0;
        }
      }
      
      .glow-effect {
        animation: glow 2s infinite alternate;
      }
      
      @keyframes glow {
        0% {
          box-shadow: 0 0 5px var(--primary-purple);
        }
        100% {
          box-shadow: 0 0 20px var(--primary-purple);
        }
      }
    `;
    document.head.appendChild(styleElement);
  }
  
  // Add the psychedelic background script if it's not already loaded
  if (!document.querySelector('script[src*="psychedelic-bg.js"]')) {
    const script = document.createElement('script');
    script.src = '/js/psychedelic-bg.js';
    document.body.appendChild(script);
  }
});