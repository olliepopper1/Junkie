"""
Real API Integration Tests
Tests the actual API connections with valid credentials
"""
import os
import json
import logging
import argparse
import sys
import asyncio
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("api_test_results.log")
    ]
)
logger = logging.getLogger("api_tests")

# Import the API integrations
try:
    from api_integrations import APIIntegrations
    logger.info("Successfully imported API integrations")
except ImportError as e:
    logger.error(f"Failed to import API integrations: {e}")
    sys.exit(1)

class APITester:
    """Class to test all API integrations"""
    
    def __init__(self, verbose=False):
        """Initialize the API tester"""
        self.verbose = verbose
        self.results = {
            "identity": {"success": False, "data": None, "error": None},
            "virtual_number": {"success": False, "data": None, "error": None},
            "card": {"success": False, "data": None, "error": None},
            "email": {"success": False, "data": None, "error": None},
            "complete_trial": {"success": False, "data": None, "error": None}
        }
        
        # Check if RapidAPI key is available
        self.api_key = os.environ.get("RAPIDAPI_KEY")
        if not self.api_key:
            logger.warning("RAPIDAPI_KEY not found in environment variables")
            print("⚠️ RAPIDAPI_KEY is missing! Tests may fail.")
        else:
            logger.info("RAPIDAPI_KEY found in environment")
            # Mask the key for security when logging
            masked_key = f"{self.api_key[:4]}...{self.api_key[-4:]}" if len(self.api_key) > 8 else "****"
            logger.info(f"Using API key: {masked_key}")
    
    def test_identity_generation(self):
        """Test the identity generation API"""
        logger.info("Testing identity generation API...")
        try:
            result = APIIntegrations.generate_identity()
            self.results["identity"]["success"] = "first_name" in result and "last_name" in result
            self.results["identity"]["data"] = result
            
            if self.verbose:
                if self.results["identity"]["success"]:
                    print(f"✅ Identity Generation: {result.get('first_name', '')} {result.get('last_name', '')}")
                    logger.info(f"Identity generation successful: {result.get('first_name', '')} {result.get('last_name', '')}")
                else:
                    print(f"❌ Identity Generation Failed: {result}")
                    logger.warning(f"Identity generation returned incomplete data: {result}")
            return self.results["identity"]["success"]
            
        except Exception as e:
            self.results["identity"]["error"] = str(e)
            self.results["identity"]["success"] = False
            if self.verbose:
                print(f"❌ Identity Generation Error: {e}")
            logger.error(f"Error testing identity generation: {e}")
            return False
    
    def test_virtual_number(self):
        """Test the virtual phone number API"""
        logger.info("Testing virtual phone number API...")
        try:
            result = APIIntegrations.generate_virtual_number()
            self.results["virtual_number"]["success"] = "phone_number" in result
            self.results["virtual_number"]["data"] = result
            
            if self.verbose:
                if self.results["virtual_number"]["success"]:
                    print(f"✅ Virtual Number: {result.get('phone_number', '')}")
                    logger.info(f"Virtual number generation successful: {result.get('phone_number', '')}")
                else:
                    print(f"❌ Virtual Number Failed: {result}")
                    logger.warning(f"Virtual number generation returned incomplete data: {result}")
            return self.results["virtual_number"]["success"]
            
        except Exception as e:
            self.results["virtual_number"]["error"] = str(e)
            self.results["virtual_number"]["success"] = False
            if self.verbose:
                print(f"❌ Virtual Number Error: {e}")
            logger.error(f"Error testing virtual number generation: {e}")
            return False
    
    def test_card_generation(self):
        """Test the credit card generation API"""
        logger.info("Testing credit card generation API...")
        try:
            result = APIIntegrations.generate_card()
            self.results["card"]["success"] = "card_number" in result and "expiry" in result and "cvv" in result
            self.results["card"]["data"] = result
            
            if self.verbose:
                if self.results["card"]["success"]:
                    # Mask card number for security
                    card_number = result.get("card_number", "")
                    masked_number = f"{'*' * (len(card_number) - 4)}{card_number[-4:]}" if card_number else ""
                    print(f"✅ Card Generation: {masked_number}")
                    logger.info(f"Card generation successful: {masked_number}")
                else:
                    print(f"❌ Card Generation Failed: {result}")
                    logger.warning(f"Card generation returned incomplete data: {result}")
            return self.results["card"]["success"]
            
        except Exception as e:
            self.results["card"]["error"] = str(e)
            self.results["card"]["success"] = False
            if self.verbose:
                print(f"❌ Card Generation Error: {e}")
            logger.error(f"Error testing card generation: {e}")
            return False
    
    def test_email_generation(self):
        """Test the email generation API"""
        logger.info("Testing email generation API...")
        try:
            result = APIIntegrations.generate_email()
            self.results["email"]["success"] = "email" in result
            self.results["email"]["data"] = result
            
            if self.verbose:
                if self.results["email"]["success"]:
                    print(f"✅ Email Generation: {result.get('email', '')}")
                    logger.info(f"Email generation successful: {result.get('email', '')}")
                else:
                    print(f"❌ Email Generation Failed: {result}")
                    logger.warning(f"Email generation returned incomplete data: {result}")
            return self.results["email"]["success"]
            
        except Exception as e:
            self.results["email"]["error"] = str(e)
            self.results["email"]["success"] = False
            if self.verbose:
                print(f"❌ Email Generation Error: {e}")
            logger.error(f"Error testing email generation: {e}")
            return False
    
    def test_complete_trial_data(self, service="netflix"):
        """Test the complete trial data generation"""
        logger.info(f"Testing complete trial data generation for {service}...")
        try:
            result = APIIntegrations.generate_complete_trial_data(service=service)
            self.results["complete_trial"]["success"] = "identity" in result and "card" in result and "email" in result
            self.results["complete_trial"]["data"] = result
            
            if self.verbose:
                if self.results["complete_trial"]["success"]:
                    print(f"✅ Complete Trial Data Generation for {service}")
                    logger.info(f"Complete trial data generation successful for {service}")
                else:
                    print(f"❌ Complete Trial Data Failed: {result}")
                    logger.warning(f"Complete trial data generation returned incomplete data: {result}")
            return self.results["complete_trial"]["success"]
            
        except Exception as e:
            self.results["complete_trial"]["error"] = str(e)
            self.results["complete_trial"]["success"] = False
            if self.verbose:
                print(f"❌ Complete Trial Data Error: {e}")
            logger.error(f"Error testing complete trial data generation: {e}")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🧪 Running API Integration Tests with Real Credentials")
        print("=" * 50)
        
        # Run each test
        identity_success = self.test_identity_generation()
        phone_success = self.test_virtual_number()
        card_success = self.test_card_generation()
        email_success = self.test_email_generation()
        trial_success = self.test_complete_trial_data()
        
        # Calculate success rate
        tests_run = 5
        successful_tests = sum([
            1 if identity_success else 0,
            1 if phone_success else 0,
            1 if card_success else 0,
            1 if email_success else 0,
            1 if trial_success else 0
        ])
        
        success_rate = (successful_tests / tests_run) * 100
        
        # Print summary
        print("\n" + "=" * 50)
        print(f"📊 Test Summary: {successful_tests}/{tests_run} tests passed ({success_rate:.1f}%)")
        print(f"📝 Identity Generation: {'✅ Passed' if identity_success else '❌ Failed'}")
        print(f"📱 Virtual Phone Number: {'✅ Passed' if phone_success else '❌ Failed'}")
        print(f"💳 Card Generation: {'✅ Passed' if card_success else '❌ Failed'}")
        print(f"📧 Email Generation: {'✅ Passed' if email_success else '❌ Failed'}")
        print(f"🧩 Complete Trial Data: {'✅ Passed' if trial_success else '❌ Failed'}")
        print("=" * 50)
        
        # Log results
        logger.info(f"Test summary: {successful_tests}/{tests_run} tests passed ({success_rate:.1f}%)")
        
        # Get timestamp for the results file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results to file
        results_file = f"api_test_results_{timestamp}.json"
        with open(results_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "tests_run": tests_run,
                "successful_tests": successful_tests,
                "success_rate": success_rate,
                "results": self.results
            }, f, indent=2)
        
        logger.info(f"Detailed results saved to {results_file}")
        print(f"📄 Detailed results saved to {results_file}")
        
        return successful_tests == tests_run

