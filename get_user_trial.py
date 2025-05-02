"""
User Trial Fetcher
Retrieves trial information for a specific user
"""
import argparse
import logging
import sys
from trial_storage import TrialStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("user_trials.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def get_user_trials(user_id, service=None):
    """
    Get all trials for a user, optionally filtered by service
    
    Args:
        user_id (str): The user ID to retrieve trials for
        service (str, optional): Filter by service name
        
    Returns:
        list: List of trials
    """
    storage = TrialStorage()
    trials = storage.get_user_trials(user_id, service)
    return trials

def display_trials(trials):
    """Display trial information in a human-readable format"""
    if not trials:
        print("No trials found")
        return
    
    print(f"Found {len(trials)} trials:\n")
    
    for i, trial in enumerate(trials):
        print(f"Trial #{i+1}:")
        print(f"  Service: {trial['service']}")
        print(f"  Plan: {trial['plan']}")
        print(f"  Login: {trial['email']} / {trial['password']}")
        print(f"  Payment: {trial['payment_method']}")
        print(f"  Expires: {trial['expiry_date']}")
        print(f"  Status: {trial['status']}")
        print(f"  Created: {trial['created_at']}")
        print("")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve trial information for a user")
    parser.add_argument("--user_id", required=True, help="User ID to retrieve trials for")
    parser.add_argument("--service", help="Filter by service name (optional)")
    
    args = parser.parse_args()
    
    print(f"Getting trials for user {args.user_id}")
    if args.service:
        print(f"Filtering by service: {args.service}")
    
    trials = get_user_trials(args.user_id, args.service)
    display_trials(trials)