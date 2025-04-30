#!/usr/bin/env python3
"""
Verify API Integrations for Trial Junkie
Tests all API connections and outputs results
"""
import time
import logging
from api_integrations import APIIntegrations

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("verify_apis")

def test_identity_generation():
    """Test the identity generation API"""
    logger.info("Testing identity generation...")
    try:
        identity = APIIntegrations.generate_identity()
        if identity and identity.get("first_name") and identity.get("last_name"):
            logger.info(f"✅ Successfully generated identity: {identity['first_name']} {identity['last_name']}")
            return True
        else:
            logger.error("❌ Generated identity data is incomplete")
            return False
    except Exception as e:
        logger.error(f"❌ Error generating identity: {e}")
        return False

def test_virtual_number():
    """Test the virtual number API"""
    logger.info("Testing virtual number generation...")
    try:
        phone = APIIntegrations.generate_virtual_number()
        if phone and phone.get("phone_number") and phone.get("verification_code"):
            logger.info(f"✅ Successfully generated virtual number: {phone['phone_number']}")
            return True
        else:
            logger.error("❌ Generated phone data is incomplete")
            return False
    except Exception as e:
        logger.error(f"❌ Error generating virtual number: {e}")
        return False

def test_card_generation():
    """Test the card generation API"""
    logger.info("Testing card generation...")
    try:
        card = APIIntegrations.generate_card()
        if card and card.get("card_number") and card.get("cvv"):
            logger.info(f"✅ Successfully generated card: {card['card_type']} ending with {card['card_number'][-4:]}")
            return True
        else:
            logger.error("❌ Generated card data is incomplete")
            return False
    except Exception as e:
        logger.error(f"❌ Error generating card: {e}")
        return False

def test_virtual_card():
    """Test the virtual card API"""
    logger.info("Testing virtual card generation...")
    try:
        card = APIIntegrations.generate_virtual_card(amount=1.00)
        if card and card.get("card_number") and card.get("cvv"):
            logger.info(f"✅ Successfully generated virtual card with ${card.get('amount', 0)} limit")
            return True
        else:
            logger.error("❌ Generated virtual card data is incomplete")
            return False
    except Exception as e:
        logger.error(f"❌ Error generating virtual card: {e}")
        return False

def test_email_generation():
    """Test the email generation API"""
    logger.info("Testing email generation...")
    try:
        email = APIIntegrations.generate_email()
        if email and email.get("email") and email.get("password"):
            logger.info(f"✅ Successfully generated email: {email['email']}")
            return True
        else:
            logger.error("❌ Generated email data is incomplete")
            return False
    except Exception as e:
        logger.error(f"❌ Error generating email: {e}")
        return False

def test_complete_trial_data():
    """Test the complete trial data generation"""
    logger.info("Testing complete trial data generation...")
    try:
        data = APIIntegrations.generate_complete_trial_data("netflix")
        if (data and data.get("user_info") and data.get("payment_info") and 
            data["user_info"].get("email") and data["payment_info"].get("card_number")):
            logger.info(f"✅ Successfully generated complete trial data for Netflix")
            return True
        else:
            logger.error("❌ Generated trial data is incomplete")
            return False
    except Exception as e:
        logger.error(f"❌ Error generating complete trial data: {e}")
        return False

def run_all_tests():
    """Run all API tests and output results"""
    logger.info("🔍 STARTING API VERIFICATION")
    logger.info("===========================")
    
    results = {
        "Identity Generation": test_identity_generation(),
        "Virtual Number": test_virtual_number(),
        "Card Generation": test_card_generation(),
        "Virtual Card": test_virtual_card(),
        "Email Generation": test_email_generation(),
        "Complete Trial Data": test_complete_trial_data()
    }
    
    logger.info("\n📊 TEST RESULTS SUMMARY")
    logger.info("===========================")
    success_count = 0
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        if result:
            success_count += 1
        logger.info(f"{test_name}: {status}")
    
    success_percentage = (success_count / len(results)) * 100
    logger.info(f"\nOverall Success Rate: {success_percentage:.1f}%")
    
    if success_percentage == 100:
        logger.info("🎉 All API integrations are working correctly!")
    elif success_percentage >= 50:
        logger.info("⚠️ Some API integrations are working, but others need attention.")
    else:
        logger.info("❌ Most API integrations are not working correctly. Please check your API keys.")
    
    return results

if __name__ == "__main__":
    run_all_tests()