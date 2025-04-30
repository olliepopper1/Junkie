#!/usr/bin/env python3
"""
Pure Discord Bot Script
This is a completely standalone Discord bot implementation with no Flask dependencies
"""
import os
import sys
import json
import logging
import random
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
logger = logging.getLogger("pure_discord_bot")

# Load environment variables
load_dotenv()

# Check if we have the Discord bot token
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

def initialize_database():
    """Initialize database and create necessary tables if they don't exist"""
    logger.info("Initializing database...")
    
    try:
        import sqlite3
        conn = sqlite3.connect("trial_junkie.db")
        cursor = conn.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            discriminator TEXT,
            avatar TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create credentials table if it doesn't exist
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
        
        # Create trials table if it doesn't exist
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
        
        # Create payments table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            amount REAL NOT NULL,
            service_type TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            reference TEXT UNIQUE NOT NULL,
            tx_signature TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        
        # Create user_tiers table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_tiers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            tier TEXT DEFAULT 'free',
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        
        # Create usage_limits table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_limits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            command TEXT NOT NULL,
            count INTEGER DEFAULT 1,
            date DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, command, date)
        )
        """)
        
        # Create referral_codes table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS referral_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            code TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        
        # Create referrals table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id TEXT NOT NULL,
            referred_id TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referrer_id) REFERENCES users(id),
            FOREIGN KEY (referred_id) REFERENCES users(id)
        )
        """)
        
        # Create commissions table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS commissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id TEXT NOT NULL,
            referred_id TEXT NOT NULL,
            payment_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            paid_at TIMESTAMP,
            tx_signature TEXT,
            FOREIGN KEY (referrer_id) REFERENCES users(id),
            FOREIGN KEY (referred_id) REFERENCES users(id),
            FOREIGN KEY (payment_id) REFERENCES payments(id)
        )
        """)
        
        # Create referral_rates table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS referral_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tier TEXT UNIQUE NOT NULL,
            percentage REAL NOT NULL DEFAULT 10.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Insert default referral rates if table is empty
        cursor.execute("SELECT COUNT(*) FROM referral_rates")
        count = cursor.fetchone()[0]
        
        if count == 0:
            tiers = [("free", 5.0), ("basic", 10.0), ("premium", 15.0), ("enterprise", 20.0)]
            cursor.executemany(
                "INSERT INTO referral_rates (tier, percentage) VALUES (?, ?)",
                tiers
            )
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

def run_bot():
    """Main function to run the Discord bot"""
    logger.info("Starting Pure Discord Bot...")
    
    # Initialize the database first
    initialize_database()
    
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
            logger.info(f"Bot logged in as {bot.user.name} ({bot.user.id})")
            logger.info(f"Bot latency: {round(bot.latency * 1000)}ms")
            await bot.change_presence(activity=discord.Game(name="!help for commands"))
            logger.info("Bot is ready!")
        
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
        
        # Define basic commands
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
            
            embed.add_field(
                name="💊 Dose (Single Resource)",
                value="`!dose <agent> <service>` - Generate a specific credential\nAgents: harry (identity), mandy (card), xan (email), carl (phone)\nExample: `!dose harry Spotify`",
                inline=False
            )
            
            embed.add_field(
                name="🍄 Trip (Automation)",
                value="`!trip <script>` - Run an automation script\nExample: `!trip netflix_signup`\nUse `!trip help` for available scripts",
                inline=False
            )
            
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
        
        # Add administrative commands
        @bot.command(name="admin_refund")
        async def admin_refund_command(ctx, user_id: str = None, amount: float = None, *, reason: str = None):
            """Admin command to refund a user"""
            # Check if the user is an admin
            if ctx.author.id != 123456789:  # Replace with your admin user ID
                await ctx.send("❌ You don't have permission to use admin commands.")
                return
            
            if not user_id or not amount:
                await ctx.send("❌ Missing parameters. Usage: `!admin_refund <user_id> <amount> [reason]`")
                return
            
            logger.info(f"Admin {ctx.author.id} ({ctx.author.name}) issued refund: {user_id} for {amount} SOL. Reason: {reason}")
            
            # Process the refund (implementation would go here)
            # ...
            
            embed = discord.Embed(
                title="Admin Refund Processed",
                description=f"✅ Refund has been processed for user ID {user_id}",
                color=0x28a745  # Green
            )
            
            embed.add_field(name="Amount", value=f"{amount} SOL", inline=True)
            if reason:
                embed.add_field(name="Reason", value=reason, inline=False)
            
            embed.set_footer(text="Trial Junkie - Admin Command")
            await ctx.send(embed=embed)
        
        @bot.command(name="admin_gift")
        async def admin_gift_command(ctx, user_id: str = None, tier: str = None, days: int = 30, *, note: str = None):
            """Admin command to gift a subscription tier to a user"""
            # Check if the user is an admin
            if ctx.author.id != 123456789:  # Replace with your admin user ID
                await ctx.send("❌ You don't have permission to use admin commands.")
                return
            
            if not user_id or not tier:
                await ctx.send("❌ Missing parameters. Usage: `!admin_gift <user_id> <tier> [days=30] [note]`")
                return
            
            tiers = ["free", "basic", "premium", "enterprise"]
            # Validate tier
            if tier not in tiers:
                valid_tiers = ", ".join(tiers)
                await ctx.send(f"❌ Invalid tier. Available tiers: {valid_tiers}")
                return
            
            logger.info(f"Admin {ctx.author.id} ({ctx.author.name}) gifted tier {tier} to user {user_id} for {days} days. Note: {note}")
            
            # Process the gift subscription (implementation would go here)
            # ...
            
            embed = discord.Embed(
                title="Admin Gift Processed",
                description=f"✅ {tier.upper()} tier has been gifted to user ID {user_id}",
                color=0x28a745  # Green
            )
            
            embed.add_field(name="Tier", value=tier.upper(), inline=True)
            embed.add_field(name="Duration", value=f"{days} days", inline=True)
            if note:
                embed.add_field(name="Note", value=note, inline=False)
            
            embed.set_footer(text="Trial Junkie - Admin Command")
            await ctx.send(embed=embed)
        
        @bot.command(name="admin_referral_rate")
        async def admin_referral_rate_command(ctx, rate: float = None, tier: str = None):
            """Admin command to adjust referral percentage"""
            # Check if the user is an admin
            if ctx.author.id != 123456789:  # Replace with your admin user ID
                await ctx.send("❌ You don't have permission to use admin commands.")
                return
            
            if rate is None:
                await ctx.send("❌ Missing percentage rate. Usage: `!admin_referral_rate <rate> [tier]`")
                return
            
            if rate < 0 or rate > 100:
                await ctx.send("❌ Rate must be between 0 and 100 percent.")
                return
            
            logger.info(f"Admin {ctx.author.id} ({ctx.author.name}) adjusted referral rate to {rate}% for tier {tier if tier else 'all'}")
            
            # Process the referral rate change
            try:
                # In a real implementation, you would connect to the database
                # and update the referral rate for the specified tier
                # Here's a skeleton of what that would look like:
                
                # Connect to database
                import sqlite3
                conn = sqlite3.connect("trial_junkie.db")
                cursor = conn.cursor()
                
                # Update the referral rate in the appropriate table
                if tier:
                    cursor.execute(
                        "UPDATE referral_rates SET percentage = ? WHERE tier = ?",
                        (rate, tier.lower())
                    )
                else:
                    # Update rate for all tiers
                    cursor.execute(
                        "UPDATE referral_rates SET percentage = ?",
                        (rate,)
                    )
                
                conn.commit()
                conn.close()
                
                embed = discord.Embed(
                    title="Referral Rate Updated",
                    description=f"✅ Referral commission rate has been updated to {rate}%",
                    color=0x28a745  # Green
                )
                
                if tier:
                    embed.add_field(name="Tier", value=tier.upper(), inline=True)
                else:
                    embed.add_field(name="Applied To", value="All tiers", inline=True)
                
                embed.set_footer(text="Trial Junkie - Admin Command")
                await ctx.send(embed=embed)
                
            except Exception as e:
                logger.error(f"Error updating referral rate: {e}")
                await ctx.send(f"❌ Error updating referral rate: {str(e)}")
                return
        
        @bot.command(name="admin_pay_commission")
        async def admin_pay_commission_command(ctx, user_id: str = None, amount: float = None):
            """Admin command to pay out referral earnings"""
            # Check if the user is an admin
            if ctx.author.id != 123456789:  # Replace with your admin user ID
                await ctx.send("❌ You don't have permission to use admin commands.")
                return
            
            if not user_id:
                await ctx.send("❌ Missing user ID. Usage: `!admin_pay_commission <user_id> [amount]`")
                return
            
            logger.info(f"Admin {ctx.author.id} ({ctx.author.name}) processed commission payout for user {user_id}, amount: {amount if amount else 'ALL'}")
            
            try:
                # Connect to database
                import sqlite3
                conn = sqlite3.connect("trial_junkie.db")
                cursor = conn.cursor()
                
                # If amount is not specified, calculate and pay out all pending commissions
                if amount is None:
                    # Get total pending commissions for the user
                    cursor.execute(
                        "SELECT SUM(amount) as total FROM commissions WHERE referrer_id = ? AND status = 'pending'",
                        (user_id,)
                    )
                    result = cursor.fetchone()
                    
                    if result and result[0]:
                        amount = float(result[0])
                    else:
                        conn.close()
                        await ctx.send(f"❌ No pending commissions found for user ID {user_id}")
                        return
                
                # Update commission statuses to 'paid'
                now = time.strftime('%Y-%m-%d %H:%M:%S')
                
                if amount is not None:
                    # Generate a mock transaction signature for this payment
                    tx_signature = f"TX{random.randint(100000, 999999)}"
                    
                    # Update commissions up to the specified amount, marking them as paid
                    if amount > 0:
                        cursor.execute(
                            """
                            UPDATE commissions SET 
                            status = 'paid', 
                            paid_at = ?,
                            tx_signature = ?
                            WHERE referrer_id = ? AND status = 'pending'
                            """,
                            (now, tx_signature, user_id)
                        )
                        
                        conn.commit()
                        
                        embed = discord.Embed(
                            title="Commission Payout Processed",
                            description=f"✅ Commission has been paid out to user ID {user_id}",
                            color=0x28a745  # Green
                        )
                        
                        embed.add_field(name="Amount", value=f"{amount} SOL", inline=True)
                        embed.add_field(name="TX Signature", value=tx_signature, inline=True)
                        embed.add_field(name="Status", value="Transaction completed", inline=True)
                        embed.add_field(name="Date", value=now, inline=True)
                        
                        embed.set_footer(text="Trial Junkie - Admin Command")
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"❌ No commission amount to pay for user ID {user_id}")
                
                conn.close()
                
            except Exception as e:
                logger.error(f"Error processing commission payout: {e}")
                await ctx.send(f"❌ Error processing commission payout: {str(e)}")
                return
        
        @bot.command(name="admin_stats")
        async def admin_stats_command(ctx):
            """Admin command to view system statistics"""
            # Check if the user is an admin
            if ctx.author.id != 123456789:  # Replace with your admin user ID
                await ctx.send("❌ You don't have permission to use admin commands.")
                return
            
            logger.info(f"Admin {ctx.author.id} ({ctx.author.name}) requested system stats")
            
            try:
                # Connect to database
                import sqlite3
                conn = sqlite3.connect("trial_junkie.db")
                cursor = conn.cursor()
                
                # Initialize stats dictionary
                stats = {
                    "users": 0,
                    "active_trials": 0,
                    "paid_subscribers": 0,
                    "total_payments": 0.0,
                    "pending_commissions": 0.0,
                    "yesterday_trials": 0,
                    "yesterday_payments": 0.0
                }
                
                # Get total users count
                cursor.execute("SELECT COUNT(*) FROM users")
                result = cursor.fetchone()
                if result:
                    stats["users"] = result[0]
                
                # Get active trials count
                cursor.execute("SELECT COUNT(*) FROM credentials WHERE credential_type='trial'")
                result = cursor.fetchone()
                if result:
                    stats["active_trials"] = result[0]
                
                # Get paid subscribers count
                cursor.execute("SELECT COUNT(DISTINCT user_id) FROM user_tiers WHERE tier != 'free'")
                result = cursor.fetchone()
                if result:
                    stats["paid_subscribers"] = result[0]
                
                # Get total payments amount
                cursor.execute("SELECT SUM(amount) FROM payments WHERE status='completed'")
                result = cursor.fetchone()
                if result and result[0]:
                    stats["total_payments"] = round(float(result[0]), 2)
                
                # Get pending commissions
                cursor.execute("SELECT SUM(amount) FROM commissions WHERE status='pending'")
                result = cursor.fetchone()
                if result and result[0]:
                    stats["pending_commissions"] = round(float(result[0]), 2)
                
                # Get yesterday's activity
                yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400))
                
                # Yesterday's trials
                cursor.execute(
                    "SELECT COUNT(*) FROM credentials WHERE DATE(created_at) = ? AND credential_type='trial'", 
                    (yesterday,)
                )
                result = cursor.fetchone()
                if result:
                    stats["yesterday_trials"] = result[0]
                
                # Yesterday's payments
                cursor.execute(
                    "SELECT SUM(amount) FROM payments WHERE DATE(created_at) = ? AND status='completed'", 
                    (yesterday,)
                )
                result = cursor.fetchone()
                if result and result[0]:
                    stats["yesterday_payments"] = round(float(result[0]), 2)
                
                conn.close()
                
                # Create embed with statistics
                embed = discord.Embed(
                    title="System Statistics",
                    description="Current Trial Junkie system statistics",
                    color=0x17a2b8  # Blue
                )
                
                embed.add_field(name="👥 Total Users", value=str(stats["users"]), inline=True)
                embed.add_field(name="🧪 Active Trials", value=str(stats["active_trials"]), inline=True)
                embed.add_field(name="💰 Paid Subscribers", value=str(stats["paid_subscribers"]), inline=True)
                embed.add_field(name="💸 Total Payments", value=f"{stats['total_payments']} SOL", inline=True)
                embed.add_field(name="💼 Pending Commissions", value=f"{stats['pending_commissions']} SOL", inline=True)
                embed.add_field(name="📈 Yesterday Activity", value=f"{stats['yesterday_trials']} trials, {stats['yesterday_payments']} SOL", inline=False)
                
                embed.set_footer(text="Trial Junkie - Admin Dashboard")
                await ctx.send(embed=embed)
                
            except Exception as e:
                logger.error(f"Error fetching admin stats: {e}")
                await ctx.send(f"❌ Error fetching statistics: {str(e)}")
                return
        
        # Run the bot
        logger.info("Starting bot...")
        bot.run(DISCORD_BOT_TOKEN)
        
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        logger.error("Make sure discord.py is installed (pip install discord.py)")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    """Run the Discord bot when executed directly"""
    run_bot()