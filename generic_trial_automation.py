"""
Generic Trial Automation
A flexible script for automating trial signup on any website
"""
import time
import sys
import os
import logging
import random
import string
import re
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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

# Import config if available
try:
    from config import GENERIC_SITE_PATTERNS
except ImportError:
    GENERIC_SITE_PATTERNS = {
        "streaming": ["netflix", "hulu", "disney", "stream", "watch", "tv", "video", "movie"],
        "shopping": ["shop", "store", "amazon", "buy", "cart", "checkout", "retail"],
        "music": ["music", "audio", "listen", "spotify", "sound", "song", "track"],
        "productivity": ["work", "office", "software", "cloud", "storage", "document", "productivity"],
        "gaming": ["game", "play", "gaming", "console", "steam", "xbox", "playstation"],
        "education": ["learn", "course", "class", "education", "study", "tutorial", "teach"],
        "finance": ["bank", "money", "finance", "invest", "trading", "crypto", "payment"],
        "other": []  # Default category
    }

def generate_password(length=12):
    """Generate a random strong password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

class GenericTrialAutomator:
    """Class for automating trial signup on any website"""
    
    def __init__(self, headless=True, screenshots_dir="screenshots"):
        """Initialize the trial automator"""
        self.driver = None
        self.timeout = 30  # Default timeout in seconds
        self.headless = headless
        self.screenshots_dir = screenshots_dir
        
        # Create screenshots directory if it doesn't exist
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
    
    def setup_browser(self):
        """Set up and configure the browser"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        logger.info("Setting up Chrome browser with WebDriver Manager...")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return self.driver
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            logger.info("Closing browser...")
            self.driver.quit()
    
    def take_screenshot(self, filename):
        """Take a screenshot of the current page"""
        if not self.driver:
            return
            
        # Create a safe filename
        safe_filename = re.sub(r'[^\w\-_.]', '_', filename)
        filepath = os.path.join(self.screenshots_dir, safe_filename)
        
        logger.info(f"Taking screenshot: {filepath}")
        self.driver.save_screenshot(filepath)
    
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
    
    def detect_site_category(self, url):
        """
        Detect the category of a website based on its URL and content
        Returns category name as string
        """
        # Parse the URL to get the domain
        domain = urlparse(url).netloc.lower()
        path = urlparse(url).path.lower()
        
        # Check domain and path against patterns for each category
        for category, keywords in GENERIC_SITE_PATTERNS.items():
            for keyword in keywords:
                if keyword in domain or keyword in path:
                    logger.info(f"Detected site category: {category}")
                    return category
        
        # If browser is started, try to detect from page content
        if self.driver:
            try:
                # Get page title and meta description
                title = self.driver.title.lower()
                
                # Try to get meta description
                try:
                    meta_desc = self.driver.find_element(By.CSS_SELECTOR, "meta[name='description']").get_attribute("content").lower()
                except:
                    meta_desc = ""
                
                # Check content against patterns
                for category, keywords in GENERIC_SITE_PATTERNS.items():
                    for keyword in keywords:
                        if keyword in title or keyword in meta_desc:
                            logger.info(f"Detected site category from content: {category}")
                            return category
            except:
                pass
        
        # Default to "other" if no category detected
        logger.info("No specific category detected, using 'other'")
        return "other"
    
    def find_signup_elements(self, category="other"):
        """
        Find common signup elements based on site category
        Returns a dictionary with detected elements
        """
        elements = {}
        
        # Common patterns for all categories
        common_signup_buttons = [
            "//a[contains(text(), 'Sign up') or contains(text(), 'Signup') or contains(text(), 'Register')]",
            "//button[contains(text(), 'Sign up') or contains(text(), 'Signup') or contains(text(), 'Register')]",
            "//a[contains(text(), 'Free trial') or contains(text(), 'Trial')]",
            "//button[contains(text(), 'Free trial') or contains(text(), 'Trial')]",
            "//a[contains(text(), 'Try') or contains(text(), 'Start')]",
            "//button[contains(text(), 'Try') or contains(text(), 'Start')]",
            "//a[contains(@class, 'signup') or contains(@class, 'register') or contains(@class, 'trial')]",
            "//button[contains(@class, 'signup') or contains(@class, 'register') or contains(@class, 'trial')]"
        ]
        
        # Try each pattern
        for xpath in common_signup_buttons:
            try:
                buttons = self.driver.find_elements(By.XPATH, xpath)
                if buttons:
                    elements["signup_button"] = buttons[0]
                    logger.info(f"Found signup button with selector: {xpath}")
                    break
            except:
                continue
        
        # Category-specific patterns
        if category == "streaming":
            try:
                # Look for plan selection elements
                plan_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'plan') or contains(@class, 'subscription')]")
                if plan_elements:
                    elements["plan_selection"] = plan_elements
                    logger.info(f"Found {len(plan_elements)} plan elements")
            except:
                pass
                
        elif category == "shopping":
            try:
                # Look for add to cart or checkout buttons
                cart_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'cart') or contains(text(), 'Cart') or contains(text(), 'Checkout')]")
                if cart_buttons:
                    elements["cart_button"] = cart_buttons[0]
                    logger.info("Found cart/checkout button")
            except:
                pass
        
        # Find common form fields (regardless of category)
        try:
            # Email fields
            email_fields = self.driver.find_elements(By.XPATH, "//input[@type='email' or contains(@name, 'email') or contains(@id, 'email')]")
            if email_fields:
                elements["email_field"] = email_fields[0]
                logger.info("Found email field")
                
            # Password fields
            password_fields = self.driver.find_elements(By.XPATH, "//input[@type='password' or contains(@name, 'password') or contains(@id, 'password')]")
            if password_fields:
                elements["password_field"] = password_fields[0]
                logger.info("Found password field")
                
            # Name fields
            name_fields = self.driver.find_elements(By.XPATH, "//input[contains(@name, 'name') or contains(@id, 'name') or contains(@placeholder, 'name')]")
            if name_fields:
                for field in name_fields:
                    field_name = field.get_attribute("name") or field.get_attribute("id") or ""
                    if "first" in field_name.lower():
                        elements["first_name_field"] = field
                        logger.info("Found first name field")
                    elif "last" in field_name.lower():
                        elements["last_name_field"] = field
                        logger.info("Found last name field")
                    else:
                        # If we haven't found specific first/last fields, use this as a general name field
                        if "name_field" not in elements:
                            elements["name_field"] = field
                            logger.info("Found general name field")
        except Exception as e:
            logger.error(f"Error finding form fields: {str(e)}")
        
        return elements
    
    def automate_trial_signup(self, url, user_info):
        """
        Automate trial signup on any website
        
        Args:
            url (str): The URL of the trial website
            user_info (dict): User information for signup (email, password, etc.)
            
        Returns:
            dict: Result of the automation attempt
        """
        if not self.driver:
            self.setup_browser()
        
        try:
            # Navigate to the URL
            logger.info(f"Navigating to {url}")
            self.driver.get(url)
            time.sleep(3)  # Allow page to load
            
            # Take initial screenshot
            self.take_screenshot("01_initial_page.png")
            
            # Detect site category
            category = self.detect_site_category(url)
            
            # Try to find signup elements
            elements = self.find_signup_elements(category)
            
            # If we found a signup button, click it
            if "signup_button" in elements:
                logger.info("Clicking signup button")
                elements["signup_button"].click()
                time.sleep(3)
                self.take_screenshot("02_after_signup_click.png")
                
                # Re-scan for form elements that might have appeared
                elements.update(self.find_signup_elements(category))
            
            # Fill out form fields if found
            if "email_field" in elements and user_info.get("email"):
                logger.info(f"Entering email: {user_info['email']}")
                elements["email_field"].clear()
                elements["email_field"].send_keys(user_info["email"])
            
            if "password_field" in elements and user_info.get("password"):
                logger.info("Entering password")
                elements["password_field"].clear()
                elements["password_field"].send_keys(user_info["password"])
            
            if "first_name_field" in elements and user_info.get("first_name"):
                logger.info(f"Entering first name: {user_info['first_name']}")
                elements["first_name_field"].clear()
                elements["first_name_field"].send_keys(user_info["first_name"])
            
            if "last_name_field" in elements and user_info.get("last_name"):
                logger.info(f"Entering last name: {user_info['last_name']}")
                elements["last_name_field"].clear()
                elements["last_name_field"].send_keys(user_info["last_name"])
            
            if "name_field" in elements and not ("first_name_field" in elements) and user_info.get("first_name") and user_info.get("last_name"):
                # If only a general name field is found, use full name
                full_name = f"{user_info['first_name']} {user_info['last_name']}"
                logger.info(f"Entering full name: {full_name}")
                elements["name_field"].clear()
                elements["name_field"].send_keys(full_name)
            
            # Take screenshot after filling out fields
            self.take_screenshot("03_form_filled.png")
            
            # Look for submit/continue buttons
            submit_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Continue') or contains(text(), 'Next') or contains(text(), 'Sign up') or contains(text(), 'Register')]")
            
            if submit_buttons:
                logger.info("Clicking submit/continue button")
                submit_buttons[0].click()
                time.sleep(5)
                self.take_screenshot("04_after_submit.png")
            
            # Record final URL and page title
            final_url = self.driver.current_url
            page_title = self.driver.title
            
            logger.info(f"Final URL: {final_url}")
            logger.info(f"Final page title: {page_title}")
            
            # Take final screenshot
            self.take_screenshot("05_final_state.png")
            
            # Determine if the automation was successful
            # This is approximate since we can't know for sure without site-specific logic
            success_indicators = [
                "success" in final_url.lower(),
                "thank" in final_url.lower(),
                "welcome" in final_url.lower(),
                "account" in final_url.lower() and url not in final_url.lower(),
                "dashboard" in final_url.lower(),
                "success" in page_title.lower(),
                "thank" in page_title.lower(),
                "welcome" in page_title.lower()
            ]
            
            # Count the number of successful indicators
            success_score = sum(success_indicators)
            
            # If any indicators are true, consider it at least partially successful
            if success_score > 0:
                success = True
                logger.info(f"Automation appears successful (score: {success_score}/8)")
            else:
                success = False
                logger.info("Automation does not appear to be successful")
            
            return {
                "success": success,
                "url": url,
                "final_url": final_url,
                "page_title": page_title,
                "success_score": success_score,
                "elements_found": list(elements.keys()),
                "category": category,
                "user_email": user_info.get("email", ""),
                "user_password": user_info.get("password", "")
            }
            
        except Exception as e:
            logger.error(f"Error during trial automation: {str(e)}")
            self.take_screenshot("error_automation.png")
            
            return {
                "success": False,
                "error": str(e),
                "url": url,
                "user_email": user_info.get("email", ""),
                "user_password": user_info.get("password", "")
            }
        finally:
            # Don't close the browser here - let the caller close it
            pass
    
    def create_trial(self, url, user_info):
        """
        Create a trial account on any website
        
        Args:
            url (str): Website URL
            user_info (dict): User information dictionary
            
        Returns:
            dict: Result of the trial creation
        """
        try:
            # Setup browser
            self.setup_browser()
            
            # Run the automation
            result = self.automate_trial_signup(url, user_info)
            
            return result
        finally:
            # Always close the browser
            self.close_browser()

