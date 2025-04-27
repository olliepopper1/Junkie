"""
Test suite for Bot Integration with Web API
Tests the connection between Discord bot and web application
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot_integration import BotIntegration
from bot_api_helpers import BotAPI

class TestBotIntegration(unittest.TestCase):
    """Tests for bot integration with web API"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock the database
        self.db_patcher = patch('bot_integration.Database')
        self.mock_db_class = self.db_patcher.start()
        self.mock_db = self.mock_db_class.return_value
        
        # Create integration instance
        self.integration = BotIntegration()
        self.integration.db = self.mock_db
        
        # Set up mock data
        self.user_id = "123456789012345678"
        self.mock_trials = [
            {"service": "netflix", "type": "email", "value": "test@example.com"},
            {"service": "netflix", "type": "password", "value": "password123"}
        ]
        self.mock_payments = [
            {"reference": "PAY123", "amount": 9.99, "status": "completed", 
             "service_type": "premium", "created_at": "2025-04-01"}
        ]
        self.mock_tier = {"tier": "premium", "expires_at": "2025-05-01"}
        self.mock_referrals = {
            "code": "ABC123", 
            "referrals": 5, 
            "total_commission": 24.95,
            "referral_list": [
                {"user_id": "111111111111111111", "joined_at": "2025-03-15"}
            ]
        }
        
        # Set up mock return values
        self.mock_db.get_user_credentials.return_value = self.mock_trials
        self.mock_db.get_user_payments.return_value = self.mock_payments
        self.mock_db.get_user_tier.return_value = self.mock_tier
        self.mock_db.get_referral_code.return_value = self.mock_referrals["code"]
        self.mock_db.get_user_referrals.return_value = self.mock_referrals["referral_list"]
        self.mock_db.get_total_commission.return_value = self.mock_referrals["total_commission"]
        
    def tearDown(self):
        """Clean up after tests"""
        self.db_patcher.stop()
        
    def test_get_user_trials(self):
        """Test getting user trials"""
        trials = self.integration.get_user_trials(self.user_id)
        self.assertEqual(trials, self.mock_trials)
        self.mock_db.get_user_credentials.assert_called_once_with(self.user_id)
        
    def test_get_user_payments(self):
        """Test getting user payments"""
        payments = self.integration.get_user_payments(self.user_id)
        self.assertEqual(payments, self.mock_payments)
        self.mock_db.get_user_payments.assert_called_once_with(self.user_id)
        
    def test_get_user_tier(self):
        """Test getting user tier"""
        tier = self.integration.get_user_tier(self.user_id)
        self.assertEqual(tier, self.mock_tier)
        self.mock_db.get_user_tier.assert_called_once_with(self.user_id)
        
    def test_get_referral_stats(self):
        """Test getting referral statistics"""
        stats = self.integration.get_referral_stats(self.user_id)
        self.assertEqual(stats["code"], self.mock_referrals["code"])
        self.assertEqual(stats["total_commission"], self.mock_referrals["total_commission"])
        self.assertEqual(len(stats["referrals"]), len(self.mock_referrals["referral_list"]))
        
    def test_link_discord_to_web_user(self):
        """Test linking Discord to web user"""
        discord_id = self.user_id
        web_user_id = 42
        
        # Mock link_accounts method
        self.mock_db.link_accounts = MagicMock(return_value=True)
        
        result = self.integration.link_discord_to_web_user(discord_id, web_user_id)
        self.assertTrue(result)
        self.mock_db.link_accounts.assert_called_once_with(discord_id, web_user_id)
        
class TestBotAPI(unittest.TestCase):
    """Tests for bot API helper functions"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock the database
        self.db_patcher = patch('bot_api_helpers.Database')
        self.mock_db_class = self.db_patcher.start()
        self.mock_db = self.mock_db_class.return_value
        
        # Create API instance
        self.api = BotAPI()
        self.api.db = self.mock_db
        
        # Set up test data
        self.user_id = "123456789012345678"
        
    def tearDown(self):
        """Clean up after tests"""
        self.db_patcher.stop()
        
    def test_get_user_trials(self):
        """Test getting user trials"""
        mock_trials = [{"service": "netflix", "type": "email", "value": "test@example.com"}]
        self.mock_db.get_user_credentials.return_value = mock_trials
        
        trials = self.api.get_user_trials(self.user_id)
        self.assertEqual(trials, mock_trials)
        
    def test_get_user_stats(self):
        """Test getting user stats"""
        mock_stats = {"commands": 10, "trials": 5}
        self.mock_db.get_user_stats.return_value = mock_stats
        
        stats = self.api.get_user_stats(self.user_id)
        self.assertEqual(stats, mock_stats)
        
if __name__ == "__main__":
    unittest.main()