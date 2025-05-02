#!/usr/bin/env python3
"""
Main Discord Bot Runner
Starts the updated Discord bot for Trial Junkie
"""
import os
import sys
import logging
import subprocess
import asyncio
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("main_discord_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("main_discord_bot")

# Load environment variables
load_dotenv()

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        # Check for discord.py
        import discord
        logger.info(f"Discord.py version: {discord.__version__}")
        
        # Check for selenium
        import selenium
        logger.info(f"Selenium version: {selenium.__version__}")
        
        # Check for requests
        import requests
        logger.info(f"Requests version: {requests.__version__}")
        
        return True
    except ImportError as e:
        logger.error(f"Required dependency not installed: {str(e)}")
        return False

def check_api_keys():
    """Check if required API keys are set"""
    # Check Discord bot token
    discord_token = os.getenv('DISCORD_BOT_TOKEN')
    if not discord_token:
        logger.error("DISCORD_BOT_TOKEN not found in environment variables")
        return False
    
    # Check RapidAPI key
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    if not rapidapi_key:
        logger.error("RAPIDAPI_KEY not found in environment variables")
        return False
    
    logger.info("All required API keys are set")
    return True

def test_api_connection():
    """Test a basic API connection to RapidAPI"""
    try:
        import requests
        
        # Get the RapidAPI key
        rapidapi_key = os.getenv('RAPIDAPI_KEY')
        
        # Test a simple API call (Veriphone API)
        url = "https://veriphone.p.rapidapi.com/verify"
        
        querystring = {"phone":"2125551234"}
        
        headers = {
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": "veriphone.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            logger.info("Successfully connected to RapidAPI")
            return True
        else:
            logger.error(f"Failed to connect to RapidAPI: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error testing API connection: {str(e)}")
        return False

async def start_bot():
    """Start the Discord bot"""
    try:
        # Import the bot
        from updated_discord_bot import main
        
        logger.info("Starting Discord bot")
        await main()
        return True
    except Exception as e:
        logger.error(f"Error starting Discord bot: {str(e)}")
        return False

def main():
    """Main function"""
    logger.info("Starting Trial Junkie Discord Bot")
    
    # Check if dependencies are installed
    if not check_dependencies():
        logger.error("Required dependencies not satisfied")
        return False
    
    # Check if API keys are set
    if not check_api_keys():
        logger.error("Required API keys not configured")
        return False
    
    # Test API connection
    if not test_api_connection():
        logger.warning("API connection test failed - bot may not function correctly")
    
    # Run the bot
    asyncio.run(start_bot())
    return True

if __name__ == "__main__":
    main()