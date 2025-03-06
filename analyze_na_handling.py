#!/usr/bin/env python3
"""
Analyze N/A Grade Handling in Boswell Test Results

This script analyzes how N/A grades are handled throughout the Boswell test system,
including their frequency, impact on Boswell Quotient calculations, and how they are
displayed in various report formats.
"""

import os
import json
import re
import glob
from typing import Dict, Any, List, Tuple
from collections import Counter, defaultdict
import sys
import inspect

# Add the current directory to the path so we can import Boswell modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def find_result_dirs() -> List[str]:
    """Find all result directories in the standard location."""
    result_dirs = []
    
    # Look for results in the standard location
    for dir_path in glob.glob("results/*-*-*"):
        if os.path.isdir(dir_path) and not dir_path.endswith("-aggregate"):
            result_dirs.append(dir_path)
            
    return sorted(result_dirs)

def count_na_grades(result_dir: str) -> Tuple[int, int]:
    """Count N/A grades in a result directory's grades.json file."""
    grades_file = os.path.join(result_dir, "grades.json")
    if not os.path.exists(grades_file):
        return 0, 0
        
    with open(grades_file, 'r') as f:
        grades_data = json.load(f)
        
    total_grades = 0
    na_grades = 0
    
    # Check first-level structure
    if isinstance(grades_data, dict):
        for grader, graded_models in grades_data.items():
            if not isinstance(graded_models, dict):
                continue
                
            for model, grade_info in graded_models.items():
                total_grades += 1
                
                # Handle different grade info formats
                if isinstance(grade_info, dict) and "grade" in grade_info:
                    if grade_info["grade"] == "N/A":
                        na_grades += 1
                elif isinstance(grade_info, str):
                    if grade_info == "N/A":
                        na_grades += 1
                # Add more format handlers if needed
                
    return na_grades, total_grades

def identify_na_affected_models(result_dir: str) -> Dict[str, int]:
    """Identify models that received N/A grades and count how many."""
    grades_file = os.path.join(result_dir, "grades.json")
    if not os.path.exists(grades_file):
        return {}
        
    with open(grades_file, 'r') as f:
        grades_data = json.load(f)
        
    model_na_counts = defaultdict(int)
    
    if isinstance(grades_data, dict):
        for grader, graded_models in grades_data.items():
            if not isinstance(graded_models, dict):
                continue
                
            for model, grade_info in graded_models.items():
                # Handle different grade info formats
                is_na = False
                
                if isinstance(grade_info, dict) and "grade" in grade_info:
                    is_na = grade_info["grade"] == "N/A"
                elif isinstance(grade_info, str):
                    is_na = grade_info == "N/A"
                # Add more format handlers if needed
                
                if is_na:
                    model_na_counts[model] += 1
                
    return dict(model_na_counts)

def analyze_boswell_quotient_impact(result_dir: str) -> Dict[str, Any]:
    """Analyze how N/A grades impact Boswell Quotient calculations."""
    bq_file = os.path.join(result_dir, "boswell_quotient.md")
    if not os.path.exists(bq_file):
        return {}
        
    with open(bq_file, 'r') as f:
        bq_content = f.read()
        
    # Look for models with incomplete components (e.g., "B+ (2/3)")
    incomplete_pattern = r"\|\s*(.*?)\s*\|\s*[\d\.]+\s*\|\s*[A-F][+-]?\s*\((\d+)/(\d+)\)"
    incomplete_matches = re.findall(incomplete_pattern, bq_content)
    
    components = {}
    for model, actual, total in incomplete_matches:
        components[model.strip()] = {"actual": int(actual), "total": int(total)}
        
    # Check for N/A components
    na_pattern = r"\|\s*(.*?)\s*\|.*?\|\s*N/A\s*\(0\.00\)"
    na_matches = re.findall(na_pattern, bq_content)
    
    na_components = {}
    for model in na_matches:
        na_components[model.strip()] = True
        
    return {
        "incomplete_components": components,
        "na_components": na_components
    }

