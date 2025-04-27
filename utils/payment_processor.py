"""
Payment Processor Utility
Handles all payment processing functions for Trial Junkie
"""
import asyncio
import json
import logging
import os
import random
import string
from datetime import datetime, timedelta
import re

# Configure logging
logger = logging.getLogger(__name__)

# Subscription tiers and pricing
SUBSCRIPTION_TIERS = {
    "free": {
        "name": "Free Tier",
        "description": "Basic access with limited requests",
        "price": 0.0,
        "daily_hit_limit": 1,
        "daily_dose_limit": 3,
        "daily_trip_limit": 0,
        "duration_days": 0,  # Unlimited
        "features": ["Basic trial generation", "Limited access to agents", "No automated trials"]
    },
    "five_dollar_rush": {
        "name": "Five Dollar Rush",
        "description": "Quick hit of trial automation",
        "price": 5.0,
        "daily_hit_limit": 5,
        "daily_dose_limit": 10,
        "daily_trip_limit": 3,
        "duration_days": 7,
        "features": ["Full access to all agents", "Automated trial creation", "7-day premium access"]
    },
    "one_time_hit": {
        "name": "One-time Hit",
        "description": "Single automated trial creation",
        "price": 2.0,
        "hits": 1,
        "doses": 0,
        "trips": 0,
        "duration_days": 1,
        "features": ["One automated trial", "One-time purchase", "No recurring charges"]
    },
    "junkified": {
        "name": "Junkified",
        "description": "Premium tier with unlimited access",
        "price": 19.99,
        "daily_hit_limit": 50,
        "daily_dose_limit": 100,
        "daily_trip_limit": 30,
        "duration_days": 30,
        "features": ["Unlimited trial generation", "Priority support", "Advanced automation", "Custom trial websites"]
    }
}


