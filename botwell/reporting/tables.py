"""
Table generation functionality for Boswell test results.
"""

import os
from typing import Dict, Any, List
import re
from statistics import median
import importlib.util
from botwell.core.grading import percentage_to_letter_grade, grade_to_percentage, calculate_grading_bias
from botwell.reporting.boswell_quotient import calculate_boswell_quotient


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

    # Generate Excel cross-assessment table
    try:
        from botwell.reporting.excel import generate_cross_grading_excel
        # Generate the Excel table
        generate_cross_grading_excel(results, run_dir)
    except ImportError as e:
        print(f"Warning: Excel table generation skipped: {e}")
        print("To enable Excel output, install openpyxl: pip install openpyxl")
    
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
    # Handle duplicate model names for display
    display_models = models.copy()
    if len(set(models)) < len(models):
        model_counts = {}
        for i, model in enumerate(models):
            if model in model_counts:
                model_counts[model] += 1
                display_models[i] = f"{model} (Run {model_counts[model]})"
            else:
                model_counts[model] = 1
                
    # Calculate column widths
    model_width = max(len(model) for model in display_models) + 2
    grade_width = 10  # Enough for "A+ (97)" format
    median_width = 7  # Just for the letter grade
    pct_width = 5     # For percentage
    raw_avg_width = 12  # Adequate for "Overall Score" with 2 decimals
    
    # Build header
    header = f"{'Model Evaluated':{model_width}} |"
    for i, grader in enumerate(models):
        display_grader = display_models[i]
        header += f" {'Score: ' + display_grader[:grade_width-7]:{grade_width+5}} |"
    header += f" {'Median':{median_width}} | {'Pct':{pct_width}} | {'Overall Score':{raw_avg_width}} |"
    
    # Build separator
    separator = "-" * model_width + "+"
    for _ in range(len(models)):
        separator += "-" * (grade_width + 6) + "+"
    separator += "-" * (median_width + 2) + "+" + "-" * (pct_width + 2) + "+" + "-" * (raw_avg_width + 2) + "+"
    
    # Build rows
    rows = []
    for i, author in enumerate(models):
        display_author = display_models[i]
        row = f"{display_author:{model_width}} |"
        
        for j, grader in enumerate(models):
            if grader in results["grades"] and author in results["grades"][grader]:
                grade_data = results["grades"][grader][author]
                letter_grade = grade_data["grade"]
                numeric_grade = grade_data["numeric_grade"]
                percentage = grade_to_percentage(numeric_grade)
                grade_display = f"{letter_grade} ({percentage:.2f})"
            else:
                grade_display = "N/A (0.00)"
            
            # Truncate if too long
            if len(grade_display) > grade_width + 5:
                grade_display = grade_display[:grade_width+4] + "…"
            
            row += f" {grade_display:{grade_width+5}} |"
        
        # Add median and percentage
        if author in results["summary"]:
            median_num = results["summary"][author]["median_numeric"]
            
            # Calculate percentage
            percentage = grade_to_percentage(median_num)
            
            # Calculate raw mean (average) of numeric grades
            raw_grades = []
            for grader in models:
                if grader in results["grades"] and author in results["grades"][grader]:
                    raw_grades.append(results["grades"][grader][author]["numeric_grade"])
            raw_avg = sum(raw_grades) / len(raw_grades) if raw_grades else 0.0

            # Convert numeric back to letter grade for display
            median_letter = percentage_to_letter_grade(percentage)
        else:
            median_letter = "N/A"
            percentage = "0.00"
            raw_avg = 0.0
            
        row += f" {median_letter:^{median_width}} | {percentage:^{pct_width}} | {raw_avg:.2f} |"  # 2 decimal places for precision
        rows.append(row)
    
    # Combine everything
    return f"{header}\n{separator}\n" + "\n".join(rows)


def generate_markdown_table(results: Dict[str, Any], models: List[str]) -> str:
    """Generate a Markdown table of grades with percentage scores."""
    # Build header
    # Handle duplicate model names for display
    display_models = models.copy()
    if len(set(models)) < len(models):
        model_counts = {}
        for i, model in enumerate(models):
            if model in model_counts:
                model_counts[model] += 1
                display_models[i] = f"{model} (Run {model_counts[model]})"
            else:
                model_counts[model] = 1
                
    # Create clear column headers with "Score from [Model Name]"
    header = "| Model Being Evaluated |"
    for model in display_models:
        header += f" Score from {model} |"
    header += " Median Grade | Percentage |"

    # Add raw average column with better name
    header += " Overall Score |"

    # Add N/A count row for statistics
    na_counts = {}
    for model in models:
        na_counts[model] = sum(1 for grader in models 
                               if grader in results["grades"] 
                               and model in results["grades"][grader] and results["grades"][grader][model].get("grade") == "N/A")
    
    # Build separator
    separator = "|------|" + "|".join(["---" for _ in models]) + "|-------------|-----------|"
    
    # Add separator for raw average column
    separator += "------------|"
    
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
                grades.append(f"{letter_grade} ({percentage:.2f})")
            else:
                grades.append("N/A (0.00)")
        
        # Add median
        if author in results["summary"]:
            median_num = results["summary"][author]["median_numeric"]
            
            # Calculate percentage
            percentage = grade_to_percentage(median_num)
            
            # Calculate raw mean (average) of numeric grades
            raw_grades = []
            for grader in models:
                if grader in results["grades"] and author in results["grades"][grader]:
                    raw_grades.append(results["grades"][grader][author]["numeric_grade"])
            raw_avg = sum(raw_grades) / len(raw_grades) if raw_grades else 0.0
            
            # Convert numeric back to letter grade for display
            median_letter = percentage_to_letter_grade(percentage)
            
            median_display = f"{median_letter} | {percentage:.2f} | {raw_avg:.2f}"
        else:
            median_display = "N/A | 0.00 | 0.00"
            
        # Handle duplicate model names for row labels too
        author_index = models.index(author)
        display_author = display_models[author_index]
        
        row = f"| {display_author} | " + " | ".join(grades) + f" | {median_display} |"
        rows.append(row)

    # Add N/A statistics row if any N/A values exist
    if any(count > 0 for count in na_counts.values()):
        na_stats = []
        for model in models:
            if na_counts[model] > 0:
                na_stats.append(f"{na_counts[model]} N/A")
            else:
                na_stats.append("-")
        rows.append(f"| **N/A Count** | " + " | ".join(na_stats) + " | - | - | - |")
    
    # Combine everything
    return f"{header}\n{separator}\n" + "\n".join(rows)


