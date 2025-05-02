#!/usr/bin/env python3
"""
Trial Junkie Setup Script
Initializes and tests all components of the Trial Junkie system
"""
import os
import sys
import json
import time
import logging
import requests
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("setup.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("setup")

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Environment variables loaded")
except ImportError:
    logger.warning("dotenv module not available - environment variables may not be loaded")

# Check required environment variables
def check_environment_variables() -> bool:
    """
    Check if required environment variables are set
    
    Returns:
        bool: True if all required variables are set, False otherwise
    """
    logger.info("Checking environment variables...")
    
    required_variables = [
        "DATABASE_URL"
    ]
    
    optional_variables = [
        "DISCORD_BOT_TOKEN",
        "RAPIDAPI_KEY"
    ]
    
    # Check required variables
    missing_required = []
    for var in required_variables:
        if not os.getenv(var):
            missing_required.append(var)
    
    # Check optional variables
    missing_optional = []
    for var in optional_variables:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        logger.error(f"Missing required environment variables: {', '.join(missing_required)}")
        return False
    
    if missing_optional:
        logger.warning(f"Missing optional environment variables: {', '.join(missing_optional)}")
    
    logger.info("All required environment variables are set")
    return True

# Test API endpoints
def check_api_endpoints() -> Dict[str, Any]:
    """
    Test API endpoints to ensure they are working
    
    Returns:
        dict: API test results
    """
    logger.info("Checking API endpoints...")
    
    # API configuration
    apis = [
        {
            "name": "Random Identity Generator",
            "url": "https://randomuser.me/api/",
            "method": "GET",
            "headers": {}
        },
        {
            "name": "Fake Valid CC Generator",
            "url": "https://fake-valid-cc-generator.p.rapidapi.com/creditcard/generate",
            "method": "GET",
            "headers": {
                "X-RapidAPI-Host": "fake-valid-cc-generator.p.rapidapi.com",
                "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY", "")
            },
            "params": {
                "credit_card_type": "visa",
                "quantity": "1"
            }
        },
        {
            "name": "Veriphone",
            "url": "https://veriphone.p.rapidapi.com/verify",
            "method": "GET",
            "headers": {
                "X-RapidAPI-Host": "veriphone.p.rapidapi.com",
                "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY", "")
            },
            "params": {
                "phone": "9087654321"
            }
        },
        {
            "name": "Website Scraper",
            "url": "https://website-scraper.p.rapidapi.com/scrape",
            "method": "POST",
            "headers": {
                "X-RapidAPI-Host": "website-scraper.p.rapidapi.com", 
                "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY", ""),
                "Content-Type": "application/json"
            },
            "json": {
                "url": "https://www.example.com",
                "timeout": 30
            }
        }
    ]
    
    # Test each API
    results = []
    success_count = 0
    
    for api in apis:
        logger.info(f"Testing API: {api['name']}")
        try:
            if api.get("method", "GET") == "GET":
                response = requests.get(
                    api["url"],
                    headers=api.get("headers", {}),
                    params=api.get("params", {})
                )
            else:
                response = requests.post(
                    api["url"],
                    headers=api.get("headers", {}),
                    json=api.get("json", {})
                )
            
            if response.status_code == 200:
                logger.info(f"✅ {api['name']} API: Success")
                status = "success"
                success_count += 1
            else:
                logger.warning(f"⚠️ {api['name']} API: Status code {response.status_code}")
                status = "warning"
        
        except Exception as e:
            logger.error(f"❌ {api['name']} API: Error - {str(e)}")
            status = "error"
        
        results.append({
            "name": api["name"],
            "status": status,
            "code": response.status_code if 'response' in locals() else None
        })
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"api_test_results_{timestamp}.json"
    
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"API test results saved to {results_file}")
    logger.info(f"API Check Results: {success_count}/{len(apis)} successful")
    
    return {
        "success_count": success_count,
        "total": len(apis),
        "results": results,
        "file": results_file
    }

