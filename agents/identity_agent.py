"""
Identity Agent (Heroin Harry)
Generates random identity information
"""
import logging
import aiohttp
from config import ENDPOINTS, RAPIDAPI_HOSTS, DEFAULT_HEADERS
from agents.proxy import get_proxy

logger = logging.getLogger(__name__)

class IdentityAgent:
    """Agent for generating identity information"""
    
    def __init__(self, db):
        """Initialize the identity agent"""
        self.db = db
        self.name = "Heroin Harry"
        logger.info(f"{self.name} initialized")
    
    async def generate_identity(self):
        """Generate random identity information"""
        logger.info(f"{self.name} generating identity")
        
        url = ENDPOINTS["random_user"]
        headers = DEFAULT_HEADERS.copy()
        headers["X-RapidAPI-Host"] = RAPIDAPI_HOSTS["random_user"]
        
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
                
                if not data or "results" not in data or not data["results"]:
                    raise ValueError("Invalid response from identity API")
                
                user = data["results"][0]
                
                identity = {
                    "name": f"{user['name']['first']} {user['name']['last']}",
                    "age": user["dob"]["age"],
                    "gender": user["gender"],
                    "location": f"{user['location']['city']}, {user['location']['state']}, {user['location']['country']}",
                    "dob": user["dob"]["date"],
                    "nationality": user["nat"],
                    "address": f"{user['location']['street']['number']} {user['location']['street']['name']}",
                    "postcode": user["location"]["postcode"],
                    "username": user["login"]["username"]
                }
                
                logger.info(f"Generated identity: {identity['name']}")
                return identity
                
        except Exception as e:
            logger.error(f"Error generating identity: {str(e)}")
            # Fallback to basic identity if API fails
            return {
                "name": "John Smith",
                "age": 30,
                "gender": "male",
                "location": "New York, NY, USA",
                "dob": "1993-07-22T00:00:00.000Z",
                "nationality": "US",
                "address": "123 Main Street",
                "postcode": "10001",
                "username": "jsmith93"
            }
