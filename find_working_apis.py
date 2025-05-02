#!/usr/bin/env python3
"""
API Endpoint Finder
Searches for working API endpoints from a list of potential candidates
"""
import os
import json
import time
import logging
import requests
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Get the RapidAPI key from environment variables
RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')

# List of potential credit card API endpoints to check
CARD_API_HOSTS = [
    "credit-card-generator2.p.rapidapi.com",
    "generator-credit-card.p.rapidapi.com",
    "creditcards.p.rapidapi.com",
    "random-data-api.p.rapidapi.com",
    "credit-card-checker.p.rapidapi.com",
    "credit-card-generator-faker.p.rapidapi.com",
    "bin-ip-checker.p.rapidapi.com",
    "luhn-validator.p.rapidapi.com",
    "fake-credit-card-generator.p.rapidapi.com",
    "valfirm-bin-and-credit-card-validation.p.rapidapi.com",
    "credit-card-numbers.p.rapidapi.com",
    "verified-creditcard.p.rapidapi.com",
    "namso-ccgen.p.rapidapi.com",
    "cardgenerator.p.rapidapi.com",
    "creditcardgenerator.p.rapidapi.com"
]

def check_api_endpoint(host, endpoint=None):
    """Test if a RapidAPI endpoint is working"""
    if not endpoint:
        # Generate a standard endpoint URL if none provided
        if "generator" in host or "creditcard" in host:
            endpoint = f"https://{host}/generate"
        elif "validator" in host or "checker" in host:
            endpoint = f"https://{host}/validate"
        else:
            endpoint = f"https://{host}/api"
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": host
    }
    
    # Some common query parameters for credit card APIs
    params = {
        "type": "visa",
        "card_type": "visa",
        "brand": "visa",
        "limit": "1"
    }
    
    try:
        logger.info(f"Testing endpoint: {endpoint}")
        response = requests.get(endpoint, headers=headers, params=params, timeout=5)
        
        # Check if the response indicates we're not subscribed
        response_text = response.text.lower()
        if "not subscribed" in response_text or "doesn't exist" in response_text:
            logger.warning(f"✗ API not accessible: {host}")
            return {
                "host": host,
                "endpoint": endpoint,
                "status": "not_subscribed",
                "status_code": response.status_code,
                "message": response.text
            }
            
        # Check status code
        if response.status_code >= 400:
            logger.warning(f"✗ API error: {host} - Status Code: {response.status_code}")
            return {
                "host": host,
                "endpoint": endpoint,
                "status": "error",
                "status_code": response.status_code,
                "message": response.text
            }
        
        # Try to parse response as JSON
        try:
            data = response.json()
            logger.info(f"✓ API working: {host}")
            return {
                "host": host,
                "endpoint": endpoint,
                "status": "working",
                "status_code": response.status_code,
                "data": data
            }
        except ValueError:
            logger.warning(f"✗ API returned non-JSON: {host}")
            return {
                "host": host,
                "endpoint": endpoint,
                "status": "invalid_response",
                "status_code": response.status_code,
                "message": response.text[:100]  # First 100 chars of response
            }
            
    except requests.Timeout:
        logger.warning(f"✗ API timeout: {host}")
        return {
            "host": host,
            "endpoint": endpoint,
            "status": "timeout"
        }
    except requests.ConnectionError:
        logger.warning(f"✗ API connection error: {host}")
        return {
            "host": host,
            "endpoint": endpoint,
            "status": "connection_error"
        }
    except Exception as e:
        logger.error(f"✗ API unexpected error: {host} - {str(e)}")
        return {
            "host": host,
            "endpoint": endpoint,
            "status": "error",
            "message": str(e)
        }

def main():
    """Check all API endpoints and report results"""
    if not RAPIDAPI_KEY:
        logger.error("No RAPIDAPI_KEY found in environment variables")
        return
    
    logger.info(f"Testing {len(CARD_API_HOSTS)} credit card API endpoints...")
    
    results = []
    
    # Use multithreading to check endpoints faster
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        
        # Submit all tasks
        for host in CARD_API_HOSTS:
            futures.append(executor.submit(check_api_endpoint, host))
        
        # Wait for tasks to complete
        for future in futures:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"Error getting result: {e}")
    
    # Organize results by status
    working_apis = [api for api in results if api.get("status") == "working"]
    error_apis = [api for api in results if api.get("status") == "error"]
    not_subscribed = [api for api in results if api.get("status") == "not_subscribed"]
    other_issues = [api for api in results if api.get("status") not in ("working", "error", "not_subscribed")]
    
    # Print summary
    logger.info("=== API Testing Results ===")
    logger.info(f"Total APIs tested: {len(results)}")
    logger.info(f"Working APIs: {len(working_apis)}")
    logger.info(f"Error APIs: {len(error_apis)}")
    logger.info(f"Not Subscribed: {len(not_subscribed)}")
    logger.info(f"Other Issues: {len(other_issues)}")
    
    # Print working APIs
    if working_apis:
        logger.info("\n=== Working APIs ===")
        for api in working_apis:
            logger.info(f"Host: {api['host']}")
            logger.info(f"Endpoint: {api['endpoint']}")
            logger.info(f"Status Code: {api['status_code']}")
            logger.info("-" * 50)
    
    # Save results to file for reference
    timestamp = int(time.time())
    filename = f"api_test_results_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Results saved to {filename}")

if __name__ == "__main__":
    main()