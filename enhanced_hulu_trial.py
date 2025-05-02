#!/usr/bin/env python3
"""
Enhanced Hulu Trial Generator
Creates a Hulu trial with realistic information and integrates
with the Trial Junkie delivery system
"""
import os
import json
import logging
import asyncio
import sys
import random
from datetime import datetime, timedelta
from utils.trial_generator import TrialGenerator
from utils.trial_delivery import TrialDelivery
from database import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("enhanced_hulu_trial.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class EnhancedHuluTrialGenerator:
    """
    Enhanced generator for Hulu trials that delivers results 
    through the Trial Junkie platform
    """
    def __init__(self):
        """Initialize the generator"""
        self.trial_generator = TrialGenerator()
        self.trial_delivery = TrialDelivery()
        self.db = Database()
        
    async def generate_and_deliver_trial(self, user_id, discord_id=None):
        """
        Generate a Hulu trial and deliver it to the user
        
        Args:
            user_id (str/int): The user ID in the database
            discord_id (str/int, optional): The Discord ID if available
            
        Returns:
            dict: Trial information and delivery status
        """
        try:
            # Log start of operation
            logger.info(f"Generating Hulu trial for user {user_id}")
            
            # Generate the Hulu trial
            trial_data = await self.trial_generator.generate_trial("hulu")
            
            # Format the trial data into a more user-friendly format
            formatted_trial = self.format_trial_for_user(trial_data)
            
            # Save the formatted trial to file for easy access
            self.save_trial_to_file(formatted_trial)
            
            # Determine delivery methods
            delivery_methods = ['dashboard']
            if discord_id:
                delivery_methods.append('discord')
                
            # Deliver the trial
            delivery_results = {}
            # For Discord delivery, we need to set the bot if we want to do real Discord DMs
            # For this example, we'll just simulate successful dashboard delivery
            
            # Save to dashboard
            dashboard_result = await self.trial_delivery.save_to_dashboard(user_id, trial_data)
            delivery_results['dashboard'] = dashboard_result
            
            logger.info(f"Hulu trial generated and delivered for user {user_id}")
            
            return {
                'trial': formatted_trial,
                'delivery': delivery_results
            }
            
        except Exception as e:
            logger.error(f"Error generating and delivering Hulu trial: {str(e)}")
            return {
                'error': str(e)
            }
    
    def format_trial_for_user(self, trial_data):
        """
        Format trial data into a user-friendly format
        
        Args:
            trial_data (dict): The raw trial data
            
        Returns:
            dict: Formatted trial information
        """
        user_info = trial_data.get('user_info', {})
        payment_info = trial_data.get('payment_info', {})
        service_details = trial_data.get('service_details', {})
        
        # Format card number for display
        card_number = payment_info.get('card_number', '')
        card_type = payment_info.get('card_type', 'visa').capitalize()
        if card_number:
            # Only show last 4 digits
            last_four = card_number[-4:] if len(card_number) >= 4 else card_number
            masked_card = f"{card_type} **** **** **** {last_four}"
        else:
            masked_card = "N/A"
        
        # Parse trial end date
        trial_end = trial_data.get('trial_end_date')
        if trial_end:
            try:
                # Parse ISO format date
                end_date = datetime.fromisoformat(trial_end)
                # Format as YYYY-MM-DD
                formatted_date = end_date.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                formatted_date = trial_end
        else:
            formatted_date = "Unknown"
        
        # Create formatted trial info
        return {
            'service': 'Hulu',
            'name': f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}",
            'email': user_info.get('email', ''),
            'password': user_info.get('password', ''),
            'card': masked_card,
            'plan': service_details.get('plan', 'Hulu (No Ads)'),
            'price': "$14.99/month",
            'end_date': formatted_date,
            'login_url': 'https://www.hulu.com/login',
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def save_trial_to_file(self, trial_data):
        """
        Save trial data to a JSON file
        
        Args:
            trial_data (dict): The trial data to save
        """
        with open("hulu_trial_info.json", "w") as f:
            json.dump(trial_data, f, indent=2)
        
        logger.info(f"Trial information saved to hulu_trial_info.json")

async def run_for_user(user_id, discord_id=None):
    """Run the generator for a specific user"""
    generator = EnhancedHuluTrialGenerator()
    result = await generator.generate_and_deliver_trial(user_id, discord_id)
    return result
        
# Run if executed directly
if __name__ == "__main__":
    print("=== Enhanced Hulu Trial Generator ===")
    
    # Take user_id from command line args if provided
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
    else:
        # Use a test user ID
        user_id = "test_user_123"
    
    # Take discord_id from command line args if provided
    discord_id = None
    if len(sys.argv) > 2:
        discord_id = sys.argv[2]
    
    print(f"Generating Hulu trial for user: {user_id}")
    
    # Run the generator
    result = asyncio.run(run_for_user(user_id, discord_id))
    
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        trial = result['trial']
        print("\n=== Trial Generated Successfully ===")
        print(f"Email: {trial['email']}")
        print(f"Password: {trial['password']}")
        print(f"Plan: {trial['plan']} ({trial['price']})")
        print(f"Trial Ends: {trial['end_date']}")
        print(f"\nDelivery Status:")
        
        delivery = result.get('delivery', {})
        for method, status in delivery.items():
            success = status.get('success', False)
            message = status.get('message', 'Unknown status')
            print(f"  {method.capitalize()}: {'✓' if success else '✗'} {message}")
        
        print("\nLogin at: https://www.hulu.com/login")
        print("To view detailed login instructions, run:")
        print("  python use_real_trial.py")