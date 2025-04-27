"""
Simplified Hulu Trial Generator
A more direct approach to generate a Hulu trial
"""
import asyncio
import random
import string
import logging
import sys
import json
import os
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("simplified_hulu_trial.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def generate_password(length=12):
    """Generate a random password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

# Simplified functions to generate random data without API dependencies
def generate_random_name(gender=None):
    """Generate a random first name based on gender"""
    male_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"]
    female_names = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
    
    if gender == "male":
        return random.choice(male_names)
    elif gender == "female":
        return random.choice(female_names)
    else:
        all_names = male_names + female_names
        return random.choice(all_names)
    
def generate_random_surname():
    """Generate a random surname"""
    surnames = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", 
                "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]
    return random.choice(surnames)

def generate_random_street():
    """Generate a random street address"""
    street_types = ["Street", "Avenue", "Boulevard", "Drive", "Lane", "Road", "Court", "Way", "Place", "Circle"]
    names = ["Main", "Oak", "Pine", "Maple", "Cedar", "Elm", "Washington", "Park", "Lake", "Hill", "Spring", "River"]
    
    number = random.randint(100, 9999)
    name = random.choice(names)
    street_type = random.choice(street_types)
    
    return f"{number} {name} {street_type}"

def generate_random_city():
    """Generate a random US city"""
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", 
              "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "Indianapolis", 
              "San Francisco", "Seattle", "Denver", "Washington", "Boston", "Nashville", "Baltimore"]
    return random.choice(cities)

def generate_random_state():
    """Generate a random US state code"""
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", 
              "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", 
              "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    return random.choice(states)

def generate_random_zipcode():
    """Generate a random 5-digit zipcode"""
    return f"{random.randint(10000, 99999)}"

def generate_random_email(first_name, last_name):
    """Generate a random email based on name"""
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com", "icloud.com", "mail.com"]
    separators = ["", ".", "_", "-"]
    
    separator = random.choice(separators)
    domain = random.choice(domains)
    random_num = random.randint(1, 9999)
    
    email = f"{first_name.lower()}{separator}{last_name.lower()}{random_num}@{domain}"
    return email

def generate_random_phone():
    """Generate a random US phone number"""
    area_code = random.randint(201, 999)
    prefix = random.randint(201, 999)
    line = random.randint(1000, 9999)
    return f"{area_code}-{prefix}-{line}"

def generate_card_number(card_type="visa"):
    """Generate a realistic credit card number with Luhn check"""
    # Card prefixes
    prefixes = {
        "visa": ["4"],
        "mastercard": ["51", "52", "53", "54", "55"],
        "amex": ["34", "37"],
        "discover": ["6011"]
    }
    
    # Card lengths
    lengths = {
        "visa": 16,
        "mastercard": 16,
        "amex": 15,
        "discover": 16
    }
    
    # Get prefix and length for the specified card type
    prefix = random.choice(prefixes.get(card_type.lower(), ["4"]))
    length = lengths.get(card_type.lower(), 16)
    
    # Generate the initial card number
    card_number = prefix
    
    # Generate random digits
    remaining_length = length - len(prefix) - 1  # -1 for the check digit
    for _ in range(remaining_length):
        card_number += str(random.randint(0, 9))
    
    # Apply Luhn algorithm to calculate check digit
    total = 0
    for i, digit in enumerate(reversed(card_number)):
        digit = int(digit)
        if i % 2 == 1:  # Odd positions (0-indexed reversed)
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
        
    check_digit = (10 - (total % 10)) % 10
    card_number += str(check_digit)
    
    return card_number

def generate_card_expiry():
    """Generate a future expiry date (MM/YY)"""
    current_year = datetime.now().year % 100  # Get last two digits of year
    current_month = datetime.now().month
    
    # Generate a random future date within 5 years
    year = random.randint(current_year, current_year + 5)
    
    # If it's the current year, make sure the month is in the future
    if year == current_year:
        month = random.randint(current_month + 1, 12)
    else:
        month = random.randint(1, 12)
    
    return f"{month:02d}/{year:02d}"

def generate_cvv(card_type="visa"):
    """Generate a CVV based on card type"""
    if card_type.lower() == "amex":
        return str(random.randint(1000, 9999))
    else:
        return str(random.randint(100, 999))

async def generate_hulu_trial():
    """Generate a complete Hulu trial with all required components"""
    logger.info("Generating Hulu trial with local methods")
    
    # Generate identity
    gender = random.choice(["male", "female"])
    first_name = generate_random_name(gender)
    last_name = generate_random_surname()
    
    # Generate address
    street = generate_random_street()
    city = generate_random_city()
    state = generate_random_state()
    zipcode = generate_random_zipcode()
    
    # Generate contact info
    email = generate_random_email(first_name, last_name)
    phone = generate_random_phone()
    password = generate_password()
    
    # Generate payment info
    card_type = random.choice(["visa", "mastercard", "amex", "discover"])
    card_number = generate_card_number(card_type)
    card_expiry = generate_card_expiry()
    cvv = generate_cvv(card_type)
    
    # Build the complete user profile
    user_info = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "address": street,
        "city": city,
        "state": state,
        "zipcode": zipcode,
        "phone": phone,
        "card_type": card_type,
        "card_number": card_number,
        "card_expiry": card_expiry,
        "card_cvv": cvv,
        "card_holder": f"{first_name} {last_name}"
    }
    
    # Log the generated information
    logger.info(f"Generated identity: {first_name} {last_name}")
    logger.info(f"Generated email: {email}")
    logger.info(f"Generated address: {street}, {city}, {state} {zipcode}")
    logger.info(f"Generated phone: {phone}")
    logger.info(f"Generated card: **** **** **** {card_number[-4:]}, Exp: {card_expiry}, CVV: {cvv}")
    
    # Calculate trial expiration
    trial_start_date = datetime.now()
    trial_end_date = trial_start_date + timedelta(days=30)  # Hulu typically offers 30-day trials
    
    logger.info(f"Trial start date: {trial_start_date.strftime('%Y-%m-%d')}")
    logger.info(f"Trial end date: {trial_end_date.strftime('%Y-%m-%d')}")
    
    # Return the complete trial information
    return {
        "user_info": user_info,
        "trial_start_date": trial_start_date.isoformat(),
        "trial_end_date": trial_end_date.isoformat(),
        "service": "hulu",
        "plan": "Hulu (No Ads)",
        "monthly_price": "$12.99",
        "generated_at": datetime.now().isoformat()
    }

async def main():
    """Main function to run the trial generation"""
    print("=== Simplified Hulu Trial Generator ===")
    print("Generating a complete Hulu trial without API dependencies...")
    
    try:
        trial_info = await generate_hulu_trial()
        
        # Save the trial information to a file
        with open("hulu_trial_info.json", "w") as f:
            json.dump(trial_info, f, indent=2)
        
        print("\n=== Trial Information ===")
        print(f"Name: {trial_info['user_info']['first_name']} {trial_info['user_info']['last_name']}")
        print(f"Email: {trial_info['user_info']['email']}")
        print(f"Password: {trial_info['user_info']['password']}")
        print(f"Card: **** **** **** {trial_info['user_info']['card_number'][-4:]}")
        print(f"Expiry: {trial_info['user_info']['card_expiry']}")
        print(f"Plan: {trial_info['plan']} ({trial_info['monthly_price']})")
        print(f"Trial Ends: {trial_info['trial_end_date'].split('T')[0]}")
        print("\nComplete trial information saved to hulu_trial_info.json")
        
    except Exception as e:
        print(f"Error generating trial: {str(e)}")
        logger.exception("Trial generation failed")

if __name__ == "__main__":
    asyncio.run(main())