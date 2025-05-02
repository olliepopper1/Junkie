#!/usr/bin/env python3
"""
Bot Trial Delivery Module
Handles delivering trial information to users via Discord DMs and the website
"""
import os
import sys
import json
import logging
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_trial_delivery.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("trial_delivery")

class TrialDelivery:
    """
    Delivers trial information to users through multiple channels
    """
    def __init__(self, db = None):
        """
        Initialize the delivery system with database connection
        
        Args:
            db: Database instance (if None, will be created)
        """
        self.db = db
        
        # Initialize database if not provided
        if not self.db:
            try:
                from database import Database
                self.db = Database()
                db_result = self.db.initialize()
                
                if not db_result.get("success", False):
                    logger.warning(f"Database initialization failed: {db_result.get('message')}")
                else:
                    logger.info("Database connection established")
            except ImportError:
                logger.warning("Database module not available")
            except Exception as e:
                logger.error(f"Error initializing database: {str(e)}")
    
    def load_trial_from_file(self, filepath: str = "hulu_trial.json") -> Dict[str, Any]:
        """
        Load trial information from a JSON file
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            dict: Trial information
        """
        try:
            with open(filepath, 'r') as f:
                trial_data = json.load(f)
                return trial_data
        except Exception as e:
            logger.error(f"Error loading trial from file {filepath}: {str(e)}")
            return {}
    
    def save_trial_to_database(self, user_id: int, trial_data: Dict[str, Any]) -> bool:
        """
        Save trial information to the database for a specific user
        
        Args:
            user_id: The user ID
            trial_data: The trial information
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        if not self.db:
            logger.error("No database connection available")
            return False
        
        try:
            result = self.db.save_trial(user_id, trial_data)
            return result.get("success", False)
        except Exception as e:
            logger.error(f"Error saving trial to database: {str(e)}")
            return False
    
    def format_trial_message(self, trial_data: Dict[str, Any]) -> str:
        """
        Format trial information for delivery via Discord
        
        Args:
            trial_data: The trial information
            
        Returns:
            str: Formatted message
        """
        service = trial_data.get("service", "Unknown").title()
        plan = trial_data.get("plan", "Basic")
        
        # Format card details
        card_details = trial_data.get("card_details", {})
        card_type = card_details.get("type", "Unknown").upper() if card_details else "Unknown"
        card_last4 = card_details.get("last4", "XXXX") if card_details else "XXXX"
        
        # Create a nicely formatted message
        message = f"""
📋 **{service} Trial Account**

Your {service} trial is ready! Here are your login details:

**Service:** {service}
**Plan:** {plan}
**Valid Until:** {trial_data.get('end_date', 'Unknown')}

**Login Information:**
Email: {trial_data.get('email', 'N/A')}
Password: {trial_data.get('password', 'N/A')}

**Personal Info Used:**
Name: {trial_data.get('first_name', 'John')} {trial_data.get('last_name', 'Doe')}
Phone: {trial_data.get('phone', 'N/A')}

**Payment Method:**
Card Type: {card_type}
Last 4: {card_last4}