async def run_asyncio_tests():
    """Run tests using asyncio for better performance"""
    logger.info("Starting asyncio tests...")
    
    # Create tasks for each API test
    identity_task = asyncio.create_task(async_test_identity())
    phone_task = asyncio.create_task(async_test_phone())
    card_task = asyncio.create_task(async_test_card())
    email_task = asyncio.create_task(async_test_email())
    
    # Wait for all tasks to complete
    results = await asyncio.gather(
        identity_task,
        phone_task,
        card_task,
        email_task,
        return_exceptions=True
    )
    
    # Process results
    success_count = sum(1 for r in results if isinstance(r, dict) and r.get("success", False))
    logger.info(f"Asyncio tests completed: {success_count}/{len(results)} tests passed")
    
    return {
        "success_rate": (success_count / len(results)) * 100 if len(results) > 0 else 0,
        "successful_tests": success_count,
        "total_tests": len(results),
        "results": results
    }

async def async_test_identity():
    """Test identity generation using asyncio"""
    logger.info("Testing identity generation (async)...")
    try:
        result = APIIntegrations.generate_identity()
        success = "first_name" in result and "last_name" in result
        if success:
            logger.info(f"Identity generation successful: {result.get('first_name')} {result.get('last_name')}")
        else:
            logger.warning("Identity generation returned incomplete data")
        return {"success": success, "data": result}
    except Exception as e:
        logger.error(f"Error in async identity test: {e}")
        return {"success": False, "error": str(e)}

