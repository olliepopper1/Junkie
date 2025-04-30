#!/usr/bin/env python3
"""
Main Discord Bot Entry Point for Workflow
This is a file specifically designed to be used in the Replit discord_bot workflow
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
logger = logging.getLogger("main_discord_bot")

# Set environment variables to prevent Flask conflicts
os.environ['NO_FLASK'] = '1'
os.environ['NO_WEB_APP'] = '1'
os.environ['DISCORD_BOT_ONLY'] = '1'

# Load environment variables
load_dotenv()

# Check for Discord token
if not os.getenv('DISCORD_BOT_TOKEN'):
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

if __name__ == "__main__":
    logger.info("Starting Discord bot workflow...")
    
    try:
        # Import standalone bot to avoid any Flask dependencies
        import standalone_bot
        
        # Run the bot
        standalone_bot.run_bot()
        
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)