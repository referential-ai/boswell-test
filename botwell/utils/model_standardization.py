"""
Model Name Standardization Utility

This module provides functions to ensure consistent model naming throughout the system.
All model names should pass through these standardization functions before being used
in results, reports, or visualizations.
"""

import re
from typing import Dict, Optional, List

# Define mapping of variant names to standard names
MODEL_NAME_MAPPING = {
    # OpenAI Models
    "GPT4o": "GPT-4o",
    "GPT4-o": "GPT-4o",
    "GPT-4-o": "GPT-4o",
    "GPT4o-mini": "GPT-4o-mini",
    "GPT-4-o-mini": "GPT-4o-mini",
    "GPT4-o-mini": "GPT-4o-mini",
    "GPT-4o mini": "GPT-4o-mini",
    "GPT-3.5 Turbo": "GPT-3.5-Turbo",
    
    # Anthropic Models
    "Claude 3 Opus": "Claude-3-Opus",
    "Claude-3 Opus": "Claude-3-Opus",
    "Claude 3-Opus": "Claude-3-Opus",
    "Claude 3 Sonnet": "Claude-3-Sonnet",
    "Claude-3 Sonnet": "Claude-3-Sonnet",
    "Claude 3-Sonnet": "Claude-3-Sonnet",
    "Claude 3.7 Sonnet": "Claude-3.7-Sonnet",
    "Claude-3.7 Sonnet": "Claude-3.7-Sonnet",
    "Claude 3.7-Sonnet": "Claude-3.7-Sonnet",
    "Claude-3.7-Sonnet thinking": "Claude-3.7-Sonnet-thinking",
    "Claude thinking": "Claude-3.7-Sonnet-thinking",
    "Claude-3.7 thinking": "Claude-3.7-Sonnet-thinking",
    
    # Perplexity Models (the most problematic)
    "Perplexity-Llama": "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity Llama": "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity": "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity-70B": "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity 70B": "Perplexity: Llama 3.1 Sonar 70B",
    "Sonar 70B": "Perplexity: Llama 3.1 Sonar 70B",
    "Llama Sonar": "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity-Llama 3.1 Sonar 70B": "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity-8B": "Perplexity: Llama 3.1 Sonar 8B Online",
    "Perplexity 8B": "Perplexity: Llama 3.1 Sonar 8B Online",
    "Perplexity-Llama 3.1 Sonar 8B": "Perplexity: Llama 3.1 Sonar 8B Online",
    "Perplexity: Llama 3.1 Sonar 8B": "Perplexity: Llama 3.1 Sonar 8B Online",
    "Perplexity: Llama 3.1 Sonar 405B Online": "Perplexity: Llama 3.1 Sonar 70B",  # Fix typo
    
    # Meta Models
    "Llama 3 8B": "Llama-3-8B",
    "Llama3-8B": "Llama-3-8B",
    "Llama-3 8B": "Llama-3-8B",
    "Llama 3-8B": "Llama-3-8B",
    
    # Google Models
    "Gemini Flash 2": "Gemini Flash 2.0",
    "Gemini-Flash-2.0": "Gemini Flash 2.0",
    "Gemini-Flash 2.0": "Gemini Flash 2.0",
    "Gemini Pro 1.5": "Gemini Pro 1.5",
    "Gemini-Pro-1.5": "Gemini Pro 1.5",
    "Gemini-Pro 1.5": "Gemini Pro 1.5",
    
    # DeepSeek Models
    "DeepSeek R1 Full": "DeepSeek-R1-Full",
    "DeepSeek-R1 Full": "DeepSeek-R1-Full",
    "DeepSeek R1-Full": "DeepSeek-R1-Full",
    "DeepSeek Distill Qwen 32b": "DeepSeek-Distill-Qwen-32b",
    "DeepSeek-Distill Qwen 32b": "DeepSeek-Distill-Qwen-32b",
    "DeepSeek Distill-Qwen 32b": "DeepSeek-Distill-Qwen-32b",
    "DeepSeek-Distill Qwen-32b": "DeepSeek-Distill-Qwen-32b",
    "DeepSeek Distill Qwen-32b": "DeepSeek-Distill-Qwen-32b",
    
    # Qwen Models
    "Qwen Max": "Qwen-Max",
    "Qwen Plus": "Qwen-Plus",
    "Qwen Turbo": "Qwen-Turbo",
    
    # Anthropic o Models
    "o1 mini": "o1-mini",
    "o3 mini high": "o3-mini-high",
    "o3 mini-high": "o3-mini-high",
    "o3-mini high": "o3-mini-high",
    
    # Misc Models
    "grok beta": "grok-beta",
    "grok2 1212": "grok2-1212"
}

