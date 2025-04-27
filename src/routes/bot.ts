import { Router, Request, Response } from 'express';
import { exec } from 'child_process';
import { promisify } from 'util';

const execPromise = promisify(exec);

interface BotStatus {
  running: boolean;
  startedAt?: Date;
  error?: string;
}

// Create a router
const router = Router();

// Store the bot process
let botProcess: any = null;
let botStatus: BotStatus = { running: false };

// Get the status of the bot
router.get('/status', (req: Request, res: Response) => {
  res.json(botStatus);
});

// Start the bot
router.post('/start', (req: Request, res: Response) => {
  if (botStatus.running) {
    return res.status(400).json({ error: 'Bot is already running' });
  }

  try {
    botProcess = exec('python run_discord_bot.py');
    botStatus.running = true;
    botStatus.startedAt = new Date();
    delete botStatus.error;

    botProcess.stdout.on('data', (data: Buffer) => {
      console.log(`Bot stdout: ${data}`);
    });

    botProcess.stderr.on('data', (data: Buffer) => {
      console.error(`Bot stderr: ${data}`);
      if (!botStatus.error) {
        botStatus.error = '';
      }
      botStatus.error += data.toString();
    });

    botProcess.on('exit', (code: number) => {
      console.log(`Bot process exited with code ${code}`);
      botStatus.running = false;
      if (code !== 0) {
        if (!botStatus.error) {
          botStatus.error = '';
        }
        botStatus.error += `Process exited with code ${code}`;
      }
    });

    res.json({ message: 'Bot started successfully', status: botStatus });
  } catch (error) {
    botStatus.running = false;
    botStatus.error = error.message;
    res.status(500).json({ error: 'Failed to start bot', details: error.message });
  }
});

// Stop the bot
router.post('/stop', (req: Request, res: Response) => {
  if (!botStatus.running) {
    return res.status(400).json({ error: 'Bot is not running' });
  }

  try {
    if (botProcess) {
      botProcess.kill();
      botProcess = null;
    }
    botStatus.running = false;
    delete botStatus.startedAt;
    res.json({ message: 'Bot stopped successfully' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to stop bot', details: error.message });
  }
});

// Execute a bot command
router.post('/command', async (req: Request, res: Response) => {
  try {
    const { userId, username, command, args } = req.body;

    if (!userId || !username || !command) {
      return res.status(400).json({ error: 'Missing required parameters' });
    }

    // Execute the command using the Python script
    const commandArgs = args ? JSON.stringify(args) : '[]';
    const { stdout, stderr } = await execPromise(
      `python execute_bot_command.py --user_id "${userId}" --username "${username}" --command "${command}" --args '${commandArgs}'`
    );

    if (stderr) {
      console.error(`Command error: ${stderr}`);
      return res.status(500).json({ error: 'Command execution failed', details: stderr });
    }

    // Parse the command output
    try {
      const result = JSON.parse(stdout);
      res.json(result);
    } catch (e) {
      console.error(`Failed to parse command output: ${e.message}`);
      res.status(500).json({ error: 'Invalid command output', details: e.message, output: stdout });
    }
  } catch (error) {
    console.error(`Command execution error: ${error.message}`);
    res.status(500).json({ error: 'Command execution error', details: error.message });
  }
});

export default router;