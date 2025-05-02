"""
Trial Junkie Database Module
Handles database connections and operations
"""
import os
import json
import logging
import sqlite3
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("database")

class Database:
    """
    Database interface for Trial Junkie system
    Handles both SQLite (for development) and PostgreSQL (for production)
    """
    
    def __init__(self):
        self.db_type = "postgresql"  # Default to PostgreSQL
        self.connection_pool = None
        self.db_path = "instance/database.db"  # SQLite path for fallback
        
        # Try to get PostgreSQL connection info from environment
        self.db_url = os.getenv("DATABASE_URL")
        self.db_host = os.getenv("PGHOST")
        self.db_port = os.getenv("PGPORT")
        self.db_user = os.getenv("PGUSER")
        self.db_pass = os.getenv("PGPASSWORD")
        self.db_name = os.getenv("PGDATABASE")
        
        # If no PostgreSQL info available, fallback to SQLite
        if not (self.db_url or (self.db_host and self.db_port and self.db_user and self.db_name)):
            self.db_type = "sqlite"
            logger.warning("No PostgreSQL credentials found, falling back to SQLite")
    
    def initialize(self):
        """
        Initialize the database connection and schema
        Returns:
            dict: Connection status information
        """
        logger.info("Initializing database")
        
        try:
            if self.db_type == "postgresql":
                return self._init_postgresql()
            else:
                return self._init_sqlite()
        except Exception as e:
            logger.error(f"Database initialization error: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def _init_postgresql(self):
        """
        Initialize PostgreSQL database
        """
        logger.info("Connecting to PostgreSQL database")
        
        try:
            # Use the DATABASE_URL if available, otherwise construct from components
            if self.db_url:
                # Create a connection pool with 5 connections
                self.connection_pool = pool.SimpleConnectionPool(
                    1, 5, self.db_url
                )
            else:
                # Create a connection pool with component params
                self.connection_pool = pool.SimpleConnectionPool(
                    1, 5,
                    host=self.db_host,
                    port=self.db_port,
                    user=self.db_user,
                    password=self.db_pass,
                    dbname=self.db_name
                )
            
            # Get a connection to create tables
            conn = self.connection_pool.getconn()
            conn.autocommit = True
            cursor = conn.cursor()
            
            logger.info("Initializing database schema")
            self._create_tables_postgresql(cursor)
            
            # Return connection to the pool
            self.connection_pool.putconn(conn)
            
            logger.info("Database initialized successfully")
            return {"success": True, "message": "PostgreSQL database initialized successfully"}
            
        except psycopg2.Error as e:
            logger.error(f"PostgreSQL error: {str(e)}")
            return {"success": False, "message": f"PostgreSQL error: {str(e)}"}
        except Exception as e:
            logger.error(f"Error initializing PostgreSQL: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def _init_sqlite(self):
        """
        Initialize SQLite database
        """
        logger.info("Connecting to SQLite database")
        
        try:
            # Make sure the instance directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # Create a connection
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            logger.info("Initializing database schema")
            self._create_tables_sqlite(cursor)
            
            conn.commit()
            conn.close()
            
            logger.info("Database initialized successfully")
            return {"success": True, "message": "SQLite database initialized successfully"}
            
        except sqlite3.Error as e:
            logger.error(f"SQLite error: {str(e)}")
            return {"success": False, "message": f"SQLite error: {str(e)}"}
        except Exception as e:
            logger.error(f"Error initializing SQLite: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def _create_tables_postgresql(self, cursor):
        """
        Create PostgreSQL tables if they don't exist
        """
        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(64) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(256),
            wallet_address VARCHAR(64),
            tier VARCHAR(20) DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Create trials table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trials (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            service VARCHAR(64) NOT NULL,
            plan VARCHAR(64) NOT NULL,
            email VARCHAR(120) NOT NULL,
            password VARCHAR(64) NOT NULL,
            first_name VARCHAR(64),
            last_name VARCHAR(64),
            address TEXT,
            city VARCHAR(64),
            state VARCHAR(32),
            zipcode VARCHAR(16),
            phone VARCHAR(32),
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            card_type VARCHAR(32),
            card_last4 VARCHAR(4),
            trial_data JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        
        # Create payments table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount DECIMAL(10, 6) NOT NULL,
            currency VARCHAR(10) DEFAULT 'SOL',
            payment_type VARCHAR(32) NOT NULL,
            transaction_id VARCHAR(128),
            status VARCHAR(32) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        
        # Create referrals table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            id SERIAL PRIMARY KEY,
            referrer_id INTEGER NOT NULL,
            referred_id INTEGER NOT NULL,
            referral_code VARCHAR(32) NOT NULL,
            status VARCHAR(32) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referrer_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (referred_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        
        # Create commissions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS commissions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount DECIMAL(10, 6) NOT NULL,
            currency VARCHAR(10) DEFAULT 'SOL',
            source_id INTEGER,
            status VARCHAR(32) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (source_id) REFERENCES users(id) ON DELETE SET NULL
        );
        """)
    
    def _create_tables_sqlite(self, cursor):
        """
        Create SQLite tables if they don't exist
        """
        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            wallet_address TEXT,
            tier TEXT DEFAULT 'free',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Create trials table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service TEXT NOT NULL,
            plan TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zipcode TEXT,
            phone TEXT,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            card_type TEXT,
            card_last4 TEXT,
            trial_data TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        
        # Create payments table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'SOL',
            payment_type TEXT NOT NULL,
            transaction_id TEXT,
            status TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        
        # Create referrals table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER NOT NULL,
            referred_id INTEGER NOT NULL,
            referral_code TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referrer_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (referred_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        
        # Create commissions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS commissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'SOL',
            source_id INTEGER,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (source_id) REFERENCES users(id) ON DELETE SET NULL
        );
        """)
    
    def get_connection(self):
        """
        Get a database connection
        
        Returns:
            conn: Database connection object
        """
        if self.db_type == "postgresql":
            # Get connection from pool
            if self.connection_pool:
                return self.connection_pool.getconn()
            else:
                logger.error("Connection pool not initialized")
                return None
        else:
            # Create SQLite connection
            return sqlite3.connect(self.db_path)
    
    def release_connection(self, conn):
        """
        Release a database connection
        
        Args:
            conn: Database connection to release
        """
        if self.db_type == "postgresql" and self.connection_pool:
            self.connection_pool.putconn(conn)
        else:
            conn.close()
    
    def save_trial(self, user_id, trial_data):
        """
        Save a trial to the database
        
        Args:
            user_id: The user ID to associate with the trial
            trial_data: Dictionary containing trial information
            
        Returns:
            dict: Result with success status and message
        """
        try:
            conn = self.get_connection()
            if not conn:
                return {"success": False, "message": "Could not get database connection"}
            
            if self.db_type == "postgresql":
                cursor = conn.cursor()
                
                # Extract data from trial_data
                service = trial_data.get("service", "unknown")
                plan = trial_data.get("plan", "standard")
                email = trial_data.get("email", "")
                password = trial_data.get("password", "")
                first_name = trial_data.get("first_name", "")
                last_name = trial_data.get("last_name", "")
                address = trial_data.get("address", "")
                city = trial_data.get("city", "")
                state = trial_data.get("state", "")
                zipcode = trial_data.get("zipcode", "")
                phone = trial_data.get("phone", "")
                start_date = trial_data.get("start_date", datetime.now().strftime("%Y-%m-%d"))
                end_date = trial_data.get("end_date", "")
                
                # Card info may be nested
                card_details = trial_data.get("card_details", {})
                if isinstance(card_details, str):
                    try:
                        card_details = json.loads(card_details)
                    except:
                        card_details = {}
                
                card_type = card_details.get("type", trial_data.get("card_type", ""))
                card_last4 = card_details.get("last4", trial_data.get("card_last4", ""))
                
                # Store the full trial data as JSON
                trial_json = json.dumps(trial_data)
                
                # Insert into database
                cursor.execute("""
                INSERT INTO trials 
                (user_id, service, plan, email, password, first_name, last_name, 
                address, city, state, zipcode, phone, start_date, end_date, 
                card_type, card_last4, trial_data)
                VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """, (
                    user_id, service, plan, email, password, first_name, last_name,
                    address, city, state, zipcode, phone, start_date, end_date,
                    card_type, card_last4, trial_json
                ))
                
                trial_id = cursor.fetchone()[0]
                conn.commit()
                
            else:
                cursor = conn.cursor()
                
                # Extract data from trial_data
                service = trial_data.get("service", "unknown")
                plan = trial_data.get("plan", "standard")
                email = trial_data.get("email", "")
                password = trial_data.get("password", "")
                first_name = trial_data.get("first_name", "")
                last_name = trial_data.get("last_name", "")
                address = trial_data.get("address", "")
                city = trial_data.get("city", "")
                state = trial_data.get("state", "")
                zipcode = trial_data.get("zipcode", "")
                phone = trial_data.get("phone", "")
                start_date = trial_data.get("start_date", datetime.now().strftime("%Y-%m-%d"))
                end_date = trial_data.get("end_date", "")
                
                # Card info may be nested
                card_details = trial_data.get("card_details", {})
                if isinstance(card_details, str):
                    try:
                        card_details = json.loads(card_details)
                    except:
                        card_details = {}
                
                card_type = card_details.get("type", trial_data.get("card_type", ""))
                card_last4 = card_details.get("last4", trial_data.get("card_last4", ""))
                
                # Store the full trial data as JSON
                trial_json = json.dumps(trial_data)
                
                # Insert into database
                cursor.execute("""
                INSERT INTO trials 
                (user_id, service, plan, email, password, first_name, last_name, 
                address, city, state, zipcode, phone, start_date, end_date, 
                card_type, card_last4, trial_data)
                VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id, service, plan, email, password, first_name, last_name,
                    address, city, state, zipcode, phone, start_date, end_date,
                    card_type, card_last4, trial_json
                ))
                
                trial_id = cursor.lastrowid
                conn.commit()
            
            self.release_connection(conn)
            
            logger.info(f"Trial saved successfully with ID {trial_id}")
            return {"success": True, "message": "Trial saved successfully", "trial_id": trial_id}
            
        except Exception as e:
            logger.error(f"Error saving trial: {str(e)}")
            if conn:
                self.release_connection(conn)
            return {"success": False, "message": f"Database error: {str(e)}"}
    
    def get_user_trials(self, user_id, limit=10):
        """
        Get trials for a specific user
        
        Args:
            user_id: The user ID to get trials for
            limit: Maximum number of trials to return
            
        Returns:
            list: List of trials for the user
        """
        try:
            conn = self.get_connection()
            if not conn:
                return []
            
            if self.db_type == "postgresql":
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                # Get trials from database
                cursor.execute("""
                SELECT * FROM trials 
                WHERE user_id = %s 
                ORDER BY created_at DESC 
                LIMIT %s
                """, (user_id, limit))
                
                trials = cursor.fetchall()
                
            else:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Get trials from database
                cursor.execute("""
                SELECT * FROM trials 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
                """, (user_id, limit))
                
                trials = [dict(row) for row in cursor.fetchall()]
            
            self.release_connection(conn)
            
            # Process trials if needed (e.g., parse trial_data JSON)
            for trial in trials:
                if 'trial_data' in trial and trial['trial_data']:
                    try:
                        if isinstance(trial['trial_data'], str):
                            trial['trial_data'] = json.loads(trial['trial_data'])
                    except:
                        pass
            
            return trials
            
        except Exception as e:
            logger.error(f"Error getting user trials: {str(e)}")
            if conn:
                self.release_connection(conn)
            return []
    
    def close(self):
        """Close all database connections"""
        if self.db_type == "postgresql" and self.connection_pool:
            self.connection_pool.closeall()
            logger.info("All database connections closed")

# Run standalone test
if __name__ == "__main__":
    print("Testing database connection...")
    db = Database()
    result = db.initialize()
    print(f"Initialization result: {result}")
    
    if result.get('success'):
        print("\nTesting trial saving...")
        test_trial = {
            "service": "test_service",
            "plan": "premium",
            "email": "test@example.com",
            "password": "testpassword",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d"),
            "card_details": {
                "type": "visa",
                "last4": "1234"
            }
        }
        save_result = db.save_trial(1, test_trial)
        print(f"Save result: {save_result}")
        
        print("\nTesting trial retrieval...")
        trials = db.get_user_trials(1)
        print(f"Found {len(trials)} trials for user 1")
        
    db.close()