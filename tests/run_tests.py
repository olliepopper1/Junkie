#!/usr/bin/env python3
"""
Trial Junkie Test Suite Runner
Executes all tests in a structured manner with detailed reporting
"""
import os
import sys
import unittest
import time
import argparse
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def discover_and_run_tests(pattern=None, verbosity=2):
    """Discover and run tests matching the pattern"""
    start_time = time.time()
    
    # Create test loader
    loader = unittest.TestLoader()
    
    # Discover tests in the current directory
    if pattern:
        print(f"{Fore.CYAN}Running tests matching pattern: {pattern}{Style.RESET_ALL}")
        tests = loader.discover(os.path.dirname(__file__), pattern=f"*{pattern}*.py")
    else:
        print(f"{Fore.CYAN}Running all tests{Style.RESET_ALL}")
        tests = loader.discover(os.path.dirname(__file__))
    
    # Create test runner
    runner = unittest.TextTestRunner(verbosity=verbosity)
    
    # Run tests
    result = runner.run(tests)
    
    # Calculate time taken
    elapsed_time = time.time() - start_time
    
    # Print summary
    print(f"\n{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Test Summary:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
    
    if result.wasSuccessful():
        print(f"{Fore.GREEN}All tests passed! ({result.testsRun} tests){Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Tests failed: {len(result.failures)} failures, {len(result.errors)} errors{Style.RESET_ALL}")
        
    print(f"{Fore.CYAN}Time taken: {elapsed_time:.2f} seconds{Style.RESET_ALL}")
    
    return result.wasSuccessful()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Run Trial Junkie test suite")
    parser.add_argument("-p", "--pattern", help="Pattern to match test files (e.g. 'database' for test_database.py)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase verbosity")
    args = parser.parse_args()
    
    # Print header
    print(f"\n{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Trial Junkie Test Suite{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
    
    verbosity = 3 if args.verbose else 2
    success = discover_and_run_tests(args.pattern, verbosity)
    
    # Return appropriate exit code
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())