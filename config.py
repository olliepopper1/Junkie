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
    "tier": 60,             # 1 minute for tier status
    "referral": 30,         # 30 seconds for referral code 
    "refer": 10,            # 10 seconds for using a referral code
    "commissions": 30       # 30 seconds for commission status
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
    # Identity generation - Personator API
    "personator": "https://personator.p.rapidapi.com/v1/generate",
    
    # Phone generation - Virtual Number API
    "virtual_number": "https://virtual-number.p.rapidapi.com/v1/numbers",
    
    # Card generation - Fake Valid CC Data Generator
    "fake_card": "https://fake-valid-cc-data-generator.p.rapidapi.com/v1/card/generate",
    
    # Free trial Virtual Card API for payment methods
    "virtual_card": "https://free-trial-virtual-card-issuing.p.rapidapi.com/v1/generate",
    
    # Email generation - Fast & Reliable Disposable Email
    "temp_email": "https://fast-reliable-disposable-mx-email-checker.p.rapidapi.com/v1/email/generate",
    
    # Temp Mail API as backup for email verification
    "temp_mail_backup": "https://temp-mail.p.rapidapi.com/v1/mail/create"
}

# Supported trial services with configuration
TRIAL_SERVICES = {
    "hulu": {
        "url": "https://www.hulu.com/",
        "trial_period_days": 30,
        "price": "$14.99/month",
        "plan_name": "Hulu (No Ads)",
        "required_fields": ["identity", "email", "card", "phone"],
        "supports_automation": True,
        "cancellation_path": "Account > Cancel Subscription"
    },
    "netflix": {
        "url": "https://www.netflix.com/",
        "trial_period_days": 30,
        "price": "$15.49/month",
        "plan_name": "Netflix Standard",
        "required_fields": ["identity", "email", "card"],
        "supports_automation": True,
        "cancellation_path": "Account > Cancel Membership"
    },
    "disney": {
        "url": "https://www.disneyplus.com/",
        "trial_period_days": 7,
        "price": "$10.99/month",
        "plan_name": "Disney+ Premium",
        "required_fields": ["identity", "email", "card"],
        "supports_automation": True,
        "cancellation_path": "Profile > Account > Cancel Subscription"
    },
    "spotify": {
        "url": "https://www.spotify.com/",
        "trial_period_days": 30,
        "price": "$10.99/month",
        "plan_name": "Spotify Premium",
        "required_fields": ["identity", "email", "card"],
        "supports_automation": True,
        "cancellation_path": "Account > Subscription > Cancel Premium"
    },
    "amazon": {
        "url": "https://www.amazon.com/",
        "trial_period_days": 30,
        "price": "$14.99/month",
        "plan_name": "Amazon Prime",
        "required_fields": ["identity", "email", "card"],
        "supports_automation": True,
        "cancellation_path": "Account > Prime > Manage Membership > End Membership"
    },
    "youtube": {
        "url": "https://www.youtube.com/premium",
        "trial_period_days": 30,
        "price": "$13.99/month",
        "plan_name": "YouTube Premium",
        "required_fields": ["identity", "email", "card"],
        "supports_automation": True,
        "cancellation_path": "Account > Memberships > Cancel Membership"
    },
    "paramount": {
        "url": "https://www.paramountplus.com/",
        "trial_period_days": 7,
        "price": "$11.99/month",
        "plan_name": "Paramount+ Essential",
        "required_fields": ["identity", "email", "card"],
        "supports_automation": True,
        "cancellation_path": "Account > Cancel Subscription"
    },
    "apple": {
        "url": "https://www.apple.com/apple-tv-plus/",
        "trial_period_days": 7,
        "price": "$9.99/month",
        "plan_name": "Apple TV+",
        "required_fields": ["identity", "email", "card", "apple_id"],
        "supports_automation": True,
        "cancellation_path": "Settings > Apple ID > Subscriptions > Apple TV+ > Cancel"
    },
    "hbomax": {
        "url": "https://www.max.com/",
        "trial_period_days": 7,
        "price": "$15.99/month",
        "plan_name": "Max Ad-Free",
        "required_fields": ["identity", "email", "card"],
        "supports_automation": True,
        "cancellation_path": "Account > Billing Information > Cancel Subscription"
    },
    "peacock": {
        "url": "https://www.peacocktv.com/",
        "trial_period_days": 7,
        "price": "$11.99/month",
        "plan_name": "Peacock Premium Plus",
        "required_fields": ["identity", "email", "card"],
        "supports_automation": True,
        "cancellation_path": "Account > Plans & Payment > Cancel Plan"
    }
}

# API host settings for RapidAPI
API_HOSTS = {
    "personator": "personator.p.rapidapi.com",
    "virtual_number": "virtual-number.p.rapidapi.com",
    "fake_card": "fake-valid-cc-data-generator.p.rapidapi.com",
    "virtual_card": "free-trial-virtual-card-issuing.p.rapidapi.com",
    "temp_email": "fast-reliable-disposable-mx-email-checker.p.rapidapi.com",
    "temp_mail_backup": "temp-mail.p.rapidapi.com"
}

# Proxy settings
PROXY_ENABLED = os.getenv("PROXY_ENABLED", "False").lower() == "true"

# Default headers for regular API requests
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "TrialJunkie/1.0.0"
}

# Browser automation settings
AUTOMATION_SETTINGS = {
    "enabled": True,  # Enable real browser automation for trial creation
    "screenshots_path": "screenshots",  # Path to save screenshots during automation
    "timeout": 30,  # Default timeout in seconds for waiting for elements
    "headless": True,  # Run browser in headless mode (no UI)
    "use_real_user_data": False,  # Whether to use real user data for trials
    "generic_service_enabled": True  # Enable automatic handling of any website
}

# Default trial site categories for automation - used for custom sites
GENERIC_SITE_PATTERNS = {
    "streaming": ["netflix", "hulu", "disney", "stream", "watch", "tv", "video", "movie"],
    "shopping": ["shop", "store", "amazon", "buy", "cart", "checkout", "retail"],
    "music": ["music", "audio", "listen", "spotify", "sound", "song", "track"],
    "productivity": ["work", "office", "software", "cloud", "storage", "document", "productivity"],
    "gaming": ["game", "play", "gaming", "console", "steam", "xbox", "playstation"],
    "education": ["learn", "course", "class", "education", "study", "tutorial", "teach"],
    "finance": ["bank", "money", "finance", "invest", "trading", "crypto", "payment"],
    "other": []  # Default category
}
