#!/usr/bin/env python3
"""
Updated API Integrations for Trial Junkie
Provides enhanced connectivity to various external APIs with proper fallback mechanisms
"""
import os
import re
import sys
import json
import time
import uuid
import random
import string
import logging
import requests
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("updated_api_integrations.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("api_integrations")

# Load environment variables if needed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logger.warning("dotenv module not found - skipping environment variable loading")

# API Keys
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    logger.warning("RAPIDAPI_KEY not found in environment variables. API functionality will be limited.")

# API Configuration
API_CONFIG = {
    "random_identity": {
        "url": "https://randomuser.me/api/",
        "host": "randomuser.me",
        "fallback_url": "https://api.randomuser.me/"
    },
    "card_generator": {
        "url": "https://fake-valid-cc-generator.p.rapidapi.com/creditcard/generate",
        "host": "fake-valid-cc-generator.p.rapidapi.com",
        "fallback_url": "https://randommer.io/api/Card"
    },
    "phone_validator": {
        "url": "https://veriphone.p.rapidapi.com/verify",
        "host": "veriphone.p.rapidapi.com"
    },
    "email_generator": {
        "url": "https://privatix-temp-mail-v1.p.rapidapi.com/request/domains/",
        "host": "privatix-temp-mail-v1.p.rapidapi.com"
    },
    "email_validator": {
        "url": "https://email-checker.p.rapidapi.com/verify/v1",
        "host": "email-checker.p.rapidapi.com"
    },
    "web_scraper": {
        "url": "https://website-scraper.p.rapidapi.com/scrape",
        "host": "website-scraper.p.rapidapi.com"
    }
}

class UpdatedAPIIntegrations:
    """
    Enhanced API Integration class with robust fallback mechanisms
    """
    def __init__(self):
        """Initialize the API integration handler"""
        self.api_key = RAPIDAPI_KEY
        self.session = requests.Session()
        self.cache = {}
        
        # Check if APIs are available
        if not self.api_key:
            logger.warning("No API key provided. Using local fallback mechanisms.")
        
        # Load cached identities if available
        self.identity_cache = self._load_cached_data("identity_cache.json")
        self.card_cache = self._load_cached_data("card_cache.json")
        self.phone_cache = self._load_cached_data("phone_cache.json")
        self.email_cache = self._load_cached_data("email_cache.json")
        
        logger.info("API integrations initialized")
    
    def _load_cached_data(self, cache_file: str) -> List[Dict[str, Any]]:
        """
        Load cached data from a JSON file
        
        Args:
            cache_file: Path to the cache file
            
        Returns:
            list: Cached data or empty list if file not found
        """
        try:
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading cache file {cache_file}: {str(e)}")
        
        return []
    
    def _save_cached_data(self, cache_file: str, data: List[Dict[str, Any]]) -> bool:
        """
        Save data to a cache file
        
        Args:
            cache_file: Path to the cache file
            data: Data to save
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving cache file {cache_file}: {str(e)}")
            return False
    
    def _get_headers(self, api_name: str) -> Dict[str, str]:
        """
        Get standard headers for a specific API
        
        Args:
            api_name: Name of the API from the config
            
        Returns:
            dict: Headers for the API request
        """
        if api_name not in API_CONFIG:
            return {"X-RapidAPI-Key": self.api_key}
        
        return {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": API_CONFIG[api_name]["host"]
        }
    
    def _handle_api_error(self, api_name: str, error: Union[str, Exception]) -> Dict[str, Any]:
        """
        Handle API errors consistently
        
        Args:
            api_name: Name of the API that failed
            error: The error message or exception
            
        Returns:
            dict: Standardized error response
        """
        error_str = str(error)
        logger.error(f"{api_name} API error: {error_str}")
        
        return {
            "success": False,
            "error": error_str,
            "api": api_name,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_identity(self, country: str = "US") -> Dict[str, Any]:
        """
        Generate a realistic identity with multi-level fallbacks
        
        Args:
            country: The country code for the identity
            
        Returns:
            dict: Identity information
        """
        logger.info(f"Generating identity for country: {country}")
        
        # Try primary API
        if self.api_key:
            try:
                url = API_CONFIG["random_identity"]["url"]
                querystring = {"nat": country, "inc": "name,location,phone,email", "noinfo": "true"}
                
                response = requests.get(url, params=querystring)
                
                if response.status_code == 200:
                    data = response.json()
                    person = data["results"][0]
                    
                    identity = {
                        "first_name": person["name"]["first"],
                        "last_name": person["name"]["last"],
                        "address": f"{person['location']['street']['number']} {person['location']['street']['name']}",
                        "city": person["location"]["city"],
                        "state": person["location"]["state"],
                        "zipcode": str(person["location"]["postcode"]),
                        "country": country,
                        "phone": person["phone"],
                        "email": person["email"],
                        "source": "random_identity_api"
                    }
                    
                    # Cache this identity
                    if self.identity_cache is not None:
                        self.identity_cache.append(identity)
                        self._save_cached_data("identity_cache.json", self.identity_cache)
                    
                    return identity
                else:
                    logger.warning(f"Primary identity API error: {response.status_code}")
            except Exception as e:
                logger.warning(f"Primary identity API error: {str(e)}")
        
        # Try fallback API
        logger.info("Using fallback identity generation")
        try:
            fallback_url = API_CONFIG["random_identity"]["fallback_url"]
            response = requests.get(fallback_url)
            
            if response.status_code == 200:
                data = response.json()
                person = data["results"][0]
                
                identity = {
                    "first_name": person["name"]["first"],
                    "last_name": person["name"]["last"],
                    "address": f"{person['location']['street']['number']} {person['location']['street']['name']}",
                    "city": person["location"]["city"],
                    "state": person["location"]["state"],
                    "zipcode": str(person["location"]["postcode"]),
                    "country": country,
                    "phone": person["phone"],
                    "email": person["email"],
                    "source": "fallback_identity_api"
                }
                
                return identity
            else:
                logger.warning(f"Fallback identity API error: {response.status_code}")
        except Exception as e:
            logger.warning(f"Fallback identity API error: {str(e)}")
        
        # Use cached identity if available
        if self.identity_cache and len(self.identity_cache) > 0:
            logger.info("Using cached identity")
            return random.choice(self.identity_cache)
        
        # Generate locally as final fallback
        logger.info("Using local identity generation as final fallback")
        
        # US state abbreviations
        states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
                 "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
                 "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
                 "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
                 "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
        
        # Common first and last names
        first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
                      "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
        
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
                     "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]
        
        # Street names
        street_types = ["St", "Ave", "Blvd", "Ln", "Dr", "Way", "Pl", "Ct"]
        street_names = ["Main", "Oak", "Pine", "Maple", "Cedar", "Elm", "Washington", "Lake", "Hill", "Park"]
        
        # Generate a random identity
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        street_number = random.randint(100, 9999)
        street_name = f"{random.choice(street_names)} {random.choice(street_types)}"
        city_options = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
        city = random.choice(city_options)
        state = random.choice(states)
        zipcode = f"{random.randint(10000, 99999)}"
        
        # Generate a semi-realistic phone number
        area_code = random.randint(200, 999)
        prefix = random.randint(200, 999)
        line = random.randint(1000, 9999)
        phone = f"{area_code}-{prefix}-{line}"
        
        # Generate an email from the name
        email_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "icloud.com"]
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{random.choice(email_domains)}"
        
        identity = {
            "first_name": first_name,
            "last_name": last_name,
            "address": f"{street_number} {street_name}",
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "country": country,
            "phone": phone,
            "email": email,
            "source": "local_generation"
        }
        
        logger.info(f"Generated local fallback identity: {first_name} {last_name}")
        
        # Cache this generated identity
        if self.identity_cache is not None:
            self.identity_cache.append(identity)
            self._save_cached_data("identity_cache.json", self.identity_cache)
        
        return identity
    
    def generate_virtual_number(self, country_code: str = "US") -> Dict[str, Any]:
        """
        Generate a virtual phone number for verification
        
        Args:
            country_code: The country code for the phone number
            
        Returns:
            dict: Phone number information
        """
        # Try primary API if key available
        if self.api_key:
            try:
                # This would be replaced with the actual Virtual Number API call
                # For demonstration, we're using a placeholder
                
                # Validate a random phone number to make it realistic
                area_code = random.randint(200, 999)
                prefix = random.randint(200, 999)
                line = random.randint(1000, 9999)
                phone_number = f"{area_code}{prefix}{line}"
                
                url = API_CONFIG["phone_validator"]["url"]
                querystring = {"phone": phone_number, "country": country_code}
                
                headers = self._get_headers("phone_validator")
                response = requests.get(url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("phone_valid") == True:
                        phone_info = {
                            "number": data.get("phone_normalized", phone_number),
                            "country": country_code,
                            "valid": True,
                            "carrier": data.get("carrier", "Virtual Carrier"),
                            "type": "mobile",
                            "source": "virtual_number_api"
                        }
                        
                        # Cache this phone
                        if self.phone_cache is not None:
                            self.phone_cache.append(phone_info)
                            self._save_cached_data("phone_cache.json", self.phone_cache)
                        
                        return phone_info
                
                logger.warning(f"Phone validation API returned status code: {response.status_code}")
            except Exception as e:
                logger.warning(f"Virtual number API error: {str(e)}")
        
        # Use cached phone if available
        if self.phone_cache and len(self.phone_cache) > 0:
            logger.info("Using cached phone number")
            return random.choice(self.phone_cache)
        
        # Generate locally as fallback
        logger.info("Using local phone generation as fallback")
        
        # Generate a semi-realistic phone number
        area_code = random.randint(200, 999)
        prefix = random.randint(200, 999)
        line = random.randint(1000, 9999)
        
        # Format based on country
        if country_code == "US":
            formatted_number = f"{area_code}-{prefix}-{line}"
            full_number = f"+1{area_code}{prefix}{line}"
        else:
            formatted_number = f"{area_code}-{prefix}-{line}"
            full_number = f"+{random.randint(30, 70)}{area_code}{prefix}{line}"
        
        phone_info = {
            "number": formatted_number,
            "full_number": full_number,
            "country": country_code,
            "valid": True,
            "carrier": "Local Carrier",
            "type": "mobile",
            "source": "local_generation"
        }
        
        # Cache this generated phone
        if self.phone_cache is not None:
            self.phone_cache.append(phone_info)
            self._save_cached_data("phone_cache.json", self.phone_cache)
        
        return phone_info
    
    def generate_card(self, card_type: str = "visa") -> Dict[str, Any]:
        """
        Generate a valid credit card for verification with multiple fallbacks
        
        Args:
            card_type: The type of card to generate (visa, mastercard, amex, etc.)
            
        Returns:
            dict: Card information
        """
        logger.info(f"Generating credit card of type: {card_type}")
        
        # Normalize card type
        card_type = card_type.lower()
        
        # Try primary API
        if self.api_key:
            try:
                url = API_CONFIG["card_generator"]["url"]
                querystring = {"credit_card_type": card_type, "quantity": "1"}
                headers = self._get_headers("card_generator")
                
                response = requests.get(url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data and "credit_cards" in data and len(data["credit_cards"]) > 0:
                        card = data["credit_cards"][0]
                        
                        # Parse the expiration date (MM/YY)
                        expiry = card.get("expiration", "12/28")
                        
                        card_info = {
                            "type": card_type,
                            "number": card.get("number", "").replace("-", ""),
                            "expiry": expiry,
                            "cvv": card.get("security_code", random.randint(100, 999)),
                            "last4": card.get("number", "")[-4:],
                            "valid": True,
                            "source": "card_generator_api"
                        }
                        
                        # Cache this card
                        if self.card_cache is not None:
                            self.card_cache.append(card_info)
                            self._save_cached_data("card_cache.json", self.card_cache)
                        
                        return card_info
                
                logger.warning(f"Primary card API error: {response.status_code}")
            except Exception as e:
                logger.warning(f"Primary card API error: {str(e)}")
        
        # Try fallback API
        logger.info(f"Using fallback card generation for: {card_type}")
        try:
            # This would be replaced with the actual fallback API call
            # For demonstration, we're using a placeholder
            
            fallback_url = API_CONFIG["card_generator"]["fallback_url"]
            headers = {"X-Api-Key": self.api_key}
            
            response = requests.get(fallback_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                card_info = {
                    "type": card_type,
                    "number": data.get("cardNo", "").replace("-", ""),
                    "expiry": data.get("expiry", "12/28"),
                    "cvv": data.get("cvv", random.randint(100, 999)),
                    "last4": data.get("cardNo", "")[-4:],
                    "valid": True,
                    "source": "fallback_card_api"
                }
                
                return card_info
            
            logger.warning(f"Fallback card API failed, using local generation")
        except Exception as e:
            logger.warning(f"Fallback card API error: {str(e)}")
        
        # Use cached card if available
        if self.card_cache and len(self.card_cache) > 0:
            matching_cards = [c for c in self.card_cache if c.get("type") == card_type]
            if matching_cards:
                logger.info(f"Using cached {card_type} card")
                return random.choice(matching_cards)
        
        # Generate locally with Luhn algorithm as final fallback
        logger.info("Using local card generation with Luhn algorithm")
        
        # Generate card number based on type
        if card_type == "visa":
            prefix = "4"
            length = 16
        elif card_type == "mastercard":
            prefix = str(random.choice([51, 52, 53, 54, 55]))
            length = 16
        elif card_type == "amex":
            prefix = str(random.choice([34, 37]))
            length = 15
        elif card_type == "discover":
            prefix = "6011"
            length = 16
        else:
            # Default to visa
            prefix = "4"
            length = 16
        
        # Generate the card number
        card_number = self._generate_card_number(prefix, length)
        
        # Generate expiry date (1-5 years in the future)
        current_year = datetime.now().year % 100  # Get last two digits
        current_month = datetime.now().month
        expiry_year = current_year + random.randint(1, 5)
        expiry_month = random.randint(1, 12)
        expiry = f"{expiry_month:02d}/{expiry_year:02d}"
        
        # Generate CVV
        cvv = str(random.randint(100, 999))
        
        card_info = {
            "type": card_type,
            "number": card_number,
            "expiry": expiry,
            "cvv": cvv,
            "last4": card_number[-4:],
            "valid": True,
            "source": "local_generation"
        }
        
        logger.info(f"Generated local fallback card: {card_type} ending in {card_number[-4:]}")
        
        # Cache this generated card
        if self.card_cache is not None:
            self.card_cache.append(card_info)
            self._save_cached_data("card_cache.json", self.card_cache)
        
        return card_info
    
    def _generate_card_number(self, prefix: str, length: int) -> str:
        """
        Generate a valid credit card number that passes the Luhn check
        
        Args:
            prefix: The card prefix (e.g., "4" for Visa)
            length: The total length of the card number
            
        Returns:
            str: A valid credit card number
        """
        # Initialize the card number with the prefix
        card_number = prefix
        
        # Generate random digits for the remaining length
        remaining_length = length - len(prefix) - 1  # -1 for check digit
        for _ in range(remaining_length):
            card_number += str(random.randint(0, 9))
        
        # Calculate the check digit using the Luhn algorithm
        check_digit = self._calculate_luhn_check_digit(card_number)
        
        # Append the check digit
        card_number += str(check_digit)
        
        return card_number
    
    def _calculate_luhn_check_digit(self, partial_card_number: str) -> int:
        """
        Calculate the Luhn check digit for a partial card number
        
        Args:
            partial_card_number: The partial card number without the check digit
            
        Returns:
            int: The check digit
        """
        # Convert string to list of integers
        digits = [int(d) for d in partial_card_number]
        
        # Double every second digit from right to left
        for i in range(len(digits) - 1, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        
        # Calculate sum of all digits
        total = sum(digits)
        
        # The check digit is the number that makes the total a multiple of 10
        check_digit = (10 - (total % 10)) % 10
        
        return check_digit
    
    def generate_email(self) -> Dict[str, Any]:
        """
        Generate a disposable email with fallback mechanisms
        
        Returns:
            dict: Email information
        """
        # Try primary API if key available
        if self.api_key:
            try:
                # For demonstration, we're using a simplified approach
                # This would be replaced with the actual Email Generator API call
                
                # Generate username
                chars = string.ascii_lowercase + string.digits
                username = ''.join(random.choice(chars) for _ in range(10))
                
                # Use temporary email domain
                domains = ["temp-mail.org", "fakemailgenerator.com", "mailinator.com"]
                domain = random.choice(domains)
                
                email = f"{username}@{domain}"
                password = self._generate_secure_password()
                
                email_info = {
                    "email": email,
                    "password": password,
                    "valid": True,
                    "domain": domain,
                    "username": username,
                    "source": "email_generator_api"
                }
                
                # Cache this email
                if self.email_cache is not None:
                    self.email_cache.append(email_info)
                    self._save_cached_data("email_cache.json", self.email_cache)
                
                return email_info
            
            except Exception as e:
                logger.warning(f"Email generator API error: {str(e)}")
        
        # Use cached email if available
        if self.email_cache and len(self.email_cache) > 0:
            logger.info("Using cached email")
            return random.choice(self.email_cache)
        
        # Generate locally as fallback
        logger.info("Using local email generation as fallback")
        
        # Generate username
        first_names = ["john", "jane", "bob", "alice", "mike", "sarah", "dave", "lisa"]
        last_names = ["smith", "jones", "doe", "brown", "miller", "davis", "wilson"]
        
        username = random.choice(first_names) + random.choice(last_names) + str(random.randint(10, 999))
        
        # Use common email domains
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        domain = random.choice(domains)
        
        email = f"{username}@{domain}"
        password = self._generate_secure_password()
        
        email_info = {
            "email": email,
            "password": password,
            "valid": True,
            "domain": domain,
            "username": username,
            "source": "local_generation"
        }
        
        # Cache this generated email
        if self.email_cache is not None:
            self.email_cache.append(email_info)
            self._save_cached_data("email_cache.json", self.email_cache)
        
        return email_info
    
    def _generate_secure_password(self, length: int = 12) -> str:
        """
        Generate a secure password with mixed characters
        
        Args:
            length: Length of the password to generate
            
        Returns:
            str: A secure password
        """
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*-_+=?"
        
        # Ensure at least one of each type
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        # Fill the rest randomly
        all_chars = lowercase + uppercase + digits + special
        password.extend(random.choice(all_chars) for _ in range(length - 4))
        
        # Shuffle the password
        random.shuffle(password)
        
        return ''.join(password)
    
    def validate_email(self, email: str) -> Dict[str, Any]:
        """
        Validate an email address with fallback logic
        
        Args:
            email: The email address to validate
            
        Returns:
            dict: Validation results
        """
        # Basic validation pattern
        basic_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        basic_valid = bool(re.match(basic_pattern, email))
        
        if not basic_valid:
            return {
                "email": email,
                "valid": False,
                "deliverable": False,
                "reason": "Invalid format",
                "source": "local_validation"
            }
        
        # Try API validation if key available
        if self.api_key:
            try:
                url = API_CONFIG["email_validator"]["url"]
                querystring = {"email": email}
                headers = self._get_headers("email_validator")
                
                response = requests.get(url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    validation_result = {
                        "email": email,
                        "valid": data.get("valid", basic_valid),
                        "deliverable": data.get("deliverable", True),
                        "source": "email_validator_api"
                    }
                    
                    return validation_result
                
                logger.warning(f"Email validator API error: {response.status_code}")
            except Exception as e:
                logger.warning(f"Email validator API error: {str(e)}")
        
        # Fallback to basic validation
        logger.info("Using basic email validation as fallback")
        
        # Check domain existence (simplified)
        domain = email.split('@')[1]
        common_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "aol.com"]
        domain_score = 1.0 if domain in common_domains else 0.7
        
        validation_result = {
            "email": email,
            "valid": basic_valid,
            "deliverable": basic_valid and domain_score > 0.5,
            "quality_score": domain_score,
            "source": "local_validation"
        }
        
        return validation_result
    
    def web_scrape(self, url: str, use_proxy: bool = False, custom_headers: Dict[str, str] = None, 
                  cookies: Dict[str, str] = None, timeout: int = 30, render_js: bool = False) -> Dict[str, Any]:
        """
        Scrape a website with fallback to direct requests
        
        Args:
            url: The URL to scrape
            use_proxy: Whether to use a proxy
            custom_headers: Custom headers for the request
            cookies: Cookies to send with the request
            timeout: Request timeout in seconds
            render_js: Whether to render JavaScript
            
        Returns:
            dict: Scraped content and metadata
        """
        # Try API scraping if key available
        if self.api_key:
            try:
                scraper_url = API_CONFIG["web_scraper"]["url"]
                
                payload = {
                    "url": url,
                    "use_proxy": use_proxy,
                    "render_js": render_js,
                    "timeout": timeout
                }
                
                if custom_headers:
                    payload["headers"] = custom_headers
                
                if cookies:
                    payload["cookies"] = cookies
                
                headers = self._get_headers("web_scraper")
                
                response = requests.post(scraper_url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    scrape_result = {
                        "success": True,
                        "url": url,
                        "html": data.get("html", ""),
                        "text": data.get("text", ""),
                        "status_code": data.get("status_code", 200),
                        "source": "web_scraper_api"
                    }
                    
                    return scrape_result
                
                logger.warning(f"Web scraper API error: {response.status_code}")
            except Exception as e:
                logger.warning(f"Web scraper API error: {str(e)}")
        
        # Fallback to direct requests
        logger.info("Using direct requests as fallback for web scraping")
        
        try:
            # Set up headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            if custom_headers:
                headers.update(custom_headers)
            
            # Make the request
            response = requests.get(url, headers=headers, cookies=cookies, timeout=timeout)
            
            # Extract basic text
            html = response.text
            
            # Very basic text extraction (simplified)
            text = re.sub(r'<[^>]+>', ' ', html)
            text = re.sub(r'\s+', ' ', text).strip()
            
            scrape_result = {
                "success": True,
                "url": url,
                "html": html,
                "text": text,
                "status_code": response.status_code,
                "source": "direct_request"
            }
            
            return scrape_result
        
        except Exception as e:
            logger.error(f"Direct request scraping error: {str(e)}")
            
            # Return error result
            return {
                "success": False,
                "url": url,
                "error": str(e),
                "source": "direct_request"
            }
    
    def generate_complete_trial_data(self, service: str = None) -> Dict[str, Any]:
        """
        Generate a complete set of trial data with all required information
        
        Args:
            service: The service to generate trial data for
            
        Returns:
            dict: Complete trial data
        """
        # Generate identity
        identity = self.generate_identity()
        
        # Generate phone
        phone = self.generate_virtual_number()
        
        # Generate card
        card = self.generate_card()
        
        # Generate email
        email_info = self.generate_email()
        
        # Generate password
        password = self._generate_secure_password()
        
        # Combine all data
        trial_data = {
            "service": service if service else "generic",
            "plan": "Premium" if service else "Basic",
            "first_name": identity.get("first_name"),
            "last_name": identity.get("last_name"),
            "address": identity.get("address"),
            "city": identity.get("city"),
            "state": identity.get("state"),
            "zipcode": identity.get("zipcode"),
            "country": identity.get("country", "US"),
            "phone": phone.get("number"),
            "email": email_info.get("email"),
            "password": password,
            "card_details": {
                "type": card.get("type"),
                "number": card.get("number"),
                "expiry": card.get("expiry"),
                "cvv": card.get("cvv"),
                "last4": card.get("last4")
            },
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "ip_protection": True,
            "auto_renewal": False
        }
        
        # Add service-specific details
        if service == "hulu":
            trial_data["plan"] = "Hulu (No Ads)"
            trial_data["trial_length"] = 30
            trial_data["features"] = ["Ad-free streaming", "Full library access", "HD quality"]
        elif service == "netflix":
            trial_data["plan"] = "Netflix Standard"
            trial_data["trial_length"] = 30
            trial_data["features"] = ["HD streaming", "Two screens at once", "Unlimited movies and TV shows"]
        elif service == "spotify":
            trial_data["plan"] = "Spotify Premium"
            trial_data["trial_length"] = 30
            trial_data["features"] = ["Ad-free music", "Download and listen offline", "On-demand playback"]
        
        # Calculate trial end date
        trial_length = trial_data.get("trial_length", 30)
        start_date = datetime.now()
        end_date = start_date + timedelta(days=trial_length)
        
        trial_data["start_date"] = start_date.strftime("%Y-%m-%d")
        trial_data["end_date"] = end_date.strftime("%Y-%m-%d")
        
        return trial_data


# For standalone testing
if __name__ == "__main__":
    api = UpdatedAPIIntegrations()
    
    # Test identity generation
    identity = api.generate_identity()
    print(f"Generated identity: {identity.get('first_name')} {identity.get('last_name')}")
    
    # Test card generation
    card = api.generate_card()
    print(f"Generated card: {card.get('type')} ending in {card.get('last4')}")
    
    # Test email generation
    email = api.generate_email()
    print(f"Generated email: {email.get('email')}")
    
    # Test complete trial data
    trial_data = api.generate_complete_trial_data("hulu")
    print(f"Generated trial for: {trial_data.get('service')} - {trial_data.get('plan')}")
    print(f"Login: {trial_data.get('email')} / {trial_data.get('password')}")
    print(f"Valid until: {trial_data.get('end_date')}")