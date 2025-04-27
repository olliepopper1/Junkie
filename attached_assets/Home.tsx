import React from 'react';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';
import HeroSection from '@/components/sections/HeroSection';
import HowItWorksSection from '@/components/sections/HowItWorksSection';
import MeetTheBotsSection from '@/components/sections/MeetTheBotsSection';
import ComicsSection from '@/components/sections/ComicsSection';
import RoadmapSection from '@/components/sections/RoadmapSection';
import WalletSection from '@/components/sections/WalletSection';
import ReferralSection from '@/components/sections/ReferralSection';
import redSkullLogo from '@assets/red-skull-logo.png';
import greenSkeletonImg from '@assets/skeleton-green.png';
import purpleSkeletonImg from '@assets/skeleton-purple.png';

const Home: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-black text-off-white relative overflow-hidden">
      {/* Floating background stickers */}
      <img 
        src={redSkullLogo} 
        alt="Floating skull logo" 
        className="floating-sticker floating-sticker-1 top-[15%] left-[5%] w-32 opacity-10" 
      />
      <img 
        src={greenSkeletonImg} 
        alt="Green skeleton sticker" 
        className="floating-sticker floating-sticker-2 top-[35%] right-[8%] w-20 opacity-8" 
      />
      <img 
        src={purpleSkeletonImg} 
        alt="Purple skeleton sticker" 
        className="floating-sticker floating-sticker-3 bottom-[25%] left-[7%] w-24 opacity-8" 
      />
      <img 
        src={redSkullLogo} 
        alt="Floating skull logo" 
        className="floating-sticker floating-sticker-4 bottom-[10%] right-[10%] w-28 opacity-10 rotate-12" 
      />
      
      <Navbar />
      
      <main className="flex-1 relative z-10">
        <HeroSection />
        <HowItWorksSection />
        <MeetTheBotsSection />
        <ComicsSection />
        <RoadmapSection />
        <WalletSection />
        <ReferralSection />
      </main>
      
      <Footer />
    </div>
  );
};

export default Home;
