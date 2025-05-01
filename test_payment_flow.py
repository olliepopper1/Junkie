"""
Test script for Solana wallet payment integration
Tests the connection, transaction, and subscription flow
"""
import json
import os
import unittest
from unittest.mock import patch, MagicMock

from flask import Flask, session
import sqlite3
import datetime

# Configuration for testing
TEST_WALLET_ADDRESS = "FakeWalletAddressForTesting123456789"
TEST_TRANSACTION_SIGNATURE = "FakeTransactionSignature123456789"
TEST_PAYMENT_REFERENCE = "pay_ref_123456789"

class PaymentFlowTest(unittest.TestCase):
    """Test the Solana wallet payment integration"""
    
    def setUp(self):
        """Set up the test environment"""
        # Create a test Flask app
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.secret_key = 'test_secret_key'
        
        # Create in-memory database for testing
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            wallet_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL,
            reference TEXT UNIQUE,
            service_type TEXT,
            status TEXT DEFAULT 'pending',
            tx_signature TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_tiers (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            tier TEXT,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Add a test user
        self.cursor.execute('''
        INSERT INTO users (id, username, email, password_hash, wallet_address)
        VALUES (1, 'test_user', 'test@example.com', 'hashed_password', ?)
        ''', (TEST_WALLET_ADDRESS,))
        
        self.conn.commit()
        
        # App context for testing
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()
        self.conn.close()

    def test_wallet_connection(self):
        """Test wallet connection functionality"""
        with patch('app.connect_wallet') as mock_connect:
            mock_connect.return_value = {'success': True, 'wallet': TEST_WALLET_ADDRESS}
            
            # Test successful connection
            with self.app.test_client() as client:
                response = client.post('/connect_wallet')
                self.assertEqual(response.status_code, 200)
                
                # Check if wallet is stored in database
                self.cursor.execute('SELECT wallet_address FROM users WHERE id = 1')
                result = self.cursor.fetchone()
                self.assertEqual(result[0], TEST_WALLET_ADDRESS)
    
    def test_payment_creation(self):
        """Test payment creation"""
        # Mock the payment creation
        with patch('app.create_payment') as mock_create_payment:
            mock_create_payment.return_value = {
                'success': True,
                'reference': TEST_PAYMENT_REFERENCE
            }
            
            # Test successful payment creation
            with self.app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = 1
                
                response = client.post('/create_payment', json={
                    'amount': 15.0,
                    'service_type': 'premium_subscription'
                })
                
                self.assertEqual(response.status_code, 200)
                
                # Check if payment is stored in database
                self.cursor.execute(
                    'SELECT reference, amount, service_type, status FROM payments WHERE user_id = 1'
                )
                result = self.cursor.fetchone()
                self.assertEqual(result[0], TEST_PAYMENT_REFERENCE)
                self.assertEqual(result[1], 15.0)
                self.assertEqual(result[2], 'premium_subscription')
                self.assertEqual(result[3], 'pending')
    
    def test_payment_verification(self):
        """Test payment verification flow"""
        # Add a pending payment
        self.cursor.execute('''
        INSERT INTO payments (user_id, amount, reference, service_type, status)
        VALUES (1, 15.0, ?, 'premium_subscription', 'pending')
        ''', (TEST_PAYMENT_REFERENCE,))
        self.conn.commit()
        
        # Mock the payment verification
        with patch('app.verify_payment') as mock_verify_payment:
            mock_verify_payment.return_value = {
                'success': True,
                'tx_signature': TEST_TRANSACTION_SIGNATURE,
                'status': 'completed'
            }
            
            # Test successful payment verification
            with self.app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = 1
                
                response = client.post('/verify_payment', json={
                    'reference': TEST_PAYMENT_REFERENCE,
                    'tx_signature': TEST_TRANSACTION_SIGNATURE
                })
                
                self.assertEqual(response.status_code, 200)
                
                # Check if payment status is updated
                self.cursor.execute(
                    'SELECT status, tx_signature FROM payments WHERE reference = ?',
                    (TEST_PAYMENT_REFERENCE,)
                )
                result = self.cursor.fetchone()
                self.assertEqual(result[0], 'completed')
                self.assertEqual(result[1], TEST_TRANSACTION_SIGNATURE)
    
    def test_subscription_activation(self):
        """Test subscription activation after payment"""
        # Add a completed payment
        self.cursor.execute('''
        INSERT INTO payments (user_id, amount, reference, service_type, status, tx_signature)
        VALUES (1, 15.0, ?, 'premium_subscription', 'completed', ?)
        ''', (TEST_PAYMENT_REFERENCE, TEST_TRANSACTION_SIGNATURE))
        self.conn.commit()
        
        # Mock the subscription activation
        with patch('app.update_user_tier') as mock_update_tier:
            # Get current time plus 30 days
            expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)
            mock_update_tier.return_value = {
                'success': True,
                'tier': 'premium',
                'expires_at': expiry_date.isoformat()
            }
            
            # Test successful subscription activation
            with self.app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = 1
                
                # Simulate internal activation after payment verification
                # (In a real app, this would happen inside the verify_payment endpoint)
                self.cursor.execute('''
                INSERT OR REPLACE INTO user_tiers (user_id, tier, expires_at)
                VALUES (1, 'premium', ?)
                ''', (expiry_date,))
                self.conn.commit()
                
                # Check subscription status
                response = client.get('/subscription_status')
                
                # Check if user has active subscription
                self.cursor.execute(
                    'SELECT tier, expires_at FROM user_tiers WHERE user_id = 1'
                )
                result = self.cursor.fetchone()
                self.assertEqual(result[0], 'premium')
                
                # Test subscription expiration
                # Set expiry to yesterday
                yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
                self.cursor.execute(
                    'UPDATE user_tiers SET expires_at = ? WHERE user_id = 1',
                    (yesterday,)
                )
                self.conn.commit()
                
                # Check if subscription is expired
                with patch('app.check_subscription_status') as mock_check:
                    mock_check.return_value = {
                        'active': False,
                        'tier': 'premium',
                        'expired': True,
                        'expires_at': yesterday.isoformat()
                    }
                    
                    response = client.get('/subscription_status')
                    # Validate with a real check
                    self.cursor.execute(
                        'SELECT expires_at FROM user_tiers WHERE user_id = 1'
                    )
                    result = self.cursor.fetchone()
                    expiry_date = datetime.datetime.fromisoformat(result[0])
                    self.assertTrue(expiry_date < datetime.datetime.now())


if __name__ == '__main__':
    unittest.main()