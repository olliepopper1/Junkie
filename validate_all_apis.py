#!/usr/bin/env python3
"""
Validate All API Integrations

This script tests all API integrations for the Trial Junkie platform
"""
import os
import json
import logging
import traceback
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("api_validations.log")
    ]
)
logger = logging.getLogger("api_validator")

def test_identity_generation():
    """Test identity generation using RandomUser.me API"""
    logger.info("Testing identity generation")
    
    try:
        from api_integrations import APIIntegrations
        
        # Test identity generation
        identity = APIIntegrations.generate_identity()
        
        # Check if we got the expected fields
        required_fields = ["first_name", "last_name", "address", "city", "state", "zipcode", "phone", "email", "dob"]
        
        # Validate that all required fields exist and are not empty
        validation = {field: field in identity and bool(identity[field]) for field in required_fields}
        
        # Check if all validations passed
        success = all(validation.values())
        
        # Generate report
        result = {
            "success": success,
            "validation": validation,
            "identity_sample": {k: v for k, v in identity.items() if k in ["first_name", "last_name", "city", "state"]}
        }
        
        logger.info(f"Identity generation test result: {json.dumps(result, indent=2)}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error testing identity generation: {e}")
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def test_card_generation():
    """Test credit card generation"""
    logger.info("Testing credit card generation")
    
    try:
        from api_integrations import APIIntegrations
        
        card_types = ["visa", "mastercard", "amex", "discover"]
        results = {}
        
        for card_type in card_types:
            # Generate card
            card = APIIntegrations.generate_card(card_type)
            
            # Check required fields
            required_fields = ["card_number", "card_type", "cvv", "expiry_month", "expiry_year", "cardholder_name"]
            validation = {field: field in card and bool(card[field]) for field in required_fields}
            
            # Check if card type matches what was requested
            if "card_type" in card:
                validation["type_match"] = card["card_type"].lower() == card_type.lower()
            else:
                validation["type_match"] = False
            
            # Check if all validations passed
            success = all(validation.values())
            
            results[card_type] = {
                "success": success,
                "validation": validation,
                "card_sample": {
                    "type": card.get("card_type", ""),
                    "number_prefix": card.get("card_number", "")[:6] + "******" if card.get("card_number") else "",
                    "expiry": f"{card.get('expiry_month', '')}/{card.get('expiry_year', '')}"
                }
            }
        
        # Overall success if all card types were generated successfully
        overall_success = all(result["success"] for result in results.values())
        
        logger.info(f"Credit card generation test result: Overall success={overall_success}")
        for card_type, result in results.items():
            logger.info(f"  {card_type}: {result['success']}")
        
        return {
            "success": overall_success,
            "results": results
        }
    
    except Exception as e:
        logger.error(f"Error testing card generation: {e}")
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def test_email_generation():
    """Test email generation"""
    logger.info("Testing email generation")
    
    try:
        from api_integrations import APIIntegrations
        
        # Generate email
        email = APIIntegrations.generate_email()
        
        # Check required fields
        required_fields = ["email", "password"]
        validation = {field: field in email and bool(email[field]) for field in required_fields}
        
        # Check if all validations passed
        success = all(validation.values())
        
        # Generate report
        result = {
            "success": success,
            "validation": validation,
            "email_sample": email.get("email", "N/A")
        }
        
        logger.info(f"Email generation test result: {json.dumps(result, indent=2)}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error testing email generation: {e}")
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def test_web_scraper():
    """Test web scraper"""
    logger.info("Testing web scraper")
    
    try:
        from api_integrations import APIIntegrations
        
        # Test URLs
        test_url = "https://www.example.com"
        
        # Test without JavaScript rendering
        result = APIIntegrations.web_scrape(test_url, timeout=20, render_js=False)
        
        # Check if we got a successful response
        success = "error" not in result and result.get("status_code", 0) == 200
        
        # Generate report
        scraper_result = {
            "success": success,
            "method": result.get("method", "unknown"),
            "status_code": result.get("status_code", 0),
            "content_length": len(result.get("content", ""))
        }
        
        logger.info(f"Web scraper test result: {json.dumps(scraper_result, indent=2)}")
        
        return scraper_result
    
    except Exception as e:
        logger.error(f"Error testing web scraper: {e}")
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def test_complete_trial_data():
    """Test generating complete trial data"""
    logger.info("Testing complete trial data generation")
    
    try:
        from api_integrations import APIIntegrations
        
        # Generate complete trial data
        trial_data = APIIntegrations.generate_complete_trial_data()
        
        # Check major sections
        required_sections = ["user_info", "payment_info", "verification_info"]
        validation = {section: section in trial_data and bool(trial_data[section]) for section in required_sections}
        
        # Check user_info fields
        if "user_info" in trial_data:
            user_info = trial_data["user_info"]
            user_fields = ["first_name", "last_name", "email", "password", "phone", "address"]
            validation["user_info_fields"] = all(field in user_info and bool(user_info[field]) for field in user_fields)
        else:
            validation["user_info_fields"] = False
        
        # Check payment_info fields
        if "payment_info" in trial_data:
            payment_info = trial_data["payment_info"]
            payment_fields = ["card_number", "card_type", "expiry", "cvv", "cardholder_name"]
            validation["payment_info_fields"] = all(field in payment_info and bool(payment_info[field]) for field in payment_fields)
        else:
            validation["payment_info_fields"] = False
        
        # Check if all validations passed
        success = all(validation.values())
        
        # Generate report
        result = {
            "success": success,
            "validation": validation,
            "sample": {
                "user": {
                    "name": f"{trial_data.get('user_info', {}).get('first_name', '')} {trial_data.get('user_info', {}).get('last_name', '')}",
                    "email": trial_data.get('user_info', {}).get('email', ''),
                },
                "payment": {
                    "card_type": trial_data.get('payment_info', {}).get('card_type', ''),
                    "cardholder": trial_data.get('payment_info', {}).get('cardholder_name', '')
                }
            }
        }
        
        logger.info(f"Complete trial data test result: {json.dumps(result, indent=2)}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error testing complete trial data generation: {e}")
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def run_all_tests():
    """Run all API validation tests"""
    logger.info("Running all API validation tests")
    
    results = {
        "identity": test_identity_generation(),
        "card": test_card_generation(),
        "email": test_email_generation(),
        "web_scraper": test_web_scraper(),
        "trial_data": test_complete_trial_data(),
        "timestamp": datetime.now().isoformat()
    }
    
    # Calculate overall success
    overall_success = all(result.get("success", False) for result in results.values() if isinstance(result, dict))
    results["overall_success"] = overall_success
    
    return results

def main():
    """Main function"""
    logger.info("Starting API validation")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Run all tests
    results = run_all_tests()
    
    # Print summary
    logger.info("=== API Validation Summary ===")
    logger.info(f"Overall Success: {results.get('overall_success', False)}")
    for test_name, result in results.items():
        if isinstance(result, dict) and "success" in result:
            logger.info(f"{test_name}: {'SUCCESS' if result['success'] else 'FAILED'}")
    
    # Save results to file
    filename = f"api_validation_results_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Results saved to {filename}")
    
    # Return overall success status
    return results.get("overall_success", False)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)