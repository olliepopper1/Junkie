"""
Trial Junkie Discord Bot Workflow
This script runs the Discord bot standalone without port conflicts
"""
import os
import sys
import logging
import random
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

# Try to import the database and trial generator
try:
    from database import Database
    db = Database()
    logger.info("Database connection established")
except Exception as e:
    logger.error(f"Error connecting to database: {e}")
    db = None

try:
    from simplified_hulu_trial import generate_hulu_trial, generate_identity, generate_card, generate_email
    logger.info("Trial generator successfully imported")
except Exception as e:
    logger.error(f"Error importing trial generator: {e}")
    
# Bot configuration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

# Set up the bot with intents
intents = discord.Intents.default()
intents.message_content = True  # For reading message content
intents.members = True  # For accessing member information

bot = commands.Bot(command_prefix="!", intents=intents)

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

# Define events
@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord"""
    logger.info(f"Bot connected as {bot.user.name} (ID: {bot.user.id})")
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
    
    if db:
        db.log_command(ctx.author.id, "hit", service_or_url)
    
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
    
    # Run the trial generation
    try:
        trial_result = generate_hulu_trial()
        
        # Send success message with real data
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
        
    except Exception as e:
        logger.error(f"Error generating trial: {e}")
        await ctx.send(f"Error generating trial: {e}")

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
    agent_names = {
        "harry": "Heroin Harry",
        "mandy": "Meth Mandy",
        "xan": "Xanny Xan",
        "sal": "Shroomy Sal",
        "carl": "Cokehead Carl",
        "craig": "Crypto Craig"
    }
    
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
        title=f"{agent_icons.get(agent, '🔮')} {agent_names.get(agent, agent.title())} says:",
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

if __name__ == "__main__":
    print("Starting Trial Junkie Discord Bot (Workflow Version)...")
    print("This is a standalone bot that won't conflict with the web server")
    try:
        bot.run(DISCORD_BOT_TOKEN)
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        print(f"Error: {e}")
        sys.exit(1)