# Standard names for all models - these are the "official" names
STANDARD_MODEL_NAMES = {
    # OpenAI Models
    "GPT-4o",
    "GPT-4o-mini",
    "GPT-3.5-Turbo",
    
    # Anthropic Models
    "Claude-3-Opus",
    "Claude-3-Sonnet",
    "Claude-3.7-Sonnet",
    "Claude-3.7-Sonnet-thinking",
    
    # Perplexity Models
    "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity: Llama 3.1 Sonar 8B Online",
    
    # Meta Models
    "Llama-3-8B",
    
    # Google Models
    "Gemini Flash 2.0",
    "Gemini Pro 1.5",
    
    # DeepSeek Models
    "DeepSeek-R1-Full",
    "DeepSeek-Distill-Qwen-32b",
    
    # Qwen Models
    "Qwen-Max",
    "Qwen-Plus", 
    "Qwen-Turbo",
    
    # Anthropic o Models
    "o1",
    "o1-mini",
    "o3-mini-high",
    
    # Misc Models
    "grok-beta",
    "grok2-1212"
}

def standardize_model_name(model_name: str) -> str:
    """
    Standardize a model name to ensure consistency throughout the system.
    
    Args:
        model_name: The model name to standardize
        
    Returns:
        The standardized model name
    """
    # Check if it's already a standard name
    if model_name in STANDARD_MODEL_NAMES:
        return model_name
        
    # Check if it's in our direct mapping
    if model_name in MODEL_NAME_MAPPING:
        return MODEL_NAME_MAPPING[model_name]
    
    # Apply heuristic rules for cases not explicitly mapped
    
    # Check for Perplexity without full name
    if re.match(r"perplexity\s*[-:]\s*.+70b", model_name, re.IGNORECASE):
        return "Perplexity: Llama 3.1 Sonar 70B"
    
    if re.match(r"perplexity\s*[-:]\s*.+8b", model_name, re.IGNORECASE):
        if "online" in model_name.lower():
            return "Perplexity: Llama 3.1 Sonar 8B Online"
        return "Perplexity: Llama 3.1 Sonar 8B Online"
    
    # Check for Claude models
    if "claude" in model_name.lower():
        if "3.7" in model_name and "thinking" in model_name.lower():
            return "Claude-3.7-Sonnet-thinking"
        elif "3.7" in model_name:
            return "Claude-3.7-Sonnet"
        elif "opus" in model_name.lower():
            return "Claude-3-Opus"
        elif "sonnet" in model_name.lower():
            return "Claude-3-Sonnet"
    
    # Check for GPT models
    if re.match(r"gpt.*4.*o.*mini", model_name, re.IGNORECASE):
        return "GPT-4o-mini"
    elif re.match(r"gpt.*4.*o", model_name, re.IGNORECASE):
        return "GPT-4o"
    elif re.match(r"gpt.*3\.5.*turbo", model_name, re.IGNORECASE):
        return "GPT-3.5-Turbo"
    
    # As a fallback, return the original name if we couldn't standardize it
    print(f"Warning: Could not standardize model name: {model_name}")
    return model_name

def standardize_model_names_in_dict(data: Dict, key_path: Optional[List[str]] = None) -> Dict:
    """
    Recursively standardize all model names in a dictionary.
    
    Args:
        data: The dictionary to process
        key_path: Internal parameter for tracking the current path in the dictionary
        
    Returns:
        A new dictionary with standardized model names
    """
    if key_path is None:
        key_path = []
    
    result = {}
    
    for key, value in data.items():
        current_path = key_path + [key]
        
        # If this is a model name at the top level or in a known location
        if (len(key_path) == 0 and isinstance(key, str) and 
            any(model_fragment in key for model_fragment in ["GPT", "Claude", "Llama", "Perplexity", "Gemini", "DeepSeek", "Qwen", "grok"])):
            standardized_key = standardize_model_name(key)
            
            # Skip if the model name is a key and it's been standardized to something else
            # that already exists (prevents duplicates)
            if standardized_key != key and standardized_key in data:
                continue
                
            # Use the standardized key
            result[standardized_key] = value
        else:
            # Keep the original key
            result[key] = value
        
        # Recursively process dictionaries
        if isinstance(value, dict):
            result[key] = standardize_model_names_in_dict(value, current_path)
        # Process lists of dictionaries    
        elif isinstance(value, list) and all(isinstance(item, dict) for item in value):
            result[key] = [standardize_model_names_in_dict(item, current_path + ["[]"]) for item in value]
    
    return result

def standardize_model_names_in_list(models: List[str]) -> List[str]:
    """
    Standardize all model names in a list.
    
    Args:
        models: List of model names
        
    Returns:
        A new list with standardized model names
    """
    return [standardize_model_name(model) for model in models]