"""
Payment Processor Utility
Handles payment processing and subscription management
"""
import os
import time
import uuid
import logging
import asyncio
from datetime import datetime, timedelta

# Load database connection
from database import Database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define subscription tiers
SUBSCRIPTION_TIERS = {
    'free': {
        'name': 'Free Tier',
        'price': 0,
        'duration_days': 0,  # Unlimited
        'daily_limits': {
            'hit': 1,
            'dose': 3,
            'trip': 0,
        }
    },
    'rush': {
        'name': 'Five Dollar Rush',
        'price': 5,
        'duration_days': 7,
        'daily_limits': {
            'hit': 5,
            'dose': 10,
            'trip': 3,
        }
    },
    'premium': {
        'name': 'Junkified',
        'price': 19.99,
        'duration_days': 30,
        'daily_limits': {
            'hit': 50,
            'dose': 100,
            'trip': 30,
        }
    }
}

class PaymentProcessor:
    """
    Handles payment processing and subscription management
    Integrates with Solana blockchain for payments
    """
    def __init__(self, db_url=None):
        """Initialize the payment processor"""
        self.db = Database(db_url)
        # Get the wallet address from environment variables
        self.wallet_address = os.environ.get('SOLANA_WALLET_ADDRESS')
        
    async def create_payment_request(self, user_id, plan_id, amount):
        """
        Create a payment request for a user's subscription
        
        Args:
            user_id (str): User ID
            plan_id (str): Subscription plan ID (free, rush, premium)
            amount (float): Payment amount in SOL
            
        Returns:
            dict: Payment request details
        """
        try:
            # Check if the user exists, or create them
            if not self.db.user_exists(user_id):
                return {'error': 'User not found'}
            
            # Check if plan exists
            if plan_id not in SUBSCRIPTION_TIERS:
                return {'error': 'Invalid subscription plan'}
            
            # Generate unique payment reference
            reference = f"TJ-{uuid.uuid4().hex[:8].upper()}"
            
            # Save payment request to database
            self.db.save_payment_request(
                user_id=user_id,
                amount=amount,
                reference=reference,
                service_type=plan_id
            )
            
            # Return payment details
            return {
                'success': True,
                'reference': reference,
                'amount': amount,
                'wallet_address': self.wallet_address,
                'created_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error creating payment request: {str(e)}")
            return {'error': str(e)}
    
    async def verify_payment(self, reference, tx_signature=None):
        """
        Verify a payment on the Solana blockchain
        
        Args:
            reference (str): Payment reference
            tx_signature (str, optional): Transaction signature
            
        Returns:
            dict: Verification result
        """
        try:
            # Get the payment from database
            payment = self.db.get_payment_by_reference(reference)
            
            if not payment:
                return {
                    'success': False,
                    'message': 'Payment reference not found'
                }
            
            if payment['status'] == 'completed':
                # Payment already verified
                return {
                    'success': True,
                    'message': 'Payment already verified',
                    'service_type': payment['service_type']
                }
            
            # In a real implementation, this would verify the transaction
            # on the Solana blockchain using @solana/web3.js
            
            # For demo purposes, let's simulate a successful verification
            # In production, you'd use tx_signature to verify the payment
            
            # Update payment status in database
            self.db.update_payment_status(
                reference=reference,
                status='completed',
                tx_signature=tx_signature or 'simulated_signature'
            )
            
            # Update user's subscription tier
            tier_duration = SUBSCRIPTION_TIERS[payment['service_type']]['duration_days']
            expires_at = None
            if tier_duration > 0:
                expires_at = (datetime.now() + timedelta(days=tier_duration)).isoformat()
                
            self.db.update_user_tier(
                user_id=payment['user_id'],
                tier=payment['service_type'],
                expires_at=expires_at
            )
            
            # Return success
            return {
                'success': True,
                'message': 'Payment verified successfully',
                'service_type': payment['service_type']
            }
        except Exception as e:
            logger.error(f"Error verifying payment: {str(e)}")
            return {
                'success': False,
                'message': f"Error verifying payment: {str(e)}"
            }
    
    async def get_user_payments(self, user_id, status=None):
        """
        Get a user's payment history
        
        Args:
            user_id (str): User ID
            status (str, optional): Filter by payment status
            
        Returns:
            list: List of payments
        """
        try:
            payments = self.db.get_user_payments(user_id, status)
            return payments
        except Exception as e:
            logger.error(f"Error getting user payments: {str(e)}")
            return []
    
    async def get_user_tier(self, user_id):
        """
        Get a user's subscription tier
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: Tier information
        """
        try:
            tier_info = self.db.get_user_tier(user_id)
            
            if not tier_info:
                # Default to free tier
                return {
                    'tier': 'free',
                    'name': SUBSCRIPTION_TIERS['free']['name'],
                    'limits': SUBSCRIPTION_TIERS['free']['daily_limits'],
                    'expires_at': None
                }
            
            # Check if subscription has expired
            if tier_info['expires_at'] and datetime.fromisoformat(tier_info['expires_at']) < datetime.now():
                # Subscription expired, downgrade to free tier
                self.db.update_user_tier(
                    user_id=user_id,
                    tier='free',
                    expires_at=None
                )
                
                return {
                    'tier': 'free',
                    'name': SUBSCRIPTION_TIERS['free']['name'],
                    'limits': SUBSCRIPTION_TIERS['free']['daily_limits'],
                    'expires_at': None,
                    'expired': True
                }
            
            # Return tier info
            return {
                'tier': tier_info['tier'],
                'name': SUBSCRIPTION_TIERS[tier_info['tier']]['name'],
                'limits': SUBSCRIPTION_TIERS[tier_info['tier']]['daily_limits'],
                'expires_at': tier_info['expires_at']
            }
        except Exception as e:
            logger.error(f"Error getting user tier: {str(e)}")
            return {
                'tier': 'free',
                'name': SUBSCRIPTION_TIERS['free']['name'],
                'limits': SUBSCRIPTION_TIERS['free']['daily_limits'],
                'expires_at': None,
                'error': str(e)
            }
    
    async def check_command_limit(self, user_id, command):
        """
        Check if a user has reached their daily command limit
        
        Args:
            user_id (str): User ID
            command (str): Command name (hit, dose, trip)
            
        Returns:
            bool: True if user can use the command, False otherwise
        """
        try:
            # Get user's tier
            tier_info = await self.get_user_tier(user_id)
            
            # Get daily limit for this command
            daily_limit = tier_info['limits'].get(command, 0)
            
            # If unlimited, return True
            if daily_limit < 0:
                return True
                
            # Check usage count
            usage_count = self.db.get_usage_count(user_id, command)
            
            # Return True if user has not reached their limit
            return usage_count < daily_limit
        except Exception as e:
            logger.error(f"Error checking command limit: {str(e)}")
            return False
    
    async def track_command_usage(self, user_id, command):
        """
        Track a command usage
        
        Args:
            user_id (str): User ID
            command (str): Command name (hit, dose, trip)
            
        Returns:
            bool: True if tracked successfully, False otherwise
        """
        try:
            self.db.track_usage(user_id, command)
            return True
        except Exception as e:
            logger.error(f"Error tracking command usage: {str(e)}")
            return False