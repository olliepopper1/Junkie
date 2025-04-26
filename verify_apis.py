#!/usr/bin/env python3
"""
API Verification Script for Trial Junkie
Tests all external API integrations to ensure they are working correctly
"""
import os
import sys
import json
import asyncio
import logging
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("api_verification")

# Load environment variables
load_dotenv()

# Check required environment variables
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
SOLANA_WALLET_ADDRESS = os.getenv("SOLANA_WALLET_ADDRESS", "J5ufWogRFSNYuULDC3EHTAcWYFASnbCo1kVS81eqnwyt")

if not RAPIDAPI_KEY:
    logger.error("RAPIDAPI_KEY not found in environment variables!")
    logger.info("Please set RAPIDAPI_KEY in the .env file")
    sys.exit(1)

if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables!")
    logger.info("Please set DISCORD_BOT_TOKEN in the .env file")
    sys.exit(1)


# Test API Endpoints
async def test_identity_api():
    """Test the random user API for identity generation"""
    logger.info("Testing identity generation API...")
    
    url = "https://random-user-generator.p.rapidapi.com/api"
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "random-user-generator.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Check if the response contains expected fields
        if "results" in data and len(data["results"]) > 0:
            user = data["results"][0]
            if "name" in user and "location" in user and "dob" in user:
                logger.info("✅ Identity API working!")
                logger.info(f"Sample identity: {user['name']['first']} {user['name']['last']}, {user['dob']['age']} years old")
                return True
            else:
                logger.error("❌ Identity API response missing expected fields")
                return False
        else:
            logger.error("❌ Identity API response format unexpected")
            return False
    except Exception as e:
        logger.error(f"❌ Identity API test failed: {str(e)}")
        return False


async def test_card_api():
    """Test the credit card generator API"""
    logger.info("Testing card generation API...")
    
    url = "https://fake-credit-card-generator.p.rapidapi.com/api/fake-credit-card-generator"
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "fake-credit-card-generator.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Check if the response contains expected fields
        if "card" in data and "number" in data["card"] and "expires" in data["card"]:
            logger.info("✅ Card API working!")
            logger.info(f"Sample card: {data['card']['number'][:4]}...{data['card']['number'][-4:]}, Expires: {data['card']['expires']}")
            return True
        else:
            logger.error("❌ Card API response missing expected fields")
            return False
    except Exception as e:
        logger.error(f"❌ Card API test failed: {str(e)}")
        return False


async def test_phone_api():
    """Test the phone number generator API"""
    logger.info("Testing phone generation API...")
    
    url = "https://random-phone-number.p.rapidapi.com/api/phone/random"
    
    querystring = {"country":"US"}
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "random-phone-number.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        
        # Check if the response contains expected fields
        if "phone" in data:
            logger.info("✅ Phone API working!")
            logger.info(f"Sample phone: {data['phone']}")
            return True
        else:
            logger.error("❌ Phone API response missing expected fields")
            return False
    except Exception as e:
        logger.error(f"❌ Phone API test failed: {str(e)}")
        return False


async def test_discord_api():
    """Test the Discord bot token"""
    logger.info("Testing Discord API connection...")
    
    url = "https://discord.com/api/v10/users/@me"
    
    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Check if the response contains expected fields
        if "id" in data and "username" in data:
            logger.info("✅ Discord API working!")
            logger.info(f"Bot connected as: {data['username']}#{data.get('discriminator', '0000')}")
            return True
        else:
            logger.error("❌ Discord API response missing expected fields")
            return False
    except Exception as e:
        logger.error(f"❌ Discord API test failed: {str(e)}")
        return False


async def test_solana_address():
    """Verify the Solana wallet address is valid"""
    logger.info("Verifying Solana wallet address...")
    
    # Basic format check for Solana address (should be base58 encoded, ~44 chars)
    if SOLANA_WALLET_ADDRESS and len(SOLANA_WALLET_ADDRESS) >= 43 and len(SOLANA_WALLET_ADDRESS) <= 45:
        # This is a very basic check - for a real implementation we'd verify it's valid on-chain
        logger.info("✅ Solana wallet address format is valid!")
        logger.info(f"Using wallet address: {SOLANA_WALLET_ADDRESS}")
        return True
    else:
        logger.error("❌ Solana wallet address format appears invalid")
        logger.error(f"Address provided: {SOLANA_WALLET_ADDRESS}")
        return False


async def main():
    """Run all API tests"""
    logger.info("Starting API verification for Trial Junkie...")
    
    # Track test results
    results = {
        "identity_api": await test_identity_api(),
        "card_api": await test_card_api(),
        "phone_api": await test_phone_api(),
        "discord_api": await test_discord_api(),
        "solana_address": await test_solana_address()
    }
    
    # Summary
    logger.info("\n--- API Verification Summary ---")
    all_passed = True
    for test, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"{test}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        logger.info("\n🎯 All API tests passed! Trial Junkie is ready for action.")
        sys.exit(0)
    else:
        logger.error("\n❌ Some API tests failed. Please check the logs above and fix the issues.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())