class PaymentProcessor:
    """
    Handles all payment processing functions
    """
    
    def __init__(self, db=None):
        """Initialize the payment processor"""
        self.db = db
        self.wallet_address = os.environ.get("SOLANA_WALLET_ADDRESS", "J5ufWogRFSNYuULDC3EHTAcWYFASnbCo1kVS81eqnwyt")
    
    def generate_payment_reference(self, length=12):
        """Generate a unique payment reference ID"""
        chars = string.ascii_uppercase + string.digits
        return 'TJ-' + ''.join(random.choice(chars) for _ in range(length))
    
    async def create_payment_request(self, user_id, service_type, amount=None):
        """
        Create a payment request for a service
        
        Args:
            user_id: User's Discord ID
            service_type: Type of service (e.g., hit, dose, junkified)
            amount: Optional override for the payment amount
            
        Returns:
            dict: Payment request details
        """
        # Determine amount based on service type
        if not amount:
            if service_type in SUBSCRIPTION_TIERS:
                amount = SUBSCRIPTION_TIERS[service_type]["price"]
            else:
                # Default price for unknown service types
                amount = 5.0  # $5 default
        
        # Generate reference ID
        reference = self.generate_payment_reference()
        
        # Save to database
        if self.db:
            self.db.save_payment_request(user_id, amount, reference, service_type)
        
        # Return payment details
        return {
            "user_id": user_id,
            "amount": amount,
            "reference": reference,
            "service_type": service_type,
            "wallet_address": self.wallet_address,
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
    
    async def verify_payment(self, reference, tx_signature=None):
        """
        Verify a payment using the reference ID and optionally a transaction signature
        
        Args:
            reference: Payment reference ID
            tx_signature: Optional Solana transaction signature
            
        Returns:
            dict: Payment verification result
        """
        if not self.db:
            return {"success": False, "message": "Database not available"}
        
        # Get payment request
        payment = self.db.get_payment_by_reference(reference)
        
        if not payment:
            return {"success": False, "message": "Payment reference not found"}
        
        # If already verified, return success
        if payment["status"] == "completed":
            return {"success": True, "message": "Payment already verified", "payment": payment}
        
        # In a real implementation, we would verify the transaction on the Solana blockchain
        # For now, we'll simulate verification with a 80% success rate
        verification_successful = tx_signature is not None or random.random() < 0.8
        
        if verification_successful:
            # Update payment status
            self.db.update_payment_status(reference, "completed", tx_signature)
            
            # Update user tier based on service type
            user_id = payment["user_id"]
            service_type = payment["service_type"]
            
            if service_type in SUBSCRIPTION_TIERS:
                tier_info = SUBSCRIPTION_TIERS[service_type]
                
                # Calculate expiration date if applicable
                expires_at = None
                if tier_info["duration_days"] > 0:
                    expires_at = (datetime.now() + timedelta(days=tier_info["duration_days"])).isoformat()
                
                # Update user tier
                self.db.update_user_tier(user_id, service_type, expires_at)
            
            # Process referral commission if applicable
            self.process_referral_commission(payment)
            
            # Get updated payment
            updated_payment = self.db.get_payment_by_reference(reference)
            
            return {
                "success": True, 
                "message": "Payment verified successfully", 
                "payment": updated_payment,
                "tier_updated": True,
                "service_type": service_type
            }
        else:
            return {"success": False, "message": "Payment verification failed"}
    
    def process_referral_commission(self, payment):
        """
        Process referral commission for a completed payment
        
        Args:
            payment: The completed payment
        """
        if not self.db:
            return
        
        try:
            user_id = payment["user_id"]
            amount = payment["amount"]
            payment_id = payment["id"]
            
            # Check if the user was referred by someone
            referrer = self.db.get_referrer_for_user(user_id)
            
            if referrer:
                # Calculate commission (25% of payment amount)
                commission_amount = round(amount * 0.25, 2)
                
                # Record the commission
                self.db.record_commission(payment_id, referrer["referrer_id"], commission_amount)
                
                logger.info(f"Recorded commission of {commission_amount} SOL for referrer {referrer['referrer_id']}")
        except Exception as e:
            logger.error(f"Error processing referral commission: {str(e)}")
    
    async def get_user_payments(self, user_id, status=None):
        """
        Get payments for a user
        
        Args:
            user_id: User's Discord ID
            status: Optional filter by payment status
            
        Returns:
            list: User's payments
        """
        if not self.db:
            return []
        
        return self.db.get_user_payments(user_id, status)
    
    async def get_user_tier(self, user_id):
        """
        Get a user's subscription tier
        
        Args:
            user_id: User's Discord ID
            
        Returns:
            dict: User's tier information
        """
        if not self.db:
            return {"tier": "free", "expires_at": None}
        
        tier_info = self.db.get_user_tier(user_id)
        
        if not tier_info or not tier_info["tier"]:
            return {"tier": "free", "expires_at": None}
        
        # Check if tier has expired
        if tier_info["expires_at"]:
            expires_at = datetime.fromisoformat(tier_info["expires_at"])
            
            if expires_at < datetime.now():
                # Tier has expired, reset to free
                self.db.update_user_tier(user_id, "free", None)
                return {"tier": "free", "expires_at": None}
        
        # Add tier features
        tier_name = tier_info["tier"]
        if tier_name in SUBSCRIPTION_TIERS:
            tier_info["features"] = SUBSCRIPTION_TIERS[tier_name]["features"]
            tier_info["name"] = SUBSCRIPTION_TIERS[tier_name]["name"]
            tier_info["limits"] = {
                "hit": SUBSCRIPTION_TIERS[tier_name].get("daily_hit_limit", 0),
                "dose": SUBSCRIPTION_TIERS[tier_name].get("daily_dose_limit", 0),
                "trip": SUBSCRIPTION_TIERS[tier_name].get("daily_trip_limit", 0)
            }
        
        return tier_info


# For testing
async def main():
    """Main function for testing"""
    processor = PaymentProcessor()
    
    # Create payment request
    payment = await processor.create_payment_request("123456789", "junkified")
    print(f"Payment request created: {payment}")
    
    # Verify payment
    verification = await processor.verify_payment(payment["reference"], "simulated_tx_signature")
    print(f"Payment verification: {verification}")


if __name__ == "__main__":
    asyncio.run(main())