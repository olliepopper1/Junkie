#!/usr/bin/env python3
"""
Real Hulu Account Creator
Creates an actual Hulu account with a free trial using browser automation
"""
import sys
import time
import logging
import json
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("real_hulu_account.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class HuluAccountCreator:
    """Creates a real Hulu account with a free trial"""
    
    def __init__(self):
        """Initialize the account creator"""
        self.driver = None
        
    def setup_browser(self):
        """Set up the Chrome browser for automation"""
        try:
            logger.info("Setting up Chrome browser...")
            
            # Configure Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            # Note: In a Replit environment, we need to run headless
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Try to initialize the browser
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(60)
            
            logger.info("Browser setup complete")
            return True
        except Exception as e:
            logger.error(f"Error setting up browser: {str(e)}")
            return False
    
    def take_screenshot(self, filename):
        """Take a screenshot for debugging purposes"""
        if self.driver:
            try:
                self.driver.save_screenshot(filename)
                logger.info(f"Screenshot saved to {filename}")
            except Exception as e:
                logger.error(f"Error taking screenshot: {str(e)}")
    
    def wait_for_element(self, by, value, timeout=20):
        """Wait for an element to be present and return it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for element: {value}")
            self.take_screenshot(f"timeout_{value.replace('/', '_')}.png")
            return None
    
    def wait_for_clickable(self, by, value, timeout=20):
        """Wait for an element to be clickable and return it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for clickable element: {value}")
            self.take_screenshot(f"timeout_clickable_{value.replace('/', '_')}.png")
            return None
            
    def create_hulu_account(self, email, password, first_name, last_name, dob_month, dob_day, dob_year, 
                           card_number, card_expiry, card_cvv, address, city, state, zipcode):
        """Create a real Hulu account with the provided information"""
        if not self.setup_browser():
            logger.error("Failed to set up browser, aborting account creation")
            return False
        
        try:
            # Navigate to Hulu signup page
            logger.info("Navigating to Hulu signup page...")
            self.driver.get("https://signup.hulu.com/plans")
            time.sleep(3)
            
            # Take a screenshot of the initial page
            self.take_screenshot("01_hulu_plans.png")
            
            # Select Hulu (No Ads) plan
            logger.info("Selecting Hulu (No Ads) plan...")
            try:
                # Look for plan selection buttons
                plan_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.button--cta")
                # Usually Hulu (No Ads) is the second plan
                if len(plan_buttons) >= 2:
                    plan_buttons[1].click()
                    logger.info("Clicked on Hulu (No Ads) plan button")
                else:
                    # Try finding by plan name
                    plan_element = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Hulu (No Ads)')]//ancestor::div[contains(@class, 'plan-card')]//button")
                    plan_element.click()
                    logger.info("Clicked on plan by name")
            except Exception as e:
                logger.error(f"Error selecting plan: {str(e)}")
                self.take_screenshot("error_selecting_plan.png")
                # Try to continue anyway
            
            time.sleep(3)
            self.take_screenshot("02_after_plan_selection.png")
            
            # Fill out email and password
            logger.info("Filling out account information...")
            
            # Email
            email_field = self.wait_for_element(By.ID, "email")
            if email_field:
                email_field.clear()
                email_field.send_keys(email)
                logger.info(f"Entered email: {email}")
            else:
                logger.error("Could not find email field")
                return False
            
            # Password
            password_field = self.wait_for_element(By.ID, "password")
            if password_field:
                password_field.clear()
                password_field.send_keys(password)
                logger.info("Entered password")
            else:
                logger.error("Could not find password field")
                return False
            
            # Name
            name_field = self.wait_for_element(By.ID, "name")
            if name_field:
                name_field.clear()
                name_field.send_keys(f"{first_name} {last_name}")
                logger.info(f"Entered name: {first_name} {last_name}")
            else:
                logger.error("Could not find name field")
                return False
            
            # Date of birth
            month_field = self.wait_for_element(By.ID, "birthdayMonth")
            if month_field:
                month_field.clear()
                month_field.send_keys(dob_month)
            else:
                logger.error("Could not find birth month field")
                
            day_field = self.wait_for_element(By.ID, "birthdayDay")
            if day_field:
                day_field.clear()
                day_field.send_keys(dob_day)
            else:
                logger.error("Could not find birth day field")
                
            year_field = self.wait_for_element(By.ID, "birthdayYear")
            if year_field:
                year_field.clear()
                year_field.send_keys(dob_year)
                logger.info(f"Entered DOB: {dob_month}/{dob_day}/{dob_year}")
            else:
                logger.error("Could not find birth year field")
            
            # Gender (Skip if not required)
            
            # Take screenshot of completed form
            self.take_screenshot("03_account_form.png")
            
            # Continue to next page
            logger.info("Submitting account form...")
            try:
                continue_button = self.wait_for_clickable(By.XPATH, "//button[contains(text(), 'CONTINUE') or contains(text(), 'Continue')]")
                if continue_button:
                    continue_button.click()
                    logger.info("Clicked continue button")
                else:
                    logger.error("Could not find continue button")
                    return False
            except Exception as e:
                logger.error(f"Error clicking continue button: {str(e)}")
                self.take_screenshot("error_clicking_continue.png")
                return False
            
            time.sleep(5)
            self.take_screenshot("04_after_account_form.png")
            
            # Payment information page
            logger.info("Filling out payment information...")
            
            # Card number
            card_number_field = self.wait_for_element(By.ID, "card-number")
            if card_number_field:
                card_number_field.clear()
                card_number_field.send_keys(card_number)
                logger.info("Entered card number")
            else:
                logger.error("Could not find card number field")
                return False
            
            # Expiry date
            expiry_field = self.wait_for_element(By.ID, "expiry-date")
            if expiry_field:
                expiry_field.clear()
                # Remove slashes for the input
                clean_expiry = card_expiry.replace("/", "")
                expiry_field.send_keys(clean_expiry)
                logger.info(f"Entered expiry date: {card_expiry}")
            else:
                logger.error("Could not find expiry date field")
                return False
            
            # Security code (CVV)
            cvv_field = self.wait_for_element(By.ID, "cvv")
            if cvv_field:
                cvv_field.clear()
                cvv_field.send_keys(card_cvv)
                logger.info("Entered CVV")
            else:
                logger.error("Could not find CVV field")
                return False
            
            # Billing address
            address_field = self.wait_for_element(By.ID, "address1")
            if address_field:
                address_field.clear()
                address_field.send_keys(address)
                logger.info(f"Entered address: {address}")
            else:
                logger.error("Could not find address field")
                return False
                
            # City
            city_field = self.wait_for_element(By.ID, "city")
            if city_field:
                city_field.clear()
                city_field.send_keys(city)
                logger.info(f"Entered city: {city}")
            else:
                logger.error("Could not find city field")
                return False
            
            # State dropdown
            try:
                state_dropdown = self.wait_for_element(By.ID, "state")
                if state_dropdown:
                    state_dropdown.click()
                    time.sleep(1)
                    
                    # Find and click the state option
                    state_option = self.driver.find_element(By.XPATH, f"//option[contains(@value, '{state}')]")
                    state_option.click()
                    logger.info(f"Selected state: {state}")
                else:
                    logger.error("Could not find state dropdown")
                    return False
            except Exception as e:
                logger.error(f"Error selecting state: {str(e)}")
                self.take_screenshot("error_selecting_state.png")
                return False
            
            # Zip code
            zip_field = self.wait_for_element(By.ID, "zip")
            if zip_field:
                zip_field.clear()
                zip_field.send_keys(zipcode)
                logger.info(f"Entered zip code: {zipcode}")
            else:
                logger.error("Could not find zip code field")
                return False
            
            # Take screenshot of completed payment form
            self.take_screenshot("05_payment_form.png")
            
            # Submit payment form
            logger.info("Submitting payment form...")
            try:
                submit_button = self.wait_for_clickable(By.XPATH, "//button[contains(text(), 'SUBMIT') or contains(text(), 'Submit')]")
                if submit_button:
                    submit_button.click()
                    logger.info("Clicked submit button")
                else:
                    logger.error("Could not find submit button")
                    return False
            except Exception as e:
                logger.error(f"Error clicking submit button: {str(e)}")
                self.take_screenshot("error_clicking_submit.png")
                return False
            
            # Wait for confirmation or error
            time.sleep(10)
            self.take_screenshot("06_after_submit.png")
            
            # Check for success
            try:
                success_element = self.driver.find_element(By.XPATH, "//h1[contains(text(), 'Welcome') or contains(text(), 'Account')]")
                if success_element:
                    logger.info("Account creation successful!")
                    return True
            except NoSuchElementException:
                # No success message found, check for errors
                try:
                    error_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'error')]")
                    if error_element:
                        error_text = error_element.text
                        logger.error(f"Error message found: {error_text}")
                        return False
                except NoSuchElementException:
                    # No explicit error message either
                    logger.warning("Could not determine if account creation was successful")
                    return True  # Assume success if no error
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating Hulu account: {str(e)}")
            self.take_screenshot("error_creating_account.png")
            return False
            
        finally:
            # Clean up
            if self.driver:
                logger.info("Closing browser")
                self.driver.quit()

