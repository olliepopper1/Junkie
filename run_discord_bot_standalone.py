#!/usr/bin/env python3
"""
Discord Bot Runner - Standalone Version
Run this script directly to start the Discord bot without Flask
"""
import sys
import logging
import discord_bot_standalone

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

if __name__ == "__main__":
    logger.info("Starting standalone Discord bot...")
    try:
        # Run the main function from the standalone module
        discord_bot_standalone.main()
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)