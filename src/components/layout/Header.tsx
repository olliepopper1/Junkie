import React, { useState, useEffect } from 'react';
import Link from 'next/link';

const Header: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header 
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled ? 'bg-black bg-opacity-90 shadow-lg py-3' : 'py-5'
      }`}
    >
      <div className="container mx-auto px-4 flex justify-between items-center">
        {/* Logo */}
        <Link href="/">
          <div className="flex items-center cursor-pointer">
            <img 
              src="/assets/fire-skull.png" 
              alt="Trial Junkies" 
              className="h-10 w-auto mr-3" 
            />
            <span className="font-bebas text-2xl text-orange">TRIAL JUNKIES</span>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-8">
          <Link 
            href="#how-it-works" 
            className="text-white hover:text-orange transition-colors duration-300"
          >
            How It Works
          </Link>
          <Link 
            href="#meet-the-bots" 
            className="text-white hover:text-orange transition-colors duration-300"
          >
            Meet The Bots
          </Link>
          <Link 
            href="#roadmap" 
            className="text-white hover:text-orange transition-colors duration-300"
          >
            Roadmap
          </Link>
          <Link 
            href="#wallet-section" 
            className="px-6 py-2 bg-orange text-black font-bold rounded-md hover:bg-blood-red hover:text-white transition-all duration-300"
          >
            Connect Wallet
          </Link>
        </nav>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden text-white focus:outline-none"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        >
          {isMobileMenuOpen ? (
            <i className="fas fa-times text-2xl"></i>
          ) : (
            <i className="fas fa-bars text-2xl"></i>
          )}
        </button>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-black bg-opacity-95 absolute w-full py-4 shadow-lg">
          <div className="container mx-auto px-4 flex flex-col space-y-4">
            <Link 
              href="#how-it-works" 
              className="text-white hover:text-orange transition-colors duration-300 py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              How It Works
            </Link>
            <Link 
              href="#meet-the-bots" 
              className="text-white hover:text-orange transition-colors duration-300 py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Meet The Bots
            </Link>
            <Link 
              href="#roadmap" 
              className="text-white hover:text-orange transition-colors duration-300 py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Roadmap
            </Link>
            <Link 
              href="#wallet-section" 
              className="px-6 py-2 bg-orange text-black font-bold rounded-md hover:bg-blood-red hover:text-white transition-all duration-300 inline-block"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Connect Wallet
            </Link>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;