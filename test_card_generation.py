"""
Test Card Generation
Simple script to test the CardAgent functionality
"""
import asyncio
import logging
from database import Database
from agents.card_agent import CardAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_card_generation():
    """Test generating a credit card"""
    db = Database()
    card_agent = CardAgent(db)
    
    logger.info("Generating credit card...")
    card = await card_agent.generate_card()
    
    logger.info("Card Generation Results:")
    logger.info(f"Type: {card['type']}")
    logger.info(f"Number: {card['number']}")
    logger.info(f"Expiry: {card['expiry']}")
    logger.info(f"CVV: {card['cvv']}")
    logger.info(f"Holder: {card['holder']}")
    
    return card

if __name__ == "__main__":
    card = asyncio.run(test_card_generation())
    print("\nGenerated Card:")
    print(f"Card Type: {card['type']}")
    print(f"Card Number: {card['number']}")
    print(f"Expiry Date: {card['expiry']}")
    print(f"CVV: {card['cvv']}")
    print(f"Card Holder: {card['holder']}")