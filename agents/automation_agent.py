"""
Automation Agent (Shroomy Sal)
Handles browser automation for trial signups
"""
import logging
import asyncio
import random
from datetime import datetime

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
            "cancel": self._run_cancel_script
        }
        logger.info(f"{self.name} initialized")
    
    async def run_script(self, script_name, credentials):
        """Run an automation script"""
        script_name = script_name.lower()
        
        if script_name not in self.available_scripts:
            raise ValueError(f"Unknown script: {script_name}. Available scripts: {', '.join(self.available_scripts.keys())}")
        
        logger.info(f"{self.name} running script: {script_name}")
        
        # Run the appropriate script
        result = await self.available_scripts[script_name](credentials)
        
        return result
    
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
            expiry_date = datetime.now() + asyncio.timedelta(days=trial_days)
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
