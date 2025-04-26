"""
Email Agent (Xanny Xan)
Generates random email addresses
"""
import logging
import random
import string
from config import DEFAULT_HEADERS

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
            if identity:
                # Use the identity information to create a more realistic email
                name = identity["name"].lower().replace(" ", "")
                username = identity["username"]
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
            else:
                # Generate a random username
                username_length = random.randint(6, 12)
                username_chars = string.ascii_lowercase + string.digits
                email_user = ''.join(random.choice(username_chars) for _ in range(username_length))
            
            # Select a domain
            domain = random.choice(self.domains)
            
            email = f"{email_user}@{domain}"
            logger.info(f"Generated email: {email}")
            return email
                
        except Exception as e:
            logger.error(f"Error generating email: {str(e)}")
            # Fallback to basic email if there's an error
            return f"user{random.randint(1000, 9999)}@example.com"
    
    async def generate_temp_email(self):
        """Generate a temporary disposable email address"""
        logger.info(f"{self.name} generating temp email")
        
        try:
            # For now, we'll just generate a random string with a temp domain
            # In a real implementation, you'd use a temp mail API
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
            logger.info(f"Generated temp email: {email}")
            return email
                
        except Exception as e:
            logger.error(f"Error generating temp email: {str(e)}")
            # Fallback to basic email if there's an error
            return f"temp{random.randint(1000, 9999)}@temp-mail.org"
