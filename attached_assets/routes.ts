import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import discordBotApi from "../discord_bot_api";

export async function registerRoutes(app: Express): Promise<Server> {
  // Discord Bot API - register the router
  app.use('/api/discord-bot', discordBotApi);
  
  // Referral API endpoints
  app.get('/api/referral/stats', (req, res) => {
    // Simulated referral stats for the Trial Junkies project
    const stats = {
      clicks: 21,
      signups: 8,
      activeUsers: 5,
      solEarned: 0.31
    };
    
    res.json(stats);
  });
  
  app.get('/api/referral/code', (req, res) => {
    // Generate a referral code (in a real app, this would be linked to user account)
    res.json({ code: 'TRIALJUNKIES123' });
  });
  
  // Wallet integration endpoint
  app.post('/api/wallet/verify', (req, res) => {
    // In a real app, this would verify the wallet signature
    res.json({ verified: true });
  });
  
  // Comics API endpoint
  app.get('/api/comics', (req, res) => {
    // Return comic strip data
    const comics = [
      {
        title: "THE ADDICTION BEGINS",
        panels: [
          {
            image: "https://images.unsplash.com/photo-1590439471364-192aa70c0b53?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&h=300&q=80",
            dialogue: "Why pay for subscriptions when you can get them for free?",
            caption: "Heroin Harry discovers the power of free trials"
          },
          // Additional panels would be here
        ]
      },
      // Additional comics would be here
    ];
    
    res.json(comics);
  });
  
  // Bot trials API endpoint - connect to Python bot database
  app.get('/api/trials', (req, res) => {
    // Execute Python script to get trials
    const { spawn } = require('child_process');
    const userId = req.query.user_id || 'test_user';
    
    const process = spawn('python', ['get_bot_trials.py', '--user_id', userId.toString()]);
    
    let outputData = '';
    let errorData = '';
    
    process.stdout.on('data', (data) => {
      outputData += data.toString();
    });
    
    process.stderr.on('data', (data) => {
      errorData += data.toString();
    });
    
    process.on('close', (code) => {
      if (code !== 0) {
        return res.status(500).json({ 
          error: 'Failed to fetch trials', 
          details: errorData || `Process exited with code ${code}` 
        });
      }
      
      try {
        const result = JSON.parse(outputData);
        return res.json(result.trials || []);
      } catch (e) {
        return res.status(500).json({ 
          error: 'Failed to parse trials data',
          details: e instanceof Error ? e.message : 'Unknown error'
        });
      }
    });
  });

  const httpServer = createServer(app);

  return httpServer;
}
