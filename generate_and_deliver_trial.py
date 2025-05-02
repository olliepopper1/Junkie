"""
Generate and Deliver Hulu Trial
End-to-end script to generate a trial and deliver it to a user
"""
import argparse
import logging
import sys
from simplified_hulu_trial import SimpleTrialGenerator
from bot_trial_delivery import TrialDelivery

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("generate_and_deliver_trial.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def generate_and_deliver_trial(user_id, discord_id=None, service="hulu", plan_index=1):
    """
    End-to-end process to generate and deliver a trial to a user
    
    Args:
        user_id: The user ID for saving to the database
        discord_id: Optional Discord ID for delivering via Discord
        service: The service to generate a trial for (default: hulu)
        plan_index: The plan index to use (default: 1 for No Ads)
        
    Returns:
        dict: Complete information about the generation and delivery
    """
    logger.info(f"Starting end-to-end trial generation and delivery for user {user_id}")
    
    # Step 1: Generate the trial
    logger.info("Step 1: Generating trial")
    generator = SimpleTrialGenerator()
    trial_data = generator.generate_trial(service, plan_index)
    
    if not trial_data or "error" in trial_data:
        logger.error(f"Trial generation failed: {trial_data.get('error', 'Unknown error')}")
        return {"success": False, "message": f"Trial generation failed: {trial_data.get('error', 'Unknown error')}"}
    
    logger.info(f"Trial generated for {service}")
    
    # Step 2: Deliver the trial
    logger.info("Step 2: Delivering trial")
    delivery = TrialDelivery()
    delivery_result = delivery.deliver_trial_to_user(user_id, discord_id)
    
    if not delivery_result["success"]:
        logger.error(f"Trial delivery failed: {delivery_result.get('message', 'Unknown error')}")
        return {"success": False, "message": f"Trial delivery failed: {delivery_result.get('message', 'Unknown error')}"}
    
    logger.info("Trial successfully delivered")
    
    # Return the complete result
    return {
        "success": True,
        "message": "Trial generation and delivery completed successfully",
        "trial_data": trial_data,
        "delivery_result": delivery_result
    }

def main():
    """Main function to run from command line"""
    parser = argparse.ArgumentParser(description="Generate and deliver a Hulu trial")
    parser.add_argument("--user-id", type=int, required=True, help="User ID for saving to database")
    parser.add_argument("--discord-id", type=str, help="Discord ID for Discord delivery")
    parser.add_argument("--service", type=str, default="hulu", help="Service to generate a trial for")
    parser.add_argument("--plan-index", type=int, default=1, help="Plan index to use")
    
    args = parser.parse_args()
    
    result = generate_and_deliver_trial(
        args.user_id,
        args.discord_id,
        args.service,
        args.plan_index
    )
    
    if result["success"]:
        print("✓ Trial generation and delivery completed successfully")
        print(f"Trial service: {result['trial_data']['service']}")
        print(f"Trial plan: {result['trial_data']['plan']}")
        print(f"Login: {result['trial_data']['email']} / {result['trial_data']['password']}")
    else:
        print(f"✗ Error: {result['message']}")

if __name__ == "__main__":
    print("=== Trial Generation and Delivery System ===")
    
    # For interactive testing without command-line arguments
    if len(sys.argv) == 1:
        # Use test user ID and discord_id without prompting
        test_user_id = 12345
        test_discord_id = None
        
        print(f"Using default user ID: {test_user_id}")
        print(f"Using default Discord ID: {test_discord_id if test_discord_id else 'None'}")
        
        result = generate_and_deliver_trial(test_user_id, test_discord_id)
        
        if result["success"]:
            print("\n=== Trial Generation and Delivery Successful ===")
            print(f"Service: {result['trial_data']['service']}")
            print(f"Plan: {result['trial_data']['plan']}")
            print(f"Email: {result['trial_data']['email']}")
            print(f"Password: {result['trial_data']['password']}")
            print(f"Trial end date: {result['trial_data']['end_date']}")
            
            if test_discord_id:
                print("\nMessage would be delivered to Discord.")
            
            print("\nTrial has been saved to the database for dashboard display.")
        else:
            print(f"\n=== Error ===\n{result['message']}")
    else:
        # Use command-line arguments
        main()