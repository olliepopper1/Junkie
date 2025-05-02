#!/usr/bin/env python3
"""
Updated Discord Bot for Trial Junkie
Uses the updated API integrations for creating trials via Discord
"""
import os
import sys
import logging
import json
import random
import asyncio
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from dotenv import load_dotenv
from updated_api_integrations import UpdatedAPIIntegrations
from hulu_trial_generator import HuluTrialGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("updated_discord_bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Load the bot token from environment variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

# Load RapidAPI key
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
if not RAPIDAPI_KEY:
    logger.error("RAPIDAPI_KEY not found in environment variables")
    sys.exit(1)

# Set up the bot with intents
intents = discord.Intents.default()
intents.message_content = True  # For reading message content
intents.members = True  # For accessing member information

bot = commands.Bot(command_prefix="/", intents=intents)

# Limit tracking to ensure users can only create one trial
USER_TRIAL_LIMITS = {}

# Admin credentials
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

# Colors for embeds
COLORS = {
    "success": 0x4CAF50,  # Green
    "error": 0xF44336,    # Red
    "warning": 0xFFC107,  # Yellow
    "info": 0x2196F3,     # Blue
    "payment": 0x9C27B0   # Purple
}

# Trial services
TRIAL_SERVICES = {
    "hulu": {
        "url": "https://www.hulu.com/",
        "trial_period_days": 30,
        "price": "$14.99/month",
        "plan_name": "Hulu (No Ads)",
        "required_fields": ["identity", "email", "card", "phone"],
        "supports_automation": True,
        "cancellation_path": "Account > Cancel Subscription"
    },
    "disney": {
        "url": "https://www.disneyplus.com/",
        "trial_period_days": 7,
        "price": "$10.99/month",
        "plan_name": "Disney+ Premium",
        "required_fields": ["identity", "email", "card"],
        "supports_automation": True,
        "cancellation_path": "Profile > Account > Cancel Subscription"
    },
    "spotify": {
        "url": "https://www.spotify.com/",
        "trial_period_days": 30,
        "price": "$10.99/month",
        "plan_name": "Spotify Premium",
        "required_fields": ["identity", "email", "card"],
        "supports_automation": True,
        "cancellation_path": "Account > Subscription > Cancel Premium"
    },
    "amazon": {
        "url": "https://www.amazon.com/",
        "trial_period_days": 30,
        "price": "$14.99/month",
        "plan_name": "Amazon Prime",
        "required_fields": ["identity", "email", "card"],
        "supports_automation": True,
        "cancellation_path": "Account > Prime > Manage Membership > End Membership"
    },
    "youtube": {
        "url": "https://www.youtube.com/premium",
        "trial_period_days": 30,
        "price": "$13.99/month",
        "plan_name": "YouTube Premium",
        "required_fields": ["identity", "email", "card"],
        "supports_automation": True,
        "cancellation_path": "Account > Memberships > Cancel Membership"
    }
}

# Agent quotes and information
AGENT_QUOTES = {
    "harry": [
        "Identity is just a construct, man...",
        "I've got the perfect identity for you. Trust me, it's pure.",
        "Names, addresses, birthdays... it's all just data, man.",
        "This identity is so clean you could inject it.",
        "I don't deal in fake IDs, I deal in alternative realities."
    ],
    "mandy": [
        "Need a card? I'm ON IT! RIGHT NOW! LET'S GO!",
        "This card is FIRE! It'll authorize but NEVER charge!",
        "I JUST MADE ANOTHER CARD! WANT IT? IT'S YOURS!",
        "Cards, cards, CARDS! I can't stop making them!",
        "This is the FASTEST card generation you've ever seen!"
    ],
    "xan": [
        "Chill... your email is being created... no stress...",
        "Don't worry... about disposable emails... I got you...",
        "Your digital identity... is safe with me... relax...",
        "Verification emails... are no problem... stay calm...",
        "I'll handle all your email needs... just breathe..."
    ],
    "sal": [
        "I can see the patterns in the website... the flows... they talk to me...",
        "The captchas... they reveal themselves if you just... look beyond...",
        "Let the automation guide you... let it take control...",
        "The website's defenses are just illusions, man... I can walk right through them...",
        "I'm not automating the website... I'm becoming one with it..."
    ],
    "carl": [
        "Need a phone number? I'm your man. *sniff*",
        "SMS verification? Consider it DONE! *sniff*",
        "I can get you a clean number RIGHT NOW! Just ask!",
        "My phone numbers are the BEST in the business!",
        "Need to verify? My numbers ALWAYS work! ALWAYS!"
    ],
    "craig": [
        "Payments are just energy transfers in the cosmic blockchain.",
        "Your wallet and mine - connected through the crypto-verse.",
        "I don't just process payments, I commune with the blockchain spirits.",
        "Every transaction leaves ripples in the digital ether.",
        "The beauty of crypto is in its immutable truth, man."
    ]
}

# Agent names and themes
AGENT_NAMES = {
    "harry": "Heroin Harry",      # Identity generation
    "mandy": "Meth Mandy",        # Card generation
    "xan": "Xanny Xan",           # Email generation
    "sal": "Shroomy Sal",         # Browser automation
    "carl": "Cokehead Carl",      # SMS/Phone verification
    "craig": "Crypto Craig"       # Payment processing
}

# Define events
@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord"""
    logger.info(f"Trial Junkie Bot connected as {bot.user.name} (ID: {bot.user.id})")
    logger.info(f"Connected to {len(bot.guilds)} guilds")
    
    # Set bot activity
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="for /guide commands"
        )
    )

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Type `/guide` for a list of commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Invalid argument: {error}")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send(f"An error occurred: {error}")

# Helper functions
async def check_user_limit(user_id):
    """
    Check if a user has already used their trial
    
    Args:
        user_id (int): The Discord user ID
        
    Returns:
        bool: True if the user is allowed to create a trial, False otherwise
    """
    # Check if user has already used their trial
    if user_id in USER_TRIAL_LIMITS:
        return False
    
    # User hasn't used their trial yet, allow it
    return True

def save_user_trial(user_id, service, trial_info):
    """
    Save a user's trial information
    
    Args:
        user_id (int): The Discord user ID
        service (str): The service name
        trial_info (dict): The trial information
    """
    USER_TRIAL_LIMITS[user_id] = {
        'service': service,
        'created_at': datetime.now().isoformat(),
        'trial_info': trial_info
    }
    
    # Also save to a file for persistence
    try:
        # Create a unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"discord_message_{user_id}_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            json.dump({
                'user_id': user_id,
                'service': service,
                'created_at': datetime.now().isoformat(),
                'trial_info': trial_info
            }, f, indent=2)
        
        logger.info(f"User trial saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving user trial to file: {str(e)}")

# Define commands
@bot.command(name="guide")
async def guide_command(ctx):
    """Display help information"""
    embed = discord.Embed(
        title="Trial Junkie Help",
        description="Your guide to digital service trials",
        color=0x6f42c1
    )
    
    # Trial commands
    embed.add_field(
        name="🔥 Trial Commands",
        value=(
            "`/hit [service]` - Full trial setup\n"
            "`/dose [agent] [type]` - Single resource generation\n"
            "`/trip [url]` - Run automation on custom URL\n"
            "`/stash` - View your generated items\n"
            "`/rehab` - Clear your data"
        ),
        inline=False
    )
    
    # Fun commands
    embed.add_field(
        name="😎 Agent Commands",
        value=(
            "`/quote [agent]` - Get a quote from an agent\n"
            "`/agents` - View all agents"
        ),
        inline=False
    )
    
    # Admin commands
    embed.add_field(
        name="🔑 Admin Commands",
        value=(
            "`/admin login [username] [password]` - Log in as admin\n"
            "`/admin reset [user_id]` - Reset a user's trial limit"
        ),
        inline=False
    )
    
    embed.set_footer(text="Trial Junkie - Get your digital fix")
    await ctx.send(embed=embed)

@bot.command(name="hit")
async def hit_command(ctx, *, service: str = None):
    """Full trial setup command"""
    if not service:
        await ctx.send("Please specify a service (e.g., `/hit hulu`)")
        return
    
    # Normalize service name
    service = service.lower()
    
    # Check if service is supported
    if service not in TRIAL_SERVICES:
        await ctx.send(f"Service '{service}' is not supported. Available services: {', '.join(TRIAL_SERVICES.keys())}")
        return
    
    # Check if user has already created a trial
    user_id = ctx.author.id
    if not await check_user_limit(user_id):
        embed = discord.Embed(
            title="Trial Limit Reached",
            description="⚠️ You have already created a trial. Each user can only create one trial.",
            color=COLORS["warning"]
        )
        embed.add_field(
            name="Need More?",
            value="Contact an administrator to reset your limit.",
            inline=False
        )
        await ctx.send(embed=embed)
        return
    
    # Log the command
    logger.info(f"User {user_id} ({ctx.author.name}) executed /hit with service: {service}")
    
    # Send initial message
    embed = discord.Embed(
        title="Trial Generation Started",
        description=f"🌐 Running full trial setup for service: {service.upper()}",
        color=COLORS["info"]
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
    message = await ctx.send(embed=embed)
    
    # Generate the trial
    if service == "hulu":
        # Create the trial generator
        generator = HuluTrialGenerator(headless=True)
        
        try:
            # Try to create a trial
            result = generator.create_trial()
            
            if result['success']:
                # Trial was created successfully
                trial_info = result['trial_info']
                
                # Save the user's trial
                save_user_trial(user_id, service, trial_info)
                
                # Send success message
                success_embed = discord.Embed(
                    title="Trial Generation Complete",
                    description=f"✅ Your {service.upper()} trial is ready!",
                    color=COLORS["success"]
                )
                
                # Add credentials
                success_embed.add_field(
                    name="📧 Login Email",
                    value=f"{trial_info['email']}",
                    inline=True
                )
                
                success_embed.add_field(
                    name="🔑 Password",
                    value=f"{trial_info['password']}",
                    inline=True
                )
                
                success_embed.add_field(
                    name="💳 Card Used",
                    value=f"{trial_info['card']}",
                    inline=False
                )
                
                success_embed.add_field(
                    name="⏱️ Expires",
                    value=f"{trial_info['end_date']}",
                    inline=False
                )
                
                success_embed.add_field(
                    name="🔍 Note",
                    value="Use `/stash` to view your saved credentials anytime.",
                    inline=False
                )
                
                success_embed.set_footer(text="Trial Junkie - Get your digital fix")
                await ctx.send(embed=success_embed)
            else:
                # Trial creation failed
                error_embed = discord.Embed(
                    title="Trial Generation Failed",
                    description=f"❌ Failed to create {service.upper()} trial",
                    color=COLORS["error"]
                )
                
                error_embed.add_field(
                    name="Error Message",
                    value=result['message'],
                    inline=False
                )
                
                error_embed.add_field(
                    name="What Next?",
                    value="Try again later or contact an administrator for help.",
                    inline=False
                )
                
                await ctx.send(embed=error_embed)
        
        except Exception as e:
            logger.error(f"Error creating trial: {str(e)}")
            
            # Send error message
            error_embed = discord.Embed(
                title="Error Creating Trial",
                description=f"❌ An error occurred while creating your {service.upper()} trial",
                color=COLORS["error"]
            )
            
            error_embed.add_field(
                name="Error Details",
                value=str(e),
                inline=False
            )
            
            await ctx.send(embed=error_embed)
    else:
        # For other services (not implemented yet)
        await ctx.send(f"Service '{service}' is supported but not yet implemented.")

@bot.command(name="stash")
async def stash_command(ctx):
    """View user's generated items"""
    user_id = ctx.author.id
    
    # Check if user has any trials
    if user_id not in USER_TRIAL_LIMITS:
        embed = discord.Embed(
            title="No Trials Found",
            description="You haven't generated any trials yet. Use `/hit [service]` to create one.",
            color=COLORS["warning"]
        )
        await ctx.send(embed=embed)
        return
    
    # Get the user's trial information
    user_trial = USER_TRIAL_LIMITS[user_id]
    trial_info = user_trial['trial_info']
    service = user_trial['service']
    
    # Create embed for trial information
    embed = discord.Embed(
        title=f"Your {service.upper()} Trial",
        description="Here are your saved trial credentials:",
        color=COLORS["info"]
    )
    
    # Add credentials
    embed.add_field(
        name="📧 Login Email",
        value=f"{trial_info['email']}",
        inline=True
    )
    
    embed.add_field(
        name="🔑 Password",
        value=f"{trial_info['password']}",
        inline=True
    )
    
    embed.add_field(
        name="💳 Payment Method",
        value=f"{trial_info['card']}",
        inline=False
    )
    
    embed.add_field(
        name="⏱️ Expires",
        value=f"{trial_info['end_date']}",
        inline=True
    )
    
    embed.add_field(
        name="🌐 Login URL",
        value=f"{trial_info['login_url']}",
        inline=True
    )
    
    embed.add_field(
        name="📝 Note",
        value="Remember to cancel before the trial ends to avoid charges.",
        inline=False
    )
    
    embed.set_footer(text=f"Created on: {user_trial['created_at']}")
    await ctx.send(embed=embed)

@bot.command(name="rehab")
async def rehab_command(ctx):
    """Clear user data"""
    user_id = ctx.author.id
    
    # Check if user has any trials
    if user_id not in USER_TRIAL_LIMITS:
        embed = discord.Embed(
            title="No Data to Clear",
            description="You don't have any stored trial data.",
            color=COLORS["info"]
        )
        await ctx.send(embed=embed)
        return
    
    # Ask for confirmation
    embed = discord.Embed(
        title="Confirm Data Deletion",
        description="Are you sure you want to delete all your trial data? This action cannot be undone.",
        color=COLORS["warning"]
    )
    embed.add_field(
        name="Respond Within 30 Seconds",
        value="React with ✅ to confirm or ❌ to cancel",
        inline=False
    )
    
    # Send confirmation message
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    
    # Check for user's reaction
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == message.id
    
    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
        
        if str(reaction.emoji) == "✅":
            # User confirmed, delete the data
            if user_id in USER_TRIAL_LIMITS:
                del USER_TRIAL_LIMITS[user_id]
            
            embed = discord.Embed(
                title="Data Deleted",
                description="All your trial data has been deleted successfully.",
                color=COLORS["success"]
            )
            await ctx.send(embed=embed)
        else:
            # User cancelled
            embed = discord.Embed(
                title="Operation Cancelled",
                description="Your data was not deleted.",
                color=COLORS["info"]
            )
            await ctx.send(embed=embed)
    
    except asyncio.TimeoutError:
        # User didn't respond in time
        embed = discord.Embed(
            title="Operation Timed Out",
            description="You didn't respond in time. Your data was not deleted.",
            color=COLORS["warning"]
        )
        await ctx.send(embed=embed)

@bot.command(name="quote")
async def quote_command(ctx, agent: str = None):
    """Get a random quote from an agent"""
    agent_keys = list(AGENT_QUOTES.keys())
    
    if not agent:
        # Random agent if none specified
        agent = random.choice(agent_keys)
    else:
        agent = agent.lower()
        if agent not in agent_keys:
            await ctx.send(f"Agent not found. Try one of: {', '.join(agent_keys)}")
            return
    
    # Get the agent's icon
    agent_icons = {
        "harry": "💉",
        "mandy": "💨",
        "xan": "💊",
        "sal": "🍄",
        "carl": "❄️",
        "craig": "💸"
    }
    
    # Get a random quote
    quote = random.choice(AGENT_QUOTES[agent])
    
    # Build and send the embed
    embed = discord.Embed(
        title=f"{agent_icons.get(agent, '🔮')} {AGENT_NAMES.get(agent, agent.title())} says:",
        description=f"*\"{quote}\"*",
        color=0x9c27b0
    )
    
    embed.set_footer(text="Trial Junkie - Words of wisdom from the street")
    await ctx.send(embed=embed)

@bot.command(name="agents")
async def agents_command(ctx):
    """Display information about all agents"""
    embed = discord.Embed(
        title="Trial Junkie Agents",
        description="Meet the specialized agents that power Trial Junkie",
        color=0xff9800
    )
    
    # Add fields for each agent
    embed.add_field(
        name="💉 Heroin Harry - Identity Specialist",
        value="Generates realistic identities using Personator API for verification.",
        inline=False
    )
    
    embed.add_field(
        name="💨 Meth Mandy - Card Generator",
        value="Creates valid credit card information using Fake Valid CC Data Generator API.",
        inline=False
    )
    
    embed.add_field(
        name="💊 Xanny Xan - Email Specialist",
        value="Validates emails with Advanced Email Validator API and checks for disposable emails.",
        inline=False
    )
    
    embed.add_field(
        name="❄️ Cokehead Carl - Phone Verifier",
        value="Validates phone numbers using Veriphone API and Abstract Phone Validation API.",
        inline=False
    )
    
    embed.add_field(
        name="🍄 Shroomy Sal - Automation Expert",
        value="Handles browser automation with ScrapeNinja API for bypassing website protections.",
        inline=False
    )
    
    embed.add_field(
        name="💸 Crypto Craig - Payment Processor",
        value="Manages Solana wallet transactions for subscriptions.",
        inline=False
    )
    
    embed.set_footer(text="Trial Junkie - Get your digital fix")
    await ctx.send(embed=embed)

@bot.command(name="admin")
async def admin_command(ctx, action: str = None, *args):
    """Admin commands"""
    if not action:
        await ctx.send("Please specify an admin action. Use `/guide` to see available commands.")
        return
    
    action = action.lower()
    
    if action == "login":
        # Admin login
        if len(args) != 2:
            await ctx.send("Invalid syntax. Use `/admin login [username] [password]`")
            return
        
        username, password = args
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            # Successful login
            embed = discord.Embed(
                title="Admin Access Granted",
                description="You now have access to admin commands.",
                color=COLORS["success"]
            )
            # DM the user instead of sending to the channel for security
            await ctx.author.send(embed=embed)
            
            # Delete the command message to hide credentials
            try:
                await ctx.message.delete()
            except:
                pass
        else:
            # Failed login
            embed = discord.Embed(
                title="Admin Access Denied",
                description="Invalid username or password.",
                color=COLORS["error"]
            )
            await ctx.author.send(embed=embed)
            
            # Delete the command message to hide credentials
            try:
                await ctx.message.delete()
            except:
                pass
    
    elif action == "reset":
        # Reset a user's trial limit
        if len(args) != 1:
            await ctx.send("Invalid syntax. Use `/admin reset [user_id]`")
            return
        
        try:
            target_user_id = int(args[0])
        except ValueError:
            await ctx.send("Invalid user ID. User ID must be a number.")
            return
        
        # Check if the requesting user is an admin
        # For simplicity, we're just checking username/password here
        # In a real implementation, you might want to track admin status
        await ctx.send("Please enter admin credentials in a direct message")
        
        def check(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)
        
        try:
            # Wait for DM with credentials
            await ctx.author.send("Please enter admin username:")
            username_msg = await bot.wait_for("message", timeout=60.0, check=check)
            username = username_msg.content
            
            await ctx.author.send("Please enter admin password:")
            password_msg = await bot.wait_for("message", timeout=60.0, check=check)
            password = password_msg.content
            
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                # Valid admin credentials, reset the user's limit
                if target_user_id in USER_TRIAL_LIMITS:
                    del USER_TRIAL_LIMITS[target_user_id]
                
                embed = discord.Embed(
                    title="User Reset Successful",
                    description=f"User ID {target_user_id} has been reset and can now create a new trial.",
                    color=COLORS["success"]
                )
                await ctx.send(embed=embed)
                
                # Confirm in DM too
                await ctx.author.send("Reset successful.")
            else:
                # Invalid credentials
                await ctx.author.send("Invalid admin credentials. Access denied.")
        
        except asyncio.TimeoutError:
            await ctx.author.send("Timed out waiting for credentials.")
    
    else:
        await ctx.send(f"Unknown admin action: '{action}'. Use `/guide` to see available commands.")

async def main():
    """Run the Discord bot"""
    await bot.start(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())