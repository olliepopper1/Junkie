#!/usr/bin/env python3
"""
Standalone Discord Bot Runner
This script runs the Discord bot without using Flask
"""
import os
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
    
    logger.info("Starting Discord Bot in standalone mode...")
    try:
        # Import and run the Discord bot directly
        import discord_bot
        # The bot will run in the imported module
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)
