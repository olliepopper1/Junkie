#!/usr/bin/env python3
"""
Discord Bot Workflow Runner
This script is specifically designed to work with the Replit 'discord_bot' workflow
It runs the Discord bot without any Flask dependencies
"""
import os
import sys
import logging
from dotenv import load_dotenv
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("discord_bot_workflow")

# Make sure we don't import Flask
os.environ['NO_FLASK'] = 'true'

# Main function to run the bot
def run_discord_bot():
    """Run the Discord bot using our standalone implementation"""
    logger.info("Loading standalone Discord bot...")
    
    try:
        # Import our standalone bot implementation
        import standalone_discord_bot
        
        # Run the bot
        logger.info("Starting standalone Discord bot...")
        standalone_discord_bot.run_bot()
        
    except ImportError as e:
        logger.error(f"Failed to import standalone_discord_bot: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    logger.info("Starting Discord Bot Workflow Runner...")
    run_discord_bot()