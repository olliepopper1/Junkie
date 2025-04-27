"""
Referral System Utility
Handles user referrals and commissions
"""
import asyncio
import json
import logging
import random
import string
from datetime import datetime, timedelta

# Configure logging
logger = logging.getLogger(__name__)

class ReferralSystem:
    """
    Handles user referrals and commission tracking
    """
    
    def __init__(self, db=None):
        """Initialize the referral system"""
        self.db = db
    
    def generate_referral_code(self, user_id):
        """
        Generate a unique referral code for a user
        
        Args:
            user_id: User's Discord ID
            
        Returns:
            str: Generated referral code
        """
        if not self.db:
            # If no DB, generate a temporary code
            chars = string.ascii_uppercase + string.digits
            return 'TJ-' + ''.join(random.choice(chars) for _ in range(8))
            
        # Check if user already has a code
        existing_code = self.db.get_referral_code(user_id)
        
        if existing_code:
            return existing_code
            
        # Generate a new code
        return self.db.create_referral_code(user_id)
    
    async def register_referral(self, referred_id, referral_code):
        """
        Register a user as referred by another user
        
        Args:
            referred_id: ID of the user being referred
            referral_code: Referral code used
            
        Returns:
            dict: Registration result
        """
        if not self.db:
            return {"success": False, "message": "Database not available"}
            
        # Check if the user is already registered
        referrer = self.db.get_referrer_for_user(referred_id)
        
        if referrer:
            return {
                "success": False, 
                "message": "You've already registered with a referral code", 
                "referrer": referrer
            }
            
        # Register the referral
        result = self.db.register_referral(referred_id, referral_code)
        
        if result["success"]:
            return {
                "success": True,
                "message": "Referral registered successfully",
                "referrer": result["referrer"]
            }
        else:
            return {
                "success": False,
                "message": result["message"]
            }
    
    async def get_user_referrals(self, user_id):
        """
        Get all users referred by a given user
        
        Args:
            user_id: User's Discord ID
            
        Returns:
            list: Referred users
        """
        if not self.db:
            return []
            
        return self.db.get_user_referrals(user_id)
    
    async def get_user_commissions(self, user_id, status=None):
        """
        Get commissions for a user
        
        Args:
            user_id: User's Discord ID
            status: Optional filter by commission status
            
        Returns:
            list: User's commissions
        """
        if not self.db:
            return []
            
        return self.db.get_user_commissions(user_id, status)
    
    async def get_total_commission(self, user_id):
        """
        Get the total commission amount for a user
        
        Args:
            user_id: User's Discord ID
            
        Returns:
            float: Total commission amount
        """
        if not self.db:
            return 0.0
            
        return self.db.get_total_commission(user_id)
    
    async def get_referral_stats(self, user_id):
        """
        Get comprehensive referral statistics for a user
        
        Args:
            user_id: User's Discord ID
            
        Returns:
            dict: Referral statistics
        """
        if not self.db:
            return {
                "referral_code": None,
                "total_referrals": 0,
                "total_commissions": 0.0,
                "pending_commissions": 0.0,
                "paid_commissions": 0.0,
                "referrals": []
            }
            
        # Get referral code
        referral_code = self.db.get_referral_code(user_id)
        
        # Get referrals
        referrals = self.db.get_user_referrals(user_id)
        
        # Get commissions
        commissions = self.db.get_user_commissions(user_id)
        
        # Calculate totals
        total_commissions = self.db.get_total_commission(user_id)
        
        pending_commissions = sum(comm["amount"] for comm in commissions if comm["status"] == "pending")
        paid_commissions = sum(comm["amount"] for comm in commissions if comm["status"] == "paid")
        
        return {
            "referral_code": referral_code,
            "total_referrals": len(referrals),
            "total_commissions": total_commissions,
            "pending_commissions": pending_commissions,
            "paid_commissions": paid_commissions,
            "referrals": referrals
        }


# For testing
async def main():
    """Main function for testing"""
    referral_system = ReferralSystem()
    
    # Generate a referral code
    code = referral_system.generate_referral_code("123456789")
    print(f"Generated referral code: {code}")


if __name__ == "__main__":
    asyncio.run(main())