import React from 'react';

type BotType = 'heroin-harry' | 'molly-morphine' | 'keta-kev';

interface Feature {
  icon: string;
  text: string;
}

interface BotProps {
  bot: {
    name: string;
    subtitle: string;
    image: string;
    description: string;
    command: string;
    commandDescription: string;
    features: Feature[];
    animation: string;
    botType: BotType;
  };
}

const BotCard: React.FC<BotProps> = ({ bot }) => {
  // Set dynamic classes based on bot type
  const getBotSpecificClasses = () => {
    switch (bot.botType) {
      case 'heroin-harry':
        return {
          gradient: 'from-green-500 to-green-800',
          accent: 'border-green-500',
          glow: 'bg-green-500',
          buttonHover: 'hover:bg-green-700',
        };
      case 'molly-morphine':
        return {
          gradient: 'from-purple-500 to-purple-800',
          accent: 'border-purple-500',
          glow: 'bg-purple-500',
          buttonHover: 'hover:bg-purple-700',
        };
      case 'keta-kev':
        return {
          gradient: 'from-orange to-blood-red',
          accent: 'border-orange',
          glow: 'bg-orange',
          buttonHover: 'hover:bg-blood-red',
        };
      default:
        return {
          gradient: 'from-orange to-blood-red',
          accent: 'border-orange',
          glow: 'bg-orange',
          buttonHover: 'hover:bg-blood-red',
        };
    }
  };

  const botClasses = getBotSpecificClasses();

  return (
    <div className={`bg-black p-6 rounded-lg shadow-xl border border-opacity-40 ${botClasses.accent} relative overflow-hidden group`}>
      {/* Background glow effect */}
      <div className={`absolute top-0 right-0 w-40 h-40 ${botClasses.glow} opacity-10 rounded-full blur-3xl group-hover:opacity-20 transition-opacity duration-700`}></div>
      <div className={`absolute -bottom-20 -left-20 w-40 h-40 ${botClasses.glow} opacity-5 rounded-full blur-3xl group-hover:opacity-10 transition-opacity duration-700`}></div>
      
      {/* Image and title section */}
      <div className="flex flex-col items-center text-center mb-4">
        <div className="w-32 h-32 mb-4 relative">
          <img 
            src={bot.image} 
            alt={bot.name} 
            className={`w-full h-full object-contain ${bot.animation}`}
          />
        </div>
        <h3 className="font-bebas text-3xl text-orange mb-1">{bot.name}</h3>
        <div className="bg-black px-3 py-1 rounded-full border border-orange border-opacity-30 inline-block mb-3">
          <span className="text-sm opacity-70">{bot.subtitle}</span>
        </div>
      </div>
      
      {/* Description */}
      <p className="mb-6 text-sm opacity-80">{bot.description}</p>
      
      {/* Command section */}
      <div className="bg-black bg-opacity-70 p-4 rounded-md mb-4 border border-orange border-opacity-20">
        <h4 className="font-bold text-orange mb-2">Command:</h4>
        <div className="bg-black p-2 rounded border border-orange border-opacity-10">
          <code className="text-orange font-mono text-sm">{bot.command}</code>
        </div>
        <p className="mt-2 text-xs opacity-70">{bot.commandDescription}</p>
      </div>
      
      {/* Features */}
      <div className="mb-4">
        <h4 className="font-bold text-orange mb-2">Features:</h4>
        <ul className="space-y-2">
          {bot.features.map((feature, index) => (
            <li key={index} className="flex items-start">
              <i className={`fas ${feature.icon} text-orange mt-1 mr-2`}></i>
              <span className="text-sm">{feature.text}</span>
            </li>
          ))}
        </ul>
      </div>
      
      {/* Action button */}
      <div className="mt-4">
        <a 
          href="#wallet-section" 
          className={`w-full block text-center px-4 py-2 bg-orange text-black font-bold rounded-md hover:text-white transition-all duration-300 ${botClasses.buttonHover}`}
        >
          Deploy Agent
        </a>
      </div>
    </div>
  );
};

export default BotCard;