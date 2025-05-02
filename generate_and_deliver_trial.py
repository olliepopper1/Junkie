"""
Generate and Deliver Trial
Main script to generate a real Hulu trial and deliver it to a user
"""
import logging
import sys
import argparse
from simplified_hulu_trial import SimpleTrialGenerator
from bot_trial_delivery import TrialDelivery

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("trial_generation.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def generate_and_deliver_trial(user_id, discord_id=None, service="hulu", plan_index=1):
    """
    Generate a trial and deliver it to the user
    
    Args:
        user_id: The user ID in the database
        discord_id: The Discord ID if available (for Discord delivery)
        service: The service to generate a trial for (default: hulu)
        plan_index: The index of the plan to use
        
    Returns:
        dict: Result of the generation and delivery process
    """
    logger.info(f"Generating {service} trial for user {user_id}")
    
    # Generate the trial
    generator = SimpleTrialGenerator()
    trial = generator.generate_trial(service_name=service, plan_index=plan_index)
    
    if not trial or not trial.get('success', False):
        logger.error("Trial generation failed")
        return {
            "success": False,
            "error": "Failed to generate trial",
            "details": trial
        }
    
    # Deliver the trial
    logger.info("Trial generated successfully, delivering to user")
    delivery = TrialDelivery()
    result = delivery.deliver_trial_to_user(user_id, discord_id)
    
    if not result.get('success', False):
        logger.error(f"Trial delivery failed: {result.get('error', 'Unknown error')}")
        return {
            "success": False,
            "error": "Failed to deliver trial",
            "details": result
        }
    
    logger.info(f"Trial successfully generated and delivered to user {user_id}")
    return {
        "success": True,
        "message": f"{service.capitalize()} trial successfully created and delivered",
        "trial": trial,
        "delivery": result
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate and deliver a trial to a user')
    parser.add_argument('--user_id', type=str, required=True, help='User ID in the database')
    parser.add_argument('--discord_id', type=str, help='Discord ID for delivery (optional)')
    parser.add_argument('--service', type=str, default='hulu', help='Service to generate trial for (default: hulu)')
    parser.add_argument('--plan', type=int, default=1, help='Plan index (default: 1, which is No Ads for Hulu)')
    
    args = parser.parse_args()
    
    print("=== Trial Generation and Delivery ===")
    print(f"Generating {args.service.capitalize()} trial for user {args.user_id}")
    
    result = generate_and_deliver_trial(
        user_id=args.user_id,
        discord_id=args.discord_id,
        service=args.service,
        plan_index=args.plan
    )
    
    if result["success"]:
        print("✅ Trial successfully generated and delivered!")
        print(f"\nService: {result['trial']['service']} - {result['trial']['plan']}")
        print(f"Email: {result['trial']['email']}")
        print(f"Password: {result['trial']['password']}")
        print(f"Trial End Date: {result['trial']['end_date']}")
        print("\nThis information has been saved to your account.")
        if args.discord_id:
            print("A message has also been sent to your Discord account.")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        if 'details' in result:
            print(f"Details: {result['details']}")