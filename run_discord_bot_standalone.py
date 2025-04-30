#!/usr/bin/env python3
"""
Standalone Discord Bot Runner
This script ensures no Flask dependencies are imported
"""
import os
import sys
import subprocess
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot_standalone.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("discord_bot_standalone")

def main():
    """Run the Discord bot in a completely separate process"""
    logger.info("Starting standalone Discord bot runner...")
    
    # Set environmental variables to prevent Flask from being imported
    env = os.environ.copy()
    env['NO_FLASK'] = '1'
    env['PYTHONPATH'] = os.getcwd()
    
    try:
        # Launch the standalone Discord bot in a subprocess
        logger.info("Launching pure_discord_bot.py...")
        with subprocess.Popen(
            [sys.executable, "pure_discord_bot.py"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        ) as process:
            # Read and log output from the bot
            logger.info("Discord bot process started with PID: %d", process.pid)
            
            # Log each line of output from the bot process
            for line in process.stdout:
                line = line.strip()
                if line:
                    logger.info("Bot output: %s", line)
            
            # Wait for process to finish
            return_code = process.wait()
            if return_code != 0:
                logger.error("Discord bot process exited with code: %d", return_code)
                return 1
            else:
                logger.info("Discord bot process completed successfully")
                return 0
                
    except Exception as e:
        logger.error("Error running Discord bot: %s", str(e))
        return 1

if __name__ == "__main__":
    sys.exit(main())
