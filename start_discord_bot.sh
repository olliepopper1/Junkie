#!/bin/bash
# Script to start the Discord bot without Flask
# This avoids port conflicts with the web server
echo "Starting Discord Bot in standalone mode..."

# Set environment variables
export NO_FLASK=1
export NO_WEB_SERVER=1
export DISCORD_BOT_ONLY=1
export PYTHONUNBUFFERED=1

# Use a dedicated entry point that doesn't import Flask
python discord_bot_entry.py