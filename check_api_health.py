#!/usr/bin/env python3
"""
API Health Check Script
Checks the health of all configured APIs and reports their status.
"""
import argparse
import json
import logging
import os
import sys
from datetime import datetime

from utils.api_health_monitor import check_all_apis_now, get_overall_health, check_api_now, get_api_status

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("api_health_check")

def check_all_apis(args):
    """Check the health of all configured APIs"""
    print("🔍 Checking health of all APIs...")
    status = check_all_apis_now()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(status, f, indent=2)
        print(f"✅ Results saved to {args.output}")
    
    print("\n📊 API Health Summary:")
    health = get_overall_health()
    
    print(f"Status: {health['overall_status'].upper()}")
    print(f"Healthy APIs: {health['healthy_apis']}/{health['total_apis']} ({health['healthy_percent']}%)")
    print(f"Message: {health['message']}")
    print(f"Timestamp: {health['timestamp']}")
    
    if args.verbose:
        print("\n📋 Detailed API Status:")
        for api_name, api_status in status.items():
            current = api_status["current"]
            print(f"{api_name}: {current['status'].upper()}")
            if current['status'] == 'down':
                print(f"  Error: {current.get('error', 'Unknown error')}")
            print(f"  Response Code: {current.get('response_code', 'N/A')}")
            print(f"  Response Time: {current.get('response_time', 'N/A')} ms")
            print(f"  Last Checked: {current['timestamp']}")
            print()

def check_specific_api(args):
    """Check the health of a specific API"""
    api_name = args.api
    print(f"🔍 Checking health of {api_name} API...")
    
    try:
        status = check_api_now(api_name)
        print(f"\n📊 {api_name} API Status: {status['status'].upper()}")
        
        if status['status'] == 'down':
            print(f"Error: {status.get('error', 'Unknown error')}")
        
        print(f"Response Code: {status.get('response_code', 'N/A')}")
        print(f"Response Time: {status.get('response_time', 'N/A')} ms")
        print(f"Last Checked: {status['timestamp']}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(status, f, indent=2)
            print(f"✅ Results saved to {args.output}")
            
    except ValueError as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

def show_history(args):
    """Show the history of API health checks"""
    api_name = args.api
    status = get_api_status(api_name if api_name else None)
    
    if api_name:
        print(f"📜 {api_name} API Health History:")
        api_status = status
        if not api_status or not api_status.get("history"):
            print(f"❌ No history available for {api_name} API")
            sys.exit(1)
            
        for i, check in enumerate(api_status["history"]):
            print(f"Check {i+1}:")
            print(f"  Status: {check['status'].upper()}")
            if check['status'] == 'down':
                print(f"  Error: {check.get('error', 'Unknown error')}")
            print(f"  Response Code: {check.get('response_code', 'N/A')}")
            print(f"  Response Time: {check.get('response_time', 'N/A')} ms")
            print(f"  Timestamp: {check['timestamp']}")
            print()
    else:
        print("📜 API Health Check History Summary:")
        for api_name, api_status in status.items():
            print(f"{api_name}:")
            if not api_status or not api_status.get("history"):
                print(f"  No history available")
                continue
                
            # Count statuses
            up_count = sum(1 for check in api_status["history"] if check['status'] == 'up')
            down_count = len(api_status["history"]) - up_count
            
            print(f"  Total Checks: {len(api_status['history'])}")
            print(f"  Up: {up_count}, Down: {down_count}")
            print(f"  Current Status: {api_status['current']['status'].upper()}")
            print()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(status, f, indent=2)
        print(f"✅ Results saved to {args.output}")

def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(description="API Health Check")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Check all APIs
    all_parser = subparsers.add_parser("all", help="Check all APIs")
    all_parser.add_argument("-o", "--output", help="Output file for the results")
    all_parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed output")
    
    # Check specific API
    api_parser = subparsers.add_parser("api", help="Check a specific API")
    api_parser.add_argument("api", help="Name of the API to check")
    api_parser.add_argument("-o", "--output", help="Output file for the results")
    
    # Show history
    history_parser = subparsers.add_parser("history", help="Show API health check history")
    history_parser.add_argument("-a", "--api", help="Name of the API to show history for")
    history_parser.add_argument("-o", "--output", help="Output file for the results")
    
    args = parser.parse_args()
    
    if args.command == "all":
        check_all_apis(args)
    elif args.command == "api":
        check_specific_api(args)
    elif args.command == "history":
        show_history(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()