#!/usr/bin/env python3
"""
N/A Grade Handling Analysis Script

This script analyzes how N/A grades are handled throughout the Boswell system:
1. When and how they occur
2. How they affect calculations
3. How they appear in reports
"""

import os
import json
import re
from collections import defaultdict, Counter
from typing import Dict, List, Any, Tuple

# Function to analyze N/A grades in result directories
def analyze_na_grades_in_results(base_dir="results"):
    """Analyze N/A grades in all result directories."""
    print("Analyzing N/A grade handling in result directories...\n")
    
    result_stats = {
        "total_dirs": 0,
        "dirs_with_na": 0,
        "total_grades": 0,
        "na_grades": 0,
        "na_by_model": defaultdict(int),
        "na_by_grader": defaultdict(int),
        "na_patterns": []
    }
    
    # Find all result directories
    for dirname in os.listdir(base_dir):
        dir_path = os.path.join(base_dir, dirname)
        if not os.path.isdir(dir_path) or 'aggregate' in dirname:
            continue
            
        result_stats["total_dirs"] += 1
        
        # Look for full_results.json
        results_file = os.path.join(dir_path, "full_results.json")
        if not os.path.exists(results_file):
            continue
            
        with open(results_file, 'r') as f:
            try:
                results = json.load(f)
                
                # Check for N/A grades
                has_na = False
                for grader, graded_models in results.get("grades", {}).items():
                    for model, grade_data in graded_models.items():
                        result_stats["total_grades"] += 1
                        
                        if grade_data.get("grade") == "N/A":
                            has_na = True
                            result_stats["na_grades"] += 1
                            result_stats["na_by_model"][model] += 1
                            result_stats["na_by_grader"][grader] += 1
                            
                            # Get context for N/A
                            feedback = grade_data.get("feedback", "")
                            context = feedback[:100] + "..." if feedback else "No feedback"
                            result_stats["na_patterns"].append({
                                "dir": dirname,
                                "grader": grader,
                                "model": model,
                                "context": context
                            })
                
                if has_na:
                    result_stats["dirs_with_na"] += 1
            except json.JSONDecodeError:
                print(f"Error parsing JSON in {results_file}")
    
    # Print summary
    print(f"Analyzed {result_stats['total_dirs']} result directories")
    print(f"Directories with N/A grades: {result_stats['dirs_with_na']}")
    print(f"Total grades: {result_stats['total_grades']}")
    print(f"Total N/A grades: {result_stats['na_grades']} ({result_stats['na_grades'] / result_stats['total_grades'] * 100:.2f}%)")
    
    if result_stats["na_grades"] > 0:
        print("\nN/A grades by model being graded:")
        for model, count in sorted(result_stats["na_by_model"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {model}: {count}")
            
        print("\nN/A grades by grader model:")
        for grader, count in sorted(result_stats["na_by_grader"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {grader}: {count}")
            
        print("\nSample N/A contexts:")
        for i, pattern in enumerate(result_stats["na_patterns"][:5]):
            print(f"  {i+1}. {pattern['grader']} -> {pattern['model']}: {pattern['context']}")
    
    return result_stats

# Function to analyze how N/A grades affect the Boswell Quotient calculation
def analyze_na_impact_on_quotient(base_dir="results"):
    """Analyze how N/A grades affect Boswell Quotient calculations."""
    print("\nAnalyzing impact of N/A grades on Boswell Quotient calculations...\n")
    
    impact_stats = {
        "models_with_na": set(),
        "component_counts": defaultdict(int),
    }
    
    for dirname in os.listdir(base_dir):
        dir_path = os.path.join(base_dir, dirname)
        if not os.path.isdir(dir_path) or 'aggregate' in dirname:
            continue
            
        # Look for full_results.json
        results_file = os.path.join(dir_path, "full_results.json")
        if not os.path.exists(results_file):
            continue
            
        with open(results_file, 'r') as f:
            try:
                results = json.load(f)
                
                # Check Boswell Quotient components
                for model, data in results.get("boswell_quotient", {}).get("model_scores", {}).items():
                    components = data.get("components", {})
                    
                    # Count which components are present
                    available_components = set(components.keys())
                    impact_stats["component_counts"][tuple(sorted(available_components))] += 1
                    
                    # Check if any model with N/A grades got a Boswell Quotient
                    na_grades = False
                    for grader, grades in results.get("grades", {}).items():
                        if model in grades and grades[model].get("grade") == "N/A":
                            na_grades = True
                            break
                    
                    if na_grades:
                        impact_stats["models_with_na"].add(model)
            except json.JSONDecodeError:
                pass
    
    # Print summary
    print(f"Models affected by N/A grades: {len(impact_stats['models_with_na'])}")
    print("\nBoswell Quotient component combinations:")
    for components, count in sorted(impact_stats["component_counts"].items(), key=lambda x: x[1], reverse=True):
        print(f"  {', '.join(components)}: {count} instances")
    
    return impact_stats

# Function to check how N/A grades are displayed in reports
def analyze_na_in_reports(base_dir="results"):
    """Analyze how N/A grades are presented in different report formats."""
    print("\nAnalyzing how N/A grades are presented in reports...\n")
    
    report_stats = {
        "markdown_na_formats": set(),
        "csv_na_formats": set(),
        "txt_na_formats": set()
    }
    
    for dirname in os.listdir(base_dir):
        dir_path = os.path.join(base_dir, dirname)
        if not os.path.isdir(dir_path) or 'aggregate' in dirname:
            continue
            
        # Check report formats
        report_files = {
            "markdown": os.path.join(dir_path, "grades_table.md"),
            "csv": os.path.join(dir_path, "grades_table.csv"),
            "txt": os.path.join(dir_path, "grades_table.txt")
        }
        
        for format_name, filepath in report_files.items():
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    content = f.read()
                    
                    # Find N/A patterns in the report
                    if format_name == "markdown":
                        # Look for N/A patterns in markdown tables
                        na_patterns = re.findall(r'\|\s*(N/A[^|]*)', content)
                        for pattern in na_patterns:
                            report_stats["markdown_na_formats"].add(pattern.strip())
                    elif format_name == "csv":
                        # Look for N/A patterns in CSV
                        na_patterns = re.findall(r'N/A[^,\n]*', content)
                        for pattern in na_patterns:
                            report_stats["csv_na_formats"].add(pattern.strip())
                    elif format_name == "txt":
                        # Look for N/A patterns in txt tables
                        na_patterns = re.findall(r'N/A[^\|]*', content)
                        for pattern in na_patterns:
                            report_stats["txt_na_formats"].add(pattern.strip())
    
    # Print summary
    print("N/A formats in different report types:")
    for format_name, patterns in report_stats.items():
        print(f"\n{format_name.upper()} report N/A formats:")
        for pattern in patterns:
            print(f"  \"{pattern}\"")
    
    return report_stats

def analyze_retry_mechanism(core_dir="botwell/core", reporting_dir="botwell/reporting"):
    """Analyze the current retry mechanism for grade extraction."""
    print("\nAnalyzing grade extraction retry mechanism...\n")
    
    # Check if retry_grade_extraction exists in test.py
    test_py_path = os.path.join(core_dir, "test.py")
    has_retry = False
    has_retry_in_grade_essay = False
    
    if os.path.exists(test_py_path):
        with open(test_py_path, 'r') as f:
            test_content = f.read()
            has_retry = "def retry_grade_extraction" in test_content
            has_retry_in_grade_essay = "retry" in test_content and "grade_essay" in test_content
    
    print(f"Dedicated retry extraction function exists: {has_retry}")
    print(f"Retry logic in grade_essay function: {has_retry_in_grade_essay}")
    
    # Check logging for N/A grades in grading.py
    grading_py_path = os.path.join(core_dir, "grading.py")
    has_log_function = False
    
    if os.path.exists(grading_py_path):
        with open(grading_py_path, 'r') as f:
            grading_content = f.read()
            has_log_function = "def log_failed_extraction" in grading_content
    
    print(f"Dedicated logging for failed extractions: {has_log_function}")
    
    # Check N/A handling in Boswell Quotient calculation
    boswell_quotient_py_path = os.path.join(reporting_dir, "boswell_quotient.py")
    has_na_handling = False
    
    if os.path.exists(boswell_quotient_py_path):
        with open(boswell_quotient_py_path, 'r') as f:
            boswell_content = f.read()
            
            # Check for N/A handling patterns
            na_patterns = [
                "numeric_grade" in boswell_content and "0.0" in boswell_content,
                "skip" in boswell_content.lower() and "N/A" in boswell_content,
                "!=" in boswell_content and "N/A" in boswell_content,
            ]
            has_na_handling = any(na_patterns)
    
    print("N/A handling in Boswell Quotient calculation:")
    print(f"  - Special handling for N/A grades: {has_na_handling}")
    
    return {
        "has_retry_mechanism": has_retry,
        "grade_essay_has_retry": has_retry_in_grade_essay,
        "has_na_logging": has_log_function,
        "na_handling_in_quotient": has_na_handling
    }

if __name__ == "__main__":
    print("=" * 70)
    print("N/A GRADE HANDLING ANALYSIS")
    print("=" * 70)
    
    result_stats = analyze_na_grades_in_results()
    impact_stats = analyze_na_impact_on_quotient()
    report_stats = analyze_na_in_reports()
    retry_stats = analyze_retry_mechanism()
    
    print("\n" + "=" * 70)
    print("SUMMARY OF N/A GRADE HANDLING")
    print("=" * 70)
    
    print(f"\nN/A Grade Frequency: {result_stats['na_grades']} / {result_stats['total_grades']} grades ({result_stats['na_grades'] / result_stats['total_grades'] * 100:.2f}%)")
    
    # Create a recommendation based on findings
    print("\nRECOMMENDATIONS:")
    
    if result_stats['na_grades'] / result_stats['total_grades'] > 0.05:
        print("- High N/A frequency suggests need for improved grade extraction patterns")
    
    if not retry_stats["has_retry_mechanism"]:
        print("- Implement dedicated retry mechanism for grade extraction failures")
    
    if not retry_stats["has_na_logging"]:
        print("- Add comprehensive logging for N/A grade occurrences")
    
    # Output to a markdown file for easier reading
    with open("na_grade_analysis.md", "w") as f:
        f.write("# N/A Grade Handling Analysis\n\n")
        
        f.write("## Statistics\n\n")
        f.write(f"- Total grades analyzed: {result_stats['total_grades']}\n")
        f.write(f"- N/A grades: {result_stats['na_grades']} ({result_stats['na_grades'] / result_stats['total_grades'] * 100:.2f}%)\n")
        f.write(f"- Result directories with N/A grades: {result_stats['dirs_with_na']} / {result_stats['total_dirs']}\n\n")
        
        f.write("## N/A Grades by Model\n\n")
        for model, count in sorted(result_stats["na_by_model"].items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {model}: {count}\n")
        
        f.write("\n## N/A Grades by Grader\n\n")
        for grader, count in sorted(result_stats["na_by_grader"].items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {grader}: {count}\n")
        
        f.write("\n## Impact on Boswell Quotient\n\n")
        f.write(f"- Models affected by N/A grades: {len(impact_stats['models_with_na'])}\n")
        f.write("\nComponent combinations in results:\n\n")
        for components, count in sorted(impact_stats["component_counts"].items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {', '.join(components)}: {count} instances\n")
        
        f.write("\n## Current System Behavior\n\n")
        f.write(f"- Dedicated retry extraction function: {'Yes' if retry_stats['has_retry_mechanism'] else 'No'}\n")
        f.write(f"- Retry logic in grade_essay: {'Yes' if retry_stats['grade_essay_has_retry'] else 'No'}\n")
        f.write(f"- Dedicated logging for failed extractions: {'Yes' if retry_stats['has_na_logging'] else 'No'}\n")
        f.write(f"- Special handling for N/A grades in Boswell Quotient: {'Yes' if retry_stats['na_handling_in_quotient'] else 'No'}\n")
        
        f.write("\n## Recommendations\n\n")
        recommendations = []
        
        if result_stats['na_grades'] / result_stats['total_grades'] > 0.05:
            recommendations.append("Improve grade extraction patterns due to high N/A frequency")
        
        if not retry_stats["has_retry_mechanism"]:
            recommendations.append("Implement dedicated retry mechanism for grade extraction failures")
        
        if not retry_stats["has_na_logging"]:
            recommendations.append("Add comprehensive logging for N/A grade occurrences")
            
        recommendations.append("Standardize N/A display format across all report types")
        recommendations.append("Consider adding specific N/A handling documentation")
        
        for rec in recommendations:
            f.write(f"- {rec}\n")
    
    print(f"\nDetailed analysis written to na_grade_analysis.md")