"""
Test Identity Generation
Simple script to test the IdentityAgent functionality
"""
import asyncio
import logging
from database import Database
from agents.identity_agent import IdentityAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_identity_generation():
    """Test generating an identity"""
    db = Database()
    identity_agent = IdentityAgent(db)
    
    logger.info("Generating identity...")
    identity = await identity_agent.generate_identity(nationality="US")
    
    logger.info("Identity Generation Results:")
    logger.info(f"Name: {identity['name']}")
    logger.info(f"Gender: {identity['gender']}")
    logger.info(f"Age: {identity['age']}")
    logger.info(f"Location: {identity['location']}")
    logger.info(f"Email: {identity['email']}")
    logger.info(f"Phone: {identity['phone']}")
    
    return identity

if __name__ == "__main__":
    identity = asyncio.run(test_identity_generation())
    print("\nGenerated Identity:")
    print(f"Name: {identity['name']}")
    print(f"Gender: {identity['gender']}")
    print(f"Age: {identity['age']}")
    print(f"DOB: {identity['dob']}")
    print(f"Address: {identity['address']}")
    print(f"City: {identity['city']}")
    print(f"State: {identity['state']}")
    print(f"Country: {identity['country']}")
    print(f"Email: {identity['email']}")
    print(f"Phone: {identity['phone']}")
    print(f"Username: {identity['username']}")
    print(f"Password: {identity['password']}")