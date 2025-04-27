"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const child_process_1 = require("child_process");
const util_1 = require("util");
const execPromise = (0, util_1.promisify)(child_process_1.exec);
// Create a router
const router = (0, express_1.Router)();
// Get trials for a user
router.get('/trials/:userId', async (req, res) => {
    try {
        const { userId } = req.params;
        if (!userId) {
            return res.status(400).json({ error: 'Missing user ID' });
        }
        // Execute the Python script to get trials
        const { stdout, stderr } = await execPromise(`python get_bot_trials.py --user_id "${userId}"`);
        if (stderr) {
            console.error(`Get trials stderr: ${stderr}`);
            return res.status(500).json({ error: 'Failed to get trials', details: stderr });
        }
        // Parse the output
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        }
        catch (e) {
            console.error(`Failed to parse trials output: ${e.message}`);
            res.status(500).json({ error: 'Invalid trials output', details: e.message, output: stdout });
        }
    }
    catch (error) {
        console.error(`Get trials error: ${error.message}`);
        res.status(500).json({ error: 'Failed to get trials', details: error.message });
    }
});
// Get user statistics
router.get('/stats/:userId', async (req, res) => {
    try {
        const { userId } = req.params;
        if (!userId) {
            return res.status(400).json({ error: 'Missing user ID' });
        }
        // Execute the Python script to get user stats
        const { stdout, stderr } = await execPromise(`python bot_api_helpers.py --user_id "${userId}" --action get_user_stats`);
        if (stderr) {
            console.error(`Get stats stderr: ${stderr}`);
            return res.status(500).json({ error: 'Failed to get user stats', details: stderr });
        }
        // Parse the output
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        }
        catch (e) {
            console.error(`Failed to parse stats output: ${e.message}`);
            res.status(500).json({ error: 'Invalid stats output', details: e.message, output: stdout });
        }
    }
    catch (error) {
        console.error(`Get stats error: ${error.message}`);
        res.status(500).json({ error: 'Failed to get user stats', details: error.message });
    }
});
// Get user payments
router.get('/payments/:userId', async (req, res) => {
    try {
        const { userId } = req.params;
        const { status } = req.query;
        if (!userId) {
            return res.status(400).json({ error: 'Missing user ID' });
        }
        // Build the command
        let command = `python bot_api_helpers.py --user_id "${userId}" --action get_user_payments`;
        if (status) {
            command += ` --status "${status}"`;
        }
        // Execute the Python script to get user payments
        const { stdout, stderr } = await execPromise(command);
        if (stderr) {
            console.error(`Get payments stderr: ${stderr}`);
            return res.status(500).json({ error: 'Failed to get user payments', details: stderr });
        }
        // Parse the output
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        }
        catch (e) {
            console.error(`Failed to parse payments output: ${e.message}`);
            res.status(500).json({ error: 'Invalid payments output', details: e.message, output: stdout });
        }
    }
    catch (error) {
        console.error(`Get payments error: ${error.message}`);
        res.status(500).json({ error: 'Failed to get user payments', details: error.message });
    }
});
// Get user tier
router.get('/tier/:userId', async (req, res) => {
    try {
        const { userId } = req.params;
        if (!userId) {
            return res.status(400).json({ error: 'Missing user ID' });
        }
        // Execute the Python script to get user tier
        const { stdout, stderr } = await execPromise(`python bot_api_helpers.py --user_id "${userId}" --action get_user_tier`);
        if (stderr) {
            console.error(`Get tier stderr: ${stderr}`);
            return res.status(500).json({ error: 'Failed to get user tier', details: stderr });
        }
        // Parse the output
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        }
        catch (e) {
            console.error(`Failed to parse tier output: ${e.message}`);
            res.status(500).json({ error: 'Invalid tier output', details: e.message, output: stdout });
        }
    }
    catch (error) {
        console.error(`Get tier error: ${error.message}`);
        res.status(500).json({ error: 'Failed to get user tier', details: error.message });
    }
});
// Get referral stats
router.get('/referrals/:userId', async (req, res) => {
    try {
        const { userId } = req.params;
        if (!userId) {
            return res.status(400).json({ error: 'Missing user ID' });
        }
        // Execute the Python script to get referral stats
        const { stdout, stderr } = await execPromise(`python bot_api_helpers.py --user_id "${userId}" --action get_referral_stats`);
        if (stderr) {
            console.error(`Get referrals stderr: ${stderr}`);
            return res.status(500).json({ error: 'Failed to get referral stats', details: stderr });
        }
        // Parse the output
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        }
        catch (e) {
            console.error(`Failed to parse referrals output: ${e.message}`);
            res.status(500).json({ error: 'Invalid referrals output', details: e.message, output: stdout });
        }
    }
    catch (error) {
        console.error(`Get referrals error: ${error.message}`);
        res.status(500).json({ error: 'Failed to get referral stats', details: error.message });
    }
});
exports.default = router;
//# sourceMappingURL=api.js.map