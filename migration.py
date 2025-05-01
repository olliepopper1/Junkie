"""
Migration script to update the database schema
Adds reset_password_token and reset_password_expires fields to WebUser model
"""
import os
import sys
import logging
from app import app, db
from models import WebUser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def migrate():
    with app.app_context():
        try:
            # Check if migration is needed
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('web_user')]
            
            needs_migration = 'reset_password_token' not in columns or 'reset_password_expires' not in columns
            
            if not needs_migration:
                logger.info("Migration not needed - columns already exist")
                return
            
            # Add columns using raw SQL to avoid recreating the table
            logger.info("Starting migration - adding reset password columns")
            
            if 'reset_password_token' not in columns:
                db.session.execute(
                    'ALTER TABLE web_user ADD COLUMN reset_password_token VARCHAR(100) UNIQUE'
                )
                logger.info("Added reset_password_token column")
            
            if 'reset_password_expires' not in columns:
                db.session.execute(
                    'ALTER TABLE web_user ADD COLUMN reset_password_expires DATETIME'
                )
                logger.info("Added reset_password_expires column")
            
            db.session.commit()
            logger.info("Migration completed successfully")
        
        except Exception as e:
            logger.error(f"Migration failed: {str(e)}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    migrate()