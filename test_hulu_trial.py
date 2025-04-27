"""
Comprehensive Hulu Trial Test
Tests the complete Hulu trial creation process with real payment verification
"""
import asyncio
import logging
import os
import random
import string
import sys
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("hulu_test.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import our trial creator and database
from create_real_trial import TrialCreator
from database import Database
from agents.identity_agent import IdentityAgent
from agents.card_agent import CardAgent
from agents.email_agent import EmailAgent
from agents.phone_agent import PhoneAgent

def generate_password(length=12):
    """Generate a random strong password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

async def test_hulu_trial():
    """Run a comprehensive test of Hulu trial creation"""
    logger.info("Starting comprehensive Hulu trial test")
    
    # Create screenshots directory if it doesn't exist
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    
    # Step 1: Initialize database and agents
    logger.info("Initializing database and agents")
    db = Database()
    identity_agent = IdentityAgent(db)
    card_agent = CardAgent(db)
    email_agent = EmailAgent(db)
    phone_agent = PhoneAgent(db)
    
    # Step 2: Generate credentials
    logger.info("Generating identity information")
    identity = await identity_agent.generate_identity(nationality="US")
    logger.info(f"Generated identity: {identity.get('first_name')} {identity.get('last_name')}")
    
    logger.info("Generating credit card information")
    card = await card_agent.generate_card()
    logger.info(f"Generated card ending in: {card.get('number', '')[-4:]}")
    
    logger.info("Generating email address")
    email = await email_agent.generate_email(identity=identity)
    logger.info(f"Generated email: {email}")
    
    logger.info("Generating phone number")
    phone = await phone_agent.generate_phone()
    logger.info(f"Generated phone: {phone}")
    
    # Generate a secure password
    password = generate_password()
    logger.info(f"Generated password: {password}")
    
    # Step 3: Prepare user information
    user_info = {
        "email": email,
        "password": password,
        "first_name": identity.get("first_name", ""),
        "last_name": identity.get("last_name", ""),
        "address": identity.get("street", ""),
        "city": identity.get("city", ""),
        "state": identity.get("state", ""),
        "zipcode": identity.get("postal_code", ""),
        "card_number": card.get("number", ""),
        "card_expiry": card.get("expiry", ""),
        "card_cvv": card.get("cvv", ""),
        "card_holder": f"{identity.get('first_name', '')} {identity.get('last_name', '')}",
        "phone": phone
    }
    
    # Log all the generated credentials
    logger.info("Generated credentials summary:")
    logger.info(f"Name: {user_info['first_name']} {user_info['last_name']}")
    logger.info(f"Email: {user_info['email']}")
    logger.info(f"Password: {user_info['password']}")
    logger.info(f"Address: {user_info['address']}, {user_info['city']}, {user_info['state']} {user_info['zipcode']}")
    logger.info(f"Card: **** **** **** {user_info['card_number'][-4:]}, Exp: {user_info['card_expiry']}, CVV: {user_info['card_cvv']}")
    logger.info(f"Phone: {user_info['phone']}")
    
    # Step 4: Create the trial
    logger.info("Creating Hulu trial account with generated credentials")
    
    # Initialize TrialCreator and run
    creator = TrialCreator()
    
    # Main test - Create the trial
    logger.info("Starting Hulu trial creation process...")
    result = creator.create_trial("hulu", user_info)
    
    # Step 5: Analyze results
    if result.get("success", False):
        logger.info("✅ Hulu trial created successfully!")
        logger.info(f"Final URL: {result.get('final_url', 'N/A')}")
        
        # Calculate trial end date
        trial_days = 30  # Hulu usually offers 30-day trials
        end_date = datetime.now() + timedelta(days=trial_days)
        logger.info(f"Trial started: {datetime.now().strftime('%Y-%m-%d')}")
        logger.info(f"Trial expires: {end_date.strftime('%Y-%m-%d')} (in {trial_days} days)")
        
        # Save the trial information to database
        logger.info("Saving trial information to database")
        try:
            db.save_credential(0, "hulu", "email", user_info["email"])
            db.save_credential(0, "hulu", "password", user_info["password"])
            logger.info("Credentials saved to database")
        except Exception as e:
            logger.error(f"Error saving to database: {str(e)}")
    else:
        logger.error("❌ Hulu trial creation failed")
        if "error" in result:
            logger.error(f"Error details: {result['error']}")
    
    # Return the trial result
    return result

# Main function
async def main():
    """Main function to run the comprehensive test"""
    print("=== Comprehensive Hulu Trial Test ===")
    print("This will test the entire Hulu trial creation process with:")
    print("- Real identity generation")
    print("- Valid credit card generation")
    print("- Email and phone verification")
    print("- Browser automation")
    print("- Payment verification")
    print("- Database storage")
    print("\nResults will be logged to hulu_test.log and displayed on screen.")
    
    try:
        result = await test_hulu_trial()
        
        print("\n=== Test Results ===")
        if result.get("success", False):
            print("✅ TEST PASSED: Hulu trial created successfully!")
            print(f"Login Email: {result.get('email', 'N/A')}")
            print(f"Password: {result.get('password', 'N/A')}")
        else:
            print("❌ TEST FAILED: Could not create Hulu trial")
            if "error" in result:
                print(f"Error: {result['error']}")
            
        print("\nCheck hulu_test.log for detailed logs")
        print("Check the screenshots directory for visual confirmation of the process")
        
    except Exception as e:
        print(f"❌ ERROR: Test encountered an exception: {str(e)}")
        logger.exception("Test failed with exception")

if __name__ == "__main__":
    # Run the test
    asyncio.run(main())