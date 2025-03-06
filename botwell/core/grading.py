"""
Grading functionality and utilities for Boswell tests.
"""

import re
from typing import Dict, Any
from statistics import median
import time
import os
from botwell.utils.model_standardization import standardize_model_name
from collections import Counter

def extract_grade(feedback: str, model_name: str = "Unknown") -> str:
    """Extract letter grade from grading feedback."""
    # First try to match the exact format we requested
    match = re.search(r"Grade:\s*([A-C][+-]?)", feedback)
    if match:
        return match.group(1)
    
    # Fall back to more flexible patterns if the exact format isn't found
    # Look for letter grades in various contexts
    # Extended set of patterns to capture more grade formats
    grade_patterns = [
        # Original patterns
        r"([A-C][+-]?)\s*grade",  # "A+ grade" or "B- grade"
        r"grade\s*(?:of|is|:)?\s*([A-C][+-]?)",  # "grade of A" or "grade: B+"
        r"grade\s*[\"']([A-C][+-]?)[\"']",  # grade "A-" or grade 'B'
        r"([A-C][+-]?)$",  # Just the grade at the end of a line
        r"final\s*grade\s*[:\-=]\s*([A-C][+-]?)",  # "final grade: A+"
        r"grade\s*for\s*this\s*essay\s*[:\-=]\s*([A-C][+-]?)",  # "grade for this essay: B"
        r"([A-C][+-]?)\s*grade\s*for\s*this\s*essay",  # "A grade for this essay"
        r"assign\s*a\s*grade\s*of\s*([A-C][+-]?)",  # "assign a grade of B+"
        r"assign\s*([A-C][+-]?)",  # "assign B+"
        r"grade\s*assignment\s*[:\-=]\s*([A-C][+-]?)",  # "grade assignment: A-"
        r"overall\s*grade\s*[:\-=]\s*([A-C][+-]?)",  # "overall grade: C+"
        
        # Enhanced patterns for better coverage
        r"Grade\s*([A-C][+-]?)\s*$",  # For cases ending with just "Grade A" with no punctuation
        r"([A-C][+-]?)\s*grade\s*$",  # For cases ending with "A grade" 
        r"grade[^A-Za-z0-9]*([A-C][+-]?)[^A-Za-z0-9]*$",  # For "grade: [A]" at the end
        r"grade[^:]*?([A-C][+-]?)",  # More flexible pattern without colon
        r"^\s*([A-C][+-]?)\s*$",  # For cases where a line contains just the grade
        r"evaluation.*?([A-C][+-]?)",  # Looking for grades near evaluation-related words
        r"assessment.*?([A-C][+-]?)",  # Looking for grades near assessment-related words
        r"([A-C][+-]?)\s*(?:overall|rating|score)",  # For "A- overall" or similar
        
        # Conclusion section patterns
        r"(?:in\s*conclusion|to\s*conclude|overall|summary|finally).*?([A-C][+-]?)",
        r"([A-C][+-]?)\s*(?:is\s*appropriate|would\s*be\s*fair|seems\s*fair|is\s*a\s*fair\s*assessment)",
        r"(?:deserve|earned|warrants|merits).*?([A-C][+-]?)",
        r"(?:final|overall|appropriate)\s*grade\s*(?:is|would\s*be).*?([A-C][+-]?)"
    ]
    
    # Try each pattern in order of specificity
    for pattern in sorted(grade_patterns, key=len, reverse=True):
        for line in feedback.split('\n'):
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1).upper()  # Normalize to uppercase
    
    # If we've reached here, no grade was found
    print(f"  Warning: Could not extract grade from feedback. Using N/A.")
    # Standardize model name when logging extraction failures
    log_failed_extraction(standardize_model_name(model_name), feedback)
    
    # Special multi-pass attempt to recover grade when primary patterns fail
    # This is particularly helpful for cases with "Grade:" but no direct grade following
    if "Grade:" in feedback or "grade:" in feedback:
        # Find the position of the last "Grade:" mention
        grade_idx = max(feedback.lower().rfind("grade:"), feedback.lower().rfind("grade :"))
        if grade_idx != -1:
            # Check what comes after "Grade:" (50 chars should be enough to find a grade)
            after_grade = feedback[grade_idx:grade_idx+50]
            
            # Look for any letter grade pattern after "Grade:"
            match = re.search(r'[A-C][+-]?', after_grade, re.IGNORECASE)
            if match:
                print(f"  Recovered grade using multi-pass strategy: {match.group(0).upper()}")
                return match.group(0).upper()
    
    # As a last resort, look for grade descriptors to infer the grade
    grade_descriptors = {
        "A+": ["exceptional", "outstanding", "excellent", "superb", "flawless", "perfect"],
        "A": ["excellent", "superior", "exceptional", "outstanding", "remarkable"],
        "A-": ["very good", "strong", "impressive", "solid", "thorough"],
        "B+": ["good", "above average", "commendable", "solid", "effective"],
        "B": ["good", "competent", "satisfactory", "acceptable", "adequate"],
        "B-": ["satisfactory", "acceptable", "adequate", "sufficient", "passable"],
        "C+": ["fair", "average", "passable", "moderate", "mediocre"],
        "C": ["average", "passable", "fair", "mediocre", "basic"],
        "C-": ["below average", "minimal", "basic", "weak", "limited"]
    }
    
    # Implement semantic descriptor approach
    feedback_lower = feedback.lower()
    grade_scores = {grade: 0 for grade in grade_descriptors}
    
    for grade, descriptors in grade_descriptors.items():
        for descriptor in descriptors:
            count = feedback_lower.count(descriptor)
            grade_scores[grade] += count
    
    # Find the grade with the highest descriptor count
    max_score = max(grade_scores.values())
    if max_score > 0:
        # Get all grades with the max score
        best_grades = [grade for grade, score in grade_scores.items() if score == max_score]
        best_grade = best_grades[0]  # Default to first if multiple
        
        print(f"  Recovered grade {best_grade} using semantic descriptor matching")
        return best_grade
    
    return "N/A"  # Grade not found

