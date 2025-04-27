"""
Test suite for Trial Automation
Tests browser automation and trial generation
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from create_real_trial import TrialCreator
from generic_trial_automation import GenericTrialAutomator
from generate_trial_local import generate_identity, generate_card

class TestTrialGeneration(unittest.TestCase):
    """Tests for trial data generation"""
    
    def test_identity_generation(self):
        """Test identity generation"""
        identity = generate_identity()
        
        # Check identity has all required fields
        self.assertIn("first_name", identity)
        self.assertIn("last_name", identity)
        self.assertIn("email", identity)
        self.assertIn("password", identity)
        
        # Check email is properly formatted
        self.assertIn("@", identity["email"])
        
        # Check password meets minimum requirements
        self.assertGreaterEqual(len(identity["password"]), 8)
        
    def test_card_generation(self):
        """Test card generation"""
        card = generate_card()
        
        # Check card has all required fields
        self.assertIn("number", card)  # Field is called 'number' not 'card_number'
        self.assertIn("expiry", card)
        self.assertIn("cvv", card)
        self.assertIn("holder", card)
        
        # Check card number length
        self.assertTrue(len(card["number"].replace(" ", "")) in [15, 16])
        
        # Check expiry format (MM/YY)
        self.assertRegex(card["expiry"], r"\d{2}/\d{2}")
        
        # Check CVV is 3-4 digits
        self.assertTrue(len(card["cvv"]) in [3, 4])

class TestTrialAutomation(unittest.TestCase):
    """Tests for trial automation"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock selenium WebDriver
        self.selenium_patcher = patch('create_real_trial.webdriver')
        self.mock_webdriver = self.selenium_patcher.start()
        
        # Mock WebDriverWait
        self.wait_patcher = patch('create_real_trial.WebDriverWait')
        self.mock_wait = self.wait_patcher.start()
        
        # Mock expected_conditions
        self.ec_patcher = patch('create_real_trial.expected_conditions')
        self.mock_ec = self.ec_patcher.start()
        
        # Create a mock driver
        self.mock_driver = MagicMock()
        self.mock_webdriver.Chrome.return_value = self.mock_driver
        
        # Create trial creator instance
        self.creator = TrialCreator()
        self.creator.driver = self.mock_driver
        
    def tearDown(self):
        """Clean up after tests"""
        self.selenium_patcher.stop()
        self.wait_patcher.stop()
        self.ec_patcher.stop()
        
    @patch('create_real_trial.TrialCreator.setup_browser')
    @patch('create_real_trial.TrialCreator.close_browser')
    def test_hulu_trial_creation(self, mock_close, mock_setup):
        """Test Hulu trial creation"""
        # Mock successful element finding
        self.mock_driver.find_element.return_value = MagicMock()
        
        # Define test data
        user_data = {
            "email": "test@example.com",
            "password": "Password123",
            "first_name": "Test",
            "last_name": "User",
            "address": "123 Main St",
            "city": "Testville",
            "state": "CA",
            "zipcode": "90210",
            "card_number": "4111111111111111",
            "card_expiry": "12/25",
            "card_cvv": "123",
            "card_holder": "Test User"
        }
        
        # Run the trial creation
        result = self.creator.create_hulu_trial(
            user_data["email"], user_data["password"], 
            user_data["first_name"], user_data["last_name"],
            user_data["address"], user_data["city"], 
            user_data["state"], user_data["zipcode"],
            user_data["card_number"], user_data["card_expiry"], 
            user_data["card_cvv"], user_data["card_holder"]
        )
        
        # Verify the driver interactions
        self.mock_driver.get.assert_called_once()
        self.assertTrue(self.mock_driver.find_element.called)
        
class TestGenericAutomation(unittest.TestCase):
    """Tests for generic trial automation"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock selenium WebDriver
        self.selenium_patcher = patch('generic_trial_automation.webdriver')
        self.mock_webdriver = self.selenium_patcher.start()
        
        # Mock WebDriverWait
        self.wait_patcher = patch('generic_trial_automation.WebDriverWait')
        self.mock_wait = self.wait_patcher.start()
        
        # Mock expected_conditions
        self.ec_patcher = patch('generic_trial_automation.expected_conditions')
        self.mock_ec = self.ec_patcher.start()
        
        # Create a mock driver
        self.mock_driver = MagicMock()
        self.mock_webdriver.Chrome.return_value = self.mock_driver
        
        # Create automator instance
        self.automator = GenericTrialAutomator(headless=True)
        self.automator.driver = self.mock_driver
        
    def tearDown(self):
        """Clean up after tests"""
        self.selenium_patcher.stop()
        self.wait_patcher.stop()
        self.ec_patcher.stop()
        
    @patch('generic_trial_automation.GenericTrialAutomator.setup_browser')
    @patch('generic_trial_automation.GenericTrialAutomator.close_browser')
    def test_detect_site_category(self, mock_close, mock_setup):
        """Test site category detection"""
        # Mock page source
        self.mock_driver.page_source = """
        <html>
            <body>
                <h1>Netflix Sign Up</h1>
                <form id="signup-form">
                    <input type="email" name="email">
                    <input type="password" name="password">
                    <button type="submit">Start Trial</button>
                </form>
            </body>
        </html>
        """
        
        # Mock URL
        self.mock_driver.current_url = "https://www.netflix.com/signup"
        
        # Detect category
        category = self.automator.detect_site_category("https://www.netflix.com/signup")
        
        # Verify detection
        self.assertEqual(category, "streaming")
        
    @patch('generic_trial_automation.GenericTrialAutomator.setup_browser')
    @patch('generic_trial_automation.GenericTrialAutomator.close_browser')
    def test_find_signup_elements(self, mock_close, mock_setup):
        """Test finding signup elements"""
        # Mock element finding
        mock_email = MagicMock()
        mock_password = MagicMock()
        mock_button = MagicMock()
        
        self.mock_driver.find_elements.side_effect = lambda by, value: {
            "email": [mock_email],
            "password": [mock_password],
            "submit": [mock_button]
        }.get(value, [])
        
        # Find elements
        elements = self.automator.find_signup_elements(category="streaming")
        
        # Verify elements found
        self.assertIn("email_field", elements)
        self.assertIn("password_field", elements)
        self.assertIn("submit_button", elements)
        
if __name__ == "__main__":
    unittest.main()