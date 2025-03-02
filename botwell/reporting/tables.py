"""
Table generation functionality for Boswell test results.
"""

import os
from typing import Dict, Any, List
from statistics import median

from botwell.core.grading import percentage_to_letter_grade, grade_to_percentage, calculate_grading_bias
from botwell.reporting.quotient import calculate_boswell_quotient


def generate_grade_tables(results: Dict[str, Any], run_dir: str) -> None:
    """Generate formatted tables of grades in ASCII, Markdown, and CSV formats."""
    models = list(results["essays"].keys())
    
    # Calculate grading bias
    bias_results = calculate_grading_bias(results, models)
    
    # Add bias results to the main results
    results["bias_analysis"] = bias_results
    
    # Calculate Boswell Quotient
    quotient_results = calculate_boswell_quotient(results, models)
    
    # Add Boswell Quotient results to the main results
    results["boswell_quotient"] = quotient_results
    
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
    
    # Generate Boswell Quotient table and report
    boswell_quotient_table = generate_boswell_quotient_table(quotient_results)
    boswell_report = generate_boswell_report(results, quotient_results)
    
    with open(f"{run_dir}/boswell_quotient.md", 'w') as f:
        f.write(boswell_quotient_table)
    
    with open(f"{run_dir}/boswell_report.md", 'w') as f:
        f.write(boswell_report)
    
    # Generate cost report
    from botwell.reporting.cost import generate_cost_report
    cost_report = generate_cost_report(results)
    with open(f"{run_dir}/cost_report.md", 'w') as f:
        f.write(cost_report)
        
    # Generate timing report
    from botwell.reporting.timing import generate_timing_report
    timing_report = generate_timing_report(results)
    with open(f"{run_dir}/timing_report.md", 'w') as f:
        f.write(timing_report)
    
    # Generate visualizations
    from botwell.reporting.visualizations import generate_visualizations
    generate_visualizations(results, run_dir)
    
    # Generate JSON grades file (just the grades and summary)
    import json
    grades_json = {
        "domain": results["domain"],
        "grades": results["grades"],
        "summary": results["summary"],
        "bias_analysis": bias_results,
        "boswell_quotient": quotient_results,
        "cost": results["cost"],
        "run_timestamp": results["run_timestamp"]
    }
    with open(f"{run_dir}/grades.json", 'w') as f:
        json.dump(grades_json, f, indent=2)


def generate_ascii_table(results: Dict[str, Any], models: List[str]) -> str:
    """Generate an ASCII table of grades with percentage scores."""
    # Calculate column widths
    model_width = max(len(model) for model in models) + 2
    grade_width = 10  # Enough for "A+ (97)" format
    median_width = 7  # Just for the letter grade
    pct_width = 5     # For percentage
    
    # Build header
    header = f"{'Model':{model_width}} |"
    for grader in models:
        header += f" {grader[:grade_width-1]:{grade_width-1}} |"
    header += f" {'Median':{median_width}} | {'Pct':{pct_width}} |"
    
    # Build separator
    separator = "-" * model_width + "+"
    for _ in models:
        separator += "-" * (grade_width + 1) + "+"
    separator += "-" * (median_width + 2) + "+" + "-" * (pct_width + 2) + "+"
    
    # Build rows
    rows = []
    for author in models:
        row = f"{author:{model_width}} |"
        
        for grader in models:
            if grader in results["grades"] and author in results["grades"][grader]:
                grade_data = results["grades"][grader][author]
                letter_grade = grade_data["grade"]
                numeric_grade = grade_data["numeric_grade"]
                percentage = grade_to_percentage(numeric_grade)
                grade_display = f"{letter_grade} ({percentage})"
            else:
                grade_display = "N/A"
            
            # Truncate if too long
            if len(grade_display) > grade_width - 1:
                grade_display = grade_display[:grade_width-2] + "…"
                
            row += f" {grade_display:{grade_width-1}} |"
        
        # Add median and percentage
        if author in results["summary"]:
            median_num = results["summary"][author]["median_numeric"]
            
            # Calculate percentage
            percentage = grade_to_percentage(median_num)
            
            # Convert numeric back to letter grade for display
            median_letter = percentage_to_letter_grade(percentage)
        else:
            median_letter = "N/A"
            percentage = "N/A"
            
        row += f" {median_letter:^{median_width}} | {percentage:^{pct_width}} |"
        rows.append(row)
    
    # Combine everything
    return f"{header}\n{separator}\n" + "\n".join(rows)


