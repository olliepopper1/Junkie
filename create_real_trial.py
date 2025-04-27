"""
Real Trial Creator
Uses browser automation to create genuine trial accounts
"""
import asyncio
import time
import os
import logging
import random
import string
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Available services with their configuration
SERVICES = {
    "hulu": {
        "url": "https://www.hulu.com/",
        "signup_url": "https://signup.hulu.com/plans",
        "trial_days": 30,
        "monthly_price": "$14.99"
    },
    "youtube": {
        "url": "https://www.youtube.com/",
        "signup_url": "https://www.youtube.com/premium",
        "trial_days": 30,
        "monthly_price": "$13.99"
    },
    "paramount": {
        "url": "https://www.paramountplus.com/",
        "signup_url": "https://www.paramountplus.com/account/signup/",
        "trial_days": 7,
        "monthly_price": "$11.99"
    }
}

def generate_password(length=12):
    """Generate a random strong password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

class TrialCreator:
    """Class for creating real trials on websites through browser automation"""
    
    def __init__(self):
        """Initialize the trial creator"""
        self.driver = None
        self.timeout = 30  # Timeout in seconds for waiting for elements
    
    def setup_browser(self):
        """Set up and configure the browser"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        logger.info("Setting up Chrome browser with WebDriver Manager...")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_window_size(1920, 1080)
        
        return self.driver
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            logger.info("Closing browser...")
            self.driver.quit()
    
    def wait_for_element(self, by, value, timeout=None):
        """Wait for an element to be present"""
        if timeout is None:
            timeout = self.timeout
            
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for element: {value}")
            return None
    
    def take_screenshot(self, filename):
        """Take a screenshot of the current page"""
        if self.driver:
            logger.info(f"Taking screenshot: {filename}")
            self.driver.save_screenshot(filename)
    
    def create_hulu_trial(self, email, password, first_name, last_name, 
                         address, city, state, zipcode, card_number, 
                         card_expiry, card_cvv, card_holder):
        """
        Create a Hulu trial with the provided information
        """
        service = SERVICES["hulu"]
        logger.info(f"Creating Hulu trial for {email}")
        
        try:
            # Navigate to Hulu signup page
            self.driver.get(service["signup_url"])
            logger.info(f"Navigated to Hulu signup page: {service['signup_url']}")
            
            # Wait for the page to load
            time.sleep(5)
            self.take_screenshot("01_hulu_plans.png")
            
            # Select the No Ads plan
            try:
                select_plan_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Select') and contains(@class, 'StyledButton')]")
                select_plan_button.click()
                logger.info("Selected Hulu No Ads plan")
                time.sleep(3)
            except NoSuchElementException:
                logger.warning("Could not find plan selection button, trying to continue...")
            
            self.take_screenshot("02_hulu_after_plan.png")
            
            # Create account
            logger.info("Filling out account creation form...")
            
            # Fill out email
            email_field = self.wait_for_element(By.ID, "email")
            if email_field:
                email_field.clear()
                email_field.send_keys(email)
                logger.info(f"Entered email: {email}")
            
            # Fill out password
            password_field = self.wait_for_element(By.ID, "password")
            if password_field:
                password_field.clear()
                password_field.send_keys(password)
                logger.info("Entered password")
            
            # Fill out name
            name_field = self.wait_for_element(By.ID, "name")
            if name_field:
                name_field.clear()
                name_field.send_keys(f"{first_name} {last_name}")
                logger.info(f"Entered name: {first_name} {last_name}")
            
            # Fill out birthdate
            month_field = self.wait_for_element(By.ID, "birthdayMonth")
            if month_field:
                month_field.clear()
                month_field.send_keys("01")
            
            day_field = self.wait_for_element(By.ID, "birthdayDay")
            if day_field:
                day_field.clear()
                day_field.send_keys("01")
            
            year_field = self.wait_for_element(By.ID, "birthdayYear")
            if year_field:
                year_field.clear()
                year_field.send_keys("1990")
                logger.info("Entered birthdate: 01/01/1990")
            
            # Select gender (if present)
            try:
                gender_dropdown = self.driver.find_element(By.ID, "gender")
                gender_dropdown.click()
                gender_option = self.driver.find_element(By.XPATH, "//option[@value='male']")
                gender_option.click()
                logger.info("Selected gender: Male")
            except NoSuchElementException:
                logger.warning("Gender selection not found, continuing...")
            
            self.take_screenshot("03_hulu_account_form.png")
            
            # Submit account form
            try:
                continue_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'CONTINUE') or contains(text(), 'Continue')]")
                continue_button.click()
                logger.info("Submitted account information")
                time.sleep(3)
            except NoSuchElementException:
                logger.error("Could not find continue button")
                self.take_screenshot("error_no_continue_button.png")
            
            self.take_screenshot("04_hulu_billing.png")
            
            # Fill out billing information
            logger.info("Filling out billing information...")
            
            # Fill out card number
            card_number_field = self.wait_for_element(By.ID, "card-number")
            if card_number_field:
                card_number_field.clear()
                card_number_field.send_keys(card_number)
                logger.info(f"Entered card number ending in {card_number[-4:]}")
            
            # Fill out expiration date
            expiry_field = self.wait_for_element(By.ID, "expiry-date")
            if expiry_field:
                expiry_field.clear()
                expiry_field.send_keys(card_expiry.replace("/", ""))
                logger.info(f"Entered expiry: {card_expiry}")
            
            # Fill out CVV
            cvv_field = self.wait_for_element(By.ID, "cvv")
            if cvv_field:
                cvv_field.clear()
                cvv_field.send_keys(card_cvv)
                logger.info(f"Entered CVV: {card_cvv}")
            
            # Fill out billing address
            address_field = self.wait_for_element(By.ID, "address1")
            if address_field:
                address_field.clear()
                address_field.send_keys(address)
                logger.info(f"Entered address: {address}")
            
            city_field = self.wait_for_element(By.ID, "city")
            if city_field:
                city_field.clear()
                city_field.send_keys(city)
                logger.info(f"Entered city: {city}")
            
            # Select state
            try:
                state_dropdown = self.driver.find_element(By.ID, "state")
                state_dropdown.click()
                state_option = self.driver.find_element(By.XPATH, f"//option[contains(text(), '{state}')]")
                state_option.click()
                logger.info(f"Selected state: {state}")
            except NoSuchElementException:
                logger.warning("State selection not found or state not available")
            
            # Fill out zip code
            zip_field = self.wait_for_element(By.ID, "zip")
            if zip_field:
                zip_field.clear()
                zip_field.send_keys(zipcode)
                logger.info(f"Entered zipcode: {zipcode}")
            
            self.take_screenshot("05_hulu_billing_filled.png")
            
            # Submit billing form
            try:
                submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'SUBMIT') or contains(text(), 'Submit')]")
                submit_button.click()
                logger.info("Submitted billing information")
                time.sleep(5)
            except NoSuchElementException:
                logger.error("Could not find submit button")
                self.take_screenshot("error_no_submit_button.png")
            
            self.take_screenshot("06_hulu_confirmation.png")
            
            # Check for success indicators
            success = False
            try:
                success_element = self.wait_for_element(By.XPATH, "//h1[contains(text(), 'Welcome') or contains(text(), 'Account')]")
                if success_element:
                    success = True
                    logger.info("Successfully created Hulu trial!")
            except:
                logger.warning("Could not confirm successful trial creation")
            
            # Get current URL to verify where we ended up
            final_url = self.driver.current_url
            logger.info(f"Final URL: {final_url}")
            
            trial_info = {
                "service": "Hulu",
                "email": email,
                "password": password,
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "end_date": None,  # Will be calculated later
                "success": success,
                "final_url": final_url
            }
            
            return trial_info
            
        except Exception as e:
            logger.error(f"Error creating Hulu trial: {str(e)}")
            self.take_screenshot("error_hulu_trial.png")
            return {"service": "Hulu", "email": email, "success": False, "error": str(e)}
    
    def create_trial(self, service_name, user_info):
        """Create a trial for the specified service"""
        if service_name.lower() not in SERVICES:
            logger.error(f"Service not supported: {service_name}")
            return {"success": False, "error": f"Service not supported: {service_name}"}
        
        # Set up the browser
        self.setup_browser()
        
        try:
            # Call the appropriate method based on the service
            if service_name.lower() == "hulu":
                result = self.create_hulu_trial(
                    email=user_info["email"],
                    password=user_info["password"],
                    first_name=user_info["first_name"],
                    last_name=user_info["last_name"],
                    address=user_info["address"],
                    city=user_info["city"],
                    state=user_info["state"],
                    zipcode=user_info["zipcode"],
                    card_number=user_info["card_number"],
                    card_expiry=user_info["card_expiry"],
                    card_cvv=user_info["card_cvv"],
                    card_holder=user_info["card_holder"]
                )
            # Add other services as needed
            
            return result
        finally:
            # Always close the browser
            self.close_browser()

