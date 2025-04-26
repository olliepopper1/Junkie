"""
Card Agent (Meth Mandy)
Generates random credit card information
"""
import logging
import aiohttp
import random
from datetime import datetime, timedelta
from config import ENDPOINTS, RAPIDAPI_HOSTS, DEFAULT_HEADERS
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
        headers["X-RapidAPI-Host"] = RAPIDAPI_HOSTS["fake_card"]
        
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
                
                card = {
                    "number": data.get("card_number", "4111111111111111"),
                    "expiry": data.get("expiration_date", "12/26"),
                    "cvv": data.get("cvv", "123"),
                    "type": data.get("card_type", "Visa"),
                    "name": data.get("name", "CARD HOLDER")
                }
                
                logger.info(f"Generated card: {card['type']} ending in {card['number'][-4:]}")
                return card
                
        except Exception as e:
            logger.error(f"Error generating card: {str(e)}")
            # Fallback to fake card generation if API fails
            return self._generate_fallback_card()
    
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
