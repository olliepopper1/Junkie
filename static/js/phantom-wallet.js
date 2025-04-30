/**
 * Phantom Wallet Integration for Trial Junkie
 * Manages wallet connections and transaction signing
 */

// Wallet state tracking
let walletConnected = false;
let walletAddress = null;
let walletBalance = 0;

// DOM elements (will be initialized when DOM is ready)
let connectButton;
let disconnectButton;
let walletAddressDisplay;
let walletSection;
let walletBalanceDisplay;
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
  walletBalanceDisplay = document.getElementById('wallet-balance');
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
  
  // Check if the wallet is already connected
  checkConnection();
});

// Check for existing connection
async function checkConnection() {
  try {
    const isPhantomInstalled = window.phantom?.solana?.isPhantom;
    if (!isPhantomInstalled) {
      console.log('Phantom wallet extension not detected');
      walletStatus.textContent = 'Not Installed';
      walletStatus.classList.remove('bg-secondary', 'bg-success');
      walletStatus.classList.add('bg-danger');
      return;
    }
    
    // Check if we're already connected
    const provider = window.phantom?.solana;
    const resp = await provider.connect({ onlyIfTrusted: true });
    
    if (resp && resp.publicKey) {
      walletAddress = resp.publicKey.toString();
      walletConnected = true;
      updateWalletUI(true);
    }
  } catch (error) {
    console.log('Not connected to wallet:', error.message);
  }
}

// Connect to Phantom wallet
async function connectWallet() {
  try {
    // Check if Phantom is installed
    const isPhantomInstalled = window.phantom?.solana?.isPhantom;
    if (!isPhantomInstalled) {
      alert('Phantom wallet extension not detected. Please install Phantom wallet first.');
      return;
    }
    
    // Connect to the wallet
    const provider = window.phantom?.solana;
    const resp = await provider.connect();
    walletAddress = resp.publicKey.toString();
    walletConnected = true;
    
    // Update the UI
    updateWalletUI(true);
    
    // Get wallet balance
    await updateWalletBalance();
    
    // Save connection to server
    saveWalletConnection();
  } catch (error) {
    console.error('Error connecting to wallet:', error);
    alert('Could not connect to Phantom wallet. Please try again.');
  }
}

// Disconnect from Phantom wallet
async function disconnectWallet() {
  try {
    // Disconnect from the wallet
    const provider = window.phantom?.solana;
    await provider.disconnect();
    
    // Update state
    walletConnected = false;
    walletAddress = null;
    
    // Update the UI
    updateWalletUI(false);
    
    // Save disconnection to server
    saveWalletDisconnection();
  } catch (error) {
    console.error('Error disconnecting from wallet:', error);
    alert('Could not disconnect from Phantom wallet. Please try again.');
  }
}

// Update wallet balance
async function updateWalletBalance() {
  try {
    if (!walletConnected || !walletAddress) return;
    
    // Get the Solana connection
    const provider = window.phantom?.solana;
    const connection = provider.connection;
    
    // Get wallet balance
    const balance = await connection.getBalance(new solanaWeb3.PublicKey(walletAddress));
    walletBalance = balance / 1000000000; // Convert lamports to SOL
    
    // Update UI
    walletBalanceDisplay.textContent = `Balance: ${walletBalance.toFixed(4)} SOL`;
  } catch (error) {
    console.error('Error getting wallet balance:', error);
    walletBalanceDisplay.textContent = `Balance: Unknown`;
  }
}

// Update UI based on wallet connection status
function updateWalletUI(connected) {
  if (connected) {
    // Connected state
    connectButton.style.display = 'none';
    disconnectButton.style.display = 'inline-block';
    walletStatus.textContent = 'Connected';
    walletStatus.classList.remove('bg-secondary', 'bg-danger');
    walletStatus.classList.add('bg-success');
    walletAddressDisplay.textContent = shortenAddress(walletAddress);
    walletLogo.style.opacity = '1';
    
    // Add a connected class to wallet section
    walletSection.classList.add('wallet-connected');
  } else {
    // Disconnected state
    connectButton.style.display = 'inline-block';
    disconnectButton.style.display = 'none';
    walletStatus.textContent = 'Disconnected';
    walletStatus.classList.remove('bg-success', 'bg-danger');
    walletStatus.classList.add('bg-secondary');
    walletAddressDisplay.textContent = 'Not connected';
    walletBalanceDisplay.textContent = '';
    walletLogo.style.opacity = '0.7';
    
    // Remove connected class from wallet section
    walletSection.classList.remove('wallet-connected');
  }
}

// Save wallet connection to server
function saveWalletConnection() {
  fetch('/api/connect-wallet', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ address: walletAddress })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Wallet connection saved:', data);
  })
  .catch(error => {
    console.error('Error saving wallet connection:', error);
  });
}

// Save wallet disconnection to server
function saveWalletDisconnection() {
  fetch('/api/disconnect-wallet', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    console.log('Wallet disconnection saved:', data);
  })
  .catch(error => {
    console.error('Error saving wallet disconnection:', error);
  });
}

// Helper to shorten address for display
function shortenAddress(address) {
  if (!address) return '';
  return address.slice(0, 6) + '...' + address.slice(-4);
}

// Log initialization
console.log('Phantom wallet integration script loaded');