def main():
    """Main function for CLI usage"""
    # Get input from user for trial creation
    print("=== Real Trial Creator ===")
    print("Note: You will need to provide legitimate information to create a real trial.")
    print("Services available:")
    for service in SERVICES:
        print(f"- {service.capitalize()}: {SERVICES[service]['trial_days']} day trial, {SERVICES[service]['monthly_price']}/month")
    
    service = input("\nWhich service do you want to create a trial for? ").lower()
    if service not in SERVICES:
        print(f"Service not supported: {service}")
        return
    
    print(f"\nYou'll need to provide the following information for your {service.capitalize()} trial:")
    
    email = input("Email address: ")
    password = input("Password (leave blank to generate): ") or generate_password()
    
    first_name = input("First name: ")
    last_name = input("Last name: ")
    address = input("Street address: ")
    city = input("City: ")
    state = input("State (2-letter code): ")
    zipcode = input("ZIP code: ")
    
    print("\nCredit card information (for trial signup):")
    card_number = input("Card number: ")
    card_expiry = input("Expiry date (MM/YY): ")
    card_cvv = input("CVV: ")
    card_holder = input("Card holder name: ")
    
    # Create the trial
    print(f"\nCreating {service.capitalize()} trial for {email}...")
    
    user_info = {
        "email": email,
        "password": password,
        "first_name": first_name, 
        "last_name": last_name,
        "address": address,
        "city": city,
        "state": state,
        "zipcode": zipcode,
        "card_number": card_number,
        "card_expiry": card_expiry,
        "card_cvv": card_cvv,
        "card_holder": card_holder
    }
    
    creator = TrialCreator()
    result = creator.create_trial(service, user_info)
    
    if result["success"]:
        print(f"\n✅ Successfully created {service.capitalize()} trial!")
        print(f"Login email: {result['email']}")
        print(f"Password: {result['password']}")
        print(f"Start date: {result['start_date']}")
        
        # Calculate end date based on trial period
        end_date = datetime.strptime(result['start_date'], "%Y-%m-%d")
        days = SERVICES[service]['trial_days']
        end_date = end_date.replace(day=end_date.day + days)
        print(f"End date: {end_date.strftime('%Y-%m-%d')}")
        
        print(f"\nIMPORTANT: Remember to cancel before {end_date.strftime('%Y-%m-%d')} to avoid charges!")
        print(f"Login at {SERVICES[service]['url']} to access your subscription.")
    else:
        print(f"\n❌ Failed to create {service.capitalize()} trial")
        if "error" in result:
            print(f"Error: {result['error']}")
        print("Check the error screenshots for more information.")

if __name__ == "__main__":
    main()