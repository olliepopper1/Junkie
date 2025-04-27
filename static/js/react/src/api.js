// Trial Junkie API Service
// Handles API calls to the backend for payment processing, trial generation, etc.

/**
 * Generate a new trial account
 * @param {string} service - The streaming service (netflix, hulu, etc.)
 * @param {string} type - The trial generation type (hit, dose_identity, etc.)
 * @param {boolean} automate - Whether to automate the signup process
 * @returns {Promise} - API response with trial details
 */
export async function generateTrial(service, type, automate = false) {
  try {
    const response = await fetch('/api/generate-trial', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        service,
        type,
        automate
      })
    });
    
    return await response.json();
  } catch (error) {
    console.error('Error generating trial:', error);
    throw error;
  }
}

/**
 * Get user's existing trials
 * @returns {Promise} - API response with list of trials
 */
export async function getUserTrials() {
  try {
    const response = await fetch('/api/trials');
    return await response.json();
  } catch (error) {
    console.error('Error fetching trials:', error);
    throw error;
  }
}

/**
 * Create a payment request for subscription
 * @param {string} planId - The subscription plan ID
 * @returns {Promise} - API response with payment details
 */
export async function createPaymentRequest(planId) {
  try {
    const response = await fetch('/api/create-payment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        plan_id: planId
      })
    });
    
    return await response.json();
  } catch (error) {
    console.error('Error creating payment request:', error);
    throw error;
  }
}

/**
 * Verify payment status for a payment reference
 * @param {string} reference - Payment reference ID
 * @param {string} txSignature - Optional Solana transaction signature
 * @returns {Promise} - API response with verification status
 */
export async function verifyPayment(reference, txSignature = null) {
  try {
    const response = await fetch('/api/verify-payment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        reference,
        tx_signature: txSignature
      })
    });
    
    return await response.json();
  } catch (error) {
    console.error('Error verifying payment:', error);
    throw error;
  }
}

/**
 * Withdraw referral commission
 * @param {number} amount - Amount to withdraw in SOL
 * @param {string} walletAddress - Solana wallet address
 * @returns {Promise} - API response with withdrawal status
 */
export async function withdrawCommission(amount, walletAddress) {
  try {
    const response = await fetch('/api/withdraw-commission', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        amount,
        wallet_address: walletAddress
      })
    });
    
    return await response.json();
  } catch (error) {
    console.error('Error processing withdrawal:', error);
    throw error;
  }
}

/**
 * Get user's referral statistics
 * @returns {Promise} - API response with referral stats
 */
export async function getReferralStats() {
  try {
    const response = await fetch('/api/referral-stats');
    return await response.json();
  } catch (error) {
    console.error('Error fetching referral stats:', error);
    throw error;
  }
}

/**
 * Register with a referral code
 * @param {string} referralCode - The referral code to use
 * @returns {Promise} - API response with registration status
 */
export async function registerReferral(referralCode) {
  try {
    const response = await fetch('/api/register-referral', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        referral_code: referralCode
      })
    });
    
    return await response.json();
  } catch (error) {
    console.error('Error registering referral:', error);
    throw error;
  }
}

/**
 * Get user subscription tier information
 * @returns {Promise} - API response with tier details
 */
export async function getUserTier() {
  try {
    const response = await fetch('/api/user-tier');
    return await response.json();
  } catch (error) {
    console.error('Error fetching user tier:', error);
    throw error;
  }
}

/**
 * Get payment history
 * @param {string} status - Optional filter by payment status
 * @returns {Promise} - API response with payment history
 */
export async function getPaymentHistory(status = null) {
  try {
    const url = status ? `/api/payments?status=${status}` : '/api/payments';
    const response = await fetch(url);
    return await response.json();
  } catch (error) {
    console.error('Error fetching payment history:', error);
    throw error;
  }
}