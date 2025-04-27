// Trials JavaScript

document.addEventListener('DOMContentLoaded', function() {
  console.log('Trial Junkie Trials Page Initialized');
  
  // Elements
  const discordIdInput = document.getElementById('discord-id-input');
  const loadTrialsBtn = document.getElementById('load-trials-btn');
  const serviceFilter = document.getElementById('service-filter');
  const statusFilter = document.getElementById('status-filter');
  const searchInput = document.getElementById('search-input');
  const searchBtn = document.getElementById('search-btn');
  const sortBy = document.getElementById('sort-by');
  const trialsContainer = document.getElementById('trials-container');
  const emptyState = document.getElementById('empty-state');
  const trialCardTemplate = document.getElementById('trial-card-template');
  
  // Modal elements
  const trialDetailsModal = document.getElementById('trialDetailsModal');
  const modalServiceName = document.getElementById('modal-service-name');
  const modalServiceIcon = document.getElementById('modal-service-icon');
  const modalServicePlan = document.getElementById('modal-service-plan');
  const modalStatusBadge = document.getElementById('modal-status-badge');
  const modalExpiryAlert = document.getElementById('modal-expiry-alert');
  const modalDaysRemaining = document.getElementById('modal-days-remaining');
  const modalEmail = document.getElementById('modal-email');
  const modalPassword = document.getElementById('modal-password');
  const modalLoginLink = document.getElementById('modal-login-link');
  const modalCreatedDate = document.getElementById('modal-created-date');
  const modalExpiryDate = document.getElementById('modal-expiry-date');
  const modalTrialLength = document.getElementById('modal-trial-length');
  const modalCredentialsTable = document.getElementById('modal-credentials-table');
  
  // Check for saved Discord ID
  const savedDiscordId = localStorage.getItem('discordId');
  if (savedDiscordId) {
    discordIdInput.value = savedDiscordId;
  }
  
  // Event listeners
  loadTrialsBtn.addEventListener('click', loadTrials);
  serviceFilter.addEventListener('change', filterTrials);
  statusFilter.addEventListener('change', filterTrials);
  searchBtn.addEventListener('click', filterTrials);
  searchInput.addEventListener('keyup', function(e) {
    if (e.key === 'Enter') {
      filterTrials();
    }
  });
  sortBy.addEventListener('change', sortTrials);
  
  // Copy button functionality
  document.addEventListener('click', function(e) {
    if (e.target.closest('.copy-btn')) {
      const btn = e.target.closest('.copy-btn');
      const targetId = btn.getAttribute('data-target');
      const targetInput = targetId ? document.getElementById(targetId) : btn.previousElementSibling;
      
      if (targetInput) {
        copyToClipboard(targetInput.value);
        showCopiedTooltip(btn);
      }
    }
  });
  
  // Toggle password visibility
  document.addEventListener('click', function(e) {
    if (e.target.closest('.toggle-password-btn')) {
      const btn = e.target.closest('.toggle-password-btn');
      const targetId = btn.getAttribute('data-target');
      const targetInput = targetId ? document.getElementById(targetId) : btn.previousElementSibling;
      
      if (targetInput) {
        const type = targetInput.getAttribute('type');
        targetInput.setAttribute('type', type === 'password' ? 'text' : 'password');
        
        // Toggle icon
        const icon = btn.querySelector('i');
        if (icon) {
          icon.className = type === 'password' ? 'bi bi-eye-slash' : 'bi bi-eye';
        }
      }
    }
  });
  
  // View details button click
  document.addEventListener('click', function(e) {
    if (e.target.closest('.view-details-btn')) {
      const btn = e.target.closest('.view-details-btn');
      const card = btn.closest('.trial-card');
      const trialData = card.trialData;
      
      openTrialDetailsModal(trialData);
    }
  });
  
  // Auto-load if Discord ID is present
  if (savedDiscordId) {
    loadTrials();
  }
  
  // Functions
  function loadTrials() {
    const discordId = discordIdInput.value.trim();
    
    if (!discordId) {
      showToast('Please enter your Discord ID', 'warning');
      return;
    }
    
    // Save for future use
    localStorage.setItem('discordId', discordId);
    
    // Show loading state
    trialsContainer.innerHTML = `
      <div class="col-12 text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3">Loading your trials...</p>
      </div>
    `;
    
    // Fetch trials
    fetch(`/api/trials/${discordId}`)
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          if (data.trials && data.trials.length > 0) {
            renderTrials(data.trials);
            emptyState.classList.add('d-none');
          } else {
            trialsContainer.innerHTML = '';
            emptyState.classList.remove('d-none');
          }
        } else {
          showToast(`Error: ${data.error || 'Failed to load trials'}`, 'danger');
          trialsContainer.innerHTML = `
            <div class="col-12 text-center py-5">
              <i class="bi bi-exclamation-triangle-fill display-1 text-warning"></i>
              <h2 class="mt-4">Error Loading Trials</h2>
              <p class="text-muted">${data.error || 'Failed to load trials'}</p>
              <button class="btn btn-primary mt-3" onclick="loadTrials()">Try Again</button>
            </div>
          `;
        }
      })
      .catch(error => {
        console.error('Error loading trials:', error);
        showToast(`Error: ${error.message}`, 'danger');
        trialsContainer.innerHTML = `
          <div class="col-12 text-center py-5">
            <i class="bi bi-exclamation-triangle-fill display-1 text-warning"></i>
            <h2 class="mt-4">Error Loading Trials</h2>
            <p class="text-muted">${error.message}</p>
            <button class="btn btn-primary mt-3" onclick="loadTrials()">Try Again</button>
          </div>
        `;
      });
  }
  
  function renderTrials(trials) {
    trialsContainer.innerHTML = '';
    
    // Sort trials
    sortTrialsByOption(trials, sortBy.value);
    
    // Create trial cards
    trials.forEach(trial => {
      const trialCard = createTrialCard(trial);
      trialsContainer.appendChild(trialCard);
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }
  
  function createTrialCard(trial) {
    const clone = trialCardTemplate.content.cloneNode(true);
    const card = clone.querySelector('.trial-card');
    
    // Store trial data on the card element
    card.trialData = trial;
    
    // Set service icon
    const serviceIcon = clone.querySelector('.trial-service-icon');
    serviceIcon.src = getServiceIconUrl(trial.service);
    serviceIcon.alt = `${trial.service} Icon`;
    
    // Set service name
    clone.querySelector('.trial-service-name').textContent = formatServiceName(trial.service);
    
    // Set plan
    const planElement = clone.querySelector('.trial-plan');
    planElement.textContent = trial.plan || '';
    
    // Set status badge
    const statusBadge = clone.querySelector('.trial-status-badge');
    const isActive = !isExpired(trial.expires_at);
    statusBadge.innerHTML = `<span class="badge ${isActive ? 'bg-success' : 'bg-danger'}">${isActive ? 'Active' : 'Expired'}</span>`;
    
    // Set expiry
    const expiryElement = clone.querySelector('.trial-expiry');
    if (trial.expires_at) {
      const daysRemaining = getDaysRemaining(trial.expires_at);
      expiryElement.textContent = isActive
        ? `Expires in ${daysRemaining} day${daysRemaining !== 1 ? 's' : ''}`
        : `Expired on ${formatDate(trial.expires_at)}`;
    } else {
      expiryElement.textContent = 'No expiration date';
    }
    
    // Set email and password
    const emailInput = clone.querySelector('.trial-email');
    const passwordInput = clone.querySelector('.trial-password');
    emailInput.value = trial.email || trial.credentials?.email || '';
    passwordInput.value = trial.password || trial.credentials?.password || '';
    
    return clone;
  }
  
  function openTrialDetailsModal(trial) {
    // Set service info
    modalServiceName.textContent = formatServiceName(trial.service);
    modalServiceIcon.src = getServiceIconUrl(trial.service);
    modalServicePlan.textContent = trial.plan || '';
    
    // Set status
    const isActive = !isExpired(trial.expires_at);
    modalStatusBadge.className = `badge ${isActive ? 'bg-success' : 'bg-danger'} mb-3`;
    modalStatusBadge.textContent = isActive ? 'Active' : 'Expired';
    
    // Expiry alert
    if (isActive && trial.expires_at) {
      const daysRemaining = getDaysRemaining(trial.expires_at);
      if (daysRemaining <= 7) {
        modalExpiryAlert.classList.remove('d-none');
        modalDaysRemaining.textContent = daysRemaining;
      } else {
        modalExpiryAlert.classList.add('d-none');
      }
    } else {
      modalExpiryAlert.classList.add('d-none');
    }
    
    // Set login details
    modalEmail.value = trial.email || trial.credentials?.email || '';
    modalPassword.value = trial.password || trial.credentials?.password || '';
    
    // Set login link
    modalLoginLink.href = getServiceLoginUrl(trial.service);
    
    // Set dates
    modalCreatedDate.textContent = formatDate(trial.created_at);
    modalExpiryDate.textContent = formatDate(trial.expires_at) || 'No expiration';
    
    // Set trial length
    let trialLength = 'Unknown';
    if (trial.expires_at && trial.created_at) {
      const startDate = new Date(trial.created_at);
      const endDate = new Date(trial.expires_at);
      const days = Math.round((endDate - startDate) / (1000 * 60 * 60 * 24));
      trialLength = `${days} day${days !== 1 ? 's' : ''}`;
    }
    modalTrialLength.textContent = trialLength;
    
    // Set credentials table
    modalCredentialsTable.innerHTML = '';
    if (trial.credentials) {
      Object.entries(trial.credentials).forEach(([key, value]) => {
        // Skip email and password as they're shown above
        if (key === 'email' || key === 'password') return;
        
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${formatCredentialType(key)}</td>
          <td>
            <div class="input-group">
              <input type="text" class="form-control bg-dark border-0" value="${value}" readonly>
            </div>
          </td>
          <td>
            <button class="btn btn-sm btn-outline-primary copy-btn" data-bs-toggle="tooltip" title="Copy to clipboard">
              <i class="bi bi-clipboard"></i>
            </button>
          </td>
        `;
        modalCredentialsTable.appendChild(row);
      });
    }
    
    // If no additional credentials
    if (modalCredentialsTable.children.length === 0) {
      modalCredentialsTable.innerHTML = `
        <tr>
          <td colspan="3" class="text-center">No additional credentials</td>
        </tr>
      `;
    }
    
    // Show modal
    const modal = new bootstrap.Modal(trialDetailsModal);
    modal.show();
  }
  
  function filterTrials() {
    const service = serviceFilter.value;
    const status = statusFilter.value;
    const searchQuery = searchInput.value.toLowerCase();
    
    // Get all trial cards
    const cards = document.querySelectorAll('.trial-card');
    
    cards.forEach(card => {
      const trial = card.trialData;
      
      // Service filter
      const serviceMatch = service === 'all' || trial.service.toLowerCase() === service.toLowerCase();
      
      // Status filter
      let statusMatch = true;
      if (status !== 'all') {
        const isTrialActive = !isExpired(trial.expires_at);
        const isExpiringSoon = isTrialActive && getDaysRemaining(trial.expires_at) <= 7;
        
        statusMatch = (status === 'active' && isTrialActive && !isExpiringSoon) ||
                      (status === 'expired' && !isTrialActive) ||
                      (status === 'expiring' && isExpiringSoon);
      }
      
      // Search filter
      const searchMatch = !searchQuery || 
        trial.service.toLowerCase().includes(searchQuery) ||
        (trial.email && trial.email.toLowerCase().includes(searchQuery)) ||
        (trial.plan && trial.plan.toLowerCase().includes(searchQuery));
      
      // Show or hide
      if (serviceMatch && statusMatch && searchMatch) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
    
    // Check if any visible cards
    const visibleCards = document.querySelectorAll('.trial-card[style=""]');
    if (visibleCards.length === 0) {
      if (cards.length > 0) {
        // No matches
        const noMatchesEl = document.createElement('div');
        noMatchesEl.className = 'col-12 text-center py-5 no-matches';
        noMatchesEl.innerHTML = `
          <i class="bi bi-search display-1 text-muted"></i>
          <h2 class="mt-4">No Matching Trials</h2>
          <p class="text-muted">Try adjusting your filters</p>
          <button class="btn btn-primary mt-3" onclick="resetFilters()">Reset Filters</button>
        `;
        
        // Remove any existing no-matches element
        document.querySelector('.no-matches')?.remove();
        
        // Append to container
        trialsContainer.appendChild(noMatchesEl);
      }
    } else {
      // Remove no-matches element if it exists
      document.querySelector('.no-matches')?.remove();
    }
  }
  
  function sortTrials() {
    const trials = Array.from(document.querySelectorAll('.trial-card'))
      .map(card => card.trialData);
    
    renderTrials(trials);
  }
  
  function sortTrialsByOption(trials, option) {
    switch (option) {
      case 'newest':
        return trials.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      case 'oldest':
        return trials.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
      case 'expiry':
        return trials.sort((a, b) => {
          // Put nulls at the end
          if (!a.expires_at) return 1;
          if (!b.expires_at) return -1;
          return new Date(a.expires_at) - new Date(b.expires_at);
        });
      default:
        return trials;
    }
  }
  
  // Utility functions
  function isExpired(dateString) {
    if (!dateString) return false;
    const expiryDate = new Date(dateString);
    return expiryDate < new Date();
  }
  
  function getDaysRemaining(dateString) {
    if (!dateString) return 0;
    const expiryDate = new Date(dateString);
    const today = new Date();
    const timeDiff = expiryDate - today;
    return Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
  }
  
  function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
  }
  
  function formatServiceName(service) {
    if (!service) return 'Unknown Service';
    
    // Handle special cases
    switch (service.toLowerCase()) {
      case 'netflix':
      case 'spotify':
      case 'hulu':
      case 'disney':
        return service.charAt(0).toUpperCase() + service.slice(1);
      case 'youtube':
        return 'YouTube Premium';
      default:
        // Capitalize each word
        return service
          .split(' ')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1))
          .join(' ');
    }
  }
  
  function formatCredentialType(type) {
    if (!type) return '';
    
    // Replace underscores with spaces and capitalize each word
    return type
      .replace(/_/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
  
  function getServiceIconUrl(service) {
    // This would ideally come from a proper icon library
    const defaultIcon = '/img/default-service.svg';
    
    if (!service) return defaultIcon;
    
    // For now, just return placeholder path (you'll need to create these icons)
    switch (service.toLowerCase()) {
      case 'netflix':
        return '/img/netflix-icon.svg';
      case 'hulu':
        return '/img/hulu-icon.svg';
      case 'disney':
        return '/img/disney-icon.svg';
      case 'spotify':
        return '/img/spotify-icon.svg';
      case 'youtube':
        return '/img/youtube-icon.svg';
      default:
        return defaultIcon;
    }
  }
  
  function getServiceLoginUrl(service) {
    // Return the login URL for the service
    if (!service) return '#';
    
    switch (service.toLowerCase()) {
      case 'netflix':
        return 'https://www.netflix.com/login';
      case 'hulu':
        return 'https://www.hulu.com/welcome';
      case 'disney':
        return 'https://www.disneyplus.com/login';
      case 'spotify':
        return 'https://accounts.spotify.com/login';
      case 'youtube':
        return 'https://www.youtube.com/';
      default:
        // Try to form a URL but fall back to hash
        try {
          if (service.includes('.')) {
            return `https://${service}`;
          }
          return `https://www.${service}.com`;
        } catch (e) {
          return '#';
        }
    }
  }
  
  function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
      .then(() => console.log('Copied to clipboard'))
      .catch(err => console.error('Error copying to clipboard:', err));
  }
  
  function showCopiedTooltip(element) {
    // Get existing tooltip
    let tooltip = bootstrap.Tooltip.getInstance(element);
    
    // If tooltip exists, dispose it
    if (tooltip) {
      tooltip.dispose();
    }
    
    // Create new tooltip
    tooltip = new bootstrap.Tooltip(element, {
      title: 'Copied!',
      trigger: 'manual',
      placement: 'top'
    });
    
    // Show tooltip
    tooltip.show();
    
    // Hide after delay
    setTimeout(() => {
      tooltip.hide();
      
      // Restore original tooltip after hiding
      setTimeout(() => {
        tooltip.dispose();
        new bootstrap.Tooltip(element, {
          title: 'Copy to clipboard',
          trigger: 'hover focus'
        });
      }, 150);
    }, 1000);
  }
  
  function showToast(message, type = 'info') {
    // Create toast element
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    
    toastEl.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">
          ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    `;
    
    // Add to container
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
      document.body.appendChild(toastContainer);
    }
    
    toastContainer.appendChild(toastEl);
    
    // Initialize and show toast
    const toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 5000 });
    toast.show();
    
    // Remove from DOM after hidden
    toastEl.addEventListener('hidden.bs.toast', () => {
      toastEl.remove();
    });
  }
  
  // Make resetFilters globally available
  window.resetFilters = function() {
    serviceFilter.value = 'all';
    statusFilter.value = 'all';
    searchInput.value = '';
    sortBy.value = 'newest';
    
    // Refilter trials
    filterTrials();
  };
});