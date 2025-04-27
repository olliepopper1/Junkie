#!/usr/bin/env python3
"""
Discord Bot Runner for Trial Junkie
Standalone script to run the Discord bot without the web server
"""
import os
import sys
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("discord_bot")

# Load environment variables
load_dotenv()

def run_discord_bot():
    # Check for token
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        logger.error("No Discord bot token found. Please set DISCORD_BOT_TOKEN environment variable.")
        sys.exit(1)

    # Create bot instance
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    # Import the setup_commands function from discord_bot_standalone
    try:
        from discord_bot_standalone import setup_commands
        setup_commands(bot)
        logger.info("Bot commands set up successfully")
    except Exception as e:
        logger.error(f"Error setting up bot commands: {e}")
        sys.exit(1)

    # Run the bot
    try:
        logger.info("Starting Discord bot...")
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_discord_bot()
