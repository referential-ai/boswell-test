"""
Model verification functionality.
"""

import concurrent.futures
from typing import List, Dict, Tuple, Any

from botwell.models.api import call_openrouter_api
from botwell.models.config import MODELS


def verify_model(model: Dict[str, str]) -> Tuple[bool, Dict[str, str]]:
    """Verify a single model is available on OpenRouter.
    
    This function is designed to be run concurrently.
    
    Returns:
        Tuple of (success, model) where success is a boolean indicating if model is available
    """
    model_name = model["name"]
    model_id = model["model_id"]
    
    print(f"  Testing model: {model_name}...")
    # Using a minimal prompt just to check if the model is available
    test_prompt = "Hello, please respond with a single word."
    response = call_openrouter_api(model_id, test_prompt)
    
    if "error" in response:
        print(f"  ❌ Model {model_name} ({model_id}) is not available: {response.get('error', {}).get('message', 'Unknown error')}")
        return (False, model)
        
    print(f"  ✅ Model {model_name} verified and available")
    return (True, model)


def verify_available_models() -> List[Dict[str, str]]:
    """Verify which models are available on OpenRouter and return only valid ones.
    Verifies models concurrently to speed up the process.
    
    Returns:
        List of verified model dictionaries
    """
    print("Verifying available models...")
    verified_models = []
    
    # Use ThreadPoolExecutor to verify models concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(10, len(MODELS))) as executor:
        # Submit all verification tasks
        future_to_model = {
            executor.submit(verify_model, model): model["name"]
            for model in MODELS
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_model):
            model_name = future_to_model[future]
            try:
                success, model = future.result()
                if success:
                    verified_models.append(model)
            except Exception as e:
                print(f"  Error verifying model {model_name}: {e}")
    
    if not verified_models:
        raise ValueError("No valid models available on OpenRouter.")
        
    return verified_models