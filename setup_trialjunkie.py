#!/usr/bin/env python3
"""
Trial Junkie Setup Script
This script validates the environment and prepares the Trial Junkie system for use
"""
import os
import sys
import json
import logging
import requests
import subprocess
from datetime import datetime
from dotenv import load_dotenv

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

# Load environment variables
load_dotenv()

class TrialJunkieSetup:
    """Setup and validation for the Trial Junkie system"""
    
    def __init__(self):
        self.api_keys = {
            "DISCORD_BOT_TOKEN": os.getenv("DISCORD_BOT_TOKEN"),
            "RAPIDAPI_KEY": os.getenv("RAPIDAPI_KEY")
        }
        self.api_configs = {}
        self.database_status = None
        logger.info("TrialJunkie Setup initialized")
    
    def check_environment(self):
        """Check if all required environment variables are set"""
        logger.info("Checking environment variables...")
        
        missing_keys = []
        for key, value in self.api_keys.items():
            if not value:
                logger.error(f"Missing environment variable: {key}")
                missing_keys.append(key)
        
        if missing_keys:
            logger.error(f"Missing {len(missing_keys)} required environment variables")
            return False
        
        logger.info("All required environment variables are set")
        return True
    
    def check_apis(self):
        """Check if all required API endpoints are accessible"""
        logger.info("Checking API endpoints...")
        
        rapidapi_key = self.api_keys.get("RAPIDAPI_KEY")
        if not rapidapi_key:
            logger.error("RAPIDAPI_KEY is required to test API endpoints")
            return False
        
        # Define APIs to check
        apis = [
            {
                "name": "Random Identity Generator",
                "host": "random-identity-generator.p.rapidapi.com",
                "endpoint": "https://random-identity-generator.p.rapidapi.com/",
                "headers": {
                    "X-RapidAPI-Key": rapidapi_key,
                    "X-RapidAPI-Host": "random-identity-generator.p.rapidapi.com"
                }
            },
            {
                "name": "Fake Valid CC Generator",
                "host": "fake-valid-cc-data-generator.p.rapidapi.com",
                "endpoint": "https://fake-valid-cc-data-generator.p.rapidapi.com/generate",
                "params": {"brand": "visa", "format": "json"},
                "headers": {
                    "X-RapidAPI-Key": rapidapi_key,
                    "X-RapidAPI-Host": "fake-valid-cc-data-generator.p.rapidapi.com"
                }
            },
            {
                "name": "Veriphone",
                "host": "veriphone.p.rapidapi.com",
                "endpoint": "https://veriphone.p.rapidapi.com/verify",
                "params": {"phone": "2125551234"},
                "headers": {
                    "X-RapidAPI-Key": rapidapi_key,
                    "X-RapidAPI-Host": "veriphone.p.rapidapi.com"
                }
            },
            {
                "name": "Website Scraper",
                "host": "website-scraper-api.p.rapidapi.com",
                "endpoint": "https://website-scraper-api.p.rapidapi.com/scrape",
                "params": {"url": "https://www.example.com", "javascript": "true"},
                "headers": {
                    "X-RapidAPI-Key": rapidapi_key,
                    "X-RapidAPI-Host": "website-scraper-api.p.rapidapi.com"
                }
            }
        ]
        
        results = []
        for api in apis:
            try:
                logger.info(f"Testing API: {api['name']}")
                if api.get('params'):
                    response = requests.get(api['endpoint'], headers=api['headers'], params=api['params'], timeout=10)
                else:
                    response = requests.get(api['endpoint'], headers=api['headers'], timeout=10)
                
                status = response.status_code
                if status == 200:
                    logger.info(f"✅ {api['name']} API: Success")
                    results.append({"name": api['name'], "status": "success", "code": status})
                else:
                    logger.warning(f"⚠️ {api['name']} API: Status code {status}")
                    results.append({"name": api['name'], "status": "warning", "code": status})
            
            except requests.RequestException as e:
                logger.error(f"❌ {api['name']} API: Error - {str(e)}")
                results.append({"name": api['name'], "status": "error", "message": str(e)})
        
        # Save API test results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"api_test_results_{timestamp}.json"
        with open(result_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"API test results saved to {result_file}")
        
        # Count successful APIs
        success_count = sum(1 for r in results if r['status'] == 'success')
        logger.info(f"API Check Results: {success_count}/{len(apis)} successful")
        
        self.api_configs = {api['name']: api for api in apis}
        return success_count > 0
    
    def check_database(self):
        """Check if the database is accessible"""
        logger.info("Checking database connection...")
        
        try:
            from database import Database
            db = Database()
            connection_result = db.initialize()
            self.database_status = connection_result
            
            if connection_result.get('success'):
                logger.info("✅ Database connection successful")
                return True
            else:
                logger.error(f"❌ Database connection failed: {connection_result.get('message', 'Unknown error')}")
                return False
            
        except ImportError:
            logger.error("❌ Database module not found")
            return False
        except Exception as e:
            logger.error(f"❌ Database check error: {str(e)}")
            return False
    
    def create_example_trial(self):
        """Create an example trial file to test the system"""
        logger.info("Creating example trial file...")
        
        from updated_api_integrations import UpdatedAPIIntegrations
        
        try:
            # Initialize API
            api = UpdatedAPIIntegrations()
            
            # Generate core data
            identity = api.generate_identity()
            card = api.generate_card("visa")
            
            # Assemble trial data
            trial_data = {
                "service": "hulu",
                "plan": "Hulu (No Ads)",
                "email": identity.get('email', f"{identity['first_name'].lower()}.{identity['last_name'].lower()}@example.com"),
                "password": "TrialJunkie2025!",
                "first_name": identity.get('first_name', ''),
                "last_name": identity.get('last_name', ''),
                "address": identity.get('address', ''),
                "city": identity.get('city', ''),
                "state": identity.get('state', ''),
                "zipcode": identity.get('zipcode', ''),
                "phone": identity.get('phone', ''),
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "end_date": datetime.now().strftime("%Y-%m-%d"),
                "card_details": {
                    "type": card.get('card_type', 'visa'),
                    "number": card.get('card_number', ''),
                    "expiry": card.get('expiry', ''),
                    "cvv": card.get('cvv', ''),
                    "last4": card.get('card_number', '')[-4:] if card.get('card_number') else ''
                }
            }
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            trial_file = f"hulu_trial_{timestamp}.json"
            with open(trial_file, 'w') as f:
                json.dump(trial_data, f, indent=2)
            
            logger.info(f"Example trial saved to {trial_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create example trial: {str(e)}")
            return False
    
    def run_setup(self):
        """Run the complete setup process"""
        logger.info("Starting Trial Junkie setup...")
        
        # Step 1: Check environment variables
        env_check = self.check_environment()
        if not env_check:
            logger.error("Environment check failed. Please set required environment variables.")
            return False
        
        # Step 2: Check API access
        api_check = self.check_apis()
        if not api_check:
            logger.warning("API check encountered issues. Setup will continue but some features may not work.")
        
        # Step 3: Check database
        db_check = self.check_database()
        if not db_check:
            logger.error("Database check failed. Please check database configuration.")
            return False
        
        # Step 4: Create example trial
        trial_check = self.create_example_trial()
        if not trial_check:
            logger.warning("Example trial creation failed. Setup will continue but you may encounter issues.")
        
        logger.info("Trial Junkie setup completed successfully")
        return True

if __name__ == "__main__":
    setup = TrialJunkieSetup()
    success = setup.run_setup()
    
    if success:
        print("\n✅ Trial Junkie setup completed successfully!")
        print("You can now run the system using:")
        print("1. For the web app: workflow 'Start application'")
        print("2. For the Discord bot: workflow 'discord_bot'")
    else:
        print("\n❌ Trial Junkie setup encountered issues.")
        print("Please check setup.log for more details.")
        sys.exit(1)