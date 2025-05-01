/**
 * Phantom Wallet integration for Trial Junkie
 * 
 * Handles interactions with the Phantom wallet extension for Solana blockchain
 */

// Check if Phantom is available
const isPhantomInstalled = window.phantom?.solana?.isPhantom;

// Wallet connection status
let walletStatus = {
    connected: false,
    address: null,
    balance: null
};

/**
 * Connect to Phantom Wallet
 * @returns {Promise<Object>} The connection result
 */
async function connectWallet() {
    try {
        if (!isPhantomInstalled) {
            console.error("Phantom wallet is not installed");
            return {
                success: false,
                message: "Phantom wallet is not installed"
            };
        }
        
        const provider = window.phantom?.solana;
        const resp = await provider.connect();
        const walletAddress = resp.publicKey.toString();
        
        walletStatus.connected = true;
        walletStatus.address = walletAddress;
        
        // Get wallet balance
        try {
            const connection = new solanaWeb3.Connection("https://api.mainnet-beta.solana.com");
            const balance = await connection.getBalance(new solanaWeb3.PublicKey(walletAddress));
            const solBalance = balance / 1000000000; // Convert lamports to SOL
            walletStatus.balance = solBalance;
        } catch (error) {
            console.error("Error fetching wallet balance:", error);
            walletStatus.balance = null;
        }
        
        return {
            success: true,
            address: walletAddress,
            balance: walletStatus.balance
        };
    } catch (error) {
        console.error("Error connecting to wallet:", error);
        return {
            success: false,
            message: error.message || "Could not connect to Phantom wallet"
        };
    }
}

/**
 * Disconnect from Phantom Wallet
 */
async function disconnectWallet() {
    try {
        if (isPhantomInstalled) {
            // Note: Phantom doesn't have a direct disconnect method
            // But we can reset our connection state
            walletStatus.connected = false;
            walletStatus.address = null;
            walletStatus.balance = null;
        }
    } catch (error) {
        console.error("Error disconnecting wallet:", error);
    }
}

/**
 * Check if wallet is already connected
 * @returns {Promise<Object>} Connection status
 */
async function checkWalletConnection() {
    try {
        if (!isPhantomInstalled) {
            return { connected: false };
        }
        
        const provider = window.phantom?.solana;
        
        try {
            // This will only succeed if user has already authorized
            const resp = await provider.connect({ onlyIfTrusted: true });
            if (resp && resp.publicKey) {
                const walletAddress = resp.publicKey.toString();
                walletStatus.connected = true;
                walletStatus.address = walletAddress;
                
                return {
                    connected: true,
                    address: walletAddress
                };
            }
        } catch (error) {
            // Not connected, which is fine - not an error
            return { connected: false };
        }
    } catch (error) {
        console.error("Error checking wallet connection:", error);
        return { connected: false, error: error.message };
    }
}

/**
 * Helper function to shorten wallet address for display
 * @param {string} address - The full wallet address
 * @returns {string} The shortened address
 */
function shortenAddress(address) {
    if (!address) return '';
    return address.slice(0, 6) + '...' + address.slice(-4);
}

/**
 * Send a transaction via Phantom Wallet
 * @param {string} recipient - Recipient wallet address
 * @param {number} amount - Amount in SOL
 * @returns {Promise<Object>} Transaction result
 */
async function sendTransaction(recipient, amount) {
    try {
        if (!isPhantomInstalled) {
            return {
                success: false,
                message: "Phantom wallet is not installed"
            };
        }
        
        if (!walletStatus.connected) {
            // Try to connect first
            const connectionResult = await connectWallet();
            if (!connectionResult.success) {
                return connectionResult;
            }
        }
        
        const provider = window.phantom?.solana;
        const connection = new solanaWeb3.Connection("https://api.mainnet-beta.solana.com");
        
        // Convert amount to lamports (1 SOL = 1,000,000,000 lamports)
        const lamports = amount * 1000000000;
        
        // Create transaction
        const transaction = new solanaWeb3.Transaction().add(
            solanaWeb3.SystemProgram.transfer({
                fromPubkey: new solanaWeb3.PublicKey(walletStatus.address),
                toPubkey: new solanaWeb3.PublicKey(recipient),
                lamports: lamports
            })
        );
        
        // Set recent blockhash and fee payer
        transaction.feePayer = new solanaWeb3.PublicKey(walletStatus.address);
        transaction.recentBlockhash = (await connection.getRecentBlockhash()).blockhash;
        
        // Sign and send transaction
        const signed = await provider.signTransaction(transaction);
        const signature = await connection.sendRawTransaction(signed.serialize());
        
        // Wait for confirmation
        await connection.confirmTransaction(signature);
        
        return {
            success: true,
            signature: signature,
            message: "Transaction successful"
        };
    } catch (error) {
        console.error("Error sending transaction:", error);
        return {
            success: false,
            message: error.message || "Transaction failed"
        };
    }
}

// Export wallet functions as globals
window.phantomWallet = {
    connect: connectWallet,
    disconnect: disconnectWallet,
    checkConnection: checkWalletConnection,
    shortenAddress: shortenAddress,
    sendTransaction: sendTransaction,
    isInstalled: isPhantomInstalled,
    status: walletStatus
};