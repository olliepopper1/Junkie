#!/usr/bin/env python3
"""
Test Credit Card API Endpoints
Test the updated credit card generation APIs
"""
import json
import os
import logging

from api_integrations import APIIntegrations

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def test_credit_card_api():
    """Test the primary and backup credit card APIs"""
    logger.info("Testing credit card API endpoints...")
    
    # Test for different card types
    card_types = ["visa", "mastercard", "amex"]
    
    for card_type in card_types:
        logger.info(f"Generating card of type: {card_type}")
        card_info = APIIntegrations.generate_card(card_type)
        
        # Check if we got a card number
        if card_info and card_info.get("card_number"):
            logger.info(f"✓ Successfully generated {card_type} card: {card_info['card_number'][:6]}******")
            logger.info(f"  → Card details: CVV: {card_info.get('cvv', 'N/A')}, Expiry: {card_info.get('expiry_month', '')} / {card_info.get('expiry_year', '')}")
        else:
            logger.error(f"✗ Failed to generate {card_type} card: {card_info}")
    
    logger.info("Credit card API test completed.")

def test_virtual_card_api():
    """Test the virtual card API"""
    logger.info("Testing virtual card API endpoint...")
    
    # Test with different amounts
    amounts = [0.00, 10.00, 50.00]
    currencies = ["USD", "EUR"]
    
    for amount in amounts:
        for currency in currencies:
            logger.info(f"Generating virtual card with {amount} {currency}")
            card_info = APIIntegrations.generate_virtual_card(amount, currency)
            
            # Check if we got a card number
            if card_info and card_info.get("card_number"):
                logger.info(f"✓ Successfully generated virtual card: {card_info['card_number'][:6]}******")
                logger.info(f"  → Virtual card details: Amount: {card_info.get('amount', 'N/A')} {card_info.get('currency', 'USD')}")
                logger.info(f"  → CVV: {card_info.get('cvv', 'N/A')}, Expiry: {card_info.get('expiry', 'N/A')}")
            else:
                logger.error(f"✗ Failed to generate virtual card: {card_info}")
    
    logger.info("Virtual card API test completed.")

def main():
    """Main function"""
    logger.info("Starting API test...")
    
    test_credit_card_api()
    print("\n" + "-" * 50 + "\n")
    test_virtual_card_api()
    
    logger.info("API test completed.")

if __name__ == "__main__":
    main()