"""
Test suite for Database functionality
Tests CRUD operations and data integrity
"""
import os
import sys
import unittest
import sqlite3
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Database

class TestDatabase(unittest.TestCase):
    """Tests for database functionality"""
    
    def setUp(self):
        """Set up test database"""
        # Use in-memory database for testing
        self.db = Database(db_url=":memory:")
        
    def test_user_creation(self):
        """Test creating and retrieving a user"""
        user_id = "123456789012345678"
        username = "TestUser"
        
        # Create a new user
        self.db.create_user(user_id, username)
        
        # Verify user exists
        self.assertTrue(self.db.user_exists(user_id))
        
    def test_credential_storage(self):
        """Test storing and retrieving credentials"""
        user_id = "123456789012345678"
        username = "TestUser"
        service = "netflix"
        cred_type = "email"
        cred_value = "test@example.com"
        
        # Create user first
        self.db.create_user(user_id, username)
        
        # Save credential
        self.db.save_credential(user_id, service, cred_type, cred_value)
        
        # Retrieve credentials
        credentials = self.db.get_user_credentials(user_id, service)
        
        # Check if credential exists
        found = False
        for cred in credentials:
            if cred["type"] == cred_type and cred["value"] == cred_value:
                found = True
                break
                
        self.assertTrue(found)
        
    def test_command_logging(self):
        """Test logging commands"""
        user_id = "123456789012345678"
        username = "TestUser"
        command = "hit"
        parameters = "netflix"
        
        # Create user first
        self.db.create_user(user_id, username)
        
        # Log a command
        self.db.log_command(user_id, command, parameters)
        
        # Verify in user stats
        stats = self.db.get_user_stats(user_id)
        self.assertGreater(stats["commands"], 0)
        
    def test_payment_tracking(self):
        """Test payment tracking"""
        user_id = "123456789012345678"
        username = "TestUser"
        amount = 9.99
        reference = "TEST123"
        service_type = "premium"
        
        # Create user first
        self.db.create_user(user_id, username)
        
        # Save payment request
        self.db.save_payment_request(user_id, amount, reference, service_type)
        
        # Retrieve payment
        payment = self.db.get_payment_by_reference(reference)
        self.assertEqual(payment["reference"], reference)
        self.assertEqual(payment["status"], "pending")
        
        # Update payment status
        self.db.update_payment_status(reference, "completed", "tx_12345")
        
        # Verify updated payment
        payment = self.db.get_payment_by_reference(reference)
        self.assertEqual(payment["status"], "completed")
        
    def test_referral_system(self):
        """Test referral system"""
        referrer_id = "111111111111111111"
        referred_id = "222222222222222222"
        
        # Create users
        self.db.create_user(referrer_id, "Referrer")
        self.db.create_user(referred_id, "Referred")
        
        # Generate referral code
        code = self.db.get_referral_code(referrer_id)
        self.assertIsNotNone(code)
        
        # Register referral
        self.db.register_referral(referred_id, code)
        
        # Check referrals
        referrals = self.db.get_user_referrals(referrer_id)
        self.assertEqual(len(referrals), 1)
        self.assertEqual(referrals[0]["user_id"], referred_id)
        
if __name__ == "__main__":
    unittest.main()