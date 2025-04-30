#!/usr/bin/env python3
"""
Direct Discord Bot Starter
This script ensures the Discord bot runs without any Flask dependencies
"""
import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("start_discord_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("discord_bot_starter")

def main():
    """Run the Discord bot directly"""
    logger.info("Starting Discord bot directly...")
    
    # Set essential environment variables
    os.environ['NO_FLASK'] = '1'
    os.environ['NO_WEB_APP'] = '1'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    try:
        # Import the pure Discord bot module
        logger.info("Importing pure Discord bot module...")
        from pure_discord_bot import run_bot
        
        # Run the bot directly (blocking call)
        logger.info("Calling run_bot() function...")
        run_bot()
        
        return 0
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
