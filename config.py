"""
Configuration module for Trial Junkie
Loads and provides access to environment variables and constants
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")

# Database settings
DATABASE_PATH = os.getenv("DATABASE_PATH", "trial_junkie.db")

# Cooldown settings (in seconds)
COOLDOWNS = {
    "hit": 300,             # 5 minutes
    "dose": 60,             # 1 minute
    "trip": 600,            # 10 minutes
    "rehab": 3600,          # 1 hour
    "pay": 30,              # 30 seconds for payment commands
    "verify_payment": 10,   # 10 seconds for payment verification
    "payments": 60,         # 1 minute for payment history
    "tier": 60              # 1 minute for tier status
}

# Agent names and themes
AGENT_NAMES = {
    "harry": "Heroin Harry",      # Identity generation
    "mandy": "Meth Mandy",        # Card generation
    "xan": "Xanny Xan",           # Email generation
    "sal": "Shroomy Sal",         # Browser automation
    "carl": "Cokehead Carl",      # SMS/Phone verification
    "craig": "Crypto Craig"       # Payment processing
}

# Colors for embeds
COLORS = {
    "success": 0x4CAF50,  # Green
    "error": 0xF44336,    # Red
    "warning": 0xFFC107,  # Yellow
    "info": 0x2196F3,     # Blue
    "payment": 0x9C27B0   # Purple
}

# Payment settings
ADMIN_WALLET = os.getenv("SOLANA_WALLET_ADDRESS", "J5ufWogRFSNYuULDC3EHTAcWYFASnbCo1kVS81eqnwyt")
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")

# Pricing in SOL
PRICES = {
    "hit": 0.01,       # Full trial creation costs 0.01 SOL
    "dose": 0.005,     # Single agent usage costs 0.005 SOL
    "trip": 0.02,      # Automation script costs 0.02 SOL
    "premium": 0.1,    # Premium membership monthly fee costs 0.1 SOL
    "one_time_hit": 0.0,    # Free plan - no cost
    "five_dollar_rush": 0.036,  # $5 in SOL (approx.)
    "junkified": 0.093     # $13 in SOL (approx.)
}

# Trial service tiers
SERVICE_TIERS = {
    "free": {
        "daily_limit": 3,
        "description": "Basic free tier with limited daily usage"
    },
    "paid": {
        "daily_limit": 15,
        "description": "Pay-per-use tier with higher limits"
    },
    "premium": {
        "daily_limit": 50,
        "description": "Premium tier with high daily limits and priority support"
    },
    "one_time_hit": {
        "daily_limit": 1,
        "description": "A quick blast of freedom, no strings attached",
        "features": ["One-time free trial", "No credit card required", "Basic features only"]
    },
    "five_dollar_rush": {
        "daily_limit": 25,
        "description": "A rush of power for just five bucks",
        "features": ["Limited-time access", "Multiple trials per day", "Standard features"]
    },
    "junkified": {
        "daily_limit": 100,
        "description": "Unlock unlimited possibilities—no limits, just freedom",
        "features": ["Unlimited access", "Priority support", "All premium features", "No daily limits"]
    }
}

# API endpoints - All using RapidAPI services
ENDPOINTS = {
    # Identity generation
    "random_user": "https://random-user-generator.p.rapidapi.com/api",
    
    # Phone generation
    "random_phone": "https://random-phone-number.p.rapidapi.com/api/phone/random",
    
    # Card generation
    "fake_card": "https://fake-credit-card-generator.p.rapidapi.com/api/fake-credit-card-generator",
    
    # Email generation (using random user API for consistency)
    "temp_email": "https://temp-mail44.p.rapidapi.com/api/v3/email/new",
    
    # Additional endpoints for potential expansion
    "address_generator": "https://random-address-generator.p.rapidapi.com/api",
    "currency_converter": "https://currency-converter18.p.rapidapi.com/api/v1/convert"
}

# RapidAPI host names
RAPIDAPI_HOSTS = {
    "random_user": "random-user-generator.p.rapidapi.com",
    "random_phone": "random-phone-number.p.rapidapi.com",
    "fake_card": "fake-credit-card-generator.p.rapidapi.com",
    "temp_email": "temp-mail44.p.rapidapi.com",
    "address_generator": "random-address-generator.p.rapidapi.com",
    "currency_converter": "currency-converter18.p.rapidapi.com"
}

# Proxy settings
PROXY_ENABLED = os.getenv("PROXY_ENABLED", "False").lower() == "true"

# Default headers for API requests
DEFAULT_HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "Content-Type": "application/json"
}
