"""
Check if RapidAPI endpoints are working correctly
Tests all configured API endpoints and validates responses
"""
import os
import sys
import json
import aiohttp
import asyncio
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import the configuration
from config import ENDPOINTS, API_HOSTS, DEFAULT_HEADERS, RAPIDAPI_KEY

async def test_api_endpoint(name, url):
    """Test if an API endpoint is working properly"""
    headers = DEFAULT_HEADERS.copy()
    
    # Add RapidAPI key if this endpoint is hosted on RapidAPI
    host = API_HOSTS.get(name)
    if host and host.endswith('rapidapi.com'):
        headers['X-RapidAPI-Key'] = RAPIDAPI_KEY
        headers['X-RapidAPI-Host'] = host
    
    try:
        async with aiohttp.ClientSession() as session:
            logger.info(f"Testing endpoint: {name} - {url}")
            async with session.get(url, headers=headers) as response:
                status = response.status
                
                if status == 200:
                    data = await response.text()
                    try:
                        # Try to parse as JSON
                        json_data = json.loads(data)
                        logger.info(f"✅ {name}: Success (200) - JSON response")
                        return True, f"Success: {len(str(json_data))} bytes of JSON"
                    except json.JSONDecodeError:
                        # Not JSON but still successful
                        logger.info(f"✅ {name}: Success (200) - non-JSON response")
                        return True, f"Success: {len(data)} bytes of text"
                else:
                    error_text = await response.text()
                    logger.error(f"❌ {name}: Failed ({status}) - {error_text[:100]}...")
                    return False, f"Error {status}: {error_text[:100]}..."
    except Exception as e:
        logger.error(f"❌ {name}: Exception - {str(e)}")
        return False, f"Exception: {str(e)}"

async def test_endpoints():
    """Test all configured API endpoints"""
    logger.info(f"Testing {len(ENDPOINTS)} API endpoints")
    logger.info(f"RapidAPI Key: {'Available' if RAPIDAPI_KEY else 'Missing'}")
    
    results = {}
    for name, url in ENDPOINTS.items():
        success, message = await test_api_endpoint(name, url)
        results[name] = {
            "url": url,
            "success": success,
            "message": message,
            "host": API_HOSTS.get(name, "direct")
        }
    
    return results

async def main():
    """Run the test and output results"""
    print(f"\n========= API ENDPOINT TEST =========\n")
    
    # Print environment info
    print(f"RapidAPI Key: {'✅ Available' if RAPIDAPI_KEY else '❌ Missing'}")
    print(f"Number of Endpoints: {len(ENDPOINTS)}")
    print(f"Default Headers: {DEFAULT_HEADERS}")
    print("\n")
    
    # Test the endpoints
    results = await test_endpoints()
    
    # Print summary
    success_count = sum(1 for r in results.values() if r['success'])
    print(f"\n========= SUMMARY =========")
    print(f"Success: {success_count}/{len(results)} endpoints")
    print(f"Failure: {len(results) - success_count}/{len(results)} endpoints")
    print("\n========= DETAILS =========")
    
    # Print details of each endpoint
    for name, result in results.items():
        status = "✅" if result['success'] else "❌"
        print(f"{status} {name} ({result['host']}):")
        print(f"    URL: {result['url']}")
        print(f"    Result: {result['message']}")
        print("")
    
    # Check connections to agent APIs
    print("\n========= AGENT API CONNECTIONS =========")
    agent_apis = {
        "Heroin Harry (Identity)": ["random_user", "random_address"],
        "Meth Mandy (Card)": ["fake_card", "random_bank"],
        "Xanny Xan (Email)": ["temp_email", "random_user"],
        "Cokehead Carl (Phone)": ["random_phone"],
        "Shroomy Sal (Automation)": []  # No direct APIs, uses browser automation
    }
    
    for agent, apis in agent_apis.items():
        if not apis:
            print(f"{agent}: No direct API connections (uses other methods)")
            continue
            
        api_statuses = [results.get(api, {}).get('success', False) for api in apis]
        if all(api_statuses):
            print(f"✅ {agent}: All APIs working ({', '.join(apis)})")
        elif any(api_statuses):
            working = [apis[i] for i, status in enumerate(api_statuses) if status]
            failed = [apis[i] for i, status in enumerate(api_statuses) if not status]
            print(f"⚠️ {agent}: Partially working - OK: {', '.join(working)} | Failed: {', '.join(failed)}")
        else:
            print(f"❌ {agent}: All APIs failed ({', '.join(apis)})")

if __name__ == "__main__":
    asyncio.run(main())