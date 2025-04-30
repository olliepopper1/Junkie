#!/usr/bin/env python3
"""
Test API Keys
Simple script to test that all the API keys are properly set
"""
import os
import json
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_api_keys")

def check_api_keys():
    """Check that all required API keys are set"""
    # Load environment variables
    load_dotenv()
    
    # API keys to check
    api_keys = {
        "DISCORD_BOT_TOKEN": os.getenv("DISCORD_BOT_TOKEN", ""),
        "RAPIDAPI_KEY": os.getenv("RAPIDAPI_KEY", ""),
        "PERSONATOR_API_KEY": os.getenv("PERSONATOR_API_KEY", os.getenv("RAPIDAPI_KEY", "")),
        "VIRTUAL_NUMBER_API_KEY": os.getenv("VIRTUAL_NUMBER_API_KEY", os.getenv("RAPIDAPI_KEY", "")),
        "FAKE_CARD_API_KEY": os.getenv("FAKE_CARD_API_KEY", os.getenv("RAPIDAPI_KEY", "")),
        "VIRTUAL_CARD_API_KEY": os.getenv("VIRTUAL_CARD_API_KEY", os.getenv("RAPIDAPI_KEY", "")),
        "TEMP_EMAIL_API_KEY": os.getenv("TEMP_EMAIL_API_KEY", os.getenv("RAPIDAPI_KEY", "")),
        "TEMP_MAIL_BACKUP_API_KEY": os.getenv("TEMP_MAIL_BACKUP_API_KEY", os.getenv("RAPIDAPI_KEY", ""))
    }
    
    # Check each key
    missing_keys = []
    set_keys = []
    
    for key, value in api_keys.items():
        if not value:
            missing_keys.append(key)
        else:
            # Only show the first few characters of the key for security
            masked_value = value[:4] + "..." + value[-4:] if len(value) > 10 else "***" 
            set_keys.append(f"{key}: {masked_value}")
    
    # Print results
    logger.info("API Key Check Results:")
    
    if missing_keys:
        logger.warning(f"Missing API Keys: {', '.join(missing_keys)}")
    else:
        logger.info("All required API keys are set")
    
    logger.info(f"Set API Keys: {len(set_keys)}")
    for key_info in set_keys:
        logger.info(f"  - {key_info}")
    
    return not missing_keys

if __name__ == "__main__":
    logger.info("Starting API key check...")
    all_keys_set = check_api_keys()
    
    if all_keys_set:
        logger.info("All API keys are set correctly!")
    else:
        logger.warning("Some API keys are missing. Check logs for details.")