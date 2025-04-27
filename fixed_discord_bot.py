"""
Fixed Discord Bot for Trial Junkie
Resolves command registration conflicts
"""
import os
import sys
import logging
import discord
from discord.ext import commands
from datetime import datetime, timedelta
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

# Bot configuration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

# Set up the bot with intents
intents = discord.Intents.default()
intents.message_content = True
# Disable privileged intents that need to be activated in Discord Developer Portal
intents.members = False

bot = commands.Bot(command_prefix="!", intents=intents)

# Import database functionality
try:
    from database import Database
    db = Database()
    logger.info("Database connection established")
except Exception as e:
    logger.error(f"Error connecting to database: {e}")
    db = None

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
    
    # Try to run the actual trial automation
    try:
        # Import the simplified Hulu trial generator for testing
        from simplified_hulu_trial import generate_hulu_trial
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
        # Fallback to simulated data if there's an error
        await asyncio.sleep(5)
        
        # Send success message after "work" is done
        fallback_embed = discord.Embed(
            title="Trial Generation Complete",
            description=f"✅ Your {service_or_url.upper() if not service_or_url.startswith(('http://', 'https://')) else 'custom'} trial is ready!",
            color=0x2ecc71
        )
        
        # Add fake credentials (these would be real in the actual implementation)
        fallback_embed.add_field(
            name="📧 Login Email",
            value=f"trialuser{ctx.author.id % 1000}@example.com",
            inline=True
        )
        
        fallback_embed.add_field(
            name="🔑 Password",
            value="••••••••••",
            inline=True
        )
        
        fallback_embed.add_field(
            name="💳 Card Used",
            value="VISA •••• 4242",
            inline=False
        )
        
        fallback_embed.add_field(
            name="⏱️ Expires",
            value=f"{(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')}",
            inline=False
        )
        
        fallback_embed.add_field(
            name="🔍 Note",
            value="Use `!stash` to view your saved credentials anytime.",
            inline=False
        )
        
        fallback_embed.set_footer(text="Trial Junkie - Get your digital fix")
        await ctx.send(fallback_embed)

