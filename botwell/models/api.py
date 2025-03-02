"""
API interaction for model requests and responses.
"""

import time
import requests
from typing import Dict, Any, List
import concurrent.futures
import os

from botwell.models.config import MODELS
from botwell.utils.tokenization import calculate_tokens


from botwell.utils.caching import cached_api_call

@cached_api_call
def call_openrouter_api(model_id: str, prompt: str, disable_cache: bool = False) -> Dict[str, Any]:
    """Call OpenRouter API with the specified model and prompt.
    
    Args:
        model_id: The model identifier string
        prompt: The prompt text to send to the model
        disable_cache: If True, bypass the cache and make a fresh API call
        
    Returns:
        JSON response with added cost information
    """
    API_KEY = os.environ.get("OPENROUTER_API_KEY")
    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
        
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/alanwilhelm/botwell",  # Update with actual repo
        "X-Title": "Boswell Test"
    }
    
    data = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    start_time = time.time()
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )
    end_time = time.time()
    
    if response.status_code != 200:
        print(f"Error calling API: {response.status_code}")
        print(response.text)
        return {"error": response.text, "cost": 0.0, "duration": 0.0}
    
    result = response.json()
    
    # Calculate token counts if not provided
    if "usage" not in result:
        prompt_tokens = calculate_tokens(prompt)
        completion_tokens = 0
        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0].get("message", {})
            completion_text = message.get("content", "")
            completion_tokens = calculate_tokens(completion_text)
        
        result["usage"] = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens
        }
    
    # Estimate cost (not all models provide accurate pricing info)
    # These are rough estimates, actual pricing varies by model
    input_cost_per_thousand = 0.0005  # $0.0005 per 1K input tokens (conservative)
    output_cost_per_thousand = 0.0015  # $0.0015 per 1K output tokens (conservative)
    
    # Try to get model-specific pricing from the response
    model_info = result.get("model", {})
    if isinstance(model_info, dict):
        pricing = model_info.get("pricing", {})
        if pricing:
            input_cost_per_thousand = pricing.get("input", input_cost_per_thousand)
            output_cost_per_thousand = pricing.get("output", output_cost_per_thousand)
    
    input_cost = (result["usage"]["prompt_tokens"] / 1000) * input_cost_per_thousand
    output_cost = (result["usage"]["completion_tokens"] / 1000) * output_cost_per_thousand
    total_cost = input_cost + output_cost
    
    # Add cost and duration information to the result
    result["cost_info"] = {
        "input_tokens": result["usage"]["prompt_tokens"],
        "output_tokens": result["usage"]["completion_tokens"],
        "input_cost": input_cost,
        "output_cost": output_cost, 
        "total_cost": total_cost,
        "duration": end_time - start_time
    }
    
    return result


def fetch_available_openrouter_models() -> List[Dict[str, Any]]:
    """Fetch the list of available models from OpenRouter."""
    API_KEY = os.environ.get("OPENROUTER_API_KEY")
    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
        
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("Fetching available models from OpenRouter...")
    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Error fetching models: {response.status_code}")
            print(response.text)
            return []
        
        models_data = response.json()
        # Process and format the models using a thread pool for faster processing
        formatted_models = []
        model_data_list = models_data.get("data", [])
        
        # Define a function to process each model
        def process_model(model_data):
            model_id = model_data.get("id")
            if not model_id:
                return None
                
            model_name = model_data.get("name", model_id.split("/")[-1])
            return {
                "name": model_name,
                "model_id": model_id,
                "context_length": model_data.get("context_length"),
                "pricing": model_data.get("pricing", {}),
                "description": model_data.get("description", "")
            }
            
        # Process models concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for model in executor.map(process_model, model_data_list):
                if model:
                    formatted_models.append(model)
        
        return formatted_models
        
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []