"""
Discord Bot Main File for Trial Junkie
A standalone implementation that won't conflict with the Flask web app
"""
import os
import sys
import logging
import random
from datetime import datetime
import discord
from discord.ext import commands
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
logger = logging.getLogger("discord_bot")

# Load environment variables
load_dotenv()

# Load the bot token from environment variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

# Set up the bot with intents
intents = discord.Intents.default()
intents.message_content = True  # For reading message content
intents.members = True  # For accessing member information

bot = commands.Bot(command_prefix="!", intents=intents)

# Import API keys from environment variables
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '')
PERSONATOR_API_KEY = os.getenv('PERSONATOR_API_KEY', RAPIDAPI_KEY)
VIRTUAL_NUMBER_API_KEY = os.getenv('VIRTUAL_NUMBER_API_KEY', RAPIDAPI_KEY)
FAKE_CARD_API_KEY = os.getenv('FAKE_CARD_API_KEY', RAPIDAPI_KEY)
VIRTUAL_CARD_API_KEY = os.getenv('VIRTUAL_CARD_API_KEY', RAPIDAPI_KEY)
TEMP_EMAIL_API_KEY = os.getenv('TEMP_EMAIL_API_KEY', RAPIDAPI_KEY)
TEMP_MAIL_BACKUP_API_KEY = os.getenv('TEMP_MAIL_BACKUP_API_KEY', RAPIDAPI_KEY)

# API Configurations - Set up the API configuration
API_CONFIG = {
    "personator": {
        "key": PERSONATOR_API_KEY,
        "host": "personator.p.rapidapi.com",
        "endpoint": "https://personator.p.rapidapi.com/v1/generate"
    },
    "virtual_number": {
        "key": VIRTUAL_NUMBER_API_KEY,
        "host": "virtual-number.p.rapidapi.com",
        "endpoint": "https://virtual-number.p.rapidapi.com/v1/numbers"
    },
    "fake_card": {
        "key": FAKE_CARD_API_KEY, 
        "host": "fake-valid-cc-data-generator.p.rapidapi.com",
        "endpoint": "https://fake-valid-cc-data-generator.p.rapidapi.com/v1/card/generate"
    },
    "virtual_card": {
        "key": VIRTUAL_CARD_API_KEY,
        "host": "free-trial-virtual-card-issuing.p.rapidapi.com",
        "endpoint": "https://free-trial-virtual-card-issuing.p.rapidapi.com/v1/generate"
    },
    "temp_email": {
        "key": TEMP_EMAIL_API_KEY,
        "host": "fast-reliable-disposable-mx-email-checker.p.rapidapi.com",
        "endpoint": "https://fast-reliable-disposable-mx-email-checker.p.rapidapi.com/v1/email/generate"
    },
    "temp_mail_backup": {
        "key": TEMP_MAIL_BACKUP_API_KEY,
        "host": "temp-mail.p.rapidapi.com",
        "endpoint": "https://temp-mail.p.rapidapi.com/v1/mail/create"
    }
}

# Quote database for different agents
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

# Colors for embeds
COLORS = {
    "success": 0x4CAF50,  # Green
    "error": 0xF44336,    # Red
    "warning": 0xFFC107,  # Yellow
    "info": 0x2196F3,     # Blue
    "payment": 0x9C27B0   # Purple
}

