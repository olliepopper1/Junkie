"""
Start Discord Bot
This script starts only the Discord bot without any web server dependencies
"""
import os
import sys
import logging
import discord
from discord.ext import commands
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
logger = logging.getLogger("discord_bot")

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    logger.error("No Discord bot token found. Please set DISCORD_BOT_TOKEN environment variable.")
    sys.exit(1)

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Import bot commands from the standalone bot file
from discord_bot_standalone import setup_commands

# Setup bot commands
setup_commands(bot)

# Run the bot
if __name__ == "__main__":
    logger.info("Starting Discord bot...")
    bot.run(TOKEN)