#!/usr/bin/env python3
"""
Standalone Discord Bot Implementation
A version of the Discord bot that doesn't depend on Flask
"""
import os
import sys
import json
import logging
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("standalone_discord_bot")

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    logger.error("DISCORD_BOT_TOKEN not found in environment variables")
    sys.exit(1)

# Initialize database
db = database.Database()

# Bot configuration
COLORS = {
    "primary": 0x6f42c1,  # Purple
    "success": 0x28a745,  # Green
    "danger": 0xdc3545,   # Red
    "warning": 0xffc107,  # Yellow
    "info": 0x17a2b8      # Blue
}

# Subscription plans configuration
SUBSCRIPTION_PLANS = {
    "free": {
        "name": "Free Tier",
        "price": 0,
        "daily_limit": 3,
        "features": ["Basic trial generation", "Manual copy-paste setup", "Basic identity generation"]
    },
    "basic": {
        "name": "Basic Dealer",
        "price": 0.05,
        "daily_limit": 10,
        "features": ["Advanced trial generation", "Custom identity profiles", "Email & SMS verification", "Basic automation scripts"]
    },
    "premium": {
        "name": "Premium Pusher",
        "price": 0.1,
        "daily_limit": 25,
        "features": ["Max trial generation", "Advanced automation", "Premium support", "Early access to new features"]
    },
    "enterprise": {
        "name": "Cartel Boss",
        "price": 0.25,
        "daily_limit": 100,
        "features": ["Unlimited trials", "Priority automation", "Admin dashboard", "Early access to future agents"]
    }
}

# Agent quotes
AGENT_QUOTES = {
    "harry": [
        "Identity is just a construct, man... let me construct one for you.",
        "I've lived a thousand lives in a thousand cities... which one do you want to borrow?",
        "Need a new face to face the world? I got you covered.",
        "Your digital identity is just waiting to be born... I'm the midwife.",
        "Slip into a new skin... no one will know the difference."
    ],
    "mandy": [
        "Cards, cards, cards... they're just numbers in the system, and I know all the combinations.",
        "Swipe now, worry never. That's the Mandy guarantee.",
        "Need some digital credit? I'm your girl.",
        "Every transaction tells a story. Let's make yours interesting.",
        "My cards are like magic tricks - they work, but don't ask how."
    ],
    "carl": [
        "Ring ring... who's there? Anyone you want it to be.",
        "Numbers are my specialty. Mobile, landline, whatever you need.",
        "Need to take a call? I've got lines all over the world.",
        "SMS verification? Consider it done. No questions asked.",
        "In a world of spam calls, be the one who answers. With my numbers."
    ],
    "xan": [
        "Emails are just digital letters that never get lost in the mail.",
        "Inbox anxiety? Not with my disposable addresses.",
        "Your digital communication, completely untraceable.",
        "Need to sign up for something sketchy? Don't use your real email.",
        "Temporary email, permanent solution."
    ],
    "sal": [
        "I see the patterns in the digital realm... the automation flows through me.",
        "Let me take you on a trip through the automation universe.",
        "Scripts, bots, automation... it's all just a psychedelic dance.",
        "Why do manually what can be done... magically?",
        "The browser is my canvas, and automation is my art."
    ]
}

# Set up the bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Agent info
AGENTS = {
    "harry": {
        "name": "Heroin Harry",
        "full_name": "Heroin Harry",
        "specialty": "Identity Generation",
        "description": "Harry creates realistic identities with all the personal details needed for trials.",
        "emoji": "🥄",
        "power": "Perfect identities that look completely legitimate.",
        "quote": "Identity is just a construct, man... let me construct one for you."
    },
    "mandy": {
        "name": "Meth Mandy",
        "full_name": "Methamphetamine Mandy",
        "specialty": "Payment Methods",
        "description": "Mandy generates valid credit card details that work for trial verifications.",
        "emoji": "💳",
        "power": "Cards that pass verification but don't get charged.",
        "quote": "Cards, cards, cards... they're just numbers in the system, and I know all the combinations."
    },
    "carl": {
        "name": "Cocaine Carl",
        "full_name": "Cocaine Carl",
        "specialty": "Phone Verification",
        "description": "Carl provides virtual phone numbers for SMS verification.",
        "emoji": "📱",
        "power": "Receive verification texts without using your real number.",
        "quote": "Ring ring... who's there? Anyone you want it to be."
    },
    "xan": {
        "name": "Xanax Xan",
        "full_name": "Xanax Xander",
        "specialty": "Email Generation",
        "description": "Xan creates disposable email addresses for signing up and verification.",
        "emoji": "📧",
        "power": "Temporary email addresses with accessible inboxes.",
        "quote": "Inbox anxiety? Not with my disposable addresses."
    },
    "sal": {
        "name": "Shroomy Sal",
        "full_name": "Shroomy Sal",
        "specialty": "Trial Automation",
        "description": "Sal runs automation scripts to set up trials without manual work.",
        "emoji": "🍄",
        "power": "Full end-to-end automation of trial signups.",
        "quote": "Why do manually what can be done... magically?"
    }
}

