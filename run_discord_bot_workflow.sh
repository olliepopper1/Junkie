#!/bin/bash
# Run script for the Discord bot workflow version
# This script ensures the bot runs without Flask and avoids port conflicts

echo "Starting Discord Bot Workflow version..."
export NO_FLASK=1
export NO_WEB_APP=1
export DISCORD_BOT_ONLY=1
export PYTHONUNBUFFERED=1

# Run the workflow-specific bot directly
python discord_bot_workflow.py