def log_failed_extraction(model_name: str, feedback: str, log_sample: bool = True) -> None:
    """Log failed grade extractions for analysis."""
    import time
    
    log_dir = "logs/grade_extraction"
    os.makedirs(log_dir, exist_ok=True) 
    
    # Standardize the model name
    standard_model_name = standardize_model_name(model_name)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{log_dir}/{timestamp}_{standard_model_name}_failed_extraction.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Model: {model_name}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("Feedback content:\n")
        
        # Optionally truncate very long feedback to prevent excessive log files
        if log_sample and len(feedback) > 10000:
            feedback = feedback[:5000] + "\n...\n" + feedback[-5000:]
        f.write(feedback)

def grade_to_numeric(grade: str) -> float:
    """Convert letter grade to numeric value using university standard."""
    grade_map = {
        "A+": 4.25, "A": 4.0, "A-": 3.75, 
        "B+": 3.25, "B": 3.0, "B-": 2.75,
        "C+": 2.25, "C": 2.0, "C-": 1.75,
        "D+": 1.25, "D": 1.0, "D-": 0.75,
        "F": 0.0,
        "N/A": 0.0
    }
    return grade_map.get(grade, 0.0)


def grade_to_percentage(numeric_grade: float) -> int:
    """Convert numeric grade to percentage (0-100 scale).
    
    Uses the following scale:
    A+ (4.25) -> 97-100
    A  (4.0) -> 93-96
    A- (3.75) -> 90-92
    B+ (3.25) -> 87-89
    B  (3.0) -> 83-86
    B- (2.75) -> 80-82
    C+ (2.25) -> 77-79
    C  (2.0) -> 73-76
    C- (1.75) -> 70-72
    D+ (1.25) -> 67-69
    D  (1.0) -> 63-66
    D- (0.75) -> 60-62
    F  (0.0) -> 0-59
    """
    if numeric_grade >= 4.25:  # A+
        return 100
    elif numeric_grade >= 4.0:  # A
        return 93 + int((numeric_grade - 4.0) / 0.25 * 4)
    elif numeric_grade >= 3.75:  # A- (3.75)
        return 90 + int((numeric_grade - 3.75) / 0.25 * 3)
    elif numeric_grade >= 3.25:  # B+ (3.25)
        return 87 + int((numeric_grade - 3.25) / 0.25 * 3)
    elif numeric_grade >= 3.0:  # B
        return 83 + int((numeric_grade - 3.0) / 0.25 * 4)
    elif numeric_grade >= 2.75:  # B- (2.75)
        return 80 + int((numeric_grade - 2.75) / 0.25 * 3)
    elif numeric_grade >= 2.25:  # C+ (2.25)
        return 77 + int((numeric_grade - 2.25) / 0.25 * 3)
    elif numeric_grade >= 2.0:  # C
        return 73 + int((numeric_grade - 2.0) / 0.25 * 4)
    elif numeric_grade >= 1.75:  # C- (1.75)
        return 70 + int((numeric_grade - 1.75) / 0.25 * 3)
    elif numeric_grade >= 1.25:  # D+ (1.25)
        return 67 + int((numeric_grade - 1.25) / 0.25 * 3)
    elif numeric_grade >= 1.0:  # D
        return 63 + int((numeric_grade - 1.0) / 0.25 * 4)
    elif numeric_grade >= 0.75:  # D- (0.75)
        return 60 + int((numeric_grade - 0.75) / 0.25 * 3)
    else:  # F
        # Scale F grade from 0 to 59 based on the numeric value
        return max(0, int(numeric_grade * 59 / 0.75))


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
    
    # Standardize all model names in the input list
    standardized_models = [standardize_model_name(model) for model in models]
    
    # Process using standardized names
    for grader in standardized_models:
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
    for grader, stats in grader_grades.items():
        all_numeric_grades.extend(stats["numeric_grades"])
    
    # Handle the case where no grades were collected (all N/A)
    if not all_numeric_grades:
        print("Warning: No valid grades found. Using default values for bias analysis.")
        overall_median = 3.0  # Default to B grade
        overall_mean = 3.0
    else:
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