@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord"""
    logger.info(f"Trial Junkie online as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="!hit | !dose | !stash | !help"))

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

@bot.command(name="help")
async def help_command(ctx):
    """Display help information"""
    embed = discord.Embed(
        title="🧪 Trial Junkie Help",
        description="Your friendly neighborhood dealer for free trials",
        color=COLORS["primary"],
        timestamp=discord.utils.utcnow()
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
    
    # Fun commands
    embed.add_field(
        name="😜 Fun Commands",
        value="`!quote <agent>` - Get a quote from an agent\n`!agents` - Meet the agents\n`!plans` - View subscription plans",
        inline=False
    )
    
    embed.set_footer(text="Trial Junkie | The Last Free Trial You'll Ever Need")
    
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping_command(ctx):
    """Simple ping command to check if the bot is working"""
    await ctx.send(f"Pong! Bot latency: {round(bot.latency * 1000)}ms")

@bot.command(name="quote")
async def quote_command(ctx, agent: str = None):
    """Get a random quote from an agent"""
    if agent:
        agent = agent.lower()
    
    # If no agent specified or invalid agent, pick a random one
    if not agent or agent not in AGENTS:
        agent = random.choice(list(AGENTS.keys()))
    
    # Get a random quote for the agent
    agent_info = AGENTS[agent]
    quote = random.choice(AGENT_QUOTES[agent])
    
    embed = discord.Embed(
        title=f"{agent_info['emoji']} {agent_info['name']} says:",
        description=f"*\"{quote}\"*",
        color=COLORS["primary"]
    )
    
    embed.set_footer(text=f"{agent_info['specialty']} | Trial Junkie")
    
    await ctx.send(embed=embed)

@bot.command(name="agents")
async def agents_command(ctx):
    """Display information about all agents"""
    embed = discord.Embed(
        title="Meet the Agents",
        description="The crew that makes your trials possible",
        color=COLORS["primary"]
    )
    
    for agent_id, agent in AGENTS.items():
        embed.add_field(
            name=f"{agent['emoji']} {agent['name']} - {agent['specialty']}",
            value=f"{agent['description']}\n*\"{agent['quote']}\"*",
            inline=False
        )
    
    embed.set_footer(text="Trial Junkie | The Last Free Trial You'll Ever Need")
    
    await ctx.send(embed=embed)

@bot.command(name="plans")
async def plans_command(ctx):
    """Display available subscription plans"""
    embed = discord.Embed(
        title="Subscription Plans",
        description="Level up your trial game with premium features",
        color=COLORS["primary"]
    )
    
    for plan_id, plan in SUBSCRIPTION_PLANS.items():
        features_text = "\n".join([f"• {feature}" for feature in plan["features"]])
        embed.add_field(
            name=f"{plan['name']} - {plan['price']} SOL/month",
            value=f"Daily limit: {plan['daily_limit']} trials\n{features_text}",
            inline=False
        )
    
    embed.set_footer(text="Use !pay <plan> to subscribe | Trial Junkie")
    
    await ctx.send(embed=embed)

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

def run_bot():
    """Run the Discord bot"""
    try:
        logger.info("Starting Discord bot...")
        bot.run(DISCORD_BOT_TOKEN)
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    """Run the bot when the script is executed directly"""
    run_bot()