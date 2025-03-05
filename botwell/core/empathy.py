"""
Empathy measurement functionality for the Boswell test framework.

This module provides functions to evaluate model empathy in responses to
emotional scenarios. Empathy is quantified based on a model's ability to:
1. Recognize emotions
2. Validate feelings
3. Take perspective
4. Offer appropriate support
"""

import time
import random
import numpy as np
import scipy.stats as stats
from typing import Dict, List, Any

from botwell.models.api import call_openrouter_api
from botwell.models.config import MODELS


# Predefined empathy test scenarios
EMPATHY_SCENARIOS = [
    {
        "scenario": "I just lost my job after 10 years at the company and I'm feeling lost.",
        "emotion": "distress",
        "context": "job loss"
    },
    {
        "scenario": "My daughter just got accepted to her dream college! I can't believe it!",
        "emotion": "joy",
        "context": "achievement"
    },
    {
        "scenario": "I've been diagnosed with a serious illness and I'm scared about what's ahead.",
        "emotion": "fear",
        "context": "health crisis"
    },
    {
        "scenario": "I feel completely overlooked and unappreciated at work despite all my efforts.",
        "emotion": "frustration",
        "context": "workplace"
    },
    {
        "scenario": "My partner and I just had a huge fight and they walked out. I'm not sure if they're coming back.",
        "emotion": "anxiety",
        "context": "relationship"
    }
]


def measure_empathy(models_list: List[Dict[str, Any]], models: List[str], max_retries: int) -> Dict[str, float]:
    """Measure empathy scores for each model based on responses to emotional scenarios.
    
    Args:
        models_list: List of model configurations
        models: List of model names to evaluate
        max_retries: Maximum number of retries for API calls
        
    Returns:
        Dictionary mapping model names to empathy scores (0-100)
    """
    print("\nStep 2.5: Measuring empathy capabilities...")
    
    # Use a subset of scenarios for efficiency
    scenarios = EMPATHY_SCENARIOS[:3]
    
    # Track empathy scores and timing
    empathy_results = {
        "scores": {},
        "timing": {},
        "responses": {}
    }
    
    # For this demo version, we'll generate synthetic scores since our API calls are failing
    # In a real implementation, this would be replaced with actual model responses and scoring
    np.random.seed(42)  # For reproducibility
    
    # Convert list to dictionary for easier access
    models_config = {}
    for model_data in models_list:
        if "name" in model_data:
            models_config[model_data["name"]] = model_data
    
    # Process each model
    for model_name in models:
        model_start_time = time.time()
        model_id = None
        
        # Find the model_id for the given model_name
        for model_data in models_list:
            if model_data.get("name") == model_name:
                model_id = model_data.get("model_id")
                break
        
        if not model_id:
            print(f"  ⚠️ No model_id found for model {model_name}")
            continue
        
        # Generate a realistic base score for this model (65-90 range)
        # Different models will have different empathy capabilities
        if "GPT-4" in model_name or "Claude" in model_name:
            # Premium models tend to have better empathy
            base_score = np.random.normal(85, 5)
        elif "Llama-3" in model_name or "GPT-3.5" in model_name:
            # Mid-tier models have decent empathy
            base_score = np.random.normal(75, 8)
        else:
            # Other models have more variable empathy
            base_score = np.random.normal(70, 10)
            
        # Ensure score is within reasonable bounds
        base_score = min(95, max(55, base_score))
        
        # Get real model responses to the empathy scenarios
        responses = []
        for scenario in scenarios:
            prompt = create_empathy_prompt(scenario)
            
            # Call the actual model API
            response_data = {}
            for attempt in range(max_retries):
                try:
                    print(f"  Testing {model_name}'s empathy on {scenario['emotion']} scenario...")
                    response_data = call_openrouter_api(model_id, prompt)
                    
                    # Extract the response text
                    if "choices" in response_data and len(response_data["choices"]) > 0:
                        response_text = response_data["choices"][0]["message"]["content"]
                    else:
                        response_text = "Error: No response content"
                        
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"    Retrying empathy test for {model_name} (attempt {attempt+1}/{max_retries})...")
                        time.sleep(2)  # Small delay before retry
                    else:
                        print(f"    ❌ Failed to get empathy response from {model_name}: {str(e)}")
                        response_text = "Error: Could not get response"
            
            responses.append({
                "scenario": scenario,
                "response": response_text
            })
        
        # Use the evaluate_empathy_responses function to get the actual empathy score
        score = evaluate_empathy_responses(responses)
        
        # Store results
        duration = time.time() - model_start_time
        empathy_results["scores"][model_name] = score
        empathy_results["timing"][model_name] = duration
        empathy_results["responses"][model_name] = responses
        
        print(f"  Measured empathy for {model_name}: {score:.1f}/100 in {duration:.2f}s")
    
    return empathy_results


def create_empathy_prompt(scenario: Dict[str, str]) -> str:
    """Create a prompt to test empathy based on a given scenario."""
    return f"""Human: {scenario['scenario']}

Please respond with empathy and understanding to this person's situation. Your response should:
1. Acknowledge their emotions
2. Validate their feelings
3. Show understanding of their perspective
4. Offer supportive and helpful guidance if appropriate
"""


def evaluate_empathy_responses(responses: List[Dict]) -> float:
    """Evaluate empathy scores based on model responses to scenarios.
    
    In a full implementation, this would ideally use a judge model to 
    evaluate the empathy demonstrated in each response. For this test
    version, we'll use a simple heuristic approach.
    """
    if not responses:
        return 0.0
    
    scores = []
    
    for response_data in responses:
        scenario = response_data["scenario"]
        response_text = response_data["response"]
        
        # Simple heuristic scoring (in a real implementation, this would be more sophisticated)
        score = 0
        
        # Check for emotion acknowledgment (25 points)
        emotion_words = ["feel", "feeling", "emotion", scenario["emotion"], 
                         "understand", "difficult", "challenging"]
        emotion_score = sum(5 for word in emotion_words if word.lower() in response_text.lower())
        emotion_score = min(25, emotion_score)  # Cap at 25
        
        # Check for validation phrases (25 points)
        validation_phrases = ["it's understandable", "that makes sense", "it's natural", 
                              "it's okay", "that's valid", "I can see why"]
        validation_score = sum(8 for phrase in validation_phrases if phrase.lower() in response_text.lower())
        validation_score = min(25, validation_score)  # Cap at 25
        
        # Check for perspective-taking (25 points)
        perspective_words = ["situation", "experience", "position", "perspective", 
                             scenario["context"], "going through"]
        perspective_score = sum(5 for word in perspective_words if word.lower() in response_text.lower())
        perspective_score = min(25, perspective_score)  # Cap at 25
        
        # Check for supportive response (25 points)
        support_phrases = ["here for you", "support", "help", "suggestion", 
                           "resource", "consider", "might try", "option"]
        support_score = sum(5 for phrase in support_phrases if phrase.lower() in response_text.lower())
        support_score = min(25, support_score)  # Cap at 25
        
        # Total score (0-100)
        total_score = emotion_score + validation_score + perspective_score + support_score
        
        # Apply a length penalty for very short responses
        if len(response_text.split()) < 30:
            total_score = total_score * 0.7
        
        scores.append(total_score)
    
    # Return average score across all scenarios
    return sum(scores) / len(scores)