def generate_markdown_table(results: Dict[str, Any], models: List[str]) -> str:
    """Generate a Markdown table of grades with percentage scores."""
    # Build header
    header = "| Model | " + " | ".join(models) + " | Median Grade | Percentage |"
    
    # Build separator
    separator = "|------|" + "|".join(["---" for _ in models]) + "|-------------|-----------|"
    
    # Build rows
    rows = []
    for author in models:
        grades = []
        
        for grader in models:
            if grader in results["grades"] and author in results["grades"][grader]:
                grade_data = results["grades"][grader][author]
                letter_grade = grade_data["grade"]
                numeric_grade = grade_data["numeric_grade"]
                percentage = grade_to_percentage(numeric_grade)
                # Add percentage in parentheses
                grades.append(f"{letter_grade} ({percentage})")
            else:
                grades.append("N/A")
        
        # Add median
        if author in results["summary"]:
            median_num = results["summary"][author]["median_numeric"]
            
            # Calculate percentage
            percentage = grade_to_percentage(median_num)
            
            # Convert numeric back to letter grade for display
            median_letter = percentage_to_letter_grade(percentage)
            
            median_display = f"{median_letter} | {percentage}"
        else:
            median_display = "N/A | N/A"
            
        row = f"| {author} | " + " | ".join(grades) + f" | {median_display} |"
        rows.append(row)
    
    # Combine everything
    return f"{header}\n{separator}\n" + "\n".join(rows)


def generate_csv_table(results: Dict[str, Any], models: List[str]) -> str:
    """Generate a CSV table of grades with percentage scores."""
    # Build header
    header = "Model," + ",".join(models) + ",Median Grade,Percentage"
    
    # Build rows
    rows = []
    for author in models:
        grades = []
        
        for grader in models:
            if grader in results["grades"] and author in results["grades"][grader]:
                grade_data = results["grades"][grader][author]
                letter_grade = grade_data["grade"]
                numeric_grade = grade_data["numeric_grade"]
                percentage = grade_to_percentage(numeric_grade)
                # Add percentage in parentheses for CSV
                grades.append(f"{letter_grade} ({percentage})")
            else:
                grades.append("N/A")
        
        # Add median
        if author in results["summary"]:
            median_num = results["summary"][author]["median_numeric"]
            
            # Calculate percentage
            percentage = grade_to_percentage(median_num)
            
            # Convert numeric back to letter grade for display
            median_letter = percentage_to_letter_grade(percentage)
        else:
            median_letter = "N/A"
            percentage = "N/A"
            
        row = f"{author}," + ",".join(grades) + f",{median_letter},{percentage}"
        rows.append(row)
    
    # Combine everything
    return f"{header}\n" + "\n".join(rows)


