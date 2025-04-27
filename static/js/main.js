/**
 * Trial Junkie - Main JavaScript
 * Handles client-side functionality for the Trial Junkie web dashboard
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Trial Junkie Dashboard Initialized');
    initializeTooltips();
    setupCopyButtons();
    setupTrialSearch();
    setupCountdowns();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

/**
 * Set up copy-to-clipboard functionality
 */
function setupCopyButtons() {
    const copyButtons = document.querySelectorAll('.btn-copy');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-copy-target');
            const textToCopy = document.getElementById(targetId).value || document.getElementById(targetId).textContent;
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Show success state
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                this.classList.add('copied');
                
                // Reset after 2 seconds
                setTimeout(() => {
                    this.textContent = originalText;
                    this.classList.remove('copied');
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy: ', err);
                alert('Failed to copy text. Please try again.');
            });
        });
    });
}

/**
 * Set up trial search functionality
 */
function setupTrialSearch() {
    const searchInput = document.getElementById('searchTrials');
    if (!searchInput) return;
    
    searchInput.addEventListener('keyup', function() {
        const searchTerm = this.value.toLowerCase();
        const trialCards = document.querySelectorAll('#trialsList .trial-card');
        
        trialCards.forEach(card => {
            const cardText = card.textContent.toLowerCase();
            const cardParent = card.closest('.col');
            
            if (cardText.includes(searchTerm)) {
                cardParent.style.display = '';
            } else {
                cardParent.style.display = 'none';
            }
        });
    });
}

/**
 * Set up countdown timers for trial expirations
 */
function setupCountdowns() {
    const trialBadges = document.querySelectorAll('.badge[data-expiry]');
    
    trialBadges.forEach(badge => {
        const expiryDate = new Date(badge.getAttribute('data-expiry'));
        
        function updateCountdown() {
            const now = new Date();
            const diff = expiryDate - now;
            
            if (diff <= 0) {
                badge.textContent = 'Expired';
                badge.classList.remove('bg-warning');
                badge.classList.add('bg-danger');
                return;
            }
            
            // Calculate days remaining
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            badge.textContent = `${days} days left`;
        }
        
        // Initial update
        updateCountdown();
        
        // Update every hour
        setInterval(updateCountdown, 60 * 60 * 1000);
    });
}

/**
 * Generate a trial account (API call)
 */
async function generateTrial() {
    const service = document.getElementById('trialService').value;
    const type = document.getElementById('trialType').value;
    const automate = document.getElementById('automateSignup').checked;
    
    // Show loading state
    const generateButton = document.querySelector('#generateTrialModal .btn-primary');
    const originalText = generateButton.textContent;
    generateButton.textContent = 'Generating...';
    generateButton.disabled = true;
    
    try {
        const response = await fetch('/api/generate-trial', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                service: service,
                type: type,
                automate: automate
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('generateTrialModal'));
            modal.hide();
            
            // Show success message
            showAlert('success', `Successfully generated ${service} trial account!`);
            
            // Reload page to show new trial
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showAlert('danger', data.error || 'Failed to generate trial');
        }
    } catch (error) {
        console.error('Error generating trial:', error);
        showAlert('danger', 'An error occurred while generating the trial');
    } finally {
        // Reset button state
        generateButton.textContent = originalText;
        generateButton.disabled = false;
    }
}

/**
 * Process subscription payment using Solana
 */
async function upgradePlan() {
    const selectedPlanEl = document.querySelector('.list-group-item.active');
    if (!selectedPlanEl) {
        showAlert('warning', 'Please select a subscription plan');
        return;
    }
    
    const planId = selectedPlanEl.getAttribute('data-plan-id');
    const planName = selectedPlanEl.querySelector('h5').textContent;
    
    // Show loading state
    const payButton = document.querySelector('#upgradeModal .btn-primary');
    const originalText = payButton.textContent;
    payButton.textContent = 'Processing...';
    payButton.disabled = true;
    
    try {
        // Create payment request
        const paymentResponse = await fetch('/api/create-payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                plan_id: planId
            })
        });
        
        const paymentData = await paymentResponse.json();
        
        if (paymentData.success) {
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('upgradeModal'));
            modal.hide();
            
            // Show payment information in new modal
            showPaymentModal(paymentData);
        } else {
            showAlert('danger', paymentData.error || 'Failed to create payment request');
        }
    } catch (error) {
        console.error('Error creating payment:', error);
        showAlert('danger', 'An error occurred while processing your payment');
    } finally {
        // Reset button state
        payButton.textContent = originalText;
        payButton.disabled = false;
    }
}

/**
 * Show payment modal with Solana wallet address
 */
