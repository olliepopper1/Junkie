"""
YouTube Premium Trial Creator
Simplified script to create a YouTube Premium trial
"""
import time
import logging
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

def create_youtube_premium_trial(email, password, card_number, card_expiry, card_cvv, name_on_card,
                                address, city, state, zipcode, country="US"):
    """
    Create a YouTube Premium trial account
    
    Args:
        email (str): Google account email
        password (str): Google account password
        card_number (str): Credit card number
        card_expiry (str): Credit card expiry date (MM/YY)
        card_cvv (str): Credit card CVV
        name_on_card (str): Name on credit card
        address (str): Billing address
        city (str): Billing city
        state (str): Billing state
        zipcode (str): Billing ZIP code
        country (str, optional): Billing country. Defaults to "US".
        
    Returns:
        dict: Result of the trial creation
    """
    # Setup Chrome
    chrome_options = Options()
    # Uncomment the line below if you want to run in headless mode (no UI)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    logger.info("Setting up Chrome browser...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Step 1: Go to YouTube Premium page
        logger.info("Navigating to YouTube Premium page...")
        driver.get("https://www.youtube.com/premium")
        time.sleep(2)
        
        # Take a screenshot for debugging
        driver.save_screenshot("01_youtube_premium_page.png")
        
        # Step 2: Click on Get YouTube Premium button
        try:
            get_premium_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//yt-button-renderer[contains(@class, 'style-primary')]//a"))
            )
            logger.info("Clicking on 'Get YouTube Premium' button...")
            get_premium_button.click()
            time.sleep(2)
        except Exception as e:
            logger.error(f"Error clicking Get Premium button: {str(e)}")
            driver.save_screenshot("error_get_premium.png")
        
        # Step 3: Sign in with Google account
        driver.save_screenshot("02_google_signin.png")
        logger.info("Attempting to sign in with Google account...")
        
        # Enter email
        try:
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_field.clear()
            email_field.send_keys(email)
            logger.info(f"Entered email: {email}")
            
            # Click Next
            next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            time.sleep(2)
        except Exception as e:
            logger.error(f"Error entering email: {str(e)}")
            driver.save_screenshot("error_email.png")
        
        # Enter password
        driver.save_screenshot("03_password_page.png")
        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_field.clear()
            password_field.send_keys(password)
            logger.info("Entered password")
            
            # Click Next
            next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            time.sleep(3)
        except Exception as e:
            logger.error(f"Error entering password: {str(e)}")
            driver.save_screenshot("error_password.png")
        
        # Step 4: Select YouTube Premium plan
        driver.save_screenshot("04_select_plan.png")
        logger.info("Selecting YouTube Premium plan...")
        
        try:
            # Wait for the page to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'plan-option')]"))
            )
            
            # Select the Individual plan
            individual_plan = driver.find_element(By.XPATH, "//div[contains(@class, 'plan-option') and contains(., 'Individual')]")
            individual_plan.click()
            logger.info("Selected Individual plan")
            time.sleep(2)
            
            # Click Continue or Next
            continue_button = driver.find_element(By.XPATH, "//button[contains(., 'Continue') or contains(., 'Next')]")
            continue_button.click()
            time.sleep(3)
        except Exception as e:
            logger.error(f"Error selecting plan: {str(e)}")
            driver.save_screenshot("error_plan_selection.png")
        
        # Step 5: Enter payment details
        driver.save_screenshot("05_payment_details.png")
        logger.info("Entering payment details...")
        
        try:
            # Sometimes payment details are in an iframe
            payment_frames = driver.find_elements(By.TAG_NAME, "iframe")
            if payment_frames:
                logger.info(f"Found {len(payment_frames)} iframes, switching to payment frame...")
                for frame in payment_frames:
                    try:
                        driver.switch_to.frame(frame)
                        # Check if this is the payment frame
                        if len(driver.find_elements(By.ID, "credit-card-number")) > 0:
                            logger.info("Successfully switched to payment frame")
                            break
                        # If not, switch back
                        driver.switch_to.default_content()
                    except:
                        driver.switch_to.default_content()
            
            # Now enter payment details
            # Card number
            card_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "credit-card-number"))
            )
            card_field.clear()
            card_field.send_keys(card_number)
            logger.info(f"Entered card number ending in {card_number[-4:]}")
            
            # Expiry date
            expiry_field = driver.find_element(By.ID, "credit-card-expiry")
            expiry_field.clear()
            expiry_field.send_keys(card_expiry.replace("/", ""))
            logger.info(f"Entered expiry: {card_expiry}")
            
            # CVV
            cvv_field = driver.find_element(By.ID, "credit-card-cvv")
            cvv_field.clear()
            cvv_field.send_keys(card_cvv)
            logger.info(f"Entered CVV: {card_cvv}")
            
            # Name on card
            name_field = driver.find_element(By.ID, "name-on-card")
            name_field.clear()
            name_field.send_keys(name_on_card)
            logger.info(f"Entered name on card: {name_on_card}")
            
            # Billing address
            address_field = driver.find_element(By.ID, "billing-address-line1")
            address_field.clear()
            address_field.send_keys(address)
            logger.info(f"Entered address: {address}")
            
            # City
            city_field = driver.find_element(By.ID, "billing-locality")
            city_field.clear()
            city_field.send_keys(city)
            logger.info(f"Entered city: {city}")
            
            # State
            state_field = driver.find_element(By.ID, "billing-administrative-area")
            state_field.clear()
            state_field.send_keys(state)
            logger.info(f"Entered state: {state}")
            
            # ZIP code
            zip_field = driver.find_element(By.ID, "billing-postal-code")
            zip_field.clear()
            zip_field.send_keys(zipcode)
            logger.info(f"Entered ZIP code: {zipcode}")
            
            # Submit payment information
            driver.save_screenshot("06_payment_filled.png")
            submit_button = driver.find_element(By.XPATH, "//button[contains(., 'Submit') or contains(., 'Buy') or contains(., 'Continue')]")
            submit_button.click()
            logger.info("Submitted payment information")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Error entering payment details: {str(e)}")
            driver.save_screenshot("error_payment_details.png")
        
        # Step 6: Check for confirmation
        driver.save_screenshot("07_confirmation.png")
        logger.info("Checking for confirmation...")
        
        # Switch back to main content if we were in iframe
        driver.switch_to.default_content()
        
        # Check for success indicators
        try:
            success_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Thank you') or contains(text(), 'Subscription') or contains(text(), 'Premium')]"))
            )
            success = True
            logger.info("Successfully created YouTube Premium trial!")
        except:
            success = False
            logger.warning("Could not confirm successful trial creation")
        
        # Final URL
        final_url = driver.current_url
        logger.info(f"Final URL: {final_url}")
        
        return {
            "service": "YouTube Premium",
            "email": email,
            "password": password,
            "success": success,
            "final_url": final_url
        }
    finally:
        # Always close the browser
        logger.info("Closing browser...")
        driver.quit()

