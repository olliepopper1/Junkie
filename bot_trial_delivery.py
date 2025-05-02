"""
Bot Trial Delivery Module
Handles delivering trial information to users via Discord DMs and the website
"""
import json
import logging
import sys
from datetime import datetime
from database import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_trial_delivery.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TrialDelivery:
    """
    Delivers trial information to users through multiple channels
    """
    
    def __init__(self):
        """Initialize the delivery system with database connection"""
        self.db = Database()
    
    def load_trial_from_file(self, filepath="standalone_hulu_trial.json"):
        """Load trial information from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                trial_data = json.load(f)
            logger.info(f"Loaded trial data from {filepath}")
            return trial_data
        except Exception as e:
            logger.error(f"Error loading trial data from {filepath}: {str(e)}")
            return None
    
    def save_trial_to_database(self, user_id, trial_data):
        """Save trial information to the database for a specific user"""
        try:
            # Create user if it doesn't exist
            if not self.db.user_exists(user_id):
                self.db.create_user(user_id, f"user_{user_id}")
            
            # Remove special characters from credential values to avoid SQL injection
            def sanitize(value):
                if isinstance(value, str):
                    # Replace problematic characters that might cause SQL issues
                    return value.replace("'", "''").replace("%", "%%")
                return value
            
            # Insert into credentials table
            self.db.save_credential(
                user_id=user_id,
                service=sanitize(trial_data['service']),
                credential_type="email",
                credential_value=sanitize(trial_data['email'])
            )
            
            self.db.save_credential(
                user_id=user_id,
                service=sanitize(trial_data['service']),
                credential_type="password",
                credential_value=sanitize(trial_data['password'])
            )
            
            self.db.save_credential(
                user_id=user_id,
                service=sanitize(trial_data['service']),
                credential_type="plan",
                credential_value=sanitize(trial_data['plan'])
            )
            
            self.db.save_credential(
                user_id=user_id,
                service=sanitize(trial_data['service']),
                credential_type="payment",
                credential_value=sanitize(trial_data['card'])
            )
            
            self.db.save_credential(
                user_id=user_id,
                service=sanitize(trial_data['service']),
                credential_type="expiry",
                credential_value=sanitize(trial_data['end_date'])
            )
            
            logger.info(f"Saved {trial_data['service']} trial for user {user_id} to database")
            return True
        except Exception as e:
            logger.error(f"Error saving trial to database: {str(e)}")
            return False
    
    def format_trial_message(self, trial_data):
        """Format trial information for delivery via Discord"""
        message = f"```\n"
        message += f"🎭 TRIAL JUNKIE: {trial_data['service']} Trial Created\n"
        message += f"------------------------\n"
        message += f"✅ Service: {trial_data['service']} - {trial_data['plan']}\n"
        message += f"✅ Login Email: {trial_data['email']}\n"
        message += f"✅ Password: {trial_data['password']}\n"
        message += f"✅ Payment Method: {trial_data['card']}\n"
        message += f"✅ Trial Ends: {trial_data['end_date']}\n"
        message += f"------------------------\n"
        message += f"Login at: https://www.hulu.com/login\n"
        message += f"```\n"
        message += "Remember to cancel before the trial ends to avoid being charged."
        
        return message
    
    def deliver_trial_to_user(self, user_id, discord_id=None):
        """
        Deliver a trial to a specific user
        
        Args:
            user_id: The user ID in the database
            discord_id: The Discord ID if available (for Discord delivery)
            
        Returns:
            dict: Delivery status and trial information
        """
        # Load the most recent trial
        trial_data = self.load_trial_from_file()
        if not trial_data:
            return {"success": False, "error": "Could not load trial data"}
        
        # Save to database
        db_save = self.save_trial_to_database(user_id, trial_data)
        if not db_save:
            return {"success": False, "error": "Could not save trial to database"}
        
        # Format for message delivery
        message = self.format_trial_message(trial_data)
        
        return {
            "success": True,
            "trial": trial_data,
            "message": message,
            "discord_id": discord_id
        }

# If run directly, test the delivery
if __name__ == "__main__":
    # Test user ID (this would normally come from the database)
    test_user_id = "test_user_123"
    
    print("=== Testing Trial Delivery ===")
    delivery = TrialDelivery()
    
    result = delivery.deliver_trial_to_user(test_user_id)
    
    if result["success"]:
        print("✅ Trial successfully delivered to database")
        print("\nMessage for Discord delivery:")
        print(result["message"])
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")