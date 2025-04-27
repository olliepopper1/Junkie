"""
Simplified Hulu Trial Generator
Generates trial data without relying on external APIs
"""
import os
import json
import random
import string
import logging
import datetime
from datetime import timedelta

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_random_number(min_val, max_val):
    """Generate a random number between min_val and max_val"""
    return random.randint(min_val, max_val)

def generate_street_number():
    """Generate a random street number"""
    return str(random.randint(1, 9999))

def generate_street_name():
    """Generate a random street name"""
    street_types = ["Street", "Avenue", "Boulevard", "Lane", "Drive", "Court", "Place", "Road"]
    street_names = ["Main", "Park", "Oak", "Pine", "Maple", "Cedar", "Elm", "Washington", "Lake", "Hill"]
    return f"{random.choice(street_names)} {random.choice(street_types)}"

def generate_zipcode():
    """Generate a random 5-digit zipcode"""
    return f"{random.randint(10000, 99999)}"

def generate_phone_number():
    """Generate a random US phone number"""
    area_code = random.randint(100, 999)
    prefix = random.randint(100, 999)
    line = random.randint(1000, 9999)
    return f"{area_code}-{prefix}-{line}"

def generate_email(first_name, last_name):
    """Generate an email address based on a name"""
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com"]
    numbers = ''.join(random.choices(string.digits, k=4))
    return f"{first_name.lower()}{last_name.lower()}{numbers}@{random.choice(domains)}"

