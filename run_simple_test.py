#!/usr/bin/env python3
"""
Simple test script to ensure the modular botwell is working correctly.
"""

import os
import sys
from botwell.models.config import FREE_MODELS
from botwell.domains import AVAILABLE_DOMAINS
from botwell.core.test import run_boswell_test
from botwell.reporting.summary import print_summary

def main():
    """Run a simple test of the botwell framework."""
    # Verify API key is set
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY environment variable is not set.")
        print("Please set it with: export OPENROUTER_API_KEY='your-api-key'")
        sys.exit(1)
    
    # Run with minimal parameters - just free models and a single domain
    print("Running simple Boswell test with free models...")
    
    # Use a small subset of models for a faster test
    subset_models = FREE_MODELS[:3]  # Just use first 3 free models
    domain = list(AVAILABLE_DOMAINS.keys())[0]  # First domain
    
    # Run the test
    results = run_boswell_test(
        domain_name=domain,
        output_file="simple_test_results.json",
        selected_models=subset_models,
        skip_verification=False,
        max_retries=2,
        is_free_run=True
    )
    
    # Print summary
    print_summary(results)
    
    print(f"\nSimple test completed!")
    print(f"  - Full results directory: {results['results_dir']}")

if __name__ == "__main__":
    main()