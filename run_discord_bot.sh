#!/bin/bash
# Run script for the Discord bot
# This script ensures the bot runs outside of the Flask web server

echo "Starting Discord Bot..."
export NO_FLASK=1
export NO_WEB_SERVER=1
export DISCORD_BOT_ONLY=1
export PYTHONUNBUFFERED=1

# Run the dedicated Discord bot entry point
python discord_bot_main.py