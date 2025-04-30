#!/bin/bash
# This script is specifically designed for the discord_bot workflow
# It runs the Discord bot in a completely separate process from the web app
# to avoid port conflicts

echo "Starting Discord Bot workflow script..."

# Set environment variables to prevent Flask conflicts
export NO_FLASK=1
export NO_WEB_APP=1
export DISCORD_BOT_ONLY=1
export FLASK_APP=""
export PYTHONUNBUFFERED=1

# Stop any existing Flask processes on port 5000 - IMPORTANT!
# This will prevent the bot from trying to start a Flask server
echo "Ensuring no Flask app is started in this process..."

# Run the standalone bot directly
echo "Starting Discord bot via standalone_bot.py..."
exec python standalone_bot.py