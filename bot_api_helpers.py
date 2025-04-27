#!/usr/bin/env python
"""
Bot API Helpers
Utility functions for the API to interact with the Discord bot database
"""
import os
import json
import logging
import argparse
from datetime import datetime
from database import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class BotAPI:
    def __init__(self):
        """Initialize the API with database connection"""
        self.db = Database()
    
    def get_user_trials(self, user_id):
        """Get trials for a user from the bot database"""
        try:
            # Convert user_id to integer if it's numeric
            try:
                user_id = int(user_id)
            except ValueError:
                pass  # Keep as string if not numeric
                
            # Get user credentials
            credentials = self.db.get_user_credentials(user_id)
            
            if not credentials:
                return {"success": True, "user_id": user_id, "trials": []}
            
            # Group credentials by service
            service_map = {}
            for cred in credentials:
                service = cred['service']
                if service not in service_map:
                    service_map[service] = []
                service_map[service].append(cred)
            
            # Format trials
            trials = []
            for service, creds in service_map.items():
                trial = {
                    'service': service,
                    'credentials': {},
                    'created_at': creds[0]['created_at'] if creds else None
                }
                
                # Process each credential
                for cred in creds:
                    cred_type = cred['credential_type']
                    cred_value = cred['credential_value']
                    
                    # Special handling for credential types
                    if cred_type == 'email':
                        trial['email'] = cred_value
                    elif cred_type == 'password':
                        trial['password'] = cred_value
                    elif cred_type == 'expiry':
                        trial['expires_at'] = cred_value
                    elif cred_type == 'plan':
                        trial['plan'] = cred_value
                    elif cred_type == 'url':
                        trial['url'] = cred_value
                    
                    # Add all credentials to the credentials object as well
                    trial['credentials'][cred_type] = cred_value
                
                trials.append(trial)
            
            return {"success": True, "user_id": user_id, "trials": trials}
            
        except Exception as e:
            logger.error(f"Error getting trials: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_user_stats(self, user_id):
        """Get statistics about a user from the bot database"""
        try:
            # Convert user_id to integer if it's numeric
            try:
                user_id = int(user_id)
            except ValueError:
                pass  # Keep as string if not numeric
                
            # Check if user exists
            if not self.db.user_exists(user_id):
                return {"success": True, "user_id": user_id, "stats": None}
            
            # Get user stats
            stats = self.db.get_user_stats(user_id)
            
            return {"success": True, "user_id": user_id, "stats": stats}
            
        except Exception as e:
            logger.error(f"Error getting user stats: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_user_payments(self, user_id, status=None):
        """Get payments for a user from the bot database"""
        try:
            # Convert user_id to integer if it's numeric
            try:
                user_id = int(user_id)
            except ValueError:
                pass  # Keep as string if not numeric
                
            # Get user payments
            payments = self.db.get_user_payments(user_id, status)
            
            return {"success": True, "user_id": user_id, "payments": payments}
            
        except Exception as e:
            logger.error(f"Error getting user payments: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_user_tier(self, user_id):
        """Get subscription tier for a user from the bot database"""
        try:
            # Convert user_id to integer if it's numeric
            try:
                user_id = int(user_id)
            except ValueError:
                pass  # Keep as string if not numeric
                
            # Get user tier
            tier = self.db.get_user_tier(user_id)
            
            return {"success": True, "user_id": user_id, "tier": tier}
            
        except Exception as e:
            logger.error(f"Error getting user tier: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_referral_stats(self, user_id):
        """Get referral statistics for a user from the bot database"""
        try:
            # Convert user_id to integer if it's numeric
            try:
                user_id = int(user_id)
            except ValueError:
                pass  # Keep as string if not numeric
                
            # Get referral code
            referral_code = self.db.get_referral_code(user_id)
            
            # Get referred users
            referrals = self.db.get_user_referrals(user_id)
            
            # Get commissions
            commissions = self.db.get_user_commissions(user_id)
            total_commission = self.db.get_total_commission(user_id)
            
            return {
                "success": True, 
                "user_id": user_id, 
                "referral_code": referral_code,
                "referrals": referrals,
                "commissions": commissions,
                "total_commission": total_commission
            }
            
        except Exception as e:
            logger.error(f"Error getting referral stats: {str(e)}")
            return {"success": False, "error": str(e)}

def get_user_trials_handler():
    """Command-line handler for get_user_trials"""
    parser = argparse.ArgumentParser(description='Get trials for a user')
    parser.add_argument('--user_id', required=True, help='User ID')
    
    args = parser.parse_args()
    
    api = BotAPI()
    result = api.get_user_trials(args.user_id)
    
    # Output as JSON
    print(json.dumps(result))
    
def get_user_stats_handler():
    """Command-line handler for get_user_stats"""
    parser = argparse.ArgumentParser(description='Get statistics for a user')
    parser.add_argument('--user_id', required=True, help='User ID')
    
    args = parser.parse_args()
    
    api = BotAPI()
    result = api.get_user_stats(args.user_id)
    
    # Output as JSON
    print(json.dumps(result))
    
def get_user_payments_handler():
    """Command-line handler for get_user_payments"""
    parser = argparse.ArgumentParser(description='Get payments for a user')
    parser.add_argument('--user_id', required=True, help='User ID')
    parser.add_argument('--status', required=False, help='Payment status')
    
    args = parser.parse_args()
    
    api = BotAPI()
    result = api.get_user_payments(args.user_id, args.status)
    
    # Output as JSON
    print(json.dumps(result))
    
def get_user_tier_handler():
    """Command-line handler for get_user_tier"""
    parser = argparse.ArgumentParser(description='Get subscription tier for a user')
    parser.add_argument('--user_id', required=True, help='User ID')
    
    args = parser.parse_args()
    
    api = BotAPI()
    result = api.get_user_tier(args.user_id)
    
    # Output as JSON
    print(json.dumps(result))
    
def get_referral_stats_handler():
    """Command-line handler for get_referral_stats"""
    parser = argparse.ArgumentParser(description='Get referral statistics for a user')
    parser.add_argument('--user_id', required=True, help='User ID')
    
    args = parser.parse_args()
    
    api = BotAPI()
    result = api.get_referral_stats(args.user_id)
    
    # Output as JSON
    print(json.dumps(result))

if __name__ == "__main__":
    # This code will only run if the script is executed directly
    print("Bot API Helpers - Please run one of the specific handlers:")
    print("  - get_user_trials.py")
    print("  - get_user_stats.py")
    print("  - get_user_payments.py")
    print("  - get_user_tier.py")
    print("  - get_referral_stats.py")