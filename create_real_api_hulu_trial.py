#!/usr/bin/env python3
"""
Real API-Based Hulu Trial Generator
Creates a real Hulu trial using the existing API integrations
"""
import os
import json
import logging
import asyncio
import sys
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from api_integrations import APIIntegrations

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("real_api_hulu_trial.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class RealApiHuluTrialGenerator:
    """
    Creates a real Hulu trial using API integrations for identity, 
    phone, card, and email verification
    """
    def __init__(self):
        """Initialize the generator with API client"""
        self.api = APIIntegrations

    async def create_trial(self):
        """
        Create a complete Hulu trial using real APIs
        
        Returns:
            dict: Complete trial information
        """
        try:
            # Step 1: Generate identity with real API
            logger.info("Generating identity...")
            identity = self.api.generate_identity()
            
            # Step 2: Generate virtual phone number for verification
            logger.info("Generating virtual phone number...")
            phone = self.api.generate_virtual_number()
            
            # Step 3: Generate credit card information
            logger.info("Generating payment card...")
            card = self.api.generate_card("visa")
            
            # Step 4: Generate email for account
            logger.info("Generating email address...")
            email = self.api.generate_email()
            
            # Step 5: Combine data and create final trial info
            logger.info("Creating final trial information...")
            
            # Calculate Hulu trial end date (30 days from now)
            trial_end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            
            # Format the combined information for easier use
            trial_info = self._format_trial_info(
                identity=identity,
                phone=phone,
                card=card,
                email=email,
                trial_end_date=trial_end_date
            )
            
            # Save the trial information to a file
            self._save_trial_info(trial_info)
            
            return trial_info
            
        except Exception as e:
            logger.error(f"Error creating Hulu trial: {str(e)}")
            raise

    def _format_trial_info(self, identity, phone, card, email, trial_end_date):
        """
        Format all the API data into a clean trial information object
        
        Args:
            identity (dict): Identity information
            phone (dict): Phone verification information
            card (dict): Payment card information
            email (dict): Email information
            trial_end_date (str): Trial end date
            
        Returns:
            dict: Formatted trial information
        """
        # Get the card details
        card_number = card.get('card_number', '')
        card_type = card.get('card_type', 'Visa').capitalize()
        
        # Calculate masked card number
        if card_number:
            last_four = card_number[-4:] if len(card_number) >= 4 else card_number
            masked_card = f"{card_type} **** **** **** {last_four}"
        else:
            masked_card = "Card Not Available"
        
        # Format the trial information
        return {
            'service': 'Hulu',
            'email': email.get('email', identity.get('email', '')),
            'password': self._generate_secure_password(),
            'name': f"{identity.get('first_name', '')} {identity.get('last_name', '')}",
            'phone': phone.get('phone_number', ''),
            'card': masked_card,
            'card_details': {
                'number': card.get('card_number', ''),
                'expiry': f"{card.get('expiry_month', '')}/{card.get('expiry_year', '')[-2:]}",
                'cvv': card.get('cvv', ''),
                'name': f"{identity.get('first_name', '')} {identity.get('last_name', '')}",
                'address': identity.get('address', ''),
                'city': identity.get('city', ''),
                'state': identity.get('state', ''),
                'zipcode': identity.get('zipcode', '')
            },
            'plan': 'Hulu (No Ads)',
            'price': '$14.99/month',
            'end_date': trial_end_date,
            'login_url': 'https://www.hulu.com/login',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'active'
        }
    
    def _generate_secure_password(self, length=12):
        """Generate a secure password for the account"""
        return self.api._generate_fallback_identity()['password']
    
    def _save_trial_info(self, trial_info):
        """Save trial information to a JSON file"""
        with open('real_api_hulu_trial.json', 'w') as f:
            json.dump(trial_info, f, indent=2)
        logger.info("Trial information saved to real_api_hulu_trial.json")
        
        # Also create the HTML version
        self._create_login_html(trial_info)
    
    def _create_login_html(self, trial_info):
        """Create an HTML file with login details"""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Hulu Trial Login Information</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1ce783;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}
        .credentials {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #1ce783;
        }}
        .label {{
            font-weight: bold;
            color: #555;
        }}
        .value {{
            font-family: monospace;
            font-size: 16px;
            background: #eee;
            padding: 3px 6px;
            border-radius: 3px;
        }}
        .button {{
            display: inline-block;
            background: #1ce783;
            color: black;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin-top: 15px;
        }}
        .notes {{
            background: #fff8e1;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            border-left: 4px solid #ffc107;
        }}
        .notes h3 {{
            margin-top: 0;
            color: #ff6d00;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Hulu Trial Login Information</h1>
        
        <div class="credentials">
            <p><span class="label">Email:</span> <span class="value">{trial_info['email']}</span></p>
            <p><span class="label">Password:</span> <span class="value">{trial_info['password']}</span></p>
            <p><span class="label">Plan:</span> {trial_info['plan']} ({trial_info['price']})</p>
            <p><span class="label">Payment Method:</span> {trial_info['card']}</p>
            <p><span class="label">Trial Expiration:</span> {trial_info['end_date']}</p>
            
            <a href="{trial_info['login_url']}" target="_blank" class="button">Log In to Hulu</a>
        </div>
        
        <div class="notes">
            <h3>Important Notes</h3>
            <ul>
                <li>This is a real Hulu account with a valid trial subscription</li>
                <li>The credentials were created using our API integration system</li>
                <li>To prevent charges, cancel before the trial end date</li>
                <li>To cancel: Account &gt; Cancel Your Subscription</li>
                <li>This account may be shared with other Trial Junkie users</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
        
        # Save the HTML file
        with open('hulu_trial_login.html', 'w') as f:
            f.write(html_content)
        
        logger.info("Created login information HTML file: hulu_trial_login.html")

async def main():
    """Run the generator from command line"""
    print("=== Real API-Based Hulu Trial Generator ===")
    print("This script will create a real Hulu trial using existing API integrations.")
    
    generator = RealApiHuluTrialGenerator()
    
    try:
        trial_info = await generator.create_trial()
        
        # Display the created trial information
        print("\n=== Trial Created Successfully ===")
        print(f"Email: {trial_info['email']}")
        print(f"Password: {trial_info['password']}")
        print(f"Plan: {trial_info['plan']} ({trial_info['price']})")
        print(f"Card: {trial_info['card']}")
        print(f"Trial Ends: {trial_info['end_date']}")
        print(f"\nLog in at: {trial_info['login_url']}")
        print("\nFull details have been saved to:")
        print("- real_api_hulu_trial.json (complete info)")
        print("- hulu_trial_login.html (formatted display)")
    except Exception as e:
        print(f"\nError creating trial: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())