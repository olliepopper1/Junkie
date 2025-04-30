/**
 * Phantom Wallet Integration for Trial Junkie
 * Handles connection, disconnection, and transactions with Phantom Wallet
 */

document.addEventListener('DOMContentLoaded', function() {
  // DOM elements
  const connectButton = document.getElementById('connect-wallet-btn');
  const disconnectButton = document.getElementById('disconnect-wallet-btn');
  const connectionIndicator = document.getElementById('connection-indicator');
  const walletAddressEl = document.getElementById('wallet-address');
  
  // Check if Phantom is installed
  const isPhantomInstalled = window.phantom?.solana?.isPhantom;
  
  // If Phantom is not installed, update UI to reflect that
  if (!isPhantomInstalled) {
    connectButton.innerHTML = '<i class="bi bi-download"></i> Install Phantom';
    connectButton.classList.add('btn-warning');
    connectButton.onclick = () => window.open('https://phantom.app/', '_blank');
    return;
  }
  
  // Check if already connected (stored in session)
  const checkConnection = async () => {
    try {
      // Check if the connection was previously established
      const provider = getProvider();
      if (provider) {
        const response = await provider.connect({ onlyIfTrusted: true });
        const publicKey = response.publicKey.toString();
        
        updateUIConnected(publicKey);
        return true;
      }
    } catch (error) {
      console.error("Auto-connection error:", error);
    }
    return false;
  };
  
  // Get the Phantom Provider
  const getProvider = () => {
    if ("phantom" in window) {
      const provider = window.phantom?.solana;
      if (provider?.isPhantom) {
        return provider;
      }
    }
    return null;
  };
  
  // Update UI when connected
  const updateUIConnected = (address) => {
    connectButton.classList.add('d-none');
    disconnectButton.classList.remove('d-none');
    connectionIndicator.classList.remove('bg-danger');
    connectionIndicator.classList.add('bg-success');
    connectionIndicator.textContent = 'Connected';
    
    // Format address to show first and last few characters
    const formattedAddress = `${address.slice(0, 6)}...${address.slice(-4)}`;
    walletAddressEl.textContent = formattedAddress;
    walletAddressEl.classList.remove('text-muted');
    
    // Enable subscription plan elements
    const subsectionElements = document.querySelectorAll('.subscription-section');
    subsectionElements.forEach(el => {
      el.classList.remove('opacity-50');
      el.classList.remove('pe-none');
    });
  };
  
  // Update UI when disconnected
  const updateUIDisconnected = () => {
    disconnectButton.classList.add('d-none');
    connectButton.classList.remove('d-none');
    connectionIndicator.classList.remove('bg-success');
    connectionIndicator.classList.add('bg-danger');
    connectionIndicator.textContent = 'Disconnected';
    walletAddressEl.textContent = 'Not connected';
    walletAddressEl.classList.add('text-muted');
    
    // Disable subscription plan elements
    const subsectionElements = document.querySelectorAll('.subscription-section');
    subsectionElements.forEach(el => {
      el.classList.add('opacity-50');
      el.classList.add('pe-none');
    });
  };
  
  // Connect to Phantom wallet
  const connectWallet = async () => {
    try {
      const provider = getProvider();
      if (!provider) throw new Error("Phantom provider not found");
      
      // Connect to wallet
      connectButton.innerHTML = '<i class="bi bi-hourglass-split"></i> Connecting...';
      connectButton.disabled = true;
      
      const response = await provider.connect();
      const publicKey = response.publicKey.toString();
      
      console.log("Connected to:", publicKey);
      updateUIConnected(publicKey);
      
      // Notify server about the connection
      await fetch('/api/wallet/connect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ wallet_address: publicKey }),
      });
      
    } catch (error) {
      console.error("Connection error:", error);
      alert("Could not connect to Phantom wallet. Please try again.");
    } finally {
      connectButton.innerHTML = '<i class="bi bi-wallet2"></i> Connect Wallet';
      connectButton.disabled = false;
    }
  };
  
  // Disconnect from Phantom wallet
  const disconnectWallet = async () => {
    try {
      const provider = getProvider();
      if (provider) {
        await provider.disconnect();
        console.log("Disconnected from wallet");
      }
      
      // Update UI
      updateUIDisconnected();
      
      // Notify server about the disconnection
      await fetch('/api/wallet/disconnect', {
        method: 'POST',
      });
      
    } catch (error) {
      console.error("Disconnection error:", error);
    }
  };
  
  // Event listeners
  connectButton.addEventListener('click', connectWallet);
  disconnectButton.addEventListener('click', disconnectWallet);
  
  // Check for existing connection on page load
  checkConnection();
});