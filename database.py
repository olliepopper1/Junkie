#!/usr/bin/env python3
"""
Database Module for Trial Junkie
Handles database connections and operations
"""
import os
import sys
import json
import logging
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("database.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("database")

class Database:
    """
    Database connection and operations handler
    Supports both PostgreSQL and SQLite backends
    """
    def __init__(self, db_url: str = None):
        """
        Initialize the database handler
        
        Args:
            db_url: Database URL (defaults to DATABASE_URL environment variable)
        """
        self.db_url = db_url or os.getenv("DATABASE_URL")
        self.connection = None
        self.db_type = None
        
        logger.info("Initializing database")
    
    def initialize(self) -> Dict[str, Any]:
        """
        Initialize the database connection
        
        Returns:
            dict: Initialization result
        """
        if not self.db_url:
            return {
                "success": False,
                "message": "No database URL provided"
            }
        
        # Determine database type
        if self.db_url.startswith("postgresql://") or self.db_url.startswith("postgres://"):
            return self._initialize_postgres()
        elif self.db_url.startswith("sqlite://"):
            return self._initialize_sqlite()
        else:
            return {
                "success": False,
                "message": f"Unsupported database type: {self.db_url.split('://')[0]}"
            }
    
    def _initialize_postgres(self) -> Dict[str, Any]:
        """
        Initialize PostgreSQL database connection
        
        Returns:
            dict: Initialization result
        """
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            
            logger.info("Connecting to PostgreSQL database")
            
            self.connection = psycopg2.connect(self.db_url)
            self.connection.autocommit = True
            self.db_type = "postgres"
            
            # Test the connection
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                logger.info(f"Connected to PostgreSQL: {version}")
            
            # Initialize schema
            self._initialize_schema()
            
            return {
                "success": True,
                "message": "PostgreSQL connection established",
                "db_type": self.db_type
            }
        
        except ImportError:
            return {
                "success": False,
                "message": "psycopg2 module not available"
            }
        except Exception as e:
            logger.error(f"PostgreSQL connection error: {str(e)}")
            traceback.print_exc()
            return {
                "success": False,
                "message": str(e)
            }
    
    def _initialize_sqlite(self) -> Dict[str, Any]:
        """
        Initialize SQLite database connection
        
        Returns:
            dict: Initialization result
        """
        try:
            import sqlite3
            
            # Parse SQLite URL
            db_path = self.db_url.replace("sqlite:///", "")
            
            logger.info(f"Connecting to SQLite database: {db_path}")
            
            self.connection = sqlite3.connect(db_path)
            self.connection.row_factory = sqlite3.Row
            self.db_type = "sqlite"
            
            # Test the connection
            cursor = self.connection.cursor()
            cursor.execute("SELECT sqlite_version();")
            version = cursor.fetchone()[0]
            logger.info(f"Connected to SQLite: {version}")
            
            # Initialize schema
            self._initialize_schema()
            
            return {
                "success": True,
                "message": "SQLite connection established",
                "db_type": self.db_type
            }
        
        except Exception as e:
            logger.error(f"SQLite connection error: {str(e)}")
            traceback.print_exc()
            return {
                "success": False,
                "message": str(e)
            }
    
    def _initialize_schema(self) -> None:
        """Initialize the database schema if tables don't exist"""
        logger.info("Initializing database schema")
        
        # Define the schema based on database type
        if self.db_type == "postgres":
            # PostgreSQL schema
            schema = """
            -- Users table
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                discord_id VARCHAR(255) UNIQUE,
                username VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Trials table
            CREATE TABLE IF NOT EXISTS trials (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                service VARCHAR(255),
                plan VARCHAR(255),
                email VARCHAR(255),
                password VARCHAR(255),
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                phone VARCHAR(255),
                start_date DATE,
                end_date DATE,
                card_details JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Payments table
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                amount DECIMAL(10, 2),
                currency VARCHAR(10),
                status VARCHAR(50),
                payment_method VARCHAR(100),
                reference VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Referrals table
            CREATE TABLE IF NOT EXISTS referrals (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                referral_code VARCHAR(50) UNIQUE,
                referred_by INTEGER REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- User tiers table
            CREATE TABLE IF NOT EXISTS user_tier (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) UNIQUE,
                tier VARCHAR(50),
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Commissions table
            CREATE TABLE IF NOT EXISTS commissions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                referral_id INTEGER REFERENCES referrals(id),
                amount DECIMAL(10, 2),
                status VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            
            # Execute each statement separately
            with self.connection.cursor() as cursor:
                for statement in schema.split(';'):
                    if statement.strip():
                        cursor.execute(statement)
        
        elif self.db_type == "sqlite":
            # SQLite schema
            schema = """
            -- Users table
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_id TEXT UNIQUE,
                username TEXT,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Trials table
            CREATE TABLE IF NOT EXISTS trials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id),
                service TEXT,
                plan TEXT,
                email TEXT,
                password TEXT,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                start_date DATE,
                end_date DATE,
                card_details TEXT,  -- JSON string in SQLite
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Payments table
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id),
                amount REAL,
                currency TEXT,
                status TEXT,
                payment_method TEXT,
                reference TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Referrals table
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id),
                referral_code TEXT UNIQUE,
                referred_by INTEGER REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- User tiers table
            CREATE TABLE IF NOT EXISTS user_tier (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id) UNIQUE,
                tier TEXT,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Commissions table
            CREATE TABLE IF NOT EXISTS commissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id),
                referral_id INTEGER REFERENCES referrals(id),
                amount REAL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            
            # Execute each statement separately
            cursor = self.connection.cursor()
            for statement in schema.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            self.connection.commit()
        
        logger.info("Database initialized successfully")
    
    def create_user(self, discord_id: str = None, username: str = None, 
                   email: str = None) -> Dict[str, Any]:
        """
        Create a new user
        
        Args:
            discord_id: Discord user ID
            username: Username
            email: Email address
            
        Returns:
            dict: User creation result
        """
        try:
            # Determine database type and execute appropriate query
            if self.db_type == "postgres":
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (discord_id, username, email) VALUES (%s, %s, %s) RETURNING id",
                        (discord_id, username, email)
                    )
                    user_id = cursor.fetchone()[0]
            else:  # SQLite
                cursor = self.connection.cursor()
                cursor.execute(
                    "INSERT INTO users (discord_id, username, email) VALUES (?, ?, ?)",
                    (discord_id, username, email)
                )
                self.connection.commit()
                user_id = cursor.lastrowid
            
            return {
                "success": True,
                "user_id": user_id,
                "message": "User created successfully"
            }
        
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return {
                "success": False,
                "message": str(e)
            }
    
    def save_trial(self, user_id: int, trial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a trial to the database
        
        Args:
            user_id: User ID
            trial_data: Trial data
            
        Returns:
            dict: Trial saving result
        """
        try:
            # Extract trial fields
            service = trial_data.get("service")
            plan = trial_data.get("plan")
            email = trial_data.get("email")
            password = trial_data.get("password")
            first_name = trial_data.get("first_name")
            last_name = trial_data.get("last_name")
            phone = trial_data.get("phone")
            start_date = trial_data.get("start_date")
            end_date = trial_data.get("end_date")
            
            # Handle card details based on database type
            if self.db_type == "postgres":
                card_details = json.dumps(trial_data.get("card_details", {}))
                
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO trials 
                        (user_id, service, plan, email, password, first_name, last_name, 
                        phone, start_date, end_date, card_details) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
                        RETURNING id
                        """,
                        (user_id, service, plan, email, password, first_name, last_name,
                        phone, start_date, end_date, card_details)
                    )
                    trial_id = cursor.fetchone()[0]
            else:  # SQLite
                card_details = json.dumps(trial_data.get("card_details", {}))
                
                cursor = self.connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO trials 
                    (user_id, service, plan, email, password, first_name, last_name, 
                    phone, start_date, end_date, card_details) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (user_id, service, plan, email, password, first_name, last_name,
                    phone, start_date, end_date, card_details)
                )
                self.connection.commit()
                trial_id = cursor.lastrowid
            
            return {
                "success": True,
                "trial_id": trial_id,
                "message": "Trial saved successfully"
            }
        
        except Exception as e:
            logger.error(f"Error saving trial: {str(e)}")
            traceback.print_exc()
            return {
                "success": False,
                "message": str(e)
            }
    
    def get_user_trials(self, user_id: int) -> Dict[str, Any]:
        """
        Get all trials for a user
        
        Args:
            user_id: User ID
            
        Returns:
            dict: User trials result
        """
        try:
            if self.db_type == "postgres":
                from psycopg2.extras import RealDictCursor
                
                with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        """
                        SELECT * FROM trials
                        WHERE user_id = %s
                        ORDER BY created_at DESC
                        """,
                        (user_id,)
                    )
                    trials = cursor.fetchall()
                    
                    # Convert JSON strings to dictionaries
                    for trial in trials:
                        if "card_details" in trial and trial["card_details"]:
                            if isinstance(trial["card_details"], str):
                                trial["card_details"] = json.loads(trial["card_details"])
                            
                            # Convert dates to strings
                            if "start_date" in trial and trial["start_date"]:
                                trial["start_date"] = trial["start_date"].strftime("%Y-%m-%d")
                            if "end_date" in trial and trial["end_date"]:
                                trial["end_date"] = trial["end_date"].strftime("%Y-%m-%d")
            else:  # SQLite
                cursor = self.connection.cursor()
                cursor.execute(
                    """
                    SELECT * FROM trials
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    """,
                    (user_id,)
                )
                rows = cursor.fetchall()
                
                # Convert rows to dictionaries
                trials = []
                for row in rows:
                    trial = dict(zip([column[0] for column in cursor.description], row))
                    
                    # Convert JSON strings to dictionaries
                    if "card_details" in trial and trial["card_details"]:
                        trial["card_details"] = json.loads(trial["card_details"])
                    
                    trials.append(trial)
            
            return {
                "success": True,
                "trials": trials,
                "count": len(trials)
            }
        
        except Exception as e:
            logger.error(f"Error getting user trials: {str(e)}")
            traceback.print_exc()
            return {
                "success": False,
                "message": str(e),
                "trials": []
            }
    
    def close(self) -> None:
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def __del__(self) -> None:
        """Destructor to ensure connection is closed"""
        self.close()

