#!/usr/bin/env python3
"""
Discord Bot Workflow Runner
This script is specifically designed to work with the Replit 'discord_bot' workflow
It runs the Discord bot without any Flask dependencies
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("discord_bot_workflow")

# Main function
def main():
    """Run the Discord bot directly"""
    logger.info("Starting Discord Bot Workflow Runner...")
    
    try:
        # Import our pure Discord bot without importing any Flask dependencies
        # Set environment variables to prevent Flask conflicts
        os.environ['NO_FLASK'] = '1'
        os.environ['FLASK_PORT'] = '5001'  # Use a different port if Flask is used
        os.environ['PORT'] = '5001'  # For applications that check PORT directly
        
        # Run the Discord bot directly
        logger.info("Executing pure Discord bot implementation...")
        os.system("python pure_discord_bot.py")
    except Exception as e:
        logger.error(f"Error in Discord Bot Workflow Runner: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()