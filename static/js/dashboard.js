// Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
  console.log('Trial Junkie Dashboard Initialized');
  
  // Elements
  const commandItems = document.querySelectorAll('.command-item');
  const commandForm = document.getElementById('command-form');
  const commandNameInput = document.getElementById('command-name');
  const commandArgsInput = document.getElementById('command-args');
  const discordIdInput = document.getElementById('discord-id');
  const executeCommandBtn = document.getElementById('execute-command-btn');
  
  // Saved Discord ID in local storage
  const savedDiscordId = localStorage.getItem('discordId');
  if (savedDiscordId) {
    discordIdInput.value = savedDiscordId;
    loadUserData(savedDiscordId);
  } else {
    // Show a toast or message to enter Discord ID
    showMessage('Please enter your Discord ID to view your dashboard data', 'warning');
  }
  
  // Event Listeners
  commandItems.forEach(item => {
    item.addEventListener('click', function(e) {
      e.preventDefault();
      const command = this.getAttribute('data-command');
      openCommandModal(command);
    });
  });
  
  executeCommandBtn.addEventListener('click', executeCommand);
  
  // Functions
  function openCommandModal(command) {
    commandNameInput.value = command;
    
    // Set placeholder based on command
    switch (command) {
      case 'hit':
        commandArgsInput.placeholder = 'service name (e.g., netflix, hulu, spotify)';
        break;
      case 'dose':
        commandArgsInput.placeholder = 'agent type service (e.g., identity hulu)';
        break;
      case 'trip':
        commandArgsInput.placeholder = 'URL or service name';
        break;
      default:
        commandArgsInput.placeholder = '';
        break;
    }
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('commandModal'));
    modal.show();
  }
  
  function executeCommand() {
    const command = commandNameInput.value;
    const args = commandArgsInput.value;
    const discordId = discordIdInput.value;
    
    if (!discordId) {
      showMessage('Please enter your Discord ID', 'danger');
      return;
    }
    
    // Save Discord ID for future use
    localStorage.setItem('discordId', discordId);
    
    // Prepare request data
    const requestData = {
      userId: discordId,
      username: 'WebUser',
      command: command,
      args: args ? args.split(' ') : []
    };
    
    // Show loading state
    executeCommandBtn.disabled = true;
    executeCommandBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Executing...';
    
    // Execute command
    fetch('/bot/command', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
      // Reset button state
      executeCommandBtn.disabled = false;
      executeCommandBtn.innerHTML = 'Execute';
      
      // Close modal
      const modal = bootstrap.Modal.getInstance(document.getElementById('commandModal'));
      modal.hide();
      
      if (data.success) {
        showMessage('Command executed successfully!', 'success');
        // Refresh data
        loadUserData(discordId);
      } else {
        showMessage(`Error: ${data.error}`, 'danger');
      }
    })
    .catch(error => {
      executeCommandBtn.disabled = false;
      executeCommandBtn.innerHTML = 'Execute';
      showMessage(`Error: ${error.message}`, 'danger');
    });
  }
  
  function loadUserData(discordId) {
    // Show loading indicators
    document.getElementById('username').innerText = 'Loading...';
    document.getElementById('user-discord-id').innerText = `Discord ID: ${discordId}`;
    document.getElementById('tier-badge').innerText = 'Loading...';
    document.getElementById('join-date').innerText = 'Loading...';
    document.getElementById('trial-count').innerText = 'Loading...';
    document.getElementById('subscription-status').innerText = 'Loading...';
    document.getElementById('active-trials-count').innerText = '...';
    document.getElementById('referrals-count').innerText = '...';
    document.getElementById('commission-amount').innerText = '...';
    document.getElementById('daily-allowance').innerText = '...';
    document.getElementById('activity-table-body').innerHTML = '<tr><td colspan="3" class="text-center">Loading activity...</td></tr>';
    
    // Load user data from API
    Promise.all([
      fetch(`/api/stats/${discordId}`).then(r => r.json()),
      fetch(`/api/trials/${discordId}`).then(r => r.json()),
      fetch(`/api/tier/${discordId}`).then(r => r.json()),
      fetch(`/api/referrals/${discordId}`).then(r => r.json())
    ])
    .then(([statsData, trialsData, tierData, referralsData]) => {
      // Process stats data
      if (statsData.success && statsData.stats) {
        const stats = statsData.stats;
        document.getElementById('username').innerText = stats.username || 'Unknown User';
        document.getElementById('join-date').innerText = formatDate(stats.created_at);
        document.getElementById('trial-count').innerText = stats.total_credentials || 0;
        document.getElementById('daily-allowance').innerText = `${stats.today_usage || 0}/${getTierLimit(tierData.tier?.name || 'basic')}`;
        
        // Fill activity table
        const activityTableBody = document.getElementById('activity-table-body');
        activityTableBody.innerHTML = '';
        
        if (stats.recent_commands && stats.recent_commands.length > 0) {
          stats.recent_commands.forEach(cmd => {
            const row = document.createElement('tr');
            row.innerHTML = `
              <td><strong>!${cmd.command}</strong> ${cmd.parameters || ''}</td>
              <td>${formatDate(cmd.timestamp)}</td>
              <td><span class="badge ${cmd.status === 'success' ? 'bg-success' : 'bg-danger'}">${cmd.status}</span></td>
            `;
            activityTableBody.appendChild(row);
          });
        } else {
          activityTableBody.innerHTML = '<tr><td colspan="3" class="text-center">No recent activity</td></tr>';
        }
      }
      
      // Process trials data
      if (trialsData.success) {
        const trials = trialsData.trials || [];
        const activeTrials = trials.filter(t => !isExpired(t.expires_at));
        document.getElementById('active-trials-count').innerText = activeTrials.length;
      }
      
      // Process tier data
      if (tierData.success && tierData.tier) {
        const tier = tierData.tier;
        document.getElementById('tier-badge').innerText = tier.name || 'Basic';
        document.getElementById('tier-badge').className = `badge ${getTierBadgeClass(tier.name || 'basic')}`;
        document.getElementById('subscription-status').innerText = tier.expires_at ? `Expires ${formatDate(tier.expires_at)}` : 'No active subscription';
      }
      
      // Process referrals data
      if (referralsData.success) {
        const referrals = referralsData.referrals || [];
        const commissions = referralsData.commissions || [];
        document.getElementById('referrals-count').innerText = referrals.length;
        document.getElementById('commission-amount').innerText = `$${(referralsData.total_commission || 0).toFixed(2)}`;
      }
    })
    .catch(error => {
      console.error('Error loading user data:', error);
      showMessage('Error loading data. Please try again.', 'danger');
    });
  }
  
  function getTierLimit(tierName) {
    switch(tierName.toLowerCase()) {
      case 'dealer':
        return 'Unlimited';
      case 'premium':
        return 10;
      case 'basic':
      default:
        return 3;
    }
  }
  
  function getTierBadgeClass(tierName) {
    switch(tierName.toLowerCase()) {
      case 'dealer':
        return 'bg-danger';
      case 'premium':
        return 'bg-warning text-dark';
      case 'basic':
      default:
        return 'bg-primary';
    }
  }
  
  function isExpired(dateString) {
    if (!dateString) return false;
    const expiryDate = new Date(dateString);
    return expiryDate < new Date();
  }
  
  function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  }
  
  function showMessage(message, type = 'info') {
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
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
      const container = document.createElement('div');
      container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
      document.body.appendChild(container);
      container.appendChild(toastEl);
    } else {
      toastContainer.appendChild(toastEl);
    }
    
    // Initialize and show toast
    const toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 5000 });
    toast.show();
    
    // Remove from DOM after hidden
    toastEl.addEventListener('hidden.bs.toast', () => {
      toastEl.remove();
    });
  }
});