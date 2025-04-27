import React, { useEffect, useRef, useState } from 'react';
import greenSkeletonImg from '@assets/skeleton-green.png';
import purpleSkeletonImg from '@assets/skeleton-purple.png';
import redSkullLogo from '@assets/red-skull-logo.png';

interface ComicPanel {
  botType: 'heroin-harry' | 'molly-morphine' | 'keta-kev';
  dialogue: string;
  caption: string;
  background?: string;
}

interface ComicStrip {
  title: string;
  titleColor: string;
  panels: ComicPanel[];
}

const ComicsSection: React.FC = () => {
  const comicsContainerRef = useRef<HTMLDivElement>(null);
  const [activeComic, setActiveComic] = useState(0);
  const [activePanel, setActivePanel] = useState<Record<number, number>>({0: 0, 1: 0, 2: 0});
  
  // Helper function to get the image for each bot type
  const getBotImage = (botType: 'heroin-harry' | 'molly-morphine' | 'keta-kev') => {
    switch(botType) {
      case 'heroin-harry':
        return greenSkeletonImg;
      case 'molly-morphine':
        return purpleSkeletonImg;
      case 'keta-kev':
        return redSkullLogo;
      default:
        return greenSkeletonImg;
    }
  };
  
  // Helper function to get animation class for each bot type
  const getBotAnimationClass = (botType: 'heroin-harry' | 'molly-morphine' | 'keta-kev') => {
    switch(botType) {
      case 'heroin-harry':
        return 'heroin-harry-animation';
      case 'molly-morphine':
        return 'molly-morphine-animation';
      case 'keta-kev':
        return 'keta-kev-animation';
      default:
        return 'animate-float';
    }
  };

  const comicStrips: ComicStrip[] = [
    {
      title: "THE ADDICTION BEGINS",
      titleColor: 'text-green-skeleton',
      panels: [
        {
          botType: 'heroin-harry',
          dialogue: "Why pay for subscriptions when you can get them for free?",
          caption: "Heroin Harry discovers the power of free trials",
          background: 'bg-gradient-to-br from-green-900/20 to-black'
        },
        {
          botType: 'heroin-harry',
          dialogue: "Just one more free trial... I can stop anytime I want!",
          caption: "The addiction begins",
          background: 'bg-gradient-to-br from-green-900/20 to-black/30'
        },
        {
          botType: 'molly-morphine',
          dialogue: "You're saving HOW MUCH per month?!",
          caption: "Friends notice the savings",
          background: 'bg-gradient-to-br from-purple-900/20 to-black/30'
        },
        {
          botType: 'heroin-harry',
          dialogue: "I need more... MORE FREE TRIALS!",
          caption: "Harry becomes obsessed with savings",
          background: 'bg-gradient-to-br from-green-900/30 to-black'
        }
      ]
    },
    {
      title: "THE INTERVENTION",
      titleColor: 'text-purple-skeleton',
      panels: [
        {
          botType: 'molly-morphine',
          dialogue: "Harry, we need to talk about your free trial habit...",
          caption: "The team confronts Harry",
          background: 'bg-gradient-to-br from-purple-900/20 to-black/30'
        },
        {
          botType: 'heroin-harry',
          dialogue: "I can stop whenever I want! I just saved $1,620 last year!",
          caption: "Harry defends his addiction",
          background: 'bg-gradient-to-br from-green-900/20 to-black/30'
        },
        {
          botType: 'keta-kev',
          dialogue: "But you're spending all your time managing trials!",
          caption: "The team points out the problem",
          background: 'bg-gradient-to-br from-orange/10 to-black/30'
        },
        {
          botType: 'molly-morphine',
          dialogue: "What if we automated the whole process?",
          caption: "A solution emerges",
          background: 'bg-gradient-to-br from-purple-900/20 to-black/30'
        }
      ]
    },
    {
      title: "THE OVERDOSE MODE",
      titleColor: 'text-orange',
      panels: [
        {
          botType: 'heroin-harry',
          dialogue: "NO! My Netflix trial expired! I need my fix!",
          caption: "Harry experiences withdrawal",
          background: 'bg-gradient-to-br from-green-900/20 to-black/30'
        },
        {
          botType: 'molly-morphine',
          dialogue: "Calm down! We can generate a new one in seconds.",
          caption: "Molly Morphine offers help",
          background: 'bg-gradient-to-br from-purple-900/20 to-black/30'
        },
        {
          botType: 'keta-kev',
          dialogue: "Just one click and you'll have a fresh account.",
          caption: "Keta Kev demonstrates the solution",
          background: 'bg-gradient-to-br from-orange/10 to-black/30'
        },
        {
          botType: 'heroin-harry',
          dialogue: "Ahhh... that's the good stuff. Free trials forever!",
          caption: "Harry gets his fix",
          background: 'bg-gradient-to-br from-green-900/20 to-black/30'
        }
      ]
    }
  ];

  const scrollComics = (direction: 'left' | 'right') => {
    if (comicsContainerRef.current) {
      comicsContainerRef.current.scrollBy({
        left: direction === 'left' ? -400 : 400,
        behavior: 'smooth'
      });
    }
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!comicsContainerRef.current) return;

      // Check if comics section is in viewport
      const rect = comicsContainerRef.current.getBoundingClientRect();
      const isVisible = (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
      );

      if (!isVisible) return;

      if (e.key === 'ArrowLeft') {
        scrollComics('left');
      } else if (e.key === 'ArrowRight') {
        scrollComics('right');
      }
    };

    // Add touch swipe support for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    const handleTouchStart = (e: TouchEvent) => {
      touchStartX = e.changedTouches[0].screenX;
    };

    const handleTouchEnd = (e: TouchEvent) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    };

    const handleSwipe = () => {
      if (!comicsContainerRef.current) return;

      const swipeThreshold = 50;
      if (touchEndX < touchStartX - swipeThreshold) {
        // Swipe left
        scrollComics('right');
      }
      if (touchEndX > touchStartX + swipeThreshold) {
        // Swipe right
        scrollComics('left');
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    
    const comicsContainer = comicsContainerRef.current;
    if (comicsContainer) {
      comicsContainer.addEventListener('touchstart', handleTouchStart, { passive: true });
      comicsContainer.addEventListener('touchend', handleTouchEnd, { passive: true });
    }

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      if (comicsContainer) {
        comicsContainer.removeEventListener('touchstart', handleTouchStart);
        comicsContainer.removeEventListener('touchend', handleTouchEnd);
      }
    };
  }, []);

  // Handle advancing to next panel within the current comic
  const handlePanelClick = (comicIndex: number, panelIndex: number) => {
    const maxPanels = comicStrips[comicIndex].panels.length;
    
    if (panelIndex + 1 >= maxPanels) {
      // If last panel, move to next comic on click
      if (comicIndex < comicStrips.length - 1) {
        setActiveComic(comicIndex + 1);
        setActivePanel({...activePanel, [comicIndex + 1]: 0});
        
        // Scroll to next comic
        scrollComics('right');
      }
    } else {
      // Move to next panel
      setActivePanel({...activePanel, [comicIndex]: panelIndex + 1});
    }
  };

  return (
    <section id="comics" className="comics-section bg-gradient-to-b from-black to-dark-gray py-20 relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('@assets/red-skull-logo.png')] bg-repeat opacity-5"></div>
      
      <div className="container mx-auto px-4">
        <h2 className="font-bebas text-4xl md:text-5xl text-orange text-center mb-12 relative">
          <span className="inline-block relative">
            THE ADDICTION CHRONICLES
            <div className="absolute -bottom-2 left-0 w-full h-1 bg-orange opacity-50"></div>
          </span>
        </h2>
        
        {/* Mobile swipe instructions */}
        <div className="md:hidden text-center mb-4 text-sm text-gray-400">
          <p><i className="fas fa-hand-point-right text-orange mr-1"></i> Swipe to navigate comics</p>
        </div>
        
        {/* Desktop click instructions */}
        <div className="hidden md:block text-center mb-4 text-sm text-gray-400">
          <p><i className="fas fa-mouse-pointer text-orange mr-1"></i> Click panels to advance | Use arrow buttons to switch comics</p>
        </div>
        
        <div 
          ref={comicsContainerRef} 
          className="comics-container relative overflow-x-auto pb-6 -mx-4 px-4 mb-8 snap-x snap-mandatory"
        >
          <div className="inline-flex space-x-8 md:space-x-12">
            {comicStrips.map((comic, comicIndex) => (
              <div 
                key={comicIndex}
                className={`comic-strip snap-center ${activeComic === comicIndex ? 'scale-100 opacity-100' : 'scale-95 opacity-80'} 
                           transition-all duration-300 border-2 border-transparent hover:border-orange/30 rounded-xl overflow-hidden
                           min-w-[280px] sm:min-w-[400px] md:min-w-[520px]`}
              >
                <h3 className={`comic-title font-bebas text-2xl ${comic.titleColor} text-center py-3 bg-black/60`}>
                  {comic.title}
                </h3>
                
                <div className="comic-panels grid grid-cols-1 md:grid-cols-2 gap-2 p-2 bg-black/40">
                  {comic.panels.map((panel, panelIndex) => {
                    const isActive = activePanel[comicIndex] === panelIndex;
                    const isPast = activePanel[comicIndex] > panelIndex;
                    
                    return (
                      <div 
                        key={panelIndex} 
                        className={`comic-panel cursor-pointer ${panel.background || 'bg-black/30'} 
                                   rounded-lg overflow-hidden transition-all duration-300 transform
                                   ${isActive ? 'ring-2 ring-orange scale-105 z-10' : 'ring-0 scale-100'} 
                                   ${isPast ? 'opacity-60' : 'opacity-100'}`}
                        onClick={() => handlePanelClick(comicIndex, panelIndex)}
                      >
                        <div className="panel-image-container relative p-4 flex justify-center items-center">
                          <img 
                            src={getBotImage(panel.botType)} 
                            alt={`${panel.botType} character`} 
                            className={`w-24 h-24 object-contain ${getBotAnimationClass(panel.botType)}`} 
                          />
                          
                          <div className="speech-bubble absolute top-0 right-0 max-w-[80%] bg-white/10 backdrop-blur-sm rounded-lg p-3 transform -translate-y-1/3 translate-x-1/4">
                            <p className="text-xs md:text-sm">{panel.dialogue}</p>
                          </div>
                        </div>
                        
                        <div className="panel-content p-3 bg-black/50">
                          <p className="panel-caption text-xs text-center text-white/80">
                            {panel.caption}
                          </p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Comic Navigation */}
        <div className="comics-navigation flex justify-center space-x-4">
          <button 
            className="comics-scroll-btn prev px-6 py-2 bg-black/50 hover:bg-orange/80 text-white rounded-full border border-orange/30
                      transition-all duration-300 flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={() => {
              if (activeComic > 0) {
                setActiveComic(activeComic - 1);
                scrollComics('left');
              }
            }}
            disabled={activeComic === 0}
            aria-label="Previous comic"
          >
            <i className="fas fa-chevron-left mr-2"></i> Previous
          </button>
          <button 
            className="comics-scroll-btn next px-6 py-2 bg-black/50 hover:bg-orange/80 text-white rounded-full border border-orange/30
                      transition-all duration-300 flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={() => {
              if (activeComic < comicStrips.length - 1) {
                setActiveComic(activeComic + 1);
                scrollComics('right');
              }
            }}
            disabled={activeComic === comicStrips.length - 1}
            aria-label="Next comic"
          >
            Next <i className="fas fa-chevron-right ml-2"></i>
          </button>
        </div>
      </div>
    </section>
  );
};

export default ComicsSection;
