#!/usr/bin/env python
"""
Get Bot Trials
Bridge script to retrieve bot-generated trials from the database
"""
import os
import sys
import json
import argparse
import logging
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

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Get trials for a user')
    parser.add_argument('--user_id', required=True, help='Discord user ID')
    
    args = parser.parse_args()
    
    try:
        # Connect to the database
        db = Database()
        
        # Convert user_id to integer if it's numeric
        try:
            user_id = int(args.user_id)
        except ValueError:
            user_id = args.user_id
        
        # Get user credentials
        credentials = db.get_user_credentials(user_id)
        
        # Process credentials and format as trials
        trials = []
        
        if credentials:
            # Group credentials by service
            service_map = {}
            for cred in credentials:
                service = cred['service']
                if service not in service_map:
                    service_map[service] = []
                service_map[service].append(cred)
            
            # Format each service group as a trial
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
        
        # Return the trials as JSON
        print(json.dumps({
            'success': True,
            'user_id': user_id,
            'trials': trials
        }))
        
    except Exception as e:
        logger.error(f"Error getting trials: {str(e)}")
        print(json.dumps({
            'success': False,
            'error': str(e)
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()