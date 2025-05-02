#!/usr/bin/env python3
"""
Discord Bot for Trial Junkie
Handles Discord interactions for trial generation and delivery
"""
import os
import sys
import json
import logging
import traceback
from datetime import datetime, timedelta
import random
import asyncio
import string
from typing import Optional, Dict, List, Any, Union

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("discord_bot")

# Load environment variables
load_dotenv()

# Check for Discord token
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("No Discord bot token found in environment variables")
    # For development/testing only - in production this should exit
    logger.info("For testing purposes, the bot will run with a dummy token")
    SIMULATION_MODE = True
else:
    SIMULATION_MODE = False

# Bot configuration
COMMAND_PREFIX = '!'
BOT_DESCRIPTION = "Trial Junkie - Generate free trials with a single command"

# Create intents for the bot (permissions)
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content
intents.members = True  # Required for interacting with members

# Create the bot instance
bot = commands.Bot(command_prefix=COMMAND_PREFIX, description=BOT_DESCRIPTION, intents=intents)

# Keep track of user limits (this should be moved to a database in production)
USER_TRIALS = {}
TRIAL_LIMIT = 1  # Free tier limit per day
PREMIUM_TRIAL_LIMIT = 5  # Premium tier limit per day

# User tiers
USER_TIERS = {}

# Supported services for trials
SUPPORTED_SERVICES = [
    "hulu",
    "netflix",
    "disney+",
    "spotify",
    "apple music",
    "youtube premium",
    "hbo max"
]

# Quotes from agents
AGENT_QUOTES = {
    "mandy": [
        "Identity generated. Looks totally legit.",
        "Got you a fresh identity. Use it wisely.",
        "New person, who dis? Your identity is ready.",
        "Identity created. Even I'm convinced it's real.",
        "Fresh identity cooked up. It'll pass any check."
    ],
    "danny": [
        "Got a phone number that won't trace back to you.",
        "SMS verification? No problem, here's your number.",
        "This number is clean. Use it for the verification.",
        "Phone number ready. It'll work for verification codes.",
        "Virtual number secured. Verification should be smooth."
    ],
    "sandy": [
        "Card's ready. It'll work for the free trial only.",
        "Generated a clean card for the trial. Don't try to buy stuff.",
        "Card info created. Will pass verification but won't charge.",
        "Virtual card ready. Perfect for that free trial.",
        "Here's your card. It's designed specifically for trials."
    ],
    "randy": [
        "Email's verified and ready to go.",
        "Fresh inbox waiting for you. Confirmation emails are no problem.",
        "Email setup complete. I'll handle any verification emails.",
        "Mailbox is hot and ready. Verification emails will be processed.",
        "Email verification? Consider it done."
    ],
    "andy": [
        "Automation complete. The trial is ready.",
        "Website conquered. Your trial account is ready.",
        "Done and done. The website never knew what hit it.",
        "Trial secured through pure automation magic.",
        "Account created automatically. Login details attached."
    ]
}

# Attempt to load from database module
try:
    from database import Database
    db = Database()
    db_result = db.initialize()
    if db_result.get('success', False):
        logger.info("Database connection successful")
        DATABASE_AVAILABLE = True
    else:
        logger.warning(f"Database initialization failed: {db_result.get('message')}")
        DATABASE_AVAILABLE = False
except ImportError:
    logger.warning("Database module not available")
    DATABASE_AVAILABLE = False

# Attempt to load API integrations
try:
    from updated_api_integrations import UpdatedAPIIntegrations
    api = UpdatedAPIIntegrations()
    API_AVAILABLE = True
    logger.info("API integrations loaded successfully")
except ImportError:
    logger.warning("API integrations module not available")
    API_AVAILABLE = False
    api = None

# Attempt to load trial delivery
try:
    from bot_trial_delivery import TrialDelivery
    trial_delivery = TrialDelivery()
    DELIVERY_AVAILABLE = True
    logger.info("Trial delivery module loaded successfully")
