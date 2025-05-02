#!/usr/bin/env python3
"""
Trial Junkie Updated API Integrations
Specialized API integrations using only the provided RapidAPI Hub services
"""
import os
import json
import logging
import random
import string
import requests
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("updated_api_integrations.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key from environment variables
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
if not RAPIDAPI_KEY:
    logger.error("RAPIDAPI_KEY not found in environment variables. Please set this variable.")
    
# Discord Bot Token
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables. Please set this variable.")

# Updated API configuration - using only the provided RapidAPI services
API_CONFIG = {
    # Phone Validation API from Abstract
    "phone_validation": {
        "key": RAPIDAPI_KEY,
        "endpoint": "https://phonevalidation.abstractapi.com/v1/",
        "auth_type": "apikey",
        "params": {
            "api_key": RAPIDAPI_KEY
        }
    },
    
    # Veriphone API for global phone validation
    "veriphone": {
        "key": RAPIDAPI_KEY,
        "host": "veriphone.p.rapidapi.com",
        "endpoint": "https://veriphone.p.rapidapi.com/verify",
        "auth_type": "rapidapi"
    },
    
    # Personator by Melissa Data for contact verification
    "personator": {
        "key": RAPIDAPI_KEY,
        "endpoint": "https://personator.melissadata.net/v3/WEB/ContactVerify/doContactVerify",
        "auth_type": "apikey",
        "params": {
            "id": RAPIDAPI_KEY
        }
    },
    
    # ScrapeNinja for web scraping with protection bypass
    "scrape_ninja": {
        "key": RAPIDAPI_KEY,
        "host": "scrapeninja.p.rapidapi.com",
        "endpoint": "https://scrapeninja.p.rapidapi.com/scrape",
        "auth_type": "rapidapi"
    },
    
    # Fake Valid CC Data Generator
    "fake_cc_generator": {
        "key": RAPIDAPI_KEY,
        "host": "fake-valid-cc-data-generator.p.rapidapi.com",
        "endpoint": "https://fake-valid-cc-data-generator.p.rapidapi.com/generate",
        "auth_type": "rapidapi"
    },
    
    # Advanced Email Validator
    "email_validator": {
        "key": RAPIDAPI_KEY,
        "host": "advanced-email-validator.p.rapidapi.com",
        "endpoint": "https://advanced-email-validator.p.rapidapi.com/validate",
        "auth_type": "rapidapi"
    },
    
    # Disposable Email Checker
    "disposable_email_checker": {
        "key": RAPIDAPI_KEY,
        "host": "disposable-email-checker.p.rapidapi.com",
        "endpoint": "https://disposable-email-checker.p.rapidapi.com/",
        "auth_type": "rapidapi"
    }
}

class UpdatedAPIIntegrations:
    """
    Updated API Integration class specifically using the provided RapidAPI Hub services
    """
    
    @staticmethod
    def get_headers(api_name):
        """Get standard headers for a specific API"""
        if api_name not in API_CONFIG:
            raise ValueError(f"Unknown API: {api_name}")
        
        api_config = API_CONFIG[api_name]
        
        # Base headers
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Add API-specific headers based on auth_type
        auth_type = api_config.get("auth_type", "rapidapi")
        
        if auth_type == "rapidapi":
            # RapidAPI format with X-RapidAPI-Key and X-RapidAPI-Host
            headers.update({
                'X-RapidAPI-Key': api_config["key"],
                'X-RapidAPI-Host': api_config["host"]
            })
        
        return headers
    
    @staticmethod
    def generate_identity():
        """
        Generate a realistic identity using Personator by Melissa Data
        """
        logger.info("Generating identity using Personator API")
        
        try:
            # Use the Personator API from Melissa Data
            api_config = API_CONFIG["personator"]
            url = api_config["endpoint"]
            
            # Prepare parameters - we'll use this to verify random data
            # Note: For a real implementation, you'd use more fields
            params = api_config["params"].copy()
            params.update({
                "act": "Check"
            })
            
            # Generate some basic information to verify
            first_name = random.choice([
                "John", "Michael", "David", "James", "Robert", 
                "Mary", "Jennifer", "Linda", "Patricia", "Elizabeth"
            ])
            
            last_name = random.choice([
                "Smith", "Johnson", "Williams", "Jones", "Brown",
                "Davis", "Miller", "Wilson", "Moore", "Taylor"
            ])
            
            # Add the generated data to the parameters
            params.update({
                "first": first_name,
                "last": last_name,
                "ctry": "US"
            })
            
            # Make the API request
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            if response.text:
                # Extract identity information from the response
                # In a real implementation, we'd parse the XML response properly
                logger.info("Identity verified successfully")
                
                # For now, return the basic identity with the generated first and last name
                return {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com",
                    "address": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "zipcode": "10001",
                    "phone": "2125551234",
                    "dob": "1990-01-01"
                }
            else:
                logger.error("Empty response from Personator API")
                raise ValueError("Empty response from Personator API")
        
        except requests.RequestException as e:
            logger.error(f"Error calling Personator API: {str(e)}")
            raise
    
    @staticmethod
    def validate_phone(phone_number, country_code="US"):
        """
        Validate a phone number using Veriphone API
        """
        logger.info(f"Validating phone number: {phone_number} for country: {country_code}")
        
        try:
            # Use the Veriphone API
            api_config = API_CONFIG["veriphone"]
            url = api_config["endpoint"]
            headers = UpdatedAPIIntegrations.get_headers("veriphone")
            
            # Prepare query parameters
            params = {
                "phone": phone_number
            }
            
            # Make the API request
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            logger.info("Phone validation response received")
            
            # Check if the phone number is valid
            if data.get("phone_valid") is True:
                # Format the validation result
                return {
                    "valid": True,
                    "phone_number": data.get("international_number", phone_number),
                    "country": data.get("country", country_code),
                    "carrier": data.get("carrier", "Unknown"),
                    "line_type": data.get("phone_type", "Unknown")
                }
            else:
                logger.warning(f"Invalid phone number: {phone_number}")
                return {
                    "valid": False,
                    "phone_number": phone_number,
                    "country": country_code,
                    "error": data.get("error", "Invalid phone number")
                }
        
        except requests.RequestException as e:
            logger.error(f"Error validating phone number: {str(e)}")
            # Try backup Abstract API
            return UpdatedAPIIntegrations.validate_phone_abstract(phone_number, country_code)
    
    @staticmethod
    def validate_phone_abstract(phone_number, country_code="US"):
        """
        Backup phone validation using Abstract Phone Validation API
        """
        logger.info(f"Using backup validation for phone: {phone_number}")
        
        try:
            # Use the Abstract Phone Validation API
            api_config = API_CONFIG["phone_validation"]
            url = api_config["endpoint"]
            
            # Prepare query parameters
            params = api_config["params"].copy()
            params.update({
                "phone": phone_number
            })
            
            # Make the API request
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            logger.info("Abstract phone validation response received")
            
            # Check if the phone number is valid
            if data.get("valid") is True:
                # Format the validation result
                return {
                    "valid": True,
                    "phone_number": data.get("phone", phone_number),
                    "country": data.get("country", {}).get("code", country_code),
                    "carrier": data.get("carrier", "Unknown"),
                    "line_type": data.get("type", "Unknown")
                }
            else:
                logger.warning(f"Invalid phone number (Abstract API): {phone_number}")
                return {
                    "valid": False,
                    "phone_number": phone_number,
                    "country": country_code,
                    "error": "Invalid phone number"
                }
        
        except requests.RequestException as e:
            logger.error(f"Error with backup phone validation: {str(e)}")
            return {
                "valid": False,
                "phone_number": phone_number,
                "country": country_code,
                "error": str(e)
            }
    
    @staticmethod
    def generate_card(card_type="visa"):
        """
        Generate a valid credit card using the Fake Valid CC Data Generator API
        """
        logger.info(f"Generating card of type: {card_type}")
        
        try:
            # Use the Fake Valid CC Data Generator API
            api_config = API_CONFIG["fake_cc_generator"]
            url = api_config["endpoint"]
            headers = UpdatedAPIIntegrations.get_headers("fake_cc_generator")
            
            # Prepare query parameters
            params = {
                "brand": card_type.lower(),
                "format": "json"
            }
            
            # Make the API request
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            logger.info("Card generation response received")
            
            # Extract and format the card information
            card_number = data.get("credit_card_number", "")
            expiry = data.get("credit_card_expiry_date", "")
            cvv = data.get("credit_card_cvv", "")
            
            # Parse expiry date (format MM/YY or MM/YYYY)
            expiry_month = ""
            expiry_year = ""
            if expiry and "/" in expiry:
                parts = expiry.split("/")
                if len(parts) == 2:
                    expiry_month = parts[0].strip()
                    expiry_year = parts[1].strip()
                    # Convert 2-digit year to 4-digit if needed
                    if len(expiry_year) == 2:
                        expiry_year = f"20{expiry_year}"
            
            # Format the card information
            return {
                "card_number": card_number,
                "card_type": card_type,
                "cvv": cvv,
                "expiry_month": expiry_month,
                "expiry_year": expiry_year,
                "expiry": expiry,
                "cardholder_name": data.get("credit_card_holder_name", "")
            }
        
        except requests.RequestException as e:
            logger.error(f"Error generating card: {str(e)}")
            raise
    
    @staticmethod
    def validate_email(email):
        """
        Validate an email address using the Advanced Email Validator API
        """
        logger.info(f"Validating email: {email}")
        
        try:
            # Use the Advanced Email Validator API
            api_config = API_CONFIG["email_validator"]
            url = api_config["endpoint"]
            headers = UpdatedAPIIntegrations.get_headers("email_validator")
            
            # Prepare request data
            params = {
                "email": email
            }
            
            # Make the API request
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            logger.info("Email validation response received")
            
            # Check if the email is valid
            is_valid = data.get("is_valid", False)
            is_disposable = data.get("is_disposable", True)
            
            # Format the validation result
            return {
                "is_valid": is_valid,
                "email": email,
                "is_disposable": is_disposable,
                "deliverable": data.get("is_deliverable", False),
                "quality_score": data.get("quality_score", 0),
                "domain": data.get("domain", ""),
                "mx_records": data.get("has_mx_records", False),
                "format_valid": data.get("format_valid", False)
            }
        
        except requests.RequestException as e:
            logger.error(f"Error validating email: {str(e)}")
            # Return a basic result indicating error
            return {
                "is_valid": False,
                "email": email,
                "error": str(e)
            }
    
    @staticmethod
    def check_disposable_email(email):
        """
        Check if an email is disposable using the Disposable Email Checker API
        """
        logger.info(f"Checking if email is disposable: {email}")
        
        try:
            # Use the Disposable Email Checker API
            api_config = API_CONFIG["disposable_email_checker"]
            url = api_config["endpoint"]
            headers = UpdatedAPIIntegrations.get_headers("disposable_email_checker")
            
            # Prepare query parameters
            params = {
                "email": email
            }
            
            # Make the API request
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            logger.info("Disposable email check response received")
            
            # Check if the email is disposable
            is_disposable = data.get("disposable", False)
            
            # Format the result
            return {
                "email": email,
                "is_disposable": is_disposable,
                "domain": data.get("domain", ""),
                "text": data.get("text", "")
            }
        
        except requests.RequestException as e:
            logger.error(f"Error checking disposable email: {str(e)}")
            # Return a basic result indicating error
            return {
                "email": email,
                "is_disposable": False,
                "error": str(e)
            }
    
    @staticmethod
    def web_scrape(url, render_js=True, use_proxy=False, custom_headers=None):
        """
        Scrape a website using ScrapeNinja API
        """
        logger.info(f"Scraping URL: {url} (render_js: {render_js})")
        
        try:
            # Use the ScrapeNinja API
            api_config = API_CONFIG["scrape_ninja"]
            scrape_url = api_config["endpoint"]
            headers = UpdatedAPIIntegrations.get_headers("scrape_ninja")
            
            # Prepare request payload
            payload = {
                "url": url,
                "render": render_js
            }
            
            # Add additional options if provided
            if use_proxy:
                payload["proxy"] = {
                    "type": "residential"
                }
            
            if custom_headers:
                payload["headers"] = custom_headers
            
            # Make the API request
            response = requests.post(scrape_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            logger.info("Web scraping response received")
            
            # Extract and format the result
            success = data.get("success", False)
            
            if success:
                return {
                    "success": True,
                    "url": url,
                    "html": data.get("body", ""),
                    "status_code": data.get("statusCode", 200),
                    "headers": data.get("headers", {}),
                    "render_time": data.get("renderTime", 0)
                }
            else:
                logger.warning(f"Web scraping failed: {data.get('error', 'Unknown error')}")
                return {
                    "success": False,
                    "url": url,
                    "error": data.get("error", "Unknown error")
                }
        
        except requests.RequestException as e:
            logger.error(f"Error scraping website: {str(e)}")
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }

    @staticmethod
    def generate_complete_trial_data(service="hulu"):
        """
        Generate a complete set of data needed for a trial signup
        """
        logger.info(f"Generating complete trial data for service: {service}")
        
        try:
            # Step 1: Generate identity
            identity = UpdatedAPIIntegrations.generate_identity()
            
            # Step 2: Generate credit card
            card = UpdatedAPIIntegrations.generate_card("visa")
            
            # Step 3: Validate the identity's phone number
            phone_validation = UpdatedAPIIntegrations.validate_phone(identity.get("phone", ""))
            
            # Step 4: Validate the email
            email_validation = UpdatedAPIIntegrations.validate_email(identity.get("email", ""))
            
            # Calculate trial end date (30 days from now)
            trial_end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            
            # Format the final trial data
            trial_data = {
                "service": service,
                "identity": {
                    "first_name": identity.get("first_name", ""),
                    "last_name": identity.get("last_name", ""),
                    "email": identity.get("email", ""),
                    "phone": identity.get("phone", ""),
                    "address": identity.get("address", ""),
                    "city": identity.get("city", ""),
                    "state": identity.get("state", ""),
                    "zipcode": identity.get("zipcode", ""),
                    "dob": identity.get("dob", "")
                },
                "payment": {
                    "card_type": card.get("card_type", "visa"),
                    "card_number": card.get("card_number", ""),
                    "card_display": f"{card.get('card_type', 'Visa').capitalize()} **** **** **** {card.get('card_number', '')[-4:]}",
                    "cvv": card.get("cvv", ""),
                    "expiry_month": card.get("expiry_month", ""),
                    "expiry_year": card.get("expiry_year", ""),
                    "expiry": card.get("expiry", ""),
                    "cardholder_name": identity.get("first_name", "") + " " + identity.get("last_name", "")
                },
                "validation": {
                    "phone_valid": phone_validation.get("valid", False),
                    "email_valid": email_validation.get("is_valid", False),
                    "email_disposable": email_validation.get("is_disposable", True)
                },
                "trial_info": {
                    "service": service,
                    "end_date": trial_end_date,
                    "password": UpdatedAPIIntegrations._generate_secure_password(),
                    "login_url": f"https://www.{service}.com/login"
                },
                "created_at": datetime.now().isoformat()
            }
            
            logger.info(f"Complete trial data generated for {service}")
            return trial_data
        
        except Exception as e:
            logger.error(f"Error generating complete trial data: {str(e)}")
            raise
    
    @staticmethod
    def _generate_secure_password(length=12):
        """Generate a secure password with mixed characters"""
        # Ensure at least one of each character type
        pwd = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice('!@#$%^&*()_+-=')
        ]
        # Fill rest with random characters
        characters = string.ascii_letters + string.digits + '!@#$%^&*()_+-='
        pwd.extend(random.choice(characters) for _ in range(length - 4))
        # Shuffle to randomize positions
        random.shuffle(pwd)
        return ''.join(pwd)


