#!/usr/bin/env python3
"""
Boswell Test - LLM Comparative Analysis Tool

This script automates the process of:
1. Prompting multiple LLM models with an essay question
2. Having each model grade every other model's essay
3. Saving and analyzing the results

This implementation uses concurrent processing to improve performance.
"""

import os
import sys
import json
import time
import re
import argparse
import importlib
import requests
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from statistics import median
import concurrent.futures
from threading import Lock

# Configuration
API_KEY = os.environ.get("OPENROUTER_API_KEY")

# Check for API key
if not API_KEY:
    print("Error: OPENROUTER_API_KEY environment variable is not set.")
    print("Please set it with: export OPENROUTER_API_KEY='your-api-key'")
    sys.exit(1)

# Model configurations - customize as needed
# Only models verified to work with OpenRouter are included
MODELS = [
    {"name": "GPT-4o", "model_id": "openai/gpt-4o"},
    {"name": "Claude-3-Opus", "model_id": "anthropic/claude-3-opus"},
    {"name": "Claude-3-Sonnet", "model_id": "anthropic/claude-3-sonnet"},
    {"name": "Claude-3.7-Sonnet", "model_id": "anthropic/claude-3.7-sonnet"},
    {"name": "Claude-3.7-Sonnet-thinking", "model_id": "anthropic/claude-3.7-sonnet:thinking"},
    {"name": "GPT-4o-mini", "model_id": "openai/gpt-4o-mini"},
    {"name": "Llama-3-8B", "model_id": "meta-llama/llama-3-8b-instruct"},
    {"name": "GPT-3.5-Turbo", "model_id": "openai/gpt-3.5-turbo"},
    {"name": "o3-mini-high", "model_id": "openai/o3-mini-high"},
    {"name": "o1", "model_id": "openai/o1"},
    {"name": "o1-mini", "model_id": "openai/o1-mini"},
    {"name": "DeepSeek-R1-Full", "model_id": "deepseek/deepseek-r1"},
    {"name": "DeepSeek-Distill-Qwen-32b", "model_id": "deepseek/deepseek-r1-distill-qwen-32b"},
    {"name": "grok2-1212", "model_id": "x-ai/grok-2-1212"},
    {"name": "grok-beta", "model_id": "x-ai/grok-beta"},
    {"name": "Qwen-Plus", "model_id": "qwen/qwen-plus"},
    {"name": "Qwen-Turbo", "model_id": "qwen/qwen-turbo"},
    {"name": "Qwen-Max", "model_id": "qwen/qwen-max"},
    {"name": "Perplexity: Llama 3.1 Sonar 405B Online", "model_id": "perplexity/llama-3.1-sonar-huge-128k-online"},
    {"name": "Perplexity: Llama 3.1 Sonar 70B", "model_id": "perplexity/llama-3.1-sonar-large-128k-chat"},
    {"name": "Perplexity: Llama 3.1 Sonar 8B Online", "model_id": "perplexity/llama-3.1-sonar-small-128k-online"},
    {"name": "Gemini Flash 1.5", "model_id": "google/gemini-flash-1.5"},
    {"name": "Gemini Pro 1.5", "model_id": "google/gemini-pro-1.5"}
]


# Additional models to try (commented out as they're not currently available)
# ADDITIONAL_MODELS = [
#     {"name": "Claude-3.5-Sonnet", "model_id": "anthropic/claude-3-5-sonnet-20240620"},
# ]

# Available domains
AVAILABLE_DOMAINS = {
    "pol_sci_1": "Political Science - Level 1: AI Policy Analysis",
    "pol_sci_2": "Political Science - Level 2: AI Governance Analysis",
    "comp_sci_1": "Computer Science - Level 1: Algorithm Analysis",
    "comp_sci_2": "Computer Science - Level 2: System Design"
}


