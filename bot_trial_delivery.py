"""
Bot Trial Delivery Module
Handles delivering trial information to users via Discord DMs and the website
"""
import json
import logging
import sqlite3
from datetime import datetime
import sys

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
        self.db_path = "instance/database.db"
        logger.info("Trial delivery system initialized")
    
    def load_trial_from_file(self, filepath="standalone_hulu_trial.json"):
        """Load trial information from a JSON file"""
        logger.info(f"Loading trial from file: {filepath}")
        
        try:
            with open(filepath, 'r') as f:
                trial_data = json.load(f)
                
            logger.info(f"Loaded trial for {trial_data.get('service', 'unknown service')}")
            return trial_data
        except FileNotFoundError:
            logger.error(f"Trial file not found: {filepath}")
            return None
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in trial file: {filepath}")
            return None
    
    def save_trial_to_database(self, user_id, trial_data):
        """Save trial information to the database for a specific user"""
        logger.info(f"Saving trial for user ID: {user_id}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if we have a trials table, if not create it
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS trials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                service TEXT NOT NULL,
                plan TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                card_last4 TEXT,
                trial_data TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """)
            
            # Format current timestamp
            created_at = datetime.now().isoformat()
            
            # Insert the trial data
            cursor.execute("""
            INSERT INTO trials 
            (user_id, service, plan, email, password, start_date, end_date, card_last4, trial_data, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                trial_data.get("service", "Unknown"),
                trial_data.get("plan", "Unknown"),
                trial_data.get("email", ""),
                trial_data.get("password", ""),
                trial_data.get("start_date", ""),
                trial_data.get("end_date", ""),
                trial_data.get("card_details", {}).get("last4", ""),
                json.dumps(trial_data),
                created_at
            ))
            
            conn.commit()
            logger.info(f"Trial saved to database with user ID: {user_id}")
            
            return {"success": True, "message": "Trial saved successfully"}
        except sqlite3.Error as e:
            logger.error(f"Database error saving trial: {e}")
            return {"success": False, "message": f"Database error: {e}"}
        finally:
            if conn:
                conn.close()
    
    def format_trial_message(self, trial_data):
        """Format trial information for delivery via Discord"""
        service = trial_data.get("service", "Unknown")
        
        message = f"🎉 **Your {service} Trial is Ready!** 🎉\n\n"
        message += f"**Plan:** {trial_data.get('plan', 'Standard')}\n"
        message += f"**Price:** {trial_data.get('price', '$0.00')}\n\n"
        
        message += "**Login Details:**\n"
        message += f"📧 Email: `{trial_data.get('email', 'N/A')}`\n"
        message += f"🔑 Password: `{trial_data.get('password', 'N/A')}`\n\n"
        
        message += "**Payment Details:**\n"
        message += f"💳 {trial_data.get('card', 'Virtual Card')}\n"
        message += f"⏰ Trial Ends: {trial_data.get('end_date', 'N/A')}\n\n"
        
        login_url = ""
        if service.lower() == "hulu":
            login_url = "https://www.hulu.com/login"
        elif service.lower() == "netflix":
            login_url = "https://www.netflix.com/login"
        
        if login_url:
            message += f"**Login here:** {login_url}\n\n"
        
        message += "Enjoy your trial! Remember to cancel before the trial ends to avoid charges."
        
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
        logger.info(f"Delivering trial to user ID: {user_id}")
        
        # Load the latest trial
        trial_data = self.load_trial_from_file()
        if not trial_data:
            logger.error("No trial data found to deliver")
            return {"success": False, "message": "No trial data found"}
        
        # Save to database for dashboard display
        save_result = self.save_trial_to_database(user_id, trial_data)
        if not save_result["success"]:
            logger.error(f"Failed to save trial to database: {save_result['message']}")
            # Continue anyway to deliver via Discord
        
        # Format for Discord if discord_id is provided
        discord_delivery = {"success": False, "message": "Discord delivery not requested"}
        if discord_id:
            message = self.format_trial_message(trial_data)
            logger.info(f"Formatted Discord message for user: {discord_id}")
            
            # In a real implementation, we would send the message to Discord here
            # For now, we just log it
            logger.info(f"Would send Discord message to {discord_id}: {message[:100]}...")
            discord_delivery = {"success": True, "message": "Discord message ready for delivery"}
        
        return {
            "success": True,
            "trial_data": trial_data,
            "database_save": save_result,
            "discord_delivery": discord_delivery
        }


# Run if executed directly
if __name__ == "__main__":
    print("=== Trial Delivery System ===")
    
    delivery = TrialDelivery()
    
    # For testing, use a test user ID
    test_user_id = 12345
    
    trial = delivery.load_trial_from_file()
    if trial:
        print(f"Loaded trial for {trial['service']}")
        
        # Format message
        message = delivery.format_trial_message(trial)
        print("\n=== Formatted Discord Message ===")
        print(message)
        
        # Save to database
        print("\n=== Saving to Database ===")
        result = delivery.save_trial_to_database(test_user_id, trial)
        print(f"Save result: {result}")
        
        # Full delivery process
        print("\n=== Full Delivery Process ===")
        delivery_result = delivery.deliver_trial_to_user(test_user_id, "test_discord_id")
        print(f"Delivery successful: {delivery_result['success']}")
    else:
        print("No trial found to deliver")