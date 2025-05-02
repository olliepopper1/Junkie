#!/usr/bin/env python3
"""
Hulu Trial Fetcher
Quick script to get the most recent Hulu trial
"""
import sys
from trial_storage import TrialStorage

def get_latest_hulu_trial(user_id):
    """Get the most recent Hulu trial for a user"""
    storage = TrialStorage()
    trials = storage.get_user_trials(user_id, service="Hulu")
    
    if not trials:
        print("No Hulu trials found for this user")
        return None
    
    # Return the most recent trial (they're already sorted by created_at DESC)
    return trials[0]

def display_trial(trial):
    """Display trial information in a clean format"""
    print("=== HULU TRIAL INFORMATION ===")
    print(f"Email: {trial['email']}")
    print(f"Password: {trial['password']}")
    print(f"Plan: {trial['plan']}")
    print(f"Card: {trial['payment_method']}")
    print(f"Expires: {trial['expiry_date']}")
    print(f"Login at: https://www.hulu.com/login")
    print("\nRemember to cancel before the trial ends to avoid being charged.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_hulu_trial.py <user_id>")
        sys.exit(1)
    
    user_id = sys.argv[1]
    print(f"Getting latest Hulu trial for user {user_id}...")
    
    trial = get_latest_hulu_trial(user_id)
    if trial:
        display_trial(trial)