"""
Email Agent (Xanny Xan)
Generates random email addresses
"""
import logging
import random
import string
import aiohttp
import json
from config import ENDPOINTS, API_HOSTS, DEFAULT_HEADERS
from agents.proxy import get_proxy

logger = logging.getLogger(__name__)

class EmailAgent:
    """Agent for generating email addresses"""
    
    def __init__(self, db):
        """Initialize the email agent"""
        self.db = db
        self.name = "Xanny Xan"
        self.domains = [
            "gmail.com", 
            "yahoo.com", 
            "hotmail.com", 
            "outlook.com", 
            "icloud.com",
            "protonmail.com",
            "mail.com",
            "aol.com"
        ]
        logger.info(f"{self.name} initialized")
    
    async def generate_email(self, identity=None):
        """Generate a random email address, optionally based on identity"""
        logger.info(f"{self.name} generating email")
        
        try:
            # Use the RapidAPI random user generator to get email
            url = ENDPOINTS["random_user"]
            headers = DEFAULT_HEADERS.copy()
            # No RapidAPI host needed for public APIs
            
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
                
                if identity and random.random() > 0.5:
                    # Use the identity information to create a realistic email 50% of the time
                    name = identity["name"].lower().replace(" ", "")
                    username = identity.get("username", "user")
                    age = str(identity["age"])
                    
                    # Create variants
                    variants = [
                        name,
                        f"{name}{age}",
                        username,
                        f"{name}.{random.choice(string.digits)}{random.choice(string.digits)}",
                        f"{name}_{random.choice(string.digits)}{random.choice(string.digits)}",
                        f"{name[:1]}{identity['name'].split()[-1].lower()}",
                        f"{name[:1]}{identity['name'].split()[-1].lower()}{random.choice(string.digits)}{random.choice(string.digits)}"
                    ]
                    
                    email_user = random.choice(variants)
                    domain = random.choice(self.domains)
                    email = f"{email_user}@{domain}"
                else:
                    # Use the API generated email or fall back to random generation
                    try:
                        email = data["results"][0]["email"]
                    except (KeyError, IndexError, TypeError):
                        # Generate a random username
                        username_length = random.randint(6, 12)
                        username_chars = string.ascii_lowercase + string.digits
                        email_user = ''.join(random.choice(username_chars) for _ in range(username_length))
                        domain = random.choice(self.domains)
                        email = f"{email_user}@{domain}"
            
            logger.info(f"Generated email: {email}")
            return email
                
        except Exception as e:
            logger.error(f"Error generating email: {str(e)}")
            # Fallback to basic email if there's an error
            return f"user{random.randint(1000, 9999)}@example.com"
    
    async def generate_temp_email(self):
        """Generate a temporary disposable email address using RapidAPI Temp Mail service"""
        logger.info(f"{self.name} generating temp email")
        
        try:
            url = ENDPOINTS["temp_email"]
            headers = DEFAULT_HEADERS.copy()
            # No RapidAPI host needed for public APIs
            
            # Get proxy if enabled
            proxy = get_proxy()
            
            async with aiohttp.ClientSession() as session:
                # Use proxy if available
                if proxy:
                    conn = aiohttp.TCPConnector(ssl=False)
                    session._connector = conn
                    async with session.post(url, headers=headers, proxy=proxy) as response:
                        data = await response.json()
                else:
                    async with session.post(url, headers=headers) as response:
                        data = await response.json()
                
                try:
                    # Extract email from the response
                    email = data["email"]
                    logger.info(f"Generated temp email from API: {email}")
                    return email
                except (KeyError, TypeError):
                    # Fallback if API doesn't return expected format
                    raise ValueError("Invalid response from temp email API")
                
        except Exception as e:
            logger.error(f"Error generating temp email: {str(e)}")
            
            # Fallback to a deterministic temp email address
            temp_domains = [
                "temp-mail.org",
                "10minutemail.com",
                "guerrillamail.com",
                "mailinator.com"
            ]
            
            username_length = random.randint(8, 16)
            username_chars = string.ascii_lowercase + string.digits
            email_user = ''.join(random.choice(username_chars) for _ in range(username_length))
            
            domain = random.choice(temp_domains)
            
            email = f"{email_user}@{domain}"
            logger.info(f"Generated fallback temp email: {email}")
            return email
