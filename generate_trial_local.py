"""
Generate a Hulu Trial Locally
Uses local generation methods rather than external APIs
"""
import random
import string
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Data for random generation
FIRST_NAMES = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Sarah", 
               "Emily", "Jessica", "Ashley", "Jennifer", "Amanda", "Elizabeth", "Linda", "Patricia", "Mary"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
             "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez"]
CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", 
         "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte"]
STATES = ["NY", "CA", "IL", "TX", "AZ", "PA", "FL", "OH", "NC", "GA", "WA", "VA", "MA", "MI", "NJ"]
STREETS = ["Main St", "First St", "Second St", "Oak St", "Maple Ave", "Washington St", "Park Ave", "Elm St", 
          "Lake St", "Pine St", "Cedar St", "Sunset Blvd", "Broadway", "Highland Ave", "River Rd"]
DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "icloud.com", "mail.com", "protonmail.com"]
CARD_TYPES = ["visa", "mastercard", "amex", "discover"]

def generate_random_number(min_val, max_val):
    """Generate a random number between min_val and max_val"""
    return random.randint(min_val, max_val)

def generate_street_number():
    """Generate a random street number"""
    return random.randint(100, 9999)

def generate_zipcode():
    """Generate a random 5-digit zipcode"""
    return str(random.randint(10000, 99999))

def generate_phone_number():
    """Generate a random US phone number"""
    area_code = random.randint(200, 999)
    middle = random.randint(200, 999)
    last = random.randint(1000, 9999)
    return f"+1 ({area_code}) {middle}-{last}"

def generate_email(first_name, last_name):
    """Generate an email address based on a name"""
    domain = random.choice(DOMAINS)
    separator = random.choice([".", "_", ""])
    suffix = random.choice(["", str(random.randint(1, 99))])
    return f"{first_name.lower()}{separator}{last_name.lower()}{suffix}@{domain}"

