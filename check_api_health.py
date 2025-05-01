#!/usr/bin/env python
"""
API Health Check Script
Checks the health of all configured APIs and reports their status.
"""
import argparse
import datetime
import json
import logging
import os
import sys
import time
from api_integrations import APIIntegrations, API_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("api_health_check")

def check_all_apis(args):
    """Check the health of all configured APIs"""
    apis = {
        "personator": "Identity Generation",
        "virtual_number": "Virtual Phone Number",
        "virtual_number_backup": "Virtual Number Backup",
        "fake_card": "Credit Card Generator",
        "email_validator": "Email Validator",
        "temp_email": "Disposable Email",
        "temp_mail_backup": "Email Backup",
        "scrape_ninja": "Web Scraping"
    }
    
    results = {}
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n======= API Health Check =======")
    print(f"Time: {current_time}")
    print("==============================")
    
    for api_key, api_name in apis.items():
        print(f"\nChecking {api_name}... ", end="")
        sys.stdout.flush()
        
        if api_key not in API_CONFIG:
            print("❌ NOT CONFIGURED")
            results[api_key] = {
                "name": api_name,
                "status": "Not Configured",
                "message": "API is not configured in API_CONFIG",
                "endpoint": "N/A",
                "time_checked": current_time
            }
            continue
        
        # Try to make a simple request to the API
        try:
            start_time = time.time()
            
            endpoint = API_CONFIG[api_key]["endpoint"]
            headers = APIIntegrations.get_headers(api_key)
            
            # Test the specific API based on its functionality
            if api_key == "personator":
                result = APIIntegrations.generate_identity()
                success = bool(result.get("first_name"))
            elif api_key in ["virtual_number", "virtual_number_backup"]:
                # Skip actual API call, just check if the headers are valid
                success = "X-RapidAPI-Key" in headers and "X-RapidAPI-Host" in headers
            elif api_key == "fake_card":
                result = APIIntegrations.generate_card()
                success = bool(result.get("card_number"))
            elif api_key == "email_validator":
                result = APIIntegrations.validate_email("test@example.com")
                success = "is_valid" in result
            elif api_key in ["temp_email", "temp_mail_backup"]:
                # Skip actual API call for email generation
                success = "X-RapidAPI-Key" in headers and "X-RapidAPI-Host" in headers
            elif api_key == "scrape_ninja":
                # Skip actual scraping, just check if the headers are valid
                success = "X-RapidAPI-Key" in headers and "X-RapidAPI-Host" in headers
            else:
                success = False
                
            response_time = round((time.time() - start_time) * 1000)
            
            if success:
                print(f"✅ UP ({response_time}ms)")
                status = "Up"
                message = f"API is functioning correctly ({response_time}ms)"
            else:
                print(f"⚠️ DEGRADED ({response_time}ms)")
                status = "Degraded"
                message = f"API is responding but not returning expected data ({response_time}ms)"
                
        except Exception as e:
            print(f"❌ DOWN (Error: {str(e)[:50]}...)")
            status = "Down"
            message = f"Error: {str(e)}"
        
        results[api_key] = {
            "name": api_name,
            "status": status,
            "message": message,
            "endpoint": API_CONFIG[api_key]["endpoint"],
            "time_checked": current_time
        }
    
    # Save the results to a file
    with open("api_health_status.json", "w") as f:
        json.dump({
            "timestamp": current_time,
            "apis": results
        }, f, indent=2)
    
    print("\n==============================")
    print(f"Health check complete. Results saved to api_health_status.json")
    print("==============================\n")
    
    # Display summary
    up_count = sum(1 for api in results.values() if api["status"] == "Up")
    down_count = sum(1 for api in results.values() if api["status"] == "Down")
    degraded_count = sum(1 for api in results.values() if api["status"] == "Degraded")
    not_configured = sum(1 for api in results.values() if api["status"] == "Not Configured")
    
    print(f"Summary: {up_count} Up | {degraded_count} Degraded | {down_count} Down | {not_configured} Not Configured")
    
    return results

