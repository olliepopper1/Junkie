#!/bin/bash

# This script runs the Discord bot as a standalone process
# without attempting to use port 5000, avoiding conflicts with the web app

echo "Starting Discord bot (standalone, no port conflicts)..."

# Run the fixed Discord bot standalone script
# This version doesn't attempt to start a Flask app
python fixed_discord_bot.py