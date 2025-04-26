"""
Payment Agent (Crypto Craig)
Handles Solana payments for Trial Junkie services
"""
import logging
import os
import json
import time
import random
from datetime import datetime, timedelta
from config import ADMIN_WALLET, COLORS, PRICES

logger = logging.getLogger(__name__)

class PaymentAgent:
    """Agent for handling Solana payments"""
    
    def __init__(self, db):
        """Initialize the payment agent"""
        self.db = db
        self.name = "Crypto Craig"
        self.admin_wallet = ADMIN_WALLET  # Admin wallet to receive payments
        
        # Setup payment tracking
        self.pending_payments = {}  # {user_id: {'amount': amount, 'timestamp': timestamp, 'reference': reference}}
        
        logger.info(f"{self.name} initialized")
    
    async def create_payment(self, user_id, username, service_type):
        """
        Create a payment request for a service
        
        Args:
            user_id (str): Discord user ID
            username (str): Discord username
            service_type (str): Type of service (hit, dose, trip, premium)
        
        Returns:
            dict: Payment information including amount and wallet address
        """
        logger.info(f"{self.name} creating payment for {username} ({service_type})")
        
        # Get price for service
        if service_type not in PRICES:
            raise ValueError(f"Unknown service type: {service_type}")
        
        amount = PRICES[service_type]
        
        # Create a unique reference for this payment
        reference = f"TJ-{user_id[:8]}-{int(time.time())}"
        
        # Store payment request in pending payments
        self.pending_payments[user_id] = {
            'amount': amount,
            'timestamp': datetime.now(),
            'reference': reference,
            'service_type': service_type,
            'status': 'pending'
        }
        
        # Store payment request in database
        if hasattr(self.db, 'save_payment_request'):
            self.db.save_payment_request(
                user_id=user_id,
                amount=amount,
                reference=reference,
                service_type=service_type
            )
        
        # Return payment details
        return {
            'amount': amount,
            'wallet': self.admin_wallet,
            'reference': reference,
            'timestamp': datetime.now().isoformat(),
            'expires': (datetime.now() + timedelta(hours=24)).isoformat()  # Extended to 24 hours for manual verification
        }
    
    async def check_payment(self, user_id, reference=None):
        """
        Check if a payment has been received
        For this simplified version, we'll manually mark payments as complete 
        when users report they've sent the payment
        
        Args:
            user_id (str): Discord user ID
            reference (str, optional): Payment reference ID
        
        Returns:
            bool: Whether the payment has been received
        """
        logger.info(f"{self.name} checking payment for user {user_id}")
        
        # For demo, we'll simulate a successful payment about 30% of the time
        # In a real implementation, you would verify on the blockchain
        # Or manually mark payments as complete after confirming the transaction
        success = random.random() < 0.3
        
        if success:
            # If reference not provided, get from pending payments
            if not reference and user_id in self.pending_payments:
                reference = self.pending_payments[user_id]['reference']
            
            if not reference:
                # No reference found, can't mark a specific payment
                return False
                
            # Get pending payment details
            payment = self.pending_payments.get(user_id)
            if not payment:
                logger.warning(f"No pending payment found for user {user_id}")
                return False
                
            # Mark payment as successful
            self.pending_payments[user_id]["status"] = "completed"
            
            # Store in database
            if hasattr(self.db, 'update_payment_status'):
                self.db.update_payment_status(
                    reference=reference,
                    status="completed",
                    tx_signature=f"demo-tx-{random.randint(10000, 99999)}"
                )
            
            logger.info(f"Payment {reference} marked as completed for demo")
            return True
        
        return False
    
    async def verify_transaction(self, transaction_id=None):
        """
        Simplified verification 
        
        Args:
            transaction_id (str, optional): Solana transaction ID or user report
        
        Returns:
            dict: Basic verification outcome
        """
        logger.info(f"{self.name} verifying transaction (simplified)")
        
        # For demo, we'll return simple verification data
        return {
            "success": True,
            "message": "Transaction reported by user",
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_payment_status(self, user_id):
        """
        Get the current payment status for a user
        
        Args:
            user_id (str): Discord user ID
        
        Returns:
            dict: Payment status information
        """
        logger.info(f"{self.name} getting payment status for user {user_id}")
        
        if user_id not in self.pending_payments:
            return {
                'status': 'no_payment',
                'message': 'No pending payment found'
            }
        
        payment = self.pending_payments[user_id]
        
        # Check if payment has expired (24 hours)
        if (datetime.now() - payment['timestamp']).total_seconds() > 86400:  # 24 hours
            return {
                'status': 'expired',
                'message': 'Payment request has expired'
            }
        
        # Check if payment has been received
        if payment['status'] == 'completed':
            return {
                'status': 'completed',
                'message': 'Payment has been received'
            }
        
        # Payment is still pending
        time_left = 86400 - (datetime.now() - payment['timestamp']).total_seconds()
        return {
            'status': 'pending',
            'message': f'Waiting for payment of {payment["amount"]} SOL',
            'time_left': int(time_left),
            'reference': payment['reference']
        }
    
    async def process_manual_payment(self, user_id, reference=None):
        """
        Manually process a payment that a user says they've sent
        
        Args:
            user_id (str): Discord user ID
            reference (str, optional): Payment reference ID
        
        Returns:
            bool: Whether the payment was successfully processed
        """
        logger.info(f"{self.name} manually processing payment for user {user_id}")
        
        # If reference not provided, get from pending payments
        if not reference and user_id in self.pending_payments:
            reference = self.pending_payments[user_id]['reference']
        
        if not reference:
            logger.warning(f"No payment reference found for user {user_id}")
            return False
            
        # Get pending payment details
        payment = self.pending_payments.get(user_id)
        if not payment:
            logger.warning(f"No pending payment found for user {user_id}")
            return False
            
        # Mark payment as successful
        self.pending_payments[user_id]["status"] = "completed"
        
        # Store in database
        if hasattr(self.db, 'update_payment_status'):
            self.db.update_payment_status(
                reference=reference,
                status="completed",
                tx_signature=f"manual-{random.randint(10000, 99999)}"
            )
        
        logger.info(f"Payment {reference} manually marked as completed")
        return True
    
    async def cancel_payment(self, user_id):
        """
        Cancel a pending payment
        
        Args:
            user_id (str): Discord user ID
        
        Returns:
            bool: Whether the payment was successfully canceled
        """
        logger.info(f"{self.name} canceling payment for user {user_id}")
        
        if user_id not in self.pending_payments:
            return False
        
        payment = self.pending_payments[user_id]
        
        # Update database if needed
        if hasattr(self.db, 'update_payment_status'):
            self.db.update_payment_status(
                reference=payment['reference'],
                status="canceled"
            )
        
        # Remove from pending payments
        del self.pending_payments[user_id]
        
        return True