// Roadmap Section Component for Trial Junkies

const RoadmapSection = () => {
  return (
    <section id="roadmap" className="roadmap-section py-5">
      <div className="container">
        <h2 className="display-4 fw-bold text-center text-burnt mb-5">EXPANSION PLANS</h2>
        <div className="roadmap-container">
          <div className="roadmap-intro text-center mb-5">
            <p className="lead">Our journey to revolutionize the free trial experience is just beginning. Here's the next supply chain for Trial Junkies:</p>
          </div>
          
          <div className="roadmap-timeline">
            <div className="roadmap-phase fade-in">
              <div className="phase-marker current">
                <span>Q2 2025</span>
              </div>
              <div className="phase-content">
                <h3>Phase 1: Core Platform Launch</h3>
                <ul className="phase-items">
                  <li className="completed">
                    <span className="item-title">Core Agent Deployment</span>
                    <p>Launch of Heroin Harry, Molly Morphine, and Keta Kev agents</p>
                  </li>
                  <li className="completed">
                    <span className="item-title">Discord & Telegram Integration</span>
                    <p>Bot deployment across major community platforms</p>
                  </li>
                  <li className="completed">
                    <span className="item-title">Solana Wallet Integration</span>
                    <p>Secure payment processing with Phantom wallet</p>
                  </li>
                  <li className="in-progress">
                    <span className="item-title">Subscription System</span>
                    <p>Tiered access to trial automation features</p>
                  </li>
                </ul>
              </div>
            </div>
            
            <div className="roadmap-phase fade-in">
              <div className="phase-marker">
                <span>Q3 2025</span>
              </div>
              <div className="phase-content">
                <h3>Phase 2: Enhanced Automation & Expansion</h3>
                <ul className="phase-items">
                  <li>
                    <span className="item-title">Twitter Bot Integration</span>
                    <p>Automated monitoring of company tweets and giveaways</p>
                  </li>
                  <li>
                    <span className="item-title">Advanced Proxy System</span>
                    <p>Improved stealth and success rates with enterprise-grade proxies</p>
                  </li>
                  <li>
                    <span className="item-title">Mobile App Launch</span>
                    <p>Native iOS and Android applications for on-the-go trial management</p>
                  </li>
                  <li>
                    <span className="item-title">Service Catalog Expansion</span>
                    <p>Support for 500+ services across streaming, productivity, and gaming</p>
                  </li>
                </ul>
              </div>
            </div>
            
            <div className="roadmap-phase fade-in">
              <div className="phase-marker">
                <span>Q4 2025</span>
              </div>
              <div className="phase-content">
                <h3>Phase 3: Token Launch & Ecosystem</h3>
                <ul className="phase-items">
                  <li>
                    <span className="item-title">$TRIAL Token Launch</span>
                    <p>Native cryptocurrency for the Trial Junkies ecosystem</p>
                  </li>
                  <li>
                    <span className="item-title">DAO Governance</span>
                    <p>Community voting on new features and supported services</p>
                  </li>
                  <li>
                    <span className="item-title">Staking Rewards</span>
                    <p>Earn passive income by staking $TRIAL tokens</p>
                  </li>
                  <li>
                    <span className="item-title">NFT Membership Cards</span>
                    <p>Exclusive benefits and lifetime access options</p>
                  </li>
                </ul>
              </div>
            </div>
            
            <div className="roadmap-phase fade-in">
              <div className="phase-marker">
                <span>2026</span>
              </div>
              <div className="phase-content">
                <h3>Phase 4: Real-World Activism & Global Expansion</h3>
                <ul className="phase-items">
                  <li>
                    <span className="item-title">Trial Junkies IRL Events</span>
                    <p>Community meetups and hackathons in major cities</p>
                  </li>
                  <li>
                    <span className="item-title">Corporate Partnerships</span>
                    <p>Official collaborations with service providers</p>
                  </li>
                  <li>
                    <span className="item-title">Multi-Chain Support</span>
                    <p>Expansion to Ethereum, Binance Smart Chain, and more</p>
                  </li>
                  <li>
                    <span className="item-title">Trial Junkies Platform API</span>
                    <p>Developer tools for building on top of our infrastructure</p>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          
          <div className="roadmap-cta text-center mt-5 pt-4">
            <p className="lead mb-4">Want to help us progress faster? Join our community and contribute to our development.</p>
            <a href="#discord" className="btn btn-lg btn-burnt me-3">
              <i className="fab fa-discord me-2"></i> Join Discord
            </a>
            <a href="#referral" className="btn btn-lg btn-outline-burnt">
              <i className="fas fa-users me-2"></i> Referral Program
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export default RoadmapSection;