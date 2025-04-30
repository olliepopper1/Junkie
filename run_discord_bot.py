#!/usr/bin/env python3
"""
Discord Bot Runner for Trial Junkie
Simple wrapper script to start the Discord bot
"""
import sys
import logging
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
logger = logging.getLogger("discord_bot_runner")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    logger.info("Starting Discord Bot...")
    try:
        # Import and run the bot
        import discord_bot
        # The bot will run from the imported module
    except Exception as e:
        logger.error(f"Error importing Discord bot: {e}")
        sys.exit(1)