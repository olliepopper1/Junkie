/**
 * Phantom Wallet Integration for Trial Junkie
 * Manages wallet connections and transaction signing
 */

// Wallet state tracking
let walletConnected = false;
let walletAddress = null;

// DOM elements (will be initialized when DOM is ready)
let connectButton;
let disconnectButton;
let walletAddressDisplay;
let walletSection;
let walletBalance;
let walletLogo;
let walletStatus;

// Initialize wallet functionality
document.addEventListener('DOMContentLoaded', async function() {
  console.log('Initializing Phantom Wallet integration');
  
  // Get wallet DOM elements
  connectButton = document.getElementById('connect-wallet-btn');
  disconnectButton = document.getElementById('disconnect-wallet-btn');
  walletAddressDisplay = document.getElementById('wallet-address');
  walletSection = document.getElementById('wallet-section');
  walletBalance = document.getElementById('wallet-balance');
  walletLogo = document.getElementById('phantom-logo');
  walletStatus = document.getElementById('wallet-status');
  
  // Check if the wallet section exists on this page
  if (!walletSection) {
    console.log('Wallet section not found on this page');
    return;
  }
  
  // Add event listeners
  if (connectButton) {
    connectButton.addEventListener('click', connectWallet);
  }
  
  if (disconnectButton) {
    disconnectButton.addEventListener('click', disconnectWallet);
  }
  
  // Check if Phantom is installed
  if (!isPhantomInstalled()) {
    console.log('Phantom wallet not installed');
    showInstallPrompt();
    return;
  }
  
  // Check if wallet is already connected on the server
  await checkWalletConnection();
});

// Check if Phantom is installed
function isPhantomInstalled() {
  const provider = getProvider();
  return provider !== null;
}

// Get Phantom provider if available
function getProvider() {
  if ('phantom' in window) {
    const provider = window.phantom?.solana;
    
    if (provider?.isPhantom) {
      return provider;
    }
  }
  
  return null;
}

// Show installation prompt
function showInstallPrompt() {
  if (!walletSection) return;
  
  // Update UI to show installation prompt
  walletSection.innerHTML = `
    <div class="card-body text-center">
      <img src="/img/phantom-logo.svg" alt="Phantom Wallet" style="width: 64px; margin-bottom: 20px;">
      <h5 class="card-title">Phantom Wallet Required</h5>
      <p class="card-text">To connect your wallet, you need to install Phantom first.</p>
      <a href="https://phantom.app/" target="_blank" class="btn btn-primary mt-3">
        <i class="bi bi-box-arrow-up-right me-2"></i>Get Phantom
      </a>
    </div>
  `;
}

// Connect to Phantom wallet
async function connectWallet() {
  try {
    const provider = getProvider();
    
    if (!provider) {
      console.error('Phantom wallet not installed');
      showInstallPrompt();
      return;
    }
    
    updateWalletUI('connecting');
    
    // Request connection to Phantom
    const resp = await provider.connect();
    const address = resp.publicKey.toString();
    
    console.log('Connected to wallet:', address);
    
    // Save connection on server
    const saveResult = await saveWalletConnection(address);
    
    if (saveResult.status === 'success') {
      walletConnected = true;
      walletAddress = address;
      updateWalletUI('connected', address);
    } else {
      console.error('Failed to save wallet connection on server:', saveResult.error);
      updateWalletUI('error', null, 'Failed to save connection');
    }
  } catch (err) {
    console.error('Error connecting to Phantom wallet:', err);
    updateWalletUI('error', null, 'Connection rejected');
  }
}

// Disconnect from Phantom wallet
async function disconnectWallet() {
  try {
    updateWalletUI('disconnecting');
    
    // Disconnect on server first
    const result = await fetch('/api/wallet/disconnect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(res => res.json());
    
    if (result.status === 'success') {
      walletConnected = false;
      walletAddress = null;
      updateWalletUI('disconnected');
      
      // Try to disconnect from Phantom provider as well
      try {
        const provider = getProvider();
        if (provider && provider.disconnect) {
          await provider.disconnect();
        }
      } catch (err) {
        console.warn('Could not disconnect from Phantom provider:', err);
      }
    } else {
      console.error('Failed to disconnect wallet on server:', result.error);
      updateWalletUI('error', walletAddress, 'Failed to disconnect');
    }
  } catch (err) {
    console.error('Error disconnecting wallet:', err);
    updateWalletUI('error', walletAddress, 'Disconnect failed');
  }
}

// Check existing wallet connection status
async function checkWalletConnection() {
  try {
    // Check if connected on server
    const result = await fetch('/api/wallet/status').then(res => res.json());
    
    if (result.status === 'success' && result.connected) {
      walletConnected = true;
      walletAddress = result.address;
      updateWalletUI('connected', result.address);
    } else {
      updateWalletUI('disconnected');
    }
  } catch (err) {
    console.error('Error checking wallet connection:', err);
    updateWalletUI('error', null, 'Failed to check status');
  }
}

// Save wallet connection to server
async function saveWalletConnection(address) {
  try {
    const result = await fetch('/api/wallet/connect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        address: address
      })
    }).then(res => res.json());
    
    return result;
  } catch (err) {
    console.error('Error saving wallet connection:', err);
    return { status: 'error', error: err.message };
  }
}

// Update wallet UI based on connection state
function updateWalletUI(state, address = null, errorMessage = null) {
  if (!walletSection) return;
  
  // Update address display if needed
  if (walletAddressDisplay) {
    if (address) {
      // Format address with ellipsis
      const shortAddress = address.substring(0, 4) + '...' + address.substring(address.length - 4);
      walletAddressDisplay.textContent = shortAddress;
      walletAddressDisplay.title = address; // Full address on hover
    } else {
      walletAddressDisplay.textContent = 'Not Connected';
      walletAddressDisplay.title = '';
    }
  }
  
  // Update status text
  if (walletStatus) {
    switch (state) {
      case 'connected':
        walletStatus.textContent = 'Connected';
        walletStatus.className = 'text-success';
        break;
      case 'connecting':
        walletStatus.textContent = 'Connecting...';
        walletStatus.className = 'text-warning';
        break;
      case 'disconnected':
        walletStatus.textContent = 'Disconnected';
        walletStatus.className = 'text-secondary';
        break;
      case 'disconnecting':
        walletStatus.textContent = 'Disconnecting...';
        walletStatus.className = 'text-warning';
        break;
      case 'error':
        walletStatus.textContent = errorMessage || 'Error';
        walletStatus.className = 'text-danger';
        break;
    }
  }
  
  // Show/hide buttons based on state
  if (connectButton) {
    connectButton.style.display = (state === 'disconnected' || state === 'error') ? 'inline-block' : 'none';
  }
  
  if (disconnectButton) {
    disconnectButton.style.display = (state === 'connected') ? 'inline-block' : 'none';
  }
  
  // Update logo opacity
  if (walletLogo) {
    walletLogo.style.opacity = (state === 'connected') ? '1' : '0.6';
  }
}

// Helper to create a payment request
async function createPayment(amount, serviceType) {
  if (!walletConnected) {
    alert('Please connect your wallet first');
    return null;
  }
  
  try {
    const result = await fetch('/api/create-payment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        amount: amount,
        service_type: serviceType
      })
    }).then(res => res.json());
    
    if (result.status === 'success') {
      return result;
    } else {
      console.error('Failed to create payment:', result.error);
      return null;
    }
  } catch (err) {
    console.error('Error creating payment:', err);
    return null;
  }
}