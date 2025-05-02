#!/usr/bin/env python3
"""
Test Updated Credit Card API Integration

This script tests the integration with the Random Key credit card generator API
"""
import os
import json
import logging
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_card_api")

def test_random_key_card_api():
    """Test the Random Key credit card generator API"""
    logger.info("Testing Random Key Credit Card Generator API")
    
    # The Random Key credit card generator endpoint
    url = "https://random.api.randomkey.io/v1/ccn"
    
    # Parameters for the API
    params = {
        "records": 1,
        "card_type": "visa",
        "valid": True,
        "luhn": True
    }
    
    # Headers for the request (will need to be replaced with the actual API key)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "api-key": "YOUR_API_KEY_HERE"  # This would need to be replaced with a real API key
    }
    
    try:
        # Make the request
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        # Check the status code
        if response.status_code == 200:
            logger.info("API request successful!")
            
            # Parse the response
            try:
                data = response.json()
                logger.info(f"Response data: {json.dumps(data, indent=2)}")
                
                # Check if the response contains credit card data
                if isinstance(data, list) and len(data) > 0:
                    card = data[0]
                    logger.info("Credit card generated successfully!")
                    logger.info(f"Card Number: {card.get('card_number', 'N/A')}")
                    logger.info(f"Card Type: {card.get('card_type', 'N/A')}")
                    logger.info(f"CVV: {card.get('cvv', 'N/A')}")
                    logger.info(f"Expiry: {card.get('expiry', 'N/A')}")
                    
                    return True
                else:
                    logger.error("Unexpected response format")
                    logger.info(f"Full response: {response.text}")
                    return False
                
            except ValueError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.info(f"Response text: {response.text}")
                return False
                
        else:
            logger.error(f"API request failed with status code: {response.status_code}")
            logger.info(f"Response text: {response.text}")
            return False
            
    except requests.RequestException as e:
        logger.error(f"Request exception: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

def test_with_enhanced_card_generator():
    """Test our enhanced card generator utility"""
    logger.info("Testing enhanced card generator utility")
    
    try:
        # Import the enhanced card generator
        from utils.card_generator import CreditCardGenerator
        
        # Generate cards of different types
        card_types = ["visa", "mastercard", "amex", "discover"]
        
        for card_type in card_types:
            logger.info(f"Generating {card_type} card...")
            card = CreditCardGenerator.generate_card(card_type)
            
            logger.info(f"Card Type: {card.get('card_type', 'N/A')}")
            logger.info(f"Card Number: {card.get('card_number', 'N/A')}")
            logger.info(f"CVV: {card.get('cvv', 'N/A')}")
            logger.info(f"Expiry Month: {card.get('expiry_month', 'N/A')}")
            logger.info(f"Expiry Year: {card.get('expiry_year', 'N/A')}")
            logger.info(f"Cardholder Name: {card.get('cardholder_name', 'N/A')}")
            logger.info("-" * 50)
        
        return True
        
    except ImportError:
        logger.error("Enhanced card generator utility not found")
        return False
    except Exception as e:
        logger.error(f"Error testing enhanced card generator: {e}")
        return False

def test_api_integrations_card_generator():
    """Test the card generator in api_integrations.py"""
    logger.info("Testing APIIntegrations.generate_card()")
    
    try:
        # Import the APIIntegrations class
        from api_integrations import APIIntegrations
        
        # Generate cards of different types
        card_types = ["visa", "mastercard", "amex", "discover"]
        
        for card_type in card_types:
            logger.info(f"Generating {card_type} card...")
            card = APIIntegrations.generate_card(card_type)
            
            logger.info(f"Card Type: {card.get('card_type', 'N/A')}")
            logger.info(f"Card Number: {card.get('card_number', 'N/A')}")
            logger.info(f"CVV: {card.get('cvv', 'N/A')}")
            logger.info(f"Expiry Month: {card.get('expiry_month', 'N/A')}")
            logger.info(f"Expiry Year: {card.get('expiry_year', 'N/A')}")
            logger.info(f"Cardholder Name: {card.get('cardholder_name', 'N/A')}")
            logger.info("-" * 50)
        
        return True
        
    except ImportError:
        logger.error("APIIntegrations class not found")
        return False
    except Exception as e:
        logger.error(f"Error testing APIIntegrations.generate_card(): {e}")
        return False

def main():
    """Run the test suite"""
    logger.info("Starting credit card API tests")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    results = {
        "random_key_api": "skipped",  # Skip by default as it requires an API key
        "enhanced_card_generator": test_with_enhanced_card_generator(),
        "api_integrations": test_api_integrations_card_generator()
    }
    
    # Only test the Random Key API if an API key is provided
    if os.getenv("RANDOM_KEY_API_KEY"):
        results["random_key_api"] = test_random_key_card_api()
    
    # Print summary
    logger.info("=== Test Results ===")
    for test_name, result in results.items():
        logger.info(f"{test_name}: {'SUCCESS' if result is True else 'FAILED' if result is False else 'SKIPPED'}")
    
    # Save results to file
    with open(f"card_api_test_results_{timestamp}.json", "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Results saved to card_api_test_results_{timestamp}.json")

if __name__ == "__main__":
    main()