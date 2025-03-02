"""
Core testing functionality for Boswell tests.
"""

import time
import json
import concurrent.futures
from threading import Lock
from typing import List, Dict, Any, Optional

from botwell.domains import load_domain, AVAILABLE_DOMAINS
from botwell.models.api import call_openrouter_api
from botwell.core.files import create_results_directory, save_essay_with_grades, save_results
from botwell.core.grading import extract_grade, grade_to_numeric, calculate_grading_bias
from botwell.core.verification import verify_available_models
from botwell.models.config import MODELS
from botwell.reporting.tables import generate_grade_tables


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


def run_boswell_test(domain_name: str, output_file: str, selected_models: List[str] = None, 
                 skip_verification: bool = False, max_retries: int = 3, is_free_run: bool = False) -> Dict[str, Any]:
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
            return {}
    
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
        "timing": timing_tracking,  # Add timing tracking
        "is_free_run": is_free_run  # Track if this is a free run
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
        
        # Still create a results directory to save the partial results
        run_dir, essays_dir = create_results_directory(domain_name, timestamp, results["is_free_run"])
        results["results_dir"] = run_dir
        
        # Save the partial results
        save_results(results, output_file)
        save_results(results, f"{run_dir}/partial_results.json")
        
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
        
        # Create tasks for each author-grader pair (including self-grading)
        for author, essay in results["essays"].items():
            # Allow self-grading (no longer skip when grader_name == author)
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
    
    from statistics import median as calc_median
    
    for author in results["essays"].keys():
        numeric_grades = [
            results["grades"][grader][author]["numeric_grade"]
            for grader in results["grades"]
            if author in results["grades"][grader]
        ]
        
        if numeric_grades:
            results["summary"][author] = {
                "median_numeric": calc_median(numeric_grades),
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
    run_dir, essays_dir = create_results_directory(domain_name, timestamp, results["is_free_run"])
    
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
    
    return results


def run_all_domains(args) -> None:
    """Run Boswell Test on all available domains."""
    print(f"Starting Boswell Test for ALL available domains ({len(AVAILABLE_DOMAINS)} domains)...")
    
    # Determine which models to use
    models_to_use = None
    if args.models:
        print(f"Using {len(args.models)} specified models: {', '.join(args.models)}")
        models_to_use = args.models
    elif args.free:
        from botwell.models.config import FREE_MODELS
        print(f"Using free models only: {', '.join(FREE_MODELS)}")
        models_to_use = FREE_MODELS
        print("Premium models will be excluded from the test.")
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
                max_retries=args.max_retries,
                is_free_run=args.free
            )
            
            # Store results
            all_results[domain_name] = {
                "directory": results.get("results_dir", ""),
                "domain": domain_description,
                "boswell_quotient": results.get("boswell_quotient", {}),
                "run_timestamp": results.get("run_timestamp", "")
            }
            
            # Print summary
            from botwell.reporting.summary import print_summary
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
    
    # Generate aggregate Boswell Quotient if we have multiple domains
    if len(all_results) > 1:
        print("\nGenerating aggregate Boswell Quotient report across all domains...")
        
        # Create timestamp for aggregate results
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        
        # Create aggregate results directory
        aggregate_dir = f"results/{timestamp}-aggregate"
        os.makedirs(aggregate_dir, exist_ok=True)
        
        # Generate aggregate data
        from botwell.reporting.aggregate import aggregate_boswell_quotient, generate_aggregate_boswell_report
        aggregated_data = aggregate_boswell_quotient(all_results)
        
        # Create mapping of domain IDs to descriptions
        domain_descriptions = {name: desc for name, desc in AVAILABLE_DOMAINS.items()}
        
        # Generate aggregate report
        aggregate_report = generate_aggregate_boswell_report(aggregated_data, domain_descriptions)
        
        # Save aggregate report
        with open(f"{aggregate_dir}/aggregate_boswell_report.md", 'w') as f:
            f.write(aggregate_report)
        
        # Generate aggregate visualizations
        from botwell.reporting.visualizations import generate_aggregate_visualizations
        generate_aggregate_visualizations(aggregated_data, aggregate_dir)
        
        # Save aggregate data as JSON
        with open(f"{aggregate_dir}/aggregate_boswell_quotient.json", 'w') as f:
            json.dump({
                "timestamp": timestamp,
                "aggregated_data": aggregated_data,
                "source_domains": [d for d in aggregated_data["domains_analyzed"]],
                "domain_descriptions": domain_descriptions
            }, f, indent=2)
        
        print(f"Aggregate results saved to: {aggregate_dir}")
        print(f"  - Aggregate report: {aggregate_dir}/aggregate_boswell_report.md")
        print(f"  - Visualizations: {aggregate_dir}/charts/")
    
    print("\nBoswell Test for all domains has been completed!")