"""
Simplified Hulu Trial Generator
A more direct approach to generate a Hulu trial
"""
import asyncio
import logging
import random
import string
from datetime import datetime, timedelta
from database import Database
from agents.identity_agent import IdentityAgent
from agents.card_agent import CardAgent
from agents.email_agent import EmailAgent
from agents.phone_agent import PhoneAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_password(length=12):
    """Generate a random password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

async def generate_hulu_trial():
    """Generate a complete Hulu trial with all required components"""
    # Initialize database
    db = Database()
    
    # Initialize agents
    identity_agent = IdentityAgent(db)
    card_agent = CardAgent(db)
    email_agent = EmailAgent(db)
    phone_agent = PhoneAgent(db)
    
    # Generate identity (US resident)
    logger.info("Generating identity...")
    identity = await identity_agent.generate_identity(nationality="US")
    
    # Generate credit card
    logger.info("Generating credit card...")
    card = await card_agent.generate_card()
    
    # Generate email address based on identity
    logger.info("Generating email address...")
    email = await email_agent.generate_email(identity)
    
    # Generate phone number (US)
    logger.info("Generating phone number...")
    phone = await phone_agent.generate_phone(country_code="US")
    
    # Generate a secure password
    password = generate_password()
    
    # Create trial dates
    now = datetime.now()
    expiry = now + timedelta(days=30)  # Hulu free trial is 30 days
    
    # Compile the trial information
    trial = {
        "service": "Hulu",
        "plan": "Hulu (No Ads)",
        "price": "$14.99/month",
        "identity": identity,
        "card": card,
        "email": email,
        "phone": phone,
        "login": {
            "username": email,
            "password": password
        },
        "activation_date": now.strftime("%Y-%m-%d"),
        "expiry_date": expiry.strftime("%Y-%m-%d"),
        "auto_renewal": True,
        "cancellation_url": "https://www.hulu.com/account/cancel",
        "notes": "Remember to cancel before trial expiry to avoid charges"
    }
    
    return trial

async def main():
    """Main function to run the trial generation"""
    logger.info("Starting simplified Hulu trial generation...")
    
    trial = await generate_hulu_trial()
    
    # Display results
    logger.info("\n== HULU TRIAL GENERATED SUCCESSFULLY ==")
    logger.info(f"Service: {trial['service']} - {trial['plan']} ({trial['price']})")
    logger.info(f"Account holder: {trial['identity']['name']}")
    logger.info(f"Login email: {trial['login']['username']}")
    logger.info(f"Password: {trial['login']['password']}")
    logger.info(f"Activation date: {trial['activation_date']}")
    logger.info(f"Expiry date: {trial['expiry_date']}")
    logger.info(f"Payment method: {trial['card']['type'].upper()} ending in {trial['card']['number'][-4:]}")
    logger.info("\nIMPORTANT: To avoid charges, cancel before trial expiry at:")
    logger.info(trial['cancellation_url'])
    
    # Format for nice printing on the console
    print("\n===== HULU TRIAL DETAILS =====")
    print(f"SERVICE: {trial['service']} - {trial['plan']}")
    print(f"COST: {trial['price']} (first 30 days free)")
    print("\n--- ACCOUNT INFO ---")
    print(f"Email: {trial['login']['username']}")
    print(f"Password: {trial['login']['password']}")
    print(f"Activation: {trial['activation_date']}")
    print(f"Expiry: {trial['expiry_date']}")
    print("\n--- PERSONAL INFO ---")
    print(f"Name: {trial['identity']['name']}")
    print(f"Address: {trial['identity']['address']}")
    print(f"City: {trial['identity']['city']}, {trial['identity']['state']} {trial['identity']['postcode']}")
    print(f"Phone: {trial['phone']}")
    print("\n--- PAYMENT INFO ---")
    print(f"Card: {trial['card']['type'].upper()} **** **** **** {trial['card']['number'][-4:]}")
    print(f"Expiry: {trial['card']['expiry']}")
    print(f"CVV: {trial['card']['cvv']}")
    print(f"Holder: {trial['card']['holder']}")
    print("\n--- IMPORTANT ---")
    print("To avoid charges, cancel before trial expiry at:")
    print(trial['cancellation_url'])
    
    return trial

if __name__ == "__main__":
    asyncio.run(main())