except ImportError:
    logger.warning("Trial delivery module not available")
    DELIVERY_AVAILABLE = False
    trial_delivery = None

# Bot event handlers
@bot.event
async def on_ready():
    """Called when the bot is ready"""
    logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    logger.info(f"Connected to {len(bot.guilds)} guilds")
    
    # Set bot activity
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name=f"for {COMMAND_PREFIX}help commands"
        )
    )
    
    logger.info(f"Bot is ready - using prefix: {COMMAND_PREFIX}")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            f"Command not found. Use `{COMMAND_PREFIX}help` to see available commands."
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f"Missing required argument: {error.param.name}. Use `{COMMAND_PREFIX}help {ctx.command}` for proper usage."
        )
    else:
        logger.error(f"Command error: {str(error)}")
        await ctx.send(
            f"An error occurred: {str(error)}. Please try again later."
        )

# Helper functions
def check_user_limit(user_id: int, tier: str = "free") -> bool:
    """
    Check if a user has reached their daily trial limit
    
    Args:
        user_id: The Discord user ID
        tier: The user's subscription tier
        
    Returns:
        bool: True if user can generate more trials, False if limit reached
    """
    # Get the current date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Initialize user trial tracking if not exists
    if user_id not in USER_TRIALS:
        USER_TRIALS[user_id] = {"date": today, "count": 0}
    
    # Reset counter if it's a new day
    if USER_TRIALS[user_id]["date"] != today:
        USER_TRIALS[user_id] = {"date": today, "count": 0}
    
    # Check against the appropriate limit
    limit = PREMIUM_TRIAL_LIMIT if tier.lower() == "premium" else TRIAL_LIMIT
    
    # Return true if under limit, false if at or over limit
    return USER_TRIALS[user_id]["count"] < limit

def increment_user_trial(user_id: int) -> None:
    """
    Increment the trial count for a user
    
    Args:
        user_id: The Discord user ID
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Initialize if not exists
    if user_id not in USER_TRIALS:
        USER_TRIALS[user_id] = {"date": today, "count": 0}
    
    # Reset if new day
    if USER_TRIALS[user_id]["date"] != today:
        USER_TRIALS[user_id] = {"date": today, "count": 0}
    
    # Increment count
    USER_TRIALS[user_id]["count"] += 1

def get_user_tier(user_id: int) -> str:
    """
    Get the subscription tier for a user
    
    Args:
        user_id: The Discord user ID
        
    Returns:
        str: The user's subscription tier
    """
    if DATABASE_AVAILABLE:
        # TODO: Implement database lookup
        pass
    
    # Fallback to in-memory storage
    return USER_TIERS.get(str(user_id), "free")

def save_trial(user_id: int, trial_data: Dict[str, Any]) -> bool:
    """
    Save trial information to storage
    
    Args:
        user_id: The Discord user ID
        trial_data: The trial information
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    if DATABASE_AVAILABLE:
        # TODO: Implement database storage
        pass
    
    # Fallback to saving to a json file for each user
    try:
        user_trials_file = f"trials_{user_id}.json"
        existing_trials = []
        
        # Load existing trials if available
        if os.path.exists(user_trials_file):
            with open(user_trials_file, 'r') as f:
                existing_trials = json.load(f)
        
        # Add the new trial
        existing_trials.append(trial_data)
        
        # Save back to file
        with open(user_trials_file, 'w') as f:
            json.dump(existing_trials, f, indent=2)
        
        return True
    except Exception as e:
        logger.error(f"Error saving trial: {str(e)}")
        return False

