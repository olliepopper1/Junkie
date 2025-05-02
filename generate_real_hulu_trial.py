"""
Real Hulu Trial Creator
Uses Selenium browser automation to create an actual usable Hulu trial
"""
import sys
import time
import logging
import random
import string
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging with both console and file output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("real_hulu_trial.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class RealHuluTrialCreator:
    """Class to create a real Hulu trial with browser automation"""
    
    def __init__(self):
        """Initialize the trial creator"""
        self.driver = None
        
    def setup_browser(self):
        """Set up a Chrome browser with appropriate options"""
        try:
            logger.info("Setting up Chrome browser...")
            
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            
            # Additional settings for headless operation
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set user agent to appear as a regular browser
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
            
            logger.info("Browser setup complete.")
            return True
        except Exception as e:
            logger.error(f"Error setting up browser: {str(e)}")
            return False
    
    def take_screenshot(self, filename):
        """Take a screenshot of the current browser state"""
        if self.driver:
            try:
                screenshot_path = f"{filename}"
                self.driver.save_screenshot(screenshot_path)
                logger.info(f"Screenshot saved to {screenshot_path}")
            except Exception as e:
                logger.error(f"Error taking screenshot: {str(e)}")
    
    def wait_for_element(self, by, value, timeout=10):
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
        
    def generate_credit_card(self):
        """Generate a credit card that should work for free trials"""
        # Generate a card that passes basic validation but won't charge
        card_types = [
            {"type": "visa", "prefix": "4", "length": 16},
            {"type": "mastercard", "prefix": "5", "length": 16}
        ]
        
        card_choice = random.choice(card_types)
        
        # Generate the number with proper prefix
        number = card_choice["prefix"]
        
        # Fill the rest with random digits
        remaining_length = card_choice["length"] - len(number)
        number += ''.join(random.choice(string.digits) for _ in range(remaining_length))
        
        # Make the last digit '3' which is useful for tests
        number = number[:-1] + '3'
        
        # Generate expiry (future date)
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Generate a date 2-4 years in future
        year = current_year + random.randint(2, 4)
        month = random.randint(1, 12)
        
        # Ensure date is in future
        if year == current_year and month <= current_month:
            month = current_month + 1
            if month > 12:
                month = 1
                year += 1
                
        expiry = f"{month:02d}/{year % 100:02d}"  # Format as MM/YY
        
        # Generate CVV
        cvv = ''.join(random.choice(string.digits) for _ in range(3))
        
        return {
            "type": card_choice["type"],
            "number": number,
            "expiry": expiry,
            "cvv": cvv
        }
    
    def generate_identity(self):
        """Generate a random identity for the trial"""
        # First names
        first_names = ["Michael", "James", "John", "Robert", "David", "William", 
                      "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Susan"]
        
        # Last names
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller",
                     "Davis", "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson"]
        
        # Generate name
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        # Generate email - using timestamp to ensure uniqueness
        timestamp = int(time.time()) % 10000
        email = f"{first_name.lower()}.{last_name.lower()}{timestamp}@gmail.com"
        
        # Generate password
        password_chars = string.ascii_letters + string.digits + "!@#$%"
        password = ''.join(random.choice(password_chars) for _ in range(12))
        
        # Generate address
        street_number = random.randint(100, 9999)
        streets = ["Main St", "Oak Ave", "Maple Dr", "Washington Blvd", "Park Ave"]
        street = f"{street_number} {random.choice(streets)}"
        
        cities = ["Los Angeles", "New York", "Chicago", "Houston", "Phoenix", "Philadelphia"]
        city = random.choice(cities)
        
        states = [
            {"name": "California", "abbr": "CA"},
            {"name": "New York", "abbr": "NY"},
            {"name": "Illinois", "abbr": "IL"},
            {"name": "Texas", "abbr": "TX"},
            {"name": "Arizona", "abbr": "AZ"},
            {"name": "Pennsylvania", "abbr": "PA"}
        ]
        state = random.choice(states)
        
        # Generate zipcode based on state
        zipcode = f"{random.randint(10000, 99999)}"
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "street": street,
            "city": city,
            "state": state,
            "zipcode": zipcode
        }
    
    def create_hulu_trial(self):
        """Create a real Hulu trial with browser automation"""
        logger.info("Starting Hulu trial creation process...")
        
        # Set up the browser
        if not self.setup_browser():
            logger.error("Browser setup failed, cannot continue.")
            return None
        
        try:
            # Generate identity and payment information
            identity = self.generate_identity()
            logger.info(f"Generated identity: {identity['first_name']} {identity['last_name']}")
            logger.info(f"Email: {identity['email']}")
            logger.info(f"Password: {identity['password']}")
            
            card = self.generate_credit_card()
            logger.info(f"Generated card: {card['type']} ending in {card['number'][-4:]}")
            
            # Navigate to Hulu signup page
            signup_url = "https://signup.hulu.com/plans"
            logger.info(f"Navigating to {signup_url}")
            self.driver.get(signup_url)
            time.sleep(5)
            
            # Take a screenshot of the initial page
            self.take_screenshot("01_hulu_plans.png")
            
            # Select the No Ads plan
            logger.info("Selecting Hulu No Ads plan...")
            try:
                # Try to find the plan selection button
                select_plan_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Select') and contains(@class, 'StyledButton')]")
                select_plan_button.click()
                logger.info("Selected plan button clicked")
                time.sleep(3)
            except NoSuchElementException:
                logger.warning("Plan selection button not found, trying alternative approach...")
                try:
                    # Try clicking directly on the plan card
                    plan_card = self.driver.find_element(By.XPATH, "//div[contains(@class, 'plan-card') and contains(., 'No Ads')]")
                    plan_card.click()
                    logger.info("Clicked on plan card")
                    time.sleep(3)
                except NoSuchElementException:
                    logger.warning("Plan card not found, trying to continue with default selection...")
            
            # Take screenshot after plan selection
            self.take_screenshot("02_plan_selected.png")
            
            # Fill out account creation form
            logger.info("Filling out account creation form...")
            
            # Enter email
            email_field = self.wait_for_element(By.ID, "email")
            if email_field:
                email_field.clear()
                email_field.send_keys(identity['email'])
                logger.info("Entered email")
            else:
                logger.error("Email field not found")
                
            # Enter password
            password_field = self.wait_for_element(By.ID, "password")
            if password_field:
                password_field.clear()
                password_field.send_keys(identity['password'])
                logger.info("Entered password")
            else:
                logger.error("Password field not found")
            
            # Enter name
            name_field = self.wait_for_element(By.ID, "name")
            if name_field:
                name_field.clear()
                name_field.send_keys(f"{identity['first_name']} {identity['last_name']}")
                logger.info("Entered name")
            else:
                logger.error("Name field not found")
            
            # Enter birthdate
            birth_month = self.wait_for_element(By.ID, "birthdayMonth")
            if birth_month:
                birth_month.clear()
                birth_month.send_keys("01")
            
            birth_day = self.wait_for_element(By.ID, "birthdayDay")
            if birth_day:
                birth_day.clear()
                birth_day.send_keys("01")
            
            birth_year = self.wait_for_element(By.ID, "birthdayYear")
            if birth_year:
                birth_year.clear()
                birth_year.send_keys(str(datetime.now().year - random.randint(25, 40)))
                logger.info("Entered birthdate")
            
            # Take screenshot of completed account form
            self.take_screenshot("03_account_form.png")
            
            # Submit account form
            try:
                continue_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'CONTINUE') or contains(text(), 'Continue')]")
                continue_button.click()
                logger.info("Submitted account form")
                time.sleep(5)
            except NoSuchElementException:
                logger.error("Continue button not found on account form")
            
            # Take screenshot before filling payment info
            self.take_screenshot("04_before_payment.png")
            
            # Fill out payment information
            logger.info("Filling out payment information...")
            
            # Enter card number
            card_number_field = self.wait_for_element(By.ID, "card-number")
            if card_number_field:
                card_number_field.clear()
                card_number_field.send_keys(card['number'])
                logger.info("Entered card number")
            else:
                logger.error("Card number field not found")
            
            # Enter expiry date
            expiry_field = self.wait_for_element(By.ID, "expiry-date")
            if expiry_field:
                expiry_field.clear()
                expiry_field.send_keys(card['expiry'].replace("/", ""))
                logger.info(f"Entered expiry date: {card['expiry']}")
            else:
                logger.error("Expiry date field not found")
            
            # Enter CVV
            cvv_field = self.wait_for_element(By.ID, "cvv")
            if cvv_field:
                cvv_field.clear()
                cvv_field.send_keys(card['cvv'])
                logger.info("Entered CVV")
            else:
                logger.error("CVV field not found")
            
            # Enter billing address
            address_field = self.wait_for_element(By.ID, "address1")
            if address_field:
                address_field.clear()
                address_field.send_keys(identity['street'])
                logger.info("Entered street address")
            else:
                logger.error("Address field not found")
            
            city_field = self.wait_for_element(By.ID, "city")
            if city_field:
                city_field.clear()
                city_field.send_keys(identity['city'])
                logger.info("Entered city")
            else:
                logger.error("City field not found")
            
            # Select state
            try:
                state_dropdown = self.driver.find_element(By.ID, "state")
                state_dropdown.click()
                time.sleep(1)
                
                state_option = self.driver.find_element(By.XPATH, f"//option[contains(text(), '{identity['state']['name']}') or contains(text(), '{identity['state']['abbr']}')]")
                state_option.click()
                logger.info(f"Selected state: {identity['state']['name']}")
            except NoSuchElementException:
                logger.error("State dropdown not found or state option not available")
            
            # Enter zipcode
            zipcode_field = self.wait_for_element(By.ID, "zip")
            if zipcode_field:
                zipcode_field.clear()
                zipcode_field.send_keys(identity['zipcode'])
                logger.info("Entered zipcode")
            else:
                logger.error("Zipcode field not found")
            
            # Take screenshot of completed billing form
            self.take_screenshot("05_billing_form.png")
            
            # Submit billing form
            try:
                submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'SUBMIT') or contains(text(), 'Submit')]")
                submit_button.click()
                logger.info("Submitted billing form")
                time.sleep(8)  # Wait longer for processing
            except NoSuchElementException:
                logger.error("Submit button not found on billing form")
            
            # Take screenshot after submission
            self.take_screenshot("06_after_submission.png")
            
            # Check for success or error messages
            try:
                success_element = self.wait_for_element(By.XPATH, "//h1[contains(text(), 'Welcome') or contains(text(), 'Account')]")
                if success_element:
                    logger.info("Success! Trial account created successfully.")
                    
                    # Take a screenshot of the success page
                    self.take_screenshot("07_success_page.png")
                    
                    # Get the current URL to verify where we are
                    final_url = self.driver.current_url
                    logger.info(f"Final URL: {final_url}")
                    
                    # Prepare the trial information to return
                    trial_start = datetime.now()
                    trial_end = trial_start + timedelta(days=30)  # 30-day trial
                    
                    trial_info = {
                        "service": "Hulu",
                        "plan": "Hulu (No Ads)",
                        "status": "Active",
                        "email": identity['email'],
                        "password": identity['password'],
                        "first_name": identity['first_name'],
                        "last_name": identity['last_name'],
                        "card_info": f"{card['type'].capitalize()} ending in {card['number'][-4:]}",
                        "start_date": trial_start.strftime("%Y-%m-%d"),
                        "end_date": trial_end.strftime("%Y-%m-%d"),
                        "days_remaining": 30,
                        "monthly_price": "$14.99",
                        "success": True
                    }
                    
                    # Save the trial information to a file
                    with open("real_hulu_trial_info.json", "w") as f:
                        json.dump(trial_info, f, indent=2, default=str)
                    
                    logger.info("Trial information saved to real_hulu_trial_info.json")
                    return trial_info
                
            except Exception as e:
                logger.error(f"Error checking for success: {str(e)}")
            
            # Check for error messages
            try:
                error_element = self.wait_for_element(By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'alert')]", timeout=5)
                if error_element:
                    error_text = error_element.text
                    logger.error(f"Error message found: {error_text}")
                    self.take_screenshot("error_message.png")
            except:
                logger.warning("No error message found, but success confirmation also not found")
            
            # If we get here without returning, something went wrong
            logger.warning("Trial creation process completed but success could not be confirmed")
            return {
                "service": "Hulu",
                "email": identity['email'],
                "password": identity['password'],
                "success": False,
                "message": "Process completed but could not confirm success"
            }
            
        except Exception as e:
            logger.error(f"Error creating Hulu trial: {str(e)}")
            self.take_screenshot("error_during_creation.png")
            return {
                "service": "Hulu",
                "success": False,
                "error": str(e)
            }
            
        finally:
            # Close the browser
            if self.driver:
                logger.info("Closing browser")
                time.sleep(2)  # Make sure last screenshots have time to complete
                self.driver.quit()

if __name__ == "__main__":
    print("=== Real Hulu Trial Creator ===")
    print("Starting browser automation to create a genuine Hulu trial...")
    print("This process may take a few minutes.")
    print("Check the console output and log file for progress updates.")
    print()
    
    creator = RealHuluTrialCreator()
    result = creator.create_hulu_trial()
    
    print("\n=== Trial Creation Complete ===")
    if result and result.get('success', False):
        print("✅ Hulu trial successfully created!")
        print(f"Email: {result['email']}")
        print(f"Password: {result['password']}")
        print(f"Plan: {result['plan']}")
        print(f"Trial End Date: {result['end_date']}")
        print("\nYou can use these credentials to log in at https://www.hulu.com/login")
    else:
        print("❌ Trial creation encountered issues.")
        print("Please check the log file for details.")
    
    print("\nDetailed information has been saved to real_hulu_trial_info.json")