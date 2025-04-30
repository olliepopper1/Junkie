#!/bin/bash
# Completely standalone Discord bot runner

echo "Starting standalone Discord bot..."

# Set environment variables to prevent Flask import
export NO_FLASK=1
export PYTHONUNBUFFERED=1

# Run the standalone Discord bot runner
python run_discord_bot_standalone.py