def generate_password(length=12):
    """Generate a random password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = ''.join(random.choices(chars, k=length))
    return password

def generate_card_number(card_type):
    """Generate a valid credit card number based on card type"""
    if card_type.lower() == "visa":
        # Visa starts with 4
        return "4" + ''.join(random.choices(string.digits, k=15))
    elif card_type.lower() == "mastercard":
        # Mastercard starts with 5
        return "5" + ''.join(random.choices(string.digits, k=15))
    elif card_type.lower() == "amex":
        # Amex starts with 34 or 37 and has 15 digits
        return random.choice(["34", "37"]) + ''.join(random.choices(string.digits, k=13))
    else:
        # Generic
        return ''.join(random.choices(string.digits, k=16))

def generate_card_expiry():
    """Generate a future expiry date (MM/YY)"""
    current_year = datetime.datetime.now().year % 100  # Get last 2 digits
    current_month = datetime.datetime.now().month
    
    # Generate a date 1-5 years in the future
    year = current_year + random.randint(1, 5)
    month = random.randint(1, 12)
    
    # Ensure the date is in the future
    if year == current_year and month <= current_month:
        month = current_month + 1
        if month > 12:
            month = 1
            year += 1
    
    return f"{month:02d}/{year:02d}"

def generate_cvv(card_type):
    """Generate a CVV based on card type"""
    if card_type.lower() == "amex":
        return str(random.randint(1000, 9999))
    else:
        return str(random.randint(100, 999))

def generate_first_name(gender=None):
    """Generate a random first name"""
    male_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", 
                  "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Mark"]
    female_names = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", 
                    "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Margaret", "Sandra"]
    
    if gender == "male":
        return random.choice(male_names)
    elif gender == "female":
        return random.choice(female_names)
    else:
        return random.choice(male_names + female_names)

def generate_last_name():
    """Generate a random last name"""
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", 
                 "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin"]
    return random.choice(last_names)

def generate_city():
    """Generate a random US city"""
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", 
             "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", 
             "Fort Worth", "Columbus", "San Francisco", "Charlotte", "Indianapolis", "Seattle"]
    return random.choice(cities)

def generate_state():
    """Generate a random US state abbreviation"""
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", 
              "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", 
              "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", 
              "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    return random.choice(states)

def generate_card_type():
    """Generate a random credit card type"""
    card_types = ["visa", "mastercard", "amex"]
    return random.choice(card_types)

def generate_identity():
    """Generate a random identity"""
    gender = random.choice(["male", "female"])
    first_name = generate_first_name(gender)
    last_name = generate_last_name()
    street_number = generate_street_number()
    street = generate_street_name()
    city = generate_city()
    state = generate_state()
    zipcode = generate_zipcode()
    phone = generate_phone_number()
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "street": f"{street_number} {street}",
        "city": city,
        "state": state,
        "zipcode": zipcode,
        "phone": phone
    }

def generate_card():
    """Generate a random credit card"""
    card_type = generate_card_type()
    card_number = generate_card_number(card_type)
    card_expiry = generate_card_expiry()
    card_cvv = generate_cvv(card_type)
    
    return {
        "card_type": card_type,
        "card_number": card_number,
        "expiry": card_expiry,
        "cvv": card_cvv
    }

def generate_hulu_trial():
    """Generate a complete Hulu trial"""
    logger.info("Generating Hulu trial with local methods")
    
    # Generate identity
    identity = generate_identity()
    logger.info(f"Generated identity: {identity['first_name']} {identity['last_name']}")
    
    # Generate email
    email = generate_email(identity['first_name'], identity['last_name'])
    logger.info(f"Generated email: {email}")
    
    # Generate address info
    address = identity['street']
    city = identity['city']
    state = identity['state']
    zipcode = identity['zipcode']
    logger.info(f"Generated address: {address}, {city}, {state} {zipcode}")
    
    # Generate phone
    phone = identity['phone']
    logger.info(f"Generated phone: {phone}")
    
    # Generate password
    password = generate_password()
    
    # Generate card
    card = generate_card()
    card_number = card['card_number']
    card_expiry = card['expiry']
    card_cvv = card['cvv']
    card_type = card['card_type']
    logger.info(f"Generated card: **** **** **** {card_number[-4:]}, Exp: {card_expiry}, CVV: {card_cvv}")
    
    # Generate trial dates
    trial_start_date = datetime.datetime.now()
    trial_end_date = trial_start_date + timedelta(days=30)
    logger.info(f"Trial start date: {trial_start_date.date()}")
    logger.info(f"Trial end date: {trial_end_date.date()}")
    
    # Create the trial object
    trial_info = {
        "user_info": {
            "email": email,
            "password": password,
            "first_name": identity['first_name'],
            "last_name": identity['last_name'],
            "gender": identity['gender'],
            "address": address,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "phone": phone,
            "card_type": card_type,
            "card_number": card_number,
            "card_expiry": card_expiry,
            "card_cvv": card_cvv,
            "card_holder": f"{identity['first_name']} {identity['last_name']}"
        },
        "trial_start_date": trial_start_date.isoformat(),
        "trial_end_date": trial_end_date.isoformat(),
        "service": "hulu",
        "plan": "Hulu (No Ads)",
        "monthly_price": "$12.99",
        "generated_at": datetime.datetime.now().isoformat()
    }
    
    # Save to file
    with open('hulu_trial_info.json', 'w') as f:
        json.dump(trial_info, f, indent=2)
    
    print("\n=== Trial Information ===")
    print(f"Name: {trial_info['user_info']['first_name']} {trial_info['user_info']['last_name']}")
    print(f"Email: {trial_info['user_info']['email']}")
    print(f"Password: {trial_info['user_info']['password']}")
    print(f"Card: **** **** **** {trial_info['user_info']['card_number'][-4:]}")
    print(f"Expiry: {trial_info['user_info']['card_expiry']}")
    print(f"Plan: {trial_info['plan']} (${trial_info['monthly_price'].replace('$', '')})")
    print(f"Trial Ends: {trial_info['trial_end_date'].split('T')[0]}")
    print()
    print("Complete trial information saved to hulu_trial_info.json")
    
    # Return a simpler version for the bot
    return {
        'email': email,
        'password': password,
        'name': f"{identity['first_name']} {identity['last_name']}",
        'card_type': card_type.upper(),
        'card_number': card_number,
        'card_expiry': card_expiry,
        'trial_end_date': trial_end_date.date().isoformat()
    }

if __name__ == "__main__":
    print("=== Simplified Hulu Trial Generator ===")
    print("Generating a complete Hulu trial without API dependencies...")
    generate_hulu_trial()