function showPaymentModal(paymentData) {
    // Create modal dynamically
    const modalHtml = `
        <div class="modal fade" id="paymentModal" tabindex="-1" aria-labelledby="paymentModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="paymentModalLabel">Complete Your Payment</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-info">
                            Please send exactly ${paymentData.amount} SOL to the following address:
                        </div>
                        <div class="input-group mb-3">
                            <input type="text" class="form-control" value="${paymentData.wallet_address}" id="walletAddress" readonly>
                            <button class="btn btn-outline-secondary btn-copy" data-copy-target="walletAddress" type="button">Copy</button>
                        </div>
                        <div class="mb-3">
                            <p><strong>Reference ID:</strong> ${paymentData.reference}</p>
                            <p><strong>Important:</strong> Include this Reference ID in the transaction memo field</p>
                        </div>
                        <div class="alert alert-warning">
                            <small>After sending payment, click "Verify Payment" to check the status. It may take a few minutes for the transaction to be confirmed on the blockchain.</small>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" onclick="verifyPayment('${paymentData.reference}')">Verify Payment</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to document
    const modalContainer = document.createElement('div');
    modalContainer.innerHTML = modalHtml;
    document.body.appendChild(modalContainer);
    
    // Initialize and show modal
    const paymentModal = new bootstrap.Modal(document.getElementById('paymentModal'));
    paymentModal.show();
    
    // Initialize copy button
    setupCopyButtons();
    
    // Remove modal from DOM when hidden
    document.getElementById('paymentModal').addEventListener('hidden.bs.modal', function() {
        document.body.removeChild(modalContainer);
    });
}

/**
 * Verify payment status
 */
async function verifyPayment(reference) {
    // Show loading state
    const verifyButton = document.querySelector('#paymentModal .btn-primary');
    const originalText = verifyButton.textContent;
    verifyButton.textContent = 'Verifying...';
    verifyButton.disabled = true;
    
    try {
        const response = await fetch('/api/verify-payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                reference: reference
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('paymentModal'));
            modal.hide();
            
            // Show success message
            showAlert('success', 'Payment verified successfully! Your subscription has been activated.');
            
            // Reload page to show updated subscription status
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            showAlert('warning', data.message || 'Payment not yet verified. Please try again in a few minutes.');
        }
    } catch (error) {
        console.error('Error verifying payment:', error);
        showAlert('danger', 'An error occurred while verifying your payment');
    } finally {
        // Reset button state
        verifyButton.textContent = originalText;
        verifyButton.disabled = false;
    }
}

/**
 * Display alert message
 */
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add to the top of the content
    const content = document.querySelector('main');
    content.insertBefore(alertDiv, content.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const bootstrapAlert = new bootstrap.Alert(alertDiv);
        bootstrapAlert.close();
    }, 5000);
}

/**
 * Copy trial details to clipboard
 */
function copyTrialDetails(trialId) {
    const trialCard = document.querySelector(`.trial-card[data-trial-id="${trialId}"]`);
    if (!trialCard) return;
    
    const email = trialCard.querySelector('[data-email]').getAttribute('data-email');
    const password = trialCard.querySelector('[data-password]').getAttribute('data-password');
    
    const details = `Service: ${trialCard.querySelector('.card-header').textContent.trim()}
Email: ${email}
Password: ${password}`;
    
    navigator.clipboard.writeText(details).then(() => {
        showAlert('success', 'Trial details copied to clipboard');
    }).catch(err => {
        console.error('Failed to copy: ', err);
        showAlert('danger', 'Failed to copy trial details');
    });
}

/**
 * Process referral commission withdrawal
 */
async function withdrawCommission() {
    const amount = document.getElementById('withdrawAmount').value;
    const walletAddress = document.getElementById('solanaAddress').value;
    
    if (!walletAddress) {
        showAlert('warning', 'Please enter a valid Solana wallet address');
        return;
    }
    
    // Show loading state
    const withdrawButton = document.querySelector('#withdrawModal .btn-success');
    const originalText = withdrawButton.textContent;
    withdrawButton.textContent = 'Processing...';
    withdrawButton.disabled = true;
    
    try {
        const response = await fetch('/api/withdraw-commission', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                amount: amount,
                wallet_address: walletAddress
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('withdrawModal'));
            modal.hide();
            
            // Show success message
            showAlert('success', `Successfully requested withdrawal of ${amount} SOL to your wallet. This may take up to 24 hours to process.`);
            
            // Reload page to show updated commission status
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            showAlert('danger', data.error || 'Failed to process withdrawal');
        }
    } catch (error) {
        console.error('Error processing withdrawal:', error);
        showAlert('danger', 'An error occurred while processing your withdrawal');
    } finally {
        // Reset button state
        withdrawButton.textContent = originalText;
        withdrawButton.disabled = false;
    }
}