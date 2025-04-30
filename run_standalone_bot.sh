#!/bin/bash
# Run the completely standalone Discord bot with no Flask dependencies

echo "Starting standalone Discord bot..."
export PYTHONUNBUFFERED=1

# Run the standalone bot
python standalone_bot.py