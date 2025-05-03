"""
Test suite for Web Application
Tests web routes, authentication, and API endpoints
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main
from bot_integration import BotIntegration

class TestWebApp(unittest.TestCase):
    """Tests for web application"""
    
    def setUp(self):
        """Set up test environment"""
        # Configure app for testing
        main.app.config['TESTING'] = True
        main.app.config['WTF_CSRF_ENABLED'] = False
        
        # Create test client
        self.client = main.app.test_client()
        
        # Mock bot integration
        self.bot_patcher = patch('main.BotIntegration')
        self.mock_bot_class = self.bot_patcher.start()
        self.mock_bot = self.mock_bot_class.return_value
        
        # Mock database
        self.db_patcher = patch('main.Database')
        self.mock_db_class = self.db_patcher.start()
        self.mock_db = self.mock_db_class.return_value
        
    def tearDown(self):
        """Clean up after tests"""
        self.bot_patcher.stop()
        self.db_patcher.stop()
        
    def test_home_page(self):
        """Test home page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_dashboard_redirect_when_not_logged_in(self):
        """Test dashboard redirects when not logged in"""
        response = self.client.get('/dashboard')
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        
    def test_login_page(self):
        """Test login page loads"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        
    def test_api_discord_client_id(self):
        """Test Discord client ID API endpoint"""
        # Mock environment variable
        with patch.dict('os.environ', {'DISCORD_CLIENT_ID': '1356990568739110922'}):
            response = self.client.get('/api/discord-client-id')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['client_id'], '1356990568739110922')
            
    def test_api_trials_without_auth(self):
        """Test trials API without authentication"""
        response = self.client.get('/api/trials')
        # Should return unauthorized
        self.assertEqual(response.status_code, 401)
        
    def test_bot_api_status(self):
        """Test bot API status endpoint"""
        # Mock bot process
        with patch('main.bot_process', MagicMock()):
            main.bot_process.poll.return_value = None  # Bot is running
            response = self.client.get('/api/bot/status')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['running'])
            
            # Test bot not running
            main.bot_process.poll.return_value = 0  # Bot exited
            response = self.client.get('/api/bot/status')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertFalse(data['running'])
            
class TestDiscordOAuth(unittest.TestCase):
    """Tests for Discord OAuth2 integration"""
    
    def setUp(self):
        """Set up test environment"""
        # Configure app for testing
        main.app.config['TESTING'] = True
        main.app.config['WTF_CSRF_ENABLED'] = False
        
        # Create test client
        self.client = main.app.test_client()
        
        # Mock requests for OAuth
        self.requests_patcher = patch('main.requests')
        self.mock_requests = self.requests_patcher.start()
        
        # Mock OAuth token response
        mock_token_response = MagicMock()
        mock_token_response.json.return_value = {
            'access_token': 'test_token',
            'token_type': 'Bearer',
            'expires_in': 604800,
            'refresh_token': 'test_refresh',
            'scope': 'identify guilds'
        }
        self.mock_requests.post.return_value = mock_token_response
        
        # Mock Discord user info response
        mock_user_response = MagicMock()
        mock_user_response.json.return_value = {
            'id': '123456789012345678',
            'username': 'TestUser',
            'avatar': 'abcdef',
            'discriminator': '1234'
        }
        self.mock_requests.get.return_value = mock_user_response
        
        # Mock database
        self.db_patcher = patch('main.Database')
        self.mock_db_class = self.db_patcher.start()
        self.mock_db = self.mock_db_class.return_value
        self.mock_db.user_exists.return_value = False
        
    def tearDown(self):
        # Properly indented block
        pass
        
    def test_discord_oauth_flow(self):
        """Test Discord OAuth flow"""
        # Test oauth redirect
        response = self.client.get('/login/discord')
        self.assertEqual(response.status_code, 302)  # Should redirect to Discord
        
        # Test oauth callback
        with patch.dict('os.environ', {
            'DISCORD_CLIENT_ID': 'test_client_id',
            'DISCORD_CLIENT_SECRET': 'test_client_secret'
        }):
            response = self.client.get('/login/discord/callback?code=test_code')
            self.assertEqual(response.status_code, 302)  # Should redirect to dashboard
            
            # Check if token exchange was called
            self.mock_requests.post.assert_called_once()
            
            # Check if user info was fetched
            self.mock_requests.get.assert_called_once()
            
            # Check if user was created in database
            self.mock_db.create_user.assert_called_once()
            
if __name__ == "__main__":
    unittest.main()