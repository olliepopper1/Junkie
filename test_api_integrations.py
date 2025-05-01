"""
API Integration Tests
Tests the configured API integrations with the RapidAPI key
"""
import logging
import time
import json
from api_integrations import APIIntegrations

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("api_integration_tests")

def test_identity_generation():
    """Test the identity generation API"""
    logger.info("Testing identity generation API...")
    try:
        identity = APIIntegrations.generate_identity()
        
        # Check if required fields are present
        required_fields = ["first_name", "last_name", "address", "city", "state", "zipcode"]
        missing_fields = [field for field in required_fields if not identity.get(field)]
        
        if missing_fields:
            logger.warning(f"Identity missing fields: {missing_fields}")
            return False
        
        logger.info(f"Identity generated successfully: {identity['first_name']} {identity['last_name']}")
        return True
    except Exception as e:
        logger.error(f"Error testing identity generation: {e}")
        return False

def test_email_generation():
    """Test the email generation API"""
    logger.info("Testing email generation API...")
    try:
        email_data = APIIntegrations.generate_email()
        
        # Check if required fields are present
        if not email_data.get("email"):
            logger.warning("No email address was generated")
            return False
        
        logger.info(f"Email generated successfully: {email_data['email']}")
        return True
    except Exception as e:
        logger.error(f"Error testing email generation: {e}")
        return False

def test_email_validation():
    """Test the email validation API"""
    logger.info("Testing email validation API...")
    try:
        # Use a known valid email for testing
        test_email = "test@example.com"
        validation = APIIntegrations.validate_email(test_email)
        
        # Check if validation was performed
        if "is_valid" not in validation:
            logger.warning("Email validation didn't return validation status")
            return False
        
        logger.info(f"Email validation successful: {validation}")
        return True
    except Exception as e:
        logger.error(f"Error testing email validation: {e}")
        return False

def test_virtual_number():
    """Test the virtual number API"""
    logger.info("Testing virtual number API...")
    try:
        phone_data = APIIntegrations.generate_virtual_number()
        
        # Check if required fields are present
        if not phone_data.get("phone_number"):
            logger.warning("No phone number was generated")
            return False
        
        logger.info(f"Phone number generated successfully: {phone_data['phone_number']}")
        return True
    except Exception as e:
        logger.error(f"Error testing virtual number generation: {e}")
        return False

def test_card_generation():
    """Test the credit card generation API"""
    logger.info("Testing credit card generation API...")
    try:
        card_data = APIIntegrations.generate_card()
        
        # Check if required fields are present
        required_fields = ["card_number", "card_type", "cvv", "expiry"]
        missing_fields = [field for field in required_fields if not card_data.get(field)]
        
        if missing_fields:
            logger.warning(f"Card data missing fields: {missing_fields}")
            return False
        
        logger.info(f"Card generated successfully: {card_data['card_type']} ending in {card_data['card_number'][-4:]}")
        return True
    except Exception as e:
        logger.error(f"Error testing card generation: {e}")
        return False

def test_web_scraping():
    """Test the ScrapeNinja web scraping API"""
    logger.info("Testing ScrapeNinja web scraping API...")
    try:
        # Use a simple public website for testing
        test_url = "https://example.com"
        scrape_result = APIIntegrations.web_scrape(test_url, use_proxy=True)
        
        # Check if we got valid content
        if "error" in scrape_result:
            logger.warning(f"Scraping error: {scrape_result['error']}")
            return False
        
        if not scrape_result.get("content"):
            logger.warning("No content retrieved from scraping")
            return False
        
        content_length = len(scrape_result.get("content", ""))
        logger.info(f"Scraping successful: Retrieved {content_length} characters from {test_url}")
        return True
    except Exception as e:
        logger.error(f"Error testing web scraping: {e}")
        return False

def test_complete_trial_data():
    """Test generating complete trial data"""
    logger.info("Testing complete trial data generation...")
    try:
        trial_data = APIIntegrations.generate_complete_trial_data()
        
        # Check if main sections are present
        required_sections = ["user_info", "payment_info", "verification_info"]
        missing_sections = [section for section in required_sections if section not in trial_data]
        
        if missing_sections:
            logger.warning(f"Trial data missing sections: {missing_sections}")
            return False
        
        logger.info("Complete trial data generated successfully")
        return True
    except Exception as e:
        logger.error(f"Error testing complete trial data generation: {e}")
        return False

def run_all_tests():
    """Run all API integration tests"""
    logger.info("Starting API integration tests...")
    
    # Store test results
    results = {
        "identity_generation": {"success": False, "time": 0},
        "email_generation": {"success": False, "time": 0},
        "email_validation": {"success": False, "time": 0},
        "virtual_number": {"success": False, "time": 0},
        "card_generation": {"success": False, "time": 0},
        "web_scraping": {"success": False, "time": 0},
        "complete_trial_data": {"success": False, "time": 0}
    }
    
    # Test identity generation
    start_time = time.time()
    results["identity_generation"]["success"] = test_identity_generation()
    results["identity_generation"]["time"] = round(time.time() - start_time, 2)
    
    # Test email validation
    start_time = time.time()
    results["email_validation"]["success"] = test_email_validation()
    results["email_validation"]["time"] = round(time.time() - start_time, 2)
    
    # Test email generation
    start_time = time.time()
    results["email_generation"]["success"] = test_email_generation()
    results["email_generation"]["time"] = round(time.time() - start_time, 2)
    
    # Test virtual number
    start_time = time.time()
    results["virtual_number"]["success"] = test_virtual_number()
    results["virtual_number"]["time"] = round(time.time() - start_time, 2)
    
    # Test card generation
    start_time = time.time()
    results["card_generation"]["success"] = test_card_generation()
    results["card_generation"]["time"] = round(time.time() - start_time, 2)
    
    # Test web scraping
    start_time = time.time()
    results["web_scraping"]["success"] = test_web_scraping()
    results["web_scraping"]["time"] = round(time.time() - start_time, 2)
    
    # Test complete trial data
    start_time = time.time()
    results["complete_trial_data"]["success"] = test_complete_trial_data()
    results["complete_trial_data"]["time"] = round(time.time() - start_time, 2)
    
    # Calculate overall success
    total_tests = len(results)
    successful_tests = sum(1 for test in results.values() if test["success"])
    success_rate = round((successful_tests / total_tests) * 100, 2)
    
    # Create test summary
    summary = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "success_rate": success_rate,
        "successful_tests": successful_tests,
        "total_tests": total_tests,
        "results": results
    }
    
    # Save test results to file
    filename = f"api_test_results_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Test results saved to {filename}")
    
    # Print summary
    print("\n=============== API Integration Test Summary ===============")
    print(f"Success Rate: {success_rate}% ({successful_tests}/{total_tests} tests passed)")
    print("\nDetailed Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status} ({result['time']}s)")
    print("==========================================================\n")
    
    return summary

if __name__ == "__main__":
    run_all_tests()