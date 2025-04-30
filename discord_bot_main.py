#!/usr/bin/env python3
"""
Discord Bot Main Entry Point
A standalone version that doesn't conflict with the Flask web server
"""
import os
import sys
import logging
import subprocess
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
logger = logging.getLogger("discord_bot_main")

# Load environment variables
load_dotenv()

def main():
    """Run the standalone Discord bot"""
    logger.info("Starting standalone Discord bot...")
    
    try:
        # Import discord.py to check if it's installed
        import discord
        logger.info(f"Using discord.py version: {discord.__version__}")
        
        # Import our pure Discord bot implementation
        import pure_discord_bot
        
        # Run the bot
        pure_discord_bot.run_bot()
        
        return 0
    except ImportError as e:
        logger.error(f"Missing required module: {e}")
        return 1
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())