// Meet The Bots Section Component for Trial Junkies

const MeetTheBotsSection = () => {
  const bots = [
    {
      name: "HEROIN HARRY",
      subtitle: "Microdose",
      image: "/img/purple-pill-logo.png",
      description: "Harry handles one-shot free trial creation using burner emails, SMS verification, and fake debit cards. He's sarcastic and teasing, acting like he's doing you a shady favor.",
      command: "!hit [service]",
      commandDescription: "Triggers one full account generation",
      features: [
        { icon: "fa-bolt", text: "Fast & Efficient" },
        { icon: "fa-shield-alt", text: "Basic Protection" }
      ],
      animation: "heroin-harry-animation",
      botType: "heroin-harry"
    },
    {
      name: "MOLLY MORPHINE",
      subtitle: "Binge",
      image: "/img/purple-pill-logo.png",
      description: "Molly runs 3 trial signups at a time for the same service. Her personality is cool and smooth-talking, always delivering like a reliable plug.",
      command: "!binge [service]",
      commandDescription: "Runs 3 trial signups for the specified service",
      features: [
        { icon: "fa-users", text: "Multi-Account" },
        { icon: "fa-database", text: "Credential Storage" }
      ],
      animation: "molly-morphine-animation",
      botType: "molly-morphine"
    },
    {
      name: "KETA KEV",
      subtitle: "Overdose",
      image: "/img/purple-pill-logo.png",
      description: "Kev generates free trials on an infinite loop with login token capture. He's spaced out but insanely reliable, with psychedelic coder vibes.",
      command: "!overdose [service]",
      commandDescription: "Generates trials on an infinite loop",
      features: [
        { icon: "fa-infinity", text: "Infinite Loop" },
        { icon: "fa-robot", text: "Advanced AI" }
      ],
      animation: "keta-kev-animation",
      botType: "keta-kev"
    }
  ];

  // Bot Card Component
  const BotCard = ({ bot }) => (
    <div className="bot-card fade-in h-100">
      <div className="card bg-dark border-burnt" style={{borderRadius: '8px', overflow: 'hidden'}}>
        <div className="bot-header position-relative">
          <div className="bg-black d-flex justify-content-center py-4">
            <img 
              src={bot.image} 
              alt={bot.name} 
              className={`bot-image ${bot.animation}`} 
              style={{maxHeight: '150px'}} 
            />
          </div>
          <div className="bot-subtitle position-absolute top-0 end-0 bg-burnt text-dark py-1 px-3 m-2 rounded-pill">
            {bot.subtitle}
          </div>
        </div>
        
        <div className="card-body">
          <h3 className="text-burnt text-center mb-3">{bot.name}</h3>
          <p className="bot-description opacity-80 mb-4">{bot.description}</p>
          
          <div className="command-box bg-black p-3 rounded mb-4 border border-burnt border-opacity-30">
            <div className="command-title small text-muted mb-1">Command:</div>
            <div className="command-code font-monospace text-burnt">
              {bot.command}
            </div>
            <div className="command-description small opacity-70 mt-1">
              {bot.commandDescription}
            </div>
          </div>
          
          <div className="bot-features d-flex justify-content-around">
            {bot.features.map((feature, index) => (
              <div key={index} className="feature-item text-center">
                <div className="feature-icon">
                  <i className={`fas ${feature.icon} text-burnt`}></i>
                </div>
                <div className="feature-text small mt-2">{feature.text}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <section id="meet-the-bots" className="py-5 bg-black position-relative overflow-hidden">
      <div className="position-absolute top-0 start-0 w-100 h-100 bg-radial-gradient opacity-20"></div>
      
      <div className="container position-relative z-1">
        <div className="text-center mb-5">
          <h2 className="display-4 fw-bold text-burnt">MEET THE BOTS</h2>
          <p className="lead">Our specialized agents are here to hook you up with free trials</p>
        </div>
        
        <div className="row row-cols-1 row-cols-md-3 g-4 mb-5">
          {bots.map((bot, index) => (
            <div className="col" key={index}>
              <BotCard bot={bot} />
            </div>
          ))}
        </div>
        
        {/* Overdose Mode */}
        <div className="overdose-mode-card p-4 bg-gradient-to-r-dark-purple border border-burnt border-opacity-40 rounded-lg mt-5 position-relative overflow-hidden glow-animation">
          <div className="overdose-glow-1 position-absolute top-0 end-0"></div>
          <div className="overdose-glow-2 position-absolute bottom-0 start-0"></div>
          
          <h3 className="text-burnt display-6 mb-4 position-relative">
            OVERDOSE MODE ACTIVATED
            <span className="position-absolute top-0 end-0 badge bg-warning animate-pulse">PREMIUM</span>
          </h3>
          
          <p className="lead mb-4">Get all trials, no limits. Includes full automation, premium support, and first dibs on new services. Ride the wave—risk-free.</p>
          
          <div className="row g-3 mb-4">
            <div className="col-md-6">
              <div className="bg-black bg-opacity-50 p-3 rounded-md border border-burnt border-opacity-20">
                <h4 className="text-burnt fs-5 mb-3">Commands:</h4>
                <div className="bg-black p-3 rounded font-monospace border border-burnt border-opacity-10">
                  <code className="text-burnt">!overdose_mode [service] [fullsend:true/false]</code>
                  <div className="small opacity-70 mt-1">Runs all agents together</div>
                </div>
              </div>
            </div>
            <div className="col-md-6">
              <div className="bg-black bg-opacity-50 p-3 rounded-md border border-burnt border-opacity-20">
                <h4 className="text-burnt fs-5 mb-3">Features:</h4>
                <ul className="list-unstyled mb-0">
                  <li className="d-flex align-items-start mb-2">
                    <i className="fas fa-check text-burnt mt-1 me-2 animate-pulse"></i>
                    <span>Maximum parallelization</span>
                  </li>
                  <li className="d-flex align-items-start mb-2">
                    <i className="fas fa-check text-burnt mt-1 me-2 animate-pulse"></i>
                    <span>Auto-retry on failures</span>
                  </li>
                  <li className="d-flex align-items-start">
                    <i className="fas fa-check text-burnt mt-1 me-2 animate-pulse"></i>
                    <span>Advanced stealth measures</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          
          <div className="text-center">
            <a 
              href="#wallet-section" 
              className="btn btn-burnt btn-lg pulse-animation"
            >
              <i className="fas fa-syringe me-2"></i> Activate Overdose Mode
            </a>
            <div className="small mt-2 bg-black bg-opacity-70 py-1 px-3 rounded d-inline-block border border-warning border-opacity-30">
              <span className="text-warning"><i className="fas fa-exclamation-triangle me-1"></i> Premium subscription required</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default MeetTheBotsSection;