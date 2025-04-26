"""
Pusher Agent - Main controller for all other agents
Orchestrates the flow between commands and specialized agents
"""
import logging
import discord
from datetime import datetime, timedelta
import os

from config import AGENT_NAMES, COLORS
from agents.identity_agent import IdentityAgent
from agents.card_agent import CardAgent
from agents.email_agent import EmailAgent
from agents.phone_agent import PhoneAgent
from agents.automation_agent import AutomationAgent
from agents.payment_agent import PaymentAgent

logger = logging.getLogger(__name__)

class Pusher:
    """Main controller for all specialized agents"""
    
    def __init__(self, db):
        """Initialize the pusher with all agents"""
        self.db = db
        
        # Check if RapidAPI key is available
        rapidapi_key = os.getenv("RAPIDAPI_KEY")
        if not rapidapi_key:
            logger.warning("RAPIDAPI_KEY not found in environment variables. API requests will likely fail.")
        
        # Initialize all specialized agents
        self.identity_agent = IdentityAgent(db)
        self.card_agent = CardAgent(db)
        self.email_agent = EmailAgent(db)
        self.phone_agent = PhoneAgent(db)
        self.automation_agent = AutomationAgent(db)
        self.payment_agent = PaymentAgent(db)
        
        # Check if Solana wallet is available
        solana_wallet = os.getenv("SOLANA_WALLET_ADDRESS")
        if not solana_wallet or solana_wallet == "YourSolanaWalletAddressHere":
            logger.warning("SOLANA_WALLET_ADDRESS not properly configured. Payment features will use a placeholder address.")
        
        logger.info("Pusher agent initialized with all specialized agents")
    
    async def process_hit(self, user_id, username, service):
        """Process a full trial setup with all agents"""
        logger.info(f"Processing hit command for {username} ({user_id}) - Service: {service}")
        
        # Ensure user exists in database
        self.db.create_user(user_id, username)
        
        # Check if this is a known service in our configuration
        from config import TRIAL_SERVICES
        service_name = service.lower()
        
        # Get service configuration or use default
        service_config = TRIAL_SERVICES.get(service_name, None)
        
        if not service_config:
            # Unknown service - suggest registering it first
            raise ValueError(f"Unknown service: {service}. Use `!trip url https://{service}.com` to register this service first.")
        
        # Determine required fields for this service
        required_fields = service_config.get("required_fields", ["identity", "email", "card", "phone"])
        
        # Dictionary to store all generated credentials
        credentials = {}
        
        # Generate identity if needed
        if "identity" in required_fields:
            identity = await self.identity_agent.generate_identity()
            self.db.save_credential(user_id, service_name, "identity", identity)
            credentials["identity"] = identity
        else:
            identity = None
            credentials["identity"] = None
        
        # Generate email address
        if "email" in required_fields:
            email = await self.email_agent.generate_email(identity)
            self.db.save_credential(user_id, service_name, "email", email)
            credentials["email"] = email
        else:
            email = None
            credentials["email"] = None
        
        # Generate card if needed
        if "card" in required_fields:
            card = await self.card_agent.generate_card()
            self.db.save_credential(user_id, service_name, "card", card)
            credentials["card"] = card
        else:
            card = None
            credentials["card"] = None
        
        # Generate phone number if needed
        if "phone" in required_fields:
            phone = await self.phone_agent.generate_phone()
            self.db.save_credential(user_id, service_name, "phone", phone)
            credentials["phone"] = phone
        else:
            phone = None
            credentials["phone"] = None
        
        # Log the command
        self.db.log_command(user_id, "hit", service_name)
        
        # Get additional service information for response
        service_url = service_config.get("url", f"https://{service_name}.com")
        trial_days = service_config.get("trial_period_days", 30)
        expiry_date = (datetime.now() + timedelta(days=trial_days)).strftime("%Y-%m-%d")
        plan_name = service_config.get("plan_name", f"{service_name.capitalize()} Premium")
        price = service_config.get("price", "Unknown")
        
        # Create response embed with thematic branding
        if service_config.get("is_custom", False):
            title = f"🎯 Custom Trial Ready: {service_name.capitalize()}"
            description = f"Credentials generated for your custom trial at {service_url}"
        else:
            title = f"🎯 Trial Ready for {service_name.capitalize()}"
            description = f"All credentials generated by **The Pusher** for your {service_name} trial."
            
        # Add trial details
        description += f"\n\n📺 **Plan:** {plan_name}\n"
        description += f"📅 **Trial Expires:** {expiry_date} ({trial_days} days)\n"
        if price != "Unknown":
            description += f"💰 **Price After Trial:** {price}\n"
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=COLORS["success"],
            timestamp=datetime.now()
        )
        
        # Only add fields for credentials that were generated
        if identity:
            embed.add_field(name="👤 Identity", value=f"Name: **{identity['name']}**\nAge: **{identity['age']}**\nLocation: **{identity['location']}**", inline=False)
        
        if email:
            embed.add_field(name="📧 Email", value=f"**{email}**", inline=True)
        
        if phone:
            embed.add_field(name="📱 Phone", value=f"**{phone}**", inline=True)
        
        if card:
            embed.add_field(name="💳 Card", value=f"**{card['number']}**\nExp: **{card['expiry']}**\nCVV: **{card['cvv']}**", inline=False)
        
        # Add usage hints
        embed.add_field(name="Next Steps", value=f"Use `!trip {service_name}` to automate the signup process\nUse `!stash` to view your saved credentials", inline=False)
        
        embed.set_footer(text=f"Requested by {username} | Trial Junkie", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        
        return embed
    
    async def process_dose(self, user_id, username, agent_type, platform):
        """Process a partial credential generation with a single agent"""
        logger.info(f"Processing dose command for {username} ({user_id}) - Agent: {agent_type}, Platform: {platform}")
        
        # Ensure user exists in database
        self.db.create_user(user_id, username)
        
        # Map agent type to the corresponding agent
        agent_type = agent_type.lower()
        
        # Determine agent and operation
        if agent_type == "harry":
            # Identity generation
            result = await self.identity_agent.generate_identity()
            cred_type = "identity"
            display_value = f"Name: **{result['name']}**\nAge: **{result['age']}**\nLocation: **{result['location']}**"
            agent_name = AGENT_NAMES["harry"]
            
        elif agent_type == "mandy":
            # Card generation
            result = await self.card_agent.generate_card()
            cred_type = "card"
            display_value = f"Number: **{result['number']}**\nExp: **{result['expiry']}**\nCVV: **{result['cvv']}**"
            agent_name = AGENT_NAMES["mandy"]
            
        elif agent_type == "xan":
            # Email generation
            identity = await self.identity_agent.generate_identity()
            result = await self.email_agent.generate_email(identity)
            cred_type = "email"
            display_value = f"**{result}**"
            agent_name = AGENT_NAMES["xan"]
            
        elif agent_type == "phone":
            # Phone generation
            result = await self.phone_agent.generate_phone()
            cred_type = "phone"
            display_value = f"**{result}**"
            agent_name = AGENT_NAMES["phone"]
            
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        # Save the credential
        self.db.save_credential(user_id, platform, cred_type, result)
        
        # Log the command
        self.db.log_command(user_id, "dose", f"{agent_type} {platform}")
        
        # Create response embed
        embed = discord.Embed(
            title=f"💊 Dose Ready for {platform}",
            description=f"Credential generated by **{agent_name}** for your {platform} account.",
            color=COLORS["info"],
            timestamp=datetime.now()
        )
        
        embed.add_field(name=f"{cred_type.title()}", value=display_value, inline=False)
        embed.add_field(name="Usage", value="Use `!stash` to view your saved credentials", inline=False)
        
        embed.set_footer(text=f"Requested by {username} | Trial Junkie", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        
        return embed
    
    async def process_trip(self, user_id, username, script):
        """Process an automation script run"""
        logger.info(f"Processing trip command for {username} ({user_id}) - Script: {script}")
        
        # Ensure user exists in database
        self.db.create_user(user_id, username)
        
        # Get user's latest credentials
        credentials = self.db.get_user_credentials(user_id)
        
        if not credentials:
            raise ValueError("No credentials found. Generate some first with !hit or !dose")
        
        # Check if the script is a service name from TRIAL_SERVICES
        from config import TRIAL_SERVICES
        is_service = script.lower() in TRIAL_SERVICES
        script_name = script.lower()
        service_name = script_name if is_service else "custom"
        
        # Run the automation script
        result = await self.automation_agent.run_script(script_name, credentials)
        
        # Log the command
        self.db.log_command(user_id, "trip", script_name)
        
        # Create response embed with appropriate title
        if is_service:
            service_config = TRIAL_SERVICES.get(script_name)
            service_url = service_config.get("url", "")
            # If a known service
            title = f"🍄 Trip Report: {script_name.capitalize()}"
            description = f"Automation run by **{AGENT_NAMES['sal']}** for `{script_name}` trial."
            if service_url:
                description += f"\nService URL: {service_url}"
        else:
            # If a basic script or unknown service
            title = f"🍄 Trip Report: {script_name}"
            description = f"Automation run by **{AGENT_NAMES['sal']}** for script `{script_name}`."
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=COLORS["warning"],
            timestamp=datetime.now()
        )
        
        embed.add_field(name="Status", value=result["status"], inline=False)
        embed.add_field(name="Details", value=result["details"], inline=False)
        
        if "steps" in result:
            embed.add_field(name="Steps Completed", value="\n".join(f"✅ {step}" for step in result["steps"]), inline=False)
        
        embed.set_footer(text=f"Requested by {username} | Trial Junkie", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        
        return embed
    
    async def process_stash(self, user_id, username):
        """Process a stash view request"""
        logger.info(f"Processing stash command for {username} ({user_id})")
        
        # Ensure user exists in database
        self.db.create_user(user_id, username)
        
        # Get user stats
        stats = self.db.get_user_stats(user_id)
        
        # Get user's credentials
        credentials = self.db.get_user_credentials(user_id)
        
        # Log the command
        self.db.log_command(user_id, "stash", "")
        
        # Create response embed
        embed = discord.Embed(
            title=f"🧪 Your Trial Junkie Stash",
            description=f"All your saved credentials and trial data.",
            color=COLORS["info"],
            timestamp=datetime.now()
        )
        
        # Add stats
        total_creds = stats.get('total_credentials', 0)
        embed.add_field(name="📊 Stats", value=f"Total Items: **{total_creds}**\nServices: **{len(set(c['service'] for c in credentials))}**", inline=False)
        
        # Group credentials by service
        services = {}
        for cred in credentials:
            if cred['service'] not in services:
                services[cred['service']] = []
            services[cred['service']].append(cred)
        
        # Add latest credentials for each service (up to 3 services)
        for i, (service, creds) in enumerate(list(services.items())[:3]):
            # Group by credential type
            service_data = {}
            for cred in creds:
                if cred['type'] not in service_data:
                    service_data[cred['type']] = cred['value']
            
            # Format the credential data
            cred_text = []
            if 'identity' in service_data:
                identity = service_data['identity']
                cred_text.append(f"👤 **{identity['name']}** ({identity['age']})")
            
            if 'email' in service_data:
                cred_text.append(f"📧 **{service_data['email']}**")
            
            if 'phone' in service_data:
                cred_text.append(f"📱 **{service_data['phone']}**")
            
            if 'card' in service_data:
                card = service_data['card']
                cred_text.append(f"💳 **{card['number']}** (Exp: {card['expiry']})")
            
            # Add field for this service
            embed.add_field(
                name=f"🔑 {service}",
                value="\n".join(cred_text) or "No details available",
                inline=False
            )
        
        # If there are more services, indicate that
        if len(services) > 3:
            remaining = len(services) - 3
            embed.add_field(
                name="➕ More Services",
                value=f"**{remaining}** more services not shown. Use `!hit <service>` to generate more.",
                inline=False
            )
        
        embed.set_footer(text=f"Requested by {username} | Trial Junkie", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        
        return embed
    
    async def process_rehab(self, user_id, username):
        """Process a rehab (data clearing) request"""
        logger.info(f"Processing rehab command for {username} ({user_id})")
        
        # Ensure user exists in database
        self.db.create_user(user_id, username)
        
        # Clear user data
        self.db.clear_user_data(user_id)
        
        # Log the command
        self.db.log_command(user_id, "rehab", "")
        
        # Create response embed
        embed = discord.Embed(
            title=f"🏥 Rehab Complete",
            description=f"Your credentials have been cleared. You're clean now.",
            color=COLORS["success"],
            timestamp=datetime.now()
        )
        
        embed.add_field(name="Status", value="✅ **All credentials deleted**", inline=False)
        embed.add_field(name="What's Next", value="Use `!hit <service>` to start generating new trials", inline=False)
        
        embed.set_footer(text=f"Requested by {username} | Trial Junkie", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        
        return embed
        
    async def process_payment(self, user_id, username, service_type):
        """Process a payment request"""
        logger.info(f"Processing payment request for {username} ({user_id}) - Service: {service_type}")
        
        # Ensure user exists in database
        self.db.create_user(user_id, username)
        
        # Create a payment request
        payment_info = await self.payment_agent.create_payment(user_id, username, service_type)
        
        # Log the command
        self.db.log_command(user_id, "pay", service_type)
        
        # Create response embed with thematic titles for new plans
        if service_type == "one_time_hit":
            title = "💨 One-Time Hit (Free Plan)"
            description = "A quick blast of freedom, no strings attached."
        elif service_type == "five_dollar_rush":
            title = "💵 Five Dollar Rush ($5 Plan)"
            description = "A rush of power for just five bucks."
        elif service_type == "junkified":
            title = "💎 13 Junkified ($13 Plan)"
            description = "Unlock unlimited possibilities—no limits, just freedom."
        else:
            title = f"💰 Payment Required for {service_type}"
            description = f"Payment request generated by **{AGENT_NAMES['craig']}** for {service_type}."
            
        embed = discord.Embed(
            title=title,
            description=description,
            color=COLORS["payment"],
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="Amount", 
            value=f"**{payment_info['amount']} SOL**", 
            inline=True
        )
        
        embed.add_field(
            name="Wallet Address", 
            value=f"```{payment_info['wallet']}```", 
            inline=False
        )
        
        embed.add_field(
            name="Reference", 
            value=f"```{payment_info['reference']}```", 
            inline=False
        )
        
        embed.add_field(
            name="Instructions", 
            value=(
                "1. Send the exact amount to the wallet address above\n"
                "2. Include the reference in the transaction memo\n"
                "3. Use `!verify_payment` to check the status"
            ), 
            inline=False
        )
        
        embed.add_field(
            name="Expires", 
            value=f"<t:{int(datetime.fromisoformat(payment_info['expires']).timestamp())}:R>", 
            inline=True
        )
        
        embed.set_footer(text=f"Requested by {username} | Trial Junkie", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        
        return embed
    
    async def process_verify_payment(self, user_id, username, tx_id=None):
        """Verify a payment"""
        logger.info(f"Verifying payment for {username} ({user_id})")
        
        # Ensure user exists in database
        self.db.create_user(user_id, username)
        
        # For this simplified version, we'll consider providing a tx_id as manual confirmation
        is_manual_confirmation = tx_id is not None and tx_id.lower() != "check"
        
        if is_manual_confirmation:
            # User is confirming they sent payment
            is_paid = await self.payment_agent.process_manual_payment(user_id)
        else:
            # Check payment status automatically (simulated for demo)
            is_paid = await self.payment_agent.check_payment(user_id)
        
        # Log the command
        self.db.log_command(user_id, "verify_payment", tx_id or "")
        
        # Get payment status
        status = await self.payment_agent.get_payment_status(user_id)
        
        # Create response embed based on payment status
        if status['status'] == 'completed' or is_paid:
            # Payment was successful
            
            # Update user tier based on the service type
            reference = status.get('reference', '')
            payment = self.db.get_payment_by_reference(reference)
            
            # Set appropriate tier and expiry based on plan type
            if payment:
                service_type = payment['service_type']
                
                if service_type == 'premium':
                    # Set premium membership for 30 days
                    expiry_date = (datetime.now() + timedelta(days=30)).isoformat()
                    self.db.update_user_tier(user_id, 'premium', expiry_date)
                    tier_message = "Your Premium membership is now active for 30 days!"
                    plan_name = "Premium"
                    
                elif service_type == 'one_time_hit':
                    # Free plan - single use
                    self.db.update_user_tier(user_id, 'one_time_hit')
                    tier_message = "Your One-Time Hit is now active. You get one free trial!"
                    plan_name = "One-Time Hit"
                    
                elif service_type == 'five_dollar_rush':
                    # $5 plan - active for 7 days
                    expiry_date = (datetime.now() + timedelta(days=7)).isoformat()
                    self.db.update_user_tier(user_id, 'five_dollar_rush', expiry_date)
                    tier_message = "Your Five Dollar Rush is now active for 7 days!"
                    plan_name = "Five Dollar Rush"
                    
                elif service_type == 'junkified':
                    # $13 plan - active for 30 days with premium features
                    expiry_date = (datetime.now() + timedelta(days=30)).isoformat()
                    self.db.update_user_tier(user_id, 'junkified', expiry_date)
                    tier_message = "Your 13 Junkified unlimited plan is now active for 30 days!"
                    plan_name = "13 Junkified"
                    
                else:
                    # Default to basic paid tier for other service types
                    expiry_date = (datetime.now() + timedelta(days=1)).isoformat()
                    self.db.update_user_tier(user_id, 'paid', expiry_date)
                    tier_message = f"Your payment for {service_type} has been processed!"
                    plan_name = service_type.title()
            else:
                tier_message = "Your payment has been processed!"
                plan_name = "Service"
            
            # Create themed embed titles based on plan
            if payment and payment['service_type'] == "one_time_hit":
                title = "💨 One-Time Hit Activated!"
                description = "Your free trial blast is ready to use."
            elif payment and payment['service_type'] == "five_dollar_rush":
                title = "💵 Five Dollar Rush Unlocked!"
                description = "Your power rush has been activated."
            elif payment and payment['service_type'] == "junkified":
                title = "💎 You're Now Fully Junkified!"
                description = "Unlimited access to everything is now yours."
            else:
                title = "✅ Payment Verified"
                description = "Your payment has been successfully verified!"
            
            embed = discord.Embed(
                title=title,
                description=description,
                color=COLORS["success"],
                timestamp=datetime.now()
            )
            
            embed.add_field(
                name="Status", 
                value="**Payment Complete**", 
                inline=False
            )
            
            embed.add_field(
                name=f"{plan_name} Status", 
                value=tier_message, 
                inline=False
            )
            
            embed.add_field(
                name="Next Steps", 
                value=f"You can now use the features of Trial Junkie for your `{plan_name}` subscription!", 
                inline=False
            )
            
        elif status['status'] == 'expired':
            # Payment request expired
            embed = discord.Embed(
                title="⏱️ Payment Expired",
                description="Your payment request has expired.",
                color=COLORS["error"],
                timestamp=datetime.now()
            )
            
            embed.add_field(
                name="What Now?", 
                value="You can create a new payment request using the `!pay` command.", 
                inline=False
            )
            
        else:
            # Payment still pending
            embed = discord.Embed(
                title="⏳ Payment Pending",
                description="Your payment has not been verified yet.",
                color=COLORS["warning"],
                timestamp=datetime.now()
            )
            
            embed.add_field(
                name="Status", 
                value=f"**{status['message']}**", 
                inline=False
            )
            
            if 'time_left' in status:
                # Convert seconds to hours and minutes for better readability
                hours = status['time_left'] // 3600
                minutes = (status['time_left'] % 3600) // 60
                time_display = f"**{hours}h {minutes}m**" if hours > 0 else f"**{minutes}m**"
                
                embed.add_field(
                    name="Time Remaining", 
                    value=time_display, 
                    inline=True
                )
            
            if 'reference' in status:
                embed.add_field(
                    name="Reference Code", 
                    value=f"```{status['reference']}```", 
                    inline=False
                )
            
            embed.add_field(
                name="Instructions", 
                value=(
                    "1. Send the exact SOL amount to the wallet address provided\n"
                    "2. Once sent, use `!verify_payment sent` to confirm your payment\n"
                    "3. Your payment will be manually verified\n"
                    "4. Use `!verify_payment` at any time to check status"
                ), 
                inline=False
            )
        
        embed.set_footer(text=f"Requested by {username} | Trial Junkie", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        
        return embed
    
    async def process_payments(self, user_id, username):
        """View payment history"""
        logger.info(f"Viewing payment history for {username} ({user_id})")
        
        # Ensure user exists in database
        self.db.create_user(user_id, username)
        
        # Get all user payments
        payments = self.db.get_user_payments(user_id)
        
        # Log the command
        self.db.log_command(user_id, "payments", "")
        
        # Create response embed
        embed = discord.Embed(
            title="💰 Payment History",
            description=f"View all your payments to Trial Junkie.",
            color=COLORS["info"],
            timestamp=datetime.now()
        )
        
        if not payments:
            embed.add_field(
                name="No Payments Found", 
                value="You haven't made any payments yet. Use `!pay <service>` to get started.", 
                inline=False
            )
        else:
            # Count payments by status
            status_counts = {}
            for payment in payments:
                status = payment['status']
                if status not in status_counts:
                    status_counts[status] = 0
                status_counts[status] += 1
            
            # Add summary field
            embed.add_field(
                name="Summary", 
                value="\n".join([f"**{status.title()}: {count}**" for status, count in status_counts.items()]), 
                inline=False
            )
            
            # Show last 3 payments
            for i, payment in enumerate(payments[:3]):
                created_at = datetime.fromisoformat(payment['created_at'])
                status_emoji = "✅" if payment['status'] == 'completed' else "⏳" if payment['status'] == 'pending' else "❌"
                
                embed.add_field(
                    name=f"{status_emoji} {payment['service_type'].title()} Payment", 
                    value=(
                        f"**Amount:** {payment['amount']} SOL\n"
                        f"**Status:** {payment['status'].title()}\n"
                        f"**Date:** <t:{int(created_at.timestamp())}:R>\n"
                        f"**Reference:** {payment['reference'][:10]}..."
                    ), 
                    inline=False
                )
                
            # If more than 3 payments, indicate that
            if len(payments) > 3:
                embed.add_field(
                    name="More Payments", 
                    value=f"**{len(payments) - 3}** more payments not shown.", 
                    inline=False
                )
                
        embed.set_footer(text=f"Requested by {username} | Trial Junkie", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        
        return embed
        
    async def process_user_tier(self, user_id, username):
        """View user tier status"""
        logger.info(f"Viewing tier status for {username} ({user_id})")
        
        # Ensure user exists in database
        self.db.create_user(user_id, username)
        
        # Get user tier information
        tier_info = self.db.get_user_tier(user_id)
        
        # Log the command
        self.db.log_command(user_id, "tier", "")
        
        # Get information about the tier
        tier = tier_info['tier']
        tier_data = None
        
        # Get tier information from config
        from config import SERVICE_TIERS
        if tier in SERVICE_TIERS:
            tier_data = SERVICE_TIERS[tier]
        
        # Create response embed with themed titles based on tier
        if tier == 'one_time_hit':
            title = "💨 Your One-Time Hit Status"
            description = "A quick blast of freedom, no strings attached."
            embed_color = COLORS['info']
        elif tier == 'five_dollar_rush':
            title = "💵 Your Five Dollar Rush Status"
            description = "A rush of power for just five bucks."
            embed_color = COLORS['warning']
        elif tier == 'junkified':
            title = "💎 Your Junkified Status"
            description = "Unlimited possibilities—no limits, just freedom."
            embed_color = COLORS['success']
        elif tier == 'premium':
            title = "🏆 Your Premium Membership"
            description = "Premium tier with high daily limits and priority support."
            embed_color = COLORS['success']
        elif tier == 'paid':
            title = "💰 Your Paid Membership"
            description = "Pay-per-use tier with higher limits."
            embed_color = COLORS['warning']
        else:
            title = "🏆 Your Trial Junkie Membership"
            description = "Current membership tier and benefits."
            embed_color = COLORS['info']
            
        embed = discord.Embed(
            title=title,
            description=description,
            color=embed_color,
            timestamp=datetime.now()
        )
        
        # Add tier field
        tier_name = tier.title()
        embed.add_field(
            name="Current Tier", 
            value=f"**{tier_name}**", 
            inline=True
        )
        
        # Add daily limit field
        if tier_data:
            embed.add_field(
                name="Daily Limit", 
                value=f"**{tier_data['daily_limit']}** commands", 
                inline=True
            )
        
        # Add description field
        if tier_data:
            embed.add_field(
                name="Description", 
                value=tier_data['description'], 
                inline=False
            )
        
        # Add expiry field for timed subscriptions
        if tier_info['membership_expires'] and tier in ['premium', 'five_dollar_rush', 'junkified']:
            expiry = datetime.fromisoformat(tier_info['membership_expires'])
            if tier == 'junkified':
                expires_name = "Junkified Expires"
            elif tier == 'five_dollar_rush':
                expires_name = "Rush Expires"
            else:
                expires_name = "Premium Expires"
                
            embed.add_field(
                name=expires_name, 
                value=f"<t:{int(expiry.timestamp())}:R>", 
                inline=False
            )
        
        # Add upgrade suggestion field for non-premium tiers
        if tier == 'free' or tier == 'one_time_hit':
            embed.add_field(
                name="Want More?", 
                value="Use `!plans` to see our subscription options!", 
                inline=False
            )
        elif tier == 'five_dollar_rush':
            embed.add_field(
                name="Want Maximum Power?", 
                value="Use `!pay junkified` to upgrade to our unlimited plan!", 
                inline=False
            )
        
        embed.set_footer(text=f"Requested by {username} | Trial Junkie", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        
        return embed
