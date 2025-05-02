"""
Standalone Hulu Trial Generator

Generate a simplified Hulu trial without database integration.
"""
import logging
import json
import random
import string
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_random_string(length=10, include_special=True):
    """Generate a random string of specified length"""
    characters = string.ascii_letters + string.digits
    if include_special:
        characters += "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

def generate_hulu_trial():
    """Generate a complete Hulu trial"""
    logger.info("Generating standalone Hulu trial")
    
    # Generate random user data
    first_name = random.choice(["James", "John", "Robert", "Michael", "William", "David", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth"])
    last_name = random.choice(["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"])
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}@example.com"
    password = generate_random_string(12, include_special=True)
    
    # Generate card data
    card_types = ["Visa", "Mastercard", "Amex"]
    card_type = random.choice(card_types)
    card_number = "4" + ''.join(random.choice(string.digits) for _ in range(15))  # Visa format
    
    # Generate expiry date 2-4 years in the future
    current_year = datetime.now().year % 100  # Get last 2 digits
    expiry_year = current_year + random.randint(2, 4)
    expiry_month = random.randint(1, 12)
    card_expiry = f"{expiry_month:02d}/{expiry_year:02d}"
    
    # Generate cvv
    cvv = ''.join(random.choice(string.digits) for _ in range(3))
    
    # Generate trial dates
    trial_start = datetime.now()
    trial_end = trial_start + timedelta(days=30)
    
    # Create the trial data
    trial_data = {
        "service": "Hulu",
        "plan": "Hulu (No Ads)",
        "monthly_price": "$12.99",
        "user_info": {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "card_type": card_type,
            "card_number": card_number,
            "card_expiry": card_expiry,
            "cvv": cvv
        },
        "trial_start_date": trial_start.strftime("%Y-%m-%d"),
        "trial_end_date": trial_end.strftime("%Y-%m-%d"),
        "generated_at": datetime.now().isoformat()
    }
    
    # Save to file
    with open("standalone_hulu_trial.json", "w") as f:
        json.dump(trial_data, f, indent=2)
    
    # Print details
    logger.info(f"Generated Hulu trial for {first_name} {last_name}")
    logger.info(f"Email: {email}")
    logger.info(f"Password: {password}")
    logger.info(f"Card: {card_type} **** **** **** {card_number[-4:]}")
    logger.info(f"Expiry: {card_expiry}")
    logger.info(f"Trial ends: {trial_end.strftime('%Y-%m-%d')}")
    logger.info(f"Details saved to standalone_hulu_trial.json")
    
    return trial_data

if __name__ == "__main__":
    print("=== Standalone Hulu Trial Generator ===")
    trial = generate_hulu_trial()
    
    # Print a nice summary
    print("\n=== Trial Information ===")
    print(f"Name: {trial['user_info']['first_name']} {trial['user_info']['last_name']}")
    print(f"Email: {trial['user_info']['email']}")
    print(f"Password: {trial['user_info']['password']}")
    print(f"Card: {trial['user_info']['card_type']} **** **** **** {trial['user_info']['card_number'][-4:]}")
    print(f"Plan: {trial['plan']} ({trial['monthly_price']})")
    print(f"Trial Ends: {trial['trial_end_date']}")
    print("\nThis trial has been generated successfully and saved to standalone_hulu_trial.json")