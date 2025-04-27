"""
Discord Bot Runner for Trial Junkie
This script runs only the Discord bot functionality without starting a web server
"""
import os
import sys
import logging
import discord
from discord.ext import commands
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
    """Run the Discord bot without starting a Flask server"""
    # Load environment variables
    load_dotenv()
    
    # Check if Discord token is available
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("DISCORD_BOT_TOKEN not found in environment variables")
        logger.info("Please set DISCORD_BOT_TOKEN in the .env file")
        return False
    
    # Create the bot using the setup function
    bot = setup_bot()
    
    # Run the bot
    logger.info("Starting Trial Junkie Discord Bot...")
    
    try:
        bot.run(token)
        return True
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if run_discord_bot() else 1)