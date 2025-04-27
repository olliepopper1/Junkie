"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const child_process_1 = require("child_process");
const util_1 = require("util");
const execPromise = (0, util_1.promisify)(child_process_1.exec);
// Create a router
const router = (0, express_1.Router)();
// Store the bot process
let botProcess = null;
let botStatus = { running: false };
// Get the status of the bot
router.get('/status', (req, res) => {
    res.json(botStatus);
});
// Start the bot
router.post('/start', (req, res) => {
    if (botStatus.running) {
        return res.status(400).json({ error: 'Bot is already running' });
    }
    try {
        botProcess = (0, child_process_1.exec)('python run_discord_bot.py');
        botStatus.running = true;
        botStatus.startedAt = new Date();
        delete botStatus.error;
        botProcess.stdout.on('data', (data) => {
            console.log(`Bot stdout: ${data}`);
        });
        botProcess.stderr.on('data', (data) => {
            console.error(`Bot stderr: ${data}`);
            if (!botStatus.error) {
                botStatus.error = '';
            }
            botStatus.error += data.toString();
        });
        botProcess.on('exit', (code) => {
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
    }
    catch (error) {
        botStatus.running = false;
        botStatus.error = error.message;
        res.status(500).json({ error: 'Failed to start bot', details: error.message });
    }
});
// Stop the bot
router.post('/stop', (req, res) => {
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
    }
    catch (error) {
        res.status(500).json({ error: 'Failed to stop bot', details: error.message });
    }
});
// Execute a bot command
router.post('/command', async (req, res) => {
    try {
        const { userId, username, command, args } = req.body;
        if (!userId || !username || !command) {
            return res.status(400).json({ error: 'Missing required parameters' });
        }
        // Execute the command using the Python script
        const commandArgs = args ? JSON.stringify(args) : '[]';
        const { stdout, stderr } = await execPromise(`python execute_bot_command.py --user_id "${userId}" --username "${username}" --command "${command}" --args '${commandArgs}'`);
        if (stderr) {
            console.error(`Command error: ${stderr}`);
            return res.status(500).json({ error: 'Command execution failed', details: stderr });
        }
        // Parse the command output
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        }
        catch (e) {
            console.error(`Failed to parse command output: ${e.message}`);
            res.status(500).json({ error: 'Invalid command output', details: e.message, output: stdout });
        }
    }
    catch (error) {
        console.error(`Command execution error: ${error.message}`);
        res.status(500).json({ error: 'Command execution error', details: error.message });
    }
});
exports.default = router;
//# sourceMappingURL=bot.js.map