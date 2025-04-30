#!/bin/bash
# Standalone runner for Discord bot that avoids Flask
echo "Starting standalone Discord bot..."

# Ensure we're not importing app.py or Flask
export NO_FLASK=1

# Run the pure Discord bot script
python pure_discord_bot.py
