#!/usr/bin/env python3
"""
Discord Bot API for Trial Junkie

Provides an API for interacting with the Discord bot
"""
import os
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("discord_bot_api.log")
    ]
)
logger = logging.getLogger("discord_bot_api")

class DiscordBotAPI:
    """
    API for interacting with the Discord bot
    
    This class provides methods for sending messages, checking user status,
    and delivering trial information via the Discord bot.
    """
    
    def __init__(self):
        """Initialize the Discord bot API"""
        logger.info("Initializing Discord Bot API")
        self.discord_token = os.environ.get("DISCORD_BOT_TOKEN")
        
        if not self.discord_token:
            logger.warning("No Discord bot token found in environment variables")
            logger.warning("Only simulated Discord operations will be available")
    
    def send_direct_message(self, user_id, message):
        """
        Send a direct message to a Discord user
        
        Args:
            user_id (str): The Discord user ID
            message (str): The message to send
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        logger.info(f"Sending direct message to Discord user {user_id}")
        
        if not self.discord_token:
            logger.warning("Simulating Discord message - no token available")
            logger.info(f"Would send to user {user_id}: {message[:50]}...")
            return self._simulate_send_message(user_id, message)
        
        try:
            # In a real implementation, this would use the Discord.py library
            # to send a direct message to the user
            
            # For now, we'll just simulate it
            return self._simulate_send_message(user_id, message)
        
        except Exception as e:
            logger.error(f"Error sending Discord message: {e}")
            return False
    
    def _simulate_send_message(self, user_id, message):
        """
        Simulate sending a message for testing purposes
        
        Args:
            user_id (str): The Discord user ID
            message (str): The message to send
            
        Returns:
            bool: True to simulate success
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"discord_message_{user_id}_{timestamp}.txt"
        
        try:
            with open(filename, "w") as f:
                f.write(f"To Discord User: {user_id}\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Message:\n\n{message}")
            
            logger.info(f"Simulated Discord message saved to {filename}")
            return True
        
        except Exception as e:
            logger.error(f"Error simulating Discord message: {e}")
            return False
    
    def deliver_trial(self, user_id, trial_data):
        """
        Deliver trial information to a Discord user
        
        Args:
            user_id (str): The Discord user ID
            trial_data (dict): The trial information
            
        Returns:
            bool: True if the trial was delivered successfully, False otherwise
        """
        logger.info(f"Delivering trial to Discord user {user_id}")
        
        try:
            # Format the message
            service = trial_data.get("service", "unknown").title()
            login_credentials = trial_data.get("login_credentials", {})
            account_details = trial_data.get("account_details", {})
            expiration_date = trial_data.get("expiration_date", "unknown")
            
            message = (
                f"🎉 Your {service} trial is ready! 🎉\n\n"
                f"**Login Information**\n"
                f"📧 Email: {login_credentials.get('email', 'N/A')}\n"
                f"🔑 Password: {login_credentials.get('password', 'N/A')}\n\n"
                f"**Plan Details**\n"
                f"📋 Plan: {account_details.get('plan', 'N/A')}\n"
                f"💰 Price: {account_details.get('price', 'N/A')}\n"
                f"⏱️ Expires: {expiration_date}\n\n"
                f"Enjoy your trial! Remember to cancel before the trial ends to avoid charges."
            )
            
            # Send the message
            return self.send_direct_message(user_id, message)
            
        except Exception as e:
            logger.error(f"Error delivering trial to Discord: {e}")
            return False
    
    def check_user_subscription(self, user_id):
        """
        Check a user's subscription status
        
        Args:
            user_id (str): The Discord user ID
            
        Returns:
            dict: The user's subscription status
        """
        logger.info(f"Checking subscription for Discord user {user_id}")
        
        # For demonstration purposes, we'll return a simulated result
        return {
            "discord_id": user_id,
            "has_subscription": True,
            "tier": "premium",
            "subscribed_since": "2025-01-01T00:00:00.000Z",
            "next_billing": "2025-06-01T00:00:00.000Z"
        }
    
    def get_user_trials(self, user_id):
        """
        Get a user's trials
        
        Args:
            user_id (str): The Discord user ID
            
        Returns:
            list: The user's trials
        """
        logger.info(f"Getting trials for Discord user {user_id}")
        
        # For demonstration purposes, we'll read any trial files containing this user ID
        trials = []
        
        try:
            import glob
            
            # Look for trial files
            trial_files = glob.glob("*_trial_*.json")
            
            for file_path in trial_files:
                try:
                    with open(file_path, "r") as f:
                        trial_data = json.load(f)
                    
                    # Add to the list if this is for the user
                    # In a real implementation, this would check the database
                    trials.append(trial_data)
                    
                except Exception as e:
                    logger.error(f"Error reading trial file {file_path}: {e}")
            
            return trials
            
        except Exception as e:
            logger.error(f"Error getting trials for Discord user {user_id}: {e}")
            return []

def test_discord_api():
    """Test the Discord bot API"""
    logger.info("Testing Discord Bot API")
    
    api = DiscordBotAPI()
    
    # Test sending a direct message
    test_user_id = "123456789"
    test_message = "This is a test message from the Discord Bot API."
    
    success = api.send_direct_message(test_user_id, test_message)
    logger.info(f"Send message test: {'Passed' if success else 'Failed'}")
    
    # Test delivering a trial
    test_trial = {
        "service": "test_service",
        "success": True,
        "creation_date": datetime.now().isoformat(),
        "expiration_date": datetime.now().isoformat(),
        "login_credentials": {
            "email": "test@example.com",
            "password": "test_password"
        },
        "account_details": {
            "first_name": "Test",
            "last_name": "User",
            "plan": "Test Plan",
            "price": "$9.99/month",
            "trial_length": "30 days"
        }
    }
    
    success = api.deliver_trial(test_user_id, test_trial)
    logger.info(f"Deliver trial test: {'Passed' if success else 'Failed'}")
    
    return success

if __name__ == "__main__":
    test_discord_api()