#!/usr/bin/env python3
"""
Run Discord Integration
This script runs the integrated Discord bot for the Trial Junkie system
"""
import os
import sys
import logging
import traceback
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_integration.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("discord_integration")

def main():
    """Main function"""
    logger.info("Starting Trial Junkie Discord integration")
    start_time = datetime.now()
    
    try:
        # Import the integrated Discord bot
        from integrated_discord_bot import IntegratedBot
        
        # Create and run the bot
        bot = IntegratedBot()
        result = bot.run()
        
        if result:
            logger.info("Discord bot ran successfully")
        else:
            logger.error("Discord bot failed to run")
    
    except Exception as e:
        logger.error(f"Error running Discord integration: {str(e)}")
        traceback.print_exc()
        return 1
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    logger.info(f"Discord integration completed in {duration:.2f} seconds")
    return 0

if __name__ == "__main__":
    sys.exit(main())