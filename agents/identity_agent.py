"""
Identity Agent (Heroin Harry)
Generates random identity information
"""
import logging
import aiohttp
import random
import json
from datetime import datetime, timedelta
from config import ENDPOINTS, RAPIDAPI_HOSTS, DEFAULT_HEADERS
from agents.proxy import get_proxy

logger = logging.getLogger(__name__)

class IdentityAgent:
    """Agent for generating identity information"""
    
    def __init__(self, db):
        """Initialize the identity agent"""
        self.db = db
        self.name = "Heroin Harry"
        
        # Nationalities supported by randomuser.me API
        self.nationalities = [
            "US", "GB", "FR", "DE", "CA", "AU", "NZ", 
            "IE", "BR", "MX", "ES", "NL", "DK", "NO", 
            "FI", "TR", "IR"
        ]
        
        logger.info(f"{self.name} initialized")
    
    async def generate_identity(self, nationality=None, gender=None):
        """
        Generate random identity information
        
        Args:
            nationality (str, optional): Two-letter country code (e.g., 'US', 'GB') 
            gender (str, optional): 'male' or 'female'
        """
        logger.info(f"{self.name} generating identity. Nationality: {nationality}, Gender: {gender}")
        
        url = ENDPOINTS["random_user"]
        headers = DEFAULT_HEADERS.copy()
        headers["X-RapidAPI-Host"] = RAPIDAPI_HOSTS["random_user"]
        
        # Add query parameters if provided
        params = {}
        if nationality and nationality.upper() in self.nationalities:
            params["nat"] = nationality.upper()
        if gender and gender.lower() in ["male", "female"]:
            params["gender"] = gender.lower()
        
        try:
            # Get proxy if enabled
            proxy = get_proxy()
            
            async with aiohttp.ClientSession() as session:
                # Use proxy if available
                if proxy:
                    conn = aiohttp.TCPConnector(ssl=False)
                    session._connector = conn
                    async with session.get(url, headers=headers, params=params, proxy=proxy) as response:
                        if response.status != 200:
                            logger.error(f"API error: {response.status} - {await response.text()}")
                            raise ValueError(f"API returned status code {response.status}")
                            
                        data = await response.json()
                else:
                    async with session.get(url, headers=headers, params=params) as response:
                        if response.status != 200:
                            logger.error(f"API error: {response.status} - {await response.text()}")
                            raise ValueError(f"API returned status code {response.status}")
                            
                        data = await response.json()
                
                if not data or "results" not in data or not data["results"]:
                    raise ValueError("Invalid response from identity API")
                
                user = data["results"][0]
                
                # Create enhanced identity information
                identity = {
                    "name": f"{user['name']['first']} {user['name']['last']}",
                    "first_name": user['name']['first'],
                    "last_name": user['name']['last'],
                    "age": user["dob"]["age"],
                    "gender": user["gender"],
                    "location": f"{user['location']['city']}, {user['location']['state']}, {user['location']['country']}",
                    "dob": user["dob"]["date"],
                    "nationality": user["nat"],
                    "address": f"{user['location']['street']['number']} {user['location']['street']['name']}",
                    "city": user['location']['city'],
                    "state": user['location']['state'],
                    "country": user['location']['country'],
                    "postcode": user["location"]["postcode"],
                    "email": user["email"],
                    "username": user["login"]["username"],
                    "password": user["login"]["password"],
                    "phone": user["phone"],
                    "cell": user["cell"],
                    "picture": user["picture"]["large"]
                }
                
                # Store a screenshot of generated data for debugging
                logger.info(f"Generated identity: {identity['name']} ({identity['age']}, {identity['gender']}) from {identity['nationality']}")
                return identity
                
        except Exception as e:
            logger.error(f"Error generating identity with RapidAPI: {str(e)}")
            logger.warning("Using alternative random user generation API...")
            
            # Try alternative API if primary one fails
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://randomuser.me/api/") as response:
                        if response.status == 200:
                            data = await response.json()
                            if "results" in data and data["results"]:
                                user = data["results"][0]
                                
                                identity = {
                                    "name": f"{user['name']['first']} {user['name']['last']}",
                                    "first_name": user['name']['first'],
                                    "last_name": user['name']['last'],
                                    "age": user["dob"]["age"],
                                    "gender": user["gender"],
                                    "location": f"{user['location']['city']}, {user['location']['state']}, {user['location']['country']}",
                                    "dob": user["dob"]["date"],
                                    "nationality": user["nat"],
                                    "address": f"{user['location']['street']['number']} {user['location']['street']['name']}",
                                    "city": user['location']['city'],
                                    "state": user['location']['state'],
                                    "country": user['location']['country'],
                                    "postcode": user["location"]["postcode"],
                                    "email": user["email"],
                                    "username": user["login"]["username"],
                                    "password": user["login"]["password"],
                                    "phone": user["phone"],
                                    "cell": user["cell"],
                                    "picture": user["picture"]["large"]
                                }
                                
                                logger.info(f"Generated fallback identity: {identity['name']} (Using randomuser.me directly)")
                                return identity
            
            except Exception as fallback_error:
                logger.error(f"Error with fallback identity generation: {str(fallback_error)}")
            
            # Last resort fallback with static data
            logger.error("All identity generation methods failed. Using last resort fallback.")
            
            # Report error to database for tracking
            if hasattr(self.db, 'log_error'):
                self.db.log_error("identity_generation", str(e))
            
            return {
                "name": "John Smith",
                "first_name": "John",
                "last_name": "Smith",
                "age": 30,
                "gender": "male",
                "location": "New York, NY, USA",
                "city": "New York",
                "state": "NY",
                "country": "USA",
                "dob": "1993-07-22T00:00:00.000Z",
                "nationality": "US",
                "address": "123 Main Street",
                "postcode": "10001",
                "username": "jsmith93",
                "password": "password123",
                "phone": "+1 555-123-4567",
                "cell": "+1 555-987-6543",
                "picture": "https://randomuser.me/api/portraits/men/1.jpg"
            }
    
    async def generate_multiple_identities(self, count=5, nationality=None, gender=None):
        """Generate multiple identities with the same parameters"""
        logger.info(f"{self.name} generating {count} identities")
        
        identities = []
        for _ in range(count):
            identity = await self.generate_identity(nationality, gender)
            identities.append(identity)
            
        return identities