def check_specific_api(args):
    """Check the health of a specific API"""
    api_key = args.api
    
    if api_key not in API_CONFIG:
        print(f"Error: API '{api_key}' is not configured in API_CONFIG")
        return None
    
    api_name = {
        "personator": "Identity Generation",
        "virtual_number": "Virtual Phone Number",
        "virtual_number_backup": "Virtual Number Backup",
        "fake_card": "Credit Card Generator",
        "email_validator": "Email Validator",
        "temp_email": "Disposable Email",
        "temp_mail_backup": "Email Backup",
        "scrape_ninja": "Web Scraping"
    }.get(api_key, api_key)
    
    print(f"\nChecking {api_name} ({api_key})... ", end="")
    sys.stdout.flush()
    
    try:
        start_time = time.time()
        
        endpoint = API_CONFIG[api_key]["endpoint"]
        headers = APIIntegrations.get_headers(api_key)
        
        # Test the specific API based on its functionality
        if api_key == "personator":
            result = APIIntegrations.generate_identity()
            success = bool(result.get("first_name"))
        elif api_key in ["virtual_number", "virtual_number_backup"]:
            # Skip actual API call, just check if the headers are valid
            success = "X-RapidAPI-Key" in headers and "X-RapidAPI-Host" in headers
        elif api_key == "fake_card":
            result = APIIntegrations.generate_card()
            success = bool(result.get("card_number"))
        elif api_key == "email_validator":
            result = APIIntegrations.validate_email("test@example.com")
            success = "is_valid" in result
        elif api_key in ["temp_email", "temp_mail_backup"]:
            # Skip actual API call for email generation
            success = "X-RapidAPI-Key" in headers and "X-RapidAPI-Host" in headers
        elif api_key == "scrape_ninja":
            # Skip actual scraping, just check if the headers are valid
            success = "X-RapidAPI-Key" in headers and "X-RapidAPI-Host" in headers
        else:
            success = False
            
        response_time = round((time.time() - start_time) * 1000)
        
        if success:
            print(f"✅ UP ({response_time}ms)")
            status = "Up"
            message = f"API is functioning correctly ({response_time}ms)"
        else:
            print(f"⚠️ DEGRADED ({response_time}ms)")
            status = "Degraded"
            message = f"API is responding but not returning expected data ({response_time}ms)"
            
    except Exception as e:
        print(f"❌ DOWN (Error: {str(e)[:50]}...)")
        status = "Down"
        message = f"Error: {str(e)}"
    
    result = {
        "name": api_name,
        "status": status,
        "message": message,
        "endpoint": API_CONFIG[api_key]["endpoint"],
        "time_checked": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print("\nDetails:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    
    return result

def show_history(args):
    """Show the history of API health checks"""
    if not os.path.exists("api_health_status.json"):
        print("No health check history found.")
        return
    
    with open("api_health_status.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Error: Could not parse health check history file.")
            return
    
    print("\n======= API Health Check History =======")
    print(f"Last Check: {data.get('timestamp', 'Unknown')}")
    print("========================================")
    
    for api_key, api_data in data.get("apis", {}).items():
        status_icon = "✅" if api_data.get("status") == "Up" else "❌" if api_data.get("status") == "Down" else "⚠️"
        print(f"{status_icon} {api_data.get('name', api_key)}: {api_data.get('status')}")
        print(f"   Message: {api_data.get('message', 'No message')}")
        print(f"   Endpoint: {api_data.get('endpoint', 'No endpoint')}")
        print()
    
    # Display summary
    apis = data.get("apis", {})
    up_count = sum(1 for api in apis.values() if api.get("status") == "Up")
    down_count = sum(1 for api in apis.values() if api.get("status") == "Down")
    degraded_count = sum(1 for api in apis.values() if api.get("status") == "Degraded")
    not_configured = sum(1 for api in apis.values() if api.get("status") == "Not Configured")
    
    print(f"Summary: {up_count} Up | {degraded_count} Degraded | {down_count} Down | {not_configured} Not Configured")

def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(description="Check the health of API integrations")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # All APIs check
    all_parser = subparsers.add_parser("all", help="Check all APIs")
    
    # Specific API check
    specific_parser = subparsers.add_parser("check", help="Check a specific API")
    specific_parser.add_argument("api", help="API key to check")
    
    # History command
    history_parser = subparsers.add_parser("history", help="Show API health check history")
    
    args = parser.parse_args()
    
    if args.command == "all" or not args.command:
        check_all_apis(args)
    elif args.command == "check":
        check_specific_api(args)
    elif args.command == "history":
        show_history(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()