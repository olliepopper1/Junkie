#!/usr/bin/env python
"""
Get User Trials
Command-line script to retrieve trials for a user from the bot database
"""
import sys
import argparse
from bot_api_helpers import BotAPI
import json

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Get trials for a user')
    parser.add_argument('--user_id', required=True, help='User ID')
    
    args = parser.parse_args()
    
    api = BotAPI()
    result = api.get_user_trials(args.user_id)
    
    # Output as JSON
    print(json.dumps(result))
    return 0

if __name__ == "__main__":
    sys.exit(main())