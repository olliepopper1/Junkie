#!/usr/bin/env python3
"""
Test Web Scraper Integration

This script tests the integration with the ScrapeNinja API for web scraping
"""
import os
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_web_scraper")

def test_scrape_ninja_integration():
    """Test the ScrapeNinja API integration"""
    logger.info("Testing ScrapeNinja API integration")
    
    try:
        # Import the APIIntegrations class
        from api_integrations import APIIntegrations
        
        # Test URLs
        test_urls = [
            "https://www.hulu.com/welcome",
            "https://www.netflix.com/",
            "https://www.disneyplus.com/"
        ]
        
        results = {}
        
        for url in test_urls:
            logger.info(f"Testing web scraping for URL: {url}")
            
            # Test without JavaScript rendering
            logger.info("Scraping without JavaScript rendering...")
            result_no_js = APIIntegrations.web_scrape(url, timeout=30, render_js=False)
            
            # Check if the scrape was successful
            success_no_js = "error" not in result_no_js
            status_code_no_js = result_no_js.get("status_code", 0)
            method_no_js = result_no_js.get("method", "unknown")
            
            logger.info(f"Scrape result without JS: Success={success_no_js}, Status Code={status_code_no_js}, Method={method_no_js}")
            
            # Test with JavaScript rendering if API key is available
            if os.getenv("SCRAPE_NINJA_API_KEY"):
                logger.info("Scraping with JavaScript rendering...")
                result_with_js = APIIntegrations.web_scrape(url, timeout=45, render_js=True)
                
                # Check if the scrape was successful
                success_with_js = "error" not in result_with_js
                status_code_with_js = result_with_js.get("status_code", 0)
                method_with_js = result_with_js.get("method", "unknown")
                
                logger.info(f"Scrape result with JS: Success={success_with_js}, Status Code={status_code_with_js}, Method={method_with_js}")
                
                # Store the results
                results[url] = {
                    "without_js": {
                        "success": success_no_js,
                        "status_code": status_code_no_js,
                        "method": method_no_js,
                        "content_length": len(result_no_js.get("content", ""))
                    },
                    "with_js": {
                        "success": success_with_js,
                        "status_code": status_code_with_js,
                        "method": method_with_js,
                        "content_length": len(result_with_js.get("content", ""))
                    }
                }
            else:
                # Store only the no-JS results if API key is not available
                results[url] = {
                    "without_js": {
                        "success": success_no_js,
                        "status_code": status_code_no_js,
                        "method": method_no_js,
                        "content_length": len(result_no_js.get("content", ""))
                    },
                    "with_js": "skipped - API key not available"
                }
            
            logger.info(f"Testing complete for URL: {url}")
            logger.info("-" * 50)
        
        return results
        
    except ImportError:
        logger.error("APIIntegrations class not found")
        return {"error": "APIIntegrations class not found"}
    except Exception as e:
        logger.error(f"Error testing web scraper: {e}")
        return {"error": str(e)}

def main():
    """Run the web scraper tests"""
    logger.info("Starting web scraper tests")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    results = test_scrape_ninja_integration()
    
    # Print summary
    logger.info("=== Test Results ===")
    if isinstance(results, dict) and "error" not in results:
        for url, result in results.items():
            logger.info(f"URL: {url}")
            
            # No-JS results
            no_js = result.get("without_js", {})
            if isinstance(no_js, dict):
                logger.info(f"  Without JS: Success={no_js.get('success', False)}, Method={no_js.get('method', 'unknown')}")
            else:
                logger.info(f"  Without JS: {no_js}")
            
            # With-JS results
            with_js = result.get("with_js", {})
            if isinstance(with_js, dict):
                logger.info(f"  With JS: Success={with_js.get('success', False)}, Method={with_js.get('method', 'unknown')}")
            else:
                logger.info(f"  With JS: {with_js}")
    else:
        error = results.get("error", "Unknown error")
        logger.error(f"Tests failed: {error}")
    
    # Save results to file
    with open(f"web_scraper_test_results_{timestamp}.json", "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Results saved to web_scraper_test_results_{timestamp}.json")

if __name__ == "__main__":
    main()