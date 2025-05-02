#!/usr/bin/env python3
"""
Trial Delivery Service

Centralized service for generating and delivering trials to users
via both the web dashboard and Discord
"""
import os
import json
import logging
import traceback
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("trial_delivery.log")
    ]
)
logger = logging.getLogger("trial_delivery_service")

class TrialDeliveryService:
    """
    Service for generating and delivering trials to users
    via both the web dashboard and Discord
    """
    def __init__(self):
        """Initialize the trial delivery service"""
        logger.info("Initializing Trial Delivery Service")
        self.discord_bot = None
        self.db_connection = None
        
        # Try to initialize database connection
        try:
            from database import Database
            self.db_connection = Database()
            logger.info("Database connection established")
        except ImportError:
            logger.warning("Database module not found, database delivery disabled")
        except Exception as e:
            logger.error(f"Error initializing database connection: {e}")
        
        # Try to initialize Discord bot connection
        try:
            from discord_bot_api import DiscordBotAPI
            self.discord_bot = DiscordBotAPI()
            logger.info("Discord bot connection established")
        except ImportError:
            logger.warning("Discord bot module not found, Discord delivery disabled")
        except Exception as e:
            logger.error(f"Error initializing Discord bot connection: {e}")
    
    def generate_trial(self, service_name):
        """Generate a trial for the specified service"""
        logger.info(f"Generating trial for service: {service_name}")
        
        try:
            # Import the necessary components
            from api_integrations import APIIntegrations
            
            # Generate complete trial data
            logger.info(f"Generating trial data for {service_name}...")
            trial_data = APIIntegrations.generate_complete_trial_data(service_name)
            
            # Extract key components
            user_info = trial_data["user_info"]
            payment_info = trial_data["payment_info"]
            
            # Determine the expiration date based on service
            if service_name.lower() == "hulu":
                trial_length_days = 30
                trial_plan = "Hulu (No Ads)"
                trial_price = "$14.99/month"
            elif service_name.lower() == "netflix":
                trial_length_days = 30
                trial_plan = "Standard with ads"
                trial_price = "$6.99/month"
            elif service_name.lower() == "disney":
                trial_length_days = 7
                trial_plan = "Disney+ Basic"
                trial_price = "$7.99/month"
            else:
                trial_length_days = 7
                trial_plan = f"{service_name.title()} Basic"
                trial_price = "$9.99/month"
            
            expiration_date = datetime.now() + timedelta(days=trial_length_days)
            
            # Create trial result structure
            trial_result = {
                "service": service_name.lower(),
                "success": True,
                "creation_date": datetime.now().isoformat(),
                "expiration_date": expiration_date.isoformat(),
                "login_credentials": {
                    "email": user_info["email"],
                    "password": user_info["password"]
                },
                "account_details": {
                    "first_name": user_info["first_name"],
                    "last_name": user_info["last_name"],
                    "plan": trial_plan,
                    "price": trial_price,
                    "trial_length": f"{trial_length_days} days"
                },
                "payment_method": {
                    "card_type": payment_info["card_type"],
                    "last_four": payment_info["card_number"][-4:],
                    "expiry": payment_info["expiry"]
                }
            }
            
            # Save the trial information to a file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{service_name.lower()}_trial_{timestamp}.json"
            
            with open(filename, "w") as f:
                json.dump(trial_result, f, indent=2)
            
            logger.info(f"Trial information saved to {filename}")
            
            return trial_result
            
        except Exception as e:
            logger.error(f"Error generating trial: {e}")
            traceback.print_exc()
            return {"success": False, "error": str(e)}
    
    def deliver_to_dashboard(self, trial_data, user_id):
        """Deliver trial information to user's dashboard"""
        logger.info(f"Delivering trial to dashboard for user {user_id}")
        
        if not self.db_connection:
            logger.error("Cannot deliver to dashboard: No database connection")
            return False
            
        try:
            # Save trial to database for dashboard access
            trial_id = self.db_connection.insert_trial(user_id, trial_data)
            
            logger.info(f"Trial saved to database with ID {trial_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error delivering trial to dashboard: {e}")
            traceback.print_exc()
            return False
    
    def deliver_to_discord(self, trial_data, discord_id):
        """Deliver trial information to user via Discord DM"""
        logger.info(f"Delivering trial to Discord for user {discord_id}")
        
        if not self.discord_bot:
            logger.error("Cannot deliver to Discord: No Discord bot connection")
            return False
            
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
            sent = self.discord_bot.send_direct_message(discord_id, message)
            
            if sent:
                logger.info(f"Trial delivered to Discord user {discord_id}")
                return True
            else:
                logger.error(f"Failed to deliver trial to Discord user {discord_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error delivering trial to Discord: {e}")
            traceback.print_exc()
            return False
    
    def generate_and_deliver(self, service_name, user_id=None, discord_id=None):
        """Generate and deliver a trial"""
        logger.info(f"Generating and delivering {service_name} trial")
        
        # Generate the trial
        trial_result = self.generate_trial(service_name)
        
        if not trial_result.get("success", False):
            logger.error("Trial generation failed")
            return trial_result
        
        # Deliver to dashboard if user_id is provided
        dashboard_delivery = False
        if user_id:
            dashboard_delivery = self.deliver_to_dashboard(trial_result, user_id)
            status = "Success" if dashboard_delivery else "Failed"
            logger.info(f"Dashboard delivery: {status}")
        
        # Deliver to Discord if discord_id is provided
        discord_delivery = False
        if discord_id:
            discord_delivery = self.deliver_to_discord(trial_result, discord_id)
            status = "Success" if discord_delivery else "Failed"
            logger.info(f"Discord delivery: {status}")
        
        # Return the result including delivery status
        delivery_result = {
            **trial_result,
            "delivery": {
                "dashboard": {
                    "delivered": dashboard_delivery,
                    "user_id": user_id
                } if user_id else None,
                "discord": {
                    "delivered": discord_delivery,
                    "discord_id": discord_id
                } if discord_id else None
            }
        }
        
        return delivery_result

def main():
    """Main function for command-line use"""
    parser = argparse.ArgumentParser(description="Generate and deliver a trial")
    parser.add_argument("service", help="The service to generate a trial for")
    parser.add_argument("--user_id", help="User ID for dashboard delivery", default=None)
    parser.add_argument("--discord_id", help="Discord ID for Discord delivery", default=None)
    args = parser.parse_args()
    
    logger.info("Starting trial delivery service")
    service = TrialDeliveryService()
    
    result = service.generate_and_deliver(args.service, args.user_id, args.discord_id)
    
    if result.get("success", False):
        logger.info("Trial successfully generated and delivered")
        return 0
    else:
        logger.error(f"Trial generation failed: {result.get('error', 'Unknown error')}")
        return 1

if __name__ == "__main__":
    exit(main())