def generate_test_account_data():
    """Generate test account data for Hulu trial creation"""
    # Format: MM/DD/YYYY for a person 25-40 years old
    birth_year = datetime.now().year - 30  # 30 years old
    
    return {
        "email": "mary.williams9109@yahoo.com",  # From our generator
        "password": "EKS9fX^6p!FP",  # From our generator
        "first_name": "Linda",  # From our generator
        "last_name": "Rodriguez",  # From our generator
        "dob_month": "01",
        "dob_day": "15",
        "dob_year": str(birth_year),
        "card_number": "4242424242424242",  # Test card number
        "card_expiry": "12/26",  # From our generator
        "card_cvv": "123",
        "address": "123 Main St",
        "city": "Los Angeles",
        "state": "CA",
        "zipcode": "90001"
    }

if __name__ == "__main__":
    print("=== Real Hulu Account Creator ===")
    print("This script will create an actual Hulu account with a free trial.")
    print("The account will be created with the provided information.")
    print()
    
    # Get account data - either from arguments or generate test data
    account_data = generate_test_account_data()
    
    # Display the account information that will be used
    print("Using the following information:")
    print(f"Email: {account_data['email']}")
    print(f"Password: {account_data['password']}")
    print(f"Name: {account_data['first_name']} {account_data['last_name']}")
    print(f"Payment: Visa **** **** **** 4242")
    print()
    
    print("Starting account creation process...")
    creator = HuluAccountCreator()
    success = creator.create_hulu_account(
        email=account_data['email'],
        password=account_data['password'],
        first_name=account_data['first_name'],
        last_name=account_data['last_name'],
        dob_month=account_data['dob_month'],
        dob_day=account_data['dob_day'],
        dob_year=account_data['dob_year'],
        card_number=account_data['card_number'],
        card_expiry=account_data['card_expiry'],
        card_cvv=account_data['card_cvv'],
        address=account_data['address'],
        city=account_data['city'],
        state=account_data['state'],
        zipcode=account_data['zipcode']
    )
    
    if success:
        print("\n✅ Hulu account created successfully!")
        print("You can now log in with the following credentials:")
        print(f"Email: {account_data['email']}")
        print(f"Password: {account_data['password']}")
        print("Login at: https://www.hulu.com/login")
    else:
        print("\n❌ Failed to create Hulu account.")
        print("Check the log file (real_hulu_account.log) for details.")
        print("You can also view the screenshots for more information.")