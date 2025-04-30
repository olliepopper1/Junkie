#!/usr/bin/env python3
"""
Completely Standalone Discord Bot Runner
This implementation ensures no Flask app is imported at all
"""
import os
import sys
import subprocess
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot_fixed.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("discord_bot_runner_fixed")

# This script's path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    """Run the Discord bot in a completely isolated environment"""
    logger.info("Starting fixed standalone Discord bot runner...")
    
    # Create a clean environment for the subprocess
    env = os.environ.copy()
    env['NO_FLASK'] = '1'  # Flag to prevent Flask imports
    env['NO_WEB_APP'] = '1'  # Additional flag
    env['PYTHONPATH'] = SCRIPT_DIR  # Set Python path to our directory
    env['PYTHONUNBUFFERED'] = '1'  # Ensure unbuffered output
    
    # Command to run the pure Discord bot implementation
    # We use a subprocess to completely isolate it
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, "pure_discord_bot.py")]
    
    logger.info(f"Launching command: {' '.join(cmd)}")
    
    try:
        # Launch the subprocess with the isolated environment
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=SCRIPT_DIR
        )
        
        logger.info(f"Bot process started with PID: {process.pid}")
        
        # Stream and log output from the bot process
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
                
            line = line.strip()
            if line:
                logger.info(f"Bot: {line}")
        
        # Process has finished
        return_code = process.poll()
        if return_code != 0:
            logger.error(f"Discord bot process exited with code: {return_code}")
            return 1
        else:
            logger.info("Discord bot process completed successfully")
            return 0
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, stopping bot...")
        if 'process' in locals():
            process.terminate()
            process.wait(timeout=5)
        return 0
    except Exception as e:
        logger.error(f"Error running Discord bot: {str(e)}")
        return 1

if __name__ == "__main__":
    # Run the Discord bot and exit with its status code
    sys.exit(main())