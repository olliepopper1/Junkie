#!/usr/bin/env python3
"""
Database Module for Trial Junkie

This module provides database connectivity and operations for the Trial Junkie application
"""
import os
import json
import logging
import sqlite3
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("database")

class Database:
    """
    Database connection and operations for Trial Junkie
    
    This class handles database connections and provides methods for
    storing and retrieving data related to trials, users, and payments.
    """
    
    def __init__(self):
        """Initialize the database connection"""
        logger.info("Initializing database")
        
        # Check if we have a PostgreSQL connection string
        db_url = os.environ.get("DATABASE_URL", "")
        
        if db_url.startswith("postgresql"):
            self.db_type = "postgres"
            self.connection = self._connect_postgres(db_url)
        else:
            self.db_type = "sqlite"
            if db_url.startswith("sqlite"):
                # Extract path from SQLite URL if provided
                sqlite_path = db_url.replace("sqlite:///", "")
                self.connection = self._connect_sqlite(sqlite_path)
            else:
                self.connection = self._connect_sqlite()
        
        # Initialize database schema if needed
        self._initialize_schema()
        
        logger.info("Database initialized successfully")
    
    def _connect_postgres(self, db_url=None):
        """Connect to PostgreSQL database"""
        logger.info("Connecting to PostgreSQL database")
        
        try:
            connection = psycopg2.connect(db_url or os.environ.get("DATABASE_URL"))
            return connection
        except Exception as e:
            logger.error(f"Error connecting to PostgreSQL: {e}")
            raise
    
    def _connect_sqlite(self, db_path=None):
        """Connect to SQLite database"""
        logger.info("Connecting to SQLite database")
        
        try:
            # Create the data directory if it doesn't exist
            if not db_path:
                os.makedirs("data", exist_ok=True)
                db_path = "data/trialjunkie.db"
                
            # Connect to the database file
            connection = sqlite3.connect(db_path)
            connection.row_factory = sqlite3.Row  # Return rows as dictionaries
            
            return connection
        except Exception as e:
            logger.error(f"Error connecting to SQLite: {e}")
            raise
    
    def _initialize_schema(self):
        """Initialize database schema if needed"""
        logger.info("Initializing database schema")
        
        try:
            cursor = self.connection.cursor()
            
            # Create the trials table if it doesn't exist
            if self.db_type == "postgres":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS trials (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(50) NOT NULL,
                        service VARCHAR(50) NOT NULL,
                        creation_date TIMESTAMP NOT NULL,
                        expiration_date TIMESTAMP NOT NULL,
                        trial_data JSONB NOT NULL
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS trials (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        service TEXT NOT NULL,
                        creation_date TEXT NOT NULL,
                        expiration_date TEXT NOT NULL,
                        trial_data TEXT NOT NULL
                    )
                """)
            
            self.connection.commit()
            cursor.close()
            
        except Exception as e:
            logger.error(f"Error initializing schema: {e}")
            raise
    
    def insert_trial(self, user_id, trial_data):
        """
        Insert a trial into the database
        
        Args:
            user_id (str): The user ID
            trial_data (dict): The trial data
            
        Returns:
            int: The ID of the inserted trial
        """
        logger.info(f"Inserting trial for user {user_id}")
        
        try:
            cursor = self.connection.cursor()
            
            # Extract values from trial data
            service = trial_data.get("service", "unknown")
            creation_date = trial_data.get("creation_date", datetime.now().isoformat())
            expiration_date = trial_data.get("expiration_date", "")
            
            # Convert trial data to JSON string for storage
            trial_data_json = json.dumps(trial_data)
            
            # Insert the trial
            if self.db_type == "postgres":
                cursor.execute("""
                    INSERT INTO trials (user_id, service, creation_date, expiration_date, trial_data)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (user_id, service, creation_date, expiration_date, trial_data_json))
                trial_id = cursor.fetchone()[0]
            else:
                cursor.execute("""
                    INSERT INTO trials (user_id, service, creation_date, expiration_date, trial_data)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, service, creation_date, expiration_date, trial_data_json))
                trial_id = cursor.lastrowid
            
            self.connection.commit()
            cursor.close()
            
            logger.info(f"Trial inserted with ID {trial_id}")
            return trial_id
            
        except Exception as e:
            logger.error(f"Error inserting trial: {e}")
            self.connection.rollback()
            raise
    
    def get_user_trials(self, user_id):
        """
        Get all trials for a user
        
        Args:
            user_id (str): The user ID
            
        Returns:
            list: A list of trial dictionaries
        """
        logger.info(f"Getting trials for user {user_id}")
        
        try:
            cursor = self.connection.cursor()
            
            # Get all trials for the user
            if self.db_type == "postgres":
                cursor.execute("""
                    SELECT id, service, creation_date, expiration_date, trial_data
                    FROM trials
                    WHERE user_id = %s
                    ORDER BY creation_date DESC
                """, (user_id,))
                
                # Use RealDictCursor for row dictionaries
                trials = []
                for row in cursor.fetchall():
                    trial = {
                        "id": row[0],
                        "service": row[1],
                        "creation_date": row[2],
                        "expiration_date": row[3],
                        **json.loads(row[4])
                    }
                    trials.append(trial)
                    
            else:
                cursor.execute("""
                    SELECT id, service, creation_date, expiration_date, trial_data
                    FROM trials
                    WHERE user_id = ?
                    ORDER BY creation_date DESC
                """, (user_id,))
                
                # SQLite Row Factory returns dictionaries
                trials = []
                for row in cursor.fetchall():
                    trial = {
                        "id": row["id"],
                        "service": row["service"],
                        "creation_date": row["creation_date"],
                        "expiration_date": row["expiration_date"],
                        **json.loads(row["trial_data"])
                    }
                    trials.append(trial)
            
            cursor.close()
            
            logger.info(f"Found {len(trials)} trials for user {user_id}")
            return trials
            
        except Exception as e:
            logger.error(f"Error getting user trials: {e}")
            raise
    
    def get_trial(self, trial_id):
        """
        Get a specific trial by ID
        
        Args:
            trial_id (int): The trial ID
            
        Returns:
            dict: The trial data
        """
        logger.info(f"Getting trial with ID {trial_id}")
        
        try:
            cursor = self.connection.cursor()
            
            # Get the trial
            if self.db_type == "postgres":
                cursor.execute("""
                    SELECT id, user_id, service, creation_date, expiration_date, trial_data
                    FROM trials
                    WHERE id = %s
                """, (trial_id,))
                
                row = cursor.fetchone()
                if row:
                    trial = {
                        "id": row[0],
                        "user_id": row[1],
                        "service": row[2],
                        "creation_date": row[3],
                        "expiration_date": row[4],
                        **json.loads(row[5])
                    }
                else:
                    trial = None
                    
            else:
                cursor.execute("""
                    SELECT id, user_id, service, creation_date, expiration_date, trial_data
                    FROM trials
                    WHERE id = ?
                """, (trial_id,))
                
                row = cursor.fetchone()
                if row:
                    trial = {
                        "id": row["id"],
                        "user_id": row["user_id"],
                        "service": row["service"],
                        "creation_date": row["creation_date"],
                        "expiration_date": row["expiration_date"],
                        **json.loads(row["trial_data"])
                    }
                else:
                    trial = None
            
            cursor.close()
            
            if trial:
                logger.info(f"Found trial with ID {trial_id}")
            else:
                logger.warning(f"No trial found with ID {trial_id}")
                
            return trial
            
        except Exception as e:
            logger.error(f"Error getting trial: {e}")
            raise
    
    def close(self):
        """Close the database connection"""
        logger.info("Closing database connection")
        
        try:
            self.connection.close()
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")

def test_database():
    """Test the database module"""
    logger.info("Testing database module")
    
    # Initialize the database
    db = Database()
    
    # Generate test data
    test_user_id = "test_user_123"
    test_trial = {
        "service": "test_service",
        "success": True,
        "creation_date": datetime.now().isoformat(),
        "expiration_date": datetime.now().isoformat(),
        "login_credentials": {
            "email": "test@example.com",
            "password": "test_password"
        },
        "account_details": {
            "first_name": "Test",
            "last_name": "User",
            "plan": "Test Plan",
            "price": "$9.99/month",
            "trial_length": "30 days"
        }
    }
    
    # Insert the test trial
    trial_id = db.insert_trial(test_user_id, test_trial)
    logger.info(f"Inserted test trial with ID {trial_id}")
    
    # Get the trial by ID
    retrieved_trial = db.get_trial(trial_id)
    logger.info(f"Retrieved trial: {retrieved_trial['service']}")
    
    # Get all trials for the user
    user_trials = db.get_user_trials(test_user_id)
    logger.info(f"User has {len(user_trials)} trials")
    
    # Close the connection
    db.close()
    
    return True

if __name__ == "__main__":
    test_database()