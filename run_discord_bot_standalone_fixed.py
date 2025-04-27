"""
Run Discord Bot Standalone (Fixed)
Avoids port conflict with Flask app by removing web dependencies
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

# Load environment variables
load_dotenv()

def run_discord_bot():
    """Run the Discord bot directly with no web server dependency"""
    logger.info("Starting Discord bot standalone process (no web server dependency)...")
    
    try:
        from discord_bot_standalone import main as discord_main
        discord_main()
    except Exception as e:
        logger.error(f"Failed to start Discord bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_discord_bot()