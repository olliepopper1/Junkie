import React, { useState } from 'react';

const ReferralSection: React.FC = () => {
  const [referralCode] = useState('TRIALJUNKIES123');
  const [copySuccess, setCopySuccess] = useState(false);

  const referralCards = [
    {
      icon: "fa-link",
      title: "SHARE YOUR LINK",
      description: "Get your unique referral link and share it with friends, on social media, or in communities where people are looking to save money.",
      features: [
        "Automatic tracking of clicks",
        "Custom link shortening",
        "Social media friendly"
      ],
      button: {
        text: "Generate Link",
        action: () => console.log("Generating link...")
      }
    },
    {
      icon: "fa-users",
      title: "EARN REWARDS",
      description: "Earn 20% of every subscription payment made by users who sign up with your referral link, for as long as they remain subscribed.",
      features: [
        "20% commission on all plans",
        "Recurring passive income",
        "Paid directly to your wallet"
      ],
      button: {
        text: "View Commission Rates",
        action: () => console.log("Viewing commission rates...")
      }
    },
    {
      icon: "fa-chart-line",
      title: "TRACK PROGRESS",
      description: "Monitor your referral performance with detailed analytics. See clicks, sign-ups, and earnings in real-time.",
      features: [
        "Real-time referral dashboard",
        "Conversion tracking",
        "Earnings forecasts"
      ],
      button: {
        text: "Open Dashboard",
        action: () => console.log("Opening dashboard...")
      }
    }
  ];

  const stats = [
    { number: "21", label: "Link Clicks" },
    { number: "8", label: "Sign-ups" },
    { number: "5", label: "Active Users" },
    { number: "0.31", label: "SOL Earned" }
  ];

  const platforms = [
    {
      icon: "fab fa-discord",
      title: "DISCORD",
      description: "Join our Discord server for tech support, updates, and to connect with other trial junkies.",
      button: {
        text: "Join Discord",
        className: "discord",
        url: "#"
      }
    },
    {
      icon: "fab fa-telegram-plane",
      title: "TELEGRAM",
      description: "Join our Telegram channel for instant notifications about new trials and features.",
      button: {
        text: "Join Telegram",
        className: "telegram",
        url: "#"
      }
    }
  ];

  const copyToClipboard = () => {
    navigator.clipboard.writeText(referralCode).then(() => {
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    });
  };

  return (
    <section id="referral" className="referral-section">
      <div className="referral-container">
        <h2 className="font-bebas text-4xl md:text-5xl text-[#FF5500] text-center mb-16">REFERRAL PROGRAM</h2>
        
        <div className="referral-intro">
          <h3 className="font-bebas text-2xl md:text-3xl text-[#FF5500] mb-4">SHARE THE ADDICTION</h3>
          <p className="mb-8">Earn SOL by inviting others to join Trial Junkies. The more users you refer, the more you earn. It's like being a dealer, but legal!</p>
        </div>
        
        <div className="referral-cards">
          {referralCards.map((card, index) => (
            <div key={index} className="referral-card">
              <div className="referral-card-header">
                <div className="referral-card-icon">
                  <i className={`fas ${card.icon}`}></i>
                </div>
                <h3 className="referral-card-title">{card.title}</h3>
              </div>
              <div className="referral-card-content">
                <p>{card.description}</p>
                <ul>
                  {card.features.map((feature, featureIndex) => (
                    <li key={featureIndex}>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="referral-card-footer">
                <button 
                  className="referral-button"
                  onClick={card.button.action}
                >
                  {card.button.text}
                </button>
              </div>
            </div>
          ))}
        </div>
        
        {/* Referral Code Section */}
        <div className="referral-code-container">
          <h3 className="referral-code-title">YOUR REFERRAL CODE</h3>
          <div className="referral-code-input">
            <input 
              type="text" 
              value={referralCode} 
              className="referral-code" 
              readOnly
            />
            <button 
              className="copy-button"
              onClick={copyToClipboard}
            >
              <i className={`fas ${copySuccess ? 'fa-check' : 'fa-copy'} mr-2`}></i>
              {copySuccess ? 'Copied!' : 'Copy'}
            </button>
          </div>
          
          <div className="referral-stats">
            {stats.map((stat, index) => (
              <div key={index} className="stat-card">
                <div className="stat-number">{stat.number}</div>
                <div className="stat-label">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Community Section */}
        <div className="community-container">
          <div className="community-intro">
            <h3 className="font-bebas text-2xl md:text-3xl text-[#FF5500] mb-8">JOIN OUR COMMUNITY</h3>
          </div>
          <div className="community-platforms">
            {platforms.map((platform, index) => (
              <div key={index} className="platform-card">
                <i className={`${platform.icon} platform-icon`}></i>
                <h3 className="platform-title">{platform.title}</h3>
                <p className="platform-description">{platform.description}</p>
                <a 
                  href={platform.button.url} 
                  className={`platform-button ${platform.button.className}`}
                >
                  {platform.button.text}
                </a>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default ReferralSection;
