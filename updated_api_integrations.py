"""
Updated API Integrations for Trial Junkie
Provides connectivity to various external APIs for trial generation
with robust fallback mechanisms
"""
import os
import json
import random
import string
import logging
import sys
import requests
import traceback
from datetime import datetime, timedelta
import re
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_integrations.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("api_integrations")

# Load environment variables
load_dotenv()

class UpdatedAPIIntegrations:
    """
    Updated API Integration class for calling external services with fallbacks
    """
    
    def __init__(self):
        """Initialize the API integrations with API keys from environment"""
        self.rapidapi_key = os.getenv("RAPIDAPI_KEY", "")
        if not self.rapidapi_key:
            logger.warning("RAPIDAPI_KEY not found in environment variables")
        
        # Service-specific API keys (fallback to RAPIDAPI_KEY if not specified)
        self.identity_api_key = os.getenv("IDENTITY_API_KEY", self.rapidapi_key)
        self.phone_api_key = os.getenv("PHONE_API_KEY", self.rapidapi_key)
        self.card_api_key = os.getenv("CARD_API_KEY", self.rapidapi_key)
        self.virtual_card_api_key = os.getenv("VIRTUAL_CARD_API_KEY", self.rapidapi_key)
        self.email_api_key = os.getenv("EMAIL_API_KEY", self.rapidapi_key)
        self.scraper_api_key = os.getenv("SCRAPER_API_KEY", self.rapidapi_key)
    
    def get_headers(self, api_name):
        """Get standard headers for a specific API"""
        hosts = {
            "identity": "random-identity-generator.p.rapidapi.com",
            "identity_fallback": "random-data-api.p.rapidapi.com",
            "phone": "veriphone.p.rapidapi.com",
            "phone_fallback": "phone-validator-and-verification.p.rapidapi.com",
            "card": "fake-valid-cc-data-generator.p.rapidapi.com",
            "card_fallback": "credit-card-validator-generator.p.rapidapi.com",
            "virtual_card": "virtual-cards-issuance.p.rapidapi.com",
            "email": "validect-email-verification-v1.p.rapidapi.com",
            "email_fallback": "email-validator-and-verifier.p.rapidapi.com",
            "scraper": "website-scraper-api.p.rapidapi.com",
            "scraper_fallback": "scrapingant.p.rapidapi.com"
        }
        
        api_keys = {
            "identity": self.identity_api_key,
            "identity_fallback": self.identity_api_key,
            "phone": self.phone_api_key,
            "phone_fallback": self.phone_api_key,
            "card": self.card_api_key,
            "card_fallback": self.card_api_key,
            "virtual_card": self.virtual_card_api_key,
            "email": self.email_api_key,
            "email_fallback": self.email_api_key,
            "scraper": self.scraper_api_key,
            "scraper_fallback": self.scraper_api_key
        }
        
        if api_name not in hosts:
            logger.error(f"Unknown API name: {api_name}")
            return {}
        
        return {
            "X-RapidAPI-Key": api_keys.get(api_name, self.rapidapi_key),
            "X-RapidAPI-Host": hosts.get(api_name, ""),
            "Content-Type": "application/json"
        }
    
    def generate_identity(self, country="US"):
        """Generate a realistic identity using Random Identity Generator API"""
        logger.info(f"Generating identity for country: {country}")
        
        try:
            # Primary API: Random Identity Generator
            headers = self.get_headers("identity")
            url = "https://random-identity-generator.p.rapidapi.com/"
            
            # Make request
            response = requests.get(
                url, 
                headers=headers, 
                params={"locale": country.lower()}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Transform the API response into our standard format
                identity = {
                    "first_name": data.get("first_name", ""),
                    "last_name": data.get("last_name", ""),
                    "address": data.get("street", ""),
                    "city": data.get("city", ""),
                    "state": data.get("state", ""),
                    "zipcode": data.get("zip", ""),
                    "country": data.get("country", country),
                    "phone": data.get("phone", ""),
                    "email": data.get("email", ""),
                    "dob": data.get("dob", ""),
                    "gender": data.get("gender", "")
                }
                
                logger.info(f"Generated identity: {identity['first_name']} {identity['last_name']}")
                return identity
            else:
                logger.warning(f"Primary identity API error: {response.status_code}")
                
                # Try fallback API
                return self._generate_fallback_identity(country)
                
        except Exception as e:
            logger.error(f"Error in identity generation: {str(e)}")
            traceback.print_exc()
            
            # Use fallback identity generation
            return self._generate_fallback_identity(country)
    
    def _generate_fallback_identity(self, country="US"):
        """Generate a fallback identity when API call fails"""
        logger.info("Using fallback identity generation")
        
        try:
            # Try alternative Random Data API
            headers = self.get_headers("identity_fallback")
            url = "https://random-data-api.p.rapidapi.com/users/random_user"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Format the response to our standard format
                identity = {
                    "first_name": data.get("first_name", ""),
                    "last_name": data.get("last_name", ""),
                    "address": data.get("address", {}).get("street_address", ""),
                    "city": data.get("address", {}).get("city", ""),
                    "state": data.get("address", {}).get("state", ""),
                    "zipcode": data.get("address", {}).get("zip_code", ""),
                    "country": country,
                    "phone": data.get("phone_number", ""),
                    "email": data.get("email", ""),
                    "dob": data.get("date_of_birth", ""),
                    "gender": data.get("gender", "")
                }
                
                logger.info(f"Generated fallback identity from API: {identity['first_name']} {identity['last_name']}")
                return identity
                
        except Exception as e:
            logger.error(f"Error in fallback identity API: {str(e)}")
        
        # If both APIs fail, generate locally
        logger.info("Using local identity generation as final fallback")
        
        # Generate random first and last name
        first_names = ["James", "John", "Robert", "Michael", "William", "David", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Susan"]
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas"]
        
        states = {
            "US": ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"],
            "CA": ["AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"],
            "UK": ["England", "Scotland", "Wales", "Northern Ireland"]
        }
        
        cities = {
            "US": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"],
            "CA": ["Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton", "Ottawa", "Winnipeg", "Quebec City", "Hamilton", "Kitchener"],
            "UK": ["London", "Birmingham", "Manchester", "Glasgow", "Liverpool", "Bristol", "Edinburgh", "Sheffield", "Leeds", "Newcastle"]
        }
        
        # Generate identity with appropriate format for the country
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        # Use country-specific formats
        state = random.choice(states.get(country, states["US"]))
        city = random.choice(cities.get(country, cities["US"]))
        
        # Generate street address
        street_number = random.randint(100, 9999)
        street_names = ["Main", "Oak", "Maple", "Park", "Pine", "Cedar", "Elm", "Washington", "Lake", "Hill"]
        street_types = ["St", "Ave", "Blvd", "Dr", "Ln", "Rd", "Way", "Pl", "Ct"]
        street = f"{street_number} {random.choice(street_names)} {random.choice(street_types)}"
        
        # Generate postal code based on country
        if country == "US":
            zipcode = f"{random.randint(10000, 99999)}"
        elif country == "CA":
            zipcode = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(0, 9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')} {random.randint(0, 9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(0, 9)}"
        elif country == "UK":
            zipcode = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(0, 9)} {random.randint(0, 9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
        else:
            zipcode = f"{random.randint(10000, 99999)}"
        
        # Phone number format
        if country == "US":
            area_code = random.randint(200, 999)
            prefix = random.randint(200, 999)
            line_number = random.randint(1000, 9999)
            phone = f"{area_code}-{prefix}-{line_number}"
        elif country == "CA":
            area_code = random.choice(["204", "226", "236", "249", "250", "289", "306", "343", "365", "387", "403", "416", "418", "431", "437", "438", "450", "506", "514", "519", "548", "579", "581", "587", "604", "613", "639", "647", "705", "709", "778", "780", "782", "807", "819", "825", "867", "873", "902", "905"])
            prefix = random.randint(200, 999)
            line_number = random.randint(1000, 9999)
            phone = f"{area_code}-{prefix}-{line_number}"
        elif country == "UK":
            area_code = f"0{random.randint(1, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
            first_part = random.randint(100, 999)
            second_part = random.randint(1000, 9999)
            phone = f"{area_code} {first_part} {second_part}"
        else:
            phone = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            
        # Generate DOB (18-70 years old)
        current_year = datetime.now().year
        birth_year = random.randint(current_year - 70, current_year - 18)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # Simplify to avoid month-specific max days
        dob = f"{birth_month:02d}/{birth_day:02d}/{birth_year}"
            
        # Generate email based on name
        email_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "aol.com"]
        email_domain = random.choice(email_domains)
        username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}"
        email = f"{username}@{email_domain}"
        
        # Create the identity object
        identity = {
            "first_name": first_name,
            "last_name": last_name,
            "address": street,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "country": country,
            "phone": phone,
            "email": email,
            "dob": dob,
            "gender": random.choice(["Male", "Female", "Other"])
        }
        
        logger.info(f"Generated local fallback identity: {identity['first_name']} {identity['last_name']}")
        return identity
    
    def generate_virtual_number(self, country_code="US"):
        """Generate a virtual phone number for verification using Virtual Number API"""
        logger.info(f"Generating virtual phone number for country: {country_code}")
        
        try:
            # Primary API: Veriphone
            headers = self.get_headers("phone")
            url = "https://veriphone.p.rapidapi.com/verify"
            
            # Generate a random phone number format based on country
            phone = self._generate_fallback_phone(country_code)
            
            # Make request to verify the generated number
            response = requests.get(
                url, 
                headers=headers, 
                params={"phone": phone}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if phone is valid according to the API
                if data.get("phone_valid", False):
                    result = {
                        "phone": data.get("phone", phone),
                        "country_code": data.get("country_code", country_code),
                        "carrier": data.get("carrier", ""),
                        "phone_type": data.get("phone_type", "mobile"),
                        "valid": data.get("phone_valid", True)
                    }
                    
                    logger.info(f"Generated valid phone number: {result['phone']}")
                    return result
                else:
                    logger.warning(f"Generated phone number invalid according to API: {phone}")
                    # Try fallback API
                    return self._generate_fallback_phone(country_code, True)
            else:
                logger.warning(f"Primary phone API error: {response.status_code}")
                # Try fallback API
                return self._generate_fallback_phone(country_code, True)
                
        except Exception as e:
            logger.error(f"Error in phone number generation: {str(e)}")
            # Use fallback phone generation
            return self._generate_fallback_phone(country_code, True)
    
    def _generate_fallback_phone(self, country_code="US", use_fallback_api=False):
        """Generate a fallback phone number when API call fails"""
        if use_fallback_api:
            logger.info("Using fallback phone validation API")
            
            try:
                # Try alternative Phone Validator API
                headers = self.get_headers("phone_fallback")
                url = "https://phone-validator-and-verification.p.rapidapi.com/phonevalidator"
                
                # Generate a random phone based on country format
                if country_code == "US":
                    area_code = random.randint(200, 999)
                    prefix = random.randint(200, 999)
                    line_number = random.randint(1000, 9999)
                    phone = f"{area_code}{prefix}{line_number}"
                elif country_code == "CA":
                    area_code = random.choice(["204", "226", "236", "249", "250", "289", "306", "343", "365", "403", "416", "418", "431", "437", "438", "450", "506", "514", "519", "548", "579", "581", "587", "604", "613", "639", "647", "705", "709", "778", "780", "782", "807", "819", "825", "867", "873", "902", "905"])
                    prefix = random.randint(200, 999)
                    line_number = random.randint(1000, 9999)
                    phone = f"{area_code}{prefix}{line_number}"
                elif country_code == "UK":
                    area_code = f"0{random.randint(1, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
                    first_part = random.randint(100, 999)
                    second_part = random.randint(1000, 9999)
                    phone = f"{area_code}{first_part}{second_part}"
                else:
                    phone = f"{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
                
                # Make API request to validate
                response = requests.get(
                    url, 
                    headers=headers, 
                    params={"phoneNumber": phone, "country": country_code}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check if phone is valid according to the API
                    if data.get("isValid", False):
                        result = {
                            "phone": data.get("phoneNumber", phone),
                            "country_code": data.get("countryCode", country_code),
                            "carrier": data.get("carrier", ""),
                            "phone_type": data.get("lineType", "mobile"),
                            "valid": data.get("isValid", True)
                        }
                        
                        logger.info(f"Generated valid phone number from fallback API: {result['phone']}")
                        return result
                
                # If fallback API also fails, fall through to local generation
                logger.warning("Fallback phone API failed, using local generation")
            
            except Exception as e:
                logger.error(f"Error in fallback phone API: {str(e)}")
        
        # Local phone number generation
        logger.info("Using local phone number generation")
        
        # Generate phone based on country format
        if country_code == "US":
            area_code = random.randint(200, 999)
            prefix = random.randint(200, 999)
            line_number = random.randint(1000, 9999)
            phone = f"{area_code}-{prefix}-{line_number}"
            formatted_phone = f"+1{area_code}{prefix}{line_number}"
        elif country_code == "CA":
            area_code = random.choice(["204", "226", "236", "249", "250", "289", "306", "343", "365", "403", "416", "418", "431", "437", "438", "450", "506", "514", "519", "548", "579", "581", "587", "604", "613", "639", "647", "705", "709", "778", "780", "782", "807", "819", "825", "867", "873", "902", "905"])
            prefix = random.randint(200, 999)
            line_number = random.randint(1000, 9999)
            phone = f"{area_code}-{prefix}-{line_number}"
            formatted_phone = f"+1{area_code}{prefix}{line_number}"
        elif country_code == "UK":
            area_code = f"0{random.randint(1, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
            first_part = random.randint(100, 999)
            second_part = random.randint(1000, 9999)
            phone = f"{area_code} {first_part} {second_part}"
            formatted_phone = f"+44{area_code[1:]}{first_part}{second_part}"
        else:
            phone = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            formatted_phone = f"+1{phone.replace('-', '')}"
        
        # Create result object
        result = {
            "phone": phone,
            "formatted_phone": formatted_phone,
            "country_code": country_code,
            "carrier": "Local Carrier",
            "phone_type": "mobile",
            "valid": True
        }
        
        if not use_fallback_api:
            # If this is the initial call, just return the phone string
            return phone
        
        logger.info(f"Generated local fallback phone: {result['phone']}")
        return result
    
    def generate_card(self, card_type="visa"):
        """Generate a valid credit card for verification"""
        logger.info(f"Generating credit card of type: {card_type}")
        
        try:
            # Primary API: Fake Valid CC Generator
            headers = self.get_headers("card")
            url = "https://fake-valid-cc-data-generator.p.rapidapi.com/v1/card/generate"
            
            # Map our card types to the API's format
            card_type_map = {
                "visa": "visa",
                "mastercard": "mastercard",
                "amex": "amex",
                "discover": "discover",
                "diners": "diners",
                "jcb": "jcb"
            }
            
            api_card_type = card_type_map.get(card_type.lower(), "visa")
            
            # Make request
            params = {"brand": api_card_type, "format": "json"}
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Map response to our standard format
                result = {
                    "card_type": card_type,
                    "card_number": data.get("card_number", "").replace(" ", ""),
                    "expiry": data.get("expiration_date", ""),
                    "cvv": data.get("cvv", ""),
                    "cardholder_name": data.get("cardholder_name", "")
                }
                
                logger.info(f"Generated card: {card_type} ending in {result['card_number'][-4:]}")
                return result
            else:
                logger.warning(f"Primary card API error: {response.status_code}")
                # Try fallback API
                return self._generate_fallback_card(card_type)
                
        except Exception as e:
            logger.error(f"Error in card generation: {str(e)}")
            # Use fallback card generation
            return self._generate_fallback_card(card_type)
    
    def _generate_fallback_card(self, card_type="visa"):
        """Generate a fallback credit card when API call fails"""
        logger.info(f"Using fallback card generation for: {card_type}")
        
        try:
            # Try alternative Credit Card Validator Generator API
            headers = self.get_headers("card_fallback")
            url = "https://credit-card-validator-generator.p.rapidapi.com/credit-card-validator"
            
            # Map our card types to the API's format
            card_type_map = {
                "visa": "visa",
                "mastercard": "mastercard",
                "amex": "amex",
                "discover": "discover",
                "diners": "diners_club",
                "jcb": "jcb"
            }
            
            api_card_type = card_type_map.get(card_type.lower(), "visa")
            
            # Make request
            response = requests.get(
                url, 
                headers=headers, 
                params={"brand": api_card_type}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Get current date for expiry calculation
                now = datetime.now()
                exp_month = random.randint(1, 12)
                exp_year = random.randint(now.year + 1, now.year + 5)
                expiry = f"{exp_month:02d}/{str(exp_year)[2:]}"
                
                # Map response to our standard format
                result = {
                    "card_type": card_type,
                    "card_number": data.get("credit_card_number", ""),
                    "expiry": expiry,
                    "cvv": self._generate_cvv(card_type),
                    "cardholder_name": self._generate_cardholder_name()
                }
                
                logger.info(f"Generated card from fallback API: {card_type} ending in {result['card_number'][-4:]}")
                return result
            
            # If fallback API also fails, fall through to local generation
            logger.warning("Fallback card API failed, using local generation")
            
        except Exception as e:
            logger.error(f"Error in fallback card API: {str(e)}")
        
        # Local card generation using Luhn algorithm
        logger.info("Using local card generation with Luhn algorithm")
        
        # Generate a card number that passes Luhn check
        card_number = self._generate_card_number_with_luhn(card_type)
        
        # Get current date for expiry calculation
        now = datetime.now()
        exp_month = random.randint(1, 12)
        exp_year = random.randint(now.year + 1, now.year + 5)
        expiry = f"{exp_month:02d}/{str(exp_year)[2:]}"
        
        # Generate CVV
        cvv = self._generate_cvv(card_type)
        
        # Generate cardholder name
        cardholder_name = self._generate_cardholder_name()
        
        # Create result object
        result = {
            "card_type": card_type,
            "card_number": card_number,
            "expiry": expiry,
            "cvv": cvv,
            "cardholder_name": cardholder_name
        }
        
        logger.info(f"Generated local fallback card: {card_type} ending in {result['card_number'][-4:]}")
        return result
    
    def _generate_card_number_with_luhn(self, card_type="visa"):
        """Generate a valid card number that passes the Luhn check"""
        # Card number prefixes and lengths
        card_prefixes = {
            "visa": ["4"],
            "mastercard": ["51", "52", "53", "54", "55"],
            "amex": ["34", "37"],
            "discover": ["6011", "644", "645", "646", "647", "648", "649", "65"],
            "diners": ["300", "301", "302", "303", "304", "305", "36", "38"],
            "jcb": ["3528", "3529", "353", "354", "355", "356", "357", "358"]
        }
        
        card_lengths = {
            "visa": 16,
            "mastercard": 16,
            "amex": 15,
            "discover": 16,
            "diners": 14,
            "jcb": 16
        }
        
        # Get prefix and length for the card type
        prefixes = card_prefixes.get(card_type.lower(), ["4"])
        length = card_lengths.get(card_type.lower(), 16)
        
        # Choose a random prefix
        prefix = random.choice(prefixes)
        
        # Generate the rest of the card number
        number = prefix
        while len(number) < length - 1:
            number += str(random.randint(0, 9))
        
        # Calculate the check digit using Luhn algorithm
        digits = [int(d) for d in number]
        for i in range(len(digits) - 1, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        
        check_sum = sum(digits)
        check_digit = (10 - (check_sum % 10)) % 10
        
        # Add the check digit to complete the card number
        number += str(check_digit)
        
        return number
    
    def _generate_cvv(self, card_type="visa"):
        """Generate a CVV code appropriate for the card type"""
        if card_type.lower() == "amex":
            return ''.join(random.choice(string.digits) for _ in range(4))
        else:
            return ''.join(random.choice(string.digits) for _ in range(3))
    
    def _generate_cardholder_name(self):
        """Generate a random cardholder name"""
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Mary", "James", "Elizabeth", "Robert", "Linda"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson"]
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        return f"{first_name} {last_name}"
    
    def generate_virtual_card(self, amount=0.00, currency="USD"):
        """Generate a virtual card for free trial using Virtual Card Issuing API"""
        logger.info(f"Generating virtual card with amount: {amount} {currency}")
        
        try:
            # Virtual Card Issuing API
            headers = self.get_headers("virtual_card")
            url = "https://virtual-cards-issuance.p.rapidapi.com/v1/generate"
            
            # Make request
            payload = {
                "amount": amount,
                "currency": currency,
                "card_type": "visa"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Map response to our standard format
                result = {
                    "card_type": data.get("card_type", "visa"),
                    "card_number": data.get("card_number", ""),
                    "expiry": data.get("expiry", ""),
                    "cvv": data.get("cvv", ""),
                    "balance": data.get("balance", amount),
                    "currency": data.get("currency", currency),
                    "virtual": True
                }
                
                logger.info(f"Generated virtual card with balance: {result['balance']} {result['currency']}")
                return result
            else:
                logger.warning(f"Virtual card API error: {response.status_code}")
                # Fall back to regular card generation
                card = self.generate_card("visa")
                card["balance"] = amount
                card["currency"] = currency
                card["virtual"] = False
                return card
                
        except Exception as e:
            logger.error(f"Error in virtual card generation: {str(e)}")
            # Fall back to regular card generation
            card = self.generate_card("visa")
            card["balance"] = amount
            card["currency"] = currency
            card["virtual"] = False
            return card
    
    def validate_email(self, email):
        """
        Validate an email address using the Advanced Email Validator API
        
        Args:
            email (str): The email address to validate
            
        Returns:
            dict: Validation results including deliverability, quality score, etc.
        """
        logger.info(f"Validating email: {email}")
        
        try:
            # Primary API: Validect Email Verification
            headers = self.get_headers("email")
            url = "https://validect-email-verification-v1.p.rapidapi.com/validate"
            
            # Make request
            response = requests.get(
                url, 
                headers=headers, 
                params={"email": email}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Map the response to our standard format
                result = {
                    "email": email,
                    "is_valid": data.get("is_valid", False),
                    "is_deliverable": data.get("is_deliverable", False),
                    "is_disposable": data.get("is_disposable", True),
                    "score": data.get("quality_score", 0),
                    "message": data.get("message", "")
                }
                
                logger.info(f"Email validation result for {email}: Valid={result['is_valid']}, Deliverable={result['is_deliverable']}")
                return result
            else:
                logger.warning(f"Primary email validation API error: {response.status_code}")
                # Try fallback API
                return self._validate_email_fallback(email)
                
        except Exception as e:
            logger.error(f"Error in email validation: {str(e)}")
            # Use fallback email validation
            return self._validate_email_fallback(email)
    
    def _validate_email_fallback(self, email):
        """Fallback email validation when API call fails"""
        logger.info(f"Using fallback email validation for: {email}")
        
        try:
            # Try alternative Email Validator API
            headers = self.get_headers("email_fallback")
            url = "https://email-validator-and-verifier.p.rapidapi.com/v1/verify"
            
            # Make request
            response = requests.get(
                url, 
                headers=headers, 
                params={"email": email}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Map response to our standard format
                result = {
                    "email": email,
                    "is_valid": data.get("valid", False),
                    "is_deliverable": data.get("deliverable", False),
                    "is_disposable": data.get("disposable", True),
                    "score": 0.5,  # This API doesn't provide a score
                    "message": data.get("message", "")
                }
                
                logger.info(f"Fallback email validation result for {email}: Valid={result['is_valid']}, Deliverable={result['is_deliverable']}")
                return result
            
            # If fallback API also fails, fall through to local validation
            logger.warning("Fallback email validation API failed, using local validation")
            
        except Exception as e:
            logger.error(f"Error in fallback email validation API: {str(e)}")
        
        # Local email validation using regex
        logger.info("Using local email validation")
        
        # Simple email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Known disposable email domains
        disposable_domains = [
            "mailinator.com", "temp-mail.org", "fakeinbox.com", "tempmail.com", 
            "yopmail.com", "guerrillamail.com", "sharklasers.com", "trashmail.com",
            "mailnesia.com", "tempail.com", "10minutemail.com", "mailboxy.com"
        ]
        
        # Check if the email is valid using regex
        is_valid = bool(re.match(email_pattern, email))
        
        # Check if the email domain is disposable
        domain = email.split('@')[-1] if '@' in email else ''
        is_disposable = domain in disposable_domains
        
        # Create result object
        result = {
            "email": email,
            "is_valid": is_valid,
            "is_deliverable": is_valid,  # Assume deliverable if valid
            "is_disposable": is_disposable,
            "score": 0.8 if is_valid else 0.0,
            "message": "Local validation" if is_valid else "Invalid email format"
        }
        
        logger.info(f"Local email validation result for {email}: Valid={result['is_valid']}, Disposable={result['is_disposable']}")
        return result
    
    def generate_email(self):
        """Generate a disposable email using TempMail API from RapidAPI"""
        logger.info("Generating disposable email")
        
        # Random username
        username = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        domains = ["mailcatch.com", "mailbox.com", "disposable.com", "tempmail.net", "spamguy.com"]
        domain = random.choice(domains)
        
        email = f"{username}@{domain}"
        
        # Validate the email to check disposability
        validation = self.validate_email(email)
        
        if validation.get("is_valid", False):
            logger.info(f"Generated disposable email: {email}")
            return {
                "email": email,
                "password": self._generate_secure_password(),
                "is_disposable": validation.get("is_disposable", True),
                "is_valid": validation.get("is_valid", True)
            }
        else:
            # Fallback to a simple generation
            return self._generate_fallback_email()
    
    def _generate_secure_password(self, length=12):
        """Generate a secure password with mixed characters"""
        # Ensure at least one of each character type
        lowercase = random.choice(string.ascii_lowercase)
        uppercase = random.choice(string.ascii_uppercase)
        digit = random.choice(string.digits)
        special = random.choice("!@#$%^&*()-_=+[]{}|;:,.<>?")
        
        # Fill the rest randomly
        remaining = ''.join(random.choice(string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?") 
                           for _ in range(length - 4))
        
        # Combine and shuffle
        password_chars = list(lowercase + uppercase + digit + special + remaining)
        random.shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def _generate_fallback_email(self):
        """Generate a fallback email when API calls fail"""
        logger.info("Using fallback email generation")
        
        # Generate random username
        usernames = [
            ''.join(random.choice(string.ascii_lowercase) for _ in range(8)),
            f"user{random.randint(1000, 9999)}",
            f"temp{random.randint(100, 999)}user",
            f"trial{random.randint(10, 99)}account"
        ]
        
        username = random.choice(usernames)
        
        # Disposable email domains
        domains = ["mailinator.com", "temp-mail.org", "fakeinbox.com", "guerrillamail.com", "yopmail.com"]
        domain = random.choice(domains)
        
        email = f"{username}@{domain}"
        
        result = {
            "email": email,
            "password": self._generate_secure_password(),
            "is_disposable": True,
            "is_valid": True
        }
        
        logger.info(f"Generated fallback email: {email}")
        return result
    
    def generate_complete_trial_data(self, service=None):
        """Generate a complete set of trial data with all required information"""
        logger.info(f"Generating complete trial data for service: {service}")
        
        try:
            # Generate identity
            identity = self.generate_identity()
            
            # Generate email
            email_data = self.generate_email()
            
            # Generate card
            card = self.generate_card()
            
            # Generate phone number
            phone = self.generate_virtual_number()
            
            # Set trial end date based on service
            today = datetime.now()
            
            if service == "hulu":
                trial_days = 30
            elif service == "disney":
                trial_days = 7
            elif service == "netflix":
                trial_days = 30
            elif service == "spotify":
                trial_days = 30
            else:
                trial_days = 14  # Default
            
            trial_end = today + timedelta(days=trial_days)
            
            # Assemble all data
            trial_data = {
                "service": service or "generic",
                "email": email_data["email"],
                "password": email_data["password"],
                "identity": {
                    "first_name": identity["first_name"],
                    "last_name": identity["last_name"],
                    "address": identity["address"],
                    "city": identity["city"],
                    "state": identity["state"],
                    "zipcode": identity["zipcode"],
                    "country": identity["country"],
                    "phone": phone["phone"] if isinstance(phone, dict) else phone,
                    "dob": identity["dob"]
                },
                "payment": {
                    "card_type": card["card_type"],
                    "card_number": card["card_number"],
                    "expiry": card["expiry"],
                    "cvv": card["cvv"],
                    "cardholder_name": card.get("cardholder_name", f"{identity['first_name']} {identity['last_name']}")
                },
                "start_date": today.strftime("%Y-%m-%d"),
                "end_date": trial_end.strftime("%Y-%m-%d"),
                "trial_days": trial_days
            }
            
            logger.info(f"Generated complete trial data for {service or 'generic'}")
            return trial_data
            
        except Exception as e:
            logger.error(f"Error generating complete trial data: {str(e)}")
            return None
    
    def web_scrape(self, url, use_proxy=False, custom_headers=None, cookies=None, timeout=30, render_js=False):
        """
        Scrape a website using Website Scraper API with fallback to direct requests
        
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
        logger.info(f"Scraping URL: {url}")
        
        try:
            # Primary API: Website Scraper API
            headers = self.get_headers("scraper")
            api_url = "https://website-scraper-api.p.rapidapi.com/scrape"
            
            # Set up params
            params = {
                "url": url,
                "javascript": str(render_js).lower()
            }
            
            if use_proxy:
                params["proxy"] = "true"
            
            if custom_headers:
                params["headers"] = json.dumps(custom_headers)
            
            if cookies:
                params["cookies"] = json.dumps(cookies)
            
            # Make request
            response = requests.get(api_url, headers=headers, params=params, timeout=timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                result = {
                    "url": url,
                    "status": response.status_code,
                    "content": data.get("content", ""),
                    "html": data.get("html", ""),
                    "title": data.get("title", ""),
                    "metadata": data.get("metadata", {}),
                    "links": data.get("links", []),
                    "images": data.get("images", []),
                    "timestamp": datetime.now().isoformat()
                }
                
                logger.info(f"Successfully scraped URL: {url}")
                return result
            else:
                logger.warning(f"Primary scraper API error: {response.status_code}")
                # Try fallback API
                return self._web_scrape_fallback(url, use_proxy, custom_headers, cookies, timeout, render_js)
                
        except Exception as e:
            logger.error(f"Error in web scraping: {str(e)}")
            # Use fallback scraping
            return self._web_scrape_fallback(url, use_proxy, custom_headers, cookies, timeout, render_js)
    
    def _web_scrape_fallback(self, url, use_proxy=False, custom_headers=None, cookies=None, timeout=30, render_js=False):
        """Fallback web scraping when API call fails"""
        logger.info(f"Using fallback web scraping for URL: {url}")
        
        try:
            # Try alternative Scraping Ant API
            headers = self.get_headers("scraper_fallback")
            api_url = "https://scrapingant.p.rapidapi.com/get"
            
            # Set up params
            params = {
                "url": url,
                "return_text": "true"
            }
            
            if render_js:
                params["browser"] = "true"
            
            if use_proxy:
                params["proxy_country"] = "US"
            
            # Make request
            response = requests.get(api_url, headers=headers, params=params, timeout=timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                result = {
                    "url": url,
                    "status": response.status_code,
                    "content": data.get("text", ""),
                    "html": data.get("html", ""),
                    "timestamp": datetime.now().isoformat()
                }
                
                logger.info(f"Successfully scraped URL with fallback API: {url}")
                return result
            
            # If fallback API also fails, fall through to direct requests
            logger.warning("Fallback scraper API failed, using direct requests")
            
        except Exception as e:
            logger.error(f"Error in fallback scraper API: {str(e)}")
        
        # Direct request as final fallback
        logger.info("Using direct request as final fallback")
        
        try:
            # Set up headers
            request_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            if custom_headers:
                request_headers.update(custom_headers)
            
            # Make request
            response = requests.get(url, headers=request_headers, cookies=cookies, timeout=timeout)
            
            result = {
                "url": url,
                "status": response.status_code,
                "content": response.text,
                "html": response.text,
                "title": "",  # Can't easily extract without parsing
                "timestamp": datetime.now().isoformat()
            }
            
            # Try to extract title
            title_match = re.search(r"<title>(.*?)</title>", response.text, re.IGNORECASE | re.DOTALL)
            if title_match:
                result["title"] = title_match.group(1).strip()
            
            logger.info(f"Successfully scraped URL with direct request: {url}")
            return result
        
        except Exception as e:
            logger.error(f"Error in direct request scraping: {str(e)}")
            
            # Return error result
            return {
                "url": url,
                "status": 500,
                "content": "",
                "html": "",
                "title": "",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Testing
if __name__ == "__main__":
    print("Testing API Integrations")
    
    api = UpdatedAPIIntegrations()
    
    print("\nGenerating identity:")
    identity = api.generate_identity()
    print(f"Name: {identity['first_name']} {identity['last_name']}")
    print(f"Address: {identity['address']}, {identity['city']}, {identity['state']} {identity['zipcode']}")
    print(f"Phone: {identity['phone']}")
    print(f"Email: {identity['email']}")
    
    print("\nGenerating card:")
    card = api.generate_card()
    print(f"Card type: {card['card_type']}")
    print(f"Card number: {card['card_number']}")
    print(f"Expiry: {card['expiry']}")
    print(f"CVV: {card['cvv']}")
    
    print("\nGenerating email:")
    email = api.generate_email()
    print(f"Email: {email['email']}")
    print(f"Password: {email['password']}")
    
    print("\nGenerating phone:")
    phone = api.generate_virtual_number()
    if isinstance(phone, dict):
        print(f"Phone: {phone['phone']}")
        print(f"Valid: {phone.get('valid', False)}")
    else:
        print(f"Phone: {phone}")
    
    print("\nComplete trial data:")
    trial = api.generate_complete_trial_data("hulu")
    if trial:
        print(f"Service: {trial['service']}")
        print(f"Email: {trial['email']}")
        print(f"Password: {trial['password']}")
        print(f"Name: {trial['identity']['first_name']} {trial['identity']['last_name']}")
        print(f"Card: {trial['payment']['card_type']} **** **** **** {trial['payment']['card_number'][-4:]}")
        print(f"Trial period: {trial['start_date']} to {trial['end_date']} ({trial['trial_days']} days)")