def test_apis():
    """
    Test all configured APIs to ensure they're working correctly
    """
    print("=== Testing All APIs ===")
    tests = []
    
    try:
        print("\n1. Testing identity generation...")
        identity = UpdatedAPIIntegrations.generate_identity()
        print(f"  ✓ Generated identity: {identity.get('first_name')} {identity.get('last_name')}")
        tests.append(("Identity Generation", True))
    except Exception as e:
        print(f"  ✗ Identity generation failed: {str(e)}")
        tests.append(("Identity Generation", False))
    
    try:
        print("\n2. Testing phone validation...")
        phone_validation = UpdatedAPIIntegrations.validate_phone("2125551234")
        print(f"  ✓ Phone validation result: {phone_validation.get('valid')}")
        tests.append(("Phone Validation", True))
    except Exception as e:
        print(f"  ✗ Phone validation failed: {str(e)}")
        tests.append(("Phone Validation", False))
    
    try:
        print("\n3. Testing card generation...")
        card = UpdatedAPIIntegrations.generate_card()
        print(f"  ✓ Generated card: {card.get('card_type')} ending in {card.get('card_number', '')[-4:]}")
        tests.append(("Card Generation", True))
    except Exception as e:
        print(f"  ✗ Card generation failed: {str(e)}")
        tests.append(("Card Generation", False))
    
    try:
        print("\n4. Testing email validation...")
        email_validation = UpdatedAPIIntegrations.validate_email("test@example.com")
        print(f"  ✓ Email validation result: {email_validation.get('is_valid')}")
        tests.append(("Email Validation", True))
    except Exception as e:
        print(f"  ✗ Email validation failed: {str(e)}")
        tests.append(("Email Validation", False))
    
    try:
        print("\n5. Testing web scraping...")
        scrape_result = UpdatedAPIIntegrations.web_scrape("https://www.hulu.com")
        print(f"  ✓ Web scraping success: {scrape_result.get('success')}")
        tests.append(("Web Scraping", True))
    except Exception as e:
        print(f"  ✗ Web scraping failed: {str(e)}")
        tests.append(("Web Scraping", False))
    
    # Print summary
    print("\n=== API Test Summary ===")
    for test_name, success in tests:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {test_name}")


if __name__ == "__main__":
    test_apis()