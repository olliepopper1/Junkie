#!/usr/bin/env python3
"""
Discord Bot Workflow Script
This script is specifically designed for the Replit workflow system
and avoids any imports that might conflict with Flask or cause port issues.
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

# Subscription plans configuration - Matches web application plans
SUBSCRIPTION_PLANS = {
    "one_time_hit": {
        "name": "One-Time Hit",
        "price": 0.00,
        "daily_limit": 1,
        "description": "A quick blast of freedom, no strings attached",
        "features": ["One-time free trial", "No credit card required", "Basic features only"]
    },
    "five_dollar_rush": {
        "name": "Five Dollar Rush",
        "price": 5.00,
        "daily_limit": 25,
        "description": "A rush of power for just five bucks",
        "features": ["Limited-time access", "Multiple trials per day", "Standard features"]
    },
    "junkified": {
        "name": "Junkified Premium",
        "price": 13.00,
        "daily_limit": 100,
        "description": "Unlock unlimited possibilities—no limits, just freedom",
        "features": ["Unlimited access", "Priority support", "All premium features", "No daily limits"]
    }
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot_workflow.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("discord_bot_workflow")

# Load environment variables
load_dotenv()

# Check if we have the Discord bot token
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

def run_bot():
    """Run the Discord bot"""
    logger.info("Starting Discord bot workflow...")
    
    try:
        # Import Discord.py here to avoid any circular imports
        import discord
        from discord.ext import commands
        
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Create bot instance
        bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)
        
        @bot.event
        async def on_ready():
            """Called when the bot is ready"""
            logger.info(f"Trial Junkie bot is online as {bot.user}")
            await bot.change_presence(activity=discord.Game(name="/help for commands"))
        
        @bot.event
        async def on_command_error(ctx, error):
            """Handle command errors"""
            if isinstance(error, commands.CommandNotFound):
                await ctx.send("❌ Command not found. Use `/help` to see available commands.")
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
                value="`/hit <service/url>` - Generate all credentials for a trial\nExample: `/hit Netflix` or `/hit https://example.com`",
                inline=False
            )
            
            # Utility commands
            embed.add_field(
                name="🧪 Stash",
                value="`/stash` - View your saved credentials",
                inline=True
            )
            
            embed.add_field(
                name="💰 Plans",
                value="`/plans` - View subscription plans",
                inline=True
            )
            
            embed.add_field(
                name="🏓 Ping",
                value="`/ping` - Check if bot is responsive",
                inline=True
            )
            
            embed.set_footer(text="Trial Junkie | The Last Free Trial You'll Ever Need")
            await ctx.send(embed=embed)
        
        @bot.command(name="hit")
        async def hit_command(ctx, *, service_or_url: str = None):
            """Full trial setup command (all agents) - Works with services or URLs"""
            if not service_or_url:
                await ctx.send("❌ Please specify a service (e.g., `/hit Netflix`) or URL (e.g., `/hit https://example.com/trial`)")
                return
            
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
                
                success_embed.set_footer(text="Use /stash to view all your credentials")
                
                # Update the original message with the success embed
                await processing_message.edit(embed=success_embed)
                
                # Save the trial to the database using the TrialDelivery system
                try:
                    from database import Database
                    from utils.trial_delivery import TrialDelivery
                    
                    # Get the Discord user ID
                    discord_id = str(ctx.author.id)
                    
                    # Initialize the database
                    db = Database()
                    
                    # Check if the user exists, create if not
                    if not db.user_exists(discord_id):
                        db.create_user(discord_id, str(ctx.author))
                    
                    # Create the delivery object without Discord bot (we're already in Discord)
                    delivery = TrialDelivery()
                    
                    # Record the trial in the database
                    delivery_result = await delivery.save_to_dashboard(
                        user_id=discord_id,
                        trial_data=trial_data
                    )
                    
                    logger.info(f"Trial saved to database: {delivery_result}")
                    
                    # Check for linked web account and save there too if available
                    web_user_id = None
                    try:
                        # Query for linked accounts - this would need a proper implementation
                        # in your database.py based on your schema
                        linked_accounts = db.get_linked_accounts(discord_id)
                        if linked_accounts and len(linked_accounts) > 0:
                            web_user_id = linked_accounts[0].get('web_user_id')
                            
                            if web_user_id:
                                web_delivery_result = await delivery.save_to_dashboard(
                                    user_id=web_user_id,
                                    trial_data=trial_data
                                )
                                logger.info(f"Trial also saved to web account: {web_delivery_result}")
                    except Exception as link_err:
                        logger.error(f"Error checking linked accounts: {str(link_err)}")
                        # Continue anyway
                
                except Exception as db_err:
                    logger.error(f"Error saving trial to database: {str(db_err)}")
                    # We don't need to notify the user since they already have the trial info
                
            except Exception as e:
                logger.error(f"Error generating trial: {str(e)}")
                error_embed = discord.Embed(
                    title="❌ Trial Generation Failed",
                    description=f"There was an error generating your trial: ```{str(e)}```",
                    color=0xdc3545
                )
                await processing_message.edit(embed=error_embed)
        
        @bot.command(name="plans")
        async def plans_command(ctx):
            """Display available subscription plans"""
            embed = discord.Embed(
                title="💰 Trial Junkie Subscription Plans",
                description="Choose your digital trip level",
                color=0xf1c40f  # Gold color for payment/money
            )
            
            # Add fields for each plan
            for plan_id, plan in SUBSCRIPTION_PLANS.items():
                features_text = "\n".join([f"• {feature}" for feature in plan["features"]])
                embed.add_field(
                    name=f"{plan['name']} - ${plan['price']:.2f}",
                    value=f"{plan['description']}\n\n{features_text}\n\nDaily limit: {plan['daily_limit']} trials\nUse `/subscribe` to view subscription options",
                    inline=False
                )
            
            embed.set_footer(text="Trial Junkie | The Last Free Trial You'll Ever Need")
            await ctx.send(embed=embed)
        
        @bot.command(name="stash")
        async def stash_command(ctx):
            """View user's generated items"""
            # For the workflow version, we'll just show a placeholder message
            await ctx.send("🧪 Your saved trials would be displayed here in the full version.")
            
        @bot.command(name="subscribe")
        async def subscribe_command(ctx):
            """Redirect users to the website subscription page"""
            # Get your app's URL from an environment variable or config
            website_url = os.environ.get("APP_URL", "https://trialjunkie.replit.app")
            subscription_url = f"{website_url}/subscriptions"
            
            logger.info(f"User {ctx.author.id} ({ctx.author.name}) requested subscription link")
            
            embed = discord.Embed(
                title="💊 Subscribe to Trial Junkie",
                description="Visit our website to choose a subscription plan that fits your needs.",
                color=0xf1c40f
            )
            
            embed.add_field(
                name="How to Subscribe",
                value="1. Click the link below to visit our subscription page\n"
                      "2. Choose a subscription plan\n"
                      "3. Complete the payment using Solana\n"
                      "4. Return to Discord and start generating trials!",
                inline=False
            )
            
            embed.add_field(
                name="🔗 Subscription Link",
                value=f"[Click here to subscribe]({subscription_url})",
                inline=False
            )
            
            embed.set_footer(text="Trial Junkie - Get your digital fix")
            await ctx.send(embed=embed)
        
        # Run the bot
        bot.run(DISCORD_BOT_TOKEN)
        
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()