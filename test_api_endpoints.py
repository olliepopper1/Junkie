"""
Test Suite for API Endpoints
Tests all API routes for proper functionality
"""
import json
import os
import unittest
from unittest.mock import patch, MagicMock

from flask import Flask, session

class APIEndpointTests(unittest.TestCase):
    """Test the API endpoints"""

    def setUp(self):
        """Set up the test environment"""
        # Import the application
        from app import app
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        # Set up test user data
        self.test_user = {
            'id': 1,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123!'
        }
        
        self.test_wallet = "TestSolanaWallet12345"
        
        # Create an application context
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()

    def test_index_route(self):
        """Test the index route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Trial Junkie', response.data)

    def test_login_route(self):
        """Test the login route"""
        # Mock the database query
        with patch('app.WebUser') as mock_user:
            # Configure the mock to return a valid user
            mock_user_instance = MagicMock()
            mock_user_instance.id = self.test_user['id']
            mock_user_instance.username = self.test_user['username']
            mock_user_instance.email = self.test_user['email']
            mock_user_instance.check_password.return_value = True
            # Replace MagicMock with serializable values for session
            mock_user_instance.get_id.return_value = str(self.test_user['id'])
            
            # Mock the query operations
            mock_user.query.filter_by.return_value.first.return_value = mock_user_instance
            
            # Test login with valid credentials
            with patch('flask_login.login_user') as mock_login:
                mock_login.return_value = True
                response = self.client.post('/login', data={
                    'email': self.test_user['email'],
                    'password': self.test_user['password']
                })
                
                # Ensure session is properly set for redirection
                with self.client.session_transaction() as sess:
                    sess['user_id'] = self.test_user['id']
                    sess['logged_in'] = True
                
                # Check if redirected to dashboard on success
                self.assertEqual(response.status_code, 302)
                # Ensure redirection logic is properly tested
                self.assertIn('/dashboard', response.headers['Location'])
                
            # Test login with invalid credentials
            mock_user_instance.check_password.return_value = False
            response = self.client.post('/login', data={
                'email': self.test_user['email'],
                'password': 'WrongPassword'
            })
            
            # Should stay on login page with error
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invalid email or password', response.data)

    def test_register_route(self):
        """Test the registration route"""
        # Mock the database query
        with patch('app.WebUser') as mock_user:
            # Configure the mock for user creation
            mock_user.query.filter_by.return_value.first.return_value = None
            mock_user.return_value = MagicMock()
            
            # Mock the database session
            with patch('app.db.session') as mock_session:
                # Test registration with valid data
                response = self.client.post('/register', data={
                    'username': 'newuser',
                    'email': 'new@example.com',
                    'password': 'Password123!',
                    'confirm_password': 'Password123!'
                })
                
                # Check if redirected to login on success
                self.assertEqual(response.status_code, 302)
                
                # Verify database operations
                mock_user.assert_called_once()
                mock_session.add.assert_called_once()
            # Test registration with existing email
            mock_user.query.filter_by.return_value.first.return_value = MagicMock()
            response = self.client.post('/register', data={
                'username': 'newuser',
                'email': 'existing@example.com',
                'password': 'Password123!',
                'confirm_password': 'Password123!'
            })
            
            # Should stay on registration page with error
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Email or username already exists', response.data)

    def test_wallet_connection(self):
        """Test wallet connection endpoint"""
        with patch('app.connect_wallet_to_user') as mock_connect:
            mock_connect.return_value = True
            
            # Test successful wallet connection
            response = self.client.post('/connect_wallet', json={
                'wallet_address': self.test_wallet
            })
            
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data)
            self.assertTrue(response_data['success'])
            
            # Test failed wallet connection
            mock_connect.return_value = False
            response = self.client.post('/connect_wallet', json={
                'wallet_address': 'invalid_wallet'
            })
            
            self.assertEqual(response.status_code, 400)
            response_data = json.loads(response.data)
            self.assertFalse(response_data['success'])

    def test_trial_generation(self):
        """Test trial generation endpoint"""
        # Mock login
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.test_user['id']
            sess['logged_in'] = True
        
        # Mock the subscription check
        with patch('app.check_subscription_status') as mock_sub_check:
            mock_sub_check.return_value = {
                'active': True,
                'tier': 'premium',
                'trial_limit': 10,
                'trials_used': 5
            }
            
            with patch('app.generate_trial_for_service', return_value={
                'success': True,
                'email': 'trial@example.com',
                'password': 'trialpass',
                'service': 'netflix',
                'expires_at': '2023-12-01'
            }):
                # Mock trial generation logic
                
                # Test successful trial generation
                response = self.client.post('/generate_trial', json={
                    'service': 'netflix'
                })
                
                self.assertEqual(response.status_code, 200)
                response_data = json.loads(response.data)
                self.assertTrue(response_data['success'])
                self.assertEqual(response_data['service'], 'netflix')
                
                # Test trial generation with inactive subscription
                mock_sub_check.return_value = {
                    'active': False,
                    'tier': None,
                    'trial_limit': 0,
                    'trials_used': 0
                }
                
                response = self.client.post('/generate_trial', json={
                    'service': 'hulu'
                })
                
                self.assertEqual(response.status_code, 403)
                response_data = json.loads(response.data)
                self.assertFalse(response_data['success'])
                self.assertIn('subscription', response_data['message'].lower())

    def test_payment_flow(self):
        """Test payment flow endpoints"""
        # Mock login
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.test_user['id']
            sess['logged_in'] = True
        
        with patch('app.create_payment_request', return_value={
            'success': True,
            'reference': 'pay_ref_12345',
            'amount': 15.0,
            'service_type': 'premium'
        }):
            # Mock payment creation logic
            response = self.client.post('/create_payment', json={
                'amount': 15.0,
                'service_type': 'premium'
            })
            self.assertEqual(response.status_code, 200)
            response_data = response.get_json()
            self.assertTrue(response_data['success'])
            
            # Mock payment verification
            with patch('app.verify_payment_status') as mock_verify:
                mock_verify.return_value = {
                    'success': True,
                    'status': 'completed',
                    'reference': 'pay_ref_12345',
                    'tx_signature': 'tx_sig_12345'
                }
                
                # Test payment verification
                response = self.client.post('/verify_payment', json={
                    'reference': 'pay_ref_12345',
                    'tx_signature': 'tx_sig_12345'
                })
                
                self.assertEqual(response.status_code, 200)
                response_data = json.loads(response.data)
                self.assertTrue(response_data['success'])
                self.assertEqual(response_data['status'], 'completed')
                
                # Test subscription activation after payment
                with patch('app.activate_subscription') as mock_activate:
                    mock_activate.return_value = {
                        'success': True,
                        'tier': 'premium',
                        'expires_at': '2023-12-01'
                    }
                    
                    # This would typically be called internally after payment verification
                    # But we test it separately here
                    response = self.client.post('/activate_subscription', json={
                        'payment_reference': 'pay_ref_12345',
                        'tier': 'premium'
                    })
                    
                    self.assertEqual(response.status_code, 200)
                    response_data = json.loads(response.data)
                    self.assertTrue(response_data['success'])
                    self.assertEqual(response_data['tier'], 'premium')

    def test_referral_system(self):
        """Test referral system endpoints"""
        # Mock login
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.test_user['id']
            sess['logged_in'] = True
        
        with patch('app.get_or_create_referral_code', return_value={
            'success': True,
            'referral_code': 'REF123',
            'referral_count': 5,
            'commission_earned': 75.0
        }):
            # Mock referral code generation logic
            # Test getting referral code
            response = self.client.get('/referral_code')
            
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data)
            self.assertTrue(response_data['success'])
            self.assertEqual(response_data['referral_code'], 'REF123')
            
            # Mock referral registration
            with patch('app.register_referral') as mock_register:
                mock_register.return_value = {
                    'success': True,
                    'referrer': 'otheruser',
                    'referral_code': 'OTHER456'
                }
                
                # Test registering with a referral code
                response = self.client.post('/register_referral', json={
                    'referral_code': 'OTHER456'
                })
                
                self.assertEqual(response.status_code, 200)
                response_data = json.loads(response.data)
                self.assertTrue(response_data['success'])
                self.assertEqual(response_data['referrer'], 'otheruser')
                
                # Test invalid referral code
                mock_register.return_value = {
                    'success': False,
                    'message': 'Invalid referral code'
                }
                
                response = self.client.post('/register_referral', json={
                    'referral_code': 'INVALID'
                })
                
                self.assertEqual(response.status_code, 400)
                response_data = json.loads(response.data)
                self.assertFalse(response_data['success'])
                self.assertIn('invalid', response_data['message'].lower())


if __name__ == '__main__':
    unittest.main()