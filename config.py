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
    "phone": "Cokehead Carl"      # SMS/Phone verification
}

# Colors for embeds
COLORS = {
    "success": 0x4CAF50,  # Green
    "error": 0xF44336,    # Red
    "warning": 0xFFC107,  # Yellow
    "info": 0x2196F3      # Blue
}

# API endpoints
ENDPOINTS = {
    "random_user": "https://random-user-generator.p.rapidapi.com/api",
    "random_phone": "https://random-phone-number.p.rapidapi.com/api/phone/random",
    "fake_card": "https://fake-credit-card-generator.p.rapidapi.com/api/fake-credit-card-generator"
}

# RapidAPI host names
RAPIDAPI_HOSTS = {
    "random_user": "random-user-generator.p.rapidapi.com",
    "random_phone": "random-phone-number.p.rapidapi.com",
    "fake_card": "fake-credit-card-generator.p.rapidapi.com"
}

# Proxy settings
PROXY_ENABLED = os.getenv("PROXY_ENABLED", "False").lower() == "true"

# Default headers for API requests
DEFAULT_HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "Content-Type": "application/json"
}
