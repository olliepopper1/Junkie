#!/usr/bin/env python3
"""
Trial Junkie Setup
Initializes and tests all components of the Trial Junkie system
"""
import os
import sys
import json
import logging
import inspect
import importlib
from datetime import datetime
from pprint import pprint
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("setup_trialjunkie.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("setup_trialjunkie")

def check_environment_variables() -> Dict[str, Any]:
    """Check necessary environment variables"""
    result = {
        "success": True,
        "variables": {
            "RAPIDAPI_KEY": bool(os.getenv("RAPIDAPI_KEY")),
            "DISCORD_BOT_TOKEN": bool(os.getenv("DISCORD_BOT_TOKEN")),
            "DATABASE_URL": bool(os.getenv("DATABASE_URL"))
        },
        "message": "Environment variable check completed"
    }
    
    missing = [var for var, present in result["variables"].items() if not present]
    
    if missing:
        result["success"] = False
        result["message"] = f"Missing environment variables: {', '.join(missing)}"
    
    return result

def check_required_modules() -> Dict[str, Any]:
    """Check for required Python modules"""
    required_modules = [
        "discord",
        "flask",
        "sqlalchemy",
        "requests",
        "psycopg2",
        "python-dotenv",
        "gunicorn"
    ]
    
    result = {
        "success": True,
        "modules": {},
        "message": "Module check completed"
    }
    
    for module in required_modules:
        module_name = module.replace("-", "_")
        try:
            imported = importlib.import_module(module_name)
            version = getattr(imported, "__version__", "Unknown")
            result["modules"][module] = {
                "installed": True,
                "version": version
            }
        except ImportError:
            result["modules"][module] = {
                "installed": False,
                "version": None
            }
    
    missing = [mod for mod, data in result["modules"].items() if not data["installed"]]
    
    if missing:
        result["success"] = False
        result["message"] = f"Missing required modules: {', '.join(missing)}"
    
    return result

def check_api_connectivity() -> Dict[str, Any]:
    """Check RapidAPI connectivity"""
    try:
        from updated_api_integrations import UpdatedAPIIntegrations
        
        api = UpdatedAPIIntegrations()
        result = {
            "success": True,
            "apis": {},
            "message": "API connectivity check completed"
        }
        
        # Check identity generation
        try:
            identity = api.generate_identity()
            result["apis"]["identity_api"] = {
                "working": bool(identity and isinstance(identity, dict) and "first_name" in identity),
                "sample": identity
            }
        except Exception as e:
            result["apis"]["identity_api"] = {
                "working": False,
                "error": str(e)
            }
        
        # Check phone validation
        try:
            phone = api.generate_virtual_number()
            result["apis"]["phone_api"] = {
                "working": bool(phone and isinstance(phone, dict) and "number" in phone),
                "sample": phone
            }
        except Exception as e:
            result["apis"]["phone_api"] = {
                "working": False,
                "error": str(e)
            }
        
        # Check card generation
        try:
            card = api.generate_card("visa")
            result["apis"]["card_api"] = {
                "working": bool(card and isinstance(card, dict) and "number" in card),
                "sample": card
            }
        except Exception as e:
            result["apis"]["card_api"] = {
                "working": False,
                "error": str(e)
            }
        
        # Check email generation
        try:
            email = api.generate_email()
            result["apis"]["email_api"] = {
                "working": bool(email and isinstance(email, str) and "@" in email),
                "sample": email
            }
        except Exception as e:
            result["apis"]["email_api"] = {
                "working": False,
                "error": str(e)
            }
        
        # Check if any APIs are working
        working_apis = sum(1 for api_data in result["apis"].values() if api_data.get("working", False))
        
        if working_apis == 0:
            result["success"] = False
            result["message"] = "No APIs are working. Check your RAPIDAPI_KEY."
        elif working_apis < len(result["apis"]):
            result["message"] = f"{working_apis}/{len(result['apis'])} APIs are working. Some features may be limited."
        
        return result
    
    except ImportError:
        return {
            "success": False,
            "message": "API integrations module not found",
            "apis": {}
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error checking API connectivity: {str(e)}",
            "apis": {}
        }

def check_database_connectivity() -> Dict[str, Any]:
    """Check database connectivity"""
    try:
        from database import Database
        
        db = Database()
        result = db.initialize()
        
        if result.get("success", False):
            # Try to create a test table
            try:
                db_result = db.execute_query(
                    "CREATE TABLE IF NOT EXISTS setup_test "
                    "(id SERIAL PRIMARY KEY, test_date TIMESTAMP DEFAULT NOW())"
                )
                
                if db_result.get("success", False):
                    # Insert a test record
                    insert_result = db.execute_query(
                        "INSERT INTO setup_test (test_date) VALUES (NOW()) RETURNING id"
                    )
                    
                    if insert_result.get("success", False):
                        # Get the test record
                        select_result = db.execute_query(
                            "SELECT * FROM setup_test ORDER BY id DESC LIMIT 1"
                        )
                        
                        if select_result.get("success", False):
                            return {
                                "success": True,
                                "message": "Database connection and operations successful",
                                "details": {
                                    "test_record": select_result.get("data", [])
                                }
                            }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Database operations failed: {str(e)}",
                    "connection": result
                }
        
        return result
    
    except ImportError:
        return {
            "success": False,
            "message": "Database module not found"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error checking database connectivity: {str(e)}"
        }

