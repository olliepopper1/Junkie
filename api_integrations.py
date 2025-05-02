"""
API Integrations for Trial Junkie
Provides connectivity to various external APIs for trial generation
"""
import os
import json
import logging
import requests
import random
import string
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("api_integrations")

# Load environment variables
load_dotenv()

# API keys from environment
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '')
PERSONATOR_API_KEY = os.getenv('PERSONATOR_API_KEY', RAPIDAPI_KEY)
VIRTUAL_NUMBER_API_KEY = os.getenv('VIRTUAL_NUMBER_API_KEY', RAPIDAPI_KEY)
FAKE_CARD_API_KEY = os.getenv('FAKE_CARD_API_KEY', RAPIDAPI_KEY)
VIRTUAL_CARD_API_KEY = os.getenv('VIRTUAL_CARD_API_KEY', RAPIDAPI_KEY)
TEMP_EMAIL_API_KEY = os.getenv('TEMP_EMAIL_API_KEY', RAPIDAPI_KEY)
TEMP_MAIL_BACKUP_API_KEY = os.getenv('TEMP_MAIL_BACKUP_API_KEY', RAPIDAPI_KEY)

# API configuration
API_CONFIG = {
    # Identity Generation API using RandomUser.me (free public API)
    "personator": {
        "key": "",
        "host": "",
        "endpoint": "https://randomuser.me/api/",
        "auth_type": "none",
        "content_type": "application/json"
    },
    
    # Personator Identity Verification API
    "personator_search": {
        "key": "api_key",  # Will be replaced at runtime
        "host": "personator-search-api.example.com",
        "endpoint": "https://personator-search-api.example.com/search",
        "auth_type": "authtoken",
        "content_type": "application/json"
    },
    
    # Phone Verification API using NumVerify
    "virtual_number": {
        "key": RAPIDAPI_KEY,
        "host": "numverify.p.rapidapi.com",
        "endpoint": "https://numverify.p.rapidapi.com/validate",
        "auth_type": "rapidapi",
        "content_type": "application/json"
    },
    
    # Backup Phone Verification using Phone Number Validation
    "virtual_number_backup": {
        "key": RAPIDAPI_KEY,
        "host": "phone-number-validation-api.p.rapidapi.com",
        "endpoint": "https://phone-number-validation-api.p.rapidapi.com/validate",
        "auth_type": "rapidapi",
        "content_type": "application/json"
    },
    
    # Credit Card Generation API (Primary)
    "fake_card": {
        "key": "api_key",  # Will be replaced at runtime
        "host": "random.api.randomkey.io",
        "endpoint": "https://random.api.randomkey.io/v1/ccn",
        "auth_type": "apikey",
        "content_type": "application/json"
    },
    
    # Credit Card Generation API (Backup)
    "fake_card_backup": {
        "key": RAPIDAPI_KEY,
        "host": "creditcards.p.rapidapi.com",
        "endpoint": "https://creditcards.p.rapidapi.com/creditcard/generate",
        "auth_type": "rapidapi",
        "content_type": "application/json"
    },
    
    # Virtual Card Issuing API
    "virtual_card": {
        "key": "api_key",  # Will be replaced at runtime
        "host": "random.api.randomkey.io",
        "endpoint": "https://random.api.randomkey.io/v1/virtualcard",
        "auth_type": "rapidapi",
        "content_type": "application/json"
    },
    
    # Email Validation API - ZeroBounce
    "email_validator": {
        "key": "api_key",  # Will be replaced at runtime
        "host": "api.zerobounce.net",
        "endpoint": "https://api.zerobounce.net/v2/validate",
        "auth_type": "apikey",
        "content_type": "application/json"
    },
    
    # Disposable Email Generator
    "temp_email": {
        "key": RAPIDAPI_KEY,
        "host": "tempmail42.p.rapidapi.com",
        "endpoint": "https://tempmail42.p.rapidapi.com/generate",
        "auth_type": "rapidapi",
        "content_type": "application/json"
    },
    
    # Backup Disposable Email
    "temp_mail_backup": {
        "key": RAPIDAPI_KEY,
        "host": "temp-mail17.p.rapidapi.com",
        "endpoint": "https://temp-mail17.p.rapidapi.com/api/v1/email/domain/list",
        "auth_type": "rapidapi",
        "content_type": "application/json"
    },
    
    # Web Scraping with ScrapeNinja
    "scrape_ninja": {
        "key": "api_key",  # Will be replaced at runtime
        "host": "scrapeninja.net",
        "endpoint": "https://scrapeninja.net/api/scrape",
        "auth_type": "apikey",
        "content_type": "application/json"
    },
    
    # Web Scraping with JavaScript rendering via ScrapeNinja
    "scrape_ninja_js": {
        "key": "api_key",  # Will be replaced at runtime
        "host": "scrapeninja.net",
        "endpoint": "https://scrapeninja.net/api/scrape-js",
        "auth_type": "apikey",
        "content_type": "application/json"
    }
}

