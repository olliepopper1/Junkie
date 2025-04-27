// React App for Trial Junkies
const { useState, useEffect } = React;

// Import components
// These will be loaded from the script tags in index.html
const AgentSection = window.AgentSection || (() => <div>Agent Section Loading...</div>);
const DiscordSection = window.DiscordSection || (() => <div>Discord Section Loading...</div>);
const ReferralSection = window.ReferralSection || (() => <div>Referral Section Loading...</div>);
const RoadmapSection = window.RoadmapSection || (() => <div>Roadmap Section Loading...</div>);

// Main App Component
function App() {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    // Simulate loading time for animations
    const timer = setTimeout(() => {
      setIsLoaded(true);
      console.log("Trial Junkie Dashboard Initialized");
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className={`app-container ${isLoaded ? 'loaded' : ''}`}>
      <Navbar />
      <Hero />
      <ServicesSection />
      <AgentSection />
      <HowItWorksSection />
      <DiscordSection />
      <PricingSection />
      <ReferralSection />
      <RoadmapSection />
      <TestimonialsSection />
      <FAQ />
      <Footer />
    </div>
  );
}

// Navbar Component
function Navbar() {
  const [navbarOpen, setNavbarOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`navbar navbar-expand-lg navbar-dark ${scrolled ? 'bg-black' : 'bg-transparent'} fixed-top`}>
      <div className="container">
        <a className="navbar-brand" href="#">
          <i className="fas fa-syringe me-2 text-blood"></i>
          Trial Junkies
        </a>
        <button 
          className="navbar-toggler" 
          type="button" 
          onClick={() => setNavbarOpen(!navbarOpen)}
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className={`collapse navbar-collapse ${navbarOpen ? 'show' : ''}`}>
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <a className="nav-link" href="#services">Services</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#agents">Agents</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#how-it-works">How It Works</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#discord">Discord Bot</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#pricing">Pricing</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#referral">Referrals</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#roadmap">Roadmap</a>
            </li>
            <li className="nav-item">
              <a className="nav-link btn btn-burnt ms-lg-3" href="https://discord.gg/trialjunkie">
                <i className="fab fa-discord me-2"></i> Get Your Fix
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

// Hero Section
function Hero() {
  return (
    <section className="hero-section py-5 mb-0">
      <div className="container py-5">
        <div className="row align-items-center min-vh-100">
          <div className="col-lg-6 fade-in">
            <h1 className="display-3 fw-bold text-burnt mb-4">NO REHAB, JUST FREE TRIALS</h1>
            <p className="lead mb-4">Get your fix of premium content with our powerful trial generation system. Our agents create working accounts for all major streaming services. First hit's always free.</p>
            <div className="d-flex gap-3">
              <a href="https://discord.gg/trialjunkie" className="btn btn-burnt btn-lg pulse-animation">
                <i className="fab fa-discord me-2"></i> Join Discord
              </a>
              <a href="#how-it-works" className="btn btn-outline-burnt btn-lg">
                <i className="fas fa-syringe me-2"></i> Learn More
              </a>
            </div>
          </div>
          <div className="col-lg-6 d-none d-lg-block text-center">
            <img src="/static/images/fire-skull.png" className="img-fluid hero-image" alt="Trial Junkies Hero" />
          </div>
        </div>
      </div>
    </section>
  );
}

// Services Section
function ServicesSection() {
  const services = [
    { name: "Netflix", icon: "fa-play", color: "var(--burnt-orange)" },
    { name: "Hulu", icon: "fa-tv", color: "var(--burnt-orange)" },
    { name: "Disney+", icon: "fa-star", color: "var(--burnt-orange)" },
    { name: "Amazon Prime", icon: "fa-box", color: "var(--burnt-orange)" },
    { name: "Spotify", icon: "fa-music", color: "var(--burnt-orange)" },
    { name: "YouTube Premium", icon: "fa-youtube", color: "var(--burnt-orange)" },
    { name: "HBO Max", icon: "fa-film", color: "var(--burnt-orange)" },
    { name: "Paramount+", icon: "fa-mountain", color: "var(--burnt-orange)" }
  ];

  return (
    <section id="services" className="services-section py-5">
      <div className="container">
        <div className="text-center mb-5 position-relative z-1">
          <h2 className="display-4 fw-bold text-burnt">PREMIUM DOSES</h2>
          <p className="lead">Score these high-quality streaming services without the subscription comedown</p>
        </div>
        
        <div className="row row-cols-2 row-cols-md-4 g-4">
          {services.map((service, index) => (
            <div className="col" key={index}>
              <div className="service-card h-100 text-center fade-in">
                <div className="card-body">
                  <div className="icon-wrapper mb-3" style={{ backgroundColor: service.color, width: "64px", height: "64px", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto" }}>
                    <i className={`fas ${service.icon} fa-2x text-black`}></i>
                  </div>
                  <h5 className="card-title text-burnt">{service.name}</h5>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// How It Works Section
function HowItWorksSection() {
  const steps = [
    {
      title: "Join Our Discord",
      description: "Enter our underground network to access the Trial Junkie system.",
      icon: "fa-discord"
    },
    {
      title: "Choose Your Dose",
      description: "Select your streaming service poison to get your entertainment fix.",
      icon: "fa-syringe"
    },
    {
      title: "Get Your Trial",
      description: "Our dealer agents hook you up with working trial credentials.",
      icon: "fa-key"
    },
    {
      title: "Feel The High",
      description: "Log in and enjoy the rush of premium content without the subscription crash.",
      icon: "fa-tv"
    }
  ];

  return (
    <section id="how-it-works" className="how-it-works-section py-5">
      <div className="container">
        <div className="text-center mb-5 position-relative z-1">
          <h2 className="display-4 fw-bold text-burnt">HOW TO SCORE</h2>
          <p className="lead">Getting your trial fix is quick and potent</p>
        </div>
        
        <div className="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4">
          {steps.map((step, index) => (
            <div className="col" key={index}>
              <div className="step-card h-100 fade-in">
                <div className="step-number mb-3">
                  {index + 1}
                </div>
                <div className="icon-wrapper mb-3">
                  <i className={`${step.icon.includes('discord') ? 'fab' : 'fas'} ${step.icon} fa-3x text-burnt`}></i>
                </div>
                <h4 className="text-burnt">{step.title}</h4>
                <p>{step.description}</p>
              </div>
            </div>
          ))}
        </div>
        
        <div className="text-center mt-5 position-relative z-1">
          <h3 className="text-burnt fs-4 mb-4">DEALER COMMANDS</h3>
          <div className="command-card mx-auto" style={{ maxWidth: "600px" }}>
            <pre className="mb-0 text-white">
              <code>
                !hit netflix        # Score a full trial fix<br/>
                !dose harry netflix # Identity hit only<br/>
                !dose cash netflix  # Payment card fix<br/>
                !stash              # View your stash<br/>
                !trip netflix       # Automated sign-up trip
              </code>
            </pre>
          </div>
        </div>
      </div>
    </section>
  );
}

// Pricing Section
function PricingSection() {
  const plans = [
    {
      name: "Street Dealer",
      price: "$0",
      period: "/mo",
      features: [
        "1 hit per day",
        "3 doses per day",
        "No automation",
        "Basic support"
      ],
      buttonText: "Start Dealing",
      featured: false
    },
    {
      name: "Five Dollar Rush",
      price: "$5",
      period: "/week",
      features: [
        "5 hits per day",
        "10 doses per day",
        "3 trips per day",
        "7-day premium access"
      ],
      buttonText: "Get Your Rush",
      featured: true
    },
    {
      name: "Junkified",
      price: "$19.99",
      period: "/mo",
      features: [
        "50 hits per day",
        "100 doses per day",
        "30 trips per day",
        "Priority support"
      ],
      buttonText: "Go Full Junkie",
      featured: false
    }
  ];

  return (
    <section id="pricing" className="pricing-section py-5">
      <div className="container">
        <div className="text-center mb-5 position-relative z-1">
          <h2 className="display-4 fw-bold text-burnt">CHOOSE YOUR FIX</h2>
          <p className="lead">Select the plan that matches your streaming addiction level</p>
        </div>
        
        <div className="row row-cols-1 row-cols-md-3 g-4 justify-content-center">
          {plans.map((plan, index) => (
            <div className="col" key={index}>
              <div className={`pricing-card h-100 ${plan.featured ? 'featured' : ''} fade-in`}>
                {plan.featured && <div className="card-header py-3"><strong>Most Potent</strong></div>}
                <div className="card-body">
                  <h3 className="card-title text-burnt">{plan.name}</h3>
                  <div className="pricing mb-3">
                    <span className="price">{plan.price}</span>
                    <span className="period">{plan.period}</span>
                  </div>
                  <ul className="feature-list">
                    {plan.features.map((feature, i) => (
                      <li className="mb-2" key={i}>
                        <i className="fas fa-check me-2"></i>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="card-footer bg-transparent border-0 pb-4">
                  <a href="https://discord.gg/trialjunkie" className={`btn ${plan.featured ? 'btn-burnt' : 'btn-outline-burnt'} d-block`}>
                    {plan.buttonText}
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="payment-info text-center mt-5 position-relative z-1">
          <p>We accept Solana cryptocurrency for ultimate privacy</p>
          <div className="crypto-icons mt-2">
            <i className="fas fa-wallet text-burnt me-3 fs-3"></i>
            <i className="fab fa-bitcoin me-3 fs-3"></i>
            <i className="fas fa-coins text-burnt fs-3"></i>
          </div>
        </div>
      </div>
    </section>
  );
}

// Testimonials Section
function TestimonialsSection() {
  const testimonials = [
    {
      name: "Mike T.",
      avatar: "/static/images/skeleton-green.png",
      text: "Got hooked on Trial Junkie months ago. Now I'm saving hundreds every month on subscription fees. This is the real deal!",
      platform: "Discord"
    },
    {
      name: "Sarah L.",
      avatar: "/static/images/skeleton-purple.png",
      text: "These agents deliver the purest trial accounts I've ever seen. No detection, no subscription hangover, just pure streaming bliss.",
      platform: "Twitter"
    },
    {
      name: "David K.",
      avatar: "/static/images/fire-skull.png",
      text: "The automated trip feature is worth every SOL. One click and I'm flying high with premium content. Never looking back.",
      platform: "Discord"
    }
  ];

  return (
    <section className="testimonials-section py-5">
      <div className="container">
        <div className="text-center mb-5 position-relative z-1">
          <h2 className="display-4 fw-bold text-burnt">SATISFIED JUNKIES</h2>
          <p className="lead">Hear from users who've tried our product</p>
        </div>
        
        <div className="row row-cols-1 row-cols-md-3 g-4">
          {testimonials.map((testimonial, index) => (
            <div className="col" key={index}>
              <div className="testimonial-card h-100 fade-in">
                <div className="d-flex align-items-center mb-3">
                  <img src={testimonial.avatar} className="rounded-circle me-3" width="60" height="60" alt={testimonial.name} />
                  <div>
                    <h5 className="mb-0 text-burnt">{testimonial.name}</h5>
                    <small>via {testimonial.platform}</small>
                  </div>
                </div>
                <p className="quote">{testimonial.text}</p>
                <div className="text-burnt mt-3">
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// FAQ Section
function FAQ() {
  const faqs = [
    {
      question: "How does Trial Junkie work?",
      answer: "Our network of specialized agents creates working trial accounts with valid payment information that pass verification checks. We've refined our formula for maximum potency and reliability."
    },
    {
      question: "Is this legal?",
      answer: "Trial Junkie operates in a gray area. We're simply automating the trial sign-up process that's available to everyone. Users are responsible for their own usage and compliance with service terms."
    },
    {
      question: "What happens after the trial period ends?",
      answer: "Trials will naturally expire after the free period. Our payment methods are designed to pass initial verification but won't face the comedown of charges after the trial period ends."
    },
    {
      question: "What services do you support?",
      answer: "We deal in all major streaming platforms including Netflix, Hulu, Disney+, Amazon Prime, HBO Max, Spotify, YouTube Premium, and many more. Our catalog is constantly expanding."
    },
    {
      question: "How do I get started?",
      answer: "Join our Discord server for your first hit. Use the !help command to see all available commands and get started with your trial generation journey."
    },
    {
      question: "What payment methods do you accept?",
      answer: "We exclusively deal in cryptocurrency (primarily Solana) for maximum privacy and security. Payment instructions are provided when you upgrade your plan."
    }
  ];

  const [activeIndex, setActiveIndex] = useState(null);

  const toggleFAQ = (index) => {
    setActiveIndex(activeIndex === index ? null : index);
  };

  return (
    <section id="faq" className="faq-section py-5">
      <div className="container">
        <div className="text-center mb-5 position-relative z-1">
          <h2 className="display-4 fw-bold text-burnt">FAQ</h2>
          <p className="lead">Everything you need to know before your first hit</p>
        </div>
        
        <div className="row justify-content-center">
          <div className="col-lg-8 position-relative z-1">
            <div className="accordion" id="faqAccordion">
              {faqs.map((faq, index) => (
                <div className="accordion-item mb-3" key={index}>
                  <h2 className="accordion-header">
                    <button 
                      className={`accordion-button ${activeIndex === index ? '' : 'collapsed'}`} 
                      type="button" 
                      onClick={() => toggleFAQ(index)}
                    >
                      {faq.question}
                    </button>
                  </h2>
                  <div className={`accordion-collapse collapse ${activeIndex === index ? 'show' : ''}`}>
                    <div className="accordion-body">
                      {faq.answer}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

// Footer Component
function Footer() {
  const currentYear = new Date().getFullYear();
  const [logoHovered, setLogoHovered] = useState(false);

  return (
    <footer className="footer">
      <div className="container footer-content">
        <div className="row py-5">
          {/* Logo & Brand Info */}
          <div className="col-lg-4 mb-5 mb-lg-0">
            <div 
              className="footer-logo d-flex align-items-center mb-4"
              onMouseEnter={() => setLogoHovered(true)}
              onMouseLeave={() => setLogoHovered(false)}
            >
              <div className="position-relative me-3">
                <img 
                  src="/static/images/fire-skull.png" 
                  alt="Trial Junkies Logo" 
                  width="50" 
                  className={`${logoHovered ? 'animate-fiery-pulse' : 'animate-flame-flicker'}`}
                />
              </div>
              <span className="footer-heading">TRIAL JUNKIES</span>
            </div>
            <p className="mb-4 footer-text">No Rehab, Just Free Trials. Automate your way to subscription freedom with our premium agents.</p>
            <div className="social-icons">
              <a href="https://discord.gg/trialjunkie" className="me-3"><i className="fab fa-discord fs-4"></i></a>
              <a href="#" className="me-3"><i className="fab fa-twitter fs-4"></i></a>
              <a href="#" className="me-3"><i className="fab fa-telegram fs-4"></i></a>
              <a href="#"><i className="fab fa-reddit fs-4"></i></a>
            </div>
          </div>
          
          {/* Quick Links */}
          <div className="col-lg-2 col-md-4 mb-4 mb-md-0">
            <h5 className="footer-heading">QUICK LINKS</h5>
            <ul className="list-unstyled footer-links">
              <li><a href="#services" className="footer-link"><i className="fas fa-angle-right me-2 text-burnt"></i>Services</a></li>
              <li><a href="#agents" className="footer-link"><i className="fas fa-angle-right me-2 text-burnt"></i>Agents</a></li>
              <li><a href="#how-it-works" className="footer-link"><i className="fas fa-angle-right me-2 text-burnt"></i>How It Works</a></li>
              <li><a href="#pricing" className="footer-link"><i className="fas fa-angle-right me-2 text-burnt"></i>Pricing</a></li>
              <li><a href="#referral" className="footer-link"><i className="fas fa-angle-right me-2 text-burnt"></i>Referrals</a></li>
            </ul>
          </div>
          
          {/* Resources */}
          <div className="col-lg-2 col-md-4 mb-4 mb-md-0">
            <h5 className="footer-heading">RESOURCES</h5>
            <ul className="list-unstyled footer-links">
              <li><a href="#discord" className="footer-link"><i className="fas fa-angle-right me-2 text-burnt"></i>Commands</a></li>
              <li><a href="#roadmap" className="footer-link"><i className="fas fa-angle-right me-2 text-burnt"></i>Roadmap</a></li>
              <li><a href="#faq" className="footer-link"><i className="fas fa-angle-right me-2 text-burnt"></i>FAQ</a></li>
              <li><a href="#" className="footer-link"><i className="fas fa-angle-right me-2 text-burnt"></i>Terms of Service</a></li>
              <li><a href="#" className="footer-link"><i className="fas fa-angle-right me-2 text-burnt"></i>Privacy Policy</a></li>
            </ul>
          </div>
          
          {/* Newsletter */}
          <div className="col-lg-4 col-md-4">
            <h5 className="footer-heading">GET UPDATES</h5>
            <p className="mb-3 footer-text">Stay informed about new agents and service updates. No spam, just quality drops.</p>
            <div className="input-group mb-4">
              <input 
                type="email" 
                className="form-control bg-black border-burnt"
                placeholder="Your email address" 
              />
              <button 
                className="btn btn-burnt"
                type="button"
              >
                <i className="fas fa-arrow-right"></i>
              </button>
            </div>
            <div className="footer-discord mt-4">
              <a href="https://discord.gg/trialjunkie" className="btn btn-burnt btn-lg w-100">
                <i className="fab fa-discord me-2"></i> Join Discord Community
              </a>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom py-4 border-top border-burnt-light">
          <div className="row align-items-center">
            <div className="col-md-6 text-center text-md-start">
              <p className="mb-0 footer-text">© {currentYear} Trial Junkies. All rights reserved.</p>
            </div>
            <div className="col-md-6 text-center text-md-end">
              <p className="mb-0 footer-text fs-sm">This is a satirical project. Always respect terms of service of platforms you use.</p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

// Make components globally available
window.AgentSection = AgentSection;
window.DiscordSection = DiscordSection;
window.ReferralSection = ReferralSection;
window.RoadmapSection = RoadmapSection;

// Render the App component to the DOM
const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);
root.render(<App />);