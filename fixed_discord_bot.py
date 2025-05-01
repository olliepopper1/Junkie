#!/usr/bin/env python3
"""
100% Fixed Discord Bot - Guaranteed No Flask Imports
This script completely avoids any import that could potentially load Flask,
ensuring there are no port conflicts with the web application.
"""
import os
import sys
import json
import logging
import random
import sqlite3
from datetime import datetime, timedelta
import time
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
logger = logging.getLogger("fixed_discord_bot")

# Load environment variables
load_dotenv()

# Check if we have the Discord bot token
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

# Check if we have the RapidAPI key
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
if not RAPIDAPI_KEY:
    logger.warning("RAPIDAPI_KEY not found in environment variables. API features will be limited.")

# Initialize SQLite database
def initialize_database():
    """Initialize the SQLite database with required tables"""
    logger.info("Initializing database...")
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect("trial_junkie.db")
        cursor = conn.cursor()
        
        # Create users table
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
        
        logger.info("Database initialization complete")
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

# Simple database operations
def save_user(user_id, username):
    """Save a user to the database"""
    try:
        conn = sqlite3.connect("trial_junkie.db")
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if cursor.fetchone():
            # Update last_active timestamp
            cursor.execute(
                "UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE id = ?",
                (user_id,)
            )
        else:
            # Create new user
            cursor.execute(
                "INSERT INTO users (id, username) VALUES (?, ?)",
                (user_id, username)
            )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error saving user: {e}")
        return False

def save_credential(user_id, service, credential_type, credential_value):
    """Save a credential to the database"""
    try:
        conn = sqlite3.connect("trial_junkie.db")
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO credentials (user_id, service, credential_type, credential_value) VALUES (?, ?, ?, ?)",
            (user_id, service, credential_type, credential_value)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error saving credential: {e}")
        return False