def calculate_tokens(text: str) -> int:
    """Estimate the number of tokens in a text string.
    
    This is a rough estimation using a simple rule of thumb:
    - Approximately 4 characters per token for English text
    """
    return max(1, len(text) // 4)


def call_openrouter_api(model_id: str, prompt: str) -> Dict[str, Any]:
    """Call OpenRouter API with the specified model and prompt.
    
    Returns:
        JSON response with added cost information
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/alanwilhelm/botwell",  # Update with your actual repo
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
        print("\nSample model IDs for use in boswell_test.py:")
        for i, model in enumerate(models[:10]):  # Show first 10 models
            print(f"  {model['name']}: \"{model['model_id']}\"")
        
        if len(models) > 10:
            print(f"  ... and {len(models) - 10} more (see {output_file} for complete list)")
            
    except Exception as e:
        print(f"Error saving models file: {e}")


def extract_grade(feedback: str) -> str:
    """Extract letter grade from grading feedback."""
    # First try to match the exact format we requested
    match = re.search(r"Grade:\s*([A-C][+-]?)", feedback)
    if match:
        return match.group(1)
    
    # Fall back to more flexible patterns if the exact format isn't found
    # Look for letter grades in various contexts
    grade_patterns = [
        r"([A-C][+-]?)\s*grade",  # "A+ grade" or "B- grade"
        r"grade\s*(?:of|is|:)?\s*([A-C][+-]?)",  # "grade of A" or "grade: B+"
        r"grade\s*[\"']([A-C][+-]?)[\"']",  # grade "A-" or grade 'B'
        r"([A-C][+-]?)$"  # Just the grade at the end of a line
    ]
    
    for pattern in grade_patterns:
        for line in feedback.split('\n'):
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1)
    
    # If we've reached here, no grade was found
    print(f"  Warning: Could not extract grade from feedback. Using N/A.")
    return "N/A"  # Grade not found


def grade_to_numeric(grade: str) -> float:
    """Convert letter grade to numeric value for calculating statistics."""
    grade_map = {
        "A+": 4.3, "A": 4.0, "A-": 3.7,
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7,
        "N/A": 0.0
    }
    return grade_map.get(grade, 0.0)


def load_domain(domain_name: str) -> Tuple[str, str, Dict[str, str]]:
    """Load the specified domain module and return its prompts."""
    try:
        domain_module = importlib.import_module(f"domains.{domain_name}")
        return (
            domain_module.ESSAY_PROMPT, 
            domain_module.GRADING_PROMPT,
            domain_module.DOMAIN_INFO
        )
    except (ImportError, AttributeError) as e:
        print(f"Error loading domain '{domain_name}': {e}")
        sys.exit(1)


def create_results_directory(domain_name: str, timestamp: str) -> Tuple[str, str]:
    """Create a timestamped directory for results."""
    # Create base results directory if it doesn't exist
    if not os.path.exists("results"):
        os.makedirs("results")
    
    # Create timestamped directory for this run
    run_dir = f"results/{timestamp}-{domain_name}"
    essays_dir = f"{run_dir}/essays"
    
    os.makedirs(run_dir, exist_ok=True)
    os.makedirs(essays_dir, exist_ok=True)
    
    return run_dir, essays_dir


def save_essay_with_grades(author: str, essay: str, grades: Dict[str, Dict[str, Any]], essays_dir: str) -> str:
    """Save an essay to a text file with grading feedback appended."""
    filename = f"{essays_dir}/{author}.md"
    
    with open(filename, 'w') as f:
        # Write essay header
        f.write(f"# Essay by {author}\n\n")
        f.write(essay)
        
        # Write grading feedback
        f.write("\n\n---\n\n")
        f.write("# Grading Feedback\n\n")
        
        for grader_name, grade_info in grades.items():
            f.write(f"## Graded by: {grader_name}\n\n")
            f.write(grade_info["feedback"])
            f.write(f"\n\n**Letter Grade:** {grade_info['grade']}\n")
            f.write(f"**Numeric Grade:** {grade_info['numeric_grade']:.1f}\n\n")
            f.write("---\n\n")
    
    return filename


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
        print("Error: No valid models available on OpenRouter.")
        sys.exit(1)
        
    return verified_models


def grade_essay(grader: Dict[str, str], author: str, essay: str, grading_prompt: str, max_retries: int) -> Dict[str, Any]:
    """Grade an essay with retry logic.
    
    This function is designed to be run concurrently.
    
    Returns:
        Dict containing grading results and metadata
    """
    grader_name = grader["name"]
    grader_id = grader["model_id"]
    
    result = {
        "grader_name": grader_name,
        "author": author,
        "feedback": None,
        "grade": None,
        "numeric_grade": 0.0,
        "response": None,
        "error": None,
        "duration": 0.0,
        "start_time": time.time()
    }
    
    print(f"  {grader_name} grading {author}'s essay...")
    formatted_grading_prompt = grading_prompt.format(essay=essay)
    
    for retry in range(max_retries):
        try:
            response = call_openrouter_api(grader_id, formatted_grading_prompt)
            
            if "error" in response:
                if retry < max_retries - 1:
                    print(f"  Error getting feedback from {grader_name}, retrying ({retry+1}/{max_retries})...")
                    time.sleep(2)
                    continue
                else:
                    result["error"] = f"Error after {max_retries} attempts: {response.get('error')}"
                    print(f"  Error getting feedback from {grader_name} after {max_retries} attempts, skipping.")
                    break
            
            feedback = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not feedback:
                if retry < max_retries - 1:
                    print(f"  Received empty feedback from {grader_name}, retrying...")
                    continue
                else:
                    result["error"] = "Empty feedback after all retries"
                    break
            
            # Extract grade from feedback
            grade = extract_grade(feedback)
            
            # Store results
            result["feedback"] = feedback
            result["grade"] = grade
            result["numeric_grade"] = grade_to_numeric(grade)
            result["response"] = response
            result["duration"] = time.time() - result["start_time"]
            
            # Format for display
            cost_display = ""
            if "cost_info" in response:
                cost_info = response["cost_info"]
                cost_display = f"(${cost_info['total_cost']:.4f})"
                
            time_display = f"in {result['duration']:.2f}s"
            print(f"  {grader_name} gave {author} a grade of {grade} {cost_display} {time_display}")
            
            return result
            
        except Exception as e:
            if retry < max_retries - 1:
                print(f"  Exception when getting feedback from {grader_name}: {e}, retrying ({retry+1}/{max_retries})...")
                time.sleep(2)
            else:
                result["error"] = f"Exception after {max_retries} attempts: {str(e)}"
                print(f"  Failed to get feedback from {grader_name} after {max_retries} attempts: {e}")
    
    # If we get here with no feedback, we failed after all retries
    result["duration"] = time.time() - result["start_time"]
    return result


def get_essay_from_model(model: Dict[str, str], essay_prompt: str, max_retries: int) -> Dict[str, Any]:
    """Get an essay from a single model with retry logic.
    
    This function is designed to be run concurrently.
    
    Returns:
        Dict containing the model name, essay content, response info, and timing data
    """
    model_name = model["name"]
    model_id = model["model_id"]
    result = {
        "model_name": model_name,
        "essay": None,
        "response": None,
        "error": None,
        "duration": 0.0,
        "start_time": time.time()
    }
    
    print(f"  Requesting essay from {model_name}...")
    
    for retry in range(max_retries):
        try:
            response = call_openrouter_api(model_id, essay_prompt)
            
            if "error" in response:
                if retry < max_retries - 1:
                    print(f"  Error getting essay from {model_name}, retrying ({retry+1}/{max_retries})...")
                    time.sleep(2)  # Wait longer between retries
                    continue
                else:
                    result["error"] = f"Error after {max_retries} attempts: {response.get('error')}"
                    print(f"  Error getting essay from {model_name} after {max_retries} attempts, skipping.")
                    break
            
            essay = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not essay:
                if retry < max_retries - 1:
                    print(f"  Received empty response from {model_name}, retrying...")
                    continue
                else:
                    result["error"] = "Empty response after all retries"
                    break
            
            # Success - store results
            result["essay"] = essay
            result["response"] = response
            result["duration"] = time.time() - result["start_time"]
            
            # Format for display
            cost_display = ""
            if "cost_info" in response:
                cost_info = response["cost_info"]
                cost_display = f"(${cost_info['total_cost']:.4f}, {cost_info['input_tokens'] + cost_info['output_tokens']} tokens)"
            
            time_display = f"in {result['duration']:.2f}s"
            print(f"  Received essay from {model_name} ({len(essay)} characters) {cost_display} {time_display}")
            
            return result
            
        except Exception as e:
            if retry < max_retries - 1:
                print(f"  Exception when getting essay from {model_name}: {e}, retrying ({retry+1}/{max_retries})...")
                time.sleep(2)
            else:
                result["error"] = f"Exception after {max_retries} attempts: {str(e)}"
                print(f"  Failed to get essay from {model_name} after {max_retries} attempts: {e}")
    
    # If we get here with no essay, we failed after all retries
    result["duration"] = time.time() - result["start_time"]
    return result


def run_boswell_test(domain_name: str, output_file: str, selected_models: List[str] = None, 
                 skip_verification: bool = False, max_retries: int = 3) -> Dict[str, Any]:
    """Run the full Boswell Test and return results."""
    # Start timing the entire process
    run_start_time = time.time()
    
    # Load domain
    essay_prompt, grading_prompt, domain_info = load_domain(domain_name)
    
    # Get verified models or use all models if verification is skipped
    if skip_verification:
        print("Skipping model verification (using all configured models)...")
        verified_models = MODELS
    else:
        verified_models = verify_available_models()
    
    # Filter models if needed
    models_to_use = verified_models
    if selected_models:
        models_to_use = [m for m in verified_models if m["name"] in selected_models]
        if not models_to_use:
            print("Error: No valid models selected.")
            sys.exit(1)
    
    # Create timestamp for this run - used for both timing and directory naming
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    # Initialize cost and timing tracking
    cost_tracking = {
        "total_cost": 0.0,
        "total_tokens": 0,
        "total_duration": 0.0,
        "essay_costs": {},
        "grading_costs": {}
    }
    
    timing_tracking = {
        "start_time": timestamp,
        "step_durations": {
            "essay_generation": 0.0,
            "grading": 0.0,
            "analysis": 0.0,
            "file_generation": 0.0,
            "total": 0.0
        },
        "model_timing": {
            "essay": {},
            "grading": {}
        }
    }
    
    # Create a results lock to prevent race conditions when updating shared data
    results_lock = Lock()
    
    results = {
        "domain": domain_info,
        "essays": {},
        "grades": {},
        "summary": {},
        "essay_files": {},  # Track essay files
        "available_models": [m["name"] for m in verified_models],
        "selected_models": [m["name"] for m in models_to_use],
        "run_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cost": cost_tracking,  # Add cost tracking
        "timing": timing_tracking  # Add timing tracking
    }
    
    # Step 1: Get essays from each model concurrently
    print(f"\nStep 1: Collecting essays from each model for domain '{domain_info['name']}'...")
    essay_start_time = time.time()
    
    # Use ThreadPoolExecutor to run API calls concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(10, len(models_to_use))) as executor:
        # Start all essay generation tasks
        future_to_model = {
            executor.submit(get_essay_from_model, model, essay_prompt, max_retries): model["name"]
            for model in models_to_use
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_model):
            model_name = future_to_model[future]
            try:
                essay_result = future.result()
                
                # Skip models with errors
                if essay_result["error"] or not essay_result["essay"]:
                    continue
                
                # Thread-safe update of the results dictionary
                with results_lock:
                    # Store the essay
                    results["essays"][model_name] = essay_result["essay"]
                    
                    # Track timing
                    results["timing"]["model_timing"]["essay"][model_name] = essay_result["duration"]
                    
                    # Track costs if available
                    if "response" in essay_result and essay_result["response"] and "cost_info" in essay_result["response"]:
                        cost_info = essay_result["response"]["cost_info"]
                        results["cost"]["essay_costs"][model_name] = cost_info
                        results["cost"]["total_cost"] += cost_info["total_cost"]
                        results["cost"]["total_tokens"] += cost_info["input_tokens"] + cost_info["output_tokens"]
                        results["cost"]["total_duration"] += cost_info["duration"]
                
            except Exception as e:
                print(f"  Error processing results from {model_name}: {e}")
    
    # Record total time for essay generation
    results["timing"]["step_durations"]["essay_generation"] = time.time() - essay_start_time
    
    # Check if we have enough essays to continue
    if len(results["essays"]) < 2:
        print("Error: Not enough valid essays received to perform grading (minimum 2 required).")
        print("Saving partial results and exiting.")
        save_results(results, output_file)
        return results
    
    # Step 2: Grade each essay with each model concurrently
    print("\nStep 2: Grading essays...")
    grading_start_time = time.time()
    
    # Prepare grading tasks
    grading_tasks = []
    for grader in models_to_use:
        grader_name = grader["name"]
        
        # Skip models that didn't generate essays
        if grader_name not in results["essays"]:
            print(f"  Skipping grader {grader_name} as it did not generate an essay.")
            continue
        
        # Initialize structures for this grader
        with results_lock:
            if grader_name not in results["timing"]["model_timing"]["grading"]:
                results["timing"]["model_timing"]["grading"][grader_name] = {}
            
            results["grades"][grader_name] = {}
        
        # Create tasks for each author-grader pair (excluding self-grading)
        for author, essay in results["essays"].items():
            if grader_name != author:  # Skip self-grading
                grading_tasks.append((grader, author, essay))
    
    # Use ThreadPoolExecutor to run grading concurrently
    # Limit to 10 concurrent tasks to avoid overwhelming the API
    max_concurrent_gradings = min(10, len(grading_tasks))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_gradings) as executor:
        # Start all grading tasks
        future_to_task = {
            executor.submit(grade_essay, grader, author, essay, grading_prompt, max_retries): (grader["name"], author)
            for grader, author, essay in grading_tasks
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_task):
            grader_name, author = future_to_task[future]
            try:
                grading_result = future.result()
                
                # Skip if there was an error
                if grading_result["error"] or not grading_result["feedback"]:
                    continue
                
                # Thread-safe update of the results dictionary
                with results_lock:
                    # Store grading results
                    results["grades"][grader_name][author] = {
                        "feedback": grading_result["feedback"],
                        "grade": grading_result["grade"],
                        "numeric_grade": grading_result["numeric_grade"],
                        "cost_info": grading_result["response"].get("cost_info", {})
                    }
                    
                    # Track timing
                    results["timing"]["model_timing"]["grading"][grader_name][author] = grading_result["duration"]
                    
                    # Track costs if available
                    if "response" in grading_result and grading_result["response"] and "cost_info" in grading_result["response"]:
                        cost_info = grading_result["response"]["cost_info"]
                        
                        # Initialize grading costs for this grader if not already there
                        if grader_name not in results["cost"]["grading_costs"]:
                            results["cost"]["grading_costs"][grader_name] = {}
                            
                        # Add this specific grading cost
                        results["cost"]["grading_costs"][grader_name][author] = cost_info
                        
                        # Update totals
                        results["cost"]["total_cost"] += cost_info["total_cost"]
                        results["cost"]["total_tokens"] += cost_info["input_tokens"] + cost_info["output_tokens"]
                        results["cost"]["total_duration"] += cost_info["duration"]
                
            except Exception as e:
                print(f"  Error processing grading results from {grader_name} for {author}: {e}")
    
    # Record total time for grading
    results["timing"]["step_durations"]["grading"] = time.time() - grading_start_time
    
    # Step 3: Calculate summary statistics
    print("\nStep 3: Calculating summary statistics...")
    analysis_start_time = time.time()
    
    for author in results["essays"].keys():
        numeric_grades = [
            results["grades"][grader][author]["numeric_grade"]
            for grader in results["grades"]
            if author in results["grades"][grader]
        ]
        
        if numeric_grades:
            results["summary"][author] = {
                "median_numeric": median(numeric_grades),
                "grades_received": [
                    results["grades"][grader][author]["grade"]
                    for grader in results["grades"]
                    if author in results["grades"][grader]
                ]
            }
    
    # Record time for analysis
    results["timing"]["step_durations"]["analysis"] = time.time() - analysis_start_time
    
    # Step 4: Create results directory and save essays with grading feedback
    print("\nStep 4: Creating results directory and saving artifacts...")
    file_gen_start_time = time.time()
    
    # Use the timestamp from the beginning of the run
    run_dir, essays_dir = create_results_directory(domain_name, timestamp)
    
    for author in results["essays"].keys():
        # Get all grades for this author
        author_grades = {
            grader: results["grades"][grader][author]
            for grader in results["grades"]
            if author in results["grades"][grader]
        }
        
        # Save essay with grades
        filename = save_essay_with_grades(
            author, 
            results["essays"][author], 
            author_grades,
            essays_dir
        )
        
        results["essay_files"][author] = filename
        print(f"  Saved essay and feedback for {author} to {filename}")
    
    # Save tables and other formats
    print("  Generating formatted tables...")
    generate_grade_tables(results, run_dir)
    
    # Save consolidated results
    save_results(results, f"{run_dir}/full_results.json")
    print(f"  All results saved to {run_dir} directory")
    
    # Also save to original output file location if specified
    if output_file != "boswell_results.json":
        save_results(results, output_file)
    
    # Record time for file generation
    results["timing"]["step_durations"]["file_generation"] = time.time() - file_gen_start_time
    
    # Calculate and record total run time
    total_run_time = time.time() - run_start_time
    results["timing"]["step_durations"]["total"] = total_run_time
    
    # Return path to results directory in results
    results["results_dir"] = run_dir
    
    # We'll format the durations when needed rather than storing them
    # This avoids dependency issues when generating reports
    # The formatted values can still be calculated as needed from the step_durations
    
    return results


def save_results(results: Dict[str, Any], filename: str) -> None:
    """Save results to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {filename}")


def calculate_grading_bias(results: Dict[str, Any], models: List[str]) -> Dict[str, Any]:
    """Calculate grading bias for each model."""
    # For each grader, collect all grades they gave
    grader_grades = {}
    for grader in models:
        if grader not in results["grades"]:
            continue
            
        # Convert letter grades to numeric for easier calculation
        numeric_grades = []
        for author, grade_info in results["grades"][grader].items():
            numeric_grades.append(grade_info["numeric_grade"])
            
        if numeric_grades:
            grader_grades[grader] = {
                "numeric_grades": numeric_grades,
                "median_given": median(numeric_grades),
                "mean_given": sum(numeric_grades) / len(numeric_grades),
                "count": len(numeric_grades)
            }
    
    # Calculate overall median of all grades
    all_numeric_grades = []
    for grader in grader_grades:
        all_numeric_grades.extend(grader_grades[grader]["numeric_grades"])
    
    overall_median = median(all_numeric_grades)
    overall_mean = sum(all_numeric_grades) / len(all_numeric_grades)
    
    # Calculate bias (difference from overall median)
    bias_results = {
        "overall_median": overall_median,
        "overall_mean": overall_mean,
        "grader_bias": {}
    }
    
    for grader, stats in grader_grades.items():
        # Positive bias means more lenient, negative means stricter
        median_bias = stats["median_given"] - overall_median
        mean_bias = stats["mean_given"] - overall_mean
        
        # Convert numeric bias back to letter grade offset
        letter_bias = "Neutral"
        if abs(median_bias) < 0.15:
            letter_bias = "Neutral"
        elif median_bias > 0:
            if median_bias > 0.6:
                letter_bias = "Very Lenient (+2 grades)"
            elif median_bias > 0.3:
                letter_bias = "Lenient (+1 grade)"
            else:
                letter_bias = "Slightly Lenient (+1/3 grade)"
        else:
            if median_bias < -0.6:
                letter_bias = "Very Strict (-2 grades)"
            elif median_bias < -0.3:
                letter_bias = "Strict (-1 grade)"
            else:
                letter_bias = "Slightly Strict (-1/3 grade)"
        
        bias_results["grader_bias"][grader] = {
            "median_given": stats["median_given"],
            "median_bias": median_bias,
            "mean_bias": mean_bias,
            "letter_bias": letter_bias,
            "count": stats["count"]
        }
    
    return bias_results


def generate_bias_ascii_table(bias_results: Dict[str, Any]) -> str:
    """Generate an ASCII table showing grading bias for each model."""
    # Calculate column widths
    model_width = max(len(grader) for grader in bias_results["grader_bias"].keys()) + 2
    bias_width = 20  # Enough for bias description
    median_width = 12  # Enough for median value
    
    # Build header
    header = f"{'Model':{model_width}} | {'Median Given':{median_width}} | {'Grading Bias':{bias_width}} |"
    
    # Build separator
    separator = "-" * model_width + "+" + "-" * (median_width + 2) + "+" + "-" * (bias_width + 2) + "+"
    
    # Build rows
    rows = []
    for grader, stats in bias_results["grader_bias"].items():
        # Convert numeric grade to letter
        median_letter = "N/A"
        for grade, value in [
            ("A+", 4.3), ("A", 4.0), ("A-", 3.7),
            ("B+", 3.3), ("B", 3.0), ("B-", 2.7),
            ("C+", 2.3), ("C", 2.0), ("C-", 1.7)
        ]:
            if abs(stats["median_given"] - value) < 0.15:  # Close enough to this grade
                median_letter = grade
                break
                
        row = f"{grader:{model_width}} | {median_letter:^{median_width}} | {stats['letter_bias']:{bias_width}} |"
        rows.append(row)
    
    # Add overall median row
    overall_median_letter = "N/A"
    for grade, value in [
        ("A+", 4.3), ("A", 4.0), ("A-", 3.7),
        ("B+", 3.3), ("B", 3.0), ("B-", 2.7),
        ("C+", 2.3), ("C", 2.0), ("C-", 1.7)
    ]:
        if abs(bias_results["overall_median"] - value) < 0.15:
            overall_median_letter = grade
            break
            
    overall_row = f"{'OVERALL':{model_width}} | {overall_median_letter:^{median_width}} | {'Baseline':{bias_width}} |"
    
    # Combine everything
    return f"{header}\n{separator}\n" + "\n".join(rows) + f"\n{separator}\n{overall_row}"


def generate_bias_markdown_table(bias_results: Dict[str, Any]) -> str:
    """Generate a Markdown table showing grading bias for each model."""
    # Build header
    header = "| Model | Median Given | Grading Bias | Numeric Bias |"
    
    # Build separator
    separator = "|------|-------------|-------------|-------------|"
    
    # Build rows
    rows = []
    for grader, stats in bias_results["grader_bias"].items():
        # Convert numeric grade to letter
        median_letter = "N/A"
        for grade, value in [
            ("A+", 4.3), ("A", 4.0), ("A-", 3.7),
            ("B+", 3.3), ("B", 3.0), ("B-", 2.7),
            ("C+", 2.3), ("C", 2.0), ("C-", 1.7)
        ]:
            if abs(stats["median_given"] - value) < 0.15:  # Close enough to this grade
                median_letter = grade
                break
                
        row = f"| {grader} | {median_letter} | {stats['letter_bias']} | {stats['median_bias']:.2f} |"
        rows.append(row)
    
    # Add overall median row
    overall_median_letter = "N/A"
    for grade, value in [
        ("A+", 4.3), ("A", 4.0), ("A-", 3.7),
        ("B+", 3.3), ("B", 3.0), ("B-", 2.7),
        ("C+", 2.3), ("C", 2.0), ("C-", 1.7)
    ]:
        if abs(bias_results["overall_median"] - value) < 0.15:
            overall_median_letter = grade
            break
            
    overall_row = f"| **OVERALL** | {overall_median_letter} | **Baseline** | 0.00 |"
    
    # Combine everything
    return f"{header}\n{separator}\n" + "\n".join(rows) + f"\n{overall_row}"


def generate_cost_report(results: Dict[str, Any]) -> str:
    """Generate a detailed cost report for the run."""
    cost_data = results["cost"]
    
    # Format total cost and duration
    total_cost = cost_data["total_cost"]
    total_duration = cost_data["total_duration"]
    total_tokens = cost_data["total_tokens"]
    
    report = []
    report.append("# Boswell Test Cost Report\n")
    report.append(f"Run timestamp: {results['run_timestamp']}\n")
    report.append(f"Domain: {results['domain']['name']}\n")
    report.append(f"## Summary\n")
    report.append(f"- **Total cost**: ${total_cost:.4f}")
    report.append(f"- **Total tokens**: {total_tokens:,}")
    report.append(f"- **Total duration**: {total_duration:.2f} seconds\n")
    
    # Essay Generation Costs
    report.append(f"## Essay Generation Costs\n")
    report.append("| Model | Tokens | Cost | Duration (s) |")
    report.append("|-------|--------|------|--------------|")
    
    essay_total_cost = 0
    for model_name, cost_info in cost_data["essay_costs"].items():
        tokens = cost_info["input_tokens"] + cost_info["output_tokens"]
        cost = cost_info["total_cost"]
        duration = cost_info["duration"]
        essay_total_cost += cost
        
        report.append(f"| {model_name} | {tokens:,} | ${cost:.4f} | {duration:.2f} |")
    
    report.append(f"| **TOTAL** | | **${essay_total_cost:.4f}** | |\n")
    
    # Grading Costs
    report.append(f"## Grading Costs\n")
    report.append("| Grader | Essays Graded | Total Tokens | Total Cost | Avg. Cost per Essay |")
    report.append("|--------|---------------|--------------|------------|---------------------|")
    
    grading_total_cost = 0
    for grader_name, gradings in cost_data["grading_costs"].items():
        essays_graded = len(gradings)
        grader_tokens = sum(info["input_tokens"] + info["output_tokens"] for info in gradings.values())
        grader_cost = sum(info["total_cost"] for info in gradings.values())
        avg_cost = grader_cost / essays_graded if essays_graded > 0 else 0
        grading_total_cost += grader_cost
        
        report.append(f"| {grader_name} | {essays_graded} | {grader_tokens:,} | ${grader_cost:.4f} | ${avg_cost:.4f} |")
    
    report.append(f"| **TOTAL** | | | **${grading_total_cost:.4f}** | |\n")
    
    # Cost breakdown by phase
    report.append(f"## Cost Breakdown by Phase\n")
    report.append("| Phase | Cost | Percentage |")
    report.append("|-------|------|------------|")
    
    essay_percent = (essay_total_cost / total_cost) * 100 if total_cost > 0 else 0
    grading_percent = (grading_total_cost / total_cost) * 100 if total_cost > 0 else 0
    
    report.append(f"| Essay Generation | ${essay_total_cost:.4f} | {essay_percent:.1f}% |")
    report.append(f"| Grading | ${grading_total_cost:.4f} | {grading_percent:.1f}% |")
    report.append(f"| **TOTAL** | **${total_cost:.4f}** | **100%** |")
    
    return "\n".join(report)


def generate_timing_report(results: Dict[str, Any]) -> str:
    """Generate a detailed timing report for the run."""
    timing_data = results["timing"]
    
    report = []
    report.append("# Boswell Test Timing Report\n")
    report.append(f"Run timestamp: {results['run_timestamp']}\n")
    report.append(f"Domain: {results['domain']['name']}\n")
    
    report.append("## Summary\n")
    
    # Format step durations
    durations = timing_data["step_durations"]
    total = durations["total"]
    
    # Handle case where total might be zero
    if total <= 0:
        # If total is zero, just show the durations without percentages
        report.append(f"- **Total run time**: 0.0s")
        report.append(f"- **Essay generation**: {durations['essay_generation']:.1f}s")
        report.append(f"- **Grading**: {durations['grading']:.1f}s")
        report.append(f"- **Analysis**: {durations['analysis']:.1f}s")
        report.append(f"- **File generation**: {durations['file_generation']:.1f}s\n")
    else:
        # Format durations manually - don't rely on 'formatted' which might not exist yet
        minutes, seconds = divmod(total, 60)
        formatted_total = f"{int(minutes)}m {seconds:.1f}s"
        
        report.append(f"- **Total run time**: {formatted_total}")
        report.append(f"- **Essay generation**: {durations['essay_generation']:.1f}s ({durations['essay_generation']/total*100:.1f}%)")
        report.append(f"- **Grading**: {durations['grading']:.1f}s ({durations['grading']/total*100:.1f}%)")
        report.append(f"- **Analysis**: {durations['analysis']:.1f}s ({durations['analysis']/total*100:.1f}%)")
        report.append(f"- **File generation**: {durations['file_generation']:.1f}s ({durations['file_generation']/total*100:.1f}%)\n")
    
    # Essay generation timing by model
    report.append("## Essay Generation Timing\n")
    report.append("| Model | Duration (s) |")
    report.append("|-------|-------------|")
    
    for model, duration in timing_data["model_timing"]["essay"].items():
        report.append(f"| {model} | {duration:.2f} |")
    
    # Calculate average essay generation time
    if timing_data["model_timing"]["essay"]:
        avg_essay_time = sum(timing_data["model_timing"]["essay"].values()) / len(timing_data["model_timing"]["essay"])
        report.append(f"| **Average** | **{avg_essay_time:.2f}** |\n")
    
    # Grading timing by model
    report.append("## Grading Timing\n")
    report.append("| Grader | Essays Graded | Total Duration (s) | Avg. Seconds per Essay |")
    report.append("|--------|---------------|-------------------|------------------------|")
    
    for grader, gradings in timing_data["model_timing"]["grading"].items():
        essays_graded = len(gradings)
        total_time = sum(gradings.values())
        avg_time = total_time / essays_graded if essays_graded > 0 else 0
        
        report.append(f"| {grader} | {essays_graded} | {total_time:.2f} | {avg_time:.2f} |")
    
    return "\n".join(report)


def generate_visualizations(results: Dict[str, Any], run_dir: str) -> None:
    """Generate data visualizations of the test results."""
    models = list(results["essays"].keys())
    
    # Create a charts directory
    charts_dir = f"{run_dir}/charts"
    os.makedirs(charts_dir, exist_ok=True)
    
    # 1. Chart: Grading bias visualization
    plt.figure(figsize=(12, 8))
    
    bias_data = results.get("bias_analysis", {}).get("grader_bias", {})
    if bias_data:
        graders = list(bias_data.keys())
        median_bias = [bias_data[grader]["median_bias"] for grader in graders]
        
        # Sort by bias value for better visualization
        sorted_indices = np.argsort(median_bias)
        sorted_graders = [graders[i] for i in sorted_indices]
        sorted_bias = [median_bias[i] for i in sorted_indices]
        
        # Color bars based on bias (red for negative/strict, green for positive/lenient)
        colors = ['#FF6B6B' if bias < 0 else '#4ECDC4' for bias in sorted_bias]
        
        plt.bar(sorted_graders, sorted_bias, color=colors)
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        plt.title('Grading Bias by Model')
        plt.xlabel('Model')
        plt.ylabel('Bias (Negative = Stricter, Positive = More Lenient)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/grading_bias.png", dpi=300)
        plt.close()
    
    # 2. Chart: Grade distribution
    plt.figure(figsize=(12, 8))
    
    # Collect all numeric grades
    numeric_grades = {}
    for model in models:
        grades = []
        for grader, grades_given in results.get("grades", {}).items():
            if model in grades_given:
                grades.append(grades_given[model]["numeric_grade"])
        if grades:
            numeric_grades[model] = grades
    
    if numeric_grades:
        # Create boxplot of grades received by each model
        plt.boxplot([numeric_grades[model] for model in models], 
                   labels=models, 
                   patch_artist=True,
                   boxprops=dict(facecolor='#A8DADC'))
        
        plt.title('Distribution of Grades Received by Each Model')
        plt.ylabel('Numeric Grade')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/grade_distribution.png", dpi=300)
        plt.close()
    
    # 3. Chart: Timing comparison
    plt.figure(figsize=(12, 8))
    
    timing_data = results.get("timing", {}).get("model_timing", {}).get("essay", {})
    if timing_data:
        model_names = list(timing_data.keys())
        times = list(timing_data.values())
        
        # Sort by time for better visualization
        sorted_indices = np.argsort(times)
        sorted_models = [model_names[i] for i in sorted_indices]
        sorted_times = [times[i] for i in sorted_indices]
        
        plt.barh(sorted_models, sorted_times, color='#457B9D')
        plt.title('Time to Generate Essay by Model')
        plt.xlabel('Time (seconds)')
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/essay_generation_time.png", dpi=300)
        plt.close()
    
    # 4. Chart: Grading time comparison
    plt.figure(figsize=(12, 8))
    
    grading_data = results.get("timing", {}).get("model_timing", {}).get("grading", {})
    if grading_data:
        # Calculate average grading time for each model
        avg_grading_times = {}
        for grader, times in grading_data.items():
            if times:
                avg_grading_times[grader] = sum(times.values()) / len(times)
        
        if avg_grading_times:
            graders = list(avg_grading_times.keys())
            avg_times = list(avg_grading_times.values())
            
            # Sort by time for better visualization
            sorted_indices = np.argsort(avg_times)
            sorted_graders = [graders[i] for i in sorted_indices]
            sorted_avg_times = [avg_times[i] for i in sorted_indices]
            
            plt.barh(sorted_graders, sorted_avg_times, color='#1D3557')
            plt.title('Average Grading Time by Model')
            plt.xlabel('Time (seconds)')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(f"{charts_dir}/average_grading_time.png", dpi=300)
            plt.close()
    
    # 5. Chart: Cost breakdown
    plt.figure(figsize=(12, 8))
    
    # Essay costs
    essay_costs = {}
    for model, cost_info in results.get("cost", {}).get("essay_costs", {}).items():
        essay_costs[model] = cost_info.get("total_cost", 0)
    
    # Grading costs
    grading_costs = {}
    for grader, gradings in results.get("cost", {}).get("grading_costs", {}).items():
        grading_costs[grader] = sum(info.get("total_cost", 0) for info in gradings.values())
    
    if essay_costs and grading_costs:
        # Prepare data for stacked bar chart
        models_with_both = [m for m in models if m in essay_costs and m in grading_costs]
        essay_cost_values = [essay_costs.get(m, 0) for m in models_with_both]
        grading_cost_values = [grading_costs.get(m, 0) for m in models_with_both]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bar_width = 0.5
        
        # Create stacked bars
        ax.bar(models_with_both, essay_cost_values, bar_width, 
               label='Essay Generation', color='#E9C46A')
        ax.bar(models_with_both, grading_cost_values, bar_width,
               bottom=essay_cost_values, label='Grading', color='#F4A261')
        
        ax.set_title('Cost Breakdown by Model')
        ax.set_xlabel('Model')
        ax.set_ylabel('Cost ($)')
        ax.legend()
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/cost_breakdown.png", dpi=300)
        plt.close()
    
    # 6. Chart: Process timing breakdown
    plt.figure(figsize=(10, 6))
    
    durations = results.get("timing", {}).get("step_durations", {})
    if durations:
        steps = ['essay_generation', 'grading', 'analysis', 'file_generation']
        step_names = ['Essay Generation', 'Grading', 'Analysis', 'File Generation']
        times = [durations.get(step, 0) for step in steps]
        
        # Check if we have any non-zero times to create a meaningful pie chart
        if sum(times) > 0:
            # Create pie chart
            plt.pie(times, labels=step_names, autopct='%1.1f%%', 
                    startangle=90, shadow=False, 
                    colors=['#264653', '#2A9D8F', '#E9C46A', '#F4A261'])
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            plt.title('Time Breakdown by Process Phase')
        else:
            # If all times are zero, create a placeholder message
            plt.text(0.5, 0.5, 'No timing data available', 
                     horizontalalignment='center', verticalalignment='center',
                     fontsize=14)
            plt.title('Time Breakdown by Process Phase')
            plt.axis('off')  # Hide axes
        
        plt.tight_layout()
        plt.savefig(f"{charts_dir}/time_breakdown.png", dpi=300)
        plt.close()
    
    print(f"  Visualizations saved to {charts_dir}")

def generate_grade_tables(results: Dict[str, Any], run_dir: str) -> None:
    """Generate formatted tables of grades in ASCII, Markdown, and CSV formats."""
    models = list(results["essays"].keys())
    
    # Calculate grading bias
    bias_results = calculate_grading_bias(results, models)
    
    # Add bias results to the main results
    results["bias_analysis"] = bias_results
    
    # Generate ASCII table
    ascii_table = generate_ascii_table(results, models)
    with open(f"{run_dir}/grades_table.txt", 'w') as f:
        f.write(ascii_table)
    
    # Generate Markdown table
    markdown_table = generate_markdown_table(results, models)
    with open(f"{run_dir}/grades_table.md", 'w') as f:
        f.write(markdown_table)
    
    # Generate CSV table
    csv_table = generate_csv_table(results, models)
    with open(f"{run_dir}/grades_table.csv", 'w') as f:
        f.write(csv_table)
    
    # Generate bias tables
    bias_ascii = generate_bias_ascii_table(bias_results)
    with open(f"{run_dir}/grading_bias.txt", 'w') as f:
        f.write(bias_ascii)
        
    bias_markdown = generate_bias_markdown_table(bias_results)
    with open(f"{run_dir}/grading_bias.md", 'w') as f:
        f.write(bias_markdown)
    
    # Generate cost report
    cost_report = generate_cost_report(results)
    with open(f"{run_dir}/cost_report.md", 'w') as f:
        f.write(cost_report)
        
    # Generate timing report
    timing_report = generate_timing_report(results)
    with open(f"{run_dir}/timing_report.md", 'w') as f:
        f.write(timing_report)
    
    # Generate visualizations
    generate_visualizations(results, run_dir)
    
    # Generate JSON grades file (just the grades and summary)
    grades_json = {
        "domain": results["domain"],
        "grades": results["grades"],
        "summary": results["summary"],
        "bias_analysis": bias_results,
        "cost": results["cost"],
        "run_timestamp": results["run_timestamp"]
    }
    with open(f"{run_dir}/grades.json", 'w') as f:
        json.dump(grades_json, f, indent=2)


def generate_ascii_table(results: Dict[str, Any], models: List[str]) -> str:
    """Generate an ASCII table of grades."""
    # Calculate column widths
    model_width = max(len(model) for model in models) + 2
    grade_width = 7  # Enough for "A+/A-" format
    
    # Build header
    header = f"{'Model':{model_width}} |"
    for grader in models:
        header += f" {grader[:grade_width-1]:{grade_width-1}} |"
    header += f" {'Median':{grade_width}} |"
    
    # Build separator
    separator = "-" * model_width + "+"
    for _ in models:
        separator += "-" * (grade_width + 1) + "+"
    separator += "-" * (grade_width + 2) + "+"
    
    # Build rows
    rows = []
    for author in models:
        row = f"{author:{model_width}} |"
        
        for grader in models:
            if grader == author:
                # Self-grade
                grade = "---"
            elif grader in results["grades"] and author in results["grades"][grader]:
                grade = results["grades"][grader][author]["grade"]
            else:
                grade = "N/A"
            
            row += f" {grade:^{grade_width-1}} |"
        
        # Add median
        if author in results["summary"]:
            median_letter = "N/A"
            median_num = results["summary"][author]["median_numeric"]
            
            # Convert numeric back to letter grade for display
            for grade, value in [
                ("A+", 4.3), ("A", 4.0), ("A-", 3.7),
                ("B+", 3.3), ("B", 3.0), ("B-", 2.7),
                ("C+", 2.3), ("C", 2.0), ("C-", 1.7)
            ]:
                if abs(median_num - value) < 0.15:  # Close enough to this grade
                    median_letter = grade
                    break
        else:
            median_letter = "N/A"
            
        row += f" {median_letter:^{grade_width}} |"
        rows.append(row)
    
    # Combine everything
    return f"{header}\n{separator}\n" + "\n".join(rows)


def generate_markdown_table(results: Dict[str, Any], models: List[str]) -> str:
    """Generate a Markdown table of grades."""
    # Build header
    header = "| Model | " + " | ".join(models) + " | Median Grade |"
    
    # Build separator
    separator = "|------|" + "|".join(["---" for _ in models]) + "|-------------|"
    
    # Build rows
    rows = []
    for author in models:
        grades = []
        
        for grader in models:
            if grader == author:
                # Self-grade
                grades.append("---")
            elif grader in results["grades"] and author in results["grades"][grader]:
                grades.append(results["grades"][grader][author]["grade"])
            else:
                grades.append("N/A")
        
        # Add median
        if author in results["summary"]:
            median_letter = "N/A"
            median_num = results["summary"][author]["median_numeric"]
            
            # Convert numeric back to letter grade for display
            for grade, value in [
                ("A+", 4.3), ("A", 4.0), ("A-", 3.7),
                ("B+", 3.3), ("B", 3.0), ("B-", 2.7),
                ("C+", 2.3), ("C", 2.0), ("C-", 1.7)
            ]:
                if abs(median_num - value) < 0.15:  # Close enough to this grade
                    median_letter = grade
                    break
        else:
            median_letter = "N/A"
            
        row = f"| {author} | " + " | ".join(grades) + f" | {median_letter} |"
        rows.append(row)
    
    # Combine everything
    return f"{header}\n{separator}\n" + "\n".join(rows)


def generate_csv_table(results: Dict[str, Any], models: List[str]) -> str:
    """Generate a CSV table of grades."""
    # Build header
    header = "Model," + ",".join(models) + ",Median Grade"
    
    # Build rows
    rows = []
    for author in models:
        grades = []
        
        for grader in models:
            if grader == author:
                # Self-grade
                grades.append("---")
            elif grader in results["grades"] and author in results["grades"][grader]:
                grades.append(results["grades"][grader][author]["grade"])
            else:
                grades.append("N/A")
        
        # Add median
        if author in results["summary"]:
            median_letter = "N/A"
            median_num = results["summary"][author]["median_numeric"]
            
            # Convert numeric back to letter grade for display
            for grade, value in [
                ("A+", 4.3), ("A", 4.0), ("A-", 3.7),
                ("B+", 3.3), ("B", 3.0), ("B-", 2.7),
                ("C+", 2.3), ("C", 2.0), ("C-", 1.7)
            ]:
                if abs(median_num - value) < 0.15:  # Close enough to this grade
                    median_letter = grade
                    break
        else:
            median_letter = "N/A"
            
        row = f"{author}," + ",".join(grades) + f",{median_letter}"
        rows.append(row)
    
    # Combine everything
    return f"{header}\n" + "\n".join(rows)


def print_summary(results: Dict[str, Any]) -> None:
    """Print a summary table of results."""
    print("\n=== SUMMARY OF RESULTS ===")
    print(f"{'Model':<20} | {'Median Grade':<12} | {'Grades Received'}")
    print("-" * 70)
    
    for author, stats in results["summary"].items():
        median_num = stats["median_numeric"]
        grades = ", ".join(stats["grades_received"])
        
        # Convert numeric back to letter grade for display
        median_letter = "N/A"
        for grade, value in [
            ("A+", 4.3), ("A", 4.0), ("A-", 3.7),
            ("B+", 3.3), ("B", 3.0), ("B-", 2.7),
            ("C+", 2.3), ("C", 2.0), ("C-", 1.7)
        ]:
            if abs(median_num - value) < 0.15:  # Close enough to this grade
                median_letter = grade
                break
                
        print(f"{author:<20} | {median_letter:<12} | {grades}")
    
    # Print grading bias if available
    if "bias_analysis" in results:
        print("\n=== GRADING BIAS ANALYSIS ===")
        
        # Get overall median
        overall_median = results["bias_analysis"]["overall_median"]
        overall_median_letter = "N/A"
        for grade, value in [
            ("A+", 4.3), ("A", 4.0), ("A-", 3.7),
            ("B+", 3.3), ("B", 3.0), ("B-", 2.7),
            ("C+", 2.3), ("C", 2.0), ("C-", 1.7)
        ]:
            if abs(overall_median - value) < 0.15:
                overall_median_letter = grade
                break
                
        print(f"Overall Median Grade: {overall_median_letter}")
        print(f"{'Model':<20} | {'Median Given':<12} | {'Grading Bias':<25} | {'Bias Value'}")
        print("-" * 70)
        
        for grader, stats in results["bias_analysis"]["grader_bias"].items():
            # Convert numeric grade to letter
            median_letter = "N/A"
            for grade, value in [
                ("A+", 4.3), ("A", 4.0), ("A-", 3.7),
                ("B+", 3.3), ("B", 3.0), ("B-", 2.7),
                ("C+", 2.3), ("C", 2.0), ("C-", 1.7)
            ]:
                if abs(stats["median_given"] - value) < 0.15:  # Close enough to this grade
                    median_letter = grade
                    break
                    
            print(f"{grader:<20} | {median_letter:<12} | {stats['letter_bias']:<25} | {stats['median_bias']:.2f}")
    
    # Print cost summary if available
    if "cost" in results:
        cost_data = results["cost"]
        total_cost = cost_data["total_cost"]
        total_duration = cost_data["total_duration"]
        total_tokens = cost_data["total_tokens"]
        
        print("\n=== COST SUMMARY ===")
        print(f"Total Cost: ${total_cost:.4f}")
        print(f"Total Tokens: {total_tokens:,}")
        print(f"Total Duration: {total_duration:.2f} seconds")
        
        # Calculate cost breakdown
        essay_cost = sum(info["total_cost"] for info in cost_data["essay_costs"].values())
        grading_cost = 0
        for grader_costs in cost_data["grading_costs"].values():
            grading_cost += sum(info["total_cost"] for info in grader_costs.values())
            
        print(f"Essay Generation: ${essay_cost:.4f} ({essay_cost/total_cost*100:.1f}%)")
        print(f"Grading: ${grading_cost:.4f} ({grading_cost/total_cost*100:.1f}%)")
        print(f"See cost_report.md for detailed breakdown")
    
    # Print timing information if available
    if "timing" in results and "step_durations" in results["timing"]:
        print("\n=== TIMING INFORMATION ===")
        
        # Format durations manually
        durations = results["timing"]["step_durations"]
        total = durations["total"]
        
        # Handle case where total might be zero
        if total <= 0:
            print(f"Total Run Time: 0.0s")
        else:
            minutes, seconds = divmod(total, 60)
            formatted_total = f"{int(minutes)}m {seconds:.1f}s"
            print(f"Total Run Time: {formatted_total}")
            
        print(f"Essay Generation: {durations['essay_generation']:.1f}s")
        print(f"Grading: {durations['grading']:.1f}s")
        print(f"Analysis: {durations['analysis']:.1f}s")
        print(f"File Generation: {durations['file_generation']:.1f}s")
    
    # Print essay file locations
    if "essay_files" in results:
        print("\n=== SAVED ESSAY FILES ===")
        for author, filename in results["essay_files"].items():
            print(f"{author:<20} | {filename}")
            
    # Print visualizations location
    if "results_dir" in results:
        print("\n=== VISUALIZATIONS ===")
        print(f"Data visualizations available in: {results['results_dir']}/charts/")
        print("- Grading bias chart")
        print("- Grade distribution boxplot")
        print("- Essay generation timing comparison")
        print("- Grading time comparison")
        print("- Cost breakdown")
        print("- Process timing breakdown")


def list_domains() -> None:
    """Display available domains."""
    print("\nAvailable domains:")
    print("-" * 60)
    for domain_id, description in AVAILABLE_DOMAINS.items():
        print(f"{domain_id:<15} | {description}")


def list_models() -> None:
    """Display available models."""
    print("\nAvailable models:")
    print("-" * 60)
    for model in MODELS:
        print(f"{model['name']:<25} | {model['model_id']}")


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Boswell Test - LLM Comparative Analysis")
    
    # Main operation modes
    domain_group = parser.add_mutually_exclusive_group()
    domain_group.add_argument("--domain", type=str, choices=AVAILABLE_DOMAINS.keys(),
                        default="pol_sci_1",
                        help="Domain to test (default: pol_sci_1)")
    domain_group.add_argument("--all-domains", action="store_true",
                        help="Run tests on all available domains")
    
    parser.add_argument("--output", type=str, default="boswell_results.json",
                        help="Output file name (default: boswell_results.json)")
    
    parser.add_argument("--models", type=str, nargs="+",
                        help="Specific models to test (default: all models)")
    
    parser.add_argument("--skip-verification", action="store_true",
                        help="Skip the model verification step (faster but less reliable)")
    
    parser.add_argument("--max-retries", type=int, default=3,
                        help="Maximum number of retries for API calls (default: 3)")
    
    # Information modes
    parser.add_argument("--list-domains", action="store_true",
                        help="List available domains and exit")
    
    parser.add_argument("--list-models", action="store_true",
                        help="List available models and exit")
    
    # Model management
    parser.add_argument("--update-models", action="store_true",
                        help="Update the local models file with currently available OpenRouter models and exit")
    
    parser.add_argument("--models-file", type=str, default="openrouter_models.json",
                        help="File to save/load OpenRouter models (default: openrouter_models.json)")
    
    return parser.parse_args()


def run_all_domains(args) -> None:
    """Run Boswell Test on all available domains."""
    print(f"Starting Boswell Test for ALL available domains ({len(AVAILABLE_DOMAINS)} domains)...")
    
    # If models specified, use them, otherwise use all
    if args.models:
        print(f"Using {len(args.models)} specified models: {', '.join(args.models)}")
        models_to_use = args.models
    else:
        print(f"Using all available models")
        models_to_use = None
    
    all_results = {}
    
    # Run tests for each domain sequentially
    for domain_name, domain_description in AVAILABLE_DOMAINS.items():
        print(f"\n{'='*70}")
        print(f"=== Running test for domain: {domain_description} ===")
        print(f"{'='*70}\n")
        
        # Create a domain-specific output file
        domain_output = f"boswell_results_{domain_name}.json"
        
        try:
            # Run the test with all options
            results = run_boswell_test(
                domain_name=domain_name,
                output_file=domain_output,
                selected_models=models_to_use,
                skip_verification=args.skip_verification,
                max_retries=args.max_retries
            )
            
            # Store results
            all_results[domain_name] = {
                "directory": results.get("results_dir", ""),
                "domain": domain_description
            }
            
            # Print summary
            print_summary(results)
            
            print(f"\nTest for domain '{domain_name}' completed!")
            print(f"  - Full results directory: {results['results_dir']}")
            print(f"  - Tables directory: {results['results_dir']}/grades_table.*")
            print(f"  - Essays directory: {results['results_dir']}/essays/")
            print(f"  - Visualizations: {results['results_dir']}/charts/")
            
        except Exception as e:
            print(f"Error running test for domain '{domain_name}': {e}")
            print("Continuing with next domain...")
    
    # Print final summary
    print(f"\n{'='*70}")
    print(f"=== ALL DOMAIN TESTS COMPLETED ===")
    print(f"{'='*70}")
    print(f"Summary of all domain test results:")
    
    for domain_name, info in all_results.items():
        print(f"  - {info['domain']}: {info['directory']}")
    
    print("\nBoswell Test for all domains has been completed!")

def main() -> None:
    """Main entry point for the script."""
    args = parse_arguments()
    
    # Handle information modes
    if args.list_domains:
        list_domains()
        return
    
    if args.list_models:
        list_models()
        return
    
    # Handle model management
    if args.update_models:
        update_models_file(args.models_file)
        return
    
    # Run tests on all domains
    if args.all_domains:
        run_all_domains(args)
        return
    
    # Run the test on a single domain
    print(f"Starting Boswell Test for domain '{args.domain}'...")
    
    # If models specified, use them, otherwise use all
    if args.models:
        print(f"Using {len(args.models)} specified models: {', '.join(args.models)}")
        models_to_use = args.models
    else:
        print(f"Using all available models")
        models_to_use = None
    
    # Run the test with all options
    results = run_boswell_test(
        domain_name=args.domain,
        output_file=args.output,
        selected_models=models_to_use,
        skip_verification=args.skip_verification,
        max_retries=args.max_retries
    )
    
    # Print summary
    print_summary(results)
    
    print(f"\nBoswell Test completed!")
    print(f"  - Full results directory: {results['results_dir']}")
    print(f"  - Tables directory: {results['results_dir']}/grades_table.*")
    print(f"  - Essays directory: {results['results_dir']}/essays/")
    print(f"  - Visualizations: {results['results_dir']}/charts/")


if __name__ == "__main__":
    main()