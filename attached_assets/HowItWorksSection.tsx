import React from 'react';

const HowItWorksSection: React.FC = () => {
  const steps = [
    {
      icon: "fa-robot",
      step: 1,
      title: "CHOOSE YOUR BOT",
      description: "Select from our lineup of specialized agents, each with unique capabilities for different trial needs.",
      items: [
        "Heroin Harry: One-time trial creation",
        "Molly Morphine: Multiple account creation",
        "Keta Kev: Infinite loop automation"
      ]
    },
    {
      icon: "fa-magic",
      step: 2,
      title: "RUN AUTOMATION",
      description: "Our bots handle the entire process from account creation to verification with no user interaction required.",
      items: [
        "Automated email & SMS verification",
        "Virtual payment methods that never charge",
        "Proxy rotation for maximum security"
      ]
    },
    {
      icon: "fa-rocket",
      step: 3,
      title: "ENJOY FREE ACCESS",
      description: "Receive login credentials for your freshly created accounts with active free trials ready to use.",
      items: [
        "Get access to premium services for free",
        "Automatic trial status tracking",
        "Save $1,620+ per year on subscriptions"
      ]
    }
  ];

  return (
    <section id="how-it-works" className="py-20 bg-[#121212]">
      <div className="container mx-auto px-4">
        <h2 className="font-bebas text-4xl md:text-5xl text-[#FF5500] text-center mb-16">HOW IT WORKS</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <div 
              key={index}
              className="bg-black bg-opacity-50 p-8 rounded-lg border border-[#FF5500] border-opacity-30 transition-all duration-300 hover:-translate-y-2 hover:shadow-xl hover:border-opacity-100 relative overflow-hidden group"
            >
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-[#FF5500] to-[#8A0303]"></div>
              <div className="relative">
                <div className="text-4xl text-[#FF5500] mb-6 relative inline-block">
                  <i className={`fas ${step.icon}`}></i>
                  <div className="absolute -top-2 -right-2 w-6 h-6 bg-[#8A0303] rounded-full flex items-center justify-center text-sm text-[#F0F0F0] font-bold">
                    {step.step}
                  </div>
                </div>
                <h3 className="font-bebas text-2xl mb-4">{step.title}</h3>
                <p className="text-[#F0F0F0] opacity-80">{step.description}</p>
                <ul className="mt-4 space-y-2">
                  {step.items.map((item, itemIndex) => (
                    <li key={itemIndex} className="flex items-start">
                      <i className="fas fa-check text-[#FF5500] mt-1 mr-2"></i>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;
