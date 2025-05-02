#!/bin/bash
# Trial Junkie Discord Bot Runner
# Runs the Discord bot for the Trial Junkie system

echo "Starting Trial Junkie Discord Bot..."

# Ensure environment variables are set
if [ -z "$DISCORD_BOT_TOKEN" ]; then
    echo "Error: DISCORD_BOT_TOKEN environment variable is not set"
    echo "Please set this variable before running the bot"
    exit 1
fi

if [ -z "$RAPIDAPI_KEY" ]; then
    echo "Error: RAPIDAPI_KEY environment variable is not set"
    echo "Please set this variable before running the bot"
    exit 1
fi

# Install required dependencies if needed
echo "Checking dependencies..."
pip install -q discord.py selenium requests python-dotenv

# Make the bot runner executable
chmod +x main_discord_bot.py

# Run the bot
echo "Starting bot..."
python main_discord_bot.py