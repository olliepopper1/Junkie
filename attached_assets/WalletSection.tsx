import React, { useState, useEffect } from 'react';
import { useWallet } from '@/hooks/useWallet';
import phantomLogo from '@assets/phantom-logo.svg';

interface PaymentOption {
  title: string;
  description: string;
  amount: string;
  type: 'subscription' | 'donation';
}

const WalletSection: React.FC = () => {
  const { 
    isConnected, 
    walletAddress, 
    isConnecting, 
    connect, 
    disconnect, 
    makePayment 
  } = useWallet();
  
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingMessage, setProcessingMessage] = useState('');

  const paymentOptions: PaymentOption[] = [
    {
      title: "Basic Trial",
      description: "Access to all basic trial features for 30 days",
      amount: "0.1",
      type: "subscription"
    },
    {
      title: "Premium Trial",
      description: "Unlimited trials with premium support",
      amount: "0.5",
      type: "subscription"
    },
    {
      title: "Donation",
      description: "Support the Trial Junkies project",
      amount: "0.2",
      type: "donation"
    }
  ];

  const handlePayment = async (amount: string, type: string) => {
    setIsProcessing(true);
    setProcessingMessage(`Processing your ${type} payment of ${amount} SOL...`);

    try {
      await makePayment(amount, type);
      setProcessingMessage('Transaction confirmed! Redirecting...');
      
      // Simulate delay for UI feedback
      setTimeout(() => {
        setIsProcessing(false);
        if (type === 'subscription') {
          alert(`Your ${amount} SOL ${type} has been activated successfully!`);
        } else {
          alert(`Thank you for your ${amount} SOL donation!`);
        }
      }, 1500);
    } catch (error) {
      console.error('Payment error:', error);
      setProcessingMessage('Transaction failed. Please try again.');
      
      setTimeout(() => {
        setIsProcessing(false);
      }, 1500);
    }
  };

  const handleWalletAction = () => {
    if (isConnected) {
      disconnect();
    } else {
      connect();
    }
  };

  return (
    <section id="wallet-section" className="wallet-section">
      <div className="container mx-auto px-4">
        <h2 className="font-bebas text-4xl md:text-5xl text-[#FF5500] text-center mb-16">CONNECT YOUR WALLET</h2>
        
        <div className="max-w-5xl mx-auto">
          <div className="bg-black bg-opacity-70 rounded-lg p-6 md:p-8 border border-[#FF5500] border-opacity-30">
            <div className="flex flex-col md:flex-row items-center md:space-x-8">
              <div className="flex items-center justify-center mb-8 md:mb-0">
                <img src={phantomLogo} alt="Phantom Logo" className="w-16 h-16 md:w-20 md:h-20 wallet-logo-animation" />
              </div>
              
              <div className="flex-1 flex flex-col items-center md:items-start">
                <div className={`wallet-status ${isConnected ? 'connected' : 'disconnected'}`}>
                  {isConnected ? 'Connected' : 'Disconnected'}
                </div>
                <div className="wallet-address">
                  {isConnected ? walletAddress : 'Not connected'}
                </div>
                <button 
                  onClick={handleWalletAction}
                  disabled={isConnecting}
                  className="connect mt-4"
                >
                  {isConnecting ? (
                    <><i className="fas fa-spinner fa-spin mr-2"></i> Connecting...</>
                  ) : isConnected ? (
                    <><i className="fas fa-sign-out-alt mr-2"></i> Disconnect</>
                  ) : (
                    <><i className="fas fa-wallet mr-2"></i> Connect Phantom Wallet</>
                  )}
                </button>
              </div>
            </div>
            
            <div id="wallet-actions" className={`wallet-actions ${isConnected ? 'active' : ''}`}>
              <h3 className="font-bebas text-2xl text-[#FF5500] mb-6 text-center">SUBSCRIPTION PLANS</h3>
              <div className="payment-options">
                {paymentOptions.map((option, index) => (
                  <div 
                    key={index} 
                    className={`payment-option ${index === 1 ? 'transform scale-105 relative' : ''}`}
                  >
                    {index === 1 && (
                      <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-[#FF5500] text-black text-xs font-bold py-1 px-3 rounded-full">
                        MOST POPULAR
                      </div>
                    )}
                    <h4 className="font-bebas text-xl mb-2">{option.title}</h4>
                    <p className="text-sm opacity-80 mb-4">{option.description}</p>
                    <div className="payment-amount">
                      {option.title === "Donation" ? "Any Amount" : `${option.amount} SOL`}
                    </div>
                    <button 
                      className="payment-button"
                      onClick={() => handlePayment(option.amount, option.type)}
                    >
                      {option.type === 'donation' ? 'Donate SOL' : 'Pay with SOL'}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Payment Processing Overlay */}
      {isProcessing && (
        <div className="fixed inset-0 bg-black bg-opacity-80 flex flex-col items-center justify-center z-50 transition-opacity duration-300">
          <div className="w-16 h-16 border-4 border-[#FF5500] border-t-transparent rounded-full animate-spin mb-6"></div>
          <div className="text-xl font-bold text-center max-w-md px-4">{processingMessage}</div>
        </div>
      )}
    </section>
  );
};

export default WalletSection;
