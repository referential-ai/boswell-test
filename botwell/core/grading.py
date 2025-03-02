"""
Grading functionality and utilities for Boswell tests.
"""

import re
from typing import Dict, Any
from statistics import median

def extract_grade(feedback: str) -> str:
    """Extract letter grade from grading feedback."""
    # First try to match the exact format we requested
    match = re.search(r"Grade:\s*([A-C][+-]?)", feedback)
    if match:
        return match.group(1)
    
    # Fall back to more flexible patterns if the exact format isn't found
    # Look for letter grades in various contexts
    grade_patterns = [
        r"([A-C][+-]?)\s*grade",  # "A+ grade" or "B- grade"
        r"grade\s*(?:of|is|:)?\s*([A-C][+-]?)",  # "grade of A" or "grade: B+"
        r"grade\s*[\"']([A-C][+-]?)[\"']",  # grade "A-" or grade 'B'
        r"([A-C][+-]?)$"  # Just the grade at the end of a line
    ]
    
    for pattern in grade_patterns:
        for line in feedback.split('\n'):
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1)
    
    # If we've reached here, no grade was found
    print(f"  Warning: Could not extract grade from feedback. Using N/A.")
    return "N/A"  # Grade not found


def grade_to_numeric(grade: str) -> float:
    """Convert letter grade to numeric value for calculating statistics."""
    grade_map = {
        "A+": 4.3, "A": 4.0, "A-": 3.7,
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7,
        "D+": 1.3, "D": 1.0, "D-": 0.7,
        "F": 0.0,
        "N/A": 0.0
    }
    return grade_map.get(grade, 0.0)


def grade_to_percentage(numeric_grade: float) -> int:
    """Convert numeric grade to percentage (0-100 scale).
    
    This creates a more granular scale that spreads the grades across
    a wider range for better visualization and comparison:
    
    A+ (4.3) -> 97-100
    A  (4.0) -> 93-96
    A- (3.7) -> 90-92
    B+ (3.3) -> 87-89
    B  (3.0) -> 83-86
    B- (2.7) -> 80-82
    C+ (2.3) -> 77-79
    C  (2.0) -> 73-76
    C- (1.7) -> 70-72
    D+ (1.3) -> 67-69
    D  (1.0) -> 63-66
    D- (0.7) -> 60-62
    F  (0.0) -> 0-59
    """
    if numeric_grade >= 4.3:  # A+
        return 100
    elif numeric_grade >= 4.0:  # A
        return 93 + int((numeric_grade - 4.0) / 0.3 * 4)
    elif numeric_grade >= 3.7:  # A-
        return 90 + int((numeric_grade - 3.7) / 0.3 * 3)
    elif numeric_grade >= 3.3:  # B+
        return 87 + int((numeric_grade - 3.3) / 0.4 * 3)
    elif numeric_grade >= 3.0:  # B
        return 83 + int((numeric_grade - 3.0) / 0.3 * 4)
    elif numeric_grade >= 2.7:  # B-
        return 80 + int((numeric_grade - 2.7) / 0.3 * 3)
    elif numeric_grade >= 2.3:  # C+
        return 77 + int((numeric_grade - 2.3) / 0.4 * 3)
    elif numeric_grade >= 2.0:  # C
        return 73 + int((numeric_grade - 2.0) / 0.3 * 4)
    elif numeric_grade >= 1.7:  # C-
        return 70 + int((numeric_grade - 1.7) / 0.3 * 3)
    elif numeric_grade >= 1.3:  # D+
        return 67 + int((numeric_grade - 1.3) / 0.4 * 3)
    elif numeric_grade >= 1.0:  # D
        return 63 + int((numeric_grade - 1.0) / 0.3 * 4)
    elif numeric_grade >= 0.7:  # D-
        return 60 + int((numeric_grade - 0.7) / 0.3 * 3)
    else:  # F
        # Scale F grade from 0 to 59 based on the numeric value
        return max(0, int(numeric_grade * 59 / 0.7))


def percentage_to_letter_grade(percentage: int) -> str:
    """Convert percentage (0-100 scale) to letter grade."""
    if percentage >= 97:
        return "A+"
    elif percentage >= 93:
        return "A"
    elif percentage >= 90:
        return "A-"
    elif percentage >= 87:
        return "B+"
    elif percentage >= 83:
        return "B" 
    elif percentage >= 80:
        return "B-"
    elif percentage >= 77:
        return "C+"
    elif percentage >= 73:
        return "C"
    elif percentage >= 70:
        return "C-"
    elif percentage >= 67:
        return "D+"
    elif percentage >= 63:
        return "D"
    elif percentage >= 60:
        return "D-"
    else:
        return "F"


def calculate_grading_bias(results: Dict[str, Any], models: list) -> Dict[str, Any]:
    """Calculate grading bias for each model."""
    # For each grader, collect all grades they gave
    grader_grades = {}
    for grader in models:
        if grader not in results["grades"]:
            continue
            
        # Convert letter grades to numeric for easier calculation
        numeric_grades = []
        for author, grade_info in results["grades"][grader].items():
            numeric_grades.append(grade_info["numeric_grade"])
            
        if numeric_grades:
            grader_grades[grader] = {
                "numeric_grades": numeric_grades,
                "median_given": median(numeric_grades),
                "mean_given": sum(numeric_grades) / len(numeric_grades),
                "count": len(numeric_grades)
            }
    
    # Calculate overall median of all grades
    all_numeric_grades = []
    for grader in grader_grades:
        all_numeric_grades.extend(grader_grades[grader]["numeric_grades"])
    
    overall_median = median(all_numeric_grades)
    overall_mean = sum(all_numeric_grades) / len(all_numeric_grades)
    
    # Calculate bias (difference from overall median)
    bias_results = {
        "overall_median": overall_median,
        "overall_mean": overall_mean,
        "grader_bias": {}
    }
    
    for grader, stats in grader_grades.items():
        # Positive bias means more lenient, negative means stricter
        median_bias = stats["median_given"] - overall_median
        mean_bias = stats["mean_given"] - overall_mean
        
        # Convert numeric bias back to letter grade offset
        letter_bias = "Neutral"
        if abs(median_bias) < 0.15:
            letter_bias = "Neutral"
        elif median_bias > 0:
            if median_bias > 0.6:
                letter_bias = "Very Lenient (+2 grades)"
            elif median_bias > 0.3:
                letter_bias = "Lenient (+1 grade)"
            else:
                letter_bias = "Slightly Lenient (+1/3 grade)"
        else:
            if median_bias < -0.6:
                letter_bias = "Very Strict (-2 grades)"
            elif median_bias < -0.3:
                letter_bias = "Strict (-1 grade)"
            else:
                letter_bias = "Slightly Strict (-1/3 grade)"
        
        bias_results["grader_bias"][grader] = {
            "median_given": stats["median_given"],
            "median_bias": median_bias,
            "mean_bias": mean_bias,
            "letter_bias": letter_bias,
            "count": stats["count"]
        }
    
    return bias_results