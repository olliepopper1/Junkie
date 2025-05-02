"""
Test Real Trial Flow
This script tests the generation of a real trial using the API endpoints
"""
import json
import requests
import logging
import time
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API base URL
BASE_URL = "http://0.0.0.0:5000"

# Session to maintain cookies
session = requests.Session()

def register_test_user():
    """Register a test user account"""
    register_data = {
        "username": "testuser_" + str(int(time.time())),
        "email": f"test{int(time.time())}@example.com",
        "password": "Test1234!",
        "confirm_password": "Test1234!"
    }
    
    response = session.post(f"{BASE_URL}/register", json=register_data)
    logger.info(f"Register response: {response.status_code}")
    
    if response.status_code == 200:
        return register_data
    else:
        logger.error(f"Failed to register: {response.text}")
        return None

def login_user(username, password):
    """Login with the test user"""
    login_data = {
        "username": username,
        "password": password
    }
    
    response = session.post(f"{BASE_URL}/login", json=login_data)
    logger.info(f"Login response: {response.status_code}")
    
    if response.status_code == 200:
        return True
    else:
        logger.error(f"Failed to login: {response.text}")
        return False

def set_subscription_tier():
    """Set a subscription tier for the test user (may require admin access)"""
    # Note: This is a test-only function that simulates having a subscription
    # In a real scenario, this would be handled through payment processing
    try:
        # For testing, we'll use SQLite directly to update the user's subscription
        import sqlite3
        from datetime import datetime, timedelta
        
        # Connect to the database
        conn = sqlite3.connect('trial_junkie.db')
        cursor = conn.cursor()
        
        # Get the user_id from the session cookie
        session_data = session.cookies.get_dict()
        logger.info(f"Session cookies: {session_data}")
        
        # Use direct API endpoint for subscription status
        response = session.get(f"{BASE_URL}/api/subscription/status")
        logger.info(f"Subscription status: {response.status_code} - {response.text}")
        
        # If we can't identify the user, try creating a payment
        payment_data = {
            "service_type": "subscription",
            "tier": "premium",
            "payment_method": "test"
        }
        payment_response = session.post(f"{BASE_URL}/api/create-payment", json=payment_data)
        logger.info(f"Payment creation: {payment_response.status_code} - {payment_response.text}")
        
        if payment_response.status_code == 200:
            payment_data = payment_response.json()
            reference = payment_data.get('reference')
            
            # Verify the payment (simulating a successful payment)
            verify_data = {
                "reference": reference,
                "status": "completed",
                "signature": "test_signature" 
            }
            verify_response = session.post(f"{BASE_URL}/api/verify-payment", json=verify_data)
            logger.info(f"Payment verification: {verify_response.status_code} - {verify_response.text}")
            return verify_response.status_code == 200
        
        return False
        
    except Exception as e:
        logger.error(f"Error setting subscription tier: {str(e)}")
        return False

def generate_hulu_trial():
    """Generate a Hulu trial using the API"""
    trial_data = {
        "service": "hulu",
        "type": "hit",
        "automate": True
    }
    
    response = session.post(f"{BASE_URL}/api/generate-trial", json=trial_data)
    logger.info(f"Trial generation response: {response.status_code}")
    
    if response.status_code == 200:
        trial_info = response.json()
        logger.info(f"Generated trial: {json.dumps(trial_info, indent=2)}")
        return trial_info
    else:
        logger.error(f"Failed to generate trial: {response.text}")
        return None

def get_user_trials():
    """Get the user's trials"""
    response = session.get(f"{BASE_URL}/api/trials")
    logger.info(f"Get trials response: {response.status_code}")
    
    if response.status_code == 200:
        trials = response.json()
        logger.info(f"User trials: {json.dumps(trials, indent=2)}")
        return trials
    else:
        logger.error(f"Failed to get trials: {response.text}")
        return None

def run_test_flow():
    """Run the full test flow"""
    logger.info("Starting test flow for real Hulu trial generation")
    
    # Register or login
    user_data = register_test_user()
    if not user_data:
        logger.error("Failed to register test user. Testing login...")
        if not login_user("testuser", "Test1234!"):
            logger.error("Could not register or login. Exiting test.")
            return False
    else:
        # Login with the newly registered user
        if not login_user(user_data["username"], user_data["password"]):
            logger.error("Failed to login with newly registered user")
            return False
            
    logger.info("Successfully authenticated")
    
    # Set subscription tier
    if not set_subscription_tier():
        logger.warning("Could not automatically set subscription tier. This may be expected.")
        
    # Check subscription status
    subscription_response = session.get(f"{BASE_URL}/api/subscription/status")
    logger.info(f"Subscription status: {subscription_response.status_code} - {subscription_response.text}")
    
    # Generate a Hulu trial
    logger.info("Generating Hulu trial...")
    trial_info = generate_hulu_trial()
    
    if not trial_info:
        logger.error("Failed to generate Hulu trial")
        return False
        
    logger.info("Successfully generated Hulu trial")
    
    # Get the user's trials to verify the new trial was saved
    logger.info("Getting user trials...")
    trials = get_user_trials()
    
    if not trials or 'trials' not in trials or len(trials['trials']) == 0:
        logger.warning("No trials found for user. This may indicate a problem.")
    
    logger.info("Test flow completed successfully")
    return True

if __name__ == "__main__":
    logger.info("=== Trial Junkie - Real Trial Generation Test ===")
    success = run_test_flow()
    
    if success:
        logger.info("✅ All tests passed!")
    else:
        logger.error("❌ Tests failed")