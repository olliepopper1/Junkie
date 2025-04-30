#!/usr/bin/env python3
"""
Completely Standalone Discord Bot for Trial Junkie
This version has NO Flask imports whatsoever and avoids any import of app.py
"""
import os
import sys
import json
import logging
import random
import time
from datetime import datetime, timedelta
import sqlite3
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("standalone_bot")

# Load environment variables
load_dotenv()

# Check if we have the Discord bot token
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

def initialize_database():
    """Initialize database and create necessary tables if they don't exist"""
    logger.info("Initializing database for standalone bot...")
    
    try:
        # Use SQLite for simplicity in the standalone version
        conn = sqlite3.connect("trial_junkie.db")
        cursor = conn.cursor()
        
        # Create basic tables needed for the bot
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create credentials table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            service TEXT NOT NULL,
            credential_type TEXT NOT NULL,
            credential_value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        
        # Create trials table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            service TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

def run_bot():
    """Main function to run the Discord bot"""
    logger.info("Starting standalone Discord bot...")
    
    # Initialize the database first
    if not initialize_database():
        logger.error("Failed to initialize database, exiting...")
        sys.exit(1)
        
    try:
        # Import discord module here to avoid potential circular imports
        import discord
        from discord.ext import commands
        
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Create bot instance
        bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
        
        # Define event handlers
        @bot.event
        async def on_ready():
            """Called when the bot is ready"""
            logger.info(f"Trial Junkie online as {bot.user}")
            await bot.change_presence(activity=discord.Game(name="!help for commands"))
        
        @bot.event
        async def on_command_error(ctx, error):
            """Handle command errors"""
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"❌ Missing required argument: {error.param.name}")
            elif isinstance(error, commands.CommandNotFound):
                await ctx.send(f"❌ Command not found. Try `!help` for a list of commands.")
            elif isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f"⏳ Command on cooldown. Try again in {error.retry_after:.1f} seconds.")
            else:
                logger.error(f"Command error: {error}")
                await ctx.send(f"❌ An error occurred: {error}")
        
        # Basic commands
        @bot.command(name="ping")
        async def ping_command(ctx):
            """Simple ping command to check if the bot is working"""
            await ctx.send(f"Pong! Bot latency: {round(bot.latency * 1000)}ms")
        
        @bot.command(name="help")
        async def help_command(ctx):
            """Display help information"""
            embed = discord.Embed(
                title="🧪 Trial Junkie Help",
                description="Your friendly neighborhood dealer for free trials",
                color=0x6f42c1
            )
            
            # Main commands
            embed.add_field(
                name="🎯 Hit (Full Trial)",
                value="`!hit <service>` - Generate all credentials for a trial\nExample: `!hit Netflix`",
                inline=False
            )
            
            # Utility commands
            embed.add_field(
                name="🧪 Stash",
                value="`!stash` - View your saved credentials",
                inline=True
            )
            
            embed.add_field(
                name="🏥 Rehab",
                value="`!rehab` - Clear all your data",
                inline=True
            )
            
            embed.set_footer(text="Trial Junkie | The Last Free Trial You'll Ever Need")
            await ctx.send(embed=embed)
        
        # Run the bot
        bot.run(DISCORD_BOT_TOKEN)
        
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()