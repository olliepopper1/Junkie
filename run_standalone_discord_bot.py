"""
Run Standalone Discord Bot
This script runs the Discord bot independently from the web app
"""
import os
import sys
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord_bot_standalone import main as discord_bot_main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("discord_bot_runner")

# Load environment variables
load_dotenv()

# Verify Discord token is available
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

if __name__ == "__main__":
    logger.info("Starting standalone Discord bot...")
    try:
        # Run the bot's main function from discord_bot_standalone.py
        discord_bot_main()
    except Exception as e:
        logger.error(f"Failed to start Discord bot: {e}")
        sys.exit(1)