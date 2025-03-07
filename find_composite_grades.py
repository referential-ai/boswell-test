#!/usr/bin/env python3
"""
Script to scan through grade files and find examples of composite grades.
"""

import os
import json
import argparse
import glob
from typing import Dict, List, Any, Tuple

def scan_for_composite_grades(results_dir: str) -> List[Dict[str, Any]]:
    """
    Scan through all grade files in the specified results directory
    and identify any composite grades (scores that fall between standard grade points).
    
    Returns:
        List of found composite grade examples with details
    """
    composite_examples = []
    standard_grades = {
        4.25: "A+", 4.0: "A", 3.75: "A-",
        3.25: "B+", 3.0: "B", 2.75: "B-",
        2.25: "C+", 2.0: "C", 1.75: "C-",
        1.25: "D+", 1.0: "D", 0.75: "D-",
        0.0: "F"
    }
    
    # Grades directory path
    grades_dir = os.path.join(results_dir, "grades")
    
    if not os.path.exists(grades_dir):
        print(f"No grades directory found at {grades_dir}")
        return []
    
    # List all author directories
    for author_dir in os.listdir(grades_dir):
        author_path = os.path.join(grades_dir, author_dir)
        if not os.path.isdir(author_path):
            continue
        
        # Process all grade files for this author
        for grader_file in os.listdir(author_path):
            if not grader_file.endswith(".json"):
                continue
            
            grade_file_path = os.path.join(author_path, grader_file)
            grader_name = os.path.splitext(grader_file)[0]
            
            try:
                with open(grade_file_path, 'r') as f:
                    grade_data = json.load(f)
                
                # Check if numeric_grade is a non-standard value
                numeric_grade = grade_data.get("numeric_grade")
                if numeric_grade is not None and numeric_grade not in standard_grades:
                    # This is a composite grade
                    composite_examples.append({
                        "author": author_dir,
                        "grader": grader_name,
                        "grade": grade_data.get("grade"),
                        "numeric_grade": numeric_grade,
                        "file_path": grade_file_path
                    })
            except Exception as e:
                print(f"Error processing {grade_file_path}: {e}")
    
    return composite_examples

def show_composite_grade_details(composite_examples: List[Dict[str, Any]]) -> None:
    """
    Display detailed information about found composite grades.
    """
    if not composite_examples:
        print("No composite grades found.")
        return
    
    print(f"\nFound {len(composite_examples)} composite grades:\n")
    print(f"{'AUTHOR':<20} {'GRADER':<20} {'GRADE':<5} {'NUMERIC':<8} {'FILE PATH'}")
    print("-" * 80)
    
    for example in composite_examples:
        print(f"{example['author']:<20} {example['grader']:<20} {example['grade']:<5} {example['numeric_grade']:<8.2f} {example['file_path']}")
    
    print("\nThese grades fall between standard grade points and would be displayed as composite grades.")
    print("For example, 3.5 would be displayed as 'A-/B+' in reports.")

def main():
    parser = argparse.ArgumentParser(description="Find composite grades in test results")
    parser.add_argument("results_dir", nargs="?", help="Results directory to scan (defaults to most recent)")
    args = parser.parse_args()
    
    # If no directory specified, use most recent results
    if not args.results_dir:
        results_dirs = sorted(glob.glob("results/*-pol_sci_1"), reverse=True)
        if not results_dirs:
            print("No results directories found")
            return
        results_dir = results_dirs[0]
        print(f"Using most recent results directory: {results_dir}")
    else:
        results_dir = args.results_dir
    
    # Scan for composite grades
    composite_examples = scan_for_composite_grades(results_dir)
    
    # Display results
    show_composite_grade_details(composite_examples)

if __name__ == "__main__":
    main()