def analyze_na_formats(result_dir: str) -> Dict[str, Any]:
    """Analyze how N/A grades are formatted in different report types."""
    formats = {
        "markdown": set(),
        "csv": set(),
        "txt": set()
    }
    
    # Check Markdown format
    md_file = os.path.join(result_dir, "grades_table.md")
    if os.path.exists(md_file):
        with open(md_file, 'r') as f:
            content = f.read()
            na_matches = re.findall(r"N/A\s*\([^)]*\)", content)
            for match in na_matches:
                formats["markdown"].add(match)
                
    # Check CSV format
    csv_file = os.path.join(result_dir, "grades_table.csv")
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            content = f.read()
            na_matches = re.findall(r"N/A\s*\([^)]*\)", content)
            for match in na_matches:
                formats["csv"].add(match)
                
    # Check TXT format
    txt_file = os.path.join(result_dir, "grades_table.txt")
    if os.path.exists(txt_file):
        with open(txt_file, 'r') as f:
            content = f.read()
            na_matches = re.findall(r"N/A\s*\([^)]*", content)  # TXT might truncate
            for match in na_matches:
                formats["txt"].add(match)
                
    return formats

def check_retry_mechanism():
    """Check if there's a dedicated retry mechanism for grade extraction."""
    try:
        from botwell.core.grading import extract_grade
        
        # Check for multiple extraction methods
        extract_grade_code = inspect.getsource(extract_grade)
        
        has_pattern_matching = "grade_patterns" in extract_grade_code
        has_contextual_analysis = "after_grade" in extract_grade_code
        has_semantic_descriptor = "grade_descriptors" in extract_grade_code
        has_retry_logic = "recovered grade" in extract_grade_code.lower()
        has_logging = "log_failed_extraction" in extract_grade_code
        
        # Check for N/A handling in Boswell Quotient calculation
        try:
            from botwell.reporting.boswell_quotient import calculate_boswell_quotient
            bq_code = inspect.getsource(calculate_boswell_quotient)
            special_na_handling = "N/A" in bq_code
        except (ImportError, AttributeError):
            special_na_handling = False
            
        return {
            "has_pattern_matching": has_pattern_matching,
            "has_contextual_analysis": has_contextual_analysis, 
            "has_semantic_descriptor": has_semantic_descriptor,
            "has_retry_logic": has_retry_logic,
            "has_logging": has_logging,
            "special_na_handling": special_na_handling
        }
        
    except ImportError:
        return {
            "has_pattern_matching": False,
            "has_contextual_analysis": False,
            "has_semantic_descriptor": False,
            "has_retry_logic": False,
            "has_logging": False,
            "special_na_handling": False
        }

