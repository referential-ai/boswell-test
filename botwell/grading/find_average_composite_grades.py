#!/usr/bin/env python3
"""
Script to find average grades that would result in composite notations.
"""

import os
import json
import glob
from statistics import mean
from typing import Dict, List, Any, Tuple

def numeric_to_composite_grade(numeric_grade: float) -> str:
    """
    Convert a numeric grade to a composite letter grade notation when applicable.
    
    Based on the function in botwell/core/grading.py
    """
    # Standard grade boundaries
    grade_boundaries = {
        4.25: "A+", 4.0: "A", 3.75: "A-",
        3.25: "B+", 3.0: "B", 2.75: "B-",
        2.25: "C+", 2.0: "C", 1.75: "C-",
        1.25: "D+", 1.0: "D", 0.75: "D-",
        0.0: "F"
    }
    
    # Check if the grade is exactly at a boundary
    if numeric_grade in grade_boundaries:
        return grade_boundaries[numeric_grade]
    
    # Find surrounding grades
    sorted_boundaries = sorted(grade_boundaries.items(), reverse=True)
    
    for i in range(len(sorted_boundaries) - 1):
        upper_bound, upper_grade = sorted_boundaries[i]
        lower_bound, lower_grade = sorted_boundaries[i + 1]
        
        # If grade falls between two standard boundaries
        if lower_bound < numeric_grade < upper_bound:
            # Calculate midpoint
            midpoint = (upper_bound + lower_bound) / 2
            
            # If the grade is very close to the midpoint (within 0.01)
            # Use composite notation
            if abs(numeric_grade - midpoint) <= 0.01:
                return f"{upper_grade}/{lower_grade}"
            
            # If closer to upper boundary
            elif numeric_grade > midpoint:
                return upper_grade
            
            # If closer to lower boundary
            else:
                return lower_grade
    
    # Default fallback for any values outside the range
    if numeric_grade > 4.25:
        return "A+"
    else:
        return "F"

def analyze_model_averages(results_dir: str) -> List[Dict[str, Any]]:
    """
    Analyze the grades for each model to find average grades that would result in composite notations.
    """
    # Load the raw grade matrix
    raw_grade_matrix_path = os.path.join(results_dir, "raw_grade_matrix.json")
    if not os.path.exists(raw_grade_matrix_path):
        print(f"No raw grade matrix found at {raw_grade_matrix_path}")
        return []
    
    with open(raw_grade_matrix_path, 'r') as f:
        raw_grades = json.load(f)
    
    # Calculate average grades for each model (as graded by others)
    model_averages = {}
    composite_examples = []
    
    # First, collect all grades received by each model
    received_grades = {}
    for grader, gradings in raw_grades.items():
        for author, grade_info in gradings.items():
            if author not in received_grades:
                received_grades[author] = []
            
            if grader != author:  # Exclude self-grades
                received_grades[author].append(grade_info["numeric_grade"])
    
    # Now calculate averages
    for model, grades in received_grades.items():
        if grades:
            avg_grade = mean(grades)
            letter_grade = numeric_to_composite_grade(avg_grade)
            
            # Check if this is a composite grade
            if "/" in letter_grade:
                composite_examples.append({
                    "model": model,
                    "numeric_average": avg_grade,
                    "composite_grade": letter_grade,
                    "grades_received": grades
                })
    
    return composite_examples

def main():
    # Use the most recent results directory
    results_dirs = sorted(glob.glob("results/*-pol_sci_1"), reverse=True)
    if not results_dirs:
        print("No results directories found")
        return
    
    results_dir = results_dirs[0]
    print(f"Using results directory: {results_dir}")
    
    # Find composite grades from model averages
    composite_examples = analyze_model_averages(results_dir)
    
    if not composite_examples:
        print("No composite grades found in model averages.")
        return
    
    print(f"\nFound {len(composite_examples)} models with composite average grades:\n")
    print(f"{'MODEL':<20} {'NUMERIC AVERAGE':<15} {'COMPOSITE GRADE':<15} {'GRADES RECEIVED'}")
    print("-" * 75)
    
    for example in composite_examples:
        grades_str = ", ".join([str(g) for g in example["grades_received"]])
        print(f"{example['model']:<20} {example['numeric_average']:<15.3f} {example['composite_grade']:<15} {grades_str}")

if __name__ == "__main__":
    main()