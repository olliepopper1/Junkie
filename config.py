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
    "hit": 300,        # 5 minutes
    "dose": 60,        # 1 minute
    "trip": 600,       # 10 minutes
    "rehab": 3600      # 1 hour
}

# Agent names and themes
AGENT_NAMES = {
    "harry": "Heroin Harry",      # Identity generation
    "mandy": "Meth Mandy",        # Card generation
    "xan": "Xanny Xan",           # Email generation
    "sal": "Shroomy Sal",         # Browser automation
    "carl": "Cokehead Carl"       # SMS/Phone verification
}

# Colors for embeds
COLORS = {
    "success": 0x4CAF50,  # Green
    "error": 0xF44336,    # Red
    "warning": 0xFFC107,  # Yellow
    "info": 0x2196F3      # Blue
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
