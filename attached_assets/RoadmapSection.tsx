import React from 'react';

interface RoadmapPhase {
  date: string;
  title: string;
  items: {
    title: string;
    description: string;
    status: 'completed' | 'in-progress' | 'upcoming';
  }[];
}

const RoadmapSection: React.FC = () => {
  const phases: RoadmapPhase[] = [
    {
      date: "Q2 '25",
      title: "PHASE 1: CORE PLATFORM LAUNCH",
      items: [
        {
          title: "Core Agent Deployment",
          description: "Launch of Heroin Harry, Molly Morphine, and Keta Kev agents",
          status: "completed"
        },
        {
          title: "Discord & Telegram Integration",
          description: "Bot deployment across major community platforms",
          status: "completed"
        },
        {
          title: "Solana Wallet Integration",
          description: "Secure payment processing with Phantom wallet",
          status: "completed"
        },
        {
          title: "Subscription System",
          description: "Tiered access to trial automation features",
          status: "in-progress"
        }
      ]
    },
    {
      date: "Q3 '25",
      title: "PHASE 2: ENHANCED AUTOMATION & EXPANSION",
      items: [
        {
          title: "Twitter Bot Integration",
          description: "Automated monitoring of company tweets and giveaways",
          status: "upcoming"
        },
        {
          title: "Advanced Proxy System",
          description: "Improved stealth and success rates with enterprise-grade proxies",
          status: "upcoming"
        },
        {
          title: "Mobile App Launch",
          description: "Native iOS and Android applications for on-the-go trial management",
          status: "upcoming"
        }
      ]
    },
    {
      date: "Q4 '25",
      title: "PHASE 3: TOKEN LAUNCH & ECOSYSTEM",
      items: [
        {
          title: "$TRIAL Token Launch",
          description: "Native cryptocurrency for the Trial Junkies ecosystem",
          status: "upcoming"
        },
        {
          title: "DAO Governance",
          description: "Community voting on new features and supported services",
          status: "upcoming"
        },
        {
          title: "NFT Membership Cards",
          description: "Exclusive benefits and lifetime access options",
          status: "upcoming"
        }
      ]
    }
  ];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return (
          <span className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
            <i className="fas fa-check text-xs text-black"></i>
          </span>
        );
      case 'in-progress':
        return (
          <span className="w-5 h-5 bg-yellow-500 rounded-full flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
            <i className="fas fa-sync-alt text-xs text-black"></i>
          </span>
        );
      default:
        return (
          <span className="w-5 h-5 bg-[#121212] border border-[#FF5500] rounded-full flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
            <i className="fas fa-circle text-[6px] text-[#FF5500]"></i>
          </span>
        );
    }
  };

  return (
    <section id="roadmap" className="roadmap-section">
      <div className="roadmap-container">
        <h2 className="font-bebas text-4xl md:text-5xl text-[#FF5500] text-center mb-16">TRIAL JUNKIES ROADMAP</h2>
        
        <div className="roadmap-intro">
          <p>Our journey to revolutionize the free trial experience is just beginning. Here's what's coming next for Trial Junkies:</p>
        </div>
        
        <div className="roadmap-timeline">
          {phases.map((phase, phaseIndex) => (
            <div key={phaseIndex} className="roadmap-phase">
              <div className={`phase-marker ${phaseIndex === 0 ? 'current' : ''}`}>
                <span>{phase.date}</span>
              </div>
              
              <div className="phase-content">
                <h3>{phase.title}</h3>
                <ul className="phase-items">
                  {phase.items.map((item, itemIndex) => (
                    <li key={itemIndex} className={item.status}>
                      <div className="flex items-start">
                        {getStatusIcon(item.status)}
                        <div>
                          <span className="item-title">{item.title}</span>
                          <p>{item.description}</p>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default RoadmapSection;