def main():
    """Main analysis function."""
    print("=" * 70)
    print("N/A GRADE HANDLING ANALYSIS")
    print("=" * 70)
    
    # Debug: Check if files exist before processing
    print("Checking for result directories...")
    if not os.path.exists("results"):
        print("Warning: 'results' directory not found!")
        result_dirs = []
    else:
        result_dirs = find_result_dirs()
        print(f"Found {len(result_dirs)} result directories")
    if not result_dirs:
        print("No result directories found.")
        return
        
    print(f"Analyzing N/A grade handling in result directories...")
    print()
    
    # Count N/A grades across all result directories
    total_na = 0
    total_grades = 0
    na_dirs = 0
    
    for dir_path in result_dirs:
        na_count, grade_count = count_na_grades(dir_path)
        if na_count > 0:
            na_dirs += 1
        total_na += na_count
        total_grades += grade_count
        
    na_percentage = (total_na / total_grades * 100) if total_grades > 0 else 0
    
    print(f"Analyzed {len(result_dirs)} result directories")
    print(f"Directories with N/A grades: {na_dirs}")
    print(f"Total grades: {total_grades}")
    print(f"Total N/A grades: {total_na} ({na_percentage:.2f}%)")
    print()
    
    # Analyze impact on Boswell Quotient calculation
    print("Analyzing impact of N/A grades on Boswell Quotient calculations...")
    print()
    
    all_affected_models = {}
    for dir_path in result_dirs:
        affected_models = identify_na_affected_models(dir_path)
        for model, count in affected_models.items():
            all_affected_models[model] = all_affected_models.get(model, 0) + count
            
    print(f"Models affected by N/A grades: {len(all_affected_models)}")
    
    # Collect Boswell Quotient component combinations
    component_combinations = Counter()
    for dir_path in result_dirs:
        bq_impact = analyze_boswell_quotient_impact(dir_path)
        for model, info in bq_impact.get("incomplete_components", {}).items():
            component_combinations[(info["actual"], info["total"])] += 1
    
    print("\nBoswell Quotient component combinations:")
    for (actual, total), count in component_combinations.items():
        components = []
        if actual == 1 and total == 3:
            components = ["performance only"]
        elif actual == 2 and total == 3:
            components = ["efficiency, evaluation", "efficiency, performance", "evaluation, performance"]
        elif actual == 3 and total == 3:
            components = ["efficiency, evaluation, performance"]
            
        if components:
            component_str = ", ".join(components)
            print(f"  {actual}/{total} components ({component_str}): {count} instances")
        else:
            print(f"  {actual}/{total} components: {count} instances")
    
    # Analyze how N/A is presented in reports
    print("\nAnalyzing how N/A grades are presented in reports...")
    print()
    
    all_formats = {
        "MARKDOWN_NA_FORMATS": set(),
        "CSV_NA_FORMATS": set(),
        "TXT_NA_FORMATS": set()
    }
    
    for dir_path in result_dirs:
        formats = analyze_na_formats(dir_path)
        all_formats["MARKDOWN_NA_FORMATS"].update(formats["markdown"])
        all_formats["CSV_NA_FORMATS"].update(formats["csv"])
        all_formats["TXT_NA_FORMATS"].update(formats["txt"])
    
    print("N/A formats in different report types:\n")
    for format_type, format_set in all_formats.items():
        if format_set:
            print(f"{format_type} report N/A formats:")
            for format_str in format_set:
                print(f"  \"{format_str}\"")
            print()
            
    # Check retry mechanism
    print("Analyzing grade extraction retry mechanism...")
    print()
    
    retry_info = check_retry_mechanism()
    print(f"Dedicated retry extraction function exists: {retry_info.get('has_retry_logic', False)}")
    print(f"Retry logic in grade_essay function: {retry_info.get('has_retry_logic', False)}")
    print(f"Dedicated logging for failed extractions: {retry_info.get('has_logging', False)}")
    print(f"N/A handling in Boswell Quotient calculation:")
    print(f"  - Special handling for N/A grades: {retry_info.get('special_na_handling', False)}")
    
    # Write detailed analysis to file
    with open("na_grade_analysis.md", "w") as f:
        f.write("# N/A Grade Handling Analysis\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Total grades analyzed**: {total_grades}\n")
        f.write(f"- **N/A grades found**: {total_na} ({na_percentage:.2f}%)\n")
        f.write(f"- **Result directories with N/A grades**: {na_dirs} out of {len(result_dirs)}\n")
        f.write(f"- **Models affected by N/A grades**: {len(all_affected_models)}\n\n")
        
        f.write("## Details\n\n")
        f.write("### Grade Extraction Methods\n\n")
        f.write("The system employs three grade extraction methods:\n\n")
        f.write("1. **Pattern Matching**: Uses regex patterns to extract grades from standard formats\n")
        f.write("2. **Contextual Analysis**: Examines text near grading keywords\n")
        f.write("3. **Semantic Descriptor Matching**: Analyzes descriptive language to infer grades\n\n")
        
        f.write("These methods work in sequence, with each serving as a fallback for the previous one.\n\n")
        
        f.write("### Impact on Boswell Quotient\n\n")
        for (actual, total), count in component_combinations.items():
            f.write(f"- **{actual}/{total} components**: {count} instances\n")
        f.write("\n")
        
        f.write("### N/A Display Formats\n\n")
        for format_type, format_set in all_formats.items():
            if format_set:
                f.write(f"**{format_type}**:\n")
                for format_str in format_set:
                    f.write(f"- `{format_str}`\n")
                f.write("\n")
        
    print("\n" + "=" * 70)
    print("SUMMARY OF N/A GRADE HANDLING")
    print("=" * 70 + "\n")
    
    print(f"N/A Grade Frequency: {total_na} / {total_grades} grades ({na_percentage:.2f}%)")
    print()
    print("RECOMMENDATIONS:")
    print()
    print("Detailed analysis written to na_grade_analysis.md")

if __name__ == "__main__":
    main()