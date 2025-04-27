// SolanaPayment.js
// Handles Solana blockchain payments for Trial Junkie

/**
 * Solana Payment Component
 * Provides UI and functionality for processing Solana payments
 */
const SolanaPayment = ({ amount, reference, walletAddress, onSuccess, onCancel }) => {
  const [paymentStatus, setPaymentStatus] = useState('pending');
  const [txSignature, setTxSignature] = useState('');
  const [error, setError] = useState(null);
  const [countdown, setCountdown] = useState(900); // 15 minutes in seconds
  
  // Start countdown timer
  useEffect(() => {
    if (paymentStatus === 'pending') {
      const timer = setInterval(() => {
        setCountdown(prev => {
          if (prev <= 1) {
            clearInterval(timer);
            setPaymentStatus('expired');
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      
      return () => clearInterval(timer);
    }
  }, [paymentStatus]);
  
  // Format countdown as MM:SS
  const formatCountdown = () => {
    const minutes = Math.floor(countdown / 60);
    const seconds = countdown % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };
  
  // Copy wallet address to clipboard
  const copyWalletAddress = () => {
    navigator.clipboard.writeText(walletAddress);
    alert('Wallet address copied to clipboard!');
  };
  
  // Verify payment status
  const verifyPayment = async () => {
    try {
      setPaymentStatus('verifying');
      
      // Import the API for payment verification
      const { verifyPayment } = await import('./api.js');
      
      // Call verify payment API
      const result = await verifyPayment(reference, txSignature);
      
      if (result.success) {
        setPaymentStatus('completed');
        if (onSuccess) onSuccess(result);
      } else {
        setPaymentStatus('pending');
        setError(result.message || 'Payment verification failed. Please try again in a few minutes.');
      }
    } catch (error) {
      setPaymentStatus('pending');
      setError('An error occurred during payment verification. Please try again.');
      console.error('Payment verification error:', error);
    }
  };
  
  return (
    <div className="solana-payment-container">
      <div className="card border-primary mb-4">
        <div className="card-header bg-primary text-white">
          <h5 className="mb-0">Complete Your Payment</h5>
        </div>
        <div className="card-body">
          {paymentStatus === 'pending' && (
            <>
              <div className="alert alert-info">
                <div className="d-flex justify-content-between align-items-center">
                  <span>Amount to send: <strong>{amount} SOL</strong></span>
                  <span className="badge bg-warning">Time left: {formatCountdown()}</span>
                </div>
              </div>
              
              <div className="mb-3">
                <label className="form-label">Send payment to this Solana wallet address:</label>
                <div className="input-group mb-3">
                  <input 
                    type="text" 
                    className="form-control" 
                    value={walletAddress} 
                    readOnly 
                  />
                  <button 
                    className="btn btn-outline-secondary" 
                    type="button"
                    onClick={copyWalletAddress}
                  >
                    <i className="fas fa-copy"></i> Copy
                  </button>
                </div>
              </div>
              
              <div className="mb-3">
                <div className="d-flex justify-content-between align-items-center mb-2">
                  <label className="form-label mb-0">Payment Reference:</label>
                  <span className="badge bg-secondary">{reference}</span>
                </div>
                <div className="alert alert-warning">
                  <small>
                    <i className="fas fa-exclamation-triangle me-2"></i>
                    Important: Include this reference code in the transaction memo field
                  </small>
                </div>
              </div>
              
              <div className="mb-3">
                <label className="form-label">Transaction Signature (optional):</label>
                <input 
                  type="text" 
                  className="form-control" 
                  placeholder="Enter Solana transaction signature" 
                  value={txSignature}
                  onChange={e => setTxSignature(e.target.value)}
                />
                <div className="form-text">
                  If you know your transaction signature, enter it here to verify your payment faster.
                </div>
              </div>
              
              {error && (
                <div className="alert alert-danger mb-3">
                  {error}
                </div>
              )}
              
              <div className="d-grid gap-2">
                <button 
                  className="btn btn-primary" 
                  onClick={verifyPayment}
                >
                  <i className="fas fa-check-circle me-2"></i>
                  Verify My Payment
                </button>
                
                <button 
                  className="btn btn-outline-secondary" 
                  onClick={onCancel}
                >
                  Cancel
                </button>
              </div>
            </>
          )}
          
          {paymentStatus === 'verifying' && (
            <div className="text-center py-4">
              <div className="spinner-border text-primary mb-3" role="status">
                <span className="visually-hidden">Loading...</span>
              </div>
              <h5>Verifying your payment...</h5>
              <p className="text-muted">
                This may take a few moments while we confirm your transaction on the Solana blockchain.
              </p>
            </div>
          )}
          
          {paymentStatus === 'completed' && (
            <div className="text-center py-4">
              <div className="mb-3">
                <i className="fas fa-check-circle text-success" style={{ fontSize: '4rem' }}></i>
              </div>
              <h5>Payment Successful!</h5>
              <p>
                Your payment has been verified and your subscription has been activated.
              </p>
              <button 
                className="btn btn-success" 
                onClick={() => window.location.reload()}
              >
                Continue to Dashboard
              </button>
            </div>
          )}
          
          {paymentStatus === 'expired' && (
            <div className="text-center py-4">
              <div className="mb-3">
                <i className="fas fa-clock text-danger" style={{ fontSize: '4rem' }}></i>
              </div>
              <h5>Payment Time Expired</h5>
              <p>
                The payment session has expired. Please start a new payment session.
              </p>
              <button 
                className="btn btn-primary" 
                onClick={() => window.location.reload()}
              >
                Start New Payment
              </button>
            </div>
          )}
        </div>
      </div>
      
      <div className="card">
        <div className="card-header">
          <h5 className="mb-0">Payment Instructions</h5>
        </div>
        <div className="card-body">
          <ol className="mb-0">
            <li className="mb-2">Send <strong>{amount} SOL</strong> to the wallet address above.</li>
            <li className="mb-2">Make sure to include the reference code in the transaction memo.</li>
            <li className="mb-2">After sending, click "Verify My Payment" to check the status.</li>
            <li className="mb-2">Once verified, your subscription will be activated immediately.</li>
          </ol>
        </div>
      </div>
    </div>
  );
};