def get_user_trials(user_id: int) -> List[Dict[str, Any]]:
    """
    Get all trials for a user
    
    Args:
        user_id: The Discord user ID
        
    Returns:
        list: The user's trials
    """
    if DATABASE_AVAILABLE:
        # TODO: Implement database lookup
        pass
    
    # Fallback to reading from file
    user_trials_file = f"trials_{user_id}.json"
    if os.path.exists(user_trials_file):
        try:
            with open(user_trials_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading trials: {str(e)}")
    
    return []

def format_trial_embed(trial_data: Dict[str, Any]) -> discord.Embed:
    """
    Format trial information as a Discord embed
    
    Args:
        trial_data: The trial information
        
    Returns:
        discord.Embed: The formatted embed
    """
    service = trial_data.get("service", "Unknown").title()
    plan = trial_data.get("plan", "Basic")
    
    # Create embed
    embed = discord.Embed(
        title=f"{service} Trial Account",
        description=f"Your {service} trial is ready! Here are your login details:",
        color=0x9370DB  # Medium purple
    )
    
    # Add basic fields
    embed.add_field(name="Service", value=service, inline=True)
    embed.add_field(name="Plan", value=plan, inline=True)
    
    # Add dates
    start_date = trial_data.get("start_date", "Today")
    end_date = trial_data.get("end_date", "Unknown")
    embed.add_field(name="Valid Until", value=end_date, inline=True)
    
    # Login information
    embed.add_field(
        name="Login Information", 
        value=f"**Email:** {trial_data.get('email', 'N/A')}\n**Password:** {trial_data.get('password', 'N/A')}",
        inline=False
    )
    
    # Personal information used
    personal_info = (
        f"**Name:** {trial_data.get('first_name', 'John')} {trial_data.get('last_name', 'Doe')}\n"
        f"**Phone:** {trial_data.get('phone', 'N/A')}"
    )
    embed.add_field(name="Personal Info", value=personal_info, inline=False)
    
    # Payment information
    card_details = trial_data.get("card_details", {})
    if card_details:
        payment_info = (
            f"**Card Type:** {card_details.get('type', 'visa').upper()}\n"
            f"**Last 4:** {card_details.get('last4', 'XXXX')}\n"
            f"**Expiry:** {card_details.get('expiry', 'MM/YY')}"
        )
        embed.add_field(name="Payment Method", value=payment_info, inline=False)
    
    # Add footer with cancellation reminder
    embed.set_footer(text="Remember to cancel before the trial ends to avoid charges.")
    
    return embed

# Bot commands
@bot.command(name="help")
async def help_command(ctx):
    """Show help information for the bot"""
    help_text = (
        f"**Trial Junkie Bot Commands**\n\n"
        f"**{COMMAND_PREFIX}hit [service]** - Generate a full trial for a service (requires all agents)\n"
        f"**{COMMAND_PREFIX}dose [agent] [platform]** - Use a specific agent for part of the process\n"
        f"**{COMMAND_PREFIX}stash** - View your generated trials\n"
        f"**{COMMAND_PREFIX}agents** - Show information about all agents\n"
        f"**{COMMAND_PREFIX}quote [agent]** - Get a quote from an agent\n"
        f"**{COMMAND_PREFIX}rehab** - Delete your user data\n"
        f"**{COMMAND_PREFIX}tier** - Check your subscription tier\n"
        f"**{COMMAND_PREFIX}pay [subscription]** - Get payment information for a subscription\n"
        f"**{COMMAND_PREFIX}referral** - Get or manage your referral code\n\n"
        f"For more information, visit https://trialjunkie.replit.app"
    )
    
    embed = discord.Embed(
        title="Trial Junkie Help",
        description=help_text,
        color=0x9370DB
    )
    
    await ctx.send(embed=embed)

@bot.command(name="hit")
async def hit_command(ctx, *, service_or_url: str = None):
    """
    Generate a full trial for a service (all agents)
    
    Args:
        service_or_url: The service name or URL to generate a trial for
    """
    user_id = ctx.author.id
    username = ctx.author.name
    
    # Check if user provided a service
    if not service_or_url:
        await ctx.send(
            f"Please specify a service or URL. Example: `{COMMAND_PREFIX}hit hulu`\n"
            f"Supported services: {', '.join(SUPPORTED_SERVICES)}"
        )
        return
    
    # Normalize service name
    service = service_or_url.lower().strip()
    
    # Check if service is supported
    if service not in SUPPORTED_SERVICES and not service.startswith(('http://', 'https://')):
        await ctx.send(
            f"Sorry, {service} is not supported yet. Supported services: {', '.join(SUPPORTED_SERVICES)}\n"
            f"You can also enter a full URL for custom trial generation."
        )
        return
    
    # Check user limits
    tier = get_user_tier(user_id)
    if not check_user_limit(user_id, tier):
        limit = PREMIUM_TRIAL_LIMIT if tier.lower() == "premium" else TRIAL_LIMIT
        await ctx.send(
            f"You've reached your daily limit of {limit} trials. "
            f"Come back tomorrow or upgrade to premium for higher limits."
        )
        return
    
    # Acknowledge the request
    await ctx.send(f"🧪 Generating your {service} trial... This may take a minute.")
    
    try:
        # Show "typing" indicator during processing
        async with ctx.typing():
            # Generate trial data
            if API_AVAILABLE and api:
                # This is a placeholder for the actual API call
                if service == "hulu":
                    # Call the API integration
                    trial_data = api.generate_complete_trial_data(service)
                    
                    # For demo purposes, let's generate a synthetic end date
                    if "start_date" not in trial_data:
                        trial_data["start_date"] = datetime.now().strftime("%Y-%m-%d")
                    
                    trial_end = datetime.now() + timedelta(days=30)
                    trial_data["end_date"] = trial_end.strftime("%Y-%m-%d")
                    
                    # Save the trial to storage
                    save_trial(user_id, trial_data)
                    
                    # Increment user's trial count
                    increment_user_trial(user_id)
                    
                    # Format and send the trial information
                    embed = format_trial_embed(trial_data)
                    await ctx.author.send(embed=embed)
                    
                    # Send confirmation in the channel
                    await ctx.send(
                        f"✅ Your {service} trial has been generated and sent to your DMs!"
                    )
                else:
                    # For other services, send a placeholder message
                    await ctx.send(
                        f"Service '{service}' is under development. Check back soon!"
                    )
            else:
                # API not available, send error message
                await ctx.send(
                    "Sorry, the trial generation system is currently unavailable. "
                    "Please try again later."
                )
    except Exception as e:
        logger.error(f"Error in hit command: {str(e)}")
        traceback.print_exc()
        await ctx.send(
            f"An error occurred while generating your trial: {str(e)}. "
            f"Please try again later."
        )

@bot.command(name="dose")
async def dose_command(ctx, agent_type: str = None, platform: str = None):
    """
    Use a specific agent for part of the trial process
    
    Args:
        agent_type: The type of agent to use
        platform: The platform to generate data for
    """
    valid_agents = ["mandy", "randy", "sandy", "danny", "andy"]
    
    if not agent_type:
        await ctx.send(
            f"Please specify an agent. Valid agents: {', '.join(valid_agents)}\n"
            f"Example: `{COMMAND_PREFIX}dose mandy`"
        )
        return
    
    agent = agent_type.lower()
    if agent not in valid_agents:
        await ctx.send(
            f"Invalid agent. Valid agents: {', '.join(valid_agents)}"
        )
        return
    
    await ctx.send(f"🧪 Asking {agent.title()} to help you out... One moment.")
    
    try:
        # Different responses based on the agent
        if agent == "mandy":  # Identity generator
            if API_AVAILABLE and api:
                identity = api.generate_identity()
                
                embed = discord.Embed(
                    title="Identity Generated",
                    description=f"Here's your new identity from Mandy:",
                    color=0x00FF00
                )
                
                embed.add_field(
                    name="Personal Information",
                    value=(
                        f"**Name:** {identity.get('first_name', 'John')} {identity.get('last_name', 'Doe')}\n"
                        f"**Address:** {identity.get('address', '123 Main St')}\n"
                        f"**City:** {identity.get('city', 'Anytown')}\n"
                        f"**State:** {identity.get('state', 'CA')}\n"
                        f"**ZIP:** {identity.get('zipcode', '12345')}\n"
                    ),
                    inline=False
                )
                
                # Random quote from the agent
                quote = random.choice(AGENT_QUOTES["mandy"])
                embed.set_footer(text=f"Mandy says: \"{quote}\"")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("Identity generation is currently unavailable.")
                
        elif agent == "danny":  # Phone number generator
            if API_AVAILABLE and api:
                phone = api.generate_virtual_number()
                
                embed = discord.Embed(
                    title="Phone Number Generated",
                    description=f"Here's your virtual phone number from Danny:",
                    color=0x4169E1
                )
                
                embed.add_field(
                    name="Phone Information",
                    value=(
                        f"**Number:** {phone.get('number', 'N/A')}\n"
                        f"**Country:** {phone.get('country', 'US')}\n"
                        f"**Valid For:** SMS Verification\n"
                    ),
                    inline=False
                )
                
                # Random quote from the agent
                quote = random.choice(AGENT_QUOTES["danny"])
                embed.set_footer(text=f"Danny says: \"{quote}\"")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("Phone number generation is currently unavailable.")
                
        elif agent == "sandy":  # Card generator
            if API_AVAILABLE and api:
                card = api.generate_card()
                
                embed = discord.Embed(
                    title="Credit Card Generated",
                    description=f"Here's your virtual card from Sandy:",
                    color=0xFF6347
                )
                
                embed.add_field(
                    name="Card Information",
                    value=(
                        f"**Card Type:** {card.get('type', 'VISA').upper()}\n"
                        f"**Card Number:** {card.get('number', 'XXXX-XXXX-XXXX-XXXX')}\n"
                        f"**Expiry:** {card.get('expiry', 'MM/YY')}\n"
                        f"**CVV:** {card.get('cvv', 'XXX')}\n"
                    ),
                    inline=False
                )
                
                embed.add_field(
                    name="⚠️ Important Note",
                    value=(
                        "This card is for trial verification only. It won't work for actual purchases. "
                        "Use it only for free trial signups."
                    ),
                    inline=False
                )
                
                # Random quote from the agent
                quote = random.choice(AGENT_QUOTES["sandy"])
                embed.set_footer(text=f"Sandy says: \"{quote}\"")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("Card generation is currently unavailable.")
                
        elif agent == "randy":  # Email generator
            if API_AVAILABLE and api:
                email = api.generate_email()
                
                embed = discord.Embed(
                    title="Email Generated",
                    description=f"Here's your disposable email from Randy:",
                    color=0xFFD700
                )
                
                embed.add_field(
                    name="Email Information",
                    value=(
                        f"**Email Address:** {email.get('email', 'user@example.com')}\n"
                        f"**Password:** {email.get('password', 'password123')}\n"
                        f"**Valid For:** Email Verification\n"
                    ),
                    inline=False
                )
                
                # Random quote from the agent
                quote = random.choice(AGENT_QUOTES["randy"])
                embed.set_footer(text=f"Randy says: \"{quote}\"")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("Email generation is currently unavailable.")
                
        elif agent == "andy":  # Automation specialist
            await ctx.send(
                "Andy needs a specific target to work with. "
                f"Use `{COMMAND_PREFIX}hit [service]` to run a full automation."
            )
    except Exception as e:
        logger.error(f"Error in dose command: {str(e)}")
        await ctx.send(
            f"An error occurred while using {agent.title()}: {str(e)}. "
            f"Please try again later."
        )

@bot.command(name="stash")
async def stash_command(ctx):
    """View user's generated trials"""
    user_id = ctx.author.id
    username = ctx.author.name
    
    # Get all trials for the user
    trials = get_user_trials(user_id)
    
    if not trials:
        await ctx.send("You haven't generated any trials yet.")
        return
    
    # Create an embed to display the trials
    embed = discord.Embed(
        title="Your Trial Stash",
        description=f"You have {len(trials)} trials in your stash:",
        color=0x9370DB
    )
    
    # Add each trial to the embed
    for i, trial in enumerate(trials[:10], 1):  # Limit to 10 trials
        service = trial.get("service", "Unknown").title()
        status = "Active" if datetime.strptime(trial.get("end_date", "2020-01-01"), "%Y-%m-%d") > datetime.now() else "Expired"
        
        embed.add_field(
            name=f"{i}. {service}",
            value=(
                f"**Email:** {trial.get('email', 'N/A')}\n"
                f"**Expires:** {trial.get('end_date', 'Unknown')}\n"
                f"**Status:** {status}"
            ),
            inline=True
        )
    
    # Add a note if there are more than 10 trials
    if len(trials) > 10:
        embed.set_footer(text=f"And {len(trials) - 10} more trials not shown.")
    
    await ctx.send(embed=embed)

@bot.command(name="rehab")
async def rehab_command(ctx):
    """Clear user data (with confirmation)"""
    user_id = ctx.author.id
    
    # Ask for confirmation
    message = await ctx.send(
        "⚠️ This will delete all your trial data. Are you sure? React with ✅ to confirm, or ❌ to cancel."
    )
    
    # Add reaction options
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    
    # Define a check function for the reaction
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == message.id
    
    try:
        # Wait for a reaction
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
        
        if str(reaction.emoji) == "✅":
            # Delete the user's trial file
            user_trials_file = f"trials_{user_id}.json"
            if os.path.exists(user_trials_file):
                os.remove(user_trials_file)
                
            # Remove from in-memory storage
            if user_id in USER_TRIALS:
                del USER_TRIALS[user_id]
                
            if str(user_id) in USER_TIERS:
                del USER_TIERS[str(user_id)]
                
            await ctx.send("✅ All your data has been deleted.")
        else:
            await ctx.send("❌ Operation cancelled.")
    except asyncio.TimeoutError:
        await ctx.send("⏰ Timed out. Operation cancelled.")

@bot.command(name="quote")
async def quote_command(ctx, agent: str = None):
    """Get a random quote from an agent"""
    valid_agents = list(AGENT_QUOTES.keys())
    
    # If no agent specified, pick a random one
    if not agent:
        agent = random.choice(valid_agents)
    else:
        agent = agent.lower()
        if agent not in valid_agents:
            await ctx.send(
                f"Invalid agent. Valid agents: {', '.join(valid_agents)}"
            )
            return
    
    # Get a random quote from the agent
    quote = random.choice(AGENT_QUOTES[agent])
    
    # Agent colors
    agent_colors = {
        "mandy": 0x00FF00,  # Green
        "danny": 0x4169E1,  # Royal Blue
        "sandy": 0xFF6347,  # Tomato
        "randy": 0xFFD700,  # Gold
        "andy": 0x800080    # Purple
    }
    
    # Agent roles
    agent_roles = {
        "mandy": "Identity Specialist",
        "danny": "Phone Verification Expert",
        "sandy": "Payment Systems Specialist",
        "randy": "Email Verification Guru",
        "andy": "Automation Wizard"
    }
    
    # Create an embed for the quote
    embed = discord.Embed(
        title=f"{agent.title()} says:",
        description=f"\"{quote}\"",
        color=agent_colors.get(agent, 0x9370DB)
    )
    
    embed.set_footer(text=f"{agent.title()} - {agent_roles.get(agent, 'Agent')}")
    
    await ctx.send(embed=embed)

@bot.command(name="agents")
async def agents_command(ctx):
    """Display information about all agents"""
    embed = discord.Embed(
        title="Trial Junkie Agents",
        description="Meet the team of specialists who make your trials possible:",
        color=0x9370DB
    )
    
    # Agent descriptions
    agents = {
        "Mandy": "Identity Specialist - Creates realistic identities that pass verification checks",
        "Danny": "Phone Verification Expert - Provides virtual phone numbers for SMS verification",
        "Sandy": "Payment Systems Specialist - Generates valid cards that pass verification but don't charge",
        "Randy": "Email Verification Guru - Creates and verifies email addresses for trial accounts",
        "Andy": "Automation Wizard - Handles the website interactions to create the actual accounts"
    }
    
    # Add each agent to the embed
    for agent, description in agents.items():
        embed.add_field(
            name=agent,
            value=description,
            inline=False
        )
    
    embed.set_footer(text=f"Use {COMMAND_PREFIX}dose [agent] to use a specific agent")
    
    await ctx.send(embed=embed)

@bot.command(name="tier")
async def tier_command(ctx):
    """View user tier status"""
    user_id = ctx.author.id
    username = ctx.author.name
    
    # Get user tier
    tier = get_user_tier(user_id)
    
    # Tier information
    tier_info = {
        "free": {
            "name": "Free Tier",
            "color": 0x808080,  # Gray
            "description": "Basic access with limited trials per day",
            "limit": TRIAL_LIMIT,
            "features": [
                "Access to basic trial generation",
                f"{TRIAL_LIMIT} trials per day",
                "Standard support"
            ]
        },
        "premium": {
            "name": "Premium Tier",
            "color": 0xFFD700,  # Gold
            "description": "Enhanced access with more trials and priority service",
            "limit": PREMIUM_TRIAL_LIMIT,
            "features": [
                "Access to all trial services",
                f"{PREMIUM_TRIAL_LIMIT} trials per day",
                "Priority trial generation",
                "Premium support",
                "Early access to new features"
            ]
        }
    }
    
    # Get tier details
    tier_details = tier_info.get(tier.lower(), tier_info["free"])
    
    # Create embed
    embed = discord.Embed(
        title=f"Your Subscription: {tier_details['name']}",
        description=tier_details["description"],
        color=tier_details["color"]
    )
    
    # Add daily usage
    today = datetime.now().strftime("%Y-%m-%d")
    if user_id in USER_TRIALS and USER_TRIALS[user_id]["date"] == today:
        usage = f"{USER_TRIALS[user_id]['count']}/{tier_details['limit']} trials used today"
    else:
        usage = f"0/{tier_details['limit']} trials used today"
    
    embed.add_field(
        name="Daily Usage",
        value=usage,
        inline=False
    )
    
    # Add features
    embed.add_field(
        name="Features",
        value="\n".join(f"✅ {feature}" for feature in tier_details["features"]),
        inline=False
    )
    
    # Add upgrade info for free tier
    if tier.lower() == "free":
        embed.add_field(
            name="Upgrade",
            value=f"Use `{COMMAND_PREFIX}pay premium` to upgrade to Premium and get more trials per day!",
            inline=False
        )
    
    await ctx.send(embed=embed)

# Run the bot
def run_bot():
    """Run the Discord bot"""
    logger.info("Starting Discord bot")
    
    if SIMULATION_MODE:
        logger.error("No Discord bot token found in environment variables")
        logger.info("For testing purposes, the bot will run with a dummy token")
        logger.info("Bot is running in simulation mode - no connection to Discord")
        
        # Load trial commands
        logger.info("Loaded trial commands")
        
        # Simulate bot startup
        logger.info("Simulating bot startup...")
        logger.info("Discord bot simulated and ready")
        logger.info("Commands available: !hit, !stash, !agents, !plans, !tier, !help")
        logger.info("You can test trial generation and stash commands via the Python API")
        
        return True
    else:
        try:
            # Run the bot with the Discord token
            bot.run(DISCORD_BOT_TOKEN)
            return True
        except Exception as e:
            logger.error(f"Error running Discord bot: {str(e)}")
            traceback.print_exc()
            return False

if __name__ == "__main__":
    run_bot()