def main():
    """Main function for CLI usage"""
    print("=== Generic Trial Automator ===")
    print("This tool attempts to automatically create trial accounts on any website.")
    print("Note: Results may vary depending on the website's structure.\n")
    
    # Get URL
    url = input("Enter trial website URL: ")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    # Get user information
    print("\nEnter user information:")
    email = input("Email: ")
    password = input("Password (leave blank to generate): ") or generate_password()
    first_name = input("First name: ")
    last_name = input("Last name: ")
    
    # Create user info dictionary
    user_info = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name
    }
    
    # Create automator and run
    print(f"\nAttempting to create trial on {url}...")
    automator = GenericTrialAutomator(headless=False)  # Use headless=False to see the browser in action
    
    try:
        result = automator.create_trial(url, user_info)
        
        print("\n=== Automation Results ===")
        if result["success"]:
            print(f"✅ Automation appears successful! (Score: {result.get('success_score', 'N/A')}/8)")
        else:
            print("❌ Automation appears to have failed or is incomplete.")
            if "error" in result:
                print(f"Error: {result['error']}")
        
        print(f"\nWebsite category detected: {result.get('category', 'unknown')}")
        print(f"Elements found: {', '.join(result.get('elements_found', []))}")
        print(f"Final URL: {result.get('final_url', 'N/A')}")
        print(f"Page title: {result.get('page_title', 'N/A')}")
        
        print("\nCredentials:")
        print(f"Email: {user_info['email']}")
        print(f"Password: {user_info['password']}")
        
        print("\nScreenshots have been saved to the screenshots directory.")
        print("You may need to manually complete the signup process if it wasn't fully automated.")
    
    except Exception as e:
        print(f"\n❌ Error during automation: {str(e)}")
        print("Check the screenshots directory for visual details of what happened.")

if __name__ == "__main__":
    main()