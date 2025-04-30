#!/bin/bash
# Run script for the completely fixed Discord bot
# This script ensures the bot runs without Flask and avoids port conflicts

echo "Starting fixed Discord Bot..."
export NO_FLASK=1
export NO_WEB_APP=1
export DISCORD_BOT_ONLY=1
export PYTHONUNBUFFERED=1

# Run the standalone bot directly
python fixed_discord_bot.py