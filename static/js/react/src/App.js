// React App for Trial Junkies
const { useState, useEffect } = React;

// Main App Component
function App() {
  return (
    <div className="app-container">
      <Navbar />
      <Hero />
      <ServicesSection />
      <HowItWorksSection />
      <PricingSection />
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
    <nav className={`navbar navbar-expand-lg navbar-dark ${scrolled ? 'bg-dark' : 'bg-transparent'} fixed-top`}>
      <div className="container">
        <a className="navbar-brand" href="#">
          <i className="fas fa-syringe me-2"></i>
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
              <a className="nav-link" href="#how-it-works">How It Works</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#pricing">Pricing</a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#faq">FAQ</a>
            </li>
            <li className="nav-item">
              <a className="nav-link btn btn-outline-primary ms-lg-3" href="https://discord.gg/trialjunkie">Join Discord</a>
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
    <section className="hero-section bg-dark text-white py-5 mb-5">
      <div className="container py-5">
        <div className="row align-items-center">
          <div className="col-lg-6">
            <h1 className="display-3 fw-bold" style={{ fontFamily: 'Bebas Neue, sans-serif' }}>NO REHAB, JUST FREE TRIALS</h1>
            <p className="lead mb-4">Get your fix of premium content with our powerful trial generation system. Our Discord bot creates working trial accounts for all major streaming services.</p>
            <div className="d-flex gap-3">
              <a href="https://discord.gg/trialjunkie" className="btn btn-primary btn-lg">
                <i className="fab fa-discord me-2"></i> Join Discord
              </a>
              <a href="#how-it-works" className="btn btn-outline-light btn-lg">Learn More</a>
            </div>
          </div>
          <div className="col-lg-6 d-none d-lg-block">
            <img src="https://cdn.discordapp.com/attachments/1093661242069737552/1234567890/trial_junkie_hero.png" className="img-fluid rounded shadow-lg" alt="Trial Junkies Hero" />
          </div>
        </div>
      </div>
    </section>
  );
}

