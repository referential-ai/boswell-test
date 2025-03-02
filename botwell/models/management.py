"""
Model management functionality for updating available models.
"""

import time
import json

from botwell.models.api import fetch_available_openrouter_models


def update_models_file(output_file: str = "openrouter_models.json") -> None:
    """Update the local models file with the latest available models from OpenRouter."""
    models = fetch_available_openrouter_models()
    
    if not models:
        print("No models fetched. Check your API key and connection.")
        return
    
    # Save the models to a JSON file
    try:
        with open(output_file, 'w') as f:
            json.dump({
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "models": models
            }, f, indent=2)
        
        print(f"Successfully updated models file: {output_file}")
        print(f"Found {len(models)} available models")
        
        # Print a sample of model IDs for convenience
        print("\nSample model IDs for use in botwell.models.config:")
        for i, model in enumerate(models[:10]):  # Show first 10 models
            print(f"  {model['name']}: \"{model['model_id']}\"")
        
        if len(models) > 10:
            print(f"  ... and {len(models) - 10} more (see {output_file} for complete list)")
            
    except Exception as e:
        print(f"Error saving models file: {e}")