#!/usr/bin/env python3
"""
Token Manager for Trial Junkie
Generates and manages secure session tokens and database credentials
"""
import os
import hashlib
import secrets
import base64
import logging
from dotenv import load_dotenv, set_key

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("token_manager")

# Load environment variables
load_dotenv()

class TokenManager:
    """
    Manages secure tokens and credentials for the Trial Junkie platform
    """
    ENV_FILE = '.env'
    
    @staticmethod
    def generate_secure_token(bytes_length=32):
        """Generate a cryptographically secure random token"""
        return secrets.token_hex(bytes_length)
    
    @staticmethod
    def generate_session_secret():
        """Generate a new session secret for Flask"""
        token = TokenManager.generate_secure_token(32)
        return token
    
    @staticmethod
    def generate_database_password(length=24):
        """Generate a secure database password"""
        # Use a mix of letters, numbers, and symbols
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    @staticmethod
    def generate_database_url(username=None, password=None, host=None, port=None, database=None):
        """Generate a database URL with the given parameters"""
        # Use environment variables as defaults
        username = username or os.getenv('PGUSER')
        password = password or os.getenv('PGPASSWORD')
        host = host or os.getenv('PGHOST')
        port = port or os.getenv('PGPORT')
        database = database or os.getenv('PGDATABASE')
        
        # Check if all required components are present
        if not all([username, password, host, port, database]):
            raise ValueError("Missing required database connection parameter")
        
        # Format the database URL
        return f"postgresql://{username}:{password}@{host}:{port}/{database}"
    
    @staticmethod
    def update_env_session_secret():
        """Generate and update the session secret in .env file"""
        try:
            new_secret = TokenManager.generate_session_secret()
            set_key(TokenManager.ENV_FILE, 'SESSION_SECRET', new_secret)
            logger.info("Session secret updated successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating session secret: {e}")
            return False
    
    @staticmethod
    def update_env_database_url(new_password=None):
        """Generate and update the database URL in .env file with a new password"""
        try:
            # Get current values
            username = os.getenv('PGUSER')
            host = os.getenv('PGHOST')
            port = os.getenv('PGPORT')
            database = os.getenv('PGDATABASE')
            
            # Generate new password if not provided
            if not new_password:
                new_password = TokenManager.generate_database_password()
            
            # Update PGPASSWORD
            set_key(TokenManager.ENV_FILE, 'PGPASSWORD', new_password)
            
            # Generate and update DATABASE_URL
            new_url = TokenManager.generate_database_url(
                username=username,
                password=new_password,
                host=host,
                port=port,
                database=database
            )
            set_key(TokenManager.ENV_FILE, 'DATABASE_URL', new_url)
            
            logger.info("Database URL and password updated successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating database URL: {e}")
            return False
    
    @staticmethod
    def get_current_env_values():
        """Get current environment values for diagnostics"""
        return {
            'SESSION_SECRET': os.getenv('SESSION_SECRET', '').replace(os.getenv('SESSION_SECRET', '')[4:-4], '********') if os.getenv('SESSION_SECRET') else None,
            'DATABASE_URL': os.getenv('DATABASE_URL', 'Not set'),
            'PGUSER': os.getenv('PGUSER', 'Not set'),
            'PGPASSWORD': '********' if os.getenv('PGPASSWORD') else 'Not set',
            'PGHOST': os.getenv('PGHOST', 'Not set'),
            'PGPORT': os.getenv('PGPORT', 'Not set'),
            'PGDATABASE': os.getenv('PGDATABASE', 'Not set'),
        }

if __name__ == "__main__":
    # Display current values
    print("Current environment values:")
    current_values = TokenManager.get_current_env_values()
    for key, value in current_values.items():
        print(f"{key}: {value}")
    
    # Ask if user wants to update session secret
    update_session = input("\nUpdate session secret? (y/n): ").lower().strip() == 'y'
    if update_session:
        success = TokenManager.update_env_session_secret()
        if success:
            print("Session secret updated successfully")
        else:
            print("Error updating session secret")
    
    # Ask if user wants to update database password
    update_db = input("\nUpdate database password? (y/n): ").lower().strip() == 'y'
    if update_db:
        success = TokenManager.update_env_database_url()
        if success:
            print("Database password and URL updated successfully")
            print("NOTE: You will need to update the database user's password to match!")
        else:
            print("Error updating database password and URL")