import React, { useState } from 'react';
import fireSkullImg from '@/assets/fire-skull.png';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();
  const [logoHovered, setLogoHovered] = useState(false);

  return (
    <footer className="bg-[#121212] pt-16 pb-8 border-t border-[#FF5500] border-opacity-30">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          {/* Logo & Info */}
          <div className="md:col-span-1">
            <a 
              href="#" 
              className="footer-logo mb-4 inline-flex"
              onMouseEnter={() => setLogoHovered(true)}
              onMouseLeave={() => setLogoHovered(false)}
            >
              <div className="relative">
                <img 
                  src={fireSkullImg} 
                  alt="Trial Junkies Logo" 
                  className={`footer-logo-img fire-skull-mini ${logoHovered ? 'animate-fiery-pulse' : 'animate-flame-flicker'}`} 
                />
                <div className={`logo-flame-effect ${logoHovered ? 'opacity-100' : ''}`}></div>
              </div>
              <span className="font-bebas text-xl text-orange">TRIAL JUNKIES</span>
            </a>
            <p className="max-w-xs opacity-70 mb-4">No Rehab, Just Free Trials. Automate your way to subscription freedom.</p>
            <div className="flex space-x-4">
              <a href="#" className="text-[#FF5500] hover:text-white transition-colors duration-300">
                <i className="fab fa-twitter"></i>
              </a>
              <a href="#" className="text-[#FF5500] hover:text-white transition-colors duration-300">
                <i className="fab fa-discord"></i>
              </a>
              <a href="#" className="text-[#FF5500] hover:text-white transition-colors duration-300">
                <i className="fab fa-telegram-plane"></i>
              </a>
              <a href="#" className="text-[#FF5500] hover:text-white transition-colors duration-300">
                <i className="fab fa-github"></i>
              </a>
            </div>
          </div>
          
          {/* Quick Links */}
          <div className="md:col-span-1">
            <h3 className="font-bebas text-xl text-orange mb-4">QUICK LINKS</h3>
            <ul className="space-y-2">
              <li><a href="#how-it-works" className="hover:text-orange transition-colors duration-300">How It Works</a></li>
              <li><a href="#meet-the-bots" className="hover:text-orange transition-colors duration-300">Meet The Bots</a></li>
              <li><a href="#roadmap" className="hover:text-orange transition-colors duration-300">Roadmap</a></li>
              <li><a href="#referral" className="hover:text-orange transition-colors duration-300">Referral Program</a></li>
              <li><a href="#wallet-section" className="hover:text-orange transition-colors duration-300">Connect Wallet</a></li>
            </ul>
          </div>
          
          {/* Resources */}
          <div className="md:col-span-1">
            <h3 className="font-bebas text-xl text-orange mb-4">RESOURCES</h3>
            <ul className="space-y-2">
              <li><a href="#" className="hover:text-orange transition-colors duration-300">Documentation</a></li>
              <li><a href="#" className="hover:text-orange transition-colors duration-300">FAQs</a></li>
              <li><a href="#" className="hover:text-orange transition-colors duration-300">Support</a></li>
              <li><a href="#" className="hover:text-orange transition-colors duration-300">Terms of Service</a></li>
              <li><a href="#" className="hover:text-orange transition-colors duration-300">Privacy Policy</a></li>
            </ul>
          </div>
          
          {/* Newsletter */}
          <div className="md:col-span-1">
            <h3 className="font-bebas text-xl text-orange mb-4">GET UPDATES</h3>
            <p className="opacity-70 mb-4">Stay informed about new features and updates.</p>
            <form className="flex" onSubmit={(e) => e.preventDefault()}>
              <input 
                type="email" 
                placeholder="Your email address" 
                className="flex-grow bg-black border border-orange rounded-l-md p-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange" 
              />
              <button 
                type="submit"
                className="px-4 py-2 bg-orange text-black font-bold rounded-r-md hover:bg-blood-red hover:text-white transition-all duration-300"
              >
                <i className="fas fa-arrow-right"></i>
              </button>
            </form>
          </div>
        </div>
        
        <div className="pt-8 mt-8 border-t border-[#FF5500] border-opacity-20 flex flex-col md:flex-row justify-between items-center">
          <p className="opacity-70 text-sm mb-4 md:mb-0">© {currentYear} Trial Junkies. All Rights Reserved.</p>
          <p className="opacity-70 text-sm text-center md:text-right">This is a satirical project. Always respect terms of service of platforms you use.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
