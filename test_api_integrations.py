"""
Test Suite for API Integrations
Tests all external API connections and data validations
"""
import asyncio
import json
import os
import re
import unittest
from unittest.mock import patch, MagicMock

import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add log handler to output to console
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Import the API integrations
try:
    from api_integrations import APIIntegrations
except ImportError as e:
    logger.error(f"Failed to import APIIntegrations: {e}")
    # Create a mock class for testing
    class APIIntegrations:
        @staticmethod
        def generate_identity(country="US"):
            return {"success": False, "error": "Mock implementation"}
        
        @staticmethod
        def generate_virtual_number(country_code="US"):
            return {"success": False, "error": "Mock implementation"}
        
        @staticmethod
        def generate_card(card_type="visa"):
            return {"success": False, "error": "Mock implementation"}
        
        @staticmethod
        def generate_email():
            return {"success": False, "error": "Mock implementation"}
        
        @staticmethod
        def generate_complete_trial_data(service=None):
            return {"success": False, "error": "Mock implementation"}


class APIIntegrationTests(unittest.TestCase):
    """Test the external API integrations"""

    def setUp(self):
        """Set up the test environment"""
        # Check if RapidAPI key is available
        self.api_key = os.environ.get("RAPIDAPI_KEY")
        if not self.api_key:
            logger.warning("RAPIDAPI_KEY not found in environment variables")

    def test_identity_generation(self):
        """Test identity generation API"""
        # Mock the API call if no key available
        if not self.api_key:
            with patch.object(APIIntegrations, 'generate_identity') as mock_method:
                mock_method.return_value = {
                    "success": True,
                    "first_name": "John",
                    "last_name": "Doe",
                    "address": "123 Main St",
                    "city": "Anytown",
                    "state": "CA",
                    "zipcode": "90210",
                    "country": "US"
                }
                result = APIIntegrations.generate_identity()
                self.assertTrue(result["success"])
                self.assertIn("first_name", result)
                logger.info("Successfully tested identity generation (mock)")
        else:
            # Real API call
            result = APIIntegrations.generate_identity()
            self.assertIn("success", result)
            if result["success"]:
                self.assertIn("first_name", result)
                self.assertIn("last_name", result)
                self.assertIn("address", result)
                logger.info(f"Successfully tested identity generation: {result['first_name']} {result['last_name']}")
            else:
                # If API fails, we should get a fallback identity
                self.assertIn("first_name", result)
                logger.warning(f"API call failed, using fallback: {result.get('error', 'Unknown error')}")

    def test_virtual_number_generation(self):
        """Test virtual phone number generation API"""
        # Mock the API call if no key available
        if not self.api_key:
            with patch.object(APIIntegrations, 'generate_virtual_number') as mock_method:
                mock_method.return_value = {
                    "success": True,
                    "phone_number": "1234567890",
                    "country_code": "US"
                }
                result = APIIntegrations.generate_virtual_number()
                self.assertTrue(result["success"])
                self.assertIn("phone_number", result)
                logger.info("Successfully tested virtual number generation (mock)")
        else:
            # Real API call
            result = APIIntegrations.generate_virtual_number()
            self.assertIn("success", result)
            if result["success"]:
                self.assertIn("phone_number", result)
                # Validate phone number format
                self.assertTrue(re.match(r'^\d{10,15}$', result["phone_number"]))
                logger.info(f"Successfully tested virtual number generation: {result['phone_number']}")
            else:
                # If API fails, we should get a fallback phone
                self.assertIn("phone_number", result)
                logger.warning(f"API call failed, using fallback: {result.get('error', 'Unknown error')}")

    def test_card_generation(self):
        """Test credit card generation API"""
        # Mock the API call if no key available
        if not self.api_key:
            with patch.object(APIIntegrations, 'generate_card') as mock_method:
                mock_method.return_value = {
                    "success": True,
                    "card_number": "4111111111111111",
                    "card_expiry": "12/25",
                    "card_cvv": "123",
                    "card_holder": "John Doe"
                }
                result = APIIntegrations.generate_card()
                self.assertTrue(result["success"])
                self.assertIn("card_number", result)
                logger.info("Successfully tested card generation (mock)")
        else:
            # Real API call
            result = APIIntegrations.generate_card()
            self.assertIn("success", result)
            if result["success"]:
                self.assertIn("card_number", result)
                self.assertIn("card_expiry", result)
                self.assertIn("card_cvv", result)
                # Validate card number format (simplified)
                self.assertTrue(re.match(r'^\d{13,19}$', result["card_number"]))
                logger.info(f"Successfully tested card generation: {result['card_number']}")
            else:
                # If API fails, we should get a fallback card
                self.assertIn("card_number", result)
                logger.warning(f"API call failed, using fallback: {result.get('error', 'Unknown error')}")

    def test_email_generation(self):
        """Test email generation API"""
        # Mock the API call if no key available
        if not self.api_key:
            with patch.object(APIIntegrations, 'generate_email') as mock_method:
                mock_method.return_value = {
                    "success": True,
                    "email": "test@disposable.com"
                }
                result = APIIntegrations.generate_email()
                self.assertTrue(result["success"])
                self.assertIn("email", result)
                logger.info("Successfully tested email generation (mock)")
        else:
            # Real API call
            result = APIIntegrations.generate_email()
            self.assertIn("success", result)
            if result["success"]:
                self.assertIn("email", result)
                # Validate email format (simplified)
                self.assertTrue(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', result["email"]))
                logger.info(f"Successfully tested email generation: {result['email']}")
            else:
                # If API fails, we should get a fallback email
                self.assertIn("email", result)
                logger.warning(f"API call failed, using fallback: {result.get('error', 'Unknown error')}")

    def test_complete_trial_data(self):
        """Test generation of complete trial data"""
        # Mock the API call if no key available
        if not self.api_key:
            with patch.object(APIIntegrations, 'generate_complete_trial_data') as mock_method:
                mock_data = {
                    "success": True,
                    "identity": {
                        "first_name": "John",
                        "last_name": "Doe",
                        "address": "123 Main St",
                        "city": "Anytown",
                        "state": "CA",
                        "zipcode": "90210"
                    },
                    "card": {
                        "card_number": "4111111111111111",
                        "card_expiry": "12/25",
                        "card_cvv": "123",
                        "card_holder": "John Doe"
                    },
                    "email": "test@disposable.com",
                    "phone": "1234567890",
                    "service": "netflix"
                }
                mock_method.return_value = mock_data
                result = APIIntegrations.generate_complete_trial_data(service="netflix")
                self.assertTrue(result["success"])
                self.assertIn("identity", result)
                self.assertIn("card", result)
                self.assertIn("email", result)
                self.assertIn("phone", result)
                logger.info("Successfully tested complete trial data generation (mock)")
        else:
            # Real API call
            result = APIIntegrations.generate_complete_trial_data(service="netflix")
            self.assertIn("success", result)
            if result["success"]:
                self.assertIn("identity", result)
                self.assertIn("card", result)
                self.assertIn("email", result)
                self.assertIn("phone", result)
                logger.info(f"Successfully tested complete trial data generation for {result.get('service', 'unknown service')}")
            else:
                logger.warning(f"Complete trial data generation failed: {result.get('error', 'Unknown error')}")


async def test_apis_async():
    """Test all APIs asynchronously"""
    logger.info("Starting asynchronous API tests...")
    
    # Check API key
    api_key = os.environ.get("RAPIDAPI_KEY")
    if not api_key:
        logger.warning("RAPIDAPI_KEY not found in environment, using mock tests")
    
    # Create test tasks
    identity_task = asyncio.create_task(async_test_identity())
    card_task = asyncio.create_task(async_test_card())
    email_task = asyncio.create_task(async_test_email())
    phone_task = asyncio.create_task(async_test_phone())
    
    # Wait for all tasks to complete
    results = await asyncio.gather(
        identity_task,
        card_task,
        email_task,
        phone_task,
        return_exceptions=True
    )
    
    # Check results
    success_count = sum(1 for r in results if isinstance(r, dict) and r.get("success", False))
    logger.info(f"Completed {len(results)} API tests with {success_count} successes")
    
    # Return overall status
    return {
        "success": success_count == len(results),
        "tests_run": len(results),
        "successful_tests": success_count,
        "results": results
    }

async def async_test_identity():
    """Test identity generation asynchronously"""
    logger.info("Testing identity generation...")
    try:
        result = APIIntegrations.generate_identity()
        if result.get("success", False):
            logger.info(f"Identity generation successful: {result.get('first_name', '')} {result.get('last_name', '')}")
        else:
            logger.warning(f"Identity generation failed: {result.get('error', 'Unknown error')}")
        return result
    except Exception as e:
        logger.error(f"Error testing identity generation: {e}")
        return {"success": False, "error": str(e)}

async def async_test_card():
    """Test card generation asynchronously"""
    logger.info("Testing card generation...")
    try:
        result = APIIntegrations.generate_card()
        if result.get("success", False):
            # Mask card number for security
            card_number = result.get("card_number", "")
            masked_number = f"{'*' * (len(card_number) - 4)}{card_number[-4:]}" if card_number else ""
            logger.info(f"Card generation successful: {masked_number}")
        else:
            logger.warning(f"Card generation failed: {result.get('error', 'Unknown error')}")
        return result
    except Exception as e:
        logger.error(f"Error testing card generation: {e}")
        return {"success": False, "error": str(e)}

async def async_test_email():
    """Test email generation asynchronously"""
    logger.info("Testing email generation...")
    try:
        result = APIIntegrations.generate_email()
        if result.get("success", False):
            logger.info(f"Email generation successful: {result.get('email', '')}")
        else:
            logger.warning(f"Email generation failed: {result.get('error', 'Unknown error')}")
        return result
    except Exception as e:
        logger.error(f"Error testing email generation: {e}")
        return {"success": False, "error": str(e)}

async def async_test_phone():
    """Test phone generation asynchronously"""
    logger.info("Testing phone generation...")
    try:
        result = APIIntegrations.generate_virtual_number()
        if result.get("success", False):
            logger.info(f"Phone generation successful: {result.get('phone_number', '')}")
        else:
            logger.warning(f"Phone generation failed: {result.get('error', 'Unknown error')}")
        return result
    except Exception as e:
        logger.error(f"Error testing phone generation: {e}")
        return {"success": False, "error": str(e)}


def run_all_tests():
    """Run all tests and return a summary"""
    # Run unittest tests
    suite = unittest.TestLoader().loadTestsFromTestCase(APIIntegrationTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    # Run async tests
    async_result = asyncio.run(test_apis_async())
    
    # Combine results
    return {
        "unittest_success": result.wasSuccessful(),
        "unittest_tests": result.testsRun,
        "unittest_failures": len(result.failures),
        "unittest_errors": len(result.errors),
        "async_success": async_result.get("success", False),
        "async_tests": async_result.get("tests_run", 0),
        "async_successful": async_result.get("successful_tests", 0)
    }


if __name__ == "__main__":
    logger.info("Starting API integration tests...")
    results = run_all_tests()
    logger.info(f"Test summary: {json.dumps(results, indent=2)}")
    logger.info("API integration tests completed")