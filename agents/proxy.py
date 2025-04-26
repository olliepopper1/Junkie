"""
Proxy rotation module
Provides proxy management for API requests
"""
import os
import random
import logging
from config import PROXY_ENABLED

logger = logging.getLogger(__name__)

# Sample proxy list - in a real implementation, this would be loaded from
# a file, database, or API service (e.g., proxy provider API)
PROXIES = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080",
    "http://proxy4.example.com:8080",
    "http://proxy5.example.com:8080"
]

# Alternative: environment variable with comma-separated proxy list
if os.getenv("PROXY_LIST"):
    env_proxies = os.getenv("PROXY_LIST").split(",")
    if env_proxies:
        PROXIES = [proxy.strip() for proxy in env_proxies]

def get_proxy():
    """Get a random proxy from the proxy list"""
    if not PROXY_ENABLED or not PROXIES:
        return None
    
    proxy = random.choice(PROXIES)
    logger.debug(f"Selected proxy: {proxy}")
    return proxy

def get_all_proxies():
    """Get all available proxies"""
    if not PROXY_ENABLED:
        return []
    
    return PROXIES

class ProxyRotator:
    """Class for rotating proxies during requests"""
    
    def __init__(self):
        self.proxies = PROXIES.copy() if PROXIES else []
        self.current_index = 0
        self.enabled = PROXY_ENABLED
    
    def get_next_proxy(self):
        """Get the next proxy in the rotation"""
        if not self.enabled or not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def mark_proxy_failed(self, proxy):
        """Mark a proxy as failed (e.g., if it returns an error)"""
        if proxy in self.proxies:
            logger.warning(f"Marking proxy as failed: {proxy}")
            self.proxies.remove(proxy)
            
            if not self.proxies:
                logger.error("No more proxies available")
                self.enabled = False
