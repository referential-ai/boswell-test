"""
Boswell Quotient calculation core functionality.

The Boswell Quotient is a comprehensive metric (0-100) designed to measure how well a model can 
serve as an indispensable AI companion. It combines three key components:

1. Performance (33.3%): Based on grades received from peer models
2. Evaluation (33.3%): Based on grading accuracy, consistency, and bias measurement
3. Efficiency (33.3%): Based on response time and resource utilization

This module contains the core functionality for calculating the Boswell Quotient.
"""

from typing import Dict, Any, List


def calculate_boswell_quotient(results: Dict[str, Any], models: List[str]) -> Dict[str, Any]:
    """Calculate the Boswell Quotient for each model.
    
    The Boswell Quotient is a composite score (0-100) based on:
    1. Performance Score (33.3%): Based on grades received from other models
    2. Evaluation Score (33.3%): Based on grading accuracy and consistency
    3. Efficiency Score (33.3%): Based on timing measurements
    
    Returns:
        Dictionary with Boswell Quotient scores and component scores for each model
    """
    quotient_results = {
        "model_scores": {},
        "component_weights": {
            "performance": 0.333,  # 33.3% weight for performance
            "evaluation": 0.333,   # 33.3% weight for evaluation capability
            "efficiency": 0.334    # 33.3% weight for efficiency (slightly higher to ensure sum is 1.0)
        }
    }
    
    # Collect all performance scores (grades received)
    performance_scores = {}
    max_performance_score = 4.3  # A+ = 4.3
    
    for model in models:
        if model in results["summary"]:
            # Get median numeric grade received (on 0-4.3 scale)
            median_grade = results["summary"][model]["median_numeric"]
            # Convert to 0-100 scale for the performance component
            performance_score = (median_grade / max_performance_score) * 100
            performance_scores[model] = performance_score
    
    # Collect evaluation scores (based on grading accuracy and bias)
    evaluation_scores = {}
    if "bias_analysis" in results and "grader_bias" in results["bias_analysis"]:
        bias_data = results["bias_analysis"]["grader_bias"]
        
        for model in models:
            if model in bias_data:
                # Calculate how close the model's grading is to the consensus
                # A bias of 0 is perfect, higher absolute bias reduces score
                bias_magnitude = abs(bias_data[model]["median_bias"])
                
                # Convert bias to a score (0-100)
                # Perfect score for no bias, decreasing as bias increases
                # Bias of 0.7 (very lenient/strict) gives ~40% evaluation score
                # Bias of 0.3 (slightly lenient/strict) gives ~70% evaluation score
                evaluation_score = max(0, 100 - (bias_magnitude * 100))
                evaluation_scores[model] = evaluation_score
    
    # Collect efficiency scores (based on timing)
    efficiency_scores = {}
    timing_data = results.get("timing", {}).get("model_timing", {})
    
    if timing_data and "essay" in timing_data and "grading" in timing_data:
        # Calculate max response times to normalize
        essay_times = [timing_data["essay"].get(model, 0) for model in models if model in timing_data["essay"]]
        max_essay_time = max(essay_times) if essay_times else 1
        
        # Calculate average grading times
        avg_grading_times = {}
        for model in models:
            if model in timing_data["grading"]:
                times = timing_data["grading"][model]
                if times:
                    avg_grading_times[model] = sum(times.values()) / len(times)
        
        max_grading_time = max(avg_grading_times.values()) if avg_grading_times else 1
        
        # Calculate efficiency scores
        for model in models:
            essay_time_score = 0
            grading_time_score = 0
            
            # Essay generation efficiency (faster is better)
            if model in timing_data["essay"]:
                # Inverse relationship - faster times get higher scores
                essay_time = timing_data["essay"][model]
                essay_time_score = max(0, 100 * (1 - (essay_time / max_essay_time)))
            
            # Grading efficiency
            if model in avg_grading_times:
                # Inverse relationship - faster times get higher scores
                grading_time = avg_grading_times[model]
                grading_time_score = max(0, 100 * (1 - (grading_time / max_grading_time)))
            
            # Combine essay and grading efficiency (equal weight)
            if essay_time_score > 0 or grading_time_score > 0:
                weights = []
                scores = []
                
                if essay_time_score > 0:
                    weights.append(0.5)
                    scores.append(essay_time_score)
                
                if grading_time_score > 0:
                    weights.append(0.5)
                    scores.append(grading_time_score)
                
                total_weight = sum(weights)
                if total_weight > 0:
                    efficiency_scores[model] = sum(w * s for w, s in zip(weights, scores)) / total_weight
    
    # Calculate the final Boswell Quotient for each model
    for model in models:
        components = {}
        weighted_scores = []
        weights = []
        
        # Add performance component if available
        if model in performance_scores:
            performance = performance_scores[model]
            components["performance"] = performance
            weighted_scores.append(performance * quotient_results["component_weights"]["performance"])
            weights.append(quotient_results["component_weights"]["performance"])
        
        # Add evaluation component if available
        if model in evaluation_scores:
            evaluation = evaluation_scores[model]
            components["evaluation"] = evaluation
            weighted_scores.append(evaluation * quotient_results["component_weights"]["evaluation"])
            weights.append(quotient_results["component_weights"]["evaluation"])
        
        # Add efficiency component if available
        if model in efficiency_scores:
            efficiency = efficiency_scores[model]
            components["efficiency"] = efficiency
            weighted_scores.append(efficiency * quotient_results["component_weights"]["efficiency"])
            weights.append(quotient_results["component_weights"]["efficiency"])
        
        # Calculate final score if we have any components
        if weighted_scores:
            total_weight = sum(weights)
            if total_weight > 0:
                # Normalize by actual weights used
                final_score = sum(weighted_scores) / total_weight
                
                # Store results
                quotient_results["model_scores"][model] = {
                    "boswell_quotient": round(final_score, 1),
                    "components": components,
                    "rank": 0  # Will be filled in later
                }
    
    # Rank models by Boswell Quotient
    ranked_models = sorted(
        quotient_results["model_scores"].keys(),
        key=lambda m: quotient_results["model_scores"][m]["boswell_quotient"],
        reverse=True
    )
    
    # Assign ranks (1-based)
    for i, model in enumerate(ranked_models):
        quotient_results["model_scores"][model]["rank"] = i + 1
    
    return quotient_results


def interpret_boswell_quotient(score: float) -> str:
    """Interpret a Boswell Quotient score.
    
    Returns a string description of what the score means.
    """
    if score >= 90:
        return "Exceptional across all dimensions"
    elif score >= 80:
        return "Excellent overall capability"
    elif score >= 70:
        return "Strong performance with some areas for improvement"
    elif score >= 60:
        return "Capable but with significant limitations"
    else:
        return "Not recommended for general assistant purposes"