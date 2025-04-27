import React from 'react';
import Link from 'next/link';

const Footer: React.FC = () => {
  return (
    <footer className="bg-black bg-opacity-70 border-t border-orange border-opacity-20 py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Logo and Description */}
          <div className="md:col-span-1">
            <div className="flex items-center mb-4">
              <img src="/assets/fire-skull.png" alt="Trial Junkies" className="h-10 w-auto mr-3" />
              <span className="font-bebas text-2xl text-orange">TRIAL JUNKIES</span>
            </div>
            <p className="text-sm text-gray-400 mb-4">
              The revolutionary platform for free trials powered by next-gen agent technology.
            </p>
            <div className="flex space-x-4">
              <a href="https://discord.gg/f5Dqz69ZNt" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-orange transition-colors">
                <i className="fab fa-discord text-xl"></i>
              </a>
              <a href="https://twitter.com/trialjunkies" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-orange transition-colors">
                <i className="fab fa-twitter text-xl"></i>
              </a>
              <a href="https://github.com/trialjunkies" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-orange transition-colors">
                <i className="fab fa-github text-xl"></i>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div className="md:col-span-1">
            <h3 className="font-bebas text-xl text-orange mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="#how-it-works" className="text-gray-400 hover:text-orange transition-colors">
                  How It Works
                </Link>
              </li>
              <li>
                <Link href="#meet-the-bots" className="text-gray-400 hover:text-orange transition-colors">
                  Meet The Bots
                </Link>
              </li>
              <li>
                <Link href="#roadmap" className="text-gray-400 hover:text-orange transition-colors">
                  Roadmap
                </Link>
              </li>
              <li>
                <Link href="#referral" className="text-gray-400 hover:text-orange transition-colors">
                  Referral Program
                </Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div className="md:col-span-1">
            <h3 className="font-bebas text-xl text-orange mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <a href="/docs" className="text-gray-400 hover:text-orange transition-colors">
                  Documentation
                </a>
              </li>
              <li>
                <a href="/api" className="text-gray-400 hover:text-orange transition-colors">
                  API
                </a>
              </li>
              <li>
                <a href="/guides" className="text-gray-400 hover:text-orange transition-colors">
                  Guides
                </a>
              </li>
              <li>
                <a href="/faq" className="text-gray-400 hover:text-orange transition-colors">
                  FAQ
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div className="md:col-span-1">
            <h3 className="font-bebas text-xl text-orange mb-4">Legal</h3>
            <ul className="space-y-2">
              <li>
                <a href="/terms" className="text-gray-400 hover:text-orange transition-colors">
                  Terms of Service
                </a>
              </li>
              <li>
                <a href="/privacy" className="text-gray-400 hover:text-orange transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="/cookies" className="text-gray-400 hover:text-orange transition-colors">
                  Cookie Policy
                </a>
              </li>
              <li>
                <a href="/disclaimer" className="text-gray-400 hover:text-orange transition-colors">
                  Disclaimer
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="mt-12 pt-8 border-t border-orange border-opacity-10 text-center text-sm text-gray-500">
          <p>©2025 Trial Junkies. All rights reserved.</p>
          <p className="mt-2">We are not responsible for the services you gain access to with our bots.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;