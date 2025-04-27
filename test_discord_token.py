#!/usr/bin/env python
"""
Test Discord Token
Simple script to verify the Discord bot token is properly set
"""
import os
import sys
from dotenv import load_dotenv

def main():
    """Main function"""
    # Load environment variables
    load_dotenv()
    
    # Check if Discord token is available
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ DISCORD_BOT_TOKEN not found in environment variables")
        print("Please set DISCORD_BOT_TOKEN in the .env file")
        return 1
    
    # Print token length and first/last few characters
    token_length = len(token)
    token_preview = f"{token[:4]}...{token[-4:]}"
    print(f"✅ DISCORD_BOT_TOKEN found (length: {token_length}, preview: {token_preview})")
    return 0

if __name__ == "__main__":
    sys.exit(main())