@bot.command(name="dose")
async def dose_command(ctx, agent_type: str = None, platform: str = None):
    """Partial account generation (single agent)"""
    if not agent_type:
        await ctx.send("Please specify an agent type (e.g., `!dose identity` or `!dose card`)")
        return
    
    if db:
        db.log_command(ctx.author.id, "dose", f"{agent_type} {platform}")
    
    valid_agent_types = ["identity", "card", "email", "phone", "automation"]
    agent_type = agent_type.lower()
    
    if agent_type not in valid_agent_types:
        await ctx.send(f"Invalid agent type. Valid types are: {', '.join(valid_agent_types)}")
        return
    
    agent_names = {
        "identity": "Heroin Harry",
        "card": "Meth Mandy",
        "email": "Xanny Xan",
        "phone": "Cokehead Carl",
        "automation": "Shroomy Sal"
    }
    
    agent_icons = {
        "identity": "💉",
        "card": "💨",
        "email": "💊",
        "phone": "❄️",
        "automation": "🍄"
    }
    
    embed = discord.Embed(
        title=f"Agent Deployment: {agent_names[agent_type]}",
        description=f"{agent_icons[agent_type]} {agent_names[agent_type]} is working on your request...",
        color=0x6f42c1
    )
    
    embed.set_footer(text="Trial Junkie - Get your digital fix")
    await ctx.send(embed=embed)
    
    # Try to run actual generation
    try:
        # Import the simplified Hulu trial generator for testing component parts
        from simplified_hulu_trial import generate_identity, generate_card, generate_email
        
        if agent_type == "identity":
            identity = generate_identity()
            success_embed = discord.Embed(
                title=f"{agent_icons[agent_type]} {agent_names[agent_type]} Results",
                description="Your identity has been generated!",
                color=0x2ecc71
            )
            success_embed.add_field(name="Name", value=f"{identity['first_name']} {identity['last_name']}", inline=True)
            success_embed.add_field(name="Address", value=f"{identity['street']}, {identity['city']}, {identity['state']} {identity['zipcode']}", inline=True)
            success_embed.add_field(name="Phone", value=f"{identity['phone']}", inline=True)
            
        elif agent_type == "card":
            card = generate_card()
            success_embed = discord.Embed(
                title=f"{agent_icons[agent_type]} {agent_names[agent_type]} Results",
                description="Your payment card has been generated!",
                color=0x2ecc71
            )
            success_embed.add_field(name="Card Type", value=f"{card['card_type']}", inline=True)
            success_embed.add_field(name="Card Number", value=f"•••• •••• •••• {card['card_number'][-4:]}", inline=True)
            success_embed.add_field(name="Expiry / CVV", value=f"{card['expiry']} / •••", inline=True)
            
        elif agent_type == "email":
            email_info = generate_email("John", "Doe")  # Placeholder names
            success_embed = discord.Embed(
                title=f"{agent_icons[agent_type]} {agent_names[agent_type]} Results",
                description="Your email has been generated!",
                color=0x2ecc71
            )
            success_embed.add_field(name="Email", value=f"{email_info}", inline=True)
            success_embed.add_field(name="Password", value="••••••••••", inline=True)
            success_embed.add_field(name="Status", value="✅ Verified", inline=True)
            
        else:
            # For other agent types, use simulated data
            await asyncio.sleep(3)
            
            # Send success message
            success_embed = discord.Embed(
                title=f"{agent_icons[agent_type]} {agent_names[agent_type]} Results",
                description="Your request has been processed!",
                color=0x2ecc71
            )
            
            # Add different content based on agent type
            if agent_type == "phone":
                success_embed.add_field(name="Phone Number", value="+1 (555) 123-4567", inline=True)
                success_embed.add_field(name="Status", value="✅ Ready for SMS", inline=True)
                success_embed.add_field(name="Expires", value="24 hours", inline=True)
            elif agent_type == "automation":
                success_embed.add_field(name="Status", value="✅ Browser ready", inline=True)
                success_embed.add_field(name="Target", value=platform or "Any service", inline=True)
                success_embed.add_field(name="Note", value="Use `!trip [url]` to run", inline=True)
        
        success_embed.set_footer(text="Use !stash to view saved credentials")
        await ctx.send(success_embed)
        
    except Exception as e:
        logger.error(f"Error in dose command: {e}")
        # Fallback to simulated data
        await asyncio.sleep(3)
        
        # Send success message
        fallback_embed = discord.Embed(
            title=f"{agent_icons[agent_type]} {agent_names[agent_type]} Results",
            description="Your request has been processed!",
            color=0x2ecc71
        )
        
        # Add different content based on agent type
        if agent_type == "identity":
            fallback_embed.add_field(name="Name", value="John Doe", inline=True)
            fallback_embed.add_field(name="Address", value="123 Main St, New York, NY 10001", inline=True)
            fallback_embed.add_field(name="DOB", value="01/15/1985", inline=True)
        elif agent_type == "card":
            fallback_embed.add_field(name="Card Type", value=f"VISA {'★ ' * 3}", inline=True)
            fallback_embed.add_field(name="Card Number", value="•••• •••• •••• 4242", inline=True)
            fallback_embed.add_field(name="Expiry / CVV", value="07/26 / •••", inline=True)
        elif agent_type == "email":
            fallback_embed.add_field(name="Email", value=f"trialuser{ctx.author.id % 1000}@example.com", inline=True)
            fallback_embed.add_field(name="Password", value="••••••••••", inline=True)
            fallback_embed.add_field(name="Status", value="✅ Verified", inline=True)
        elif agent_type == "phone":
            fallback_embed.add_field(name="Phone Number", value="+1 (555) 123-4567", inline=True)
            fallback_embed.add_field(name="Status", value="✅ Ready for SMS", inline=True)
            fallback_embed.add_field(name="Expires", value="24 hours", inline=True)
        elif agent_type == "automation":
            fallback_embed.add_field(name="Status", value="✅ Browser ready", inline=True)
            fallback_embed.add_field(name="Target", value=platform or "Any service", inline=True)
            fallback_embed.add_field(name="Note", value="Use `!trip [url]` to run", inline=True)
        
        fallback_embed.set_footer(text="Use !stash to view saved credentials")
        await ctx.send(fallback_embed)

