#!/usr/bin/env python3
"""
Trial Junkie System
Main integration module that connects all components of the Trial Junkie system
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
        logging.FileHandler("trial_junkie_system.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("trial_junkie_system")

class TrialJunkieSystem:
    """
    Central system that coordinates all components of Trial Junkie
    """
    def __init__(self):
        """Initialize the Trial Junkie system"""
        self.db = None
        self.api = None
        self.delivery = None
        
        logger.info("Initializing Trial Junkie system")
        
        # Initialize components
        self._initialize_database()
        self._initialize_api()
        self._initialize_delivery()
    
    def _initialize_database(self):
        """Initialize the database connection"""
        try:
            from database import Database
            
            self.db = Database()
            db_result = self.db.initialize()
            
            if db_result.get("success", False):
                logger.info("Database connection established")
            else:
                logger.warning(f"Database initialization failed: {db_result.get('message')}")
        except ImportError:
            logger.warning("Database module not available")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
    
    def _initialize_api(self):
        """Initialize the API integrations"""
        try:
            from updated_api_integrations import UpdatedAPIIntegrations
            
            self.api = UpdatedAPIIntegrations()
            logger.info("API integrations initialized")
        except ImportError:
            logger.warning("API integrations module not available")
        except Exception as e:
            logger.error(f"Error initializing API integrations: {str(e)}")
    
    def _initialize_delivery(self):
        """Initialize the trial delivery system"""
        try:
            from bot_trial_delivery import TrialDelivery
            
            self.delivery = TrialDelivery(db=self.db)
            logger.info("Trial delivery system initialized")
        except ImportError:
            logger.warning("Trial delivery module not available")
        except Exception as e:
            logger.error(f"Error initializing trial delivery: {str(e)}")
    
    def generate_trial(self, service: str, user_id: int = None, discord_id: str = None) -> Dict[str, Any]:
        """
        Generate a trial for a service and deliver it to the user
        
        Args:
            service: The service to generate a trial for
            user_id: User ID (optional, for database storage)
            discord_id: Discord ID (optional, for delivery via Discord)
            
        Returns:
            dict: Trial generation and delivery result
        """
        if not self.api:
            return {
                "success": False,
                "message": "API integrations not available"
            }
        
        try:
            # Generate trial data
            logger.info(f"Generating trial for service: {service}")
            trial_data = self.api.generate_complete_trial_data(service)
            
            # Save to file for backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"{service}_trial_{timestamp}.json"
            
            with open(file_path, 'w') as f:
                json.dump(trial_data, f, indent=2)
            
            logger.info(f"Trial data saved to {file_path}")
            
            # Save to database if user_id provided
            if user_id and self.db:
                save_result = self.db.save_trial(user_id, trial_data)
                
                if not save_result.get("success", False):
                    logger.warning(f"Failed to save trial to database: {save_result.get('message')}")
            
            # Deliver to user if delivery system available
            if self.delivery:
                if user_id or discord_id:
                    delivery_result = self.delivery.deliver_trial_to_user(
                        user_id=user_id or 0,
                        discord_id=discord_id,
                        trial_data=trial_data
                    )
                    
                    if delivery_result.get("success", False):
                        logger.info("Trial delivered successfully")
                    else:
                        logger.warning(f"Trial delivery failed: {delivery_result.get('message')}")
                    
                    return {
                        "success": True,
                        "trial_data": trial_data,
                        "file_path": file_path,
                        "delivery_result": delivery_result
                    }
            
            return {
                "success": True,
                "trial_data": trial_data,
                "file_path": file_path
            }
        
        except Exception as e:
            logger.error(f"Error generating trial: {str(e)}")
            traceback.print_exc()
            
            return {
                "success": False,
                "message": str(e)
            }
    
    def get_user_trials(self, user_id: int) -> Dict[str, Any]:
        """
        Get all trials for a user
        
        Args:
            user_id: User ID
            
        Returns:
            dict: User trials result
        """
        if not self.db:
            return {
                "success": False,
                "message": "Database not available",
                "trials": []
            }
        
        try:
            return self.db.get_user_trials(user_id)
        except Exception as e:
            logger.error(f"Error getting user trials: {str(e)}")
            
            return {
                "success": False,
                "message": str(e),
                "trials": []
            }
    
    def create_user(self, discord_id: str = None, username: str = None, 
                   email: str = None) -> Dict[str, Any]:
        """
        Create a new user
        
        Args:
            discord_id: Discord user ID
            username: Username
            email: Email address
            
        Returns:
            dict: User creation result
        """
        if not self.db:
            return {
                "success": False,
                "message": "Database not available"
            }
        
        try:
            return self.db.create_user(discord_id, username, email)
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            
            return {
                "success": False,
                "message": str(e)
            }
    
    def close(self):
        """Close all connections and clean up resources"""
        if self.db:
            self.db.close()
            logger.info("Database connection closed")

# For standalone testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Trial Junkie System")
    parser.add_argument("--service", "-s", help="Service to generate trial for", default="hulu")
    parser.add_argument("--user-id", "-u", help="User ID", type=int)
    parser.add_argument("--discord-id", "-d", help="Discord ID")
    parser.add_argument("--action", "-a", help="Action to perform", choices=["generate", "get-trials", "create-user"], default="generate")
    
    args = parser.parse_args()
    
    system = TrialJunkieSystem()
    
    try:
        if args.action == "generate":
            result = system.generate_trial(args.service, args.user_id, args.discord_id)
            
            if result.get("success", False):
                print(f"✅ Trial generated successfully: {result.get('file_path')}")
                
                trial_data = result.get("trial_data", {})
                
                print("\nTrial Information:")
                print(f"Service: {trial_data.get('service', 'Unknown')}")
                print(f"Plan: {trial_data.get('plan', 'Unknown')}")
                print(f"Email: {trial_data.get('email', 'Unknown')}")
                print(f"Password: {trial_data.get('password', 'Unknown')}")
                print(f"Expires: {trial_data.get('end_date', 'Unknown')}")
                
                # Print delivery result if available
                if "delivery_result" in result:
                    delivery_result = result.get("delivery_result", {})
                    if delivery_result.get("success", False):
                        print("\n✅ Trial delivered successfully")
                    else:
                        print(f"\n❌ Trial delivery failed: {delivery_result.get('message')}")
            else:
                print(f"❌ Trial generation failed: {result.get('message')}")
        
        elif args.action == "get-trials":
            if not args.user_id:
                print("❌ User ID is required for get-trials action")
                sys.exit(1)
            
            result = system.get_user_trials(args.user_id)
            
            if result.get("success", False):
                trials = result.get("trials", [])
                print(f"✅ Found {len(trials)} trials for user {args.user_id}")
                
                for i, trial in enumerate(trials, 1):
                    print(f"\nTrial {i}:")
                    print(f"Service: {trial.get('service', 'Unknown')}")
                    print(f"Plan: {trial.get('plan', 'Unknown')}")
                    print(f"Email: {trial.get('email', 'Unknown')}")
                    print(f"Expires: {trial.get('end_date', 'Unknown')}")
            else:
                print(f"❌ Error getting trials: {result.get('message')}")
        
        elif args.action == "create-user":
            if not any([args.discord_id, args.user_id, args.username]):
                print("❌ At least one of discord_id, user_id, or username is required for create-user action")
                sys.exit(1)
            
            result = system.create_user(args.discord_id, args.username)
            
            if result.get("success", False):
                print(f"✅ User created with ID: {result.get('user_id')}")
            else:
                print(f"❌ Error creating user: {result.get('message')}")
    
    finally:
        system.close()