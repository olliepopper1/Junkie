/**
 * Wallet Header Integration for Trial Junkie
 * 
 * Handles the UI for the wallet connection in the site header
 */

document.addEventListener('DOMContentLoaded', function() {
    // Find the login button container in the navbar
    const loginContainer = document.querySelector('.navbar .d-flex');
    
    if (!loginContainer) {
        console.error('Login container not found');
        return;
    }
    
    // Define wallet button HTML
    const walletButtonHTML = `
        <div class="wallet-container">
            <button id="wallet-connect-btn" class="btn wallet-connect-btn text-white">
                <img src="/img/phantom-icon.svg" alt="Phantom" class="wallet-logo me-2" width="20"> 
                Connect Wallet
            </button>
            <div id="wallet-connected" class="wallet-connected d-none">
                <button class="btn btn-sm btn-outline-light dropdown-toggle" type="button" id="walletDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                    <img src="/img/phantom-icon.svg" alt="Phantom" class="wallet-logo me-1" width="16">
                    <span id="wallet-address-display"></span>
                </button>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="walletDropdown">
                    <li><span class="dropdown-item-text">Balance: <span id="wallet-balance">-- SOL</span></span></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="/dashboard">Dashboard</a></li>
                    <li><a class="dropdown-item" href="/trials">My Trials</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" id="wallet-disconnect">Disconnect</a></li>
                </ul>
            </div>
        </div>
    `;
    
    // Replace Discord login button with wallet button
    loginContainer.innerHTML = walletButtonHTML;
    
    // Add wallet styles if not already added
    if (!document.getElementById('wallet-styles')) {
        const walletStyles = document.createElement('style');
        walletStyles.id = 'wallet-styles';
        walletStyles.textContent = `
            .wallet-connect-btn {
                display: flex;
                align-items: center;
                background-color: #AB70FF;
                border-color: #AB70FF;
                transition: all 0.3s ease;
            }
            .wallet-connect-btn:hover {
                background-color: #9656FB;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(171, 112, 255, 0.5);
            }
            .wallet-logo {
                margin-right: 8px;
            }
            .wallet-connected .btn {
                display: flex;
                align-items: center;
            }
        `;
        document.head.appendChild(walletStyles);
    }
    
    // Get elements
    const connectBtn = document.getElementById('wallet-connect-btn');
    const connectedEl = document.getElementById('wallet-connected');
    const disconnectBtn = document.getElementById('wallet-disconnect');
    const addressDisplay = document.getElementById('wallet-address-display');
    const balanceDisplay = document.getElementById('wallet-balance');
    
    // Check if wallet is already connected
    async function checkWalletStatus() {
        // Make sure the Phantom wallet utilities are loaded
        if (!window.phantomWallet) {
            console.error('Phantom wallet utilities not loaded');
            return;
        }
        
        const connectionStatus = await window.phantomWallet.checkConnection();
        
        if (connectionStatus.connected) {
            // Update UI to show connected state
            connectBtn.classList.add('d-none');
            connectedEl.classList.remove('d-none');
            
            // Update address display
            if (connectionStatus.address) {
                addressDisplay.textContent = window.phantomWallet.shortenAddress(connectionStatus.address);
            }
            
            // Update balance if available
            if (window.phantomWallet.status.balance !== null) {
                balanceDisplay.textContent = window.phantomWallet.status.balance.toFixed(2) + ' SOL';
            }
            
            // Check if user is authenticated with the server
            fetch('/wallet-status')
                .then(response => response.json())
                .then(data => {
                    if (!data.authenticated) {
                        // User needs to authenticate/login with the connected wallet
                        loginWithWallet(connectionStatus.address);
                    }
                })
                .catch(error => console.error('Error checking wallet status:', error));
        }
    }
    
    // Connect wallet
    async function handleConnect() {
        const result = await window.phantomWallet.connect();
        
        if (result.success) {
            // Update UI
            connectBtn.classList.add('d-none');
            connectedEl.classList.remove('d-none');
            addressDisplay.textContent = window.phantomWallet.shortenAddress(result.address);
            
            if (result.balance !== null) {
                balanceDisplay.textContent = result.balance.toFixed(2) + ' SOL';
            }
            
            // Authenticate with server
            loginWithWallet(result.address);
        } else {
            // Show error message
            alert('Could not connect to wallet: ' + (result.message || 'Unknown error'));
        }
    }
    
    // Disconnect wallet
    async function handleDisconnect() {
        await window.phantomWallet.disconnect();
        
        // Update UI
        connectBtn.classList.remove('d-none');
        connectedEl.classList.add('d-none');
        
        // Logout from server
        fetch('/logout', { method: 'POST' })
            .then(() => {
                // Redirect to home page if on a protected page
                const currentPath = window.location.pathname;
                if (currentPath === '/dashboard' || currentPath === '/trials') {
                    window.location.href = '/';
                }
            })
            .catch(error => console.error('Error logging out:', error));
    }
    
    // Login with wallet
    function loginWithWallet(address) {
        fetch('/login-with-wallet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ wallet_address: address })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // If on login or register page, redirect to dashboard
                const currentPath = window.location.pathname;
                if (currentPath === '/login' || currentPath === '/register') {
                    window.location.href = '/dashboard';
                }
            } else {
                console.error('Login failed:', data.message);
            }
        })
        .catch(error => console.error('Error logging in with wallet:', error));
    }
    
    // Add event listeners
    if (connectBtn) {
        connectBtn.addEventListener('click', handleConnect);
    }
    
    if (disconnectBtn) {
        disconnectBtn.addEventListener('click', handleDisconnect);
    }
    
    // Check wallet status on page load
    checkWalletStatus();
});