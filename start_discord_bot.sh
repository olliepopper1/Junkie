#!/bin/bash
# Start Discord Bot Script
# This script starts the Discord bot directly without relying on the workflow

# Set environment variables to prevent Flask conflicts
export NO_FLASK=1
export NO_WEB_APP=1
export PYTHONUNBUFFERED=1

# Kill any existing Discord bot processes
pkill -f "python.*pure_discord_bot.py" || true
pkill -f "python.*start_discord_bot.py" || true

# Start the Discord bot in the background
nohup python pure_discord_bot.py > discord_bot_output.log 2>&1 &

# Wait a moment to check if it started
sleep 2

# Check if the bot started successfully
if grep -q "Bot is ready" discord_bot.log 2>/dev/null; then
  echo "Discord bot started successfully!"
  echo "Check discord_bot.log for detailed logs"
elif grep -q "Error" discord_bot.log 2>/dev/null; then
  echo "Error starting Discord bot. Check discord_bot.log for details."
  tail -n 10 discord_bot.log
else
  echo "Discord bot is starting... Check discord_bot.log for status."
fi

# Show the process
ps aux | grep -i "python.*discord_bot" | grep -v grep
