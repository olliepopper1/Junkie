import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Ensure database URL is set
if not os.environ.get("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite:///trial_junkie.db"

# Import app after setting environment variables
from app import app  # noqa: F401

# This is the main entry point for the Flask web application