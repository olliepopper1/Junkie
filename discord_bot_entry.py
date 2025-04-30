#!/usr/bin/env python3
"""
Discord Bot Standalone Entry Point
Completely separate from Flask to avoid port conflicts
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
logger = logging.getLogger("discord_bot_entry")

# Set environment variables to prevent Flask import conflicts
os.environ['NO_FLASK'] = '1'
os.environ['NO_WEB_APP'] = '1'
os.environ['FLASK_PORT'] = '5001'  # Use a different port
os.environ['PORT'] = '5001'        # For applications that check PORT directly

# Load environment variables
load_dotenv()

# Check for Discord token
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN environment variable is not set")
    logger.error("Please set it in the .env file or environment")
    sys.exit(1)

def main():
    """Run the standalone Discord bot"""
    logger.info("Starting standalone Discord bot via entry point...")
    
    try:
        # Instead of importing app.py which causes conflicts,
        # use standalone discord bot implementation
        import standalone_discord_bot
        
        # Run the bot directly
        standalone_discord_bot.run_bot()
        
    except ImportError as e:
        logger.error(f"Failed to import standalone_discord_bot: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()