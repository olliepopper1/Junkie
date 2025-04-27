// Comics Section Component for Trial Junkies

const ComicsSection = () => {
  const [activeComic, setActiveComic] = React.useState(0);
  const [activePanel, setActivePanel] = React.useState({0: 0, 1: 0, 2: 0});
  const comicsContainerRef = React.useRef(null);
  
  // Helper function to get the image for each bot type
  const getBotImage = (botType) => {
    switch(botType) {
      case 'heroin-harry':
        return '/static/images/skeleton-green.png';
      case 'molly-morphine':
        return '/static/images/skeleton-purple.png';
      case 'keta-kev':
        return '/static/images/fire-skull.png';
      default:
        return '/static/images/skeleton-green.png';
    }
  };
  
  // Helper function to get animation class for each bot type
  const getBotAnimationClass = (botType) => {
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

  const comicStrips = [
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

  const scrollComics = (direction) => {
    if (comicsContainerRef.current) {
      comicsContainerRef.current.scrollBy({
        left: direction === 'left' ? -400 : 400,
        behavior: 'smooth'
      });
    }
  };

  React.useEffect(() => {
    const handleKeyDown = (e) => {
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

    const handleTouchStart = (e) => {
      touchStartX = e.changedTouches[0].screenX;
    };

    const handleTouchEnd = (e) => {
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
  const handlePanelClick = (comicIndex, panelIndex) => {
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
    <section id="comics" className="comics-section py-5">
      <div className="container">
        <div className="text-center mb-5">
          <h2 className="display-4 fw-bold text-burnt">THE ADDICTION CHRONICLES</h2>
          <p className="lead">Stories from the underground world of trial junkies</p>
        </div>
        
        {/* Mobile swipe instructions */}
        <div className="d-md-none text-center mb-4">
          <p className="small text-muted"><i className="fas fa-hand-point-right text-burnt me-1"></i> Swipe to navigate comics</p>
        </div>
        
        {/* Desktop click instructions */}
        <div className="d-none d-md-block text-center mb-4">
          <p className="small text-muted"><i className="fas fa-mouse-pointer text-burnt me-1"></i> Click panels to advance | Use arrow buttons to switch comics</p>
        </div>
        
        <div 
          ref={comicsContainerRef} 
          className="comics-container overflow-auto pb-4 mb-4 position-relative"
          style={{scrollSnapType: 'x mandatory'}}
        >
          <div className="d-inline-flex" style={{gap: '2rem'}}>
            {comicStrips.map((comic, comicIndex) => (
              <div 
                key={comicIndex}
                className={`comic-strip ${activeComic === comicIndex ? 'scale-100 opacity-100' : 'scale-95 opacity-80'} 
                         transition-all duration-300 border border-burnt rounded-lg overflow-hidden
                         min-width-280 sm-min-width-400 md-min-width-520`}
              >
                <h3 className={`comic-title text-center py-3 bg-black bg-opacity-60 text-burnt`}>
                  {comic.title}
                </h3>
                
                <div className="comic-panels row row-cols-1 row-cols-md-2 g-2 p-2 bg-black bg-opacity-40">
                  {comic.panels.map((panel, panelIndex) => {
                    const isActive = activePanel[comicIndex] === panelIndex;
                    const isPast = activePanel[comicIndex] > panelIndex;
                    
                    return (
                      <div 
                        key={panelIndex} 
                        className={`comic-panel col cursor-pointer rounded-lg overflow-hidden transition-all duration-300
                                 ${isActive ? 'ring ring-burnt scale-105 z-10' : ''} 
                                 ${isPast ? 'opacity-60' : 'opacity-100'}`}
                        onClick={() => handlePanelClick(comicIndex, panelIndex)}
                      >
                        <div className="panel-image-container position-relative p-4 d-flex justify-content-center align-items-center">
                          <img 
                            src={getBotImage(panel.botType)} 
                            alt={`${panel.botType} character`} 
                            className={`panel-image ${getBotAnimationClass(panel.botType)}`} 
                            style={{maxWidth: '100px', maxHeight: '100px'}}
                          />
                          
                          <div className="speech-bubble position-absolute top-0 end-0 max-w-75 bg-white bg-opacity-10 rounded-lg p-3 transform translate-y--33 translate-x-25">
                            <p className="small">{panel.dialogue}</p>
                          </div>
                        </div>
                        
                        <div className="panel-content p-3 bg-black bg-opacity-50">
                          <p className="panel-caption small text-center opacity-80">
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
        <div className="comics-navigation d-flex justify-content-center" style={{gap: '1rem'}}>
          <button 
            className="btn btn-outline-burnt"
            onClick={() => {
              if (activeComic > 0) {
                setActiveComic(activeComic - 1);
                scrollComics('left');
              }
            }}
            disabled={activeComic === 0}
            aria-label="Previous comic"
          >
            <i className="fas fa-chevron-left me-2"></i> Previous
          </button>
          
          <button 
            className="btn btn-burnt"
            onClick={() => {
              if (activeComic < comicStrips.length - 1) {
                setActiveComic(activeComic + 1);
                scrollComics('right');
              }
            }}
            disabled={activeComic === comicStrips.length - 1}
            aria-label="Next comic"
          >
            Next <i className="fas fa-chevron-right ms-2"></i>
          </button>
        </div>
      </div>
    </section>
  );
};

export default ComicsSection;