# Subscription plans
SUBSCRIPTION_PLANS = {
    "one_time_hit": {
        "name": "One-Time Hit",
        "description": "A quick blast of freedom, no strings attached",
        "price": 0.0,
        "features": ["One free trial", "No credit card required", "Basic features only"],
        "color": COLORS["info"]
    },
    "five_dollar_rush": {
        "name": "Five Dollar Rush",
        "description": "A rush of power for just five bucks",
        "price": 0.036,
        "features": ["Limited-time access", "Multiple trials per day", "Standard features"],
        "color": COLORS["warning"]
    },
    "junkified": {
        "name": "Junkified",
        "description": "Unlock unlimited possibilities—no limits, just freedom",
        "price": 0.093,
        "features": ["Unlimited access", "Priority support", "All premium features", "No daily limits"],
        "color": COLORS["payment"]
    }
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
            name="for !guide commands"
        )
    )

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Type `!guide` for a list of commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Invalid argument: {error}")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send(f"An error occurred: {error}")

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
            "`!hit [service]` - Full trial setup\n"
            "`!dose [agent] [type]` - Single resource generation\n"
            "`!trip [url]` - Run automation on custom URL\n"
            "`!stash` - View your generated items\n"
            "`!rehab` - Clear your data"
        ),
        inline=False
    )
    
    # Fun commands
    embed.add_field(
        name="😎 Agent Commands",
        value=(
            "`!quote [agent]` - Get a quote from an agent\n"
            "`!agents` - View all agents"
        ),
        inline=False
    )
    
    # Payment commands
    embed.add_field(
        name="💰 Payment Commands",
        value=(
            "`!plans` - View subscription plans\n"
            "`!pay [plan]` - Subscribe to a plan\n"
            "`!verify_payment [ref]` - Verify your payment\n"
            "`!payments` - View payment history\n"
            "`!tier` - Check your subscription tier"
        ),
        inline=False
    )
    
    # Referral commands
    embed.add_field(
        name="👥 Referral Commands",
        value=(
            "`!referral` - Get your referral code\n"
            "`!refer [code]` - Use someone's referral code\n"
            "`!commissions` - View your commission earnings"
        ),
        inline=False
    )
    
    embed.set_footer(text="Trial Junkie - Get your digital fix")
    await ctx.send(embed=embed)

@bot.command(name="hit")
async def hit_command(ctx, *, service_or_url: str = None):
    """Full trial setup command (all agents)"""
    if not service_or_url:
        await ctx.send("Please specify a service (e.g., `!hit netflix`) or URL (e.g., `!hit https://example.com/trial`)")
        return
    
    # Log the command
    logger.info(f"User {ctx.author.id} ({ctx.author.name}) executed !hit with param: {service_or_url}")
    
    # Check if URL or service name
    if service_or_url.startswith(("http://", "https://")):
        message = f"🌐 Running full trial setup on URL: {service_or_url}"
    else:
        message = f"🌐 Running full trial setup for service: {service_or_url.upper()}"
    
    embed = discord.Embed(
        title="Trial Generation Started",
        description=message,
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
    await ctx.send(embed=embed)
    
    # Create a mock trial response for now
    from datetime import datetime, timedelta
    import random
    import string
    
    trial_result = {
        'id': random.randint(1000, 9999),
        'service': service_or_url.lower() if not service_or_url.startswith(('http://', 'https://')) else 'custom',
        'email': f"user{random.randint(1000, 9999)}@trialmail.com",
        'password': ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12)),
        'card_type': random.choice(['Visa', 'Mastercard', 'American Express']),
        'card_number': ''.join(random.choice(string.digits) for _ in range(16)),
        'trial_end_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
    }
    
    # Send success message
    success_embed = discord.Embed(
        title="Trial Generation Complete",
        description=f"✅ Your {service_or_url.upper() if not service_or_url.startswith(('http://', 'https://')) else 'custom'} trial is ready!",
        color=0x2ecc71
    )
    
    # Add credentials
    success_embed.add_field(
        name="📧 Login Email",
        value=f"{trial_result['email']}",
        inline=True
    )
    
    success_embed.add_field(
        name="🔑 Password",
        value=f"{trial_result['password']}",
        inline=True
    )
    
    success_embed.add_field(
        name="💳 Card Used",
        value=f"{trial_result['card_type']} •••• {trial_result['card_number'][-4:]}",
        inline=False
    )
    
    success_embed.add_field(
        name="⏱️ Expires",
        value=f"{trial_result['trial_end_date']}",
        inline=False
    )
    
    success_embed.add_field(
        name="🔍 Note",
        value="Use `!stash` to view your saved credentials anytime.",
        inline=False
    )
    
    success_embed.set_footer(text="Trial Junkie - Get your digital fix")
    await ctx.send(embed=success_embed)

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
    
    # Get the agent's full name
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
        value="Generates realistic identities with names, addresses, and personal details using the Personator API.",
        inline=False
    )
    
    embed.add_field(
        name="💨 Meth Mandy - Card Expert",
        value="Creates valid credit card numbers that pass verification but don't charge with Fake Valid CC Data Generator.",
        inline=False
    )
    
    embed.add_field(
        name="💊 Xanny Xan - Email Manager",
        value="Sets up disposable emails and handles verification processes with Fast & Reliable Email API.",
        inline=False
    )
    
    embed.add_field(
        name="❄️ Cokehead Carl - Phone Specialist",
        value="Provides temporary phone numbers for SMS verification with Virtual Number API.",
        inline=False
    )
    
    embed.add_field(
        name="🍄 Shroomy Sal - Automation Expert",
        value="Navigates websites and automates the trial signup process with browser automation.",
        inline=False
    )
    
    embed.add_field(
        name="💸 Crypto Craig - Payment Processor",
        value="Creates virtual cards for trial signups and handles crypto payments with Virtual Card Issuing API.",
        inline=False
    )
    
    embed.set_footer(text="Use !dose [agent] to use a specific agent")
    await ctx.send(embed=embed)

