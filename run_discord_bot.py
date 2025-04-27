#!/usr/bin/env python3
"""
Run Discord Bot
This script runs the standalone Discord bot without using Flask
"""
import os
import sys
import logging
from dotenv import load_dotenv
import discord_bot_standalone

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

def main():
    """Main function to run the Discord bot"""
    # Load environment variables
    load_dotenv()
    
    # Check if Discord token is available
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("DISCORD_BOT_TOKEN not found in environment variables")
        logger.info("Please set DISCORD_BOT_TOKEN in the .env file")
        sys.exit(1)
    
    # Run the bot
    logger.info("Starting Trial Junkie Discord Bot...")
    try:
        discord_bot_standalone.main()
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()