async def async_test_phone():
    """Test phone generation using asyncio"""
    logger.info("Testing virtual number generation (async)...")
    try:
        result = APIIntegrations.generate_virtual_number()
        success = "phone_number" in result
        if success:
            logger.info(f"Virtual number generation successful: {result.get('phone_number')}")
        else:
            logger.warning("Virtual number generation returned incomplete data")
        return {"success": success, "data": result}
    except Exception as e:
        logger.error(f"Error in async phone test: {e}")
        return {"success": False, "error": str(e)}

async def async_test_card():
    """Test card generation using asyncio"""
    logger.info("Testing card generation (async)...")
    try:
        result = APIIntegrations.generate_card()
        success = "card_number" in result and "expiry" in result
        if success:
            # Mask card number for security
            card_number = result.get("card_number", "")
            masked_number = f"{'*' * (len(card_number) - 4)}{card_number[-4:]}" if card_number else ""
            logger.info(f"Card generation successful: {masked_number}")
        else:
            logger.warning("Card generation returned incomplete data")
        return {"success": success, "data": result}
    except Exception as e:
        logger.error(f"Error in async card test: {e}")
        return {"success": False, "error": str(e)}

async def async_test_email():
    """Test email generation using asyncio"""
    logger.info("Testing email generation (async)...")
    try:
        result = APIIntegrations.generate_email()
        success = "email" in result
        if success:
            logger.info(f"Email generation successful: {result.get('email')}")
        else:
            logger.warning("Email generation returned incomplete data")
        return {"success": success, "data": result}
    except Exception as e:
        logger.error(f"Error in async email test: {e}")
        return {"success": False, "error": str(e)}

def main():
    """Main function for CLI usage"""
    parser = argparse.ArgumentParser(description='Test API integrations with real credentials')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--async', '-a', action='store_true', help='Run tests asynchronously', dest='async_mode')
    parser.add_argument('--service', '-s', default='netflix', help='Service to test for trial generation')
    args = parser.parse_args()
    
    if args.async_mode:
        print("🧪 Running API Tests Asynchronously")
        print("=" * 50)
        results = asyncio.run(run_asyncio_tests())
        print("\n" + "=" * 50)
        print(f"📊 Async Test Summary: {results['successful_tests']}/{results['total_tests']} tests passed ({results['success_rate']:.1f}%)")
        print("=" * 50)
    else:
        tester = APITester(verbose=args.verbose)
        tester.run_all_tests()

if __name__ == "__main__":
    main()