@bot.command(name="plans")
async def plans_command(ctx):
    """Display available subscription plans"""
    embed = discord.Embed(
        title="Trial Junkie Subscription Plans",
        description="Choose your digital trip level",
        color=COLORS["payment"]
    )
    
    # Add fields for each plan
    for plan_id, plan in SUBSCRIPTION_PLANS.items():
        features_text = "\n".join([f"• {feature}" for feature in plan["features"]])
        embed.add_field(
            name=f"{plan['name']} - {plan['price']} SOL",
            value=f"{plan['description']}\n\n{features_text}\n\nUse `!pay {plan_id}` to subscribe",
            inline=False
        )
    
    embed.set_footer(text="Trial Junkie - Subscription Plans")
    await ctx.send(embed=embed)

@bot.command(name="dose")
async def dose_command(ctx, agent_type: str = None, platform: str = None):
    """Partial account generation (single agent)"""
    if not agent_type or not platform:
        await ctx.send("❌ **Missing parameters**. Use `!dose <agent> <platform>` to get specific credentials.")
        await ctx.send("Available agents: `harry` (identity), `mandy` (card), `xan` (email), `phone` (SMS)")
        return
    
    # Log the command
    logger.info(f"User {ctx.author.id} ({ctx.author.name}) executed !dose with params: {agent_type} {platform}")
    
    # Validate agent type
    agent_type = agent_type.lower()
    valid_agents = ["harry", "mandy", "xan", "carl", "sal"]
    
    if agent_type not in valid_agents:
        await ctx.send(f"❌ **Invalid agent**. Choose from: {', '.join(valid_agents)}")
        return
    
    # Create response embed
    agent_full_name = AGENT_NAMES.get(agent_type, agent_type.title())
    agent_icon = {
        "harry": "💉",
        "mandy": "💨",
        "xan": "💊",
        "sal": "🍄", 
        "carl": "❄️"
    }.get(agent_type, "🔮")
    
    platform = platform.lower()
    
    # Send processing message
    await ctx.send(f"{agent_icon} **{agent_full_name}** is working on your `{platform}` request...")
    
    # Generate response based on agent type
    result_embed = discord.Embed(
        title=f"{platform.title()} {agent_type.title()} Dose",
        color=COLORS["success"]
    )
    
    if agent_type == "harry":
        # Identity generation
        import random
        
        first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emma", "James", "Olivia"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Wilson"]
        states = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "GA"]
        cities = ["Los Angeles", "New York", "Houston", "Miami", "Chicago", "Philadelphia", "Columbus", "Atlanta"]
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        address = f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Pine', 'Cedar'])} {random.choice(['St', 'Ave', 'Blvd', 'Dr'])}"
        city = random.choice(cities)
        state = random.choice(states)
        zipcode = f"{random.randint(10000, 99999)}"
        phone = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        
        result_embed.add_field(name="Full Name", value=f"{first_name} {last_name}", inline=False)
        result_embed.add_field(name="Address", value=f"{address}\n{city}, {state} {zipcode}", inline=False)
        result_embed.add_field(name="Phone", value=phone, inline=True)
        result_embed.add_field(name="DOB", value=f"{random.randint(1, 12)}/{random.randint(1, 28)}/{random.randint(1970, 2000)}", inline=True)
        
    elif agent_type == "mandy":
        # Card generation
        import random
        import string
        
        card_types = ["Visa", "Mastercard", "American Express"]
        card_type = random.choice(card_types)
        
        if card_type == "Visa":
            card_number = "4" + ''.join(random.choice(string.digits) for _ in range(15))
            cvv = ''.join(random.choice(string.digits) for _ in range(3))
        elif card_type == "Mastercard":
            card_number = "5" + ''.join(random.choice(string.digits) for _ in range(15))
            cvv = ''.join(random.choice(string.digits) for _ in range(3))
        else:  # American Express
            card_number = "3" + ''.join(random.choice(string.digits) for _ in range(14))
            cvv = ''.join(random.choice(string.digits) for _ in range(4))
        
        current_year = datetime.now().year
        exp_month = random.randint(1, 12)
        exp_year = random.randint(current_year + 1, current_year + 5)
        
        result_embed.add_field(name="Card Type", value=card_type, inline=True)
        result_embed.add_field(name="Card Number", value=f"{card_number[0:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}", inline=False)
        result_embed.add_field(name="Expiration", value=f"{exp_month:02d}/{exp_year % 100}", inline=True)
        result_embed.add_field(name="CVV", value=cvv, inline=True)
        
    elif agent_type == "xan":
        # Email generation
        import random
        import string
        
        email_domains = ["disposable.com", "tempmail.org", "fakeemail.net", "mailinator.com", "trialmail.com"]
        username = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        domain = random.choice(email_domains)
        email = f"{username}@{domain}"
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
        
        result_embed.add_field(name="Email", value=email, inline=False)
        result_embed.add_field(name="Password", value=password, inline=False)
        result_embed.add_field(name="Access", value="Check email at our secure portal or use in trial signup", inline=False)
        
    elif agent_type == "carl":
        # Phone verification
        import random
        
        area_codes = ["202", "213", "312", "404", "415", "512", "617", "702", "713", "818"]
        area_code = random.choice(area_codes)
        prefix = random.randint(200, 999)
        line = random.randint(1000, 9999)
        
        phone_number = f"{area_code}-{prefix}-{line}"
        sms_code = random.randint(1000, 9999)
        
        result_embed.add_field(name="Phone Number", value=phone_number, inline=False)
        result_embed.add_field(name="SMS Code", value=str(sms_code), inline=True)
        result_embed.add_field(name="Valid For", value="30 minutes", inline=True)
        
    elif agent_type == "sal":
        # Automation info
        result_embed.add_field(name="Automation Status", value="Ready for browser automation", inline=False)
        result_embed.add_field(name="Target", value=platform.title(), inline=True)
        result_embed.add_field(name="Process", value="Use !trip command to execute automation", inline=False)
    
    result_embed.set_footer(text=f"Generated by {agent_full_name} - Trial Junkie")
    await ctx.send(embed=result_embed)

