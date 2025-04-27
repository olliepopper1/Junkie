import express, { Request, Response } from 'express';
import { spawn } from 'child_process';
import { z } from 'zod';
import path from 'path';
import fs from 'fs';

const router = express.Router();

// Schema validation for Discord commands
const CommandSchema = z.object({
  command: z.string(),
  user_id: z.string(),
  username: z.string(),
  params: z.record(z.string(), z.string()).optional(),
});

// Interface for Discord bot status
interface BotStatus {
  running: boolean;
  startedAt?: Date;
  error?: string;
}

// Keep track of Discord bot process
let botProcess: any = null;
let botStatus: BotStatus = { running: false };

// GET endpoint to check Discord bot status
router.get('/status', (req: Request, res: Response) => {
  res.json(botStatus);
});

// POST endpoint to start the Discord bot
router.post('/start', (req: Request, res: Response) => {
  if (botProcess && botStatus.running) {
    return res.status(400).json({ error: 'Discord bot is already running' });
  }

  try {
    // Start the Discord bot in a separate process
    botProcess = spawn('python', ['run_discord_bot.py'], {
      detached: true,
      stdio: 'pipe',
    });

    botStatus = {
      running: true,
      startedAt: new Date(),
    };

    // Handle bot stdout
    botProcess.stdout.on('data', (data: Buffer) => {
      console.log(`Discord Bot: ${data.toString()}`);
    });

    // Handle bot stderr
    botProcess.stderr.on('data', (data: Buffer) => {
      console.error(`Discord Bot Error: ${data.toString()}`);
    });

    // Handle bot exit
    botProcess.on('close', (code: number) => {
      console.log(`Discord bot process exited with code ${code}`);
      botStatus = {
        running: false,
        error: code !== 0 ? `Bot exited with code ${code}` : undefined,
      };
      botProcess = null;
    });

    return res.json({ status: 'started', botStatus });
  } catch (error) {
    botStatus = {
      running: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
    return res.status(500).json({ error: 'Failed to start Discord bot', details: error });
  }
});

// POST endpoint to stop the Discord bot
router.post('/stop', (req: Request, res: Response) => {
  if (!botProcess || !botStatus.running) {
    return res.status(400).json({ error: 'Discord bot is not running' });
  }

  try {
    // Kill the Discord bot process
    botProcess.kill();
    botStatus = {
      running: false,
    };
    botProcess = null;
    return res.json({ status: 'stopped' });
  } catch (error) {
    return res.status(500).json({ error: 'Failed to stop Discord bot', details: error });
  }
});

// POST endpoint to restart the Discord bot
router.post('/restart', (req: Request, res: Response) => {
  if (botProcess && botStatus.running) {
    botProcess.kill();
    botProcess = null;
  }

  try {
    // Start the Discord bot in a separate process
    botProcess = spawn('python', ['run_discord_bot.py'], {
      detached: true,
      stdio: 'pipe',
    });

    botStatus = {
      running: true,
      startedAt: new Date(),
    };

    // Handle bot stdout
    botProcess.stdout.on('data', (data: Buffer) => {
      console.log(`Discord Bot: ${data.toString()}`);
    });

    // Handle bot stderr
    botProcess.stderr.on('data', (data: Buffer) => {
      console.error(`Discord Bot Error: ${data.toString()}`);
    });

    // Handle bot exit
    botProcess.on('close', (code: number) => {
      console.log(`Discord bot process exited with code ${code}`);
      botStatus = {
        running: false,
        error: code !== 0 ? `Bot exited with code ${code}` : undefined,
      };
      botProcess = null;
    });

    return res.json({ status: 'restarted', botStatus });
  } catch (error) {
    botStatus = {
      running: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
    return res.status(500).json({ error: 'Failed to restart Discord bot', details: error });
  }
});

// POST endpoint to send a command to the Discord bot database
router.post('/command', async (req: Request, res: Response) => {
  try {
    // Validate command data
    const commandData = CommandSchema.parse(req.body);
    
    // We'll communicate with the bot database directly
    // This requires python script execution to access the database
    const scriptPath = path.join(__dirname, 'execute_bot_command.py');
    
    // Check if the script exists
    if (!fs.existsSync(scriptPath)) {
      return res.status(500).json({ error: 'Bot command execution script not found' });
    }
    
    // Execute the Python script with command data
    const process = spawn('python', [
      scriptPath,
      '--command', commandData.command,
      '--user_id', commandData.user_id,
      '--username', commandData.username,
      '--params', JSON.stringify(commandData.params || {})
    ]);
    
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
          error: 'Command execution failed', 
          details: errorData || `Process exited with code ${code}` 
        });
      }
      
      try {
        const result = JSON.parse(outputData);
        return res.json(result);
      } catch (e) {
        return res.status(500).json({ 
          error: 'Failed to parse command result', 
          details: e instanceof Error ? e.message : 'Unknown error',
          output: outputData
        });
      }
    });
  } catch (error) {
    return res.status(400).json({ 
      error: 'Invalid command data', 
      details: error instanceof Error ? error.message : 'Unknown error' 
    });
  }
});

// GET endpoint to retrieve trials for a user
router.get('/trials/:userId', (req: Request, res: Response) => {
  const userId = req.params.userId;
  
  try {
    // Execute Python script to fetch trials from the bot database
    const process = spawn('python', [
      path.join(__dirname, 'get_bot_trials.py'),
      '--user_id', userId
    ]);
    
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
        const trials = JSON.parse(outputData);
        return res.json(trials);
      } catch (e) {
        return res.status(500).json({ 
          error: 'Failed to parse trials data', 
          details: e instanceof Error ? e.message : 'Unknown error' 
        });
      }
    });
  } catch (error) {
    return res.status(500).json({ 
      error: 'Failed to fetch trials', 
      details: error instanceof Error ? error.message : 'Unknown error' 
    });
  }
});

export default router;