#!/usr/bin/env python3
"""
Use Real Trial
Helper script to use a real trial account on Hulu
"""
import json
import sys
import webbrowser
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_latest_trial():
    """Get the latest trial information"""
    try:
        with open("standalone_hulu_trial.json", "r") as f:
            trial = json.load(f)
        return trial
    except Exception as e:
        logger.error(f"Error loading trial data: {e}")
        return None

def display_trial_instructions(trial):
    """Display detailed instructions for using this trial account"""
    print("\n" + "="*50)
    print("REAL HULU TRIAL ACCOUNT INSTRUCTIONS")
    print("="*50)
    print("\nAccount Information:")
    print(f"Email: {trial['email']}")
    print(f"Password: {trial['password']}")
    print(f"Plan: {trial['plan']} ({trial['price']})")
    print(f"Payment Method: {trial['card']}")
    print(f"Trial Expiration: {trial['end_date']}")
    
    print("\nHow to Use This Account:")
    print("1. Go to https://www.hulu.com/login")
    print("2. Enter the email address and password above")
    print("3. Click the 'Log In' button")
    print("4. You now have access to Hulu with the No Ads plan!")
    
    print("\nIMPORTANT NOTES:")
    print("• This is a real Hulu account with a valid trial subscription")
    print("• The credentials were created using our trial generation system")
    print("• To prevent charges, cancel before the trial end date")
    print("• To cancel: Account > Cancel Your Subscription")
    print("• This account may be shared with other Trial Junkie users")
    
    print("\nHulu login page: https://www.hulu.com/login")
    
    print("\nEnjoy your Hulu trial!")

def create_login_html(trial):
    """Create an HTML file with login details that can be opened in a browser"""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Hulu Trial Login Information</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1ce783;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}
        .credentials {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #1ce783;
        }}
        .label {{
            font-weight: bold;
            color: #555;
        }}
        .value {{
            font-family: monospace;
            font-size: 16px;
            background: #eee;
            padding: 3px 6px;
            border-radius: 3px;
        }}
        .button {{
            display: inline-block;
            background: #1ce783;
            color: black;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin-top: 15px;
        }}
        .notes {{
            background: #fff8e1;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            border-left: 4px solid #ffc107;
        }}
        .notes h3 {{
            margin-top: 0;
            color: #ff6d00;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Hulu Trial Login Information</h1>
        
        <div class="credentials">
            <p><span class="label">Email:</span> <span class="value">{trial['email']}</span></p>
            <p><span class="label">Password:</span> <span class="value">{trial['password']}</span></p>
            <p><span class="label">Plan:</span> {trial['plan']} ({trial['price']})</p>
            <p><span class="label">Payment Method:</span> {trial['card']}</p>
            <p><span class="label">Trial Expiration:</span> {trial['end_date']}</p>
            
            <a href="https://www.hulu.com/login" target="_blank" class="button">Log In to Hulu</a>
        </div>
        
        <div class="notes">
            <h3>Important Notes</h3>
            <ul>
                <li>This is a real Hulu account with a valid trial subscription</li>
                <li>The credentials were created using our trial generation system</li>
                <li>To prevent charges, cancel before the trial end date</li>
                <li>To cancel: Account &gt; Cancel Your Subscription</li>
                <li>This account may be shared with other Trial Junkie users</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
    
    # Save the HTML file
    filename = "hulu_trial_login.html"
    with open(filename, "w") as f:
        f.write(html_content)
    
    print(f"\nCreated login information HTML file: {filename}")
    print(f"You can open this file in any browser to see your login details.")
    
    # Try to open it in the browser
    try:
        file_path = os.path.abspath(filename)
        file_url = f"file://{file_path}"
        webbrowser.open(file_url)
    except:
        pass
    
    return filename

if __name__ == "__main__":
    print("=== Use Real Hulu Trial ===")
    
    # Load the latest trial
    trial = get_latest_trial()
    
    if not trial:
        print("No trial information found!")
        print("Please generate a trial first by running:")
        print("  python simplified_hulu_trial.py")
        sys.exit(1)
    
    # Display account information
    print(f"\nLatest Hulu trial found:")
    print(f"Email: {trial['email']}")
    print(f"Password: {trial['password']}")
    
    # Display detailed instructions
    display_trial_instructions(trial)
    
    # Create HTML file with login details
    create_login_html(trial)