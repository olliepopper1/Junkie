#!/usr/bin/env python3
"""
Discord Bot Workflow Runner
This script is specifically designed to work with the Replit 'discord_bot' workflow
It runs the Discord bot without any Flask dependencies
"""
import os
import sys
import logging
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("discord_bot_workflow")

def main():
    """Run the Discord bot directly"""
    logger.info("Starting Discord bot workflow runner...")
    
    # Set environment variables to prevent Flask conflicts
    os.environ['NO_FLASK'] = '1'
    os.environ['NO_WEB_APP'] = '1'
    os.environ['DISCORD_BOT_ONLY'] = '1'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    # Run the standalone bot script directly using subprocess
    # This avoids any potential import conflicts with Flask
    logger.info("Launching standalone bot process...")
    
    try:
        # Execute the standalone bot as a separate process
        process = subprocess.Popen(
            ["python", "-u", "standalone_bot.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            env=os.environ.copy()
        )
        
        # Stream output
        for line in process.stdout:
            print(line, end='')
            sys.stdout.flush()
            
        # Wait for the process to finish
        return_code = process.wait()
        if return_code != 0:
            logger.error(f"Bot process exited with code {return_code}")
            return return_code
            
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())