// Services Section
function ServicesSection() {
  const services = [
    { name: "Netflix", icon: "fa-play", color: "#E50914" },
    { name: "Hulu", icon: "fa-tv", color: "#1CE783" },
    { name: "Disney+", icon: "fa-star", color: "#0063E5" },
    { name: "Amazon Prime", icon: "fa-box", color: "#FF9900" },
    { name: "Spotify", icon: "fa-music", color: "#1DB954" },
    { name: "YouTube Premium", icon: "fa-youtube", color: "#FF0000" },
    { name: "HBO Max", icon: "fa-film", color: "#5E22AB" },
    { name: "Paramount+", icon: "fa-mountain", color: "#0064FF" }
  ];

  return (
    <section id="services" className="py-5">
      <div className="container">
        <div className="text-center mb-5">
          <h2 className="display-5 fw-bold">Premium Services We Support</h2>
          <p className="lead">Get your dose of these streaming platforms with our trial generation system</p>
        </div>
        
        <div className="row row-cols-2 row-cols-md-4 g-4">
          {services.map((service, index) => (
            <div className="col" key={index}>
              <div className="card h-100 text-center border-0 shadow-sm">
                <div className="card-body">
                  <div className="icon-wrapper mb-3" style={{ backgroundColor: service.color, width: "64px", height: "64px", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto" }}>
                    <i className={`fas ${service.icon} fa-2x text-white`}></i>
                  </div>
                  <h5 className="card-title">{service.name}</h5>
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
      description: "Connect with our Discord bot to access the Trial Junkie network.",
      icon: "fa-discord"
    },
    {
      title: "Choose Your Dose",
      description: "Select from a variety of streaming services to get your fix.",
      icon: "fa-syringe"
    },
    {
      title: "Get Your Trial",
      description: "Our specialized agents generate working trial credentials for you.",
      icon: "fa-key"
    },
    {
      title: "Enjoy Premium Content",
      description: "Log in and stream without limitations during your trial period.",
      icon: "fa-tv"
    }
  ];

  return (
    <section id="how-it-works" className="py-5 bg-light text-dark">
      <div className="container">
        <div className="text-center mb-5">
          <h2 className="display-5 fw-bold">How It Works</h2>
          <p className="lead">Getting your trial fix is quick and easy</p>
        </div>
        
        <div className="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4">
          {steps.map((step, index) => (
            <div className="col" key={index}>
              <div className="card h-100 border-0 shadow-sm">
                <div className="card-body text-center">
                  <div className="step-number mb-3">
                    <span className="badge rounded-pill bg-primary fs-4 px-3 py-2">{index + 1}</span>
                  </div>
                  <div className="icon-wrapper mb-3">
                    <i className={`fab ${step.icon.includes('discord') ? step.icon : `fas ${step.icon}`} fa-3x text-primary`}></i>
                  </div>
                  <h4 className="card-title">{step.title}</h4>
                  <p className="card-text">{step.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="text-center mt-5">
          <h3 className="fs-4 mb-4">Discord Commands</h3>
          <div className="card bg-dark text-light p-3 shadow-lg mx-auto" style={{ maxWidth: "600px" }}>
            <pre className="mb-0">
              <code>
                !hit netflix        # Generate full trial<br/>
                !dose harry netflix # Identity only<br/>
                !dose mandy netflix # Payment card only<br/>
                !stash              # View your trials<br/>
                !trip netflix       # Automated signup
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
      name: "Free Tier",
      price: "$0",
      period: "/mo",
      features: [
        "1 hit per day",
        "3 doses per day",
        "No automation",
        "Basic support"
      ],
      buttonText: "Start for free",
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
      buttonText: "Get started",
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
      buttonText: "Go premium",
      featured: false
    }
  ];

  return (
    <section id="pricing" className="py-5">
      <div className="container">
        <div className="text-center mb-5">
          <h2 className="display-5 fw-bold">Choose Your Fix</h2>
          <p className="lead">Select the plan that suits your streaming addiction</p>
        </div>
        
        <div className="row row-cols-1 row-cols-md-3 g-4 justify-content-center">
          {plans.map((plan, index) => (
            <div className="col" key={index}>
              <div className={`card h-100 ${plan.featured ? 'border-primary' : ''}`}>
                {plan.featured && <div className="card-header bg-primary text-white py-3"><strong>Most Popular</strong></div>}
                <div className="card-body">
                  <h3 className="card-title">{plan.name}</h3>
                  <div className="pricing mb-3">
                    <span className="display-5 fw-bold">{plan.price}</span>
                    <span className="text-muted">{plan.period}</span>
                  </div>
                  <ul className="list-unstyled">
                    {plan.features.map((feature, i) => (
                      <li className="mb-2" key={i}>
                        <i className="fas fa-check text-success me-2"></i>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="card-footer bg-transparent border-0 pb-4">
                  <a href="https://discord.gg/trialjunkie" className={`btn ${plan.featured ? 'btn-primary' : 'btn-outline-primary'} d-block`}>
                    {plan.buttonText}
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="payment-info text-center mt-5">
          <p className="text-muted">We accept cryptocurrency payments (Solana) for ultimate privacy</p>
          <div className="crypto-icons mt-2">
            <i className="fab fa-bitcoin me-3 fs-3"></i>
            <i className="fab fa-ethereum me-3 fs-3"></i>
            <i className="fas fa-coins fs-3"></i>
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
      avatar: "https://randomuser.me/api/portraits/men/41.jpg",
      text: "Trial Junkie is a game-changer. I've been using it for months and it's saved me hundreds on subscription fees.",
      platform: "Discord"
    },
    {
      name: "Sarah L.",
      avatar: "https://randomuser.me/api/portraits/women/63.jpg",
      text: "The agents are so reliable! I've never had an issue with any of the trials they've generated for me.",
      platform: "Twitter"
    },
    {
      name: "David K.",
      avatar: "https://randomuser.me/api/portraits/men/22.jpg",
      text: "The automated signup feature is worth every penny. Saves me so much time and hassle.",
      platform: "Discord"
    }
  ];

  return (
    <section className="py-5 bg-light text-dark">
      <div className="container">
        <div className="text-center mb-5">
          <h2 className="display-5 fw-bold">Happy Junkies</h2>
          <p className="lead">See what our community has to say</p>
        </div>
        
        <div className="row row-cols-1 row-cols-md-3 g-4">
          {testimonials.map((testimonial, index) => (
            <div className="col" key={index}>
              <div className="card h-100 border-0 shadow-sm">
                <div className="card-body">
                  <div className="d-flex align-items-center mb-3">
                    <img src={testimonial.avatar} className="rounded-circle me-3" width="50" height="50" alt={testimonial.name} />
                    <div>
                      <h5 className="card-title mb-0">{testimonial.name}</h5>
                      <small className="text-muted">via {testimonial.platform}</small>
                    </div>
                  </div>
                  <p className="card-text fst-italic">"{testimonial.text}"</p>
                </div>
                <div className="card-footer bg-transparent border-0">
                  <div className="text-warning">
                    <i className="fas fa-star"></i>
                    <i className="fas fa-star"></i>
                    <i className="fas fa-star"></i>
                    <i className="fas fa-star"></i>
                    <i className="fas fa-star"></i>
                  </div>
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
      answer: "Trial Junkie uses specialized agents to generate working trial accounts for various streaming services. Our system creates accounts with valid payment information that pass verification checks."
    },
    {
      question: "Is this legal?",
      answer: "Trial Junkie operates in a gray area. We're simply automating the trial sign-up process that's available to everyone. Users are responsible for complying with the terms of service of each platform they use."
    },
    {
      question: "What happens after the trial period ends?",
      answer: "Trials will automatically expire after the free period. The payment method used is designed to pass initial verification but will not be charged after the trial period."
    },
    {
      question: "What services do you support?",
      answer: "We support most major streaming platforms including Netflix, Hulu, Disney+, Amazon Prime, HBO Max, Spotify, YouTube Premium, and many more."
    },
    {
      question: "How do I get started?",
      answer: "Simply join our Discord server and follow the instructions to start generating trials. Use the !help command to see all available commands."
    },
    {
      question: "What payment methods do you accept?",
      answer: "We accept cryptocurrency payments (primarily Solana) for maximum privacy and security. Payment instructions are provided when you upgrade your plan."
    }
  ];

  const [activeIndex, setActiveIndex] = useState(null);

  const toggleFAQ = (index) => {
    setActiveIndex(activeIndex === index ? null : index);
  };

  return (
    <section id="faq" className="py-5">
      <div className="container">
        <div className="text-center mb-5">
          <h2 className="display-5 fw-bold">Frequently Asked Questions</h2>
          <p className="lead">Everything you need to know about Trial Junkie</p>
        </div>
        
        <div className="row justify-content-center">
          <div className="col-lg-8">
            <div className="accordion" id="faqAccordion">
              {faqs.map((faq, index) => (
                <div className="accordion-item" key={index}>
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
  return (
    <footer className="bg-dark text-white py-5">
      <div className="container">
        <div className="row">
          <div className="col-lg-4 mb-4 mb-lg-0">
            <h5 className="mb-3">
              <i className="fas fa-syringe me-2"></i>
              Trial Junkie
            </h5>
            <p className="mb-3">Your one-stop solution for premium trial accounts. Get your fix without the subscription commitment.</p>
            <div className="social-icons">
              <a href="https://discord.gg/trialjunkie" className="text-white me-3"><i className="fab fa-discord fs-4"></i></a>
              <a href="#" className="text-white me-3"><i className="fab fa-twitter fs-4"></i></a>
              <a href="#" className="text-white me-3"><i className="fab fa-reddit fs-4"></i></a>
              <a href="#" className="text-white"><i className="fab fa-telegram fs-4"></i></a>
            </div>
          </div>
          
          <div className="col-lg-2 col-md-4 mb-4 mb-md-0">
            <h5 className="mb-3">Links</h5>
            <ul className="list-unstyled">
              <li className="mb-2"><a href="#services" className="text-white text-decoration-none">Services</a></li>
              <li className="mb-2"><a href="#how-it-works" className="text-white text-decoration-none">How It Works</a></li>
              <li className="mb-2"><a href="#pricing" className="text-white text-decoration-none">Pricing</a></li>
              <li className="mb-2"><a href="#faq" className="text-white text-decoration-none">FAQ</a></li>
            </ul>
          </div>
          
          <div className="col-lg-2 col-md-4 mb-4 mb-md-0">
            <h5 className="mb-3">Resources</h5>
            <ul className="list-unstyled">
              <li className="mb-2"><a href="#" className="text-white text-decoration-none">Commands</a></li>
              <li className="mb-2"><a href="#" className="text-white text-decoration-none">Tutorials</a></li>
              <li className="mb-2"><a href="#" className="text-white text-decoration-none">Support</a></li>
              <li className="mb-2"><a href="#" className="text-white text-decoration-none">Blog</a></li>
            </ul>
          </div>
          
          <div className="col-lg-4 col-md-4">
            <h5 className="mb-3">Join Our Discord</h5>
            <p className="mb-3">Get instant access to trial generation and connect with our community.</p>
            <a href="https://discord.gg/trialjunkie" className="btn btn-primary">
              <i className="fab fa-discord me-2"></i> Join Discord
            </a>
          </div>
        </div>
        
        <hr className="my-4" />
        
        <div className="row align-items-center">
          <div className="col-md-6 text-center text-md-start">
            <p className="mb-0">© 2025 Trial Junkie. All rights reserved.</p>
          </div>
          <div className="col-md-6 text-center text-md-end">
            <small className="text-muted">
              <a href="#" className="text-white text-decoration-none">Terms of Service</a> | 
              <a href="#" className="text-white text-decoration-none ms-2">Privacy Policy</a>
            </small>
          </div>
        </div>
      </div>
    </footer>
  );
}

// Render the App component to the DOM
const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);
root.render(<App />);