⚠️ Remember to cancel before the trial ends to avoid charges.
        """
        
        return message.strip()
    
    def format_trial_html(self, trial_data: Dict[str, Any]) -> str:
        """
        Format trial information as HTML for the website
        
        Args:
            trial_data: The trial information
            
        Returns:
            str: HTML formatted trial information
        """
        service = trial_data.get("service", "Unknown").title()
        plan = trial_data.get("plan", "Basic")
        
        # Format card details
        card_details = trial_data.get("card_details", {})
        card_type = card_details.get("type", "Unknown").upper() if card_details else "Unknown"
        card_last4 = card_details.get("last4", "XXXX") if card_details else "XXXX"
        
        # Create HTML
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{service} Trial Login</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1, h2 {{
            color: #9370DB;
        }}
        .info-section {{
            margin: 20px 0;
            border-top: 1px solid #eee;
            padding-top: 10px;
        }}
        .warning {{
            background-color: #fff3cd;
            color: #856404;
            padding: 10px;
            border-radius: 3px;
            margin-top: 20px;
        }}
        .login-details {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 3px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{service} Trial Account</h1>
        <p>Your {service} trial is ready! Here are your login details:</p>
        
        <div class="login-details">
            <strong>Service:</strong> {service}<br>
            <strong>Plan:</strong> {plan}<br>
            <strong>Valid Until:</strong> {trial_data.get('end_date', 'Unknown')}
        </div>
        
        <div class="info-section">
            <h2>Login Information</h2>
            <div class="login-details">
                <strong>Email:</strong> {trial_data.get('email', 'N/A')}<br>
                <strong>Password:</strong> {trial_data.get('password', 'N/A')}
            </div>
        </div>
        
        <div class="info-section">
            <h2>Personal Info Used</h2>
            <div class="login-details">
                <strong>Name:</strong> {trial_data.get('first_name', 'John')} {trial_data.get('last_name', 'Doe')}<br>
                <strong>Phone:</strong> {trial_data.get('phone', 'N/A')}
            </div>
        </div>
        
        <div class="info-section">
            <h2>Payment Method</h2>
            <div class="login-details">
                <strong>Card Type:</strong> {card_type}<br>
                <strong>Last 4:</strong> {card_last4}
            </div>
        </div>
        
        <div class="warning">
            <strong>Important:</strong> Remember to cancel before the trial ends to avoid charges.
        </div>
    </div>
</body>
</html>
        """
        
        return html.strip()
    
    def save_trial_html(self, trial_data: Dict[str, Any], filename: str = None) -> str:
        """
        Save trial information as HTML
        
        Args:
            trial_data: The trial information
            filename: Output filename (if None, generated based on service)
            
        Returns:
            str: Path to the HTML file
        """
        if not filename:
            service = trial_data.get("service", "unknown").lower()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{service}_trial_login_{timestamp}.html"
        
        html = self.format_trial_html(trial_data)
        
        try:
            with open(filename, 'w') as f:
                f.write(html)
            
            logger.info(f"Trial HTML saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving trial HTML: {str(e)}")
            return ""
    
    def deliver_trial_to_user(self, user_id: int, discord_id: str = None, trial_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Deliver a trial to a specific user
        
        Args:
            user_id: The user ID in the database
            discord_id: The Discord ID if available (for Discord delivery)
            trial_data: The trial information (if None, retrieved from database)
            
        Returns:
            dict: Delivery status and trial information
        """
        # Get trial data if not provided
        if not trial_data:
            if not self.db:
                logger.error("No database connection available")
                return {"success": False, "message": "No database connection available"}
            
            # Get the user's most recent trial
            trials_result = self.db.get_user_trials(user_id)
            
            if not trials_result.get("success", False) or not trials_result.get("trials"):
                logger.error(f"No trials found for user {user_id}")
                return {"success": False, "message": "No trials found for user"}
            
            # Use the most recent trial
            trial_data = trials_result.get("trials")[0]
        
        # Format the message
        message = self.format_trial_message(trial_data)
        
        # Save HTML version
        html_file = self.save_trial_html(trial_data)
        
        # If Discord ID is provided, simulate sending a DM
        # (In a real implementation, this would use the Discord API)
        if discord_id:
            logger.info(f"Delivering trial to Discord user {discord_id}")
            
            # Simulate Discord delivery (would use the Discord API in production)
            # For demonstration purposes, we'll just save to a file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            discord_message_file = f"discord_message_{discord_id}_{timestamp}.txt"
            
            try:
                with open(discord_message_file, 'w') as f:
                    f.write(message)
                
                logger.info(f"Discord message saved to {discord_message_file}")
            except Exception as e:
                logger.error(f"Error saving Discord message: {str(e)}")
        
        return {
            "success": True,
            "user_id": user_id,
            "discord_id": discord_id,
            "message": message,
            "html_file": html_file,
            "trial_data": trial_data
        }

# For standalone testing
if __name__ == "__main__":
    delivery = TrialDelivery()
    
    # Load a sample trial
    sample_files = [f for f in os.listdir() if f.startswith("hulu_trial_") and f.endswith(".json")]
    
    if sample_files:
        # Use the most recent file
        sample_file = sorted(sample_files)[-1]
        print(f"Using sample file: {sample_file}")
        
        trial_data = delivery.load_trial_from_file(sample_file)
        
        if trial_data:
            # Print the formatted message
            print("\nFormatted Message:")
            print(delivery.format_trial_message(trial_data))
            
            # Save HTML version
            html_file = delivery.save_trial_html(trial_data)
            print(f"\nHTML saved to: {html_file}")
            
            # Simulate delivery
            result = delivery.deliver_trial_to_user(
                user_id=1,  # Placeholder user ID
                discord_id="123456789",  # Placeholder Discord ID
                trial_data=trial_data
            )
            
            print(f"\nDelivery result: {'Success' if result.get('success') else 'Failed'}")
    else:
        print("No sample trial files found. Please generate a trial first.")
        print("You can use the updated_api_integrations.py or setup_trialjunkie.py to generate a trial.")