def main():
    """Main function to run from command line"""
    print("=== YouTube Premium Trial Creator ===")
    print("Note: You will need an existing Google account and valid payment information.")
    
    # Get user information
    email = input("Google account email: ")
    password = input("Google account password: ")
    
    print("\nPayment Information:")
    card_number = input("Credit card number: ")
    card_expiry = input("Expiry date (MM/YY): ")
    card_cvv = input("CVV: ")
    name_on_card = input("Name on card: ")
    
    print("\nBilling Address:")
    address = input("Street address: ")
    city = input("City: ")
    state = input("State (2-letter code): ")
    zipcode = input("ZIP code: ")
    
    # Create the trial
    print("\nCreating YouTube Premium trial...")
    result = create_youtube_premium_trial(
        email=email,
        password=password,
        card_number=card_number,
        card_expiry=card_expiry,
        card_cvv=card_cvv,
        name_on_card=name_on_card,
        address=address,
        city=city,
        state=state,
        zipcode=zipcode
    )
    
    # Display result
    if result["success"]:
        print("\n✅ Successfully created YouTube Premium trial!")
        print(f"Login with: {result['email']}")
        print("\nIMPORTANT: Remember to cancel before the trial ends to avoid charges!")
        print("You can manage your subscription at: https://www.youtube.com/paid_memberships")
    else:
        print("\n❌ Could not confirm successful trial creation")
        print("Please check the screenshots folder for more information")
        print("You may need to check your Google account to see if the subscription was created")

if __name__ == "__main__":
    main()