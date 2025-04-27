// Discord Bot Section Component for Trial Junkies

const DiscordSection = () => {
  return (
    <section id="discord" className="discord-section py-5">
      <div className="container">
        <div className="row align-items-center">
          <div className="col-lg-6 mb-5 mb-lg-0">
            <div className="text-center text-lg-start">
              <h2 className="display-4 fw-bold text-burnt mb-4">GET YOUR FIRST HIT</h2>
              <p className="lead mb-4">Start your digital bender with our Discord bot - the quickest way to score free trials</p>
              
              <div className="discord-features mb-4">
                <div className="feature-item d-flex align-items-start mb-3">
                  <div className="feature-icon me-3">
                    <i className="fas fa-syringe text-burnt"></i>
                  </div>
                  <div>
                    <h4 className="fs-5 text-burnt">Instant Rush</h4>
                    <p>Type !hit and get an immediate trial fix delivered right to your DMs</p>
                  </div>
                </div>
                
                <div className="feature-item d-flex align-items-start mb-3">
                  <div className="feature-icon me-3">
                    <i className="fas fa-prescription text-burnt"></i>
                  </div>
                  <div>
                    <h4 className="fs-5 text-burnt">Custom Doses</h4>
                    <p>Choose your specific agent with !dose for specialized trial generation</p>
                  </div>
                </div>
                
                <div className="feature-item d-flex align-items-start mb-3">
                  <div className="feature-icon me-3">
                    <i className="fas fa-user-secret text-burnt"></i>
                  </div>
                  <div>
                    <h4 className="fs-5 text-burnt">Auto-Trip</h4>
                    <p>Let our bots handle the automation with !trip to sign up automatically</p>
                  </div>
                </div>
                
                <div className="feature-item d-flex align-items-start">
                  <div className="feature-icon me-3">
                    <i className="fas fa-pills text-burnt"></i>
                  </div>
                  <div>
                    <h4 className="fs-5 text-burnt">Stash Management</h4>
                    <p>Keep track of all your trial accounts with !stash command</p>
                  </div>
                </div>
              </div>
              
              <div className="discord-action">
                <a href="https://discord.gg/trialjunkie" className="btn btn-lg btn-burnt pulse-animation me-3">
                  <i className="fab fa-discord me-2"></i> Add to Discord
                </a>
                <a href="#commands" className="btn btn-lg btn-outline-burnt">View Commands</a>
              </div>
            </div>
          </div>
          
          <div className="col-lg-6">
            <div className="discord-preview p-4 bg-darker rounded-lg border border-burnt glow-animation">
              <div className="discord-header d-flex align-items-center mb-4">
                <img src="/static/images/fire-skull.png" alt="Trial Junkies Bot" className="discord-bot-avatar me-3" width="64" height="64" />
                <div>
                  <h4 className="text-burnt mb-0">Trial Junkies Bot</h4>
                  <span className="text-success">Online</span>
                </div>
              </div>
              
              <div className="discord-chat p-3 rounded mb-4" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
                <div className="discord-message mb-3">
                  <div className="message-header d-flex align-items-center mb-1">
                    <span className="username text-burnt">User</span>
                    <span className="timestamp ms-2 text-muted">Today at 4:20 PM</span>
                  </div>
                  <div className="message-content">!hit netflix</div>
                </div>
                
                <div className="discord-message mb-3">
                  <div className="message-header d-flex align-items-center mb-1">
                    <span className="username text-success">Trial Junkies</span>
                    <span className="timestamp ms-2 text-muted">Today at 4:20 PM</span>
                  </div>
                  <div className="message-content">
                    <div className="bot-embed p-3 border-left border-burnt rounded">
                      <h5 className="text-burnt">🔥 Scoring your Netflix hit...</h5>
                      <p>Heroin Harry is cooking up your trial credentials. This might give you a rush!</p>
                      <div className="progress mb-3" style={{height: '10px'}}>
                        <div className="progress-bar bg-burnt progress-bar-striped progress-bar-animated" style={{width: '100%'}}></div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="discord-message">
                  <div className="message-header d-flex align-items-center mb-1">
                    <span className="username text-success">Trial Junkies</span>
                    <span className="timestamp ms-2 text-muted">Today at 4:21 PM</span>
                  </div>
                  <div className="message-content">
                    <div className="bot-embed p-3 border-left border-burnt rounded">
                      <h5 className="text-burnt">✅ Your Netflix fix is ready!</h5>
                      <div className="credential-list mb-2">
                        <div><strong>Email:</strong> user524@protonmail.com</div>
                        <div><strong>Password:</strong> B3st#Pa$$w0rD!</div>
                        <div><strong>Plan:</strong> Premium</div>
                        <div><strong>Expires:</strong> May 27, 2025</div>
                      </div>
                      <p className="mb-0 fst-italic">That first hit's always the best. Enjoy the high! 🎭</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="discord-commands">
                <div className="command-input d-flex">
                  <input type="text" className="form-control bg-dark text-white border-burnt" placeholder="Type a command..." disabled />
                  <button className="btn btn-burnt ms-2" disabled>Send</button>
                </div>
                <div className="command-examples mt-2">
                  <small className="text-muted">Try: !hit, !dose, !trip, !stash, !referral</small>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="row mt-5 pt-5" id="commands">
          <div className="col-12">
            <h3 className="text-center text-burnt mb-4">COMMAND YOUR FIX</h3>
            <div className="command-card p-4 border border-burnt rounded">
              <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                <div className="col">
                  <div className="command-item p-3 bg-darker rounded h-100">
                    <div className="d-flex align-items-center mb-3">
                      <div className="command-icon me-3">
                        <i className="fas fa-bolt text-burnt"></i>
                      </div>
                      <h5 className="mb-0 text-burnt">!hit [service]</h5>
                    </div>
                    <p className="mb-2">Get a full trial account instantly</p>
                    <div className="command-example bg-black p-2 rounded">
                      <code>!hit netflix</code>
                      <small className="d-block text-muted">Generates complete Netflix trial</small>
                    </div>
                  </div>
                </div>
                
                <div className="col">
                  <div className="command-item p-3 bg-darker rounded h-100">
                    <div className="d-flex align-items-center mb-3">
                      <div className="command-icon me-3">
                        <i className="fas fa-syringe text-burnt"></i>
                      </div>
                      <h5 className="mb-0 text-burnt">!dose [agent] [service]</h5>
                    </div>
                    <p className="mb-2">Get specific agent help for a service</p>
                    <div className="command-example bg-black p-2 rounded">
                      <code>!dose harry netflix</code>
                      <small className="d-block text-muted">Harry generates Netflix identity</small>
                    </div>
                  </div>
                </div>
                
                <div className="col">
                  <div className="command-item p-3 bg-darker rounded h-100">
                    <div className="d-flex align-items-center mb-3">
                      <div className="command-icon me-3">
                        <i className="fas fa-robot text-burnt"></i>
                      </div>
                      <h5 className="mb-0 text-burnt">!trip [service]</h5>
                    </div>
                    <p className="mb-2">Full automation for trial signup</p>
                    <div className="command-example bg-black p-2 rounded">
                      <code>!trip youtube</code>
                      <small className="d-block text-muted">Automates YouTube Premium trial</small>
                    </div>
                  </div>
                </div>
                
                <div className="col">
                  <div className="command-item p-3 bg-darker rounded h-100">
                    <div className="d-flex align-items-center mb-3">
                      <div className="command-icon me-3">
                        <i className="fas fa-pills text-burnt"></i>
                      </div>
                      <h5 className="mb-0 text-burnt">!stash</h5>
                    </div>
                    <p className="mb-2">View all your trial accounts</p>
                    <div className="command-example bg-black p-2 rounded">
                      <code>!stash</code>
                      <small className="d-block text-muted">Shows all your active credentials</small>
                    </div>
                  </div>
                </div>
                
                <div className="col">
                  <div className="command-item p-3 bg-darker rounded h-100">
                    <div className="d-flex align-items-center mb-3">
                      <div className="command-icon me-3">
                        <i className="fas fa-money-bill-wave text-burnt"></i>
                      </div>
                      <h5 className="mb-0 text-burnt">!pay [plan]</h5>
                    </div>
                    <p className="mb-2">Upgrade your subscription tier</p>
                    <div className="command-example bg-black p-2 rounded">
                      <code>!pay rush</code>
                      <small className="d-block text-muted">Upgrade to Five Dollar Rush plan</small>
                    </div>
                  </div>
                </div>
                
                <div className="col">
                  <div className="command-item p-3 bg-darker rounded h-100">
                    <div className="d-flex align-items-center mb-3">
                      <div className="command-icon me-3">
                        <i className="fas fa-users text-burnt"></i>
                      </div>
                      <h5 className="mb-0 text-burnt">!referral</h5>
                    </div>
                    <p className="mb-2">Get your referral code to share</p>
                    <div className="command-example bg-black p-2 rounded">
                      <code>!referral</code>
                      <small className="d-block text-muted">Generates your unique referral link</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default DiscordSection;