def generate_password(length=12):
    """Generate a random password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_card_number(card_type):
    """Generate a valid credit card number based on card type"""
    prefix_map = {
        "visa": ["4"],
        "mastercard": ["51", "52", "53", "54", "55"],
        "amex": ["34", "37"],
        "discover": ["6011"]
    }
    
    prefix = random.choice(prefix_map[card_type])
    length = 15 if card_type == "amex" else 16
    remaining_digits = length - len(prefix)
    
    # Generate digits
    digits = [int(d) for d in prefix]
    for _ in range(remaining_digits - 1):
        digits.append(random.randint(0, 9))
    
    # Calculate Luhn check digit
    checksum = 0
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:  # Odd position (from right)
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    
    check_digit = (10 - (checksum % 10)) % 10
    digits.append(check_digit)
    
    # Convert to string
    return ''.join(map(str, digits))

def generate_card_expiry():
    """Generate a future expiry date (MM/YY)"""
    now = datetime.now()
    future = now + timedelta(days=random.randint(365, 1460))  # 1-4 years in future
    return future.strftime("%m/%y")

def generate_cvv(card_type):
    """Generate a CVV based on card type"""
    length = 4 if card_type == "amex" else 3
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def generate_identity():
    """Generate a random identity"""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    gender = random.choice(["male", "female"])
    
    # Calculate date of birth for someone between 25-45 years old
    age = random.randint(25, 45)
    today = datetime.now()
    year = today.year - age
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Avoiding month-specific day limits
    dob = f"{year}-{month:02d}-{day:02d}"
    
    street_number = generate_street_number()
    street = random.choice(STREETS)
    city = random.choice(CITIES)
    state = random.choice(STATES)
    zipcode = generate_zipcode()
    
    email = generate_email(first_name, last_name)
    username = f"{first_name.lower()}{random.randint(1, 999)}"
    password = generate_password()
    phone = generate_phone_number()
    
    return {
        "name": f"{first_name} {last_name}",
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "gender": gender,
        "dob": dob,
        "address": f"{street_number} {street}",
        "city": city,
        "state": state,
        "country": "USA",
        "postcode": zipcode,
        "email": email,
        "username": username,
        "password": password,
        "phone": phone,
        "cell": phone  # Same as phone for simplicity
    }

def generate_card():
    """Generate a random credit card"""
    card_type = random.choice(CARD_TYPES)
    card_number = generate_card_number(card_type)
    expiry = generate_card_expiry()
    cvv = generate_cvv(card_type)
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    
    return {
        "type": card_type,
        "number": card_number,
        "expiry": expiry,
        "cvv": cvv,
        "holder": f"{first_name} {last_name}".upper()
    }

def generate_hulu_trial():
    """Generate a complete Hulu trial"""
    # Generate identity
    logger.info("Generating identity...")
    identity = generate_identity()
    
    # Generate credit card
    logger.info("Generating credit card...")
    card = generate_card()
    
    # Create trial dates
    now = datetime.now()
    expiry = now + timedelta(days=30)  # Hulu free trial is 30 days
    
    # Create a unique password for the Hulu account
    hulu_password = generate_password()
    
    # Compile the trial information
    trial = {
        "service": "Hulu",
        "plan": "Hulu (No Ads)",
        "price": "$14.99/month",
        "identity": identity,
        "card": card,
        "email": identity["email"],
        "phone": identity["phone"],
        "login": {
            "username": identity["email"],
            "password": hulu_password
        },
        "activation_date": now.strftime("%Y-%m-%d"),
        "expiry_date": expiry.strftime("%Y-%m-%d"),
        "auto_renewal": True,
        "cancellation_url": "https://www.hulu.com/account/cancel",
        "notes": "Remember to cancel before trial expiry to avoid charges"
    }
    
    return trial

def main():
    """Main function to run the trial generation"""
    logger.info("Starting Hulu trial generation...")
    
    trial = generate_hulu_trial()
    
    # Display results
    logger.info("\n== HULU TRIAL GENERATED SUCCESSFULLY ==")
    logger.info(f"Service: {trial['service']} - {trial['plan']} ({trial['price']})")
    logger.info(f"Account holder: {trial['identity']['name']}")
    logger.info(f"Login email: {trial['login']['username']}")
    logger.info(f"Password: {trial['login']['password']}")
    logger.info(f"Activation date: {trial['activation_date']}")
    logger.info(f"Expiry date: {trial['expiry_date']}")
    logger.info(f"Payment method: {trial['card']['type'].upper()} ending in {trial['card']['number'][-4:]}")
    logger.info("\nIMPORTANT: To avoid charges, cancel before trial expiry at:")
    logger.info(trial['cancellation_url'])
    
    # Format for nice printing on the console
    print("\n===== HULU TRIAL DETAILS =====")
    print(f"SERVICE: {trial['service']} - {trial['plan']}")
    print(f"COST: {trial['price']} (first 30 days free)")
    print("\n--- ACCOUNT INFO ---")
    print(f"Email: {trial['login']['username']}")
    print(f"Password: {trial['login']['password']}")
    print(f"Activation: {trial['activation_date']}")
    print(f"Expiry: {trial['expiry_date']}")
    print("\n--- PERSONAL INFO ---")
    print(f"Name: {trial['identity']['name']}")
    print(f"Address: {trial['identity']['address']}")
    print(f"City: {trial['identity']['city']}, {trial['identity']['state']} {trial['identity']['postcode']}")
    print(f"Phone: {trial['phone']}")
    print("\n--- PAYMENT INFO ---")
    print(f"Card: {trial['card']['type'].upper()} **** **** **** {trial['card']['number'][-4:]}")
    print(f"Expiry: {trial['card']['expiry']}")
    print(f"CVV: {trial['card']['cvv']}")
    print(f"Holder: {trial['card']['holder']}")
    print("\n--- IMPORTANT ---")
    print("To avoid charges, cancel before trial expiry at:")
    print(trial['cancellation_url'])
    
    return trial

if __name__ == "__main__":
    main()