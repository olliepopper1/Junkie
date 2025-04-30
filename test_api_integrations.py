#!/usr/bin/env python3
"""
Test API Integrations
Simple script to test the API integrations for Trial Junkie
"""
import os
import json
import logging
from api_integrations import APIIntegrations

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_api_integrations")

def test_identity_generation():
    """Test identity generation"""
    logger.info("Testing identity generation...")
    identity = APIIntegrations.generate_identity()
    logger.info(f"Generated identity: {json.dumps(identity, indent=2)}")
    return identity

def test_virtual_number_generation():
    """Test virtual number generation"""
    logger.info("Testing virtual number generation...")
    phone = APIIntegrations.generate_virtual_number()
    logger.info(f"Generated virtual number: {json.dumps(phone, indent=2)}")
    return phone

def test_card_generation():
    """Test card generation"""
    logger.info("Testing card generation...")
    card = APIIntegrations.generate_card()
    logger.info(f"Generated card: {json.dumps(card, indent=2)}")
    return card

def test_virtual_card_generation():
    """Test virtual card generation"""
    logger.info("Testing virtual card generation...")
    virtual_card = APIIntegrations.generate_virtual_card()
    logger.info(f"Generated virtual card: {json.dumps(virtual_card, indent=2)}")
    return virtual_card

def test_email_generation():
    """Test email generation"""
    logger.info("Testing email generation...")
    email = APIIntegrations.generate_email()
    logger.info(f"Generated email: {json.dumps(email, indent=2)}")
    return email

def test_complete_trial_data():
    """Test complete trial data generation"""
    logger.info("Testing complete trial data generation...")
    trial_data = APIIntegrations.generate_complete_trial_data("netflix")
    logger.info(f"Generated complete trial data: {json.dumps(trial_data, indent=2)}")
    return trial_data

def run_all_tests():
    """Run all tests"""
    logger.info("Running all API integration tests...")
    
    # Test all APIs
    test_identity_generation()
    test_virtual_number_generation()
    test_card_generation()
    test_virtual_card_generation()
    test_email_generation()
    test_complete_trial_data()
    
    logger.info("All tests completed!")

if __name__ == "__main__":
    logger.info("Starting API integration tests...")
    
    # Check if RAPIDAPI_KEY is set
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        logger.warning("RAPIDAPI_KEY environment variable is not set. Using fallback methods.")
    
    # Run tests
    run_all_tests()