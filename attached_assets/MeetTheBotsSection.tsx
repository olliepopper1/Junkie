import React from 'react';
import BotCard from '@/components/ui/BotCard';
import greenSkeletonImg from '@/assets/skeleton-green.png';
import purpleSkeletonImg from '@/assets/skeleton-purple.png';
import fireSkullImg from '@/assets/fire-skull.png';

const MeetTheBotsSection: React.FC = () => {
  const bots = [
    {
      name: "HEROIN HARRY",
      subtitle: "Microdose",
      image: greenSkeletonImg,
      description: "Harry handles one-shot free trial creation using burner emails, SMS verification, and fake debit cards. He's sarcastic and teasing, acting like he's doing you a shady favor.",
      command: "!hit [service]",
      commandDescription: "Triggers one full account generation",
      features: [
        { icon: "fa-bolt", text: "Fast & Efficient" },
        { icon: "fa-shield-alt", text: "Basic Protection" }
      ],
      animation: "smoke-float",
      botType: "heroin-harry" as "heroin-harry"
    },
    {
      name: "MOLLY MORPHINE",
      subtitle: "Binge",
      image: purpleSkeletonImg,
      description: "Molly runs 3 trial signups at a time for the same service. Her personality is cool and smooth-talking, always delivering like a reliable plug.",
      command: "!binge [service]",
      commandDescription: "Runs 3 trial signups for the specified service",
      features: [
        { icon: "fa-users", text: "Multi-Account" },
        { icon: "fa-database", text: "Credential Storage" }
      ],
      animation: "pulse-glow",
      botType: "molly-morphine" as "molly-morphine"
    },
    {
      name: "KETA KEV",
      subtitle: "Overdose",
      image: fireSkullImg,
      description: "Kev generates free trials on an infinite loop with login token capture. He's spaced out but insanely reliable, with psychedelic coder vibes.",
      command: "!overdose [service]",
      commandDescription: "Generates trials on an infinite loop",
      features: [
        { icon: "fa-infinity", text: "Infinite Loop" },
        { icon: "fa-robot", text: "Advanced AI" }
      ],
      animation: "flame-dance",
      botType: "keta-kev" as "keta-kev"
    }
  ];

  return (
    <section id="meet-the-bots" className="py-20 bg-black relative">
      <div className="absolute inset-0 bg-gradient-radial from-[#1A0933] to-transparent opacity-20"></div>
      
      <div className="container mx-auto px-4 relative z-10">
        <h2 className="font-bebas text-4xl md:text-5xl text-orange text-center mb-16 relative">
          <span className="inline-block relative">
            MEET THE BOTS
            <div className="absolute -bottom-2 left-0 w-full h-1 bg-orange opacity-50"></div>
          </span>
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {bots.map((bot, index) => (
            <BotCard key={index} bot={bot} />
          ))}
        </div>
        
        {/* Overdose Mode */}
        <div className="mt-16 bg-gradient-to-r from-dark-purple to-black p-8 rounded-lg border border-orange border-opacity-40 relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-32 h-32 bg-orange opacity-10 rounded-full blur-3xl group-hover:w-40 group-hover:h-40 transition-all duration-700"></div>
          <div className="absolute bottom-0 left-0 w-32 h-32 bg-orange opacity-5 rounded-full blur-3xl group-hover:w-36 group-hover:h-36 transition-all duration-700"></div>
          
          <h3 className="font-bebas text-3xl text-orange mb-4 relative">
            OVERDOSE MODE ACTIVATED
            <span className="absolute -top-1 -right-2 text-sm animate-pulse text-yellow-400">PREMIUM</span>
          </h3>
          
          <p className="mb-6 max-w-3xl">Get all trials, no limits. Includes full automation, premium support, and first dibs on new services. Ride the wave—risk-free.</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-black bg-opacity-50 p-4 rounded-md border border-orange border-opacity-20">
              <h4 className="font-bold text-orange mb-2">Commands:</h4>
              <div className="bg-black bg-opacity-70 p-3 rounded-md font-mono text-sm border border-orange border-opacity-10">
                <code className="text-orange">!overdose_mode [service] [fullsend:true/false]</code> - Runs all agents together
              </div>
            </div>
            <div className="bg-black bg-opacity-50 p-4 rounded-md border border-orange border-opacity-20">
              <h4 className="font-bold text-orange mb-2">Features:</h4>
              <ul className="space-y-2">
                <li className="flex items-start">
                  <i className="fas fa-check text-orange mt-1 mr-2 animate-pulse"></i>
                  <span>Maximum parallelization</span>
                </li>
                <li className="flex items-start">
                  <i className="fas fa-check text-orange mt-1 mr-2 animate-pulse"></i>
                  <span>Auto-retry on failures</span>
                </li>
                <li className="flex items-start">
                  <i className="fas fa-check text-orange mt-1 mr-2 animate-pulse"></i>
                  <span>Advanced stealth measures</span>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="mt-6 flex flex-col sm:flex-row items-center justify-center sm:justify-start space-y-4 sm:space-y-0 sm:space-x-4">
            <a 
              href="#wallet-section" 
              className="px-8 py-3 bg-orange text-black font-bold rounded-md hover:bg-blood-red hover:text-white transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg w-full sm:w-auto text-center animate-fiery-pulse"
            >
              <i className="fas fa-syringe mr-2"></i> Activate Overdose Mode
            </a>
            <div className="text-sm bg-black bg-opacity-70 p-2 rounded-md border border-yellow-400 border-opacity-30">
              <span className="text-yellow-400"><i className="fas fa-exclamation-triangle mr-1"></i> Premium subscription required</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default MeetTheBotsSection;
