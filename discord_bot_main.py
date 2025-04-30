#!/usr/bin/env python3
"""
Discord Bot Main Entry Point
A standalone version that doesn't conflict with the Flask web server
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
        logging.FileHandler("discord_bot_output.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("discord_bot_main")

# Load environment variables
load_dotenv()

# Important: Set environment variables to prevent Flask conflicts
os.environ['NO_FLASK'] = '1'
os.environ['NO_WEB_SERVER'] = '1'
os.environ['DISCORD_BOT_ONLY'] = '1'

def main():
    """Run the standalone Discord bot"""
    logger.info("Starting standalone Discord bot...")
    
    try:
        # Instead of importing main.py which loads Flask,
        # import standalone_discord_bot which has no Flask dependencies
        import standalone_discord_bot
        
        # Run the bot
        # Check if 'main' function exists, otherwise try 'run_bot'
        if hasattr(standalone_discord_bot, 'main'):
            standalone_discord_bot.main()
        else:
            standalone_discord_bot.run_bot()
        
    except ImportError as e:
        logger.error(f"Failed to import standalone_discord_bot: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()