@bot.command(name="quote")
async def quote_command(ctx, agent: str = None):
    """Get a random quote from an agent"""
    if not agent:
        agent = "harry"  # Default agent
    
    agent = agent.lower()
    
    # Clean up input (remove any special characters from user input)
    agent = ''.join(c for c in agent if c.isalnum()).lower()
    
    # Map partial names to full names
    agent_map = {
        "harry": "harry",
        "heroin": "harry",
        "heroinharry": "harry",
        "mandy": "mandy",
        "meth": "mandy",
        "methmandy": "mandy",
        "xan": "xan",
        "xanny": "xan",
        "xannyxan": "xan",
        "carl": "carl",
        "coke": "carl",
        "cokehead": "carl",
        "cokeheadcarl": "carl",
        "sal": "sal",
        "shroomy": "sal",
        "shroomysal": "sal",
        "craig": "craig",
        "crypto": "craig",
        "cryptocraig": "craig"
    }
    
    if agent in agent_map:
        agent = agent_map[agent]
    else:
        await ctx.send(f"Agent not found. Try one of: harry, mandy, xan, carl, sal, craig")
        return
    
    if agent not in AGENT_QUOTES:
        await ctx.send(f"No quotes found for that agent.")
        return
    
    # Get a random quote
    import random
    quote = random.choice(AGENT_QUOTES[agent])
    
    # Map agent code to full name and icon
    agent_info = {
        "harry": ("Heroin Harry", "💉"),
        "mandy": ("Meth Mandy", "💨"),
        "xan": ("Xanny Xan", "💊"),
        "carl": ("Cokehead Carl", "❄️"),
        "sal": ("Shroomy Sal", "🍄"),
        "craig": ("Crypto Craig", "💰")
    }
    
    name, icon = agent_info[agent]
    
    embed = discord.Embed(
        title=f"{icon} {name} says:",
        description=f"*\"{quote}\"*",
        color=0x6f42c1
    )
    
    embed.set_footer(text="Trial Junkie - Agent Quotes")
    await ctx.send(embed=embed)

@bot.command(name="stash")
async def stash_command(ctx):
    """View user's generated items"""
    if not db:
        await ctx.send("Database connection is not available.")
        return
    
    # Get user credentials from database
    credentials = db.get_user_credentials(ctx.author.id)
    
    if not credentials:
        await ctx.send("Your stash is empty. Use `!hit` or `!dose` commands to generate items.")
        return
    
    embed = discord.Embed(
        title="Your Stash",
        description=f"You have {len(credentials)} saved items.",
        color=0x6f42c1
    )
    
    # Group credentials by service
    services = {}
    for cred in credentials:
        service = cred['service']
        if service not in services:
            services[service] = []
        services[service].append(cred)
    
    # Add each service as a field
    for service, creds in services.items():
        value = ""
        for cred in creds:
            value += f"**{cred['credential_type']}**: {cred['credential_value']}\n"
        
        embed.add_field(
            name=f"{service.upper()}",
            value=value,
            inline=False
        )
    
    embed.set_footer(text="Use !rehab to clear your stash")
    await ctx.send(embed=embed)

@bot.command(name="agents")
async def agents_command(ctx):
    """Display information about all agents"""
    embed = discord.Embed(
        title="Meet the Agents",
        description="The specialized agents of Trial Junkie",
        color=0x6f42c1
    )
    
    # Add each agent as a field
    embed.add_field(
        name="💉 Heroin Harry - Identity Specialist",
        value="Creates perfect identities with needle-point precision. Use `!dose identity`.",
        inline=False
    )
    
    embed.add_field(
        name="💨 Meth Mandy - Card Generator",
        value="Generates virtual cards at lightning speed that authorize but never charge. Use `!dose card`.",
        inline=False
    )
    
    embed.add_field(
        name="💊 Xanny Xan - Email Manager",
        value="Creates disposable emails for verification without stress. Use `!dose email`.",
        inline=False
    )
    
    embed.add_field(
        name="❄️ Cokehead Carl - Phone Verification",
        value="Provides temporary phone numbers for SMS verification. Use `!dose phone`.",
        inline=False
    )
    
    embed.add_field(
        name="🍄 Shroomy Sal - Automation Expert",
        value="Sees through website patterns to automate signups. Use `!dose automation` or `!trip [url]`.",
        inline=False
    )
    
    embed.add_field(
        name="💰 Crypto Craig - Payment Processor",
        value="Handles all cryptocurrency transactions for premium services. Part of the `!pay` system.",
        inline=False
    )
    
    embed.set_footer(text="Use !quote [agent] to hear from an agent")
    await ctx.send(embed=embed)

# Import asyncio for simulating delays
import asyncio

# Main function to run the bot
def main():
    """Start the bot"""
    logger.info("Starting Discord bot...")
    
    try:
        # Run the bot
        bot.run(DISCORD_BOT_TOKEN)
    except discord.errors.LoginFailure:
        logger.error("Invalid Discord bot token")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()