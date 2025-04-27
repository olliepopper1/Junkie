#!/usr/bin/env python
"""
Execute Bot Command
Bridge script to execute Discord bot commands from the web API
"""
import os
import sys
import json
import argparse
import logging
from database import Database
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Execute a Discord bot command')
    parser.add_argument('--command', required=True, help='Command to execute')
    parser.add_argument('--user_id', required=True, help='Discord user ID')
    parser.add_argument('--username', required=True, help='Discord username')
    parser.add_argument('--params', required=False, default='{}', help='JSON string of command parameters')
    
    args = parser.parse_args()
    
    try:
        # Parse parameters
        params = json.loads(args.params)
        
        # Connect to the database
        db = Database()
        
        # Log the command
        logger.info(f"Executing command: {args.command} for user {args.username} ({args.user_id})")
        
        # Convert user_id to integer if it's numeric
        try:
            user_id = int(args.user_id)
        except ValueError:
            user_id = args.user_id
            
        # Execute the command
        if args.command == 'get_user_data':
            # Check if user exists, create if not
            if not db.user_exists(user_id):
                db.create_user(user_id, args.username)
            
            # Get user stats
            stats = db.get_user_stats(user_id)
            
            print(json.dumps({
                'success': True,
                'user_id': user_id,
                'username': args.username,
                'stats': stats
            }))
            
        elif args.command == 'get_credentials':
            service = params.get('service')
            
            # Get user credentials
            credentials = db.get_user_credentials(user_id, service)
            
            print(json.dumps({
                'success': True,
                'user_id': user_id,
                'service': service,
                'credentials': credentials
            }))
            
        elif args.command == 'clear_user_data':
            # Clear user data
            db.clear_user_data(user_id)
            
            print(json.dumps({
                'success': True,
                'user_id': user_id,
                'message': 'User data cleared successfully'
            }))
            
        elif args.command == 'get_payments':
            status = params.get('status')
            
            # Get user payments
            payments = db.get_user_payments(user_id, status)
            
            print(json.dumps({
                'success': True,
                'user_id': user_id,
                'payments': payments
            }))
            
        elif args.command == 'get_tier':
            # Get user tier
            tier = db.get_user_tier(user_id)
            
            print(json.dumps({
                'success': True,
                'user_id': user_id,
                'tier': tier
            }))
            
        elif args.command == 'get_referrals':
            # Get referral code
            referral_code = db.get_referral_code(user_id)
            
            # Get referred users
            referrals = db.get_user_referrals(user_id)
            
            print(json.dumps({
                'success': True,
                'user_id': user_id,
                'referral_code': referral_code,
                'referrals': referrals
            }))
            
        elif args.command == 'get_commissions':
            status = params.get('status')
            
            # Get commissions
            commissions = db.get_user_commissions(user_id, status)
            total = db.get_total_commission(user_id)
            
            print(json.dumps({
                'success': True,
                'user_id': user_id,
                'commissions': commissions,
                'total_commission': total
            }))
            
        else:
            # Unknown command
            print(json.dumps({
                'success': False,
                'error': f'Unknown command: {args.command}'
            }))
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error executing command: {str(e)}")
        print(json.dumps({
            'success': False,
            'error': str(e)
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()