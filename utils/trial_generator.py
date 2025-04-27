"""
Trial Generator Utility
Handles generation of trial accounts and credentials
"""
import os
import random
import string
import logging
import asyncio
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrialGenerator:
    """
    Generates trial accounts for various streaming services
    Centralizes credential generation logic from other scripts
    """
    def __init__(self):
        """Initialize the trial generator"""
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
    
    async def generate_trial(self, service_name):
        """
        Generate a complete trial for a specific service
        
        Args:
            service_name (str): The streaming service name (e.g., netflix, hulu)
            
        Returns:
            dict: Complete trial information
        """
        service_name = service_name.lower()
        
        # Generate user identity
        identity = await self.generate_identity()
        
        # Generate card information
        card = await self.generate_card()
        
        # Generate additional service-specific information
        service_info = await self.generate_service_specific_info(service_name)
        
        # Calculate trial end date
        trial_days = self.trial_durations.get(service_name, 30)
        trial_end_date = (datetime.now() + timedelta(days=trial_days)).isoformat()
        
        # Combine all information into a complete trial
        return {
            'service': service_name,
            'user_info': {
                **identity,
                'email': identity['email'],
                'password': service_info.get('password', self.generate_password())
            },
            'payment_info': card,
            'service_details': service_info,
            'trial_end_date': trial_end_date,
            'generated_at': datetime.now().isoformat()
        }
    
    async def generate_identity(self):
        """
        Generate a random identity with name, address, etc.
        
        Returns:
            dict: Personal identity information
        """
        # First name based on random gender
        gender = random.choice(['male', 'female'])
        first_name = self.generate_random_name(gender)
        
        # Last name 
        last_name = self.generate_random_surname()
        
        # Email based on name
        email = self.generate_random_email(first_name, last_name)
        
        # Address details
        street = self.generate_random_street()
        city = self.generate_random_city()
        state = self.generate_random_state()
        zipcode = self.generate_random_zipcode()
        
        # Phone number
        phone = self.generate_random_phone()
        
        return {
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'email': email,
            'street': street,
            'city': city,
            'state': state,
            'zipcode': zipcode,
            'phone': phone
        }
    
    async def generate_card(self, card_type='visa'):
        """
        Generate credit card information
        
        Args:
            card_type (str): The type of card to generate (visa, mastercard, etc.)
            
        Returns:
            dict: Credit card information
        """
        # Card number with Luhn check
        card_number = self.generate_card_number(card_type)
        
        # Expiry date
        expiry = self.generate_card_expiry()
        
        # CVV
        cvv = self.generate_cvv(card_type)
        
        # Get identity details for the card holder
        identity = await self.generate_identity()
        
        return {
            'card_type': card_type,
            'card_number': card_number,
            'expiry': expiry,
            'cvv': cvv,
            'holder_name': f"{identity['first_name']} {identity['last_name']}",
            'billing_address': {
                'street': identity['street'],
                'city': identity['city'],
                'state': identity['state'],
                'zipcode': identity['zipcode']
            }
        }
    
    async def generate_service_specific_info(self, service_name):
        """
        Generate service-specific information
        
        Args:
            service_name (str): The streaming service name
            
        Returns:
            dict: Service-specific details
        """
        # Default service info
        service_info = {
            'password': self.generate_password(),
            'username': None,
            'plan': None
        }
        
        # Service-specific customizations
        if service_name == 'netflix':
            service_info['plan'] = random.choice(['Basic', 'Standard', 'Premium'])
            
        elif service_name == 'hulu':
            service_info['plan'] = random.choice(['Hulu', 'Hulu (No Ads)', 'Hulu + Live TV'])
            
        elif service_name == 'disney':
            service_info['plan'] = 'Disney+ Basic'
            
        elif service_name == 'spotify':
            service_info['plan'] = 'Individual Premium'
            service_info['username'] = f"user{random.randint(100000, 999999)}"
            
        elif service_name == 'youtube':
            service_info['plan'] = 'YouTube Premium'
        
        return service_info
    
    # Helper methods for generating identity and card details
    
    def generate_random_name(self, gender=None):
        """Generate a random first name based on gender"""
        male_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles']
        female_names = ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen']
        
        if gender == 'male':
            return random.choice(male_names)
        elif gender == 'female':
            return random.choice(female_names)
        else:
            return random.choice(male_names + female_names)
    
    def generate_random_surname(self):
        """Generate a random surname"""
        surnames = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 
                    'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson']
        return random.choice(surnames)
    
    def generate_random_street(self):
        """Generate a random street address"""
        street_number = random.randint(100, 9999)
        street_names = ['Main St', 'Park Ave', 'Oak St', 'Maple Ave', 'Cedar Ln', 'Washington St', 'High St', 'Court St', 
                        'Lake Rd', 'River Rd', 'Church St', 'Mill Rd', 'Elm St', 'View Rd', 'Lincoln Ave']
        return f"{street_number} {random.choice(street_names)}"
    
    def generate_random_city(self):
        """Generate a random US city"""
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 
                  'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte']
        return random.choice(cities)
    
    def generate_random_state(self):
        """Generate a random US state code"""
        states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 
                  'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 
                  'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
        return random.choice(states)
    
    def generate_random_zipcode(self):
        """Generate a random 5-digit zipcode"""
        return f"{random.randint(10000, 99999)}"
    
    def generate_random_email(self, first_name, last_name):
        """Generate a random email based on name"""
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com', 'mail.com', 'protonmail.com']
        separators = ['', '.', '_']
        
        # Create username with optional number suffix
        separator = random.choice(separators)
        username = f"{first_name.lower()}{separator}{last_name.lower()}"
        
        # 50% chance to add a number
        if random.random() > 0.5:
            username += str(random.randint(1, 999))
            
        domain = random.choice(domains)
        return f"{username}@{domain}"
    
    def generate_random_phone(self):
        """Generate a random US phone number"""
        area_code = random.randint(201, 999)
        prefix = random.randint(200, 999)
        line = random.randint(1000, 9999)
        return f"{area_code}-{prefix}-{line}"
    
    def generate_password(self, length=12):
        """Generate a random password"""
        characters = string.ascii_letters + string.digits + string.punctuation
        # Ensure at least one of each character type
        pwd = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice('!@#$%^&*()_+-=')
        ]
        # Fill rest with random characters
        pwd.extend(random.choice(characters) for _ in range(length - 4))
        # Shuffle to randomize positions
        random.shuffle(pwd)
        return ''.join(pwd)
    
    def generate_card_number(self, card_type='visa'):
        """Generate a valid credit card number based on card type"""
        prefixes = {
            'visa': ['4'],
            'mastercard': ['51', '52', '53', '54', '55'],
            'amex': ['34', '37'],
            'discover': ['6011', '644', '645', '646', '647', '648', '649', '65']
        }
        
        lengths = {
            'visa': 16,
            'mastercard': 16,
            'amex': 15,
            'discover': 16
        }
        
        # Get prefix and length for the card type
        prefix = random.choice(prefixes.get(card_type.lower(), ['4']))
        length = lengths.get(card_type.lower(), 16)
        
        # Generate card number without checksum
        card_number = prefix
        card_number += ''.join(random.choice('0123456789') for _ in range(length - len(prefix) - 1))
        
        # Calculate Luhn checksum
        digits = [int(d) for d in card_number]
        for i in range(len(digits) - 1, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
                
        checksum = (10 - sum(digits) % 10) % 10
        
        # Add checksum digit
        card_number += str(checksum)
        
        return card_number
    
    def generate_card_expiry(self):
        """Generate a future expiry date (MM/YY)"""
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Generate a date 1-5 years in the future
        year_offset = random.randint(1, 5)
        future_year = current_year + year_offset
        
        # If it's the same year, ensure month is in the future
        if year_offset == 0:
            future_month = random.randint(current_month + 1, 12)
        else:
            future_month = random.randint(1, 12)
            
        return f"{future_month:02d}/{str(future_year)[-2:]}"
    
    def generate_cvv(self, card_type='visa'):
        """Generate a CVV based on card type"""
        # AMEX uses 4-digit CVV, others use 3-digit
        if card_type.lower() == 'amex':
            return f"{random.randint(1000, 9999)}"
        else:
            return f"{random.randint(100, 999)}"