# For standalone testing
if __name__ == "__main__":
    db = Database()
    result = db.initialize()
    
    if result.get("success", False):
        print(f"Database connection successful: {result.get('db_type')}")
        
        # Test creating a user
        user_result = db.create_user(
            discord_id="123456789", 
            username="test_user", 
            email="test@example.com"
        )
        
        if user_result.get("success", False):
            user_id = user_result.get("user_id")
            print(f"User created with ID: {user_id}")
            
            # Test saving a trial
            trial_data = {
                "service": "test_service",
                "plan": "test_plan",
                "email": "trial@example.com",
                "password": "password123",
                "first_name": "Test",
                "last_name": "User",
                "phone": "123-456-7890",
                "start_date": "2025-01-01",
                "end_date": "2025-01-31",
                "card_details": {
                    "type": "visa",
                    "number": "4111111111111111",
                    "expiry": "12/28",
                    "cvv": "123",
                    "last4": "1111"
                }
            }
            
            trial_result = db.save_trial(user_id, trial_data)
            
            if trial_result.get("success", False):
                print(f"Trial saved with ID: {trial_result.get('trial_id')}")
                
                # Test getting user trials
                trials_result = db.get_user_trials(user_id)
                
                if trials_result.get("success", False):
                    print(f"Found {trials_result.get('count')} trials for user {user_id}")
                else:
                    print(f"Error getting trials: {trials_result.get('message')}")
            else:
                print(f"Error saving trial: {trial_result.get('message')}")
        else:
            print(f"Error creating user: {user_result.get('message')}")
    else:
        print(f"Database connection failed: {result.get('message')}")
    
    db.close()