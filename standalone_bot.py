"""
Standalone Discord Bot Runner
This script runs only the Discord bot without starting any Flask server
"""
import os
import logging
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from agents.pusher import Pusher
from database import Database
from utils.logger import CommandLogger
from utils.cooldown import Cooldown
from utils.response_templates import get_agent_quote, random_drug_emoji
from commands.trial_commands import TrialCommands

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
    
    # Set up intents
    intents = discord.Intents.default()
    intents.message_content = True
    
    # Create the bot
    bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
    
    # Create database connection
    db = Database()
    
    # Create the main pusher agent
    pusher = Pusher(db)
    
    # Create cooldown manager
    cooldown = Cooldown()
    
    # Create command logger
    cmd_logger = CommandLogger()
    
    @bot.event
    async def on_ready():
        """Called when the bot is ready and connected to Discord"""
        logger.info(f"Trial Junkie online as {bot.user}")
        await bot.change_presence(activity=discord.Game(name="!hit | !dose | !stash | !help"))
    
    # Import all command handlers from bot.py
    from bot import setup_bot
    temp_bot = setup_bot()
    
    # Copy all commands from the temporary bot to our bot
    for command in temp_bot.commands:
        bot.add_command(command)
    
    # Check if Discord token is available
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("DISCORD_BOT_TOKEN not found in environment variables")
        logger.info("Please set DISCORD_BOT_TOKEN in the .env file")
        return False
    
    # Run the bot
    logger.info("Starting Trial Junkie Discord Bot...")
    
    try:
        bot.run(token)
        return True
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        return False

if __name__ == "__main__":
    run_discord_bot()