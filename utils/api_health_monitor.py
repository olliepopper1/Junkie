"""
API Health Monitor
Monitors the health and availability of external APIs used by the application
"""
import json
import logging
import requests
import threading
import time
from datetime import datetime, timedelta
import os
from pathlib import Path

# Import the API configuration to monitor
from api_integrations import API_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_health_monitor")

class APIHealthMonitor:
    """
    Monitors the health and availability of external APIs
    Provides insights into API performance and reliability
    """
    def __init__(self, check_interval=3600, results_path="./api_health_status.json"):
        """Initialize the API health monitor"""
        self.check_interval = check_interval  # How often to check APIs (in seconds)
        self.results_path = results_path
        self.apis = API_CONFIG
        self.status = {}
        self.running = False
        self.thread = None
        
        # Load previous results if they exist
        self._load_results()
    
    def _load_results(self):
        """Load previous API health check results"""
        try:
            if os.path.exists(self.results_path):
                with open(self.results_path, "r") as f:
                    self.status = json.load(f)
                logger.info(f"Loaded existing API health data from {self.results_path}")
            else:
                logger.info("No existing API health data found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading API health data: {e}")
            self.status = {}
    
    def _save_results(self):
        """Save API health check results"""
        try:
            # Ensure directory exists
            Path(os.path.dirname(self.results_path)).mkdir(parents=True, exist_ok=True)
            
            with open(self.results_path, "w") as f:
                json.dump(self.status, f, indent=2)
            logger.info(f"Saved API health data to {self.results_path}")
        except Exception as e:
            logger.error(f"Error saving API health data: {e}")
    
    def check_api(self, api_name):
        """
        Check if an API is functioning properly
        
        Args:
            api_name (str): The name of the API to check
            
        Returns:
            dict: API health status information
        """
        if api_name not in self.apis:
            return {
                "status": "unknown",
                "error": "API not configured",
                "timestamp": datetime.now().isoformat()
            }
        
        api_info = self.apis[api_name]
        url = api_info["endpoint"]
        
        try:
            # Create a test request to check if the API is alive
            headers = {
                'Content-Type': 'application/json',
            }
            
            # Different auth methods based on API
            if api_name.startswith("personator"):
                headers['Authorization'] = f'Bearer {api_info["key"]}'
            elif api_name.startswith("virtual_number"):
                headers['api-key'] = api_info["key"]
            elif api_name.startswith("fake_card") or api_name.startswith("virtual_card"):
                headers['Authorization'] = f'Bearer {api_info["key"]}'
            elif api_name.startswith("temp_mail_backup"):
                headers['Authorization'] = f'Bearer {api_info["key"]}'
            elif api_name.startswith("temp_email"):
                headers['X-API-Key'] = api_info["key"]
            else:
                # Default RapidAPI style
                headers['X-RapidAPI-Key'] = api_info["key"]
                headers['X-RapidAPI-Host'] = api_info["host"]
            
            # Just do a HEAD request to check if the API is responsive
            # This avoids unnecessary data transfer and potential side effects
            start_time = time.time()
            response = requests.head(url, headers=headers, timeout=5)
            response_time = time.time() - start_time
            
            status = {
                "status": "up" if response.status_code < 400 else "down",
                "response_code": response.status_code,
                "response_time": round(response_time * 1000, 2),  # ms
                "timestamp": datetime.now().isoformat()
            }
            
            if response.status_code >= 400:
                status["error"] = f"API returned status code {response.status_code}"
            
            return status
            
        except requests.exceptions.Timeout:
            return {
                "status": "down",
                "error": "API request timed out",
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "down",
                "error": "Connection error",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "down",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_all_apis(self):
        """Check the health of all configured APIs"""
        for api_name in self.apis:
            logger.info(f"Checking health of {api_name} API...")
            status = self.check_api(api_name)
            
            if not api_name in self.status:
                self.status[api_name] = {
                    "current": status,
                    "history": [status]
                }
            else:
                # Update current status
                self.status[api_name]["current"] = status
                
                # Add to history, keeping the last 10 entries
                self.status[api_name]["history"].append(status)
                if len(self.status[api_name]["history"]) > 10:
                    self.status[api_name]["history"] = self.status[api_name]["history"][-10:]
            
            logger.info(f"API {api_name} status: {status['status']}")
        
        # Save results after checking all APIs
        self._save_results()
        
        return self.status
    
    def start_monitoring(self):
        """Start the API health monitoring thread"""
        if self.running:
            logger.warning("API health monitoring already running")
            return
        
        self.running = True
        
        def monitor_thread():
            while self.running:
                logger.info("Running API health check...")
                self.check_all_apis()
                time.sleep(self.check_interval)
        
        self.thread = threading.Thread(target=monitor_thread)
        self.thread.daemon = True
        self.thread.start()
        logger.info(f"API health monitoring started (interval: {self.check_interval}s)")
    
    def stop_monitoring(self):
        """Stop the API health monitoring thread"""
        if not self.running:
            logger.warning("API health monitoring not running")
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        logger.info("API health monitoring stopped")
    
    def get_api_status(self, api_name=None):
        """
        Get the status of an API or all APIs
        
        Args:
            api_name (str, optional): The name of the API to get status for
            
        Returns:
            dict: API health status information
        """
        if api_name:
            return self.status.get(api_name, {
                "current": {
                    "status": "unknown",
                    "error": "API not monitored",
                    "timestamp": datetime.now().isoformat()
                },
                "history": []
            })
        
        return self.status
    
    def get_overall_health(self):
        """
        Get an overall health summary for all APIs
        
        Returns:
            dict: Overall API health information
        """
        all_apis = len(self.apis)
        if all_apis == 0:
            return {
                "overall_status": "unknown",
                "healthy_percent": 0,
                "message": "No APIs configured for monitoring",
                "timestamp": datetime.now().isoformat()
            }
        
        healthy_apis = sum(1 for api in self.status.values() if api["current"]["status"] == "up")
        healthy_percent = round((healthy_apis / all_apis) * 100, 1)
        
        if healthy_percent == 100:
            overall_status = "healthy"
            message = "All APIs are functioning properly"
        elif healthy_percent >= 75:
            overall_status = "degraded"
            message = "Some APIs are experiencing issues"
        elif healthy_percent >= 25:
            overall_status = "poor"
            message = "Multiple APIs are down or experiencing issues"
        else:
            overall_status = "critical"
            message = "Most or all APIs are down"
        
        return {
            "overall_status": overall_status,
            "healthy_percent": healthy_percent,
            "healthy_apis": healthy_apis,
            "total_apis": all_apis,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

# Singleton instance for application-wide use
monitor = APIHealthMonitor()

def get_monitor():
    """Get the API health monitor singleton instance"""
    return monitor

def start_monitoring():
    """Start the API health monitoring thread"""
    monitor.start_monitoring()

def stop_monitoring():
    """Stop the API health monitoring thread"""
    monitor.stop_monitoring()

def get_api_status(api_name=None):
    """Get the status of an API or all APIs"""
    return monitor.get_api_status(api_name)

def get_overall_health():
    """Get an overall health summary for all APIs"""
    return monitor.get_overall_health()

def check_api_now(api_name):
    """Check an API's health immediately"""
    return monitor.check_api(api_name)

def check_all_apis_now():
    """Check the health of all APIs immediately"""
    return monitor.check_all_apis()

# For command-line usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="API Health Monitor")
    parser.add_argument("--check", action="store_true", help="Check all APIs immediately")
    parser.add_argument("--api", type=str, help="Check a specific API by name")
    parser.add_argument("--start", action="store_true", help="Start continuous monitoring")
    parser.add_argument("--interval", type=int, default=3600, help="Monitoring interval in seconds")
    
    args = parser.parse_args()
    
    if args.interval:
        monitor.check_interval = args.interval
    
    if args.api:
        status = monitor.check_api(args.api)
        print(f"API {args.api} status: {json.dumps(status, indent=2)}")
    elif args.check:
        status = monitor.check_all_apis()
        print(f"All APIs status: {json.dumps(status, indent=2)}")
    elif args.start:
        monitor.start_monitoring()
        print(f"API monitoring started with interval {monitor.check_interval}s")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()
            print("API monitoring stopped")
    else:
        parser.print_help()