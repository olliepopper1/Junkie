#!/bin/bash
# Improved runner for completely independent Discord bot

echo "Starting fixed standalone Discord bot..."

# Set essential environment variables
export NO_FLASK=1
export NO_WEB_APP=1
export PYTHONUNBUFFERED=1

# Run the fixed standalone bot runner
python run_discord_bot_standalone_fixed.py
