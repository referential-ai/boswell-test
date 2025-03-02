"""
Summary reporting functionality.
"""

from typing import Dict, Any
from botwell.core.grading import grade_to_percentage, percentage_to_letter_grade


def print_summary(results: Dict[str, Any]) -> None:
    """Print a summary table of results."""
    print("\n=== SUMMARY OF RESULTS ===")
    print(f"{'Model':<20} | {'Grade':<5} | {'Score':<5} | {'Grades Received'}")
    print("-" * 80)
    
    for author, stats in results["summary"].items():
        median_num = stats["median_numeric"]
        grades = ", ".join(stats["grades_received"])
        
        # Calculate percentage score
        percentage = grade_to_percentage(median_num)
        
        # Convert numeric back to letter grade for display
        median_letter = percentage_to_letter_grade(percentage)
                
        print(f"{author:<20} | {median_letter:<5} | {percentage:<5} | {grades}")
    
    # Print Boswell Quotient if available
    if "boswell_quotient" in results and "model_scores" in results["boswell_quotient"]:
        print("\n=== BOSWELL QUOTIENT ===")
        print(f"{'Rank':<5} | {'Model':<20} | {'Quotient':<8} | {'Grade':<5} | {'Performance':<11} | {'Evaluation':<11} | {'Efficiency':<11}")
        print("-" * 100)
        
        # Sort models by rank
        quotient_data = results["boswell_quotient"]["model_scores"]
        sorted_models = sorted(
            quotient_data.keys(),
            key=lambda m: quotient_data[m]["rank"]
        )
        
        for model in sorted_models:
            score_data = quotient_data[model]
            components = score_data["components"]
            
            rank = score_data["rank"]
            quotient = score_data["boswell_quotient"]
            
            # Convert to letter grade
            letter_grade = percentage_to_letter_grade(int(quotient))
            
            performance = components.get("performance", 0)
            performance_str = f"{performance:.1f}" if performance else "N/A"
            
            evaluation = components.get("evaluation", 0)
            evaluation_str = f"{evaluation:.1f}" if evaluation else "N/A"
            
            efficiency = components.get("efficiency", 0)
            efficiency_str = f"{efficiency:.1f}" if efficiency else "N/A"
            
            print(f"{rank:<5} | {model:<20} | {quotient:<8.1f} | {letter_grade:<5} | {performance_str:<11} | {evaluation_str:<11} | {efficiency_str:<11}")
    
    # Print grading bias if available
    if "bias_analysis" in results:
        print("\n=== GRADING BIAS ANALYSIS ===")
        
        # Get overall median
        overall_median = results["bias_analysis"]["overall_median"]
        overall_percentage = grade_to_percentage(overall_median)
        overall_median_letter = percentage_to_letter_grade(overall_percentage)
        
        print(f"Overall Median Grade: {overall_median_letter} ({overall_percentage})")
        print(f"{'Model':<20} | {'Grade':<5} | {'Score':<5} | {'Grading Bias':<25} | {'Bias Value'}")
        print("-" * 85)
        
        for grader, stats in results["bias_analysis"]["grader_bias"].items():
            # Convert numeric grade to percentage and letter
            median_grade = stats["median_given"]
            percentage = grade_to_percentage(median_grade)
            median_letter = percentage_to_letter_grade(percentage)
                    
            print(f"{grader:<20} | {median_letter:<5} | {percentage:<5} | {stats['letter_bias']:<25} | {stats['median_bias']:.2f}")
    
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
        if "boswell_quotient" in results:
            print("- Boswell Quotient chart")
            print("- Boswell Quotient component breakdown")