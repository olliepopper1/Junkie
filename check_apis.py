#!/usr/bin/env python3
"""
Check if RapidAPI endpoints are working correctly
Tests all configured API endpoints and validates responses
"""
import os
import json
import logging
import asyncio
import aiohttp
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("check_apis")

# Load environment variables
load_dotenv()

# API keys
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '')

# Test endpoints
TEST_ENDPOINTS = {
    "personator": {
        "url": "https://personator.p.rapidapi.com/v1/status",
        "host": "personator.p.rapidapi.com"
    },
    "virtual_number": {
        "url": "https://virtual-number.p.rapidapi.com/v1/status",
        "host": "virtual-number.p.rapidapi.com"
    },
    "fake_card": {
        "url": "https://fake-valid-cc-data-generator.p.rapidapi.com/v1/status",
        "host": "fake-valid-cc-data-generator.p.rapidapi.com"
    },
    "virtual_card": {
        "url": "https://free-trial-virtual-card-issuing.p.rapidapi.com/v1/status",
        "host": "free-trial-virtual-card-issuing.p.rapidapi.com"
    },
    "temp_email": {
        "url": "https://fast-reliable-disposable-mx-email-checker.p.rapidapi.com/v1/status",
        "host": "fast-reliable-disposable-mx-email-checker.p.rapidapi.com"
    }
}

async def test_api_endpoint(name, url):
    """Test if an API endpoint is working properly"""
    logger.info(f"Testing {name} API...")
    
    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': TEST_ENDPOINTS[name]['host']
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"{name} API is working. Status: {response.status}")
                    return True, f"✅ {name}: OK (200)"
                else:
                    logger.warning(f"{name} API returned status code: {response.status}")
                    text = await response.text()
                    return False, f"❌ {name}: Failed ({response.status}) - {text[:100]}"
    except Exception as e:
        logger.error(f"Error testing {name} API: {e}")
        return False, f"❌ {name}: Error - {str(e)[:100]}"

async def test_endpoints():
    """Test all configured API endpoints"""
    if not RAPIDAPI_KEY:
        logger.error("RAPIDAPI_KEY not set. Cannot test endpoints.")
        return [False, "❌ RAPIDAPI_KEY not set. Please set it in .env file."]
    
    results = []
    
    for name, config in TEST_ENDPOINTS.items():
        success, message = await test_api_endpoint(name, config['url'])
        results.append(message)
    
    return results

async def main():
    """Run the test and output results"""
    logger.info("Starting API endpoint test...")
    
    results = await test_endpoints()
    
    logger.info("API Test Results:")
    for result in results:
        logger.info(result)
    
    logger.info("API endpoint test completed.")

if __name__ == "__main__":
    asyncio.run(main())