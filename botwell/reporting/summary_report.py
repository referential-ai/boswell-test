"""
Comprehensive summary report generation for Boswell Test results.

This module provides functions to generate a single markdown report that combines
all result artifacts into a comprehensive summary.
"""

import os
import json
import time
from typing import Dict, Any, List


def generate_summary_report(results: Dict[str, Any], output_path: str = None) -> str:
    """
    Generate a comprehensive markdown summary report from Boswell Test results.
    
    Args:
        results: The complete results dictionary from a Boswell Test run
        output_path: Optional path to save the report to (if None, report is only returned)
        
    Returns:
        The generated markdown report as a string
    """
    # Start building the report
    report_parts = []
    
    # Report header
    domain_info = results.get("domain", {})
    run_timestamp = results.get("run_timestamp", "Unknown")
    
    report_parts.append(f"# Boswell Test Summary Report")
    report_parts.append(f"**Domain:** {domain_info.get('name', 'Unknown')}")
    report_parts.append(f"**Run Date:** {run_timestamp}")
    report_parts.append(f"**Report Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report_parts.append("")
    
    # Add test overview
    report_parts.append("## Test Overview")
    report_parts.append(f"- **Models Tested:** {len(results.get('essays', {}))}")
    report_parts.append(f"- **Domain Description:** {domain_info.get('description', 'No description')}")
    
    # Add timing information if available
    if "timing" in results and "step_durations" in results["timing"]:
        durations = results["timing"]["step_durations"]
        total_time = durations.get("total", 0)
        if total_time > 0:
            # Format total time
            hours, remainder = divmod(total_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{int(hours)}h {int(minutes)}m {seconds:.1f}s" if hours > 0 else f"{int(minutes)}m {seconds:.1f}s"
            
            report_parts.append(f"- **Total Runtime:** {time_str}")
            report_parts.append(f"- **Essay Generation:** {durations.get('essay_generation', 0):.1f}s ({durations.get('essay_generation', 0)/total_time*100:.1f}%)")
            report_parts.append(f"- **Grading Process:** {durations.get('grading', 0):.1f}s ({durations.get('grading', 0)/total_time*100:.1f}%)")
        
    # Add cost information if available
    if "cost" in results:
        cost_data = results["cost"]
        total_cost = cost_data.get("total_cost", 0)
        total_tokens = cost_data.get("total_tokens", 0)
        
        report_parts.append(f"- **Total Cost:** ${total_cost:.4f}")
        report_parts.append(f"- **Total Tokens:** {total_tokens:,}")
        
        # Cost breakdown if available
        essay_cost = sum(info["total_cost"] for info in cost_data.get("essay_costs", {}).values()) if "essay_costs" in cost_data else 0
        grading_cost = 0
        if "grading_costs" in cost_data:
            for grader_costs in cost_data["grading_costs"].values():
                grading_cost += sum(info["total_cost"] for info in grader_costs.values())
                
        if total_cost > 0:
            report_parts.append(f"- **Essay Generation Cost:** ${essay_cost:.4f} ({essay_cost/total_cost*100:.1f}%)")
            report_parts.append(f"- **Grading Cost:** ${grading_cost:.4f} ({grading_cost/total_cost*100:.1f}%)")
    
    report_parts.append("")
    
    # Add Boswell Quotient section if available
    if "boswell_quotient" in results and "model_scores" in results["boswell_quotient"]:
        report_parts.append("## Boswell Quotient Rankings")
        report_parts.append("The Boswell Quotient is a comprehensive metric (0-100) that combines model performance, grading ability, and efficiency.")
        report_parts.append("")
        
        # Add the Boswell Quotient table
        report_parts.append("| Rank | Model | Boswell Quotient | Grade | Performance | Evaluation | Efficiency |")
        report_parts.append("|------|-------|-----------------|-------|------------|------------|------------|")
        
        quotient_data = results["boswell_quotient"]["model_scores"]
        sorted_models = sorted(
            quotient_data.keys(),
            key=lambda m: quotient_data[m]["rank"]
        )
        
        for model in sorted_models:
            score_data = quotient_data[model]
            components = score_data.get("components", {})
            
            rank = score_data.get("rank", "N/A")
            quotient = score_data.get("boswell_quotient", 0)
            
            # Add letter grade for the Boswell Quotient
            from botwell.core.grading import percentage_to_letter_grade
            letter_grade = percentage_to_letter_grade(int(quotient)) if quotient else "N/A"
            
            performance = components.get("performance", "N/A")
            performance_str = f"{performance:.1f}" if performance != "N/A" else "N/A"
            
            evaluation = components.get("evaluation", "N/A")
            evaluation_str = f"{evaluation:.1f}" if evaluation != "N/A" else "N/A"
            
            efficiency = components.get("efficiency", "N/A")
            efficiency_str = f"{efficiency:.1f}" if efficiency != "N/A" else "N/A"
            
            row = f"| {rank} | {model} | {quotient:.1f} | {letter_grade} | {performance_str} | {evaluation_str} | {efficiency_str} |"
            report_parts.append(row)
            
        report_parts.append("")
        
    # Add Performance Summary (grades received)
    report_parts.append("## Performance Overview")
    report_parts.append("Summary of grades received by each model:")
    report_parts.append("")
    report_parts.append("| Model | Median Grade | Percentage | Grade Range |")
    report_parts.append("|-------|-------------|------------|-------------|")
    
    for model, summary in results.get("summary", {}).items():
        median_numeric = summary.get("median_numeric", 0)
        
        # Convert to percentage
        from botwell.core.grading import grade_to_percentage, percentage_to_letter_grade
        percentage = grade_to_percentage(median_numeric)
        median_letter = percentage_to_letter_grade(percentage)
        
        # Get grade range
        grades = summary.get("grades_received", [])
        grade_range = ", ".join(grades) if grades else "N/A"
        
        report_parts.append(f"| {model} | {median_letter} | {percentage} | {grade_range} |")
    
    report_parts.append("")
    
    # Add Grading Bias Analysis
    if "bias_analysis" in results:
        report_parts.append("## Grading Bias Analysis")
        report_parts.append("Analysis of each model's grading tendencies compared to the consensus:")
        report_parts.append("")
        report_parts.append("| Model | Median Given | Grading Bias | Numeric Bias |")
        report_parts.append("|-------|-------------|-------------|-------------|")
        
        bias_data = results["bias_analysis"]
        overall_median = bias_data.get("overall_median", 0)
        
        for grader, stats in bias_data.get("grader_bias", {}).items():
            median_given = stats.get("median_given", 0)
            percentage = grade_to_percentage(median_given)
            letter_grade = percentage_to_letter_grade(percentage)
            
            letter_bias = stats.get("letter_bias", "Unknown")
            numeric_bias = stats.get("median_bias", 0)
            
            report_parts.append(f"| {grader} | {letter_grade} | {letter_bias} | {numeric_bias:.2f} |")
            
        # Add overall baseline
        overall_percentage = grade_to_percentage(overall_median)
        overall_letter = percentage_to_letter_grade(overall_percentage)
        report_parts.append(f"| **OVERALL** | {overall_letter} | **Baseline** | 0.00 |")
        
        report_parts.append("")
    
    # Add Visualization References
    if "results_dir" in results:
        charts_dir = f"{results['results_dir']}/charts"
        if os.path.exists(charts_dir):
            report_parts.append("## Data Visualizations")
            report_parts.append("The following visualizations were generated during analysis:")
            report_parts.append("")
            
            # Map chart files to descriptions
            charts = {
                "boswell_quotient.png": "**Boswell Quotient Rankings**: Overall model capabilities",
                "boswell_quotient_components.png": "**Component Breakdown**: Performance, evaluation and efficiency factors",
                "grade_distribution.png": "**Grade Distribution**: Range of grades received by each model",
                "grading_bias.png": "**Grading Bias**: Models' tendency to grade strictly or leniently",
                "essay_generation_time.png": "**Essay Generation Time**: Speed of content generation",
                "average_grading_time.png": "**Average Grading Time**: Speed of evaluation",
                "cost_breakdown.png": "**Cost Analysis**: Comparison of resource usage",
                "time_breakdown.png": "**Time Distribution**: Proportion of time by process phase"
            }
            
            for chart_file, description in charts.items():
                if os.path.exists(f"{charts_dir}/{chart_file}"):
                    report_parts.append(f"- {description}")
            
            report_parts.append("")
            report_parts.append("These visualizations can be found in the `charts/` directory of the results.")
            report_parts.append("")
    
    # Final report
    report = "\n".join(report_parts)
    
    # Save the report if a path is provided
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"Summary report saved to: {output_path}")
        
    return report


def create_summary_report_for_results(results_dir: str) -> str:
    """
    Create a summary report for an existing results directory.
    
    Args:
        results_dir: Path to a Boswell Test results directory
        
    Returns:
        Path to the generated summary report
    """
    # Load the full results
    results_file = os.path.join(results_dir, "full_results.json")
    if not os.path.exists(results_file):
        raise FileNotFoundError(f"No full_results.json found in {results_dir}")
    
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    # Generate and save report
    output_path = os.path.join(results_dir, "summary_report.md")
    generate_summary_report(results, output_path)
    
    return output_path