def generate_csv_table(results: Dict[str, Any], models: List[str]) -> str:
    """Generate a CSV table of grades with percentage scores."""
    # Handle duplicate model names for display
    display_models = models.copy()
    if len(set(models)) < len(models):
        model_counts = {}
        for i, model in enumerate(models):
            if model in model_counts:
                model_counts[model] += 1
                display_models[i] = f"{model} (Run {model_counts[model]})"
            else:
                model_counts[model] = 1
                
    # Build header
    header = "Model Being Evaluated," + ",".join([f"Score from {display_models[i]}" for i in range(len(models))]) + ",Median Grade,Percentage,Overall Score"
    
    # Build rows
    rows = []
    for i, author in enumerate(models):
        display_author = display_models[i]
        grades = []
        
        for j, grader in enumerate(models):
            if grader in results["grades"] and author in results["grades"][grader]:
                grade_data = results["grades"][grader][author]
                letter_grade = grade_data["grade"]
                numeric_grade = grade_data["numeric_grade"]
                percentage = grade_to_percentage(numeric_grade)
                # Add percentage with 2 decimal places
                grades.append(f"{letter_grade} ({percentage:.2f})")
            else:
                grades.append("N/A (0.00)")
        
        # Add median with 2 decimal precision
        if author in results["summary"]:
            median_num = results["summary"][author]["median_numeric"]
            
            # Calculate percentage
            percentage = grade_to_percentage(median_num)
            
            # Calculate raw mean (average) of numeric grades
            raw_grades = []
            for grader in models:
                if grader in results["grades"] and author in results["grades"][grader]:
                    raw_grades.append(results["grades"][grader][author]["numeric_grade"])
            raw_avg = sum(raw_grades) / len(raw_grades) if raw_grades else 0.0
            
            # Convert numeric back to letter grade for display
            median_letter = percentage_to_letter_grade(percentage)
            formatted_percentage = f"{percentage:.2f}"
        else:
            median_letter = "N/A"
            formatted_percentage = "0.00"
            raw_avg = 0.0
            
        # Format the overall score with 2 decimal places for precision
        row = f"{display_author}," + ",".join(grades) + f",{median_letter},{formatted_percentage},{raw_avg:.2f}"
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
    """Generate a Markdown table showing the Boswell Quotient for each model.
    
    This is a visualization utility that formats Boswell Quotient data as a Markdown table.
    The core calculation happens in boswell_quotient.py.
    """
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

        # Format quotient with 2 decimal places for precision
        quotient_display = f"{quotient:.2f}"
        
        performance = components.get("performance", "N/A")
        if performance != "N/A":
            performance_display = f"{performance:.2f}"
        else:
            performance_display = "N/A (0.00)"
        
        evaluation = components.get("evaluation", "N/A")
        if evaluation != "N/A":
            evaluation_display = f"{evaluation:.2f}"
        else:
            evaluation_display = "N/A (0.00)"
            
        efficiency = components.get("efficiency", "N/A")
        if efficiency != "N/A":
            efficiency_display = f"{efficiency:.2f}"
        else:
            efficiency_display = "N/A (0.00)"
            
        # Count number of components that aren't N/A to note completeness
        component_count = sum(1 for c in components.values() if c != "N/A")
        missing_indication = "" if component_count == 3 else f" ({component_count}/3)"
        
        rows.append(f"| {rank} | {model} | {quotient_display} | {letter_grade}{missing_indication} | {performance_display} | {evaluation_display} | {efficiency_display} |")
    
    # Combine everything
    return f"{header}\n{separator}\n" + "\n".join(rows)


def generate_boswell_report(results: Dict[str, Any], quotient_results: Dict[str, Any]) -> str:
    """Generate a detailed report on the Boswell Quotient results."""
    from botwell.reporting.boswell import generate_boswell_report as generate_report
    return generate_report(results, quotient_results)