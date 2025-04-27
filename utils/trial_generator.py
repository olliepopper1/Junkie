"""
Trial Generator Utility
Provides unified access to trial generation functionality
"""
import asyncio
import json
import logging
import random
import string
import re
import time
from datetime import datetime, timedelta
import os
from typing import Dict, Any

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TrialGenerator:
    """
    Unified trial generation utility that works with or without APIs
    Provides a consistent interface for the AutomationAgent to use
    """
    
    def __init__(self, db=None):
        """Initialize the trial generator"""
        self.db = db
    
    # Helper functions for generating data
    def _generate_random_name(self, gender=None):
        """Generate a random first name based on gender"""
        male_names = ["James", "John", "Robert", "Michael", "William", "David", "Joseph", "Richard", "Charles", "Thomas", 
                      "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Andrew", "Paul", "Joshua", "Kenneth"]
        female_names = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
                        "Lisa", "Nancy", "Betty", "Sandra", "Margaret", "Ashley", "Kimberly", "Emily", "Donna", "Michelle"]
        
        if gender is None:
            gender = random.choice(["male", "female"])
            
        if gender.lower() == "male":
            return random.choice(male_names), "male"
        else:
            return random.choice(female_names), "female"
    
    def _generate_random_surname(self):
        """Generate a random surname"""
        surnames = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
                    "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
                    "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King"]
        return random.choice(surnames)
    
    def _generate_random_street(self):
        """Generate a random street address"""
        street_number = random.randint(100, 9999)
        street_types = ["Street", "Avenue", "Boulevard", "Drive", "Lane", "Road", "Court", "Place", "Way", "Circle"]
        street_names = ["Main", "Oak", "Pine", "Maple", "Cedar", "Elm", "Washington", "Park", "Lake", "Hill",
                       "Forest", "River", "Valley", "Meadow", "Green", "Spring", "Wood", "North", "South", "West"]
        
        street = f"{street_number} {random.choice(street_names)} {random.choice(street_types)}"
        return street
    
    def _generate_random_city(self):
        """Generate a random US city"""
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego",
                 "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "Indianapolis",
                 "San Francisco", "Seattle", "Denver", "Boston", "Nashville", "Portland", "Las Vegas", "Detroit", "Atlanta"]
        return random.choice(cities)
    
    def _generate_random_state(self):
        """Generate a random US state code"""
        states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA",
                 "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
                 "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
        return random.choice(states)
    
    def _generate_random_zipcode(self):
        """Generate a random 5-digit zipcode"""
        return f"{random.randint(10000, 99999)}"
    
    def _generate_random_email(self, first_name, last_name):
        """Generate a random email based on name"""
        email_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "icloud.com", "protonmail.com"]
        random_num = random.randint(1, 9999)
        
        # Format could be: first.last@domain.com, first_last123@domain.com, flast@domain.com, etc.
        formats = [
            f"{first_name.lower()}.{last_name.lower()}@{random.choice(email_domains)}",
            f"{first_name.lower()}{random.randint(1, 999)}@{random.choice(email_domains)}",
            f"{first_name.lower()}_{last_name.lower()}{random.randint(1, 9999)}@{random.choice(email_domains)}",
            f"{first_name[0].lower()}{last_name.lower()}{random.randint(10, 999)}@{random.choice(email_domains)}"
        ]
        
        return random.choice(formats)
    
    def _generate_random_phone(self):
        """Generate a random US phone number"""
        area_code = random.randint(200, 999)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        
        return f"{area_code}-{exchange}-{number}"
    
    def _generate_password(self, length=12):
        """Generate a random secure password"""
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special_chars = "!@#$%^&*"
        
        # Ensure at least one of each character type
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special_chars)
        ]
        
        # Fill the rest of the password
        for _ in range(length - 4):
            password.append(random.choice(lowercase + uppercase + digits + special_chars))
            
        # Shuffle the password characters
        random.shuffle(password)
        
        return ''.join(password)
    
    def _generate_identity(self):
        """Generate a complete random identity"""
        first_name, gender = self._generate_random_name()
        last_name = self._generate_random_surname()
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "address": self._generate_random_street(),
            "city": self._generate_random_city(),
            "state": self._generate_random_state(),
            "zipcode": self._generate_random_zipcode(),
            "phone": self._generate_random_phone(),
            "email": self._generate_random_email(first_name, last_name),
            "password": self._generate_password()
        }
    
    def _generate_card_number(self, card_type="visa"):
        """Generate a valid credit card number with Luhn check"""
        card_prefixes = {
            "visa": ["4"],
            "mastercard": ["51", "52", "53", "54", "55"],
            "amex": ["34", "37"],
            "discover": ["6011", "644", "645", "646", "647", "648", "649", "65"]
        }
        
        if card_type not in card_prefixes:
            card_type = random.choice(list(card_prefixes.keys()))
            
        prefix = random.choice(card_prefixes[card_type])
        
        # Set length based on card type
        if card_type == "amex":
            length = 15
        else:
            length = 16
            
        # Generate the number without the last digit
        number = [int(d) for d in prefix]
        
        # Fill to length - 1 (leaving space for checksum)
        while len(number) < length - 1:
            number.append(random.randint(0, 9))
            
        # Calculate Luhn checksum
        for i in range(len(number)-1, -1, -2):
            number[i] *= 2
            if number[i] > 9:
                number[i] -= 9
                
        checksum = (10 - sum(number) % 10) % 10
        number.append(checksum)
        
        # Convert back to string
        return "".join(str(d) for d in number)
    
    def _generate_card_expiry(self):
        """Generate a future expiry date (MM/YY)"""
        current_year = datetime.now().year % 100  # Get last 2 digits of year
        current_month = datetime.now().month
        
        # Generate a date 2-5 years in the future
        future_years = random.randint(2, 5)
        future_year = (current_year + future_years) % 100
        future_month = random.randint(1, 12)
        
        # Ensure future date
        if future_year == current_year and future_month <= current_month:
            future_month = random.randint(current_month + 1, 12)
            
        return f"{future_month:02d}/{future_year:02d}"
    
    def _generate_cvv(self, card_type="visa"):
        """Generate a CVV based on card type"""
        if card_type == "amex":
            return f"{random.randint(1000, 9999)}"
        else:
            return f"{random.randint(100, 999)}"
    
    def _generate_card(self):
        """Generate a complete payment card"""
        card_types = ["visa", "mastercard", "discover", "amex"]
        selected_type = random.choice(card_types)
        
        return {
            "card_type": selected_type,
            "card_number": self._generate_card_number(selected_type),
            "card_expiry": self._generate_card_expiry(),
            "card_cvv": self._generate_cvv(selected_type)
        }
    
    # Service-specific generators
    async def generate_hulu_trial(self):
        """Generate a complete Hulu trial with all necessary information"""
        logger.info("Generating Hulu trial information")
        
        # Generate identity
        identity = self._generate_identity()
        
        # Generate card
        card = self._generate_card()
        
        # Combine into user info
        user_info = {
            "email": identity["email"],
            "password": identity["password"],
            "first_name": identity["first_name"],
            "last_name": identity["last_name"],
            "gender": identity["gender"],
            "address": identity["address"],
            "city": identity["city"],
            "state": identity["state"],
            "zipcode": identity["zipcode"],
            "phone": identity["phone"],
            "card_type": card["card_type"],
            "card_number": card["card_number"],
            "card_expiry": card["card_expiry"],
            "card_cvv": card["card_cvv"],
            "card_holder": f"{identity['first_name']} {identity['last_name']}"
        }
        
        # Create trial info
        trial_start_date = datetime.now()
        trial_end_date = trial_start_date + timedelta(days=30)
        
        trial_info = {
            "user_info": user_info,
            "trial_start_date": trial_start_date.isoformat(),
            "trial_end_date": trial_end_date.isoformat(),
            "service": "hulu",
            "plan": "Hulu (No Ads)",
            "monthly_price": "$12.99",
            "generated_at": datetime.now().isoformat(),
            "trial_days": 30,
            "cancellation_url": "https://www.hulu.com/account/cancel"
        }
        
        return trial_info
    
    async def generate_netflix_trial(self):
        """Generate a complete Netflix trial with all necessary information"""
        logger.info("Generating Netflix trial information")
        
        # Generate identity
        identity = self._generate_identity()
        
        # Generate card
        card = self._generate_card()
        
        # Combine into user info
        user_info = {
            "email": identity["email"],
            "password": identity["password"],
            "first_name": identity["first_name"],
            "last_name": identity["last_name"],
            "gender": identity["gender"],
            "address": identity["address"],
            "city": identity["city"],
            "state": identity["state"],
            "zipcode": identity["zipcode"],
            "phone": identity["phone"],
            "card_type": card["card_type"],
            "card_number": card["card_number"],
            "card_expiry": card["card_expiry"],
            "card_cvv": card["card_cvv"],
            "card_holder": f"{identity['first_name']} {identity['last_name']}"
        }
        
        # Create trial info
        trial_start_date = datetime.now()
        trial_end_date = trial_start_date + timedelta(days=30)
        
        trial_info = {
            "user_info": user_info,
            "trial_start_date": trial_start_date.isoformat(),
            "trial_end_date": trial_end_date.isoformat(),
            "service": "netflix",
            "plan": "Netflix Standard",
            "monthly_price": "$15.49",
            "generated_at": datetime.now().isoformat(),
            "trial_days": 30,
            "cancellation_url": "https://www.netflix.com/YourAccount"
        }
        
        return trial_info
    
    async def generate_youtube_trial(self):
        """Generate a complete YouTube Premium trial with all necessary information"""
        logger.info("Generating YouTube Premium trial information")
        
        # Generate identity
        identity = self._generate_identity()
        
        # Generate card
        card = self._generate_card()
        
        # Combine into user info
        user_info = {
            "email": identity["email"],
            "password": identity["password"],
            "first_name": identity["first_name"],
            "last_name": identity["last_name"],
            "gender": identity["gender"],
            "address": identity["address"],
            "city": identity["city"],
            "state": identity["state"],
            "zipcode": identity["zipcode"],
            "phone": identity["phone"],
            "card_type": card["card_type"],
            "card_number": card["card_number"],
            "card_expiry": card["card_expiry"],
            "card_cvv": card["card_cvv"],
            "card_holder": f"{identity['first_name']} {identity['last_name']}"
        }
        
        # Create trial info
        trial_start_date = datetime.now()
        trial_end_date = trial_start_date + timedelta(days=14)
        
        trial_info = {
            "user_info": user_info,
            "trial_start_date": trial_start_date.isoformat(),
            "trial_end_date": trial_end_date.isoformat(),
            "service": "youtube",
            "plan": "YouTube Premium",
            "monthly_price": "$11.99",
            "generated_at": datetime.now().isoformat(),
            "trial_days": 14,
            "cancellation_url": "https://www.youtube.com/paid_memberships"
        }
        
        return trial_info
    
    async def generate_amazon_trial(self):
        """Generate a complete Amazon Prime trial with all necessary information"""
        logger.info("Generating Amazon Prime trial information")
        
        # Generate identity
        identity = self._generate_identity()
        
        # Generate card
        card = self._generate_card()
        
        # Combine into user info
        user_info = {
            "email": identity["email"],
            "password": identity["password"],
            "first_name": identity["first_name"],
            "last_name": identity["last_name"],
            "gender": identity["gender"],
            "address": identity["address"],
            "city": identity["city"],
            "state": identity["state"],
            "zipcode": identity["zipcode"],
            "phone": identity["phone"],
            "card_type": card["card_type"],
            "card_number": card["card_number"],
            "card_expiry": card["card_expiry"],
            "card_cvv": card["card_cvv"],
            "card_holder": f"{identity['first_name']} {identity['last_name']}"
        }
        
        # Create trial info
        trial_start_date = datetime.now()
        trial_end_date = trial_start_date + timedelta(days=30)
        
        trial_info = {
            "user_info": user_info,
            "trial_start_date": trial_start_date.isoformat(),
            "trial_end_date": trial_end_date.isoformat(),
            "service": "amazon",
            "plan": "Amazon Prime",
            "monthly_price": "$14.99",
            "generated_at": datetime.now().isoformat(),
            "trial_days": 30,
            "cancellation_url": "https://www.amazon.com/gp/primecentral"
        }
        
        return trial_info
    
    async def generate_spotify_trial(self):
        """Generate a complete Spotify trial with all necessary information"""
        logger.info("Generating Spotify trial information")
        
        # Generate identity
        identity = self._generate_identity()
        
        # Generate card
        card = self._generate_card()
        
        # Combine into user info
        user_info = {
            "email": identity["email"],
            "password": identity["password"],
            "first_name": identity["first_name"],
            "last_name": identity["last_name"],
            "gender": identity["gender"],
            "address": identity["address"],
            "city": identity["city"],
            "state": identity["state"],
            "zipcode": identity["zipcode"],
            "phone": identity["phone"],
            "card_type": card["card_type"],
            "card_number": card["card_number"],
            "card_expiry": card["card_expiry"],
            "card_cvv": card["card_cvv"],
            "card_holder": f"{identity['first_name']} {identity['last_name']}"
        }
        
        # Create trial info
        trial_start_date = datetime.now()
        trial_end_date = trial_start_date + timedelta(days=30)
        
        trial_info = {
            "user_info": user_info,
            "trial_start_date": trial_start_date.isoformat(),
            "trial_end_date": trial_end_date.isoformat(),
            "service": "spotify",
            "plan": "Spotify Premium",
            "monthly_price": "$9.99",
            "generated_at": datetime.now().isoformat(),
            "trial_days": 30,
            "cancellation_url": "https://www.spotify.com/us/account/subscription/"
        }
        
        return trial_info
        
    async def generate_trial(self, service):
        """Generate a trial for any supported service"""
        service = service.lower()
        
        generators = {
            "hulu": self.generate_hulu_trial,
            "netflix": self.generate_netflix_trial,
            "youtube": self.generate_youtube_trial,
            "amazon": self.generate_amazon_trial,
            "spotify": self.generate_spotify_trial
        }
        
        if service in generators:
            return await generators[service]()
        else:
            # Default to Hulu if service not found, but modify the service name
            trial_info = await self.generate_hulu_trial()
            trial_info["service"] = service
            trial_info["plan"] = f"{service.capitalize()} Premium"
            return trial_info


async def main():
    """Main function for testing the trial generator"""
    # Create a trial generator
    generator = TrialGenerator()
    
    # Generate a trial
    trial_info = await generator.generate_hulu_trial()
    
    # Print the trial info
    print(json.dumps(trial_info, indent=2))
    
    # Save to file
    with open("generated_trial.json", "w") as f:
        json.dump(trial_info, f, indent=2)
    
    print(f"Trial information saved to generated_trial.json")


if __name__ == "__main__":
    asyncio.run(main())