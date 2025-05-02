#!/usr/bin/env python3
"""
Credit Card Generator Utility
Generates valid credit card numbers following card issuer specifications
and satisfying the Luhn algorithm check
"""
import random
from datetime import datetime, timedelta

class CreditCardGenerator:
    """
    Generates realistic and valid credit card numbers that pass the Luhn check
    """
    
    # Card issuer specifications
    CARD_TYPES = {
        "visa": {
            "prefixes": ["4"],
            "lengths": [16],
            "cvv_length": 3
        },
        "mastercard": {
            "prefixes": ["51", "52", "53", "54", "55"],
            "lengths": [16],
            "cvv_length": 3
        },
        "amex": {
            "prefixes": ["34", "37"],
            "lengths": [15],
            "cvv_length": 4
        },
        "discover": {
            "prefixes": ["6011", "644", "645", "646", "647", "648", "649", "65"],
            "lengths": [16],
            "cvv_length": 3
        }
    }
    
    @staticmethod
    def generate_card(card_type="visa"):
        """
        Generate a valid credit card with all necessary details
        
        Args:
            card_type (str): Type of card to generate (visa, mastercard, amex, discover)
            
        Returns:
            dict: Complete card details
        """
        card_type = card_type.lower()
        if card_type not in CreditCardGenerator.CARD_TYPES:
            card_type = "visa"  # Default to Visa if card type not recognized
        
        # Get card specifications
        specs = CreditCardGenerator.CARD_TYPES[card_type]
        
        # Generate card number
        prefix = random.choice(specs["prefixes"])
        length = random.choice(specs["lengths"])
        card_number = CreditCardGenerator.generate_card_number(prefix, length)
        
        # Generate CVV
        cvv = ''.join(random.choices("0123456789", k=specs["cvv_length"]))
        
        # Generate expiration date (1-5 years in the future)
        expiry_date = CreditCardGenerator.generate_expiry_date()
        
        # Generate cardholder name
        cardholder_name = CreditCardGenerator.generate_cardholder_name()
        
        return {
            "card_number": card_number,
            "card_type": card_type,
            "cvv": cvv,
            "expiry_month": expiry_date["month"],
            "expiry_year": expiry_date["year"],
            "expiry": f"{expiry_date['month']}/{expiry_date['year']}",
            "cardholder_name": cardholder_name
        }
    
    @staticmethod
    def generate_card_number(prefix, length):
        """
        Generate a valid card number that passes the Luhn check
        
        Args:
            prefix (str): Card number prefix (BIN)
            length (int): Total length of the card number
            
        Returns:
            str: Valid card number
        """
        # Start with the prefix
        card_number = prefix
        
        # Generate random digits for the remaining length minus the check digit
        remaining_length = length - len(prefix) - 1
        for _ in range(remaining_length):
            card_number += str(random.randint(0, 9))
        
        # Calculate and append the Luhn check digit
        check_digit = CreditCardGenerator.calculate_luhn_check_digit(card_number)
        card_number += str(check_digit)
        
        return card_number
    
    @staticmethod
    def calculate_luhn_check_digit(partial_card_number):
        """
        Calculate the Luhn algorithm check digit
        
        Args:
            partial_card_number (str): Card number without the check digit
            
        Returns:
            int: Check digit (0-9)
        """
        # Convert to list of integers
        digits = [int(d) for d in partial_card_number]
        
        # Double every second digit from right to left
        for i in range(len(digits) - 1, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        
        # Calculate sum
        total = sum(digits)
        
        # The check digit is the value needed to make the sum a multiple of 10
        return (10 - (total % 10)) % 10
    
    @staticmethod
    def generate_expiry_date():
        """
        Generate a realistic expiration date
        
        Returns:
            dict: Month and year of expiration
        """
        now = datetime.now()
        years_forward = random.randint(1, 5)
        future_date = now + timedelta(days=365 * years_forward)
        
        return {
            "month": str(random.randint(1, 12)).zfill(2),
            "year": str(future_date.year)[-2:]  # Last 2 digits of the year
        }
    
    @staticmethod
    def generate_cardholder_name():
        """
        Generate a realistic cardholder name
        
        Returns:
            str: Cardholder name
        """
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", 
                     "Robert", "Emily", "Daniel", "Jessica", "Matthew", "Ashley", 
                     "Christopher", "Amanda", "Andrew", "Jennifer", "Joshua", "Megan"]
        
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", 
                     "Davis", "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson", 
                     "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson"]
        
        return f"{random.choice(first_names)} {random.choice(last_names)}"

# Test function
def test_card_generator():
    """Test the credit card generator with all card types"""
    card_types = ["visa", "mastercard", "amex", "discover"]
    
    for card_type in card_types:
        card = CreditCardGenerator.generate_card(card_type)
        print(f"Generated {card_type.upper()} card:")
        print(f"Card number: {card['card_number']}")
        print(f"CVV: {card['cvv']}")
        print(f"Expiry: {card['expiry']}")
        print(f"Cardholder: {card['cardholder_name']}")
        print("-" * 50)

if __name__ == "__main__":
    test_card_generator()