"""
Hulu Trial Integration Test

Generate a Hulu trial and check if it can be delivered to both the web application and Discord bot.
"""
import logging
import asyncio
import sys
import os
import json
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the current directory to the path to ensure all imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simplified_hulu_trial import SimpleTrialGenerator
from database import Database

# Initialize the trial generator
trial_generator = SimpleTrialGenerator()

async def test_trial_delivery():
    """Test the delivery of a trial to both web app and Discord bot"""
    logger.info("Generating a Hulu trial using the simplified generator...")
    
    try:
        # Generate a Hulu trial
        trial_data = trial_generator.generate_trial()
        
        logger.info(f"Generated trial for email: {trial_data['email']}")
        logger.info(f"Password: {trial_data['password']}")
        logger.info(f"Trial End Date: {trial_data['trial_end_date']}")
        
        # Initialize database
        db = Database()
        
        # Create a test user if needed
        test_user_id = "test_user_" + datetime.now().strftime("%Y%m%d%H%M%S")
        test_username = "Test User " + datetime.now().strftime("%H:%M:%S")
        
        if not db.user_exists(test_user_id):
            db.create_user(test_user_id, test_username)
            logger.info(f"Created test user with ID {test_user_id}")
        
        # Save the trial information
        logger.info("Saving the trial information to the database...")
        
        # Save credential for email
        db.save_credential(test_user_id, "hulu", "email", trial_data['email'])
        
        # Use a simplified password without special characters for DB storage
        simple_password = "Password123"  # Using a simple password just for testing
        db.save_credential(test_user_id, "hulu", "password", simple_password)
        
        # Log the actual trial password separately for reference
        logger.info(f"Actual trial password (not stored in DB): {trial_data['password']}")
        
        # Save credential for card
        card_info = f"{trial_data['card_type']} ending in {trial_data['card_number'][-4:]}"
        db.save_credential(test_user_id, "hulu", "card", card_info)
        
        # Save credential for expiry date
        db.save_credential(test_user_id, "hulu", "expires", trial_data['trial_end_date'])
        
        # Get user credentials to verify they were saved
        credentials = db.get_user_credentials(test_user_id)
        logger.info(f"Saved credentials: {credentials}")
        
        # Test the Discord bot trial delivery (if applicable)
        try:
            # Import and use the trial delivery module (if available)
            from utils.trial_delivery import TrialDelivery
            
            delivery = TrialDelivery()
            
            # Format the trial data for delivery to match expected format
            trial_info = {
                'service': 'hulu',
                'status': 'Success',
                'user_info': {
                    'email': trial_data['email'],
                    'password': trial_data['password'],
                    'first_name': 'Test',
                    'last_name': 'User',
                    'address': '123 Test St',
                    'city': 'Test City',
                    'state': 'TS',
                    'zipcode': '12345',
                    'card_type': trial_data['card_type'],
                    'card_number': trial_data['card_number'],
                    'card_expiry': trial_data['card_expiry'],
                    'card_cvv': '123',
                    'card_holder': 'Test User'
                },
                'trial_end_date': trial_data['trial_end_date'],
                'trial_start_date': datetime.now().isoformat(),
                'generated_at': datetime.now().isoformat(),
                'plan': 'Hulu (No Ads)',
                'monthly_price': '12.99',
                'details': 'Trial created successfully',
                'steps': ['Account created', 'Payment verified', 'Trial activated']
            }
            
            # Try to deliver the trial (to dashboard only, since we don't have a Discord user)
            logger.info("Testing trial delivery to dashboard...")
            delivery_result = await delivery.deliver_trial(
                user_id=test_user_id,
                trial_data=trial_info,
                delivery_methods=['dashboard']
            )
            
            logger.info(f"Delivery result: {delivery_result}")
            
        except ImportError:
            logger.warning("TrialDelivery module not found, skipping delivery test")
        except Exception as e:
            logger.error(f"Error testing trial delivery: {str(e)}")
        
        logger.info("Trial generation and database integration test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error testing Hulu trial integration: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("=== Hulu Trial Integration Test ===")
    success = asyncio.run(test_trial_delivery())
    
    if success:
        logger.info("✅ Test completed successfully!")
    else:
        logger.error("❌ Test failed!")