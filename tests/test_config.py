"""
Test Configuration
Contains common test configuration and shared fixtures
"""
import os
import sys
import unittest
from unittest.mock import MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test Database Configuration
TEST_DB_URL = ":memory:"

# Test Discord User
TEST_DISCORD_USER = {
    "id": "123456789012345678",
    "username": "TestUser",
    "discriminator": "1234",
    "avatar": "abcdef"
}

# Test Trial Data
TEST_TRIALS = [
    {
        "service": "netflix",
        "credentials": [
            {"type": "email", "value": "test@example.com"},
            {"type": "password", "value": "password123"}
        ]
    },
    {
        "service": "hulu",
        "credentials": [
            {"type": "email", "value": "test2@example.com"},
            {"type": "password", "value": "password456"}
        ]
    }
]

# Test Payment Data
TEST_PAYMENTS = [
    {
        "id": 1,
        "user_id": TEST_DISCORD_USER["id"],
        "amount": 9.99,
        "reference": "PAY123",
        "service_type": "premium",
        "status": "completed",
        "created_at": "2025-04-01T12:00:00",
        "updated_at": "2025-04-01T12:05:00",
        "tx_signature": "tx_abc123"
    },
    {
        "id": 2,
        "user_id": TEST_DISCORD_USER["id"],
        "amount": 4.99,
        "reference": "PAY456",
        "service_type": "basic",
        "status": "pending",
        "created_at": "2025-04-02T12:00:00",
        "updated_at": None,
        "tx_signature": None
    }
]

# Test User Tier
TEST_USER_TIER = {
    "tier": "premium",
    "created_at": "2025-04-01T12:00:00",
    "expires_at": "2025-05-01T12:00:00"
}

# Test Referral Data
TEST_REFERRAL_CODE = "ABC123"
TEST_REFERRALS = [
    {
        "user_id": "111111111111111111",
        "username": "ReferredUser1",
        "joined_at": "2025-03-15T10:00:00"
    },
    {
        "user_id": "222222222222222222",
        "username": "ReferredUser2",
        "joined_at": "2025-03-20T14:30:00"
    }
]
TEST_COMMISSIONS = [
    {
        "id": 1,
        "payment_id": 1,
        "amount": 2.00,
        "status": "paid",
        "created_at": "2025-04-01T12:05:00",
        "paid_at": "2025-04-10T09:15:00"
    },
    {
        "id": 2,
        "payment_id": 2,
        "amount": 1.00,
        "status": "pending",
        "created_at": "2025-04-02T12:00:00",
        "paid_at": None
    }
]

# Shared mock classes
class MockContext:
    """Mock Discord context for testing"""
    def __init__(self, user_id=TEST_DISCORD_USER["id"], username=TEST_DISCORD_USER["username"]):
        self.author = MagicMock()
        self.author.id = user_id
        self.author.name = username
        self.send = MagicMock()
        self.reply = MagicMock()
        self.message = MagicMock()
        self.bot = MagicMock()
        self.channel = MagicMock()

class BaseTestCase(unittest.TestCase):
    """Base test case with common setup/teardown"""
    
    def setUp(self):
        """Common test setup"""
        # Set environment variables for testing
        os.environ["TESTING"] = "true"
        
    def tearDown(self):
        # Properly indented block
        pass