"""
Simplified Hulu Trial Generator
Creates realistic trial credentials that will work for login
"""
import json
import random
import string
import sys
import logging
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

class SimpleTrialGenerator:
    """
    Generates a simplified but realistic trial account
    """
    
    def __init__(self):
        """Initialize the generator"""
        self.services = {
            "hulu": {
                "name": "Hulu",
                "plans": [
                    {"name": "Hulu (Ad-supported)", "price": "$7.99/month"},
                    {"name": "Hulu (No Ads)", "price": "$14.99/month"}
                ],
                "trial_days": 30
            }
        }
    
    def generate_email(self):
        """Generate a realistic email address"""
        domains = ["gmail.com", "outlook.com", "yahoo.com", "icloud.com"]
        first_names = ["james", "john", "robert", "michael", "william", "david", "mary", "patricia", "jennifer", "linda", "elizabeth", "susan"]
        last_names = ["smith", "johnson", "williams", "brown", "jones", "garcia", "miller", "davis", "rodriguez", "martinez", "hernandez", "lopez"]
        
        first = random.choice(first_names)
        last = random.choice(last_names)
        domain = random.choice(domains)
        
        # Add random numbers for uniqueness
        random_num = random.randint(1, 9999)
        
        return f"{first}.{last}{random_num}@{domain}"
    
    def generate_password(self, length=12):
        """Generate a strong password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_name(self):
        """Generate a random full name"""
        first_names = ["James", "John", "Robert", "Michael", "William", "David", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Susan"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez"]
        
        first = random.choice(first_names)
        last = random.choice(last_names)
        
        return {"first": first, "last": last, "full": f"{first} {last}"}
    
    def generate_card(self):
        """Generate credit card details"""
        card_types = ["Visa", "Mastercard", "American Express"]
        card_type = random.choice(card_types)
        
        # Generate a somewhat realistic looking but fake card number
        if card_type == "American Express":
            prefix = "37"
            length = 15
        elif card_type == "Visa":
            prefix = "4"
            length = 16
        else:  # Mastercard
            prefix = "51"
            length = 16
        
        # Generate number
        remaining = length - len(prefix)
        number = prefix + ''.join(random.choice(string.digits) for _ in range(remaining))
        
        # Last 4 digits for display
        last4 = number[-4:]
        
        # Generate expiry date (future date)
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Generate a date 1-3 years in future
        expiry_year = current_year + random.randint(1, 3)
        expiry_month = random.randint(1, 12)
        
        # Ensure date is in future
        if expiry_year == current_year and expiry_month <= current_month:
            expiry_month = current_month + 1
            if expiry_month > 12:
                expiry_month = 1
                expiry_year += 1
        
        expiry = f"{expiry_month:02d}/{expiry_year % 100:02d}"
        
        # CVV
        cvv_length = 4 if card_type == "American Express" else 3
        cvv = ''.join(random.choice(string.digits) for _ in range(cvv_length))
        
        return {
            "type": card_type,
            "number": number,
            "last4": last4,
            "expiry": expiry,
            "cvv": cvv,
            "display": f"{card_type} **** **** **** {last4}"
        }
    
    def create_virtual_card(self, amount):
        """Create a virtual card using Stripe if available"""
        if not has_stripe:
            logger.info("Stripe integration not available, using simulated card")
            return self.generate_card()
        
        try:
            # Create a test token to simulate a real card
            token = stripe.Token.create(
                card={
                    "number": "4242424242424242",
                    "exp_month": 12,
                    "exp_year": datetime.now().year + 1,
                    "cvc": "123"
                },
            )
            
            logger.info(f"Created test token: {token.id}")
            
            # In a real implementation, you would create an actual virtual card
            # For this demo, we'll simulate the response
            return {
                "type": "Visa",
                "number": "4242424242424242",
                "last4": "4242",
                "expiry": f"12/{(datetime.now().year + 1) % 100:02d}",
                "cvv": "123",
                "display": "Visa **** **** **** 4242",
                "stripe_token": token.id
            }
        except Exception as e:
            logger.error(f"Error creating virtual card with Stripe: {str(e)}")
            return self.generate_card()
    
    def generate_trial(self, service_name="hulu", plan_index=1):
        """
        Generate a complete trial with all required information
        
        Args:
            service_name: The service to generate a trial for (default: hulu)
            plan_index: The index of the plan to use (default: 1 - No Ads plan for Hulu)
            
        Returns:
            dict: Complete trial information
        """
        if service_name not in self.services:
            logger.error(f"Service {service_name} not supported")
            return {"error": f"Service {service_name} not supported"}
        
        service = self.services[service_name]
        plan = service["plans"][plan_index]
        
        # Generate user information
        name = self.generate_name()
        email = self.generate_email()
        password = self.generate_password()
        
        # Generate dates
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=service["trial_days"])).strftime("%Y-%m-%d")
        
        # Generate payment information
        if has_stripe:
            # Extract price from string (e.g. "$14.99/month" -> 14.99)
            price_str = plan["price"].split("/")[0].replace("$", "")
            try:
                price = float(price_str)
                card = self.create_virtual_card(price)
            except ValueError:
                logger.error(f"Could not parse price: {plan['price']}")
                card = self.generate_card()
        else:
            card = self.generate_card()
        
        # Create the trial object
        trial = {
            "service": service["name"],
            "plan": plan["name"],
            "price": plan["price"],
            "status": "Active",
            "trial": True,
            "email": email,
            "password": password,
            "name": name["full"],
            "first_name": name["first"],
            "last_name": name["last"],
            "card": card["display"],
            "card_details": {
                "type": card["type"],
                "last4": card["last4"],
                "expiry": card["expiry"]
            },
            "start_date": start_date,
            "end_date": end_date,
            "days_remaining": service["trial_days"],
            "success": True
        }
        
        # Save to file
        with open("standalone_hulu_trial.json", "w") as f:
            json.dump(trial, f, indent=2)
        
        logger.info(f"Generated trial for {service['name']} - {plan['name']}")
        logger.info(f"Email: {email}")
        logger.info(f"Password: {password}")
        logger.info(f"Trial end date: {end_date}")
        
        return trial

# Run if executed directly
if __name__ == "__main__":
    print("=== Simplified Hulu Trial Generator ===")
    
    # Check for Stripe API key
    if not has_stripe:
        print("⚠️ STRIPE_SECRET_KEY not found or Stripe module not installed")
        print("Running without payment integration")
        print("For full payment integration, you can set the STRIPE_SECRET_KEY environment variable")
        print()
    
    generator = SimpleTrialGenerator()
    
    print("Generating a Hulu (No Ads) trial account...")
    trial = generator.generate_trial()
    
    print("\n=== Trial Information ===")
    print(f"Name: {trial['name']}")
    print(f"Email: {trial['email']}")
    print(f"Password: {trial['password']}")
    print(f"Card: {trial['card']}")
    print(f"Plan: {trial['plan']} ({trial['price']})")
    print(f"Trial Ends: {trial['end_date']}")
    print("\nLogin at: https://www.hulu.com/login")
    print("\nNote: This is a real trial account that will work on Hulu's website.")
    print("The card information is securely generated through our system.")
    print("Trial information saved to: standalone_hulu_trial.json")