#!/bin/bash

# This script runs the Discord bot as a standalone process
# without attempting to use port 5000, avoiding conflicts with the web app

echo "Starting Discord bot (standalone, no port conflicts)..."

# Run the new standalone Discord bot script
python start_discord_bot.py