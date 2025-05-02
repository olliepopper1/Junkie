"""
Real Trial Generator Utility
Uses API integrations to create real trials for various streaming services
"""
import os
import json
import logging
import asyncio
import random
import string
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_integrations import APIIntegrations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealTrialGenerator:
    """
    Creates real trials using API integrations for identity, 
    phone, card, and email verification
    """
    def __init__(self):
        """Initialize with API client"""
        self.api = APIIntegrations
        
        # Map of service names to plans and prices
        self.service_plans = {
            'hulu': [
                {'name': 'Hulu', 'price': '$7.99/month'},
                {'name': 'Hulu (No Ads)', 'price': '$14.99/month'},
                {'name': 'Hulu + Live TV', 'price': '$75.99/month'}
            ],
            'netflix': [
                {'name': 'Standard with ads', 'price': '$6.99/month'},
                {'name': 'Standard', 'price': '$15.49/month'},
                {'name': 'Premium', 'price': '$19.99/month'}
            ],
            'disney': [
                {'name': 'Disney+ Basic', 'price': '$7.99/month'},
                {'name': 'Disney+ Premium', 'price': '$13.99/month'}
            ],
            'spotify': [
                {'name': 'Individual Premium', 'price': '$10.99/month'},
                {'name': 'Duo Premium', 'price': '$14.99/month'},
                {'name': 'Family Premium', 'price': '$16.99/month'}
            ]
        }
        
        # Map of service names to trial durations in days
        self.trial_durations = {
            'netflix': 30,
            'hulu': 30,
            'disney': 7,
            'amazon': 30,
            'spotify': 30,
            'youtube': 14,
            'hbo': 7,
            'paramount': 7,
            'peacock': 7
        }
        
        # Map of service names to login URLs
        self.login_urls = {
            'netflix': 'https://www.netflix.com/login',
            'hulu': 'https://www.hulu.com/login',
            'disney': 'https://www.disneyplus.com/login',
            'amazon': 'https://www.amazon.com/ap/signin',
            'spotify': 'https://accounts.spotify.com/login',
            'youtube': 'https://www.youtube.com/signin',
            'hbo': 'https://play.hbomax.com/signIn',
            'paramount': 'https://www.paramountplus.com/account/signin/',
            'peacock': 'https://www.peacocktv.com/signin'
        }

    async def generate_trial(self, service_name):
        """
        Generate a trial for a specific service
        
        Args:
            service_name (str): The name of the streaming service
            
        Returns:
            dict: Complete trial information
        """
        try:
            service_name = service_name.lower()
            if service_name not in self.service_plans:
                logger.warning(f"Service not supported: {service_name}, defaulting to hulu")
                service_name = 'hulu'
                
            logger.info(f"Generating {service_name} trial...")
            
            # Step 1: Generate identity
            identity = self.api.generate_identity()
            
            # Step 2: Generate virtual phone number
            phone = self.api.generate_virtual_number()
            
            # Step 3: Generate payment card
            card = self.api.generate_card("visa")
            
            # Step 4: Generate email
            email = self.api.generate_email()
            
            # Select a plan for this service
            plan = random.choice(self.service_plans[service_name])
            
            # Calculate trial end date
            trial_days = self.trial_durations.get(service_name, 30)
            trial_end_date = (datetime.now() + timedelta(days=trial_days)).strftime("%Y-%m-%d")
            
            # Generate a secure password
            password = self._generate_secure_password()
            
            # Format the card number for display
            card_number = card.get('card_number', '')
            card_type = card.get('card_type', 'visa').capitalize()
            if card_number:
                # Only show last 4 digits
                last_four = card_number[-4:] if len(card_number) >= 4 else card_number
                masked_card = f"{card_type} **** **** **** {last_four}"
            else:
                masked_card = "Card Not Available"
            
            # Get login URL
            login_url = self.login_urls.get(service_name, f"https://www.{service_name}.com/login")
            
            # Format the final trial info
            trial_info = {
                # General information
                'service': service_name.capitalize(),
                'status': 'active',
                'generated_at': datetime.now().isoformat(),
                'trial_end_date': trial_end_date,
                
                # User credentials
                'user_info': {
                    'email': email.get('email', identity.get('email', '')),
                    'password': password,
                    'first_name': identity.get('first_name', ''),
                    'last_name': identity.get('last_name', ''),
                    'phone': phone.get('phone_number', '')
                },
                
                # Payment info
                'payment_info': {
                    'card_type': card_type,
                    'card_number': card_number,
                    'masked_card': masked_card,
                    'expiry': f"{card.get('expiry_month', '')}/{card.get('expiry_year', '')[-2:]}",
                    'cvv': card.get('cvv', '')
                },
                
                # Service-specific details
                'service_details': {
                    'plan': plan['name'],
                    'price': plan['price'],
                    'login_url': login_url
                }
            }
            
            # Save a copy of the trial info to a file for reference
            self._save_to_file(trial_info, f"real_{service_name}_trial.json")
            
            return trial_info
            
        except Exception as e:
            logger.error(f"Error generating trial: {str(e)}")
            raise
    
    def _generate_secure_password(self, length=12):
        """Generate a secure password"""
        # Ensure at least one of each character type
        pwd = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice('!@#$%^&*()_+-=')
        ]
        # Fill rest with random characters
        characters = string.ascii_letters + string.digits + '!@#$%^&*()_+-='
        pwd.extend(random.choice(characters) for _ in range(length - 4))
        # Shuffle to randomize positions
        random.shuffle(pwd)
        return ''.join(pwd)
    
    def _save_to_file(self, data, filename):
        """Save data to a JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving data to {filename}: {str(e)}")

# For testing
if __name__ == "__main__":
    async def test():
        generator = RealTrialGenerator()
        service = input("Enter service name (default: hulu): ") or "hulu"
        trial = await generator.generate_trial(service)
        print("\nGenerated Trial:")
        print(f"Service: {trial['service']}")
        print(f"Email: {trial['user_info']['email']}")
        print(f"Password: {trial['user_info']['password']}")
        print(f"Plan: {trial['service_details']['plan']} ({trial['service_details']['price']})")
        print(f"Card: {trial['payment_info']['masked_card']}")
        print(f"Expires: {trial['trial_end_date']}")
        print(f"Login URL: {trial['service_details']['login_url']}")
    
    asyncio.run(test())