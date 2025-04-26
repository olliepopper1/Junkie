"""
Payment Agent (Crypto Craig)
Handles Solana payments for Trial Junkie services
"""
import logging
import os
import json
import asyncio
import time
from datetime import datetime, timedelta
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.system_program import SYS_PROGRAM_ID, TransferParams, transfer
from config import ADMIN_WALLET, COLORS, PRICES

logger = logging.getLogger(__name__)

class PaymentAgent:
    """Agent for handling Solana payments"""
    
    def __init__(self, db):
        """Initialize the payment agent"""
        self.db = db
        self.name = "Crypto Craig"
        self.client = Client(os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com"))
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
            service_type (str): Type of service (hit, dose, trip)
        
        Returns:
            dict: Payment information including amount and wallet address
        """
        logger.info(f"{self.name} creating payment for {username} ({service_type})")
        
        # Get price for service
        if service_type not in PRICES:
            raise ValueError(f"Unknown service type: {service_type}")
        
        amount = PRICES[service_type]
        
        # Create a unique reference for this payment
        reference = f"TJ-{user_id}-{int(time.time())}"
        
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
            'expires': (datetime.now() + timedelta(hours=1)).isoformat()
        }
    
    async def check_payment(self, user_id, reference=None):
        """
        Check if a payment has been received
        
        Args:
            user_id (str): Discord user ID
            reference (str, optional): Payment reference ID
        
        Returns:
            bool: Whether the payment has been received
        """
        logger.info(f"{self.name} checking payment for user {user_id}")
        
        # If reference not provided, get from pending payments
        if not reference and user_id in self.pending_payments:
            reference = self.pending_payments[user_id]['reference']
        
        if not reference:
            raise ValueError("No payment reference provided or found")
        
        # Get pending payment details
        payment = self.pending_payments.get(user_id)
        if not payment:
            logger.warning(f"No pending payment found for user {user_id}")
            return False
        
        # Check for transactions to admin wallet in the last 30 minutes
        # In a real implementation, we would check the memo field for the reference
        
        try:
            # Get recent signatures for admin wallet
            signatures = self.client.get_signatures_for_address(
                PublicKey(self.admin_wallet),
                limit=10
            )
            
            if "result" not in signatures:
                logger.error(f"Error getting signatures: {signatures}")
                return False
            
            # For each signature, get transaction and check if it's from this user
            for sig_info in signatures["result"]:
                tx_response = self.client.get_transaction(sig_info["signature"])
                
                # Parse transaction data 
                # Note: In a real implementation, we would check the memo field for the reference
                # and verify the amount matches
                
                # For demo purposes, we'll just check if any payment came in recently
                # and mark it as success (this is not secure, just for demo)
                tx_time = datetime.fromtimestamp(tx_response["result"]["blockTime"])
                if (datetime.now() - tx_time).total_seconds() < 1800:  # 30 minutes
                    # Mark payment as successful
                    self.pending_payments[user_id]["status"] = "completed"
                    
                    # Store in database
                    if hasattr(self.db, 'update_payment_status'):
                        self.db.update_payment_status(
                            reference=reference,
                            status="completed",
                            tx_signature=sig_info["signature"]
                        )
                    
                    logger.info(f"Payment {reference} completed")
                    return True
            
            # No matching transaction found
            return False
            
        except Exception as e:
            logger.error(f"Error checking payment: {str(e)}")
            return False
    
    async def verify_transaction(self, transaction_id):
        """
        Verify if a transaction exists and is valid
        
        Args:
            transaction_id (str): Solana transaction ID
        
        Returns:
            dict: Transaction details if valid, None otherwise
        """
        logger.info(f"{self.name} verifying transaction {transaction_id}")
        
        try:
            transaction = self.client.get_transaction(transaction_id)
            
            if "result" not in transaction or not transaction["result"]:
                logger.warning(f"Transaction {transaction_id} not found")
                return None
            
            # Check if transaction is a success
            if not transaction["result"]["meta"]["status"]["Ok"]:
                logger.warning(f"Transaction {transaction_id} failed")
                return None
            
            return transaction["result"]
            
        except Exception as e:
            logger.error(f"Error verifying transaction: {str(e)}")
            return None
    
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
        
        # Check if payment has expired (1 hour)
        if (datetime.now() - payment['timestamp']).total_seconds() > 3600:
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
        time_left = 3600 - (datetime.now() - payment['timestamp']).total_seconds()
        return {
            'status': 'pending',
            'message': f'Waiting for payment of {payment["amount"]} SOL',
            'time_left': int(time_left),
            'reference': payment['reference']
        }
    
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