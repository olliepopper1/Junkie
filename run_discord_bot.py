#!/usr/bin/env python3
"""
Run Discord Bot Script

This script runs the Discord bot and is meant to be executed
from the command line or in a workflow.
"""
import logging
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("discord_bot_workflow.log")
    ]
)
logger = logging.getLogger("discord_bot_workflow")

def main():
    """Main entry point for running the Discord bot"""
    logger.info("Starting Discord bot workflow")
    
    try:
        # Ensure commands directory exists
        os.makedirs("commands", exist_ok=True)
        
        # Run the Discord bot
        logger.info("Launching Discord bot")
        from discord_bot_main import main as bot_main
        result = bot_main()
        
        if result == 0:
            logger.info("Discord bot exited successfully")
        else:
            logger.error(f"Discord bot exited with error code {result}")
        
        return result
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Please make sure discord.py is installed: pip install discord.py")
        return 1
        
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())