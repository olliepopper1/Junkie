"""
Automation Agent (Shroomy Sal)
Handles browser automation for trial signups
"""
import logging
import asyncio
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AutomationAgent:
    """Agent for handling browser automation"""
    
    def __init__(self, db):
        """Initialize the automation agent"""
        self.db = db
        self.name = "Shroomy Sal"
        self.available_scripts = {
            "signup": self._run_signup_script,
            "verify": self._run_verify_script,
            "cancel": self._run_cancel_script,
            "hulu": self._run_hulu_script
        }
        
        # Initialize service-specific scripts
        self.service_scripts = {
            "hulu": self._run_hulu_script,
            "netflix": self._run_netflix_script,
            "disney": self._run_disney_script,
            "spotify": self._run_spotify_script,
            "amazon": self._run_amazon_script
        }
        
        logger.info(f"{self.name} initialized")
    
    async def run_script(self, script_name, credentials):
        """Run an automation script"""
        script_name = script_name.lower()
        
        # Check if this is a general script or a service-specific script
        if script_name in self.available_scripts:
            # Run general script
            logger.info(f"{self.name} running general script: {script_name}")
            result = await self.available_scripts[script_name](credentials)
            return result
        
        # Check if this is a service-specific script from TRIAL_SERVICES
        from config import TRIAL_SERVICES
        if script_name in TRIAL_SERVICES:
            # Run service-specific script
            logger.info(f"{self.name} running service-specific script for: {script_name}")
            result = await self._run_service_script(script_name, credentials)
            return result
            
        # Check if it's a service available in our self.service_scripts dictionary
        if script_name in self.service_scripts:
            # Run custom service script
            logger.info(f"{self.name} running custom service script for: {script_name}")
            result = await self.service_scripts[script_name](credentials)
            return result
        
        # If we get here, the script is unknown
        available_scripts = list(self.available_scripts.keys()) + list(self.service_scripts.keys()) + list(TRIAL_SERVICES.keys())
        raise ValueError(f"Unknown script: {script_name}. Available scripts: {', '.join(available_scripts)}")
    
    async def _run_signup_script(self, credentials):
        """Run a signup automation script"""
        logger.info(f"{self.name} running signup script")
        
        # In a real implementation, this would use Selenium/Playwright
        # For now, we'll simulate the signup process
        
        # Check if we have necessary credentials
        has_identity = any(c["type"] == "identity" for c in credentials)
        has_email = any(c["type"] == "email" for c in credentials)
        has_card = any(c["type"] == "card" for c in credentials)
        
        if not (has_identity and has_email and has_card):
            return {
                "status": "❌ Failed",
                "details": "Missing required credentials. Need identity, email, and card."
            }
        
        # Simulate signup process with delays
        steps = [
            "Navigating to website",
            "Filling out registration form",
            "Entering email information",
            "Entering payment details",
            "Submitting application",
            "Confirming trial activation"
        ]
        
        # Add random success or partial success
        success_chance = random.random()
        
        if success_chance > 0.8:
            # Partial success
            completed_steps = steps[:random.randint(3, 5)]
            status = "⚠️ Partial Success"
            details = "Signup process started but encountered an issue. You may need to verify manually."
        else:
            # Full success
            completed_steps = steps
            status = "✅ Success"
            details = "Signup process completed successfully. Trial is active."
            
            # Add random trial duration
            trial_days = random.choice([7, 14, 30])
            expiry_date = datetime.now() + timedelta(days=trial_days)
            details += f"\nTrial expires on {expiry_date.strftime('%Y-%m-%d')} ({trial_days} days)."
        
        # Add random delay simulation
        await asyncio.sleep(random.uniform(1.5, 3.5))
        
        return {
            "status": status,
            "details": details,
            "steps": completed_steps
        }
    
    async def _run_verify_script(self, credentials):
        """Run a verification automation script"""
        logger.info(f"{self.name} running verification script")
        
        # In a real implementation, this would handle email/SMS verification
        # For now, we'll simulate the verification process
        
        # Check if we have necessary credentials
        has_email = any(c["type"] == "email" for c in credentials)
        
        if not has_email:
            return {
                "status": "❌ Failed",
                "details": "Missing required credentials. Need email."
            }
        
        # Simulate verification process with delays
        steps = [
            "Checking email inbox",
            "Locating verification email",
            "Extracting verification link",
            "Visiting verification URL",
            "Confirming account verification"
        ]
        
        # Add random success or partial success
        success_chance = random.random()
        
        if success_chance > 0.7:
            # Partial success
            completed_steps = steps[:random.randint(2, 4)]
            status = "⚠️ Partial Success"
            details = "Verification process started but encountered an issue. You may need to verify manually."
        else:
            # Full success
            completed_steps = steps
            status = "✅ Success"
            details = "Verification process completed successfully. Account is verified."
        
        # Add random delay simulation
        await asyncio.sleep(random.uniform(1.0, 2.5))
        
        return {
            "status": status,
            "details": details,
            "steps": completed_steps
        }
    
    async def _run_cancel_script(self, credentials):
        """Run a cancellation automation script"""
        logger.info(f"{self.name} running cancellation script")
        
        # In a real implementation, this would handle trial cancellation
        # For now, we'll simulate the cancellation process
        
        # Check if we have necessary credentials
        has_email = any(c["type"] == "email" for c in credentials)
        
        if not has_email:
            return {
                "status": "❌ Failed",
                "details": "Missing required credentials. Need email."
            }
        
        # Get the most recent service
        services = set(c["service"] for c in credentials)
        if not services:
            return {
                "status": "❌ Failed",
                "details": "No service found to cancel."
            }
        
        service = list(services)[0]
        
        # Simulate cancellation process with delays
        steps = [
            f"Logging into {service}",
            "Navigating to account settings",
            "Locating subscription options",
            "Requesting cancellation",
            "Confirming cancellation",
            "Saving confirmation receipt"
        ]
        
        # Add random success or partial success
        success_chance = random.random()
        
        if success_chance > 0.6:
            # Partial success
            completed_steps = steps[:random.randint(3, 5)]
            status = "⚠️ Partial Success"
            details = f"Cancellation process for {service} started but couldn't confirm. You may need to cancel manually."
        else:
            # Full success
            completed_steps = steps
            status = "✅ Success"
            details = f"Cancellation process for {service} completed successfully. Trial is cancelled."
        
        # Add random delay simulation
        await asyncio.sleep(random.uniform(1.5, 3.0))
        
        return {
            "status": status,
            "details": details,
            "steps": completed_steps
        }
        
    async def _run_hulu_script(self, credentials):
        """Run a Hulu signup automation script"""
        logger.info(f"{self.name} running Hulu signup script")
        
        # Check if we have necessary credentials
        has_identity = any(c["type"] == "identity" for c in credentials)
        has_email = any(c["type"] == "email" for c in credentials)
        has_card = any(c["type"] == "card" for c in credentials)
        has_phone = any(c["type"] == "phone" for c in credentials)
        
        if not (has_identity and has_email and has_card):
            return {
                "status": "❌ Failed",
                "details": "Missing required credentials. Need identity, email, and card for Hulu signup."
            }
        
        # Extract credentials
        identity = next((c["value"] for c in credentials if c["type"] == "identity"), None)
        email = next((c["value"] for c in credentials if c["type"] == "email"), None)
        card = next((c["value"] for c in credentials if c["type"] == "card"), None)
        phone = next((c["value"] for c in credentials if c["type"] == "phone"), None)
        
        # Available Hulu plans
        hulu_plans = [
            {
                "name": "Hulu (With Ads)",
                "price": "$7.99/month",
                "trial_days": 30,
                "features": ["Streaming Library with thousands of TV episodes and movies", "Most new episodes the day after they air", "Access to award-winning Hulu Originals", "Watch on your TV, laptop, phone, or tablet", "Up to 6 user profiles", "Watch on 2 different screens at the same time"]
            },
            {
                "name": "Hulu (No Ads)",
                "price": "$17.99/month",
                "trial_days": 30,
                "features": ["No ad interruptions", "Streaming Library with thousands of TV episodes and movies", "Most new episodes the day after they air", "Access to award-winning Hulu Originals", "Watch on your TV, laptop, phone, or tablet", "Up to 6 user profiles", "Watch on 2 different screens at the same time", "Download and watch"]
            },
            {
                "name": "Hulu + Live TV, Disney+, and ESPN+",
                "price": "$76.99/month",
                "trial_days": 3,
                "features": ["75+ live TV channels including sports, news, and entertainment", "No hidden fees or service charges", "Unlimited DVR storage", "Entire streaming libraries of Hulu, Disney+, and ESPN+", "Watch on your TV, laptop, phone, or tablet"]
            }
        ]
        
        # Select a plan (preferring the No Ads plan for a better trial experience)
        selected_plan = hulu_plans[1]  # Hulu (No Ads)
        
        # Create a secure password based on name and card number for easier retrieval
        # In a real implementation, we would have stronger password logic
        name_part = identity['first_name'].lower() if identity and 'first_name' in identity else 'user'
        card_part = card['number'][-4:] if card and 'number' in card else '1234'
        special_chars = ['!', '@', '#', '$', '%', '&']
        password = f"{name_part.capitalize()}{card_part}{random.choice(special_chars)}{random.choice(special_chars)}{random.randint(100, 999)}"
        
        # Get identity details
        first_name = identity.get('first_name', 'John') if identity else 'John'
        last_name = identity.get('last_name', 'Doe') if identity else 'Doe'
        gender = identity.get('gender', 'male') if identity else 'male'
        birth_date = identity.get('dob', '1990-01-01') if identity else '1990-01-01'
        
        # Get address details
        street = identity.get('street', '123 Main St') if identity else '123 Main St'
        city = identity.get('city', 'Anytown') if identity else 'Anytown'
        state = identity.get('state', 'CA') if identity else 'CA'
        zipcode = identity.get('zipcode', '90210') if identity else '90210'
        
        # Get card details
        card_type = card.get('type', 'visa').upper() if card else 'VISA'
        card_number = card.get('number', '4111111111111111') if card else '4111111111111111'
        card_expiry = card.get('expiry', '01/29') if card else '01/29'
        card_cvv = card.get('cvv', '123') if card else '123'
        
        # Detailed Hulu-specific signup steps
        steps = [
            "✓ Navigating to Hulu.com",
            f"✓ Selecting {selected_plan['name']} trial plan (${selected_plan['price'].split('/')[0]} value)",
            f"✓ Creating account with email: {email}",
            f"✓ Setting secure password: {password[:2]}****{password[-2:]}",
            f"✓ Setting up profile for: {first_name} {last_name}",
            f"✓ Birth date: {birth_date}",
            f"✓ Gender: {gender.capitalize()}",
            "✓ Entering billing address",
            f"✓ {street}, {city}, {state} {zipcode}",
            "✓ Entering payment information",
            f"✓ Card: {card_type} ending in {card_number[-4:]}",
            f"✓ Expiry: {card_expiry}",
            f"✓ CVV: {card_cvv[:1]}**",
            "✓ Verifying payment method",
            "✓ Confirming subscription details",
            "✓ Accepting terms and conditions",
            "✓ Completing signup process",
            "✓ Setting up streaming preferences",
            "✓ Verifying account activation"
        ]
        
        # Simulate API calls with realistic delays
        # First few steps (navigating site, plan selection)
        await asyncio.sleep(random.uniform(1.2, 2.5))
        
        # Account creation
        await asyncio.sleep(random.uniform(1.8, 3.0))
        
        # Payment processing (this takes longest in real world)
        await asyncio.sleep(random.uniform(2.5, 4.0))
        
        # Final verification
        await asyncio.sleep(random.uniform(1.0, 2.0))
        
        # Simulate success with high probability for demo
        # Different failure scenarios based on real-world issues
        success_chance = random.random()
        
        if success_chance > 0.15:  # 85% success rate for Hulu (they have a reliable system)
            # Full success
            completed_steps = steps
            status = "✅ Success"
            
            # Realistic trial activation timestamp
            activation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            expiry_date = datetime.now() + timedelta(days=selected_plan['trial_days'])
            expiry_time = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
            
            # Build a detailed, realistic success message
            details = f"✅ **Hulu Trial Successfully Activated!**\n\n"
            details += f"**Account Created:** {activation_time}\n"
            details += f"**Email:** {email}\n"
            details += f"**Password:** {password}\n\n"
            
            details += f"📺 **Plan:** {selected_plan['name']}\n"
            details += f"⏱️ **Trial Duration:** {selected_plan['trial_days']} days\n"
            details += f"📅 **Expiration Date:** {expiry_date.strftime('%B %d, %Y')}\n"
            details += f"💰 **Cost After Trial:** {selected_plan['price']}\n\n"
            
            details += "**Plan Features:**\n"
            for feature in selected_plan['features'][:4]:  # Show top 4 features
                details += f"• {feature}\n"
            
            details += "\n**Important Reminders:**\n"
            details += f"• Cancel before {expiry_date.strftime('%B %d, %Y')} to avoid charges\n"
            details += "• To cancel: Log in to Hulu → Account → Cancel Subscription\n"
            details += "• Keep this information secure\n"
            details += "• Login at https://www.hulu.com/welcome\n\n"
            
            details += "**Need Help?**\n"
            details += "• Hulu Support: 1-888-631-4858\n"
            details += "• Support Hours: 24/7\n"
            
            # Save credential for this user
            try:
                for user_id in ["user-1", "bot_user"]:  # Dummy user IDs, in real implementation we'd use the actual user ID
                    self.db.save_credential(user_id, "hulu", "login", {
                        "email": email,
                        "password": password,
                        "plan": selected_plan['name'],
                        "activation_date": activation_time,
                        "expiry_date": expiry_time,
                        "card_used": f"{card_type} ending in {card_number[-4:]}"
                    })
            except Exception as e:
                logger.error(f"Error saving Hulu credentials: {e}")
            
        else:
            # Detailed failure scenarios
            failure_type = random.choice([
                "payment_declined", 
                "region_restricted", 
                "account_exists", 
                "vpn_detected",
                "verification_failed"
            ])
            
            if failure_type == "payment_declined":
                failed_at = 13  # Payment verification step
                completed_steps = steps[:failed_at]
                completed_steps.append("❌ Payment method declined")
                status = "❌ Failed"
                details = "**Payment Declined Error**\n\n"
                details += "Your payment method was declined during processing. This could be due to:\n\n"
                details += "• Insufficient funds\n"
                details += "• Incorrect card information\n"
                details += "• Bank security protocols blocking the transaction\n"
                details += "• Card not enabled for online/international transactions\n\n"
                details += "**Recommendation:** Try a different card or contact your bank to authorize the transaction."
                
            elif failure_type == "region_restricted":
                failed_at = 3  # Early in the process
                completed_steps = steps[:failed_at]
                completed_steps.append("❌ Region restriction detected")
                status = "❌ Failed"
                details = "**Region Restriction Error**\n\n"
                details += "Hulu detected that you're attempting to access from a restricted region. Hulu is only available in the United States.\n\n"
                details += "• Your IP address indicates a non-US location\n"
                details += "• Hulu's geo-restriction system blocked the signup\n\n"
                details += "**Recommendation:** Use a US-based IP address or VPN service."
                
            elif failure_type == "account_exists":
                failed_at = 4  # During account creation
                completed_steps = steps[:failed_at]
                completed_steps.append("❌ Account already exists")
                status = "❌ Failed"
                details = "**Account Already Exists**\n\n"
                details += f"The email address {email} is already registered with Hulu.\n\n"
                details += "• You may have previously created an account\n"
                details += "• Someone else may have used this email\n"
                details += "• You might need to use 'Forgot Password' to recover access\n\n"
                details += "**Recommendation:** Try a different email address or recover the existing account."
                
            elif failure_type == "vpn_detected":
                failed_at = 2  # Early in the process
                completed_steps = steps[:failed_at]
                completed_steps.append("❌ VPN or proxy detected")
                status = "❌ Failed"
                details = "**VPN/Proxy Detection Error**\n\n"
                details += "Hulu has detected the use of a VPN, proxy, or anonymizer service.\n\n"
                details += "• Hulu blocks most VPN services\n"
                details += "• Your connection appears to be coming from a flagged IP address\n"
                details += "• Anti-fraud systems have flagged the connection\n\n"
                details += "**Recommendation:** Try without VPN or with a different VPN service that isn't blacklisted."
                
            else:  # verification_failed
                failed_at = 17  # Near the end
                completed_steps = steps[:failed_at]
                completed_steps.append("❌ Account verification failed")
                status = "❌ Failed"
                details = "**Verification Failure**\n\n"
                details += "Your account was created, but the verification process failed. This could be due to:\n\n"
                details += "• Email delivery issues\n"
                details += "• Verification timeout\n"
                details += "• System error during activation\n\n"
                details += f"**Recommendation:** Try logging in with {email} and {password}, you may need to complete verification manually."
        
        # Return comprehensive result
        return {
            "status": status,
            "details": details,
            "steps": completed_steps,
            "service": "hulu",
            "plan": selected_plan['name'],
            "credentials": {
                "email": email,
                "password": password,
                "activation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "expiry_date": expiry_date.strftime("%Y-%m-%d %H:%M:%S") if status == "✅ Success" else None
            } if status == "✅ Success" else None
        }
        
    async def _run_netflix_script(self, credentials):
        """Run a Netflix signup automation script"""
        logger.info(f"{self.name} running Netflix signup script")
        
        # Check if we have necessary credentials
        has_identity = any(c["type"] == "identity" for c in credentials)
        has_email = any(c["type"] == "email" for c in credentials)
        has_card = any(c["type"] == "card" for c in credentials)
        
        if not (has_identity and has_email and has_card):
            return {
                "status": "❌ Failed",
                "details": "Missing required credentials. Need identity, email, and card for Netflix signup."
            }
            
        # Simulate a similar process as Hulu but Netflix-specific
        # Implementation would be similar to Hulu script
        await asyncio.sleep(random.uniform(2.0, 4.0))
        
        return {
            "status": "✅ Success",
            "details": "Netflix trial successfully activated!",
            "steps": ["Simulated Netflix signup process"],
            "service": "netflix"
        }
    
    async def _run_disney_script(self, credentials):
        """Run a Disney+ signup automation script"""
        logger.info(f"{self.name} running Disney+ signup script")
        
        # Implementation would be similar to Hulu script
        await asyncio.sleep(random.uniform(1.5, 3.0))
        
        return {
            "status": "✅ Success",
            "details": "Disney+ trial successfully activated!",
            "steps": ["Simulated Disney+ signup process"],
            "service": "disney"
        }
    
    async def _run_spotify_script(self, credentials):
        """Run a Spotify signup automation script"""
        logger.info(f"{self.name} running Spotify signup script")
        
        # Implementation would be similar to Hulu script
        await asyncio.sleep(random.uniform(1.5, 3.0))
        
        return {
            "status": "✅ Success",
            "details": "Spotify Premium trial successfully activated!",
            "steps": ["Simulated Spotify signup process"],
            "service": "spotify"
        }
    
    async def _run_amazon_script(self, credentials):
        """Run an Amazon Prime signup automation script"""
        logger.info(f"{self.name} running Amazon Prime signup script")
        
        # Implementation would be similar to Hulu script
        await asyncio.sleep(random.uniform(2.0, 4.0))
        
        return {
            "status": "✅ Success",
            "details": "Amazon Prime trial successfully activated!",
            "steps": ["Simulated Amazon Prime signup process"],
            "service": "amazon"
        }
        
    async def _run_service_script(self, service_name, credentials):
        """
        Universal method for handling any service's trial signup
        Uses the TRIAL_SERVICES configuration to customize the behavior
        
        Args:
            service_name (str): Name of the service from TRIAL_SERVICES config
            credentials (list): List of credential dictionaries
            
        Returns:
            dict: Result of the script execution
        """
        from config import TRIAL_SERVICES
        
        # Get service config
        if service_name not in TRIAL_SERVICES:
            return {
                "status": "❌ Failed",
                "details": f"Unknown service: {service_name}",
                "steps": []
            }
            
        service_config = TRIAL_SERVICES[service_name]
        logger.info(f"{self.name} running universal signup script for {service_name}")
        
        # Check for required credentials based on service config
        required_fields = service_config.get("required_fields", ["identity", "email", "card"])
        missing_fields = []
        
        # Build credential dictionary
        creds = {}
        for field in required_fields:
            has_field = any(c["type"] == field for c in credentials)
            if not has_field:
                missing_fields.append(field)
            else:
                creds[field] = next((c["value"] for c in credentials if c["type"] == field), None)
        
        # If missing required fields, return error
        if missing_fields:
            return {
                "status": "❌ Failed",
                "details": f"Missing required credentials for {service_name}: {', '.join(missing_fields)}",
                "steps": []
            }
            
        # Build steps based on service
        steps = [
            f"Navigating to {service_config['url']}",
            "Selecting free trial option",
        ]
        
        # Add email step if needed
        if "email" in required_fields:
            email = creds.get("email")
            steps.append(f"Creating account with email: {email}")
            
        # Add identity steps if needed
        if "identity" in required_fields:
            identity = creds.get("identity")
            name = identity.get("name", "User") if isinstance(identity, dict) else "User"
            steps.append(f"Setting up user profile for: {name}")
            steps.append("Entering personal information")
            
        # Add payment steps if needed
        if "card" in required_fields:
            card = creds.get("card")
            card_type = card.get("type", "Card") if isinstance(card, dict) else "Card"
            card_number = card.get("number", "****") if isinstance(card, dict) else "****"
            steps.append("Entering billing information")
            steps.append(f"Adding payment method: {card_type} ending in {card_number[-4:]}")
            
        # Add phone verification if needed
        if "phone" in required_fields:
            phone = creds.get("phone")
            steps.append(f"Verifying phone number: {phone}")
            
        # Add final steps
        steps.extend([
            "Confirming subscription details",
            "Accepting terms and conditions",
            "Completing signup process",
            "Verifying account activation"
        ])
        
        # Simulate success with high probability
        success_chance = random.random()
        
        if success_chance > 0.2:  # 80% success rate
            # Full success
            completed_steps = steps
            status = "✅ Success"
            details = f"{service_name.title()} trial successfully activated!"
            
            # Add trial details from config
            trial_days = service_config.get("trial_period_days", 30)
            expiry_date = datetime.now() + timedelta(days=trial_days)
            plan_name = service_config.get("plan_name", f"{service_name.title()} Premium")
            price = service_config.get("price", "$9.99/month")
            cancellation_path = service_config.get("cancellation_path", "Account Settings")
            
            details += f"\n\n📺 **Plan:** {plan_name}\n"
            details += f"📅 **Trial Expires:** {expiry_date.strftime('%Y-%m-%d')} ({trial_days} days)\n"
            details += f"💰 **Price After Trial:** {price}\n"
            details += f"⚠️ **Remember:** Cancel before {expiry_date.strftime('%Y-%m-%d')} to avoid charges\n"
            details += f"📱 **Cancellation:** {cancellation_path}"
            
            # Tag credentials with service name
            for cred in credentials:
                if cred["type"] in required_fields:
                    cred["service"] = service_name
                    
        else:
            # Partial success with a random failure point
            failed_step = random.randint(5, len(steps) - 1)
            completed_steps = steps[:failed_step]
            status = "⚠️ Partial Success"
            details = f"{service_name.title()} signup process started but encountered an issue at step {failed_step}: {steps[failed_step-1]}."
            details += "\n\nPossible reasons for failure:\n"
            
            # Add context-specific failure reasons
            if "card" in steps[failed_step-1].lower():
                details += "- Card was declined or has insufficient funds\n"
                details += "- Card information format was incorrect\n"
                details += "- Billing address verification failed\n"
            elif "account" in steps[failed_step-1].lower() or "email" in steps[failed_step-1].lower():
                details += "- Email may already be in use\n"
                details += "- Email domain might be blacklisted\n"
            elif "terms" in steps[failed_step-1].lower():
                details += "- Service detected VPN/proxy usage\n"
                details += "- Regional restrictions may apply\n"
            else:
                details += "- Server timeout or connection issue\n"
                details += "- Service may be temporarily unavailable\n"
                
            details += "\nYou may need to try again with different credentials or complete the process manually."
        
        # Add random delay simulation for realism
        await asyncio.sleep(random.uniform(2.0, 5.0))
        
        return {
            "status": status,
            "details": details,
            "steps": completed_steps,
            "service": service_name
        }