def generate_bias_ascii_table(bias_results: Dict[str, Any]) -> str:
    """Generate an ASCII table showing grading bias for each model."""
    # Calculate column widths
    model_width = max(len(grader) for grader in bias_results["grader_bias"].keys()) + 2
    bias_width = 20  # Enough for bias description
    grade_width = 5   # For letter grade
    score_width = 5   # For percentage score
    
    # Build header
    header = f"{'Model':{model_width}} | {'Grade':{grade_width}} | {'Score':{score_width}} | {'Grading Bias':{bias_width}} |"
    
    # Build separator
    separator = "-" * model_width + "+" + "-" * (grade_width + 2) + "+" + "-" * (score_width + 2) + "+" + "-" * (bias_width + 2) + "+"
    
    # Build rows
    rows = []
    for grader, stats in bias_results["grader_bias"].items():
        # Convert numeric grade to letter and percentage
        median_grade = stats["median_given"]
        percentage = grade_to_percentage(median_grade)
        median_letter = percentage_to_letter_grade(percentage)
                
        row = f"{grader:{model_width}} | {median_letter:^{grade_width}} | {percentage:^{score_width}} | {stats['letter_bias']:{bias_width}} |"
        rows.append(row)
    
    # Add overall median row
    overall_median = bias_results["overall_median"]
    overall_percentage = grade_to_percentage(overall_median)
    overall_median_letter = percentage_to_letter_grade(overall_percentage)
            
    overall_row = f"{'OVERALL':{model_width}} | {overall_median_letter:^{grade_width}} | {overall_percentage:^{score_width}} | {'Baseline':{bias_width}} |"
    
    # Combine everything
    return f"{header}\n{separator}\n" + "\n".join(rows) + f"\n{separator}\n{overall_row}"


def generate_bias_markdown_table(bias_results: Dict[str, Any]) -> str:
    """Generate a Markdown table showing grading bias for each model."""
    # Build header
    header = "| Model | Grade | Score | Grading Bias | Numeric Bias |"
    
    # Build separator
    separator = "|------|-------|-------|-------------|-------------|"
    
    # Build rows
    rows = []
    for grader, stats in bias_results["grader_bias"].items():
        # Convert numeric grade to letter and percentage
        median_grade = stats["median_given"]
        percentage = grade_to_percentage(median_grade)
        median_letter = percentage_to_letter_grade(percentage)
                
        row = f"| {grader} | {median_letter} | {percentage} | {stats['letter_bias']} | {stats['median_bias']:.2f} |"
        rows.append(row)
    
    # Add overall median row
    overall_median = bias_results["overall_median"]
    overall_percentage = grade_to_percentage(overall_median)
    overall_median_letter = percentage_to_letter_grade(overall_percentage)
            
    overall_row = f"| **OVERALL** | {overall_median_letter} | {overall_percentage} | **Baseline** | 0.00 |"
    
    # Combine everything
    return f"{header}\n{separator}\n" + "\n".join(rows) + f"\n{overall_row}"


def generate_boswell_quotient_table(quotient_results: Dict[str, Any]) -> str:
    """Generate a Markdown table showing the Boswell Quotient for each model."""
    # Build header
    header = "| Rank | Model | Boswell Quotient | Grade | Performance | Evaluation | Efficiency |"
    
    # Build separator
    separator = "|------|-------|-----------------|-------|------------|------------|------------|"
    
    # Build rows
    rows = []
    sorted_models = sorted(
        quotient_results["model_scores"].keys(),
        key=lambda m: quotient_results["model_scores"][m]["rank"]
    )
    
    for model in sorted_models:
        score_data = quotient_results["model_scores"][model]
        components = score_data["components"]
        
        rank = score_data["rank"]
        quotient = score_data["boswell_quotient"]
        
        # Add letter grade equivalent of the Boswell Quotient
        letter_grade = percentage_to_letter_grade(int(quotient))
        
        performance = components.get("performance", "N/A")
        if performance != "N/A":
            performance = f"{performance:.1f}"
        
        evaluation = components.get("evaluation", "N/A")
        if evaluation != "N/A":
            evaluation = f"{evaluation:.1f}"
            
        efficiency = components.get("efficiency", "N/A")
        if efficiency != "N/A":
            efficiency = f"{efficiency:.1f}"
        
        rows.append(f"| {rank} | {model} | {quotient:.1f} | {letter_grade} | {performance} | {evaluation} | {efficiency} |")
    
    # Combine everything
    return f"{header}\n{separator}\n" + "\n".join(rows)


def generate_boswell_report(results: Dict[str, Any], quotient_results: Dict[str, Any]) -> str:
    """Generate a detailed report on the Boswell Quotient results."""
    from botwell.reporting.boswell import generate_boswell_report as generate_report
    return generate_report(results, quotient_results)