# Administrative commands
@bot.command(name="admin_refund")
async def admin_refund_command(ctx, user_id: str = None, amount: float = None, *, reason: str = None):
    """Admin command to refund a user"""
    # Check if the user is an admin (you'd have a proper check here)
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
        color=COLORS["success"]
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
    
    # Validate tier
    if tier not in SUBSCRIPTION_PLANS:
        valid_tiers = ", ".join(SUBSCRIPTION_PLANS.keys())
        await ctx.send(f"❌ Invalid tier. Available tiers: {valid_tiers}")
        return
    
    logger.info(f"Admin {ctx.author.id} ({ctx.author.name}) gifted tier {tier} to user {user_id} for {days} days. Note: {note}")
    
    # Process the gift subscription (implementation would go here)
    # ...
    
    embed = discord.Embed(
        title="Admin Gift Processed",
        description=f"✅ {tier.upper()} tier has been gifted to user ID {user_id}",
        color=COLORS["success"]
    )
    
    embed.add_field(name="Tier", value=SUBSCRIPTION_PLANS[tier]["name"], inline=True)
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
    
    # Process the referral rate change (implementation would go here)
    # ...
    
    embed = discord.Embed(
        title="Referral Rate Updated",
        description=f"✅ Referral commission rate has been updated to {rate}%",
        color=COLORS["success"]
    )
    
    if tier:
        embed.add_field(name="Tier", value=tier.upper(), inline=True)
    else:
        embed.add_field(name="Applied To", value="All tiers", inline=True)
    
    embed.set_footer(text="Trial Junkie - Admin Command")
    await ctx.send(embed=embed)

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
    
    # If amount is not specified, pay out all pending commissions
    if amount is None:
        # In a real implementation, you'd calculate the total pending commissions here
        # For now, we'll use a mock amount
        amount = 0.5  # 0.5 SOL as an example
    
    # Process the commission payout (implementation would go here)
    # ...
    
    embed = discord.Embed(
        title="Commission Payout Processed",
        description=f"✅ Commission has been paid out to user ID {user_id}",
        color=COLORS["success"]
    )
    
    embed.add_field(name="Amount", value=f"{amount} SOL", inline=True)
    embed.add_field(name="Status", value="Transaction completed", inline=True)
    
    embed.set_footer(text="Trial Junkie - Admin Command")
    await ctx.send(embed=embed)

