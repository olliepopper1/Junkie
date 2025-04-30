#!/usr/bin/env python3
"""
Dedicated workflow script for Discord bot
Avoids any Flask imports completely
"""
import os
import sys
import logging
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_workflow.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("discord_workflow")

def main():
    """Run the standalone Discord bot"""
    logger.info("Starting Discord workflow runner...")
    
    # Set environment variables to prevent Flask conflicts
    os.environ['NO_FLASK'] = '1'
    os.environ['NO_WEB_APP'] = '1'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    try:
        # Execute the pure standalone Discord bot implementation
        logger.info("Executing pure Discord bot...")
        
        # Import only what's needed for the Discord bot
        # This avoids any Flask app imports
        from pure_discord_bot import run_bot
        
        # Run the bot function directly
        run_bot()
        
        return 0
    except Exception as e:
        logger.error(f"Error in Discord workflow: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
