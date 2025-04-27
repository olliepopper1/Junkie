// Agent Section Component for Trial Junkies

const AgentSection = () => {
  const agents = [
    {
      id: 'heroin-harry',
      name: 'Heroin Harry',
      image: '/static/images/skeleton-green.png',
      title: 'Identity Provider | The Rush Master',
      description: 'Fast-talking, addicted to efficiency, and never sleeps. Harry generates the most authentic identities with hypnotic precision.',
      specialties: ['Email Generation', 'Phone Verification', 'Identity Creation'],
      quote: 'Got a new identity for ya... first one\'s always free, but you\'ll be back for more.'
    },
    {
      id: 'cash-carter',
      name: 'Cash Carter',
      image: '/static/images/skeleton-purple.png',
      title: 'Financial Guardian | Card Dealer',
      description: 'Sarcastic and protective, Cash handles all your financial needs with surgical precision. No payment loop can trap this dealer.',
      specialties: ['Card Generation', 'Payment Protection', 'Checkout Automation'],
      quote: 'My cards are clean, untraceable, and always hit just right. No comedowns, no traces.'
    },
    {
      id: 'vape-vince',
      name: 'Vape Vince',
      image: '/static/images/fire-skull.png',
      title: 'System Infiltrator | Subscription Bypasser',
      description: 'Cool, calculated, and mysterious. Vince slips through subscription barriers like smoke through fingers.',
      specialties: ['Paywall Bypassing', 'Cookie Manipulation', 'IP Rotation'],
      quote: 'Every system has a backdoor. I don\'t knock—I just float right in.'
    },
    {
      id: 'molly-morphine',
      name: 'Molly Morphine',
      image: '/static/images/pink-skeleton.png',
      title: 'Multi-Trial Specialist | The High Roller',
      description: 'Smooth-talking and reliable, Molly delivers multiple trials simultaneously, keeping your entertainment flowing.',
      specialties: ['Parallel Processing', 'Service Stacking', 'Renewal Prevention'],
      quote: 'Why settle for one when you can ride them all? That\'s the real euphoria, baby.'
    },
    {
      id: 'keta-kev',
      name: 'Keta Kev',
      image: '/static/images/phantom-logo.png',
      title: 'The Loop Runner | Trial Infinity Dealer',
      description: 'Intense, focused, and relentless. Kev generates trials on an infinite loop, keeping you in that k-hole of content.',
      specialties: ['Extended Trials', 'Account Recycling', 'Service Rotation'],
      quote: 'Once you go down this hole, you won\'t need to come up for air. I\'ve got you covered indefinitely.'
    }
  ];

  return (
    <section id="agents" className="agent-section py-5 fade-in">
      <div className="container">
        <div className="text-center mb-5">
          <h2 className="display-4 fw-bold text-burnt">MEET THE AGENTS</h2>
          <p className="lead text-white">Our specialized crew that delivers your digital fix</p>
        </div>
        
        <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          {agents.map((agent) => (
            <div className="col" key={agent.id}>
              <div className="agent-card h-100 fade-in">
                <div className="agent-image">
                  <img 
                    src={agent.image} 
                    alt={agent.name} 
                    className="img-fluid" 
                  />
                  <h3 className="agent-name">{agent.name}</h3>
                </div>
                <div className="agent-content">
                  <div className="agent-title">{agent.title}</div>
                  <p className="agent-description">{agent.description}</p>
                  
                  <div className="agent-specialties">
                    {agent.specialties.map((specialty, index) => (
                      <span className="agent-specialty" key={index}>
                        {specialty}
                      </span>
                    ))}
                  </div>
                  
                  <p className="agent-quote">{agent.quote}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default AgentSection;