#!/usr/bin/env python3
"""
Standalone Discord Bot Runner
This version explicitly avoids using Flask or any web server to prevent port conflicts
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

def run_discord_bot():
    """Run the Discord bot standalone without any web server"""
    # Check for token
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        logger.error("No Discord bot token found. Please set DISCORD_BOT_TOKEN environment variable.")
        sys.exit(1)

    # Create bot instance with intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    # Import functionality from discord_bot_standalone
    try:
        from discord_bot_standalone import (
            on_ready, on_command_error, help_command, hit_command, 
            dose_command, stash_command, quote_command, agents_command
        )
        
        # Register event handlers and commands
        bot.event(on_ready)
        bot.event(on_command_error)
        bot.command(name="help")(help_command)
        bot.command(name="hit")(hit_command)
        bot.command(name="dose")(dose_command)
        bot.command(name="stash")(stash_command)
        bot.command(name="quote")(quote_command)
        bot.command(name="agents")(agents_command)
        
        logger.info("Bot commands set up successfully")
    except Exception as e:
        logger.error(f"Error setting up bot commands: {e}")
        sys.exit(1)

    # Run the bot
    try:
        logger.info("Starting Discord bot in standalone mode...")
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting standalone Discord bot (no web server)...")
    run_discord_bot()