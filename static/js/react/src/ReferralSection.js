// Referral Section Component for Trial Junkies

const ReferralSection = () => {
  const copyReferralCode = () => {
    // In a real implementation, this would copy the code to clipboard
    alert('Referral code copied to clipboard!');
  };

  return (
    <section id="referral" className="referral-section py-5">
      <div className="container">
        <div className="text-center mb-5">
          <h2 className="display-4 fw-bold text-burnt">DEAL & SCORE</h2>
          <p className="lead mb-4">Push our product, earn real Solana rewards. The more users you hook, the more you earn.</p>
        </div>

        <div className="row g-4 mb-5">
          <div className="col-md-4">
            <div className="referral-card h-100 pulse-animation">
              <div className="referral-icon float-animation">
                <i className="fas fa-users"></i>
              </div>
              <h3 className="referral-title">The Street Hustle</h3>
              <p className="referral-description">Share your unique referral code with friends and earn a cut every time they make a payment.</p>
              <ul className="referral-list">
                <li>20% commission on all payments</li>
                <li>Unlimited referrals</li>
                <li>Real Solana rewards</li>
                <li>Instant payouts</li>
              </ul>
            </div>
          </div>

          <div className="col-md-4">
            <div className="referral-card h-100 pulse-animation">
              <div className="referral-icon float-animation">
                <i className="fas fa-chart-line"></i>
              </div>
              <h3 className="referral-title">The Big Score</h3>
              <p className="referral-description">Climb the dealer ranks and unlock higher commission rates and exclusive rewards.</p>
              <ul className="referral-list">
                <li>Tier bonuses at 10, 25, 50 referrals</li>
                <li>Commission rate increases</li>
                <li>Early access to new features</li>
                <li>Exclusive dealer badge</li>
              </ul>
            </div>
          </div>

          <div className="col-md-4">
            <div className="referral-card h-100 pulse-animation">
              <div className="referral-icon float-animation">
                <i className="fas fa-wallet"></i>
              </div>
              <h3 className="referral-title">The Cash Out</h3>
              <p className="referral-description">Withdraw your earnings directly to your Solana wallet. No minimums, no delays.</p>
              <ul className="referral-list">
                <li>Direct Solana transfers</li>
                <li>Withdraw anytime</li>
                <li>No minimum thresholds</li>
                <li>Transparent tracking</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="referral-code-box glow-animation">
          <h3 className="referral-code-title">YOUR PERSONAL DEALER CODE</h3>
          <p className="text-center mb-4">Share this code to start earning. Each trial junkie who signs up under you puts more SOL in your wallet.</p>
          
          <div className="referral-code-input">
            <input type="text" className="referral-code" value="TRIALJUNKIES123" readOnly />
            <button className="copy-button" onClick={copyReferralCode}>
              <i className="fas fa-copy me-2"></i> Copy
            </button>
          </div>
          
          <div className="text-center mt-3">
            <a href="#" className="btn btn-burnt">
              <i className="fas fa-share-alt me-2"></i> Share Your Code
            </a>
          </div>
        </div>

        <div className="referral-stats mt-5">
          <div className="row g-4">
            <div className="col-md-3 col-6">
              <div className="stat-card float-animation">
                <div className="stat-value" id="referral-clicks">21</div>
                <div className="stat-label">Code Uses</div>
              </div>
            </div>
            
            <div className="col-md-3 col-6">
              <div className="stat-card float-animation">
                <div className="stat-value" id="referral-signups">8</div>
                <div className="stat-label">Paying Junkies</div>
              </div>
            </div>
            
            <div className="col-md-3 col-6">
              <div className="stat-card float-animation">
                <div className="stat-value" id="referral-active">5</div>
                <div className="stat-label">Active Users</div>
              </div>
            </div>
            
            <div className="col-md-3 col-6">
              <div className="stat-card float-animation">
                <div className="stat-value" id="referral-earnings">0.31</div>
                <div className="stat-label">SOL Earned</div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="community-section mt-5 pt-5">
          <div className="text-center mb-5">
            <h3 className="display-5 fw-bold text-burnt">JOIN THE CARTEL</h3>
            <p className="lead">Connect with other Trial Junkies in our underground community</p>
          </div>
          
          <div className="row g-4">
            <div className="col-md-6">
              <div className="platform-card h-100">
                <div className="platform-icon">
                  <i className="fab fa-discord"></i>
                </div>
                <h4 className="platform-title">Discord Dealers Den</h4>
                <p className="platform-description">Our main headquarters where all the action happens. Get instant hits, talk with agents, and connect with the community.</p>
                <a href="https://discord.gg/trialjunkie" className="btn btn-burnt platform-button">
                  <i className="fab fa-discord me-2"></i> Join Discord
                </a>
              </div>
            </div>
            
            <div className="col-md-6">
              <div className="platform-card h-100">
                <div className="platform-icon">
                  <i className="fab fa-telegram"></i>
                </div>
                <h4 className="platform-title">Telegram Drop Spot</h4>
                <p className="platform-description">Get mobile alerts for new services, hot trial opportunities, and quick command access on the go.</p>
                <a href="#" className="btn btn-burnt platform-button">
                  <i className="fab fa-telegram me-2"></i> Join Telegram
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ReferralSection;