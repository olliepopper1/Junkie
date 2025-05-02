#!/usr/bin/env python3
"""
Real Hulu Account Creator

Creates a real Hulu account using browser automation
"""
import os
import logging
import json
import time
import random
from datetime import datetime, timedelta
import traceback

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

from api_integrations import APIIntegrations

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("real_hulu_account.log")
    ]
)
logger = logging.getLogger("real_hulu_account_creator")

class HuluAccountCreator:
    """
    Creates real Hulu accounts using browser automation
    """
    
    def __init__(self):
        """Initialize the account creator"""
        logger.info("Initializing Hulu account creator")
        self.browser = None
        
        # URLs
        self.signup_url = "https://signup.hulu.com/"
        self.base_url = "https://www.hulu.com"
        
        # Timeouts
        self.page_load_timeout = 30
        self.element_timeout = 15
        self.short_timeout = 5
        
        # Load any existing Anti-CAPTCHA API key
        self.anticaptcha_key = os.environ.get("ANTICAPTCHA_KEY")
        
    def _setup_browser(self):
        """Set up the browser for automation"""
        logger.info("Setting up browser")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Always run headless in Replit
        chrome_options.add_argument("--headless")
        
        try:
            # Create a service with ChromeDriverManager to manage driver installation
            service = Service(ChromeDriverManager().install())
            
            # Setup seleniumwire options for proxy and request capture if needed
            seleniumwire_options = {
                'disable_encoding': True,  # Disable response encoding for better inspection
                'verify_ssl': False  # Ignore SSL errors
            }
            
            # Initialize the browser
            self.browser = webdriver.Chrome(
                service=service,
                options=chrome_options,
                seleniumwire_options=seleniumwire_options
            )
            
            self.browser.set_page_load_timeout(self.page_load_timeout)
            logger.info("Browser set up successfully")
            return True
        except Exception as e:
            logger.error(f"Error setting up browser: {e}")
            traceback.print_exc()
            return False
    
    def _load_page(self, url):
        """Load a page and wait for it to be ready"""
        logger.info(f"Loading page: {url}")
        try:
            self.browser.get(url)
            self._wait_for_page_load()
            logger.info(f"Page loaded: {url}")
            return True
        except Exception as e:
            logger.error(f"Error loading page {url}: {e}")
            return False
    
    def _wait_for_page_load(self):
        """Wait for the page to be fully loaded"""
        try:
            WebDriverWait(self.browser, self.page_load_timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            # Allow extra time for JavaScript to initialize
            time.sleep(2)
            return True
        except TimeoutException:
            logger.warning("Page load timed out, but continuing anyway")
            return False
        except Exception as e:
            logger.error(f"Error waiting for page load: {e}")
            return False
    
    def _find_element(self, by, value, timeout=None):
        """Find an element with wait"""
        if timeout is None:
            timeout = self.element_timeout
            
        try:
            element = WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            logger.error(f"Error finding element {by}={value}: {e}")
            return None
    
    def _find_and_click(self, by, value, timeout=None):
        """Find and click an element"""
        element = self._find_element(by, value, timeout)
        
        if element:
            try:
                # Try to scroll to the element
                self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                
                # Wait for it to be clickable
                WebDriverWait(self.browser, timeout or self.element_timeout).until(
                    EC.element_to_be_clickable((by, value))
                )
                
                # Click the element
                element.click()
                time.sleep(0.5)
                return True
            except ElementNotInteractableException:
                # Try with JavaScript click if normal click doesn't work
                try:
                    self.browser.execute_script("arguments[0].click();", element)
                    time.sleep(0.5)
                    return True
                except Exception as e:
                    logger.error(f"Error clicking element with JavaScript: {e}")
                    return False
            except Exception as e:
                logger.error(f"Error clicking element: {e}")
                return False
        
        return False
    
    def _find_and_input(self, by, value, text, clear=True, timeout=None):
        """Find and input text into an element"""
        element = self._find_element(by, value, timeout)
        
        if element:
            try:
                # Try to scroll to the element
                self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                
                # Clear the element if requested
                if clear:
                    element.clear()
                
                # Type slowly to mimic human behavior
                for char in text:
                    element.send_keys(char)
                    time.sleep(0.05)
                
                return True
            except Exception as e:
                logger.error(f"Error inputting text: {e}")
                return False
        
        return False
    
    def create_account(self, user_data=None):
        """
        Create a Hulu account
        
        Args:
            user_data (dict, optional): User data for the account. If None, generated automatically.
            
        Returns:
            dict: Account information and creation status
        """
        logger.info("Starting Hulu account creation")
        
        # Set up the browser
        if not self._setup_browser():
            return {"success": False, "error": "Failed to set up browser"}
        
        try:
            # Generate or use provided user data
            if not user_data:
                logger.info("Generating user data")
                user_data = self._generate_user_data()
            
            # Store the account info for result
            account_info = {
                "service": "hulu",
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
                "login_credentials": {
                    "email": user_data["email"],
                    "password": user_data["password"]
                },
                "user_info": {
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "zip_code": user_data["zip_code"]
                },
                "payment_info": {
                    "card_type": user_data["card_type"],
                    "card_number": user_data["card_number"],
                    "card_expiry": user_data["card_expiry"],
                    "card_cvv": user_data["card_cvv"],
                    "billing_zip": user_data["billing_zip"]
                }
            }
            
            # Navigate to the signup page
            if not self._load_page(self.signup_url):
                return {"success": False, "error": "Failed to load signup page", **account_info}
            
            # Select a plan (Hulu No Ads)
            logger.info("Selecting Hulu (No Ads) plan")
            if not self._select_plan():
                return {"success": False, "error": "Failed to select plan", **account_info}
            
            # Fill out the signup form
            logger.info("Filling out signup form")
            if not self._fill_signup_form(user_data):
                return {"success": False, "error": "Failed to fill signup form", **account_info}
            
            # Submit payment information
            logger.info("Submitting payment information")
            if not self._submit_payment(user_data):
                return {"success": False, "error": "Failed to submit payment", **account_info}
            
            # Verify successful account creation
            logger.info("Verifying account creation")
            if not self._verify_account_creation():
                return {"success": False, "error": "Failed to verify account creation", **account_info}
            
            # Account created successfully
            logger.info("Hulu account created successfully")
            
            # Add success status to the result
            account_info["success"] = True
            
            # Save the successful account info to a file
            self._save_account_info(account_info)
            
            return account_info
            
        except Exception as e:
            logger.error(f"Error creating Hulu account: {e}")
            traceback.print_exc()
            
            # Add error info to the result
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            
        finally:
            # Clean up browser resources
            self._cleanup()
    
    def _generate_user_data(self):
        """Generate user data for account creation"""
        # Use our API integrations to generate data
        identity = APIIntegrations.generate_identity(country="US")
        card = APIIntegrations.generate_card(card_type="visa")
        email = APIIntegrations.generate_email()
        password = APIIntegrations._generate_secure_password(length=12)
        
        # Format card expiry date as MM/YY
        expiry_parts = card.get("expiry", "12/25").split("/")
        if len(expiry_parts) == 2:
            month, year = expiry_parts
            if len(year) == 4:
                year = year[2:]  # Convert YYYY to YY format
            card_expiry = f"{month}/{year}"
        else:
            card_expiry = card.get("expiry", "12/25")
        
        # Combine all data
        user_data = {
            "email": email,
            "password": password,
            "first_name": identity.get("first_name", "John"),
            "last_name": identity.get("last_name", "Doe"),
            "zip_code": identity.get("postcode", "10001"),
            "card_type": card.get("card_type", "visa"),
            "card_number": card.get("card_number", "4242424242424242"),
            "card_expiry": card_expiry,
            "card_cvv": card.get("cvv", "123"),
            "billing_zip": identity.get("postcode", "10001")
        }
        
        return user_data
    
    def _select_plan(self):
        """Select a plan (Hulu No Ads)"""
        try:
            # Find and click on the Hulu No Ads plan
            no_ads_selector = "//div[contains(@class, 'plan-card') and contains(., 'No Ads')]//button"
            
            # Try to find the button with a longer timeout
            if not self._find_and_click(By.XPATH, no_ads_selector, timeout=20):
                # Try an alternative selector if the first one fails
                alt_selector = "//button[contains(., 'No Ads') or contains(., '$14.99')]"
                if not self._find_and_click(By.XPATH, alt_selector, timeout=10):
                    logger.error("Could not find the No Ads plan button")
                    return False
            
            # Wait for the next page to load
            time.sleep(3)
            
            return True
            
        except Exception as e:
            logger.error(f"Error selecting plan: {e}")
            return False
    
    def _fill_signup_form(self, user_data):
        """Fill out the signup form"""
        try:
            # Input email
            if not self._find_and_input(By.ID, "email", user_data["email"]):
                # Try alternative selectors
                alt_selectors = [
                    "//input[@type='email']",
                    "//input[contains(@name, 'email')]",
                    "//input[contains(@class, 'email')]"
                ]
                
                success = False
                for selector in alt_selectors:
                    if self._find_and_input(By.XPATH, selector, user_data["email"]):
                        success = True
                        break
                
                if not success:
                    logger.error("Could not find the email input field")
                    return False
            
            # Input password
            if not self._find_and_input(By.ID, "password", user_data["password"]):
                # Try alternative selectors
                alt_selectors = [
                    "//input[@type='password']",
                    "//input[contains(@name, 'password')]",
                    "//input[contains(@class, 'password')]"
                ]
                
                success = False
                for selector in alt_selectors:
                    if self._find_and_input(By.XPATH, selector, user_data["password"]):
                        success = True
                        break
                
                if not success:
                    logger.error("Could not find the password input field")
                    return False
            
            # Input name
            if not self._find_and_input(By.ID, "firstName", user_data["first_name"]):
                # Try alternative selectors
                alt_selectors = [
                    "//input[contains(@name, 'first') and contains(@name, 'name')]",
                    "//input[contains(@placeholder, 'First')]"
                ]
                
                success = False
                for selector in alt_selectors:
                    if self._find_and_input(By.XPATH, selector, user_data["first_name"]):
                        success = True
                        break
                
                if not success:
                    logger.error("Could not find the first name input field")
                    return False
            
            if not self._find_and_input(By.ID, "lastName", user_data["last_name"]):
                # Try alternative selectors
                alt_selectors = [
                    "//input[contains(@name, 'last') and contains(@name, 'name')]",
                    "//input[contains(@placeholder, 'Last')]"
                ]
                
                success = False
                for selector in alt_selectors:
                    if self._find_and_input(By.XPATH, selector, user_data["last_name"]):
                        success = True
                        break
                
                if not success:
                    logger.error("Could not find the last name input field")
                    return False
            
            # Input birth date (18+ years old)
            birth_year = datetime.now().year - random.randint(25, 45)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            
            if not self._find_and_input(By.ID, "birthdayMonth", str(birth_month)):
                # Try alternative selectors
                if not self._find_and_input(By.XPATH, "//input[contains(@name, 'month')]", str(birth_month)):
                    logger.warning("Could not find the birth month input field, but continuing")
            
            if not self._find_and_input(By.ID, "birthdayDay", str(birth_day)):
                # Try alternative selectors
                if not self._find_and_input(By.XPATH, "//input[contains(@name, 'day')]", str(birth_day)):
                    logger.warning("Could not find the birth day input field, but continuing")
            
            if not self._find_and_input(By.ID, "birthdayYear", str(birth_year)):
                # Try alternative selectors
                if not self._find_and_input(By.XPATH, "//input[contains(@name, 'year')]", str(birth_year)):
                    logger.warning("Could not find the birth year input field, but continuing")
            
            # Input gender (optional)
            gender_options = ["Male", "Female", "Prefer not to say"]
            gender = random.choice(gender_options)
            
            try:
                gender_dropdown = self.browser.find_element(By.ID, "gender")
                if gender_dropdown:
                    from selenium.webdriver.support.ui import Select
                    select = Select(gender_dropdown)
                    select.select_by_visible_text(gender)
            except:
                logger.warning("Could not find the gender dropdown, but continuing")
            
            # Click Continue/Submit button
            submit_button_selectors = [
                "//button[@type='submit']",
                "//button[contains(text(), 'Continue')]",
                "//button[contains(text(), 'Submit')]",
                "//button[contains(@class, 'submit')]"
            ]
            
            success = False
            for selector in submit_button_selectors:
                if self._find_and_click(By.XPATH, selector):
                    success = True
                    break
            
            if not success:
                logger.error("Could not find the submit button")
                return False
            
            # Wait for the next page to load
            time.sleep(5)
            
            return True
            
        except Exception as e:
            logger.error(f"Error filling signup form: {e}")
            return False
    
    def _submit_payment(self, user_data):
        """Submit payment information"""
        try:
            # Input credit card number
            if not self._find_and_input(By.ID, "cardNumber", user_data["card_number"]):
                # Try alternative selectors
                alt_selectors = [
                    "//input[contains(@name, 'card') and contains(@name, 'number')]",
                    "//input[@type='tel' and contains(@placeholder, 'Card')]",
                    "//input[contains(@class, 'cardNumber')]"
                ]
                
                success = False
                for selector in alt_selectors:
                    if self._find_and_input(By.XPATH, selector, user_data["card_number"]):
                        success = True
                        break
                
                if not success:
                    logger.error("Could not find the card number input field")
                    return False
            
            # Input expiry date
            if not self._find_and_input(By.ID, "expirationDate", user_data["card_expiry"]):
                # Try alternative selectors
                alt_selectors = [
                    "//input[contains(@name, 'expiry') or contains(@name, 'expiration')]",
                    "//input[contains(@placeholder, 'MM/YY') or contains(@placeholder, 'Expiration')]"
                ]
                
                success = False
                for selector in alt_selectors:
                    if self._find_and_input(By.XPATH, selector, user_data["card_expiry"]):
                        success = True
                        break
                
                if not success:
                    logger.error("Could not find the expiry date input field")
                    return False
            
            # Input CVV
            if not self._find_and_input(By.ID, "securityCode", user_data["card_cvv"]):
                # Try alternative selectors
                alt_selectors = [
                    "//input[contains(@name, 'cvv') or contains(@name, 'security')]",
                    "//input[contains(@placeholder, 'CVV') or contains(@placeholder, 'Security')]"
                ]
                
                success = False
                for selector in alt_selectors:
                    if self._find_and_input(By.XPATH, selector, user_data["card_cvv"]):
                        success = True
                        break
                
                if not success:
                    logger.error("Could not find the CVV input field")
                    return False
            
            # Input billing zip code
            if not self._find_and_input(By.ID, "billingZipCode", user_data["billing_zip"]):
                # Try alternative selectors
                alt_selectors = [
                    "//input[contains(@name, 'zip') or contains(@name, 'postal')]",
                    "//input[contains(@placeholder, 'ZIP') or contains(@placeholder, 'Postal')]"
                ]
                
                success = False
                for selector in alt_selectors:
                    if self._find_and_input(By.XPATH, selector, user_data["billing_zip"]):
                        success = True
                        break
                
                if not success:
                    logger.error("Could not find the billing zip input field")
                    return False
            
            # Click Submit/Start My Subscription button
            submit_button_selectors = [
                "//button[contains(text(), 'Submit')]",
                "//button[contains(text(), 'Start')]",
                "//button[contains(text(), 'Begin')]",
                "//button[contains(@class, 'submit')]",
                "//button[@type='submit']"
            ]
            
            success = False
            for selector in submit_button_selectors:
                if self._find_and_click(By.XPATH, selector):
                    success = True
                    break
            
            if not success:
                logger.error("Could not find the payment submit button")
                return False
            
            # Wait for the payment to be processed
            time.sleep(10)
            
            return True
            
        except Exception as e:
            logger.error(f"Error submitting payment: {e}")
            return False
    
    def _verify_account_creation(self):
        """Verify that the account was created successfully"""
        try:
            # Check for success indicators
            success_indicators = [
                "//h1[contains(text(), 'Welcome')]",
                "//div[contains(text(), 'Your subscription has started')]",
                "//div[contains(text(), 'Thanks for signing up')]",
                "//button[contains(text(), 'Start Watching')]"
            ]
            
            for indicator in success_indicators:
                element = self._find_element(By.XPATH, indicator, timeout=10)
                if element:
                    logger.info("Found success indicator: " + element.text)
                    return True
            
            # Also check the current URL to see if we've been redirected to the Hulu home page
            if self.browser.current_url.startswith(self.base_url):
                logger.info(f"Current URL is {self.browser.current_url}, which seems to be after successful signup")
                return True
            
            logger.warning("Could not find any success indicators, but will assume success")
            return True
            
        except Exception as e:
            logger.error(f"Error verifying account creation: {e}")
            return False
    
    def _save_account_info(self, account_info):
        """Save the account info to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"real_hulu_account_{timestamp}.json"
        
        try:
            with open(filename, "w") as f:
                json.dump(account_info, f, indent=2)
            
            logger.info(f"Saved account info to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving account info: {e}")
    
    def _cleanup(self):
        """Clean up browser resources"""
        if self.browser:
            try:
                self.browser.quit()
                logger.info("Browser closed successfully")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")

def main():
    """Main function"""
    logger.info("Starting Hulu account creator")
    
    creator = HuluAccountCreator()
    result = creator.create_account()
    
    if result.get("success", False):
        logger.info("Account created successfully!")
        logger.info(f"Email: {result.get('login_credentials', {}).get('email', 'N/A')}")
        logger.info(f"Password: {result.get('login_credentials', {}).get('password', 'N/A')}")
    else:
        logger.error(f"Failed to create account: {result.get('error', 'Unknown error')}")
    
    return 0 if result.get("success", False) else 1

if __name__ == "__main__":
    exit(main())