# Check database connection
def check_database() -> Dict[str, Any]:
    """
    Check the database connection
    
    Returns:
        dict: Database check results
    """
    logger.info("Checking database connection...")
    try:
        # Import and initialize database
        from database import Database
        db = Database()
        db_result = db.initialize()
        
        if db_result.get("success", False):
            logger.info("✅ Database connection successful")
            return {
                "success": True,
                "message": "Database connection successful"
            }
        else:
            logger.error(f"❌ Database connection failed: {db_result.get('message', 'Unknown error')}")
            return {
                "success": False,
                "message": db_result.get("message", "Unknown error")
            }
    except Exception as e:
        logger.error(f"❌ Database check error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }

# Create example trial
def create_example_trial() -> Dict[str, Any]:
    """
    Create an example trial using the API integrations
    
    Returns:
        dict: Example trial data
    """
    logger.info("Creating example trial file...")
    try:
        # Import API integrations
        from updated_api_integrations import UpdatedAPIIntegrations
        api = UpdatedAPIIntegrations()
        
        # Generate identity
        identity = api.generate_identity()
        
        # Generate card
        card = api.generate_card()
        
        # Combine data
        trial_data = {
            "service": "hulu",
            "plan": "Hulu (No Ads)",
            "email": identity.get("email"),
            "password": "TrialJunkie2025!",
            "first_name": identity.get("first_name"),
            "last_name": identity.get("last_name"),
            "address": identity.get("address"),
            "city": identity.get("city"),
            "state": identity.get("state"),
            "zipcode": identity.get("zipcode"),
            "phone": identity.get("phone"),
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d"),
            "card_details": {
                "type": card.get("type"),
                "number": card.get("number"),
                "expiry": card.get("expiry"),
                "cvv": card.get("cvv"),
                "last4": card.get("last4")
            }
        }
        
        # Save the trial data to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trial_file = f"hulu_trial_{timestamp}.json"
        
        with open(trial_file, "w") as f:
            json.dump(trial_data, f, indent=2)
        
        logger.info(f"Example trial saved to {trial_file}")
        
        return {
            "success": True,
            "file": trial_file,
            "data": trial_data
        }
    except Exception as e:
        logger.error(f"❌ Error creating example trial: {str(e)}")
        traceback.print_exc()
        return {
            "success": False,
            "message": str(e)
        }

# Main setup function
def setup() -> Dict[str, Any]:
    """
    Run the complete setup process
    
    Returns:
        dict: Setup results
    """
    logger.info("TrialJunkie Setup initialized")
    start_time = time.time()
    
    logger.info("Starting Trial Junkie setup...")
    results = {
        "environment_variables": None,
        "api_endpoints": None,
        "database": None,
        "example_trial": None,
        "success": False
    }
    
    # Check environment variables
    env_check = check_environment_variables()
    results["environment_variables"] = {"success": env_check}
    
    if not env_check:
        logger.error("❌ Environment variable check failed - setup aborted")
        return results
    
    # Check API endpoints
    api_results = check_api_endpoints()
    results["api_endpoints"] = api_results
    
    # Check database
    db_results = check_database()
    results["database"] = db_results
    
    # Create example trial
    trial_results = create_example_trial()
    results["example_trial"] = trial_results
    
    # Determine overall success
    results["success"] = (
        env_check and
        db_results.get("success", False) and
        trial_results.get("success", False)
    )
    
    end_time = time.time()
    duration = end_time - start_time
    
    results["duration"] = duration
    results["timestamp"] = datetime.now().isoformat()
    
    # Final log message
    if results["success"]:
        logger.info("Trial Junkie setup completed successfully")
        print("\n✅ Trial Junkie setup completed successfully!")
        print("You can now run the system using:")
        print("1. For the web app: workflow 'Start application'")
        print("2. For the Discord bot: workflow 'discord_bot'")
    else:
        logger.warning("Trial Junkie setup completed with warnings or errors")
        print("\n⚠️ Trial Junkie setup completed with warnings or errors")
        print("Please check the log file for details.")
    
    return results

# Entry point
if __name__ == "__main__":
    setup()