class APIIntegrations:
    """
    API Integration class for calling external services
    """
    @staticmethod
    def get_headers(api_name):
        """Get standard headers for a specific API"""
        if api_name not in API_CONFIG:
            raise ValueError(f"Unknown API: {api_name}")
        
        api_config = API_CONFIG[api_name]
        
        # Set content type from configuration
        content_type = api_config.get("content_type", "application/json")
        
        # Base headers that most APIs use
        headers = {
            'Content-Type': content_type,
        }
        
        # Add API-specific headers based on auth_type
        auth_type = api_config.get("auth_type", "rapidapi")
        
        if auth_type == "rapidapi":
            # RapidAPI format with X-RapidAPI-Key and X-RapidAPI-Host
            headers.update({
                'X-RapidAPI-Key': api_config["key"],
                'X-RapidAPI-Host': api_config["host"],
            })
        elif auth_type == "apikey":
            # Standard API key authentication
            headers.update({
                'api-key': api_config["key"],
            })
        elif auth_type == "authtoken":
            # Auth token authentication (like Personator)
            headers.update({
                'authToken': api_config["key"],
            })
        
        return headers
    
    @staticmethod
    def generate_identity(country="US"):
        """Generate a realistic identity using RandomUser.me API"""
        logger.info(f"Generating identity for country: {country}")
        
        try:
            # Use the public RandomUser.me API
            url = API_CONFIG["personator"]["endpoint"]
            
            # Format query parameters for the API
            querystring = {"nat": country.lower() if len(country) == 2 else "us"}
            
            # Initialize response variable to avoid 'possibly unbound'
            response = None
            try:
                response = requests.get(url, params=querystring, timeout=10)
                response.raise_for_status()  # Raise an exception for HTTP errors
                
                # Parse the response
                data = response.json()
                
                # Basic validation
                if not data or "results" not in data or not data["results"]:
                    raise ValueError("Invalid response from RandomUser.me API")
                
                # RandomUser.me returns data in the 'results' array
                user = data["results"][0]
                
                # Extract name components
                name = user.get("name", {})
                first_name = name.get("first", "")
                last_name = name.get("last", "")
                
                # Extract location components
                location = user.get("location", {})
                
                # Extract street address
                street = location.get("street", {})
                street_number = street.get("number", "")
                street_name = street.get("name", "")
                address = f"{street_number} {street_name}".strip()
                
                # Extract other location components
                city = location.get("city", "")
                state = location.get("state", "")
                zipcode = location.get("postcode", "")
                
                # Format the date of birth
                dob = user.get("dob", {})
                dob_date = dob.get("date", "").split("T")[0] if "date" in dob else ""
                
                # Extract contact information
                email = user.get("email", "")
                phone = user.get("phone", "")
                
                logger.info("Identity generated successfully")
                
                return {
                    "first_name": first_name,
                    "last_name": last_name,
                    "address": address,
                    "city": city,
                    "state": state,
                    "zipcode": zipcode,
                    "phone": phone,
                    "email": email,
                    "dob": dob_date,
                    "ssn": user.get("id", {}).get("value", "")  # RandomUser.me provides SSN in id.value for some nationalities
                }
            except ValueError as e:
                # JSON parsing error
                logger.error(f"Error parsing Random User Generator API response: {e}")
                if response is not None:
                    logger.error(f"Response content: {response.text[:200]}...")
                raise
                
        except requests.Timeout:
            logger.error("RandomUser API request timed out")
            logger.info("Using fallback identity generation")
            return APIIntegrations._generate_fallback_identity()
        except requests.ConnectionError:
            logger.error("Connection error when calling RandomUser API")
            logger.info("Using fallback identity generation")
            return APIIntegrations._generate_fallback_identity()
        except requests.RequestException as e:
            logger.error(f"Error calling RandomUser API: {e}")
            logger.info("Using fallback identity generation")
            return APIIntegrations._generate_fallback_identity()
        except Exception as e:
            logger.error(f"Unexpected error in generate_identity: {e}")
            logger.info("Using fallback identity generation")
            return APIIntegrations._generate_fallback_identity()
    
    @staticmethod
    def _generate_fallback_identity():
        """Generate a fallback identity when API call fails"""
        # Simple fallback method
        first_names = ["John", "Jane", "Michael", "Sarah", "David"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        street_number = random.randint(100, 9999)
        street_name = random.choice(["Main", "Oak", "Maple", "Pine", "Cedar"])
        street_type = random.choice(["St", "Ave", "Blvd", "Dr", "Ln"])
        city = random.choice(["Los Angeles", "New York", "Chicago", "Houston", "Phoenix"])
        state = random.choice(["CA", "NY", "IL", "TX", "AZ"])
        zipcode = f"{random.randint(10000, 99999)}"
        
        phone = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        
        # Generate date of birth (18-70 years old)
        today = datetime.now()
        age = random.randint(18, 70)
        birth_year = today.year - age
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        dob = f"{birth_month}/{birth_day}/{birth_year}"
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "address": f"{street_number} {street_name} {street_type}",
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "phone": phone,
            "dob": dob,
            "ssn": "XXX-XX-XXXX"
        }
    
    @staticmethod
    def generate_virtual_number(country_code="US"):
        """Generate a virtual phone number for verification using Virtual Number API"""
        logger.info(f"Generating virtual number for country: {country_code}")
        
        try:
            # Try the primary Virtual Number API (Vonage)
            url = API_CONFIG["virtual_number"]["endpoint"]
            headers = APIIntegrations.get_headers("virtual_number")
            
            # Format payload according to Vonage Verify API specs
            payload = {
                "api_key": API_CONFIG["virtual_number"]["key"],
                "number": "",  # Will be generated by API
                "brand": "TrialJunkie",
                "code_length": 6,
                "lg": "en-us",
                "country": country_code
            }
            
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                # Check if the API returned an error
                if data.get("status") and data.get("status") != "0":
                    logger.error(f"Vonage API returned error: {data.get('error_text', 'Unknown error')}")
                    raise requests.RequestException(f"API error: {data.get('error_text', 'Unknown error')}")
                
                logger.info("Virtual phone number generated successfully")
                
                # Format expires_at to ISO format
                expires_at = datetime.now() + timedelta(minutes=30)
                
                return {
                    "phone_number": data.get("number", ""),
                    "country_code": country_code,
                    "verification_code": data.get("request_id", ""),  # Vonage uses request_id for verification
                    "expires_at": expires_at.isoformat()
                }
                
            except (requests.RequestException, ValueError) as primary_api_error:
                # Try backup API if primary fails
                logger.warning(f"Primary Virtual Number API failed: {primary_api_error}")
                logger.info("Trying backup Virtual Number API...")
                
                # Use the backup API (NumVerify)
                backup_url = API_CONFIG["virtual_number_backup"]["endpoint"]
                backup_headers = APIIntegrations.get_headers("virtual_number_backup")
                
                # Format query parameters according to NumVerify API specs
                number = f"1{random.randint(2000000000, 9999999999)}"  # Generate random US number
                params = {
                    "access_key": API_CONFIG["virtual_number_backup"]["key"],
                    "number": number
                }
                
                backup_response = requests.get(backup_url, headers=backup_headers, params=params, timeout=10)
                backup_response.raise_for_status()
                
                backup_data = backup_response.json()
                
                # Check if the API returned an error
                if backup_data.get("success") is False:
                    logger.error(f"NumVerify API returned error: {backup_data.get('error', {}).get('info', 'Unknown error')}")
                    raise requests.RequestException(f"Backup API error: {backup_data.get('error', {}).get('info', 'Unknown error')}")
                
                logger.info("Virtual phone number generated successfully via backup API")
                
                # Generate verification code and expiration (NumVerify doesn't provide these)
                verification_code = ''.join(random.choices(string.digits, k=6))
                expires_at = (datetime.now() + timedelta(minutes=30)).isoformat()
                
                return {
                    "phone_number": f"+{backup_data.get('country_prefix', '1')}{backup_data.get('number', number)}",
                    "country_code": backup_data.get("country_code", country_code),
                    "verification_code": verification_code,
                    "expires_at": expires_at
                }
                
        except requests.Timeout:
            logger.error("Virtual Number API request timed out")
            logger.info("Using fallback phone number generation")
            return APIIntegrations._generate_fallback_phone()
        except requests.ConnectionError:
            logger.error("Connection error when calling Virtual Number API")
            logger.info("Using fallback phone number generation")
            return APIIntegrations._generate_fallback_phone()
        except requests.RequestException as e:
            logger.error(f"Error calling Virtual Number API: {e}")
            logger.info("Using fallback phone number generation")
            return APIIntegrations._generate_fallback_phone()
        except Exception as e:
            logger.error(f"Unexpected error in generate_virtual_number: {e}")
            logger.info("Using fallback phone number generation")
            return APIIntegrations._generate_fallback_phone()
    
    @staticmethod
    def _generate_fallback_phone():
        """Generate a fallback phone number when API call fails"""
        area_code = random.choice(["213", "310", "415", "212", "312", "512", "202"])
        middle = random.randint(100, 999)
        end = random.randint(1000, 9999)
        phone_number = f"+1{area_code}{middle}{end}"
        
        # Generate a 6-digit verification code
        verification_code = ''.join(random.choices(string.digits, k=6))
        
        # Expires in 30 minutes
        expires_at = (datetime.now() + timedelta(minutes=30)).isoformat()
        
        return {
            "phone_number": phone_number,
            "country_code": "US",
            "verification_code": verification_code,
            "expires_at": expires_at
        }
    
    @staticmethod
    def generate_card(card_type="visa"):
        """Generate a valid credit card for verification"""
        logger.info(f"Generating card of type: {card_type}")
        normalized_type = card_type.lower()
        
        # First try to use our specialized card generator
        try:
            from utils.card_generator import CreditCardGenerator
            logger.info("Using enhanced card generator")
            return CreditCardGenerator.generate_card(normalized_type)
        except ImportError:
            logger.warning("Enhanced card generator not available, trying APIs...")
        
        # If enhanced generator is not available, try APIs
        try:
            # Use the primary Credit Card Generator API
            url = API_CONFIG["fake_card"]["endpoint"]
            headers = APIIntegrations.get_headers("fake_card")
            
            # Format query parameters according to the API
            querystring = {}
            if normalized_type in ["visa", "mastercard", "amex", "discover"]:
                querystring["brand"] = normalized_type
            
            # Make the API request
            response = requests.get(url, headers=headers, params=querystring, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            
            # Check if we have a proper response
            if not data:
                raise ValueError("Empty response from Credit Card Generator API")
                
            logger.info("Credit card generated successfully via API")
            
            # Format for our standard output
            card_info = {}
            
            # Check different response formats
            if isinstance(data, dict) and "CreditCard" in data:
                # New API format
                card_data = data["CreditCard"]
                card_info = {
                    "card_number": card_data.get("CardNumber", ""),
                    "card_type": normalized_type,
                    "cvv": card_data.get("CVV", ""),
                    "expiry_month": card_data.get("ExpiryMonth", ""),
                    "expiry_year": card_data.get("ExpiryYear", ""),
                    "cardholder_name": card_data.get("Name", "")
                }
            elif isinstance(data, dict):
                # Check for common field names in different APIs
                card_info = {
                    "card_number": data.get("CreditCardNumber", data.get("card_number", data.get("number", ""))),
                    "card_type": normalized_type,
                    "cvv": data.get("CVV", data.get("cvv", data.get("security_code", ""))),
                    "expiry_month": "",
                    "expiry_year": "",
                    "cardholder_name": data.get("CardHolderName", data.get("name", data.get("holder", "")))
                }
                
                # Handle expiration date in different formats
                expiry = data.get("ExpirationDate", data.get("expiry", data.get("expiration", "")))
                if expiry and "/" in expiry:
                    parts = expiry.split("/")
                    if len(parts) == 2:
                        card_info["expiry_month"] = parts[0].strip()
                        card_info["expiry_year"] = parts[1].strip()
            elif isinstance(data, list) and len(data) > 0:
                # Some APIs return a list of cards
                card_data = data[0]
                card_info = {
                    "card_number": card_data.get("CreditCardNumber", card_data.get("card_number", card_data.get("number", ""))),
                    "card_type": normalized_type,
                    "cvv": card_data.get("CVV", card_data.get("cvv", card_data.get("security_code", ""))),
                    "expiry_month": "",
                    "expiry_year": "",
                    "cardholder_name": card_data.get("CardHolderName", card_data.get("name", card_data.get("holder", "")))
                }
                
                # Handle expiration date in different formats
                expiry = card_data.get("ExpirationDate", card_data.get("expiry", card_data.get("expiration", "")))
                if expiry and "/" in expiry:
                    parts = expiry.split("/")
                    if len(parts) == 2:
                        card_info["expiry_month"] = parts[0].strip()
                        card_info["expiry_year"] = parts[1].strip()
            else:
                logger.warning("Unexpected response format from Credit Card API")
                raise ValueError("Unexpected response format")
            
            # Validate the card data
            if not card_info.get("card_number"):
                raise ValueError("No card number in response")
                
            return card_info
            
        except (requests.RequestException, ValueError) as primary_api_error:
            # Try backup API if primary fails
            logger.warning(f"Primary Credit Card API failed: {primary_api_error}")
            logger.info("Trying backup Credit Card API...")
            
            try:
                # Use the backup API
                backup_url = API_CONFIG["fake_card_backup"]["endpoint"]
                backup_headers = APIIntegrations.get_headers("fake_card_backup")
                
                # Format query parameters for backup API
                querystring = {}
                if normalized_type in ["visa", "mastercard", "amex", "discover"]:
                    querystring["type"] = normalized_type
                
                # Make the API request
                backup_response = requests.get(backup_url, headers=backup_headers, params=querystring, timeout=10)
                backup_response.raise_for_status()
                
                # Parse the response
                backup_data = backup_response.json()
                
                # Check if we have a proper response
                if not backup_data:
                    raise ValueError("Empty response from Backup Credit Card API")
                    
                logger.info("Credit card generated successfully via backup API")
                
                # Extract data from backup API response
                card_info = {}
                
                if isinstance(backup_data, dict):
                    card_info = {
                        "card_number": backup_data.get("card_number", backup_data.get("number", "")),
                        "card_type": normalized_type,
                        "cvv": backup_data.get("cvv", backup_data.get("cvc", "")),
                        "expiry_month": "",
                        "expiry_year": "",
                        "cardholder_name": backup_data.get("name", backup_data.get("holder", ""))
                    }
                    
                    # Handle expiration date formats
                    expiry = backup_data.get("expiry", backup_data.get("expiration", ""))
                    if expiry and "/" in expiry:
                        parts = expiry.split("/")
                        if len(parts) == 2:
                            card_info["expiry_month"] = parts[0].strip()
                            card_info["expiry_year"] = parts[1].strip()
                elif isinstance(backup_data, list) and len(backup_data) > 0:
                    first_card = backup_data[0]
                    card_info = {
                        "card_number": first_card.get("card_number", first_card.get("number", "")),
                        "card_type": normalized_type,
                        "cvv": first_card.get("cvv", first_card.get("cvc", "")),
                        "expiry_month": "",
                        "expiry_year": "",
                        "cardholder_name": first_card.get("name", first_card.get("holder", ""))
                    }
                    
                    # Handle expiration date formats
                    expiry = first_card.get("expiry", first_card.get("expiration", ""))
                    if expiry and "/" in expiry:
                        parts = expiry.split("/")
                        if len(parts) == 2:
                            card_info["expiry_month"] = parts[0].strip()
                            card_info["expiry_year"] = parts[1].strip()
                
                # Validate the card data
                if not card_info.get("card_number"):
                    raise ValueError("No card number in backup API response")
                    
                return card_info
                
            except (requests.RequestException, ValueError, Exception) as backup_api_error:
                logger.error(f"Backup Credit Card API also failed: {backup_api_error}")
                logger.info("Using fallback card generation")
                return APIIntegrations._generate_fallback_card(card_type)
        except Exception as e:
            logger.error(f"Unexpected error in generate_card: {e}")
            logger.info("Using fallback card generation")
            return APIIntegrations._generate_fallback_card(card_type)
    
    @staticmethod
    def _generate_fallback_card(card_type="visa"):
        """Generate a fallback credit card when API call fails"""
        try:
            # Try to use the enhanced card generator utility
            from utils.card_generator import CreditCardGenerator
            return CreditCardGenerator.generate_card(card_type)
        except ImportError:
            # If the utility is not available, use the basic generation method
            logger.warning("Enhanced card generator not found, using basic generation")
            
            card_types = {
                "visa": {
                    "prefix": "4",
                    "length": 16,
                    "cvv_length": 3
                },
                "mastercard": {
                    "prefix": "5",
                    "length": 16,
                    "cvv_length": 3
                },
                "amex": {
                    "prefix": "3",
                    "length": 15,
                    "cvv_length": 4
                },
                "discover": {
                    "prefix": "6",
                    "length": 16,
                    "cvv_length": 3
                }
            }
            
            card_info = card_types.get(card_type.lower(), card_types["visa"])
            
            # Generate card number with basic algorithm
            card_number = card_info["prefix"]
            remaining_digits = card_info["length"] - len(card_info["prefix"]) - 1
            card_number += ''.join(random.choices(string.digits, k=remaining_digits))
            
            # Add simple check digit (not full Luhn algorithm)
            last_digit = str(random.randint(0, 9))
            card_number += last_digit
            
            # Generate CVV
            cvv = ''.join(random.choices(string.digits, k=card_info["cvv_length"]))
            
            # Generate expiry date (1-5 years in the future)
            current_year = datetime.now().year
            future_year = current_year + random.randint(1, 5)
            future_month = random.randint(1, 12)
            
            # Format month and year
            month_str = f"{future_month:02d}"
            year_str = f"{future_year % 100:02d}"
            
            # Generate cardholder name
            first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", 
                         "Robert", "Emily", "Daniel", "Jessica", "Matthew"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", 
                         "Davis", "Garcia", "Rodriguez", "Wilson", "Martinez"]
            cardholder_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            
            return {
                "card_number": card_number,
                "card_type": card_type,
                "cvv": cvv,
                "expiry_month": month_str,
                "expiry_year": year_str,
                "expiry": f"{month_str}/{year_str}",
                "cardholder_name": cardholder_name
            }
    
    @staticmethod
    def generate_virtual_card(amount=0.00, currency="USD"):
        """Generate a virtual card for free trial using Virtual Card Issuing API"""
        logger.info(f"Generating virtual card with amount: {amount} {currency}")
        
        try:
            # Use the Virtual Card Issuing API
            url = API_CONFIG["virtual_card"]["endpoint"]
            headers = APIIntegrations.get_headers("virtual_card")
            
            # Format payload based on the API requirements
            querystring = {
                "amount": str(amount),
                "currency": currency,
                "type": "visa"  # Default to Visa cards
            }
            
            # Make the API request
            response = requests.get(url, headers=headers, params=querystring, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            
            # Check if we have a proper response
            if not data:
                raise ValueError("Empty response from Virtual Card API")
                
            logger.info("Virtual card generated successfully")
            
            # Format for our standard output
            card_info = {}
            
            # Extract card info from different response formats
            if isinstance(data, dict) and "card" in data:
                # Structured response with card object
                card_data = data["card"]
                card_info = {
                    "card_number": card_data.get("number", ""),
                    "card_type": "visa",  # Default for most virtual cards
                    "cvv": card_data.get("cvv", card_data.get("cvc", "")),
                    "expiry_month": card_data.get("exp_month", ""),
                    "expiry_year": card_data.get("exp_year", ""),
                    "expiry": f"{card_data.get('exp_month', '')}/{card_data.get('exp_year', '')}",
                    "cardholder_name": card_data.get("name", ""),
                    "amount": amount,
                    "currency": currency
                }
            elif isinstance(data, dict):
                # Direct card details in root object
                card_info = {
                    "card_number": data.get("number", data.get("card_number", "")),
                    "card_type": "visa",  # Default for most virtual cards
                    "cvv": data.get("cvv", data.get("cvc", data.get("security_code", ""))),
                    "expiry": data.get("expiry", data.get("expiration", "")),
                    "cardholder_name": data.get("name", data.get("cardholder", "")),
                    "amount": data.get("amount", amount),
                    "currency": data.get("currency", currency)
                }
                
                # Parse expiry into month/year if needed
                if card_info["expiry"] and "/" in card_info["expiry"]:
                    parts = card_info["expiry"].split("/")
                    if len(parts) == 2:
                        card_info["expiry_month"] = parts[0].strip()
                        card_info["expiry_year"] = parts[1].strip()
            
            # Validate the virtual card data
            if not card_info.get("card_number"):
                raise ValueError("No card number in Virtual Card API response")
                
            return card_info
            
        except (requests.RequestException, ValueError, Exception) as e:
            logger.error(f"Error calling Virtual Card API: {e}")
            logger.info("Using fallback virtual card generation")
            
            # Generate a fallback card with expiry details formatted
            fallback_card = APIIntegrations._generate_fallback_card("visa")
            
            # Add the amount and currency details
            fallback_card["amount"] = amount
            fallback_card["currency"] = currency
            
            # Extract expiry month and year if available
            if "expiry" in fallback_card and "/" in fallback_card["expiry"]:
                parts = fallback_card["expiry"].split("/")
                if len(parts) == 2:
                    fallback_card["expiry_month"] = parts[0].strip()
                    fallback_card["expiry_year"] = parts[1].strip()
            
            return fallback_card
    
    @staticmethod
    def validate_email(email):
        """
        Validate an email address using the Advanced Email Validator API
        
        Args:
            email (str): The email address to validate
            
        Returns:
            dict: Validation results including deliverability, quality score, etc.
        """
        logger.info(f"Validating email address: {email}")
        
        try:
            # Use the Advanced Email Validator API
            url = API_CONFIG["email_validator"]["endpoint"]
            headers = APIIntegrations.get_headers("email_validator")
            
            # Prepare query parameters
            params = {
                "email": email,
                "api_key": API_CONFIG["email_validator"]["key"]
            }
            
            # Make the API request
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            
            # Check if the API returned an error
            if data.get("success") is False:
                logger.error(f"Email Validator API returned error: {data.get('message', 'Unknown error')}")
                raise requests.RequestException(f"API error: {data.get('message', 'Unknown error')}")
            
            logger.info(f"Email validation successful for: {email}")
            
            # Return validation results
            return {
                "is_valid": data.get("is_valid", False),
                "deliverable": data.get("deliverable", False),
                "quality_score": data.get("quality_score", 0.0),
                "is_disposable": data.get("is_disposable", True),
                "is_role_account": data.get("is_role_account", False),
                "is_free_provider": data.get("is_free_provider", True),
                "has_mx_records": data.get("has_mx_records", False),
                "domain": data.get("domain", ""),
                "checked_at": datetime.now().isoformat()
            }
            
        except requests.Timeout:
            logger.error(f"Email validation request timed out for: {email}")
            return {"error": "Request timed out", "is_valid": False, "email": email}
        except requests.ConnectionError:
            logger.error(f"Connection error when validating email: {email}")
            return {"error": "Connection error", "is_valid": False, "email": email}
        except requests.RequestException as e:
            logger.error(f"Error validating email {email}: {e}")
            return {"error": str(e), "is_valid": False, "email": email}
        except Exception as e:
            logger.error(f"Unexpected error in validate_email: {e}")
            return {"error": str(e), "is_valid": False, "email": email}
    
    @staticmethod
    def generate_email():
        """Generate a disposable email using TempMail API from RapidAPI"""
        logger.info("Generating disposable email")
        
        try:
            # Use the TempMail API from RapidAPI
            url = API_CONFIG["temp_email"]["endpoint"]
            headers = APIIntegrations.get_headers("temp_email")
            
            # This API uses GET requests
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info("Disposable email generated successfully")
            
            # Extract email from the response based on the API format
            # Different APIs may return different formats
            email_address = ""
            password = ""
            inbox_url = ""
            
            if isinstance(data, dict):
                # Some APIs return a direct object
                email_address = data.get("email", "")
                password = data.get("password", "")
                inbox_url = data.get("inbox_url", "")
            elif isinstance(data, list) and len(data) > 0:
                # Some APIs return a list of emails
                first_email = data[0]
                if isinstance(first_email, dict):
                    email_address = first_email.get("email", "")
                    password = first_email.get("password", "")
                    inbox_url = first_email.get("inbox_url", "")
                else:
                    # Some APIs just return a list of email strings
                    email_address = str(first_email)
                    password = APIIntegrations._generate_secure_password()
            else:
                # If we can't parse the response, generate a fallback
                logger.warning("Unexpected response format from Email API")
                return APIIntegrations._generate_fallback_email()
            
            # If we couldn't extract an email, use fallback
            if not email_address:
                logger.warning("No email found in API response")
                return APIIntegrations._generate_fallback_email()
            
            # Expires in 24 hours typically
            expires_at = (datetime.now() + timedelta(days=1)).isoformat()
            
            # Validate the email using the email validator API if possible
            validation = {"is_valid": True, "deliverable": True}  # Default to optimistic values
            try:
                if email_address:
                    validation_result = APIIntegrations.validate_email(email_address)
                    logger.info(f"Email validation results: valid={validation_result.get('is_valid', False)}, deliverable={validation_result.get('deliverable', False)}")
                    validation = validation_result
            except Exception as e:
                logger.warning(f"Email validation failed: {e}")
            
            return {
                "email": email_address,
                "password": password,
                "inbox_url": inbox_url,
                "expires_at": expires_at,
                "validation": validation
            }
            
        except requests.RequestException as e:
            logger.error(f"Error calling Temp Email API: {e}")
            
            # Try the backup email API
            try:
                logger.info("Trying backup email API")
                url = API_CONFIG["temp_mail_backup"]["endpoint"]
                headers = APIIntegrations.get_headers("temp_mail_backup")
                
                # Get list of available domains first
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                domains_data = response.json()
                
                # Generate an email using one of the domains
                if isinstance(domains_data, list) and len(domains_data) > 0:
                    # Generate a username
                    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
                    # Get a domain from the list
                    domain = random.choice(domains_data)
                    if isinstance(domain, dict):
                        domain_name = domain.get("domain", "tempmail.com")
                    else:
                        domain_name = str(domain)
                    
                    email_address = f"{username}@{domain_name}"
                    password = APIIntegrations._generate_secure_password()
                    inbox_url = f"https://{domain_name}/inbox/{username}"
                    
                    logger.info("Backup disposable email generated successfully")
                    
                    return {
                        "email": email_address,
                        "password": password,
                        "inbox_url": inbox_url,
                        "expires_at": (datetime.now() + timedelta(days=1)).isoformat()
                    }
                else:
                    # If we couldn't get domains, use fallback
                    logger.error("Could not get valid domains from backup email API")
                    return APIIntegrations._generate_fallback_email()
                
            except requests.RequestException as e_backup:
                logger.error(f"Error calling Backup Temp Email API: {e_backup}")
                # Fallback to local generation
                logger.info("Using fallback email generation")
                return APIIntegrations._generate_fallback_email()
    
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
    
    @staticmethod
    def _generate_fallback_email():
        """Generate a fallback email when API calls fail"""
        # Generate a random username
        username_length = random.randint(6, 12)
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
        
        # Choose a disposable domain
        domains = ["tempmail.org", "disposable.com", "trialmail.com", "mailinator.com", "fakeemail.net"]
        domain = random.choice(domains)
        
        email = f"{username}@{domain}"
        
        # Generate a password using our secure method
        password = APIIntegrations._generate_secure_password()
        
        # Expires in 24 hours
        expires_at = (datetime.now() + timedelta(days=1)).isoformat()
        
        return {
            "email": email,
            "password": password,
            "inbox_url": f"https://{domain}/inbox/{username}",
            "expires_at": expires_at
        }
    
    @staticmethod
    def generate_complete_trial_data(service=None):
        """Generate a complete set of trial data with all required information"""
        logger.info(f"Generating complete trial data for service: {service}")
        
        # Generate all required data
        identity = APIIntegrations.generate_identity()
        card = APIIntegrations.generate_card()
        email = APIIntegrations.generate_email()
        phone = APIIntegrations.generate_virtual_number()
        
        # Calculate trial end date (default 30 days)
        trial_days = 30
        if service:
            # Different services have different trial periods
            service_trial_days = {
                "netflix": 30,
                "hulu": 30,
                "spotify": 30,
                "disney": 7,
                "youtube": 30,
                "apple": 7,
                "amazon": 30,
                "hbomax": 7,
                "paramount": 7,
                "peacock": 7
            }
            trial_days = service_trial_days.get(service.lower(), 30)
        
        trial_end_date = (datetime.now() + timedelta(days=trial_days)).strftime('%Y-%m-%d')
        generated_at = datetime.now().isoformat()
        
        # Combine all data into a comprehensive profile
        return {
            "service": service,
            "generated_at": generated_at,
            "trial_end_date": trial_end_date,
            "user_info": {
                "first_name": identity["first_name"],
                "last_name": identity["last_name"],
                "email": email["email"],
                "password": email["password"],
                "phone": phone["phone_number"],
                "dob": identity["dob"],
                "address": identity["address"],
                "city": identity["city"],
                "state": identity["state"],
                "zipcode": identity["zipcode"]
            },
            "payment_info": {
                "card_number": card["card_number"],
                "card_type": card["card_type"],
                "expiry": card["expiry"],
                "cvv": card["cvv"],
                "cardholder_name": f"{identity['first_name']} {identity['last_name']}"
            },
            "verification_info": {
                "email_inbox": email.get("inbox_url", ""),
                "sms_verification_code": phone.get("verification_code", ""),
                "email_expires_at": email.get("expires_at", ""),
                "phone_expires_at": phone.get("expires_at", "")
            }
        }
        
    @staticmethod
    def web_scrape(url, use_proxy=False, custom_headers=None, cookies=None, timeout=30, render_js=False):
        """
        Scrape a website using ScrapeNinja API with fallback to direct requests
        
        Args:
            url (str): The URL to scrape
            use_proxy (bool): Whether to use a residential proxy for scraping
            custom_headers (dict): Optional custom headers to use for the request
            cookies (dict): Optional cookies to send with the request
            timeout (int): Time in seconds to wait for the scraping to complete
            render_js (bool): Whether to use JavaScript rendering for the scrape
            
        Returns:
            dict: Scraped content and metadata
        """
        logger.info(f"Scraping URL: {url} {'with' if render_js else 'without'} JS rendering")
        
        # Default browser headers to simulate a real browser
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # Merge custom headers if provided
        if custom_headers:
            default_headers.update(custom_headers)
        
        try:
            # Try using ScrapeNinja API first
            # Select the appropriate API endpoint based on JS rendering needs
            api_name = "scrape_ninja_js" if render_js else "scrape_ninja"
            
            try:
                scrape_ninja_api = API_CONFIG[api_name]
                scrape_ninja_headers = APIIntegrations.get_headers(api_name)
                
                # Create the ScrapeNinja payload
                payload = {
                    "url": url,
                    "proxy": "residential" if use_proxy else "datacenter",
                    "timeout": timeout * 1000,  # Convert to milliseconds
                    "headers": default_headers
                }
                
                # Add cookies if provided
                if cookies:
                    payload["cookies"] = cookies
                
                logger.info(f"Making request to ScrapeNinja API ({api_name})")
                scrape_response = requests.post(
                    scrape_ninja_api["endpoint"],
                    headers=scrape_ninja_headers,
                    json=payload,
                    timeout=timeout + 5  # Add buffer to the timeout
                )
                scrape_response.raise_for_status()
                
                # Parse the response
                scrape_data = scrape_response.json()
                
                if scrape_data.get("error"):
                    logger.warning(f"ScrapeNinja API returned error: {scrape_data.get('error')}")
                    raise ValueError(f"ScrapeNinja API error: {scrape_data.get('error')}")
                
                logger.info(f"ScrapeNinja API successfully scraped {url}")
                
                # Extract the relevant content
                html_content = scrape_data.get("content", "")
                
                # Use the trafilatura library to extract the main content
                try:
                    import trafilatura
                    extracted_text = trafilatura.extract(html_content)
                    main_content = extracted_text if extracted_text else html_content
                except ImportError:
                    main_content = html_content
                
                return {
                    "content": main_content,
                    "raw_html": html_content,
                    "status_code": scrape_data.get("status_code", 200),
                    "headers": scrape_data.get("headers", {}),
                    "cookies": scrape_data.get("cookies", {}),
                    "url": url,
                    "proxy_used": use_proxy,
                    "js_rendered": render_js,
                    "method": "scrape_ninja"
                }
                
            except (requests.RequestException, ValueError) as e:
                logger.warning(f"ScrapeNinja API failed, falling back to direct request: {e}")
            
            # Fall back to direct request if ScrapeNinja fails
            logger.info(f"Falling back to direct HTTP request for {url}")
            response = requests.get(url, headers=default_headers, cookies=cookies, timeout=timeout)
            response.raise_for_status()
            
            logger.info(f"Successfully scraped URL using direct request: {url}")
            
            # Use the trafilatura library to extract the main content if available
            try:
                import trafilatura
                extracted_text = trafilatura.extract(response.text)
                main_content = extracted_text if extracted_text else response.text
            except ImportError:
                main_content = response.text
            
            return {
                "content": main_content,
                "raw_html": response.text,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "cookies": dict(response.cookies),
                "url": response.url,
                "proxy_used": False,
                "js_rendered": False,
                "method": "direct_request"
            }
            
        except requests.Timeout:
            logger.error(f"Scraping request timed out for URL: {url}")
            return {"error": "Request timed out", "url": url}
        except requests.ConnectionError:
            logger.error(f"Connection error when scraping URL: {url}")
            return {"error": "Connection error", "url": url}
        except requests.RequestException as e:
            logger.error(f"Error scraping URL {url}: {e}")
            return {"error": str(e), "url": url}
        except Exception as e:
            logger.error(f"Unexpected error in web_scrape: {e}")
            return {"error": str(e), "url": url}
    
    @staticmethod
    def create_trial_for_url(url):
        """
        Create a trial for any given URL using generic trial automation
        
        Args:
            url (str): The URL of the website to create a trial for
            
        Returns:
            dict: Trial data including automation results
        """
        logger.info(f"Creating trial for URL: {url}")
        
        # Generate all the necessary trial data
        trial_data = APIIntegrations.generate_complete_trial_data()
        user_info = trial_data["user_info"]
        
        try:
            try:
                # First attempt: Use regular browser automation
                # Import the generic trial automator to handle any URL
                from generic_trial_automation import GenericTrialAutomator
                
                # Create the automator (headless mode)
                automator = GenericTrialAutomator(headless=True)
                
                # Attempt to create the trial
                logger.info("Starting generic trial automation...")
                result = automator.create_trial(url, user_info)
                
                # Add the result information to our trial data
                trial_data["automation_result"] = result
                trial_data["success"] = result.get("success", False)
                trial_data["success_score"] = result.get("success_score", 0)
                trial_data["final_url"] = result.get("final_url", "")
                trial_data["category"] = result.get("category", "unknown")
                trial_data["service"] = "custom_url"  # Mark as custom URL trial
                
            except Exception as automation_error:
                # If browser automation fails, fallback to Web Scraping API
                logger.warning(f"Browser automation failed, falling back to Web Scraping API: {automation_error}")
                
                # Use Web Scraping API to get the page content
                scrape_result = APIIntegrations.web_scrape(url, use_proxy=True, timeout=60)
                
                if "error" in scrape_result:
                    logger.error(f"Web Scraping API fallback also failed: {scrape_result['error']}")
                    raise Exception(f"Both automation methods failed: {automation_error}. Web Scraping error: {scrape_result['error']}")
                
                # Successfully scraped the page, add to trial data
                trial_data.update({
                    "automation_result": {
                        "success": scrape_result.get("status_code") == 200,
                        "content_length": len(scrape_result.get("content", "")),
                        "method": "web_scraping_proxy"
                    },
                    "success": scrape_result.get("status_code") == 200,
                    "success_score": 0.7 if scrape_result.get("status_code") == 200 else 0.0,
                    "final_url": scrape_result.get("url", url),
                    "category": "scraped_content",
                    "service": "custom_url_scraped"
                })
                
                logger.info(f"Trial content retrieved successfully for URL: {url} using Web Scraping API")
            
            return trial_data
            
        except Exception as e:
            logger.error(f"Error creating trial for URL {url}: {str(e)}")
            # Still return the generated data even if automation failed
            trial_data["success"] = False
            trial_data["automation_result"] = {"error": str(e)}
            trial_data["service"] = "custom_url"
            return trial_data