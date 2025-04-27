import React, { useEffect, useRef } from 'react';
import fireSkullHero from '@/assets/fire-skull.png';

const HeroSection: React.FC = () => {
  const glitchTitleRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    // Set up glitch effect
    const titleElement = glitchTitleRef.current;
    if (titleElement) {
      titleElement.setAttribute('data-text', 'TRIAL JUNKIES');
    }
  }, []);

  return (
    <section id="hero" className="min-h-screen flex items-center relative pt-20">
      <div className="absolute inset-0 bg-gradient-radial from-[#1A0933] to-transparent opacity-20"></div>
      
      <div className="container mx-auto px-4 py-16 z-10 flex flex-col md:flex-row items-center justify-between">
        {/* Hero Content */}
        <div className="w-full md:w-1/2 text-center md:text-left mb-12 md:mb-0">
          <h1 
            ref={glitchTitleRef} 
            className="font-bebas text-6xl md:text-7xl lg:text-8xl text-[#FF5500] mb-4 glitch" 
            data-text="TRIAL JUNKIES"
          >
            TRIAL JUNKIES
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-[#F0F0F0] opacity-90">No Rehab, Just Free Trials.</p>
          <p className="text-lg md:text-xl mb-8 max-w-2xl">Get hooked on the ultimate subscription hack. Our AI-powered bots automate free trials across hundreds of services so you never pay again.</p>
          <div className="relative">
            <a 
              href="#how-it-works" 
              className="inline-block px-8 py-4 bg-[#FF5500] text-black font-bold text-lg rounded-md hover:bg-[#8A0303] hover:text-white transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg relative overflow-hidden group"
            >
              <span className="relative z-10">GET YOUR FIRST HIT</span>
              <span className="absolute inset-0 bg-[#FF5500] group-hover:scale-x-[1.4] group-hover:scale-y-[1.6] group-hover:opacity-0 transition-all duration-500"></span>
            </a>
            <img 
              src={fireSkullHero} 
              alt="Trial Junkies Fire Pill" 
              className="floating-pill-image -top-10 -right-16"
            />
          </div>
        </div>
        
        {/* Hero Image */}
        <div className="w-full md:w-1/2 flex justify-center">
          <img 
            src={fireSkullHero} 
            alt="Trial Junkies Fire Skull" 
            className="w-full max-w-md fire-skull-animation" 
          />
        </div>
      </div>
      
      <div className="absolute bottom-10 left-1/2 -translate-x-1/2 animate-bounce">
        <a 
          href="#how-it-works" 
          className="text-[#F0F0F0] opacity-70 hover:opacity-100 transition-opacity duration-300"
        >
          <i className="fas fa-chevron-down text-2xl"></i>
        </a>
      </div>
    </section>
  );
};

export default HeroSection;
