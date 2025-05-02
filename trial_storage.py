"""
Trial Storage Module
Simplified storage for trial data
"""
import json
import sqlite3
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TrialStorage:
    """
    Simple storage for trial data using SQLite
    """
    def __init__(self, db_path="trial_data.db"):
        """Initialize the storage with database connection"""
        self.db_path = db_path
        self.initialize_db()
    
    def get_connection(self):
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def initialize_db(self):
        """Initialize the database with required tables"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create users table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    username TEXT,
                    created_at TEXT,
                    last_active TEXT
                )
            ''')
            
            # Create trials table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    service TEXT NOT NULL,
                    email TEXT,
                    password TEXT,
                    plan TEXT,
                    payment_method TEXT,
                    expiry_date TEXT,
                    status TEXT,
                    created_at TEXT,
                    trial_data TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Trial storage database initialized")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def get_or_create_user(self, user_id, username=None):
        """Get or create a user entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            # Create new user
            now = datetime.now().isoformat()
            username = username or f"user_{user_id}"
            
            cursor.execute(
                "INSERT INTO users (user_id, username, created_at, last_active) VALUES (?, ?, ?, ?)",
                (user_id, username, now, now)
            )
            conn.commit()
            
            logger.info(f"Created user: {username} ({user_id})")
            # Get the newly created user
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
        else:
            # Update last active
            now = datetime.now().isoformat()
            cursor.execute(
                "UPDATE users SET last_active = ? WHERE user_id = ?",
                (now, user_id)
            )
            conn.commit()
        
        result = dict(user) if user else None
        conn.close()
        return result
    
    def save_trial(self, user_id, trial_data):
        """
        Save trial information to the database
        
        Args:
            user_id: User ID to save the trial for
            trial_data: Dictionary containing trial information
            
        Returns:
            int: ID of the newly created trial record
        """
        try:
            # Ensure user exists
            self.get_or_create_user(user_id)
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            now = datetime.now().isoformat()
            
            # Extract key fields from trial data
            email = trial_data.get('email', '')
            password = trial_data.get('password', '')
            service = trial_data.get('service', '')
            plan = trial_data.get('plan', '')
            payment_method = trial_data.get('card', '')
            expiry_date = trial_data.get('end_date', '')
            status = trial_data.get('status', 'Active')
            
            # Serialize full trial data as JSON
            trial_json = json.dumps(trial_data)
            
            cursor.execute(
                """
                INSERT INTO trials 
                (user_id, service, email, password, plan, payment_method, expiry_date, status, created_at, trial_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, service, email, password, plan, payment_method, expiry_date, status, now, trial_json)
            )
            
            trial_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            logger.info(f"Saved {service} trial for user {user_id}")
            return trial_id
        except Exception as e:
            logger.error(f"Error saving trial: {e}")
            return None
    
    def get_user_trials(self, user_id, service=None):
        """
        Get all trials for a user, optionally filtered by service
        
        Args:
            user_id: User ID to get trials for
            service: Optional service name to filter by
            
        Returns:
            list: List of trial dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM trials WHERE user_id = ?"
        params = [user_id]
        
        if service:
            query += " AND service = ?"
            params.append(service)
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        trials = []
        for row in rows:
            # Convert row to dictionary
            trial = dict(row)
            
            # Parse the full trial data
            if trial.get('trial_data'):
                try:
                    trial['full_data'] = json.loads(trial['trial_data'])
                except json.JSONDecodeError:
                    trial['full_data'] = {}
            
            trials.append(trial)
        
        conn.close()
        return trials

# Test the storage if run directly
if __name__ == "__main__":
    # Example usage
    storage = TrialStorage()
    
    # Test user
    test_user_id = "test_user_789"
    
    # Example trial data
    test_trial = {
        "service": "Hulu",
        "plan": "Hulu (No Ads)",
        "price": "$14.99/month",
        "status": "Active",
        "trial": True,
        "email": "test.user@example.com",
        "password": "SecurePassword123",
        "name": "Test User",
        "card": "Visa **** **** **** 1234",
        "start_date": "2025-05-02",
        "end_date": "2025-06-01",
        "days_remaining": 30
    }
    
    # Save the trial
    print(f"Saving trial for user {test_user_id}...")
    trial_id = storage.save_trial(test_user_id, test_trial)
    
    if trial_id:
        print(f"Trial saved successfully with ID {trial_id}")
        
        # Retrieve the user's trials
        print(f"Retrieving trials for user {test_user_id}...")
        trials = storage.get_user_trials(test_user_id)
        
        print(f"Found {len(trials)} trials:")
        for trial in trials:
            print(f"  - {trial['service']} ({trial['plan']}): {trial['email']} / {trial['password']}")
            print(f"    Expires: {trial['expiry_date']}")
    else:
        print("Failed to save trial")