def test_trial_generation() -> Dict[str, Any]:
    """Test trial generation"""
    try:
        from trial_junkie_system import TrialJunkieSystem
        
        system = TrialJunkieSystem()
        result = system.generate_trial("hulu")
        
        if result.get("success", False) and "trial_data" in result:
            trial_data = result.get("trial_data", {})
            
            return {
                "success": True,
                "message": "Trial generation successful",
                "trial_data_sample": {
                    "service": trial_data.get("service"),
                    "email": trial_data.get("email"),
                    "password": "********",  # Redacted for security
                    "end_date": trial_data.get("end_date")
                },
                "file_path": result.get("file_path")
            }
        
        return result
    
    except ImportError:
        return {
            "success": False,
            "message": "Trial Junkie system module not found"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error testing trial generation: {str(e)}"
        }

def setup() -> Dict[str, Any]:
    """Run the complete setup process"""
    setup_start = datetime.now()
    logger.info("Starting Trial Junkie setup")
    
    results = {
        "timestamp": setup_start.isoformat(),
        "success": True,
        "errors": []
    }
    
    try:
        env_check = check_environment_variables()
        results["environment_variables"] = env_check
        if not env_check["success"]:
            results["success"] = False
            results["errors"].append(f"Environment error: {env_check['message']}")
            
        mod_check = check_required_modules()
        results["required_modules"] = mod_check
        if not mod_check["success"]:
            results["success"] = False 
            results["errors"].append(f"Module error: {mod_check['message']}")

        api_check = check_api_connectivity()
        results["api_connectivity"] = api_check
        if not api_check["success"]:
            results["success"] = False
            results["errors"].append("API connectivity failed")

        db_check = check_database_connectivity()
        results["database_connectivity"] = db_check
        if not db_check["success"]:
            results["success"] = False
            results["errors"].append("Database initialization failed")

    except Exception as e:
        results["success"] = False
        results["errors"].append(f"Setup error: {str(e)}")
    
    # Calculate success rate
    total_checks = len(results) - 1  # Exclude timestamp
    successful_checks = sum(1 for key, value in results.items() 
                          if key != "timestamp" and value.get("success", False))
    
    results["summary"] = {
        "success_rate": f"{successful_checks}/{total_checks}",
        "percentage": round((successful_checks / total_checks) * 100, 2),
        "setup_duration_seconds": (datetime.now() - setup_start).total_seconds(),
        "setup_completed": True,
        "ready_for_use": successful_checks >= total_checks - 1  # Allow one check to fail
    }
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"setup_results_{timestamp}.json"
    
    with open(file_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Setup completed with {successful_checks}/{total_checks} successful checks")
    logger.info(f"Results saved to {file_path}")
    
    return results

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Trial Junkie Setup")
    parser.add_argument("--check", "-c", 
                        choices=["all", "env", "modules", "api", "database", "trial"],
                        default="all", 
                        help="Specific check to run")
    
    args = parser.parse_args()
    
    if args.check == "env" or args.check == "all":
        print("\n=== Environment Variables Check ===")
        env_results = check_environment_variables()
        print(f"Success: {env_results['success']}")
        print(f"Message: {env_results['message']}")
        print("Variables:")
        for var, present in env_results["variables"].items():
            print(f"  {var}: {'✅ Present' if present else '❌ Missing'}")
    
    if args.check == "modules" or args.check == "all":
        print("\n=== Required Modules Check ===")
        mod_results = check_required_modules()
        print(f"Success: {mod_results['success']}")
        print(f"Message: {mod_results['message']}")
        print("Modules:")
        for mod, data in mod_results["modules"].items():
            status = f"✅ v{data['version']}" if data["installed"] else "❌ Missing"
            print(f"  {mod}: {status}")
    
    if args.check == "api" or args.check == "all":
        print("\n=== API Connectivity Check ===")
        api_results = check_api_connectivity()
        print(f"Success: {api_results['success']}")
        print(f"Message: {api_results['message']}")
        print("APIs:")
        for api, data in api_results.get("apis", {}).items():
            status = "✅ Working" if data.get("working", False) else f"❌ Error: {data.get('error', 'Unknown error')}"
            print(f"  {api}: {status}")
    
    if args.check == "database" or args.check == "all":
        print("\n=== Database Connectivity Check ===")
        db_results = check_database_connectivity()
        print(f"Success: {db_results['success']}")
        print(f"Message: {db_results['message']}")
    
    if args.check == "trial" or args.check == "all":
        print("\n=== Trial Generation Test ===")
        trial_results = test_trial_generation()
        print(f"Success: {trial_results['success']}")
        print(f"Message: {trial_results['message']}")
        
        if "trial_data_sample" in trial_results:
            print("Sample Data:")
            pprint(trial_results["trial_data_sample"])
    
    if args.check == "all":
        print("\n=== Setup Summary ===")
        results = setup()
        summary = results["summary"]
        
        print(f"Success Rate: {summary['success_rate']} ({summary['percentage']}%)")
        print(f"Setup Duration: {summary['setup_duration_seconds']:.2f} seconds")
        print(f"Ready for Use: {'✅ Yes' if summary['ready_for_use'] else '❌ No'}")
        
        # Print setup advice based on results
        if summary["ready_for_use"]:
            print("\n✅ Trial Junkie is ready to use!")
            print("You can now start the Discord bot with:")
            print("  python run_discord_integration.py")
        else:
            print("\n⚠️ Setup completed with some issues:")
            
            if not results["environment_variables"]["success"]:
                print("  - Missing environment variables. Check .env file.")
            
            if not results["required_modules"]["success"]:
                print("  - Missing required modules. Run: pip install -r requirements.txt")
            
            if not results["api_connectivity"]["success"]:
                print("  - API connectivity issues. Check your RAPIDAPI_KEY.")
            
            if not results["database_connectivity"]["success"]:
                print("  - Database connectivity issues. Check your DATABASE_URL.")
            
            if not results["trial_generation"]["success"]:
                print("  - Trial generation failed. Check previous logs for details.")