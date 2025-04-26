"""
Phone Agent (Cokehead Carl)
Generates random phone numbers
"""
import logging
import aiohttp
import random
from config import ENDPOINTS, RAPIDAPI_HOSTS, DEFAULT_HEADERS
from agents.proxy import get_proxy

logger = logging.getLogger(__name__)

class PhoneAgent:
    """Agent for generating phone numbers"""
    
    def __init__(self, db):
        """Initialize the phone agent"""
        self.db = db
        self.name = "Cokehead Carl"
        logger.info(f"{self.name} initialized")
    
    async def generate_phone(self, country_code="US"):
        """Generate a random phone number"""
        logger.info(f"{self.name} generating phone number for {country_code}")
        
        url = ENDPOINTS["random_phone"]
        headers = DEFAULT_HEADERS.copy()
        headers["X-RapidAPI-Host"] = RAPIDAPI_HOSTS["random_phone"]
        
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
                
                phone = data.get("phone", "")
                
                if not phone or len(phone) < 10:
                    # Fallback if API doesn't return a valid phone
                    phone = self._generate_fallback_phone(country_code)
                
                logger.info(f"Generated phone: {phone}")
                return phone
                
        except Exception as e:
            logger.error(f"Error generating phone: {str(e)}")
            # Fallback to fake phone generation if API fails
            return self._generate_fallback_phone(country_code)
    
    def _generate_fallback_phone(self, country_code="US"):
        """Generate a fallback phone number if the API fails"""
        if country_code == "US":
            # US phone format: +1AAABBBCCCC
            area_code = random.randint(200, 999)
            prefix = random.randint(200, 999)
            line = random.randint(1000, 9999)
            return f"+1{area_code}{prefix}{line}"
        elif country_code == "UK":
            # UK phone format: +44AAABBBBCCC
            area_code = random.randint(20, 99)
            prefix = random.randint(1000, 9999)
            line = random.randint(100, 999)
            return f"+44{area_code}{prefix}{line}"
        else:
            # Generic international format
            country_codes = {
                "CA": "1",
                "AU": "61",
                "DE": "49",
                "FR": "33",
                "ES": "34",
                "IT": "39",
                "JP": "81",
                "BR": "55",
                "IN": "91"
            }
            
            cc = country_codes.get(country_code, "1")
            number = ''.join(random.choice("0123456789") for _ in range(10))
            return f"+{cc}{number}"
