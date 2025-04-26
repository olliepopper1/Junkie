"""
Hulu Trial Generation Test Script
Generates realistic card data via public APIs and runs the Hulu trial automation
"""
import asyncio
import logging
import json
import random
import os
import aiohttp
from datetime import datetime, timedelta
from database import Database
from agents.automation_agent import AutomationAgent
from config import ENDPOINTS, API_HOSTS, DEFAULT_HEADERS

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# No API key needed for public APIs - all endpoints are freely accessible

async def generate_fake_card():
    """Generate a fake credit card using public APIs"""
    url = ENDPOINTS["fake_card"]
    
    # Use the standard headers for public APIs
    headers = DEFAULT_HEADERS.copy()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Log the data structure to see what we're working with
                    logger.info(f"Card API response structure: {data.keys()}")
                    
                    # Extract card information from response
                    # Now using randomuser.me API, create a card from user data
                    if "results" in data and len(data["results"]) > 0:
                        user_data = data["results"][0]
                        
                        # Generate a card based on the user data
                        card_types = ["visa", "mastercard", "amex", "discover"]
                        card_type = random.choice(card_types)
                        
                        # Generate expiry date
                        now = datetime.now()
                        future = now + timedelta(days=random.randint(365, 1460))  # 1-4 years in the future
                        expiry = future.strftime("%m/%y")
                        
                        # Generate card number
                        card_prefixes = {
                            "visa": ["4"],
                            "mastercard": ["51", "52", "53", "54", "55"],
                            "amex": ["34", "37"],
                            "discover": ["6011"]
                        }
                        prefix = random.choice(card_prefixes[card_type])
                        length = 15 if card_type == "amex" else 16
                        remaining_digits = length - len(prefix)
                        number = prefix + ''.join([str(random.randint(0, 9)) for _ in range(remaining_digits)])
                        
                        # Generate CVV
                        cvv_length = 4 if card_type == "amex" else 3
                        cvv = ''.join([str(random.randint(0, 9)) for _ in range(cvv_length)])
                        
                        # Use name from the user data
                        name = f"{user_data.get('name', {}).get('first', 'John')} {user_data.get('name', {}).get('last', 'Doe')}"
                        
                        card = {
                            "type": card_type,
                            "number": number,
                            "expiry": expiry,
                            "cvv": cvv,
                            "holder": name.upper()
                        }
                        
                        logger.info(f"Generated fake card: {card['type'].upper()} ending in {card['number'][-4:]}")
                        return card
                    else:
                        logger.error(f"Unexpected API response structure: {data}")
                        raise ValueError("Invalid API response structure")
                else:
                    error_msg = await response.text()
                    logger.error(f"API error: {response.status} - {error_msg}")
                    raise ValueError(f"API returned status code {response.status}")
    except Exception as e:
        logger.error(f"Error generating card with API: {str(e)}")
        # Return a fallback card in case of API failure
        return {
            "type": "visa",
            "number": "4111111111111111", 
            "expiry": "09/28",
            "cvv": "442",
            "holder": "John Doe"
        }

async def generate_hulu_trial():
    """Generate a complete Hulu trial with fake card data from public APIs"""
    # Create database connection
    db = Database()
    
    # Initialize only the automation agent
    automation_agent = AutomationAgent(db)
    
    # Identity information (this would normally come from an identity API)
    identity = {
        "first_name": "Jessica",
        "last_name": "Parker",
        "gender": "female",
        "dob": "1992-06-15",
        "email": "jparker92@example.com",
        "phone": "202-555-7826",
        "street": "6284 Maple Avenue",
        "city": "Chicago",
        "state": "IL",
        "zipcode": "60601",
        "country": "US"
    }
    
    # Generate a card using the randomuser.me API
    logger.info("Generating credit card using public API...")
    card = await generate_fake_card()
    logger.info(f"Using card: {card['type'].upper()} ending in {card['number'][-4:]}")
    
    # Email and phone
    email = "jparker92@example.com"
    phone = "+1 202-555-7826"
    
    # Compile all credentials
    credentials = [
        {"type": "identity", "value": identity},
        {"type": "card", "value": card},
        {"type": "email", "value": email},
        {"type": "phone", "value": phone}
    ]
    
    # Run the Hulu trial script
    logger.info("Running Hulu trial script...")
    logger.info("Using simulated credentials for demo purposes")
    result = await automation_agent._run_hulu_script(credentials)
    
    # Display the result in a readable format
    logger.info("HULU TRIAL RESULT:")
    logger.info(f"Status: {result['status']}")
    logger.info(f"Service: {result['service']}")
    
    if result.get('credentials'):
        logger.info("Login Credentials:")
        logger.info(f"Email: {result['credentials']['email']}")
        logger.info(f"Password: {result['credentials']['password']}")
        logger.info(f"Activation Date: {result['credentials']['activation_date']}")
        logger.info(f"Expiry Date: {result['credentials']['expiry_date']}")
    
    logger.info("Steps Performed:")
    for step in result['steps']:
        logger.info(f"  {step}")
    
    logger.info("Details:")
    logger.info(result['details'])
    
    return result

if __name__ == "__main__":
    # Run the async function
    result = asyncio.run(generate_hulu_trial())
    
    # Save the result to a file for reference
    with open("hulu_trial_result.json", "w") as f:
        # Remove big objects that can't be JSON serialized
        result_copy = result.copy()
        json.dump(result_copy, f, indent=2, default=str)
    
    logger.info("Result saved to hulu_trial_result.json")