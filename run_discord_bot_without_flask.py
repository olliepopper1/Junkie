#!/usr/bin/env python3
"""
Discord Bot Runner - No Flask Version
Run this script directly to start the Discord bot without Flask
This script avoids port conflicts with the main web application
"""
import os
import sys
import logging
import discord
from dotenv import load_dotenv
from discord_bot_standalone import main as discord_main

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

# Check for Discord token
if not os.getenv('DISCORD_BOT_TOKEN'):
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

if __name__ == "__main__":
    logger.info("Starting standalone Discord bot (no Flask)...")
    try:
        # Run the main function from the standalone module
        discord_main()
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)