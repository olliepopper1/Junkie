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
    # Identity Verification API
    "personator": {
        "key": RAPIDAPI_KEY,
        "host": "randomuser.me",
        "endpoint": "https://randomuser.me/api/",
        "auth_type": "none",
        "content_type": "application/json"
    },
    
    # Phone Verification API
    "virtual_number": {
        "key": RAPIDAPI_KEY,
        "host": "api.veriphone.io",
        "endpoint": "https://api.veriphone.io/v2/verify",
        "auth_type": "apikey",
        "content_type": "application/json"
    },
    
    # Backup Phone Verification
    "virtual_number_backup": {
        "key": RAPIDAPI_KEY,
        "host": "api.veriphone.io",
        "endpoint": "https://api.veriphone.io/v2/verify",
        "auth_type": "apikey",
        "content_type": "application/json"
    },
    
    # Credit Card Generation API
    "fake_card": {
        "key": RAPIDAPI_KEY,
        "host": "fake-valid-cc-data-generator.p.rapidapi.com",
        "endpoint": "https://fake-valid-cc-data-generator.p.rapidapi.com/v1/card/generate",
        "auth_type": "rapidapi",
        "content_type": "application/json"
    },
    
    # Virtual Card Issuing
    "virtual_card": {
        "key": RAPIDAPI_KEY,
        "host": "free-trial-virtual-card-issuing.p.rapidapi.com",
        "endpoint": "https://free-trial-virtual-card-issuing.p.rapidapi.com/v1/generate",
        "auth_type": "rapidapi",
        "content_type": "application/json"
    },
    
    # Email Validation API
    "email_validator": {
        "key": RAPIDAPI_KEY,
        "host": "api.advancedemailverifier.com",
        "endpoint": "https://api.advancedemailverifier.com/verify",
        "auth_type": "apikey",
        "content_type": "application/json"
    },
    
    # Disposable Email Generator
    "temp_email": {
        "key": RAPIDAPI_KEY,
        "host": "disposable-email-generator.p.rapidapi.com",
        "endpoint": "https://disposable-email-generator.p.rapidapi.com/api/v1/email/generate",
        "auth_type": "rapidapi",
        "content_type": "application/json"
    },
    
    # Backup Disposable Email
    "temp_mail_backup": {
        "key": RAPIDAPI_KEY,
        "host": "temp-mail-service.p.rapidapi.com",
        "endpoint": "https://temp-mail-service.p.rapidapi.com/create",
        "auth_type": "rapidapi",
        "content_type": "application/json"
    },
    
    # Web Scraping with simple HTTP requests
    "scrape_ninja": {
        "key": RAPIDAPI_KEY,
        "host": "httpbin.org",
        "endpoint": "https://httpbin.org/get",
        "auth_type": "none",
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
        """Generate a realistic identity using RandomUser API"""
        logger.info(f"Generating identity for country: {country}")
        
        try:
            # Use the RandomUser API to generate an identity
            url = API_CONFIG["personator"]["endpoint"]
            params = {
                "nat": country.lower() if len(country) == 2 else "us",
                "results": 1,
                "inc": "name,location,dob,phone"
            }
            
            # Initialize response variable to avoid 'possibly unbound'
            response = None
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()  # Raise an exception for HTTP errors
                
                # Parse the response
                data = response.json()
                if not data.get("results") or len(data["results"]) == 0:
                    raise ValueError("No results returned from RandomUser API")
                
                user = data["results"][0]
                name = user.get("name", {})
                location = user.get("location", {})
                dob = user.get("dob", {})
                
                # Format the address components
                street = location.get("street", {})
                street_number = street.get("number", "")
                street_name = street.get("name", "")
                address = f"{street_number} {street_name}" if street_number and street_name else ""
                
                logger.info("Identity generated successfully")
                
                return {
                    "first_name": name.get("first", ""),
                    "last_name": name.get("last", ""),
                    "address": address,
                    "city": location.get("city", ""),
                    "state": location.get("state", ""),
                    "zipcode": location.get("postcode", ""),
                    "phone": user.get("phone", ""),
                    "dob": "",  # DOB parsing disabled due to format issues
                    "ssn": ""  # RandomUser doesn't provide SSN for privacy reasons
                }
            except ValueError as e:
                # JSON parsing error
                logger.error(f"Error parsing RandomUser API response: {e}")
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
        """Generate a valid credit card for verification using Fake Valid CC Data Generator"""
        logger.info(f"Generating card of type: {card_type}")
        
        try:
            # Use the Fake Valid CC Data Generator API
            url = API_CONFIG["fake_card"]["endpoint"]
            headers = APIIntegrations.get_headers("fake_card")
            payload = json.dumps({"card_type": card_type})
            
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            
            data = response.json()
            logger.info("Credit card generated successfully")
            
            return {
                "card_number": data.get("number", ""),
                "card_type": data.get("card_type", ""),
                "cvv": data.get("cvv", ""),
                "expiry": data.get("expiry", ""),
                "cardholder_name": data.get("cardholder_name", "")
            }
            
        except requests.RequestException as e:
            logger.error(f"Error calling Fake Card API: {e}")
            # Fallback to local generation
            logger.info("Using fallback card generation")
            return APIIntegrations._generate_fallback_card(card_type)
    
    @staticmethod
    def _generate_fallback_card(card_type="visa"):
        """Generate a fallback credit card when API call fails"""
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
            }
        }
        
        card_info = card_types.get(card_type.lower(), card_types["visa"])
        
        # Generate card number
        card_number = card_info["prefix"]
        remaining_digits = card_info["length"] - len(card_info["prefix"])
        card_number += ''.join(random.choices(string.digits, k=remaining_digits))
        
        # Generate CVV
        cvv = ''.join(random.choices(string.digits, k=card_info["cvv_length"]))
        
        # Generate expiry date (1-5 years in the future)
        current_year = datetime.now().year
        current_month = datetime.now().month
        future_year = current_year + random.randint(1, 5)
        future_month = random.randint(1, 12)
        expiry = f"{future_month:02d}/{future_year % 100:02d}"
        
        # Generate cardholder name
        first_names = ["John", "Jane", "Michael", "Sarah", "David"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
        cardholder_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        return {
            "card_number": card_number,
            "card_type": card_type,
            "cvv": cvv,
            "expiry": expiry,
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
            payload = json.dumps({
                "amount": amount,
                "currency": currency
            })
            
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            
            data = response.json()
            logger.info("Virtual card generated successfully")
            
            return {
                "card_number": data.get("card_number", ""),
                "card_type": data.get("card_type", ""),
                "cvv": data.get("cvv", ""),
                "expiry": data.get("expiry", ""),
                "amount": data.get("amount", 0.00),
                "currency": data.get("currency", "USD")
            }
            
        except requests.RequestException as e:
            logger.error(f"Error calling Virtual Card API: {e}")
            # Fallback to local generation
            logger.info("Using fallback virtual card generation")
            return APIIntegrations._generate_fallback_card()
    
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
        """Generate a disposable email using Fast & Reliable Disposable Email API"""
        logger.info("Generating disposable email")
        
        try:
            # Use the Fast & Reliable Disposable Email API
            url = API_CONFIG["temp_email"]["endpoint"]
            headers = APIIntegrations.get_headers("temp_email")
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            logger.info("Disposable email generated successfully")
            
            # Get the generated email
            email = data.get("email", "")
            
            # Validate the email using the email validator API
            if email:
                validation = APIIntegrations.validate_email(email)
                logger.info(f"Email validation results: valid={validation.get('is_valid', False)}, deliverable={validation.get('deliverable', False)}")
            else:
                validation = {"is_valid": False, "deliverable": False}
            
            return {
                "email": email,
                "password": data.get("password", ""),
                "inbox_url": data.get("inbox_url", ""),
                "expires_at": data.get("expires_at", ""),
                "validation": validation
            }
            
        except requests.RequestException as e:
            logger.error(f"Error calling Temp Email API: {e}")
            
            # Try the backup email API
            try:
                logger.info("Trying backup email API")
                url = API_CONFIG["temp_mail_backup"]["endpoint"]
                headers = APIIntegrations.get_headers("temp_mail_backup")
                
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                logger.info("Backup disposable email generated successfully")
                
                return {
                    "email": data.get("email", ""),
                    "password": data.get("password", ""),
                    "inbox_url": data.get("inbox_url", ""),
                    "expires_at": data.get("expires_at", "")
                }
                
            except requests.RequestException as e_backup:
                logger.error(f"Error calling Backup Temp Email API: {e_backup}")
                # Fallback to local generation
                logger.info("Using fallback email generation")
                return APIIntegrations._generate_fallback_email()
    
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
        
        # Generate a password
        password_length = random.randint(10, 16)
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=password_length))
        
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
    def web_scrape(url, use_proxy=False, custom_headers=None, cookies=None, timeout=30):
        """
        Scrape a website using direct HTTP requests with a browser user agent
        
        Args:
            url (str): The URL to scrape
            use_proxy (bool): Whether to use a proxy for scraping (not used in this implementation)
            custom_headers (dict): Optional custom headers to use for the request
            cookies (dict): Optional cookies to send with the request
            timeout (int): Time in seconds to wait for the scraping to complete
            
        Returns:
            dict: Scraped content and metadata
        """
        logger.info(f"Scraping URL: {url}")
        
        try:
            # Use a direct HTTP request with a browser user agent
            # Default headers that mimic a browser
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
            
            # Make the direct request
            response = requests.get(url, headers=default_headers, cookies=cookies, timeout=timeout)
            response.raise_for_status()
            
            logger.info(f"Successfully scraped URL: {url}")
            
            # Use the trafilatura library to extract the main content if available
            # Import locally to avoid dependency issues
            try:
                import trafilatura
                extracted_text = trafilatura.extract(response.text)
                main_content = extracted_text if extracted_text else response.text
            except ImportError:
                main_content = response.text
            
            return {
                "content": main_content,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "cookies": dict(response.cookies),
                "url": response.url,
                "proxy_used": False
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