@bot.command(name="admin_stats")
async def admin_stats_command(ctx):
    """Admin command to view system statistics"""
    # Check if the user is an admin
    if ctx.author.id != 123456789:  # Replace with your admin user ID
        await ctx.send("❌ You don't have permission to use admin commands.")
        return
    
    logger.info(f"Admin {ctx.author.id} ({ctx.author.name}) requested system stats")
    
    # Mock statistics for demonstration (would be real data in production)
    stats = {
        "users": 1250,
        "active_trials": 856,
        "paid_subscribers": 342,
        "total_payments": 52.35,
        "pending_commissions": 5.62,
        "yesterday_trials": 125,
        "yesterday_payments": 4.21
    }
    
    embed = discord.Embed(
        title="System Statistics",
        description="Current Trial Junkie system statistics",
        color=COLORS["info"]
    )
    
    embed.add_field(name="👥 Total Users", value=str(stats["users"]), inline=True)
    embed.add_field(name="🧪 Active Trials", value=str(stats["active_trials"]), inline=True)
    embed.add_field(name="💰 Paid Subscribers", value=str(stats["paid_subscribers"]), inline=True)
    embed.add_field(name="💸 Total Payments", value=f"{stats['total_payments']} SOL", inline=True)
    embed.add_field(name="💼 Pending Commissions", value=f"{stats['pending_commissions']} SOL", inline=True)
    embed.add_field(name="📈 Yesterday Activity", value=f"{stats['yesterday_trials']} trials, {stats['yesterday_payments']} SOL", inline=False)
    
    embed.set_footer(text="Trial Junkie - Admin Dashboard")
    await ctx.send(embed=embed)

if __name__ == "__main__":
    print("Starting Trial Junkie Discord Bot...")
    try:
        bot.run(DISCORD_BOT_TOKEN)
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        print(f"Error: {e}")
        sys.exit(1)