def get_user_credentials(user_id, service=None):
    """Get a user's credentials"""
    try:
        conn = sqlite3.connect("trial_junkie.db")
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        
        if service:
            cursor.execute(
                "SELECT * FROM credentials WHERE user_id = ? AND service = ? ORDER BY created_at DESC",
                (user_id, service)
            )
        else:
            cursor.execute(
                "SELECT * FROM credentials WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            )
        
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result
    except Exception as e:
        logger.error(f"Error getting credentials: {e}")
        return []

def run_bot():
    """Run the Discord bot"""
    logger.info("Starting fixed Discord bot...")
    
    # Initialize the database
    if not initialize_database():
        logger.error("Failed to initialize database")
        sys.exit(1)
    
    try:
        # Import Discord.py here to avoid any circular imports
        import discord
        from discord.ext import commands
        
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Create bot instance
        bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
        
        @bot.event
        async def on_ready():
            """Called when the bot is ready"""
            logger.info(f"Trial Junkie bot is online as {bot.user}")
            await bot.change_presence(activity=discord.Game(name="!help for commands"))
        
        @bot.event
        async def on_command_error(ctx, error):
            """Handle command errors"""
            if isinstance(error, commands.CommandNotFound):
                await ctx.send("❌ Command not found. Use `!help` to see available commands.")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"❌ Missing required argument: {error.param.name}")
            else:
                logger.error(f"Command error: {error}")
                await ctx.send(f"❌ Error: {str(error)}")
        
        @bot.command(name="ping")
        async def ping_command(ctx):
            """Simple ping command to test the bot"""
            await ctx.send(f"🏓 Pong! Bot latency: {round(bot.latency * 1000)}ms")
        
        @bot.command(name="help")
        async def help_command(ctx):
            """Display help information"""
            embed = discord.Embed(
                title="🧪 Trial Junkie - Help",
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
            
            embed.add_field(
                name="🏓 Ping",
                value="`!ping` - Check if bot is responsive",
                inline=True
            )
            
            embed.set_footer(text="Trial Junkie | The Last Free Trial You'll Ever Need")
            await ctx.send(embed=embed)
        
        @bot.command(name="hit")
        async def hit_command(ctx, *, service_or_url: str = None):
            """Full trial setup command (all agents) - Works with services or URLs"""
            if not service_or_url:
                await ctx.send("❌ Please specify a service (e.g., `!hit Netflix`) or URL (e.g., `!hit https://example.com/trial`)")
                return
            
            # Save the user to the database
            save_user(str(ctx.author.id), ctx.author.name)
            
            # Check if URL or service name
            is_url = service_or_url.startswith(("http://", "https://"))
            
            # Create an initial message based on what was provided
            if is_url:
                embed = discord.Embed(
                    title="🧪 Trial Generation Started",
                    description=f"Running trial setup for URL: {service_or_url}",
                    color=0x6f42c1
                )
            else:
                embed = discord.Embed(
                    title="🧪 Trial Generation Started",
                    description=f"Running trial setup for service: {service_or_url.upper()}",
                    color=0x6f42c1
                )
            
            # Add agent information
            embed.add_field(
                name="Agents Deployed",
                value=(
                    "💉 **Heroin Harry** - Identity generation\n"
                    "💨 **Meth Mandy** - Card generation\n"
                    "💊 **Xanny Xan** - Email creation\n"
                    "❄️ **Cokehead Carl** - Phone verification\n"
                    "🍄 **Shroomy Sal** - Browser automation\n"
                ),
                inline=False
            )
            
            embed.add_field(
                name="Estimated Time",
                value="⏱️ 30-60 seconds",
                inline=False
            )
            
            embed.set_footer(text="Trial Junkie - Get your digital fix")
            processing_message = await ctx.send(embed=embed)
            
            try:
                # Import API integrations here to avoid circular imports
                sys.path.append('.')  # Ensure the current directory is in the path
                from api_integrations import APIIntegrations
                
                # Generate trial data based on whether it's a URL or service
                if is_url:
                    # URL-based trial generation
                    trial_data = APIIntegrations.create_trial_for_url(service_or_url)
                    service_name = "Custom URL Trial"
                else:
                    # Service-based trial generation
                    trial_data = APIIntegrations.generate_complete_trial_data(service_or_url)
                    service_name = service_or_url.upper()
                
                # Extract user info
                user_info = trial_data.get("user_info", {})
                
                # Save credentials to database
                save_credential(str(ctx.author.id), service_or_url, "email", user_info.get("email", "N/A"))
                save_credential(str(ctx.author.id), service_or_url, "password", user_info.get("password", "N/A"))
                
                if "card_number" in user_info.get("payment_info", {}):
                    save_credential(str(ctx.author.id), service_or_url, "card_number", user_info["payment_info"]["card_number"])
                
                # Create success response
                success_embed = discord.Embed(
                    title=f"✅ {service_name} Trial Ready",
                    description="Your trial credentials have been generated!",
                    color=0x28a745
                )
                
                # Add primary credentials
                success_embed.add_field(name="📧 Email", value=f"`{user_info.get('email', 'N/A')}`", inline=True)
                success_embed.add_field(name="🔑 Password", value=f"`{user_info.get('password', 'N/A')}`", inline=True)
                
                # Add payment info if available
                payment_info = user_info.get("payment_info", {})
                if payment_info:
                    card_info = (
                        f"Type: `{payment_info.get('card_type', 'N/A')}`\n"
                        f"Number: `{payment_info.get('card_number', 'N/A')}`\n"
                        f"Expiry: `{payment_info.get('expiry', 'N/A')}`\n"
                        f"CVV: `{payment_info.get('cvv', 'N/A')}`\n"
                        f"Name: `{payment_info.get('cardholder_name', 'N/A')}`"
                    )
                    success_embed.add_field(name="💳 Payment Details", value=card_info, inline=False)
                
                # Add verification info if available
                verification_info = user_info.get("verification_info", {})
                if verification_info:
                    verify_info = (
                        f"Phone: `{user_info.get('phone', 'N/A')}`\n"
                        f"Email Inbox: [Check Inbox]({verification_info.get('email_inbox', '')})"
                    )
                    success_embed.add_field(name="📱 Verification", value=verify_info, inline=False)
                
                # Add trial end date if available
                if "trial_end_date" in trial_data:
                    success_embed.add_field(name="⏰ Trial Expires", value=f"`{trial_data['trial_end_date']}`", inline=True)
                
                # Add automation result info for URLs
                if is_url and "automation_result" in trial_data:
                    auto_result = trial_data.get("automation_result", {})
                    result_status = "✅ Success" if trial_data.get("success", False) else "❌ Partial/Failed"
                    score = auto_result.get("success_score", 0)
                    
                    auto_info = (
                        f"Status: {result_status}\n"
                        f"Score: {score}/8\n"
                        f"Site Category: {trial_data.get('category', 'Unknown')}\n"
                        f"Final URL: `{trial_data.get('final_url', 'N/A')}`"
                    )
                    success_embed.add_field(name="🤖 Automation Results", value=auto_info, inline=False)
                
                success_embed.set_footer(text="Use !stash to view all your credentials")
                
                # Update the original message with the success embed
                await processing_message.edit(embed=success_embed)
                
            except Exception as e:
                logger.error(f"Error generating trial: {str(e)}")
                error_embed = discord.Embed(
                    title="❌ Trial Generation Failed",
                    description=f"There was an error generating your trial: ```{str(e)}```",
                    color=0xdc3545
                )
                await processing_message.edit(embed=error_embed)
        
        @bot.command(name="stash")
        async def stash_command(ctx):
            """View user's generated items"""
            # Get the user's credentials
            credentials = get_user_credentials(str(ctx.author.id))
            
            if not credentials:
                await ctx.send("❌ You don't have any saved credentials yet. Use `!hit <service>` to generate some!")
                return
            
            # Group credentials by service
            services = {}
            for cred in credentials:
                service = cred['service']
                if service not in services:
                    services[service] = []
                services[service].append(cred)
            
            # Create response
            embed = discord.Embed(
                title="🧪 Your Trial Stash",
                description=f"You have credentials for {len(services)} services",
                color=0x17a2b8
            )
            
            for service, creds in services.items():
                # Get the most recent credentials for each type
                cred_dict = {}
                for cred in creds:
                    cred_type = cred['credential_type']
                    if cred_type not in cred_dict:
                        cred_dict[cred_type] = cred['credential_value']
                
                # Format credential info
                cred_text = "\n".join([f"{k.capitalize()}: `{v}`" for k, v in cred_dict.items()])
                embed.add_field(name=service, value=cred_text, inline=False)
            
            embed.set_footer(text="Trial Junkie | Your trial dealer")
            
            await ctx.send(embed=embed)
        
        # Run the bot
        bot.run(DISCORD_BOT_TOKEN)
        
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()