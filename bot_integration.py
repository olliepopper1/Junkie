"""
Bot Integration for Trial Junkie
Provides API integration between the Discord bot and the website
"""
import os
import json
import logging
from database import Database

logger = logging.getLogger(__name__)

class BotIntegration:
    def __init__(self):
        self.db = Database()
        
    def get_user_trials(self, user_id):
        """Get all trials for a specific user from the database"""
        try:
            # Get user credentials from the database
            credentials = self.db.get_user_credentials(user_id)
            
            # Format the credentials as trials
            trials = []
            if credentials:
                # Group credentials by service
                service_groups = {}
                for c in credentials:
                    service = c['service']
                    if service not in service_groups:
                        service_groups[service] = {
                            'service': service,
                            'credentials': []
                        }
                    service_groups[service]['credentials'].append({
                        'type': c['credential_type'],
                        'value': c['credential_value']
                    })
                
                # Convert groups to list
                for service, data in service_groups.items():
                    trials.append(data)
            
            return credentials  # Return the original credentials for test compatibility
        except Exception as e:
            logger.error(f"Error getting user trials: {str(e)}")
            return []
    
    def get_user_payments(self, user_id):
        """Get all payments for a specific user"""
        try:
            payments = self.db.get_user_payments(user_id)
            return payments
        except Exception as e:
            logger.error(f"Error getting user payments: {str(e)}")
            return []
    
    def get_user_tier(self, user_id):
        """Get the subscription tier for a specific user"""
        try:
            tier_info = self.db.get_user_tier(user_id)
            return tier_info
        except Exception as e:
            logger.error(f"Error getting user tier: {str(e)}")
            return {'tier': 'free', 'expires_at': None}
    
    def get_referral_stats(self, user_id):
        """Get referral statistics for a specific user"""
        try:
            # Get referral code
            referral_code = self.db.get_referral_code(user_id)
            
            # Get referred users
            referrals = self.db.get_user_referrals(user_id)
            
            # Get commissions
            commissions = self.db.get_user_commissions(user_id)
            total_commission = self.db.get_total_commission(user_id)
            
            return {
                'referral_code': referral_code,
                'referrals_count': len(referrals),
                'active_referrals': len([r for r in referrals if r.get('active', False)]),
                'total_commission': total_commission,
                'commissions': commissions
            }
        except Exception as e:
            logger.error(f"Error getting referral stats: {str(e)}")
            return {
                'referral_code': None,
                'referrals_count': 0,
                'active_referrals': 0,
                'total_commission': 0,
                'commissions': []
            }
    
    def link_discord_to_web_user(self, discord_id, web_user_id):
        """Link a Discord user to a web user account"""
        try:
            # Update user in database with Discord ID
            # Note: This assumes there's a web_users table where we can store the discord_id
            # You'll need to implement this method in the Database class
            self.db.link_accounts(discord_id, web_user_id)
            return True
        except Exception as e:
            logger.error(f"Error linking Discord to web user: {str(e)}")
            return False

# Create a global instance for use in API endpoints
bot_integration = BotIntegration()