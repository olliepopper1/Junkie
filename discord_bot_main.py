#!/usr/bin/env python3
"""
Discord Bot Main Entry Point
A standalone version that doesn't conflict with the Flask web server
"""
import os
import sys
import logging
from dotenv import load_dotenv
import discord_workflow

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("discord_bot.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger("discord_bot_main")
    
    # Check if Discord token is available
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        logger.error("DISCORD_BOT_TOKEN not found in environment variables")
        sys.exit(1)
        
    logger.info("Starting Discord Bot...")
    try:
        # Run the Discord workflow module directly
        discord_workflow.bot.run(token)
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)