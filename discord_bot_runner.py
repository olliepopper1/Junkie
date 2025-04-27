"""
Discord Bot Runner for Trial Junkie
Standalone script to run the Discord bot without the web server
"""
import os
import logging
import asyncio
from dotenv import load_dotenv
from bot import setup_bot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run_discord_bot():
    # Load environment variables
    load_dotenv()
    
    # Check if Discord token is available
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("DISCORD_BOT_TOKEN not found in environment variables")
        logger.info("Please set DISCORD_BOT_TOKEN in the .env file")
        exit(1)
    
    # Run the bot
    logger.info("Starting Trial Junkie Discord Bot...")
    bot = setup_bot()
    bot.run(token)

if __name__ == "__main__":
    run_discord_bot()