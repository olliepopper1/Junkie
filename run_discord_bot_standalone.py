#!/usr/bin/env python3
"""
Discord Bot Runner for Trial Junkie
Run this script to start the Discord bot without Flask dependencies
"""
import os
import sys
import logging
import subprocess
import signal
import time
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot_output.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("discord_bot_runner")

# Load environment variables
load_dotenv()

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import discord
        logger.info(f"Discord.py version: {discord.__version__}")
        return True
    except ImportError:
        logger.error("Discord.py is not installed. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "discord.py"], check=True)
            logger.info("Discord.py installed successfully")
            return True
        except subprocess.CalledProcessError:
            logger.error("Failed to install discord.py")
            return False

def start_bot():
    """Start the Discord bot process"""
    logger.info("Starting Discord bot...")
    
    # Check if the bot token is available
    if not os.getenv('DISCORD_BOT_TOKEN'):
        logger.error("DISCORD_BOT_TOKEN not found in environment variables")
        return False
    
    try:
        # Start the bot in a new process
        process = subprocess.Popen(
            [sys.executable, "pure_discord_bot.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        logger.info(f"Bot started with PID {process.pid}")
        
        # Monitor the bot process
        try:
            while True:
                output = process.stdout.readline()
                if output:
                    logger.info(output.strip())
                
                error = process.stderr.readline()
                if error:
                    logger.error(error.strip())
                
                # Check if process has terminated
                if process.poll() is not None:
                    logger.error(f"Bot process terminated with exit code {process.returncode}")
                    remaining_output, remaining_error = process.communicate()
                    
                    if remaining_output:
                        logger.info(remaining_output.strip())
                    if remaining_error:
                        logger.error(remaining_error.strip())
                    
                    break
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, stopping bot...")
            process.terminate()
            process.wait(timeout=5)
            logger.info("Bot stopped successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        return False

def main():
    """Main function to run the bot"""
    logger.info("Discord Bot Runner starting...")
    
    if not check_dependencies():
        logger.error("Required dependencies not satisfied")
        return False
    
    return start_bot()

if __name__ == "__main__":
    main()