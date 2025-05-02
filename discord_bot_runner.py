#!/usr/bin/env python3
"""
Discord Bot Runner for Trial Junkie
Handles the startup and management of the Discord bot
"""
import os
import sys
import time
import logging
import traceback
import signal
import asyncio
from datetime import datetime
import discord
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot_workflow.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("discord_bot_runner")

# Load environment variables
load_dotenv()

# Check for Discord bot token
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

# Other required environment variables
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
if not RAPIDAPI_KEY:
    logger.warning("RAPIDAPI_KEY not found - API features may be limited")

# Import our Discord bot with error handling
try:
    logger.info("Importing Discord bot module")
    import discord_bot
    
    # Check for required bot attributes
    if not hasattr(discord_bot, 'bot'):
        logger.error("Discord bot module does not have a 'bot' attribute")
        sys.exit(1)
        
    bot = discord_bot.bot
    logger.info("Discord bot imported successfully")
    
except ImportError as e:
    logger.error(f"Failed to import Discord bot module: {str(e)}")
    sys.exit(1)
except Exception as e:
    logger.error(f"Error importing Discord bot: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

# Signal handling for graceful shutdown
def signal_handler(sig, frame):
    logger.info("Shutdown signal received, cleaning up...")
    # We need to run the asyncio event loop to properly close the bot
    if not bot.is_closed():
        asyncio.run(bot.close())
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    """Main function to run the Discord bot"""
    logger.info("Starting Discord bot...")
    start_time = datetime.now()
    
    try:
        # Initialize database
        from database import Database
        db = Database()
        db_result = db.initialize()
        
        if not db_result.get('success', False):
            logger.error(f"Database initialization failed: {db_result.get('message', 'Unknown error')}")
            logger.warning("Continuing without database connection...")
        else:
            logger.info("Database connection established")
        
        # Initialize API integrations
        from updated_api_integrations import UpdatedAPIIntegrations
        api = UpdatedAPIIntegrations()
        logger.info("API integrations initialized")
        
        # Run the bot with the Discord token from environment
        logger.info("Running Discord bot...")
        
        # Add our own on_ready event to log when bot is connected
        @bot.event
        async def on_ready():
            logger.info(f"Bot connected as {bot.user.name} (ID: {bot.user.id})")
            logger.info(f"Bot is in {len(bot.guilds)} guilds")
            logger.info(f"Bot startup took {(datetime.now() - start_time).total_seconds():.2f} seconds")
            
            # Set bot activity
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="for /help commands"
                )
            )
        
        # Start the bot
        bot.run(DISCORD_BOT_TOKEN)
        
    except Exception as e:
        logger.error(f"Error running Discord bot: {str(e)}")
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)