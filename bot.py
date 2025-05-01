"""
Discord Bot Implementation for Trial Junkie
Handles all Discord interactions and commands
"""
import os
import discord
from discord.ext import commands
import logging
import asyncio
import random
from datetime import datetime
from agents.pusher import Pusher
from utils.logger import CommandLogger
from utils.cooldown import Cooldown
from utils.response_templates import get_agent_quote, random_drug_emoji
from database import Database
from config import AGENT_NAMES, COLORS
from commands.trial_commands import TrialCommands

logger = logging.getLogger(__name__)

def setup_bot():
    # Set up intents
    intents = discord.Intents.default()
    intents.message_content = True
    
    # Create the bot with slash commands enabled
    bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)
    
    # Create database connection
    db = Database()
    
    # Create the main pusher agent
    pusher = Pusher(db)
    
    # Create cooldown manager
    cooldown = Cooldown()
    
    # Create command logger
    cmd_logger = CommandLogger()
    
    @bot.event
    async def on_ready():
        """Called when the bot is ready and connected to Discord"""
        logger.info(f"Trial Junkie online as {bot.user}")
        await bot.change_presence(activity=discord.Game(name="/hit | /dose | /stash | /help"))
    
    @bot.event
    async def on_command_error(ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Unknown command. Use `/help` to see available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param}")
        else:
            logger.error(f"Command error: {str(error)}")
            await ctx.send(f"Error: {str(error)}")
    
    @bot.command(name="help")
    async def help_command(ctx):
        """Display help information"""
        embed = discord.Embed(
            title="🧪 Trial Junkie Help",
            description="Your friendly neighborhood dealer for free trials",
            color=COLORS["info"],
            timestamp=datetime.now()
        )
        
        # Main commands
        embed.add_field(
            name="🎯 Hit (Full Trial)",
            value="`/hit <service>` - Generate all credentials for a trial\nExample: `/hit Netflix`",
            inline=False
        )
        
        embed.add_field(
            name="💊 Dose (Single Resource)",
            value="`/dose <agent> <service>` - Generate a specific credential\nAgents: harry (identity), mandy (card), xan (email), carl (phone)\nExample: `/dose harry Spotify`",
            inline=False
        )
        
        embed.add_field(
            name="🍄 Trip (Automation)",
            value="`/trip <script>` - Run an automation script\nExample: `/trip netflix_signup`\nUse `/trip help` for available scripts",
            inline=False
        )
        
        embed.add_field(
            name="🧪 Stash",
            value="`/stash` - View your saved credentials",
            inline=True
        )
        
        embed.add_field(
            name="🏥 Rehab",
            value="`/rehab` - Clear all your data",
            inline=True
        )
        
        # Fun commands
        embed.add_field(
            name="😜 Fun Commands",
            value="`/quote <agent>` - Get a quote from an agent\n`/agents` - Meet the agents\n`/stats` - View usage statistics",
            inline=False
        )
        
        embed.set_footer(text="Trial Junkie | The Last Free Trial You'll Ever Need")
        
        await ctx.send(embed=embed)
        
    @bot.command(name="hit")
    async def hit_command(ctx, *, service_or_url: str = None):
        """Full trial setup command (all agents) - Works with services or URLs"""
        user_id = ctx.author.id
        username = ctx.author.name
        
        # Check cooldown
        if cooldown.is_on_cooldown(user_id, "hit"):
            remaining = cooldown.get_remaining_time(user_id, "hit")
            await ctx.send(f"🔒 **Need to sober up first.** Try again in {remaining} seconds.")
            return
            
        # Check if service was provided
        if not service_or_url:
            from config import TRIAL_SERVICES
            services_list = ", ".join(f"`{service}`" for service in TRIAL_SERVICES.keys())
            
            await ctx.send("❌ **Missing service name or URL**. Use one of these options:")
            await ctx.send(f"1️⃣ **Predefined services:** `/hit <service>` - Available: {services_list}")
            await ctx.send("2️⃣ **Custom website:** `/hit url <website_url>` - Example: `/hit url https://www.example.com/trial`")
            return
            
        # Check if it's a URL-based request
        if service_or_url.lower().startswith("url "):
            url = service_or_url[4:].strip()  # Remove "url " prefix
            
            # Validate URL format
            if not url.startswith("http"):
                await ctx.send("❌ **Invalid URL format.** URL must start with http:// or https://")
                return
                
            # Log command usage
            cmd_logger.log_command(user_id, username, "hit", f"custom_url: {url}")
            
            # Extract domain name for service ID
            try:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc.replace("www.", "").split(".")[0]
                
                # Create temporary configuration
                from config import TRIAL_SERVICES
                
                # Register as temporary service if not already in known services
                if domain not in TRIAL_SERVICES:
                    TRIAL_SERVICES[domain] = {
                        "url": url,
                        "trial_period_days": 14,  # Default assumption
                        "price": "Unknown",
                        "plan_name": f"{domain.capitalize()} Trial",
                        "required_fields": ["identity", "email", "card"],
                        "supports_automation": True,
                        "cancellation_path": "Account Settings",
                        "is_custom": True
                    }
                
                # Send initial response
                await ctx.send(f"💉 **The Pusher** is preparing your `{domain}` trial from {url}... Hold tight.")
                
                # Set cooldown
                cooldown.set_cooldown(user_id, "hit", 300)  # 5 minute cooldown
                
                # Process the request through the pusher
                result = await pusher.process_hit(user_id, username, domain)
                await ctx.send(embed=result)
                
            except Exception as e:
                logger.error(f"Error processing hit command with URL: {e}")
                await ctx.send(f"❌ **Bad batch!** Something went wrong with the URL: {str(e)}")
        else:
            # Standard service hit
            service = service_or_url.lower()
            
            # Log command usage
            cmd_logger.log_command(user_id, username, "hit", service)
            
            # Send initial response
            await ctx.send(f"💉 **The Pusher** is preparing your `{service}` trial... Hold tight.")
            
            # Set cooldown
            cooldown.set_cooldown(user_id, "hit", 300)  # 5 minute cooldown
            
            # Process the request through the pusher
            try:
                result = await pusher.process_hit(user_id, username, service)
                await ctx.send(embed=result)
            except Exception as e:
                logger.error(f"Error processing hit command: {e}")
                await ctx.send(f"❌ **Bad batch!** Something went wrong: {str(e)}")
            
    @bot.command(name="dose")
    async def dose_command(ctx, agent_type: str = None, platform: str = None):
        """Partial account generation (single agent)"""
        user_id = ctx.author.id
        username = ctx.author.name
        
        # Check cooldown
        if cooldown.is_on_cooldown(user_id, "dose"):
            remaining = cooldown.get_remaining_time(user_id, "dose")
            await ctx.send(f"🔒 **Too soon for another hit.** Try again in {remaining} seconds.")
            return
        
        # Check if required params were provided
        if not agent_type or not platform:
            await ctx.send("❌ **Missing parameters**. Use `/dose <agent> <platform>` to get specific credentials.")
            await ctx.send("Available agents: `harry` (identity), `mandy` (card), `xan` (email), `phone` (SMS)")
            return
        
        # Log command usage
        cmd_logger.log_command(user_id, username, "dose", f"{agent_type} {platform}")
        
        # Set cooldown (shorter than full hit)
        cooldown.set_cooldown(user_id, "dose", 60)  # 1 minute cooldown
        
        # Process the dose request
        try:
            result = await pusher.process_dose(user_id, username, agent_type, platform)
            await ctx.send(embed=result)
        except Exception as e:
            logger.error(f"Error processing dose command: {e}")
            await ctx.send(f"❌ **Bad trip!** Something went wrong: {str(e)}")
    
    @bot.command(name="trip")
    async def trip_command(ctx, *, script_or_url: str = None):
        """Run automation scripts for predefined services or custom trial website URLs"""
        user_id = ctx.author.id
        username = ctx.author.name
        
        # Check cooldown
        if cooldown.is_on_cooldown(user_id, "trip"):
            remaining = cooldown.get_remaining_time(user_id, "trip")
            await ctx.send(f"🔒 **You're still tripping.** Try again in {remaining} seconds.")
            return
        
        # Check if script was provided
        if not script_or_url:
            from config import TRIAL_SERVICES
            services_list = ", ".join(f"`{service}`" for service in TRIAL_SERVICES.keys())
            
            await ctx.send("❌ **Missing service name or URL**. Use one of these options:")
            await ctx.send(f"1️⃣ **Predefined services:** `/trip <service>` - Available: {services_list}")
            await ctx.send("2️⃣ **Custom website:** `/trip url <website_url>` - Example: `/trip url https://www.example.com/trial`")
            await ctx.send("3️⃣ **Basic scripts:** `/trip <script>` - Available: `signup`, `verify`, `cancel`")
            return
        
        # Check if it's a custom URL
        if script_or_url.lower().startswith("url "):
            url = script_or_url[4:].strip()  # Remove "url " prefix
            
            # Check if URL is valid
            if not url.startswith("http"):
                await ctx.send("❌ **Invalid URL format.** URL must start with http:// or https://")
                return
                
            # Log command usage
            cmd_logger.log_command(user_id, username, "trip", f"custom_url: {url}")
            
            # Send initial response
            await ctx.send(f"🍄 **Shroomy Sal** is exploring a new trip to `{url}`... Taking you on a guided expedition.")
            
            # Register custom URL as a temporary service
            try:
                # Extract domain name for service ID
                from urllib.parse import urlparse
                domain = urlparse(url).netloc.replace("www.", "").split(".")[0]
                
                # Create temporary configuration
                from config import TRIAL_SERVICES
                
                # Register as temporary service if not already in known services
                if domain not in TRIAL_SERVICES:
                    TRIAL_SERVICES[domain] = {
                        "url": url,
                        "trial_period_days": 14,  # Default assumption
                        "price": "Unknown",
                        "plan_name": f"{domain.capitalize()} Trial",
                        "required_fields": ["identity", "email", "card"],
                        "supports_automation": True,
                        "cancellation_path": "Account Settings",
                        "is_custom": True
                    }
                    
                # Set cooldown
                cooldown.set_cooldown(user_id, "trip", 600)  # 10 minute cooldown
                
                # Process the trip request with the domain as the service name
                result = await pusher.process_trip(user_id, username, domain)
                await ctx.send(embed=result)
                
            except Exception as e:
                logger.error(f"Error processing custom URL trip command: {e}")
                await ctx.send(f"❌ **Bad trip!** Something went wrong with the custom URL: {str(e)}")
                
        else:
            # Regular predefined script or service
            script = script_or_url.lower()
            
            # Log command usage
            cmd_logger.log_command(user_id, username, "trip", script)
            
            # Send initial response
            await ctx.send(f"🍄 **Shroomy Sal** is taking you on a `{script}` trip... Enjoy the ride.")
            
            # Set cooldown
            cooldown.set_cooldown(user_id, "trip", 600)  # 10 minute cooldown
            
            # Process the trip request
            try:
                result = await pusher.process_trip(user_id, username, script)
                await ctx.send(embed=result)
            except Exception as e:
                logger.error(f"Error processing trip command: {e}")
                await ctx.send(f"❌ **Bad trip!** Something went wrong: {str(e)}")
    
    @bot.command(name="stash")
    async def stash_command(ctx):
        """View user's generated items"""
        user_id = ctx.author.id
        username = ctx.author.name
        
        # Log command usage
        cmd_logger.log_command(user_id, username, "stash", "")
        
        # Process the stash request
        try:
            result = await pusher.process_stash(user_id, username)
            await ctx.send(embed=result)
        except Exception as e:
            logger.error(f"Error processing stash command: {e}")
            await ctx.send(f"❌ **Stash is empty!** Something went wrong: {str(e)}")
    
    @bot.command(name="rehab")
    async def rehab_command(ctx):
        """Clear user data"""
        user_id = ctx.author.id
        username = ctx.author.name
        
        # Check cooldown
        if cooldown.is_on_cooldown(user_id, "rehab"):
            remaining = cooldown.get_remaining_time(user_id, "rehab")
            await ctx.send(f"🔒 **Rehab still in progress.** Try again in {remaining} seconds.")
            return
        
        # Log command usage
        cmd_logger.log_command(user_id, username, "rehab", "")
        
        # Set cooldown
        cooldown.set_cooldown(user_id, "rehab", 3600)  # 1 hour cooldown
        
        # Send confirmation message
        confirm_msg = await ctx.send(f"⚠️ **Checking into rehab will clear all your data.** React with ✅ to confirm.")
        await confirm_msg.add_reaction("✅")
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == confirm_msg.id
        
        try:
            # Wait for confirmation (30 seconds timeout)
            reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
            
            # Process the rehab request
            result = await pusher.process_rehab(user_id, username)
            await ctx.send(embed=result)
            
        except TimeoutError:
            await ctx.send("❌ **Rehab canceled** - You changed your mind. Your data is still intact.")
        except Exception as e:
            logger.error(f"Error processing rehab command: {e}")
            await ctx.send(f"❌ **Rehab failed!** Something went wrong: {str(e)}")
    
    @bot.command(name="quote")
    async def quote_command(ctx, agent: str = None):
        """Get a random quote from an agent"""
        if not agent:
            await ctx.send("Please specify an agent. Example: `/quote harry` or use `/agents` to see all agents.")
            return
        
        # Standardize agent name
        agent_aliases = {
            "harry": "harry",
            "h": "harry",
            "heroin": "harry",
            "mandy": "mandy",
            "m": "mandy",
            "meth": "mandy",
            "xan": "xan",
            "x": "xan",
            "xanny": "xan",
            "carl": "carl",
            "c": "carl",
            "coke": "carl",
            "sal": "sal",
            "s": "sal",
            "shroom": "sal",
            "shroomy": "sal",
            "pusher": "pusher",
            "p": "pusher"
        }
        
        std_agent = agent_aliases.get(agent.lower())
        if not std_agent:
            await ctx.send(f"Unknown agent '{agent}'. Use `/agents` to see all agents.")
            return
        
        # Generate quote about random topic
        topics = ["free trials", "subscriptions", "streaming", "credit cards", "online accounts", 
                  "passwords", "identities", "emails", "phone numbers", "verification",
                  "automation", "bots", "discord", "signing up", "getting high on trials"]
        
        topic = random.choice(topics)
        quote = get_agent_quote(std_agent, topic)
        
        # Format with agent emoji
        agent_emoji = {
            "harry": "💉",
            "mandy": "💊",
            "xan": "💊",
            "carl": "⚗️",
            "sal": "🍄",
            "pusher": "🎯"
        }
        emoji = agent_emoji.get(std_agent, "🧪")
        agent_name = AGENT_NAMES.get(std_agent, agent)
        
        await ctx.send(f"{emoji} **{agent_name}**: {quote}")
    
    @bot.command(name="agents")
    async def agents_command(ctx):
        """Display information about all agents"""
        embed = discord.Embed(
            title="🧪 Meet the Agents",
            description="The crew that makes Trial Junkie possible",
            color=COLORS["info"],
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="💉 Heroin Harry",
            value="Identity generation specialist. Need a new you for every trial.",
            inline=False
        )
        
        embed.add_field(
            name="💊 Meth Mandy",
            value="Card generator extraordinaire. Pure, uncut credit cards that always work.",
            inline=False
        )
        
        embed.add_field(
            name="💊 Xanny Xan",
            value="Email address creator. Helping you chill out with disposable addresses.",
            inline=False
        )
        
        embed.add_field(
            name="⚗️ Cokehead Carl",
            value="Phone number specialist. The fastest numbers in the West.",
            inline=False
        )
        
        embed.add_field(
            name="🍄 Shroomy Sal",
            value="Automation wizard. Let Sal guide you through the sign-up trip.",
            inline=False
        )
        
        embed.add_field(
            name="💰 Crypto Craig",
            value="Payment processor. Handles all your Solana transactions with the utmost discretion.",
            inline=False
        )
        
        embed.add_field(
            name="🎯 The Pusher",
            value="Main dealer. Controls all agents and delivers the goods.",
            inline=False
        )
        
        embed.set_footer(text="Use /quote <agent> to hear from your favorite agent")
        
        await ctx.send(embed=embed)
        
    @bot.command(name="plans")
    async def plans_command(ctx):
        """Display available subscription plans"""
        user_id = str(ctx.author.id)
        username = str(ctx.author)
        
        # Show typing indicator
        async with ctx.typing():
            # Create a rich embed for plans
            embed = discord.Embed(
                title="💉 Trial Junkie Subscription Plans 💊",
                description="Choose your level of addiction below:",
                color=COLORS["payment"]
            )
            
            # One-Time Hit (Free Plan)
            embed.add_field(
                name="💨 One-Time Hit (Free)",
                value="A quick blast of freedom, no strings attached.\n" + 
                      "• One-time free trial\n" +
                      "• No credit card required\n" +
                      "• Basic features only\n" +
                      "• `/pay one_time_hit` to activate",
                inline=False
            )
            
            # Five Dollar Rush
            embed.add_field(
                name="💵 Five Dollar Rush ($5)",
                value="A rush of power for just five bucks.\n" + 
                      "• Limited-time access\n" +
                      "• Multiple trials per day\n" +
                      "• Standard features\n" +
                      "• `/pay five_dollar_rush` to purchase",
                inline=False
            )
            
            # 13 Junkified
            embed.add_field(
                name="💎 13 Junkified ($13)",
                value="Unlock unlimited possibilities—no limits, just freedom.\n" + 
                      "• Unlimited access\n" +
                      "• Priority support\n" +
                      "• All premium features\n" +
                      "• No daily limits\n" +
                      "• `/pay junkified` to purchase",
                inline=False
            )
            
            # Add footer
            embed.set_footer(
                text=f"Requested by {username} | All payments in SOL | Use /pay <plan_name> to subscribe",
                icon_url="https://cdn.discordapp.com/embed/avatars/0.png"
            )
            
            # Send the embed
            await ctx.send(embed=embed)
            
            # Log command
            cmd_logger.log_command(user_id, username, "plans", "")
            
            # Add a random quote from Crypto Craig
            crypto_quotes = [
                "Pick your poison carefully. The stronger the dose, the better the high.",
                "First one's free, but the good stuff costs. That's just how the game works.",
                "These plans hit different. Choose based on how deep you wanna go.",
                "Every junkie has their preferred dose. What's yours gonna be?",
                "Quality product for quality customers. I don't cut my services with fillers."
            ]
            await ctx.send(f"💰 **{AGENT_NAMES['craig']}**: {random.choice(crypto_quotes)}")
    
    @bot.command(name="pay")
    async def pay_command(ctx, service_type: str = None):
        """Payment command for services"""
        user_id = str(ctx.author.id)
        username = str(ctx.author)
        
        # Check if user is on cooldown
        if cooldown.is_on_cooldown(user_id, "pay"):
            remaining = cooldown.get_remaining_time(user_id, "pay")
            emoji = random_drug_emoji()
            await ctx.send(f"{emoji} Payment requests are limited. Try again in {remaining} seconds.")
            return
        
        # Validate service type
        valid_services = ["hit", "dose", "trip", "premium", "one_time_hit", "five_dollar_rush", "junkified"]
        if not service_type or service_type.lower() not in valid_services:
            services_str = ", ".join([f"`{s}`" for s in valid_services])
            await ctx.send(f"Please specify a valid service type. Available types: {services_str}\n\nUse `/plans` to see details about our subscription plans.")
            return
        
        # Set cooldown
        cooldown.set_cooldown(user_id, "pay", COOLDOWNS["pay"])
        
        # Generate payment request
        try:
            # Show typing indicator
            async with ctx.typing():
                embed = await pusher.process_payment(user_id, username, service_type.lower())
                
                # Log command
                cmd_logger.log_command(user_id, username, "pay", service_type)
                
                # Send response
                await ctx.send(embed=embed)
                
                # Add a random quote from Crypto Craig
                crypto_quotes = [
                    "Blockchain doesn't lie, but people do. I only deal in the former.",
                    "Your SOL will be as secure as your trial credentials.",
                    "In crypto we trust. All other payment methods are sus.",
                    "Remember: no refunds, no chargebacks, no mercy. That's the crypto way.",
                    "Slinging SOL is my specialty. Keep it flowing and I'll keep your trials going."
                ]
                await ctx.send(f"💰 **{AGENT_NAMES['craig']}**: {random.choice(crypto_quotes)}")
                
        except Exception as e:
            await ctx.send(f"Error creating payment: {str(e)}")
            logger.error(f"Error processing payment command: {str(e)}")
    
    @bot.command(name="verify_payment")
    async def verify_payment_command(ctx, reference: str = None):
        """Verify payment status"""
        user_id = str(ctx.author.id)
        username = str(ctx.author)
        
        # Check if user is on cooldown
        if cooldown.is_on_cooldown(user_id, "verify_payment"):
            remaining = cooldown.get_remaining_time(user_id, "verify_payment")
            emoji = random_drug_emoji()
            await ctx.send(f"{emoji} Payment verification requests are limited. Try again in {remaining} seconds.")
            return
        
        # Set cooldown
        cooldown.set_cooldown(user_id, "verify_payment", COOLDOWNS["verify_payment"])
        
        # Show typing indicator
        async with ctx.typing():
            try:
                embed = await pusher.process_verify_payment(user_id, username, reference)
                
                # Log command
                cmd_logger.log_command(user_id, username, "verify_payment", reference or "")
                
                # Send response
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"Error verifying payment: {str(e)}")
                logger.error(f"Error processing verify_payment command: {str(e)}")
    
    @bot.command(name="payments")
    async def payments_command(ctx):
        """View payment history"""
        user_id = str(ctx.author.id)
        username = str(ctx.author)
        
        # Check if user is on cooldown
        if cooldown.is_on_cooldown(user_id, "payments"):
            remaining = cooldown.get_remaining_time(user_id, "payments")
            emoji = random_drug_emoji()
            await ctx.send(f"{emoji} Payment history requests are limited. Try again in {remaining} seconds.")
            return
        
        # Set cooldown
        cooldown.set_cooldown(user_id, "payments", COOLDOWNS["payments"])
        
        # Show typing indicator
        async with ctx.typing():
            try:
                embed = await pusher.process_payments(user_id, username)
                
                # Log command
                cmd_logger.log_command(user_id, username, "payments", "")
                
                # Send response
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"Error fetching payments: {str(e)}")
                logger.error(f"Error processing payments command: {str(e)}")
    
    @bot.command(name="tier")
    async def tier_command(ctx):
        """View user tier status"""
        user_id = str(ctx.author.id)
        username = str(ctx.author)
        
        # Check if user is on cooldown
        if cooldown.is_on_cooldown(user_id, "tier"):
            remaining = cooldown.get_remaining_time(user_id, "tier")
            emoji = random_drug_emoji()
            await ctx.send(f"{emoji} Tier status requests are limited. Try again in {remaining} seconds.")
            return
        
        # Set cooldown
        cooldown.set_cooldown(user_id, "tier", COOLDOWNS["tier"])
        
        # Show typing indicator
        async with ctx.typing():
            try:
                embed = await pusher.process_user_tier(user_id, username)
                
                # Log command
                cmd_logger.log_command(user_id, username, "tier", "")
                
                # Send response
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"Error fetching tier status: {str(e)}")
                logger.error(f"Error processing tier command: {str(e)}")
    
    @bot.command(name="referral")
    async def referral_command(ctx):
        """Get your referral code or see your referral stats"""
        user_id = str(ctx.author.id)
        username = str(ctx.author)
        
        # Check if user is on cooldown
        if cooldown.is_on_cooldown(user_id, "referral"):
            remaining = cooldown.get_remaining_time(user_id, "referral")
            emoji = random_drug_emoji()
            await ctx.send(f"{emoji} Referral requests are limited. Try again in {remaining} seconds.")
            return
        
        # Set cooldown
        cooldown.set_cooldown(user_id, "referral", COOLDOWNS["referral"])
        
        # Show typing indicator
        async with ctx.typing():
            try:
                # Get or create a referral code
                referral_code = db.get_referral_code(user_id)
                if not referral_code:
                    await ctx.send("❌ Could not create a referral code. Please try again later.")
                    return
                
                # Get referral statistics
                referrals = db.get_user_referrals(user_id)
                total_referrals = len(referrals) if referrals else 0
                
                # Get commission statistics
                total_commission = db.get_total_commission(user_id)
                commissions = db.get_user_commissions(user_id)
                pending_commission = sum(c['amount'] for c in commissions if c['status'] == 'pending') if commissions else 0
                paid_commission = sum(c['amount'] for c in commissions if c['status'] == 'paid') if commissions else 0
                
                # Create an embed to display the information
                embed = discord.Embed(
                    title="🔌 Your Referral Program",
                    description="Refer friends to Trial Junkie and earn 10% commission on their payments!",
                    color=discord.Color.purple()
                )
                
                embed.add_field(name="Your Referral Code", value=f"`{referral_code}`", inline=False)
                embed.add_field(name="Refer Friends", value=f"Tell friends to use `/refer {referral_code}` to join with your referral", inline=False)
                embed.add_field(name="Total Referrals", value=str(total_referrals), inline=True)
                embed.add_field(name="Earnings", value=f"{total_commission:.4f} SOL", inline=True)
                embed.add_field(name="Pending", value=f"{pending_commission:.4f} SOL", inline=True)
                embed.add_field(name="Paid", value=f"{paid_commission:.4f} SOL", inline=True)
                
                embed.set_footer(text="10% commission on all payments from your referrals")
                
                # Log command
                cmd_logger.log_command(user_id, username, "referral", "")
                
                # Send response
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"Error fetching referral info: {str(e)}")
                logger.error(f"Error processing referral command: {str(e)}")
    
    @bot.command(name="refer")
    async def refer_command(ctx, code: str = None):
        """Register with someone's referral code"""
        user_id = str(ctx.author.id)
        username = str(ctx.author)
        
        if not code:
            await ctx.send("❌ Please provide a referral code. Usage: `/refer [code]`")
            return
        
        # Show typing indicator
        async with ctx.typing():
            try:
                # Try to register the referral
                success, message = db.register_referral(user_id, code)
                
                if success:
                    # Get referrer's information
                    embed = discord.Embed(
                        title="✅ Referral Successful!",
                        description=message,
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Your Referral Benefits", value="Refer others with `/referral` to earn 10% commission on their payments!")
                else:
                    # Failed to register
                    embed = discord.Embed(
                        title="❌ Referral Failed",
                        description=message,
                        color=discord.Color.red()
                    )
                
                # Log command
                cmd_logger.log_command(user_id, username, "refer", code)
                
                # Send response
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"Error processing referral: {str(e)}")
                logger.error(f"Error processing refer command: {str(e)}")
                
    @bot.command(name="commissions")
    async def commissions_command(ctx):
        """View your commission earnings from referrals"""
        user_id = str(ctx.author.id)
        username = str(ctx.author)
        
        # Check if user is on cooldown
        if cooldown.is_on_cooldown(user_id, "commissions"):
            remaining = cooldown.get_remaining_time(user_id, "commissions")
            emoji = random_drug_emoji()
            await ctx.send(f"{emoji} Commission requests are limited. Try again in {remaining} seconds.")
            return
        
        # Set cooldown
        cooldown.set_cooldown(user_id, "commissions", COOLDOWNS["commissions"])
        
        # Show typing indicator
        async with ctx.typing():
            try:
                # Get commission details
                commissions = db.get_user_commissions(user_id)
                
                if not commissions:
                    await ctx.send("💸 You haven't earned any commissions yet. Use `!referral` to get your referral code and start earning!")
                    return
                
                # Calculate totals
                total_commission = db.get_total_commission(user_id)
                pending = sum(c['amount'] for c in commissions if c['status'] == 'pending')
                paid = sum(c['amount'] for c in commissions if c['status'] == 'paid')
                
                # Create an embed for the commissions
                embed = discord.Embed(
                    title="💰 Your Commission Earnings",
                    description=f"Total earnings: {total_commission:.4f} SOL",
                    color=discord.Color.gold()
                )
                
                embed.add_field(name="Pending", value=f"{pending:.4f} SOL", inline=True)
                embed.add_field(name="Paid", value=f"{paid:.4f} SOL", inline=True)
                embed.add_field(name="Referrals", value=str(len(set(c['referred_id'] for c in commissions))), inline=True)
                
                # Add the most recent commissions
                embed.add_field(name="Recent Commissions", value="-------------------", inline=False)
                
                for i, commission in enumerate(commissions[:5]):  # Show the 5 most recent
                    embed.add_field(
                        name=f"#{i+1} - {commission['created_at'][:10]}",
                        value=f"From: {commission['referred_username']}\nAmount: {commission['amount']:.4f} SOL\nStatus: {commission['status'].title()}",
                        inline=True
                    )
                
                embed.set_footer(text="Use /referral to get your referral code and earn more!")
                
                # Log command
                cmd_logger.log_command(user_id, username, "commissions", "")
                
                # Send response
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"Error fetching commissions: {str(e)}")
                logger.error(f"Error processing commissions command: {str(e)}")
    
    # Set up trial commands
    from commands.trial_commands import setup as setup_trial_commands
    setup_trial_commands(bot, db)
    
    return bot
