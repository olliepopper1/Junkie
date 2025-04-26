"""
Card Agent (Meth Mandy)
Generates random credit card information
"""
import logging
import aiohttp
import random
import string
from datetime import datetime, timedelta
from config import ENDPOINTS, API_HOSTS, DEFAULT_HEADERS
from agents.proxy import get_proxy

logger = logging.getLogger(__name__)

class CardAgent:
    """Agent for generating credit card information"""
    
    def __init__(self, db):
        """Initialize the card agent"""
        self.db = db
        self.name = "Meth Mandy"
        logger.info(f"{self.name} initialized")
    
    async def generate_card(self):
        """Generate random credit card information"""
        logger.info(f"{self.name} generating card")
        
        url = ENDPOINTS["fake_card"]
        headers = DEFAULT_HEADERS.copy()
        
        try:
            # Get proxy if enabled
            proxy = get_proxy()
            
            async with aiohttp.ClientSession() as session:
                # Use proxy if available
                if proxy:
                    conn = aiohttp.TCPConnector(ssl=False)
                    session._connector = conn
                    async with session.get(url, headers=headers, proxy=proxy) as response:
                        data = await response.json()
                else:
                    async with session.get(url, headers=headers) as response:
                        data = await response.json()
                
                # Parse the randomuser.me data to create a credit card
                if "results" in data and len(data["results"]) > 0:
                    user_data = data["results"][0]
                    name = f"{user_data.get('name', {}).get('first', 'John')} {user_data.get('name', {}).get('last', 'Doe')}"
                    
                    # Generate card details based on the user identity
                    card_type = self._generate_card_type()
                    number = self._generate_card_number(card_type)
                    expiry = self._generate_expiry()
                    cvv = self._generate_cvv(card_type)
                    
                    card = {
                        "number": number,
                        "expiry": expiry,
                        "cvv": cvv,
                        "type": card_type,
                        "name": name.upper()
                    }
                    
                    logger.info(f"{self.name} generated card: {card_type} ending in {number[-4:]}")
                    return card
                else:
                    # Fallback if randomuser.me API doesn't provide expected data structure
                    logger.warning("API response not in expected format, using fallback")
                    return self._generate_fallback_card()
                
        except Exception as e:
            logger.error(f"Error generating card: {str(e)}")
            # Fallback to fake card generation if API fails
            return self._generate_fallback_card()
            
    def _generate_card_type(self):
        """Generate a random card type"""
        card_types = ["Visa", "Mastercard", "Amex", "Discover"]
        return random.choice(card_types)
        
    def _generate_card_number(self, card_type):
        """Generate a valid card number based on type"""
        # Credit card type prefixes
        prefixes = {
            "Visa": ["4"],
            "Mastercard": ["51", "52", "53", "54", "55"],
            "Amex": ["34", "37"],
            "Discover": ["6011"]
        }
        
        # Choose a prefix for the card type
        prefix = random.choice(prefixes[card_type])
        
        # Generate the appropriate length
        length = 15 if card_type == "Amex" else 16
        
        # Generate digits
        remaining_digits = length - len(prefix)
        number = prefix + ''.join([str(random.randint(0, 9)) for _ in range(remaining_digits - 1)])
        
        # Apply Luhn algorithm to calculate the check digit
        sum_digits = 0
        # Double every second digit, starting from the right
        for i, digit in enumerate(reversed(number)):
            digit_value = int(digit)
            if i % 2 == 1:  # Odd positioned digits (0-indexed from right)
                digit_value *= 2
                if digit_value > 9:
                    digit_value -= 9
            sum_digits += digit_value
            
        # Calculate the check digit to make the sum divisible by 10
        check_digit = (10 - (sum_digits % 10)) % 10
        
        # Add the check digit to complete the card number
        full_number = number + str(check_digit)
        
        return full_number
    
    def _generate_expiry(self):
        """Generate a future expiry date for a credit card"""
        now = datetime.now()
        future = now + timedelta(days=random.randint(365, 1460))  # 1-4 years in the future
        return future.strftime("%m/%y")
        
    def _generate_cvv(self, card_type):
        """Generate a CVV based on card type"""
        if card_type == "Amex":
            return ''.join([str(random.randint(0, 9)) for _ in range(4)])
        else:
            return ''.join([str(random.randint(0, 9)) for _ in range(3)])
    
    def _generate_fallback_card(self):
        """Generate a fallback credit card if the API fails"""
        # Generate a future expiry date
        now = datetime.now()
        future = now + timedelta(days=random.randint(365, 1460))  # 1-4 years in the future
        expiry = future.strftime("%m/%y")
        
        # Generate a random CVV
        cvv = str(random.randint(100, 999))
        
        # Use a known test card number for different card types
        card_types = [
            {"type": "Visa", "number": "4111111111111111"},
            {"type": "Mastercard", "number": "5555555555554444"},
            {"type": "Amex", "number": "378282246310005"},
            {"type": "Discover", "number": "6011111111111117"}
        ]
        
        card_data = random.choice(card_types)
        
        return {
            "number": card_data["number"],
            "expiry": expiry,
            "cvv": cvv,
            "type": card_data["type"],
            "name": "CARD HOLDER"
        }
