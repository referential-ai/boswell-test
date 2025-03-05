#!/usr/bin/env python3
"""
List available resources (models and domains) in the Botwell framework.
"""

from botwell.models.config import MODELS, FREE_MODELS, PREMIUM_MODELS
from botwell.domains import AVAILABLE_DOMAINS

def main():
    """Display available models and domains."""
    # List domains
    print("\nAvailable domains:")
    print("-" * 60)
    for domain_id, description in AVAILABLE_DOMAINS.items():
        print(f"{domain_id:<15} | {description}")
    
    # List models
    print("\nAvailable models:")
    print("-" * 60)
    
    # Count free and premium models
    free_count = len(FREE_MODELS)
    premium_count = len(PREMIUM_MODELS)
    total_count = len(MODELS)
    
    # Print model details
    for model in MODELS:
        model_type = " (premium)" if model['name'] in PREMIUM_MODELS else " (free)"
        print(f"{model['name']:<30} | {model['model_id']}{model_type}")
    
    # Print summary
    print(f"\nTotal: {total_count} models ({free_count} free, {premium_count} premium)")
    
    # Provide usage information
    print("\nUsage information:")
    print("  - Run full tests: python -m botwell")
    print("  - List help options: python -m botwell --help")
    print("  - Run with free models only: python -m botwell --free")
    print("  - Run specific domain: python -m botwell --domain comp_sci_1")

if __name__ == "__main__":
    main()