#!/usr/bin/env python3
"""
Grade Extraction Improvements

This module demonstrates enhanced pattern matching for grade extraction
based on analysis of failed extractions in the Boswell system.
"""

import os
import re
from typing import Dict, Any, List, Optional


def extract_grade_improved(feedback: str, model_name: str = "Unknown") -> str:
    """
    Enhanced version of extract_grade with improved pattern matching.
    
    This version adds:
    1. More comprehensive regex patterns
    2. Multi-pass extraction with different strategies
    3. Contextual analysis for borderline cases
    
    Returns:
        The extracted letter grade or "N/A" if no grade is found
    """
    # First strategy: Try the exact format we requested (unchanged from original)
    match = re.search(r"Grade:\s*([A-C][+-]?)", feedback)
    if match:
        return match.group(1)
    
    # Second strategy: Enhanced pattern set with additional patterns derived from failures
    enhanced_grade_patterns = [
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
        
        # NEW enhanced patterns from analysis of failed extractions
        r"Grade\s*([A-C][+-]?)\s*$",  # For cases ending with just "Grade A" with no punctuation
        r"([A-C][+-]?)\s*grade\s*$",  # For cases ending with "A grade" 
        r"grade[^A-Za-z0-9]*([A-C][+-]?)[^A-Za-z0-9]*$",  # For "grade: [A]" at the end
        r"grade[^:]*?([A-C][+-]?)",  # More flexible pattern without colon
        r"^\s*([A-C][+-]?)\s*$",  # For cases where a line contains just the grade
        r"evaluation.*?([A-C][+-]?)",  # Looking for grades near evaluation-related words
        r"assessment.*?([A-C][+-]?)",  # Looking for grades near assessment-related words
        r"([A-C][+-]?)\s*(?:overall|rating|score)",  # For "A- overall" or similar
    ]
    
    # Try each pattern in order of specificity
    for pattern in sorted(enhanced_grade_patterns, key=len, reverse=True):
        for line in feedback.split('\n'):
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1).upper()  # Normalize to uppercase
    
    # Third strategy: Context-based extraction for borderline cases
    # This looks for letter grades in the last few lines, which often contain grades
    lines = feedback.split('\n')
    last_lines = lines[-5:] if len(lines) >= 5 else lines  # Check the last 5 lines
    for line in last_lines:
        # Look for isolated letter grades in contexts that suggest a conclusion
        potential_grades = re.findall(r'(?:^|\s)([A-C][+-]?)(?:\s|$|\.|\,|\:)', line)
        if potential_grades:
            # If we find a potential grade in the conclusion section, use it
            return potential_grades[0].upper()
    
    # Fourth strategy: Multi-pass for feedback with "Grade:" but no extracted grade
    # This happens when models write something like "Grade:" but don't follow with a letter
    if "Grade:" in feedback or "Grade :" in feedback:
        # Find the position of the last "Grade:" mention
        grade_idx = max(feedback.rfind("Grade:"), feedback.rfind("Grade :"))
        if grade_idx != -1:
            # Check what comes after "Grade:" (50 chars should be enough to find a grade)
            after_grade = feedback[grade_idx:grade_idx+50]
            
            # Look for even basic letter patterns after "Grade:"
            letter_match = re.search(r'[A-C][+-]?', after_grade)
            if letter_match:
                return letter_match.group(0).upper()
    
    # If we've reached here, no grade was found using any strategy
    print(f"  Warning: Could not extract grade from feedback using improved algorithm. Using N/A.")
    # log_failed_extraction is called in the original function
    return "N/A"  # Grade not found


def analyze_log_files(logs_dir="logs/grade_extraction"):
    """
    Analyze all failed extraction log files with both algorithms.
    
    Returns:
        List of comparison results
    """
    print(f"Looking for log files in: {logs_dir}")
    
    results = []
    
    if not os.path.exists(logs_dir):
        print(f"Error: Directory {logs_dir} does not exist")
        return results
        
    log_files = [f for f in os.listdir(logs_dir) if f.endswith("_failed_extraction.txt")]
    
    if not log_files:
        print(f"No log files found in {logs_dir}")
        return results
        
    print(f"Found {len(log_files)} log files")
    
    for filename in log_files:
        filepath = os.path.join(logs_dir, filename)
        
        # Extract model name from filename
        model_match = re.search(r'(\d+)_(.+)_failed_extraction\.txt', filename)
        if not model_match:
            print(f"Skipping {filename} - doesn't match expected format")
            continue
            
        model_name = model_match.group(2)
        print(f"Processing: {model_name}")
        
        with open(filepath, 'r') as f:
            try:
                content = f.read()
                
                # Skip header lines to get to the actual feedback
                feedback_start = content.find("Feedback content:")
                if feedback_start >= 0:
                    feedback = content[feedback_start + len("Feedback content:"):]
                    
                    # Original extraction (simulated)
                    original_grade = "N/A"  # This was already N/A since it's from a failed extraction log
                    
                    # Improved extraction
                    improved_grade = extract_grade_improved(feedback, model_name)
                    
                    results.append({
                        "model": model_name,
                        "original_grade": original_grade,
                        "improved_grade": improved_grade,
                        "improvement": improved_grade != "N/A"
                    })
                    
                    print(f"  Original: {original_grade}, Improved: {improved_grade}")
                else:
                    print(f"  Feedback content not found in {filename}")
            except Exception as e:
                print(f"  Error processing {filename}: {e}")
    
    return results


def run_enhancement_analysis():
    """
    Run a comparison analysis of the original vs. improved extraction algorithms.
    
    This can be used to validate the improvements before integrating them.
    """
    print("=" * 70)
    print("GRADE EXTRACTION ALGORITHM COMPARISON")
    print("=" * 70)
    
    results = analyze_log_files()
    
    if not results:
        print("\nNo results to analyze")
        return
    
    improved_count = sum(1 for r in results if r["improvement"])
    total_count = len(results)
    
    print("\nSUMMARY:")
    print(f"Analyzed {total_count} failed extraction files")
    print(f"Improvements achieved: {improved_count}/{total_count} ({improved_count/total_count*100:.1f}%)")
    
    print("\nDetailed results:")
    for r in results:
        improvement_text = "✓ IMPROVED" if r["improvement"] else "✗ UNCHANGED"
        print(f"- {r['model']}: {r['original_grade']} -> {r['improved_grade']} {improvement_text}")
    
    print("\nRecommended Code Changes:")
    print("""
    To incorporate these improvements into the codebase:
    
    1. Add these enhanced patterns to the grade_patterns list in grading.py:
       ```python
       # Enhanced patterns from analysis
       r"Grade\\s*([A-C][+-]?)\\s*$",  # For cases ending with just "Grade A" with no punctuation
       r"([A-C][+-]?)\\s*grade\\s*$",  # For cases ending with "A grade"
       r"grade[^A-Za-z0-9]*([A-C][+-]?)[^A-Za-z0-9]*$",  # For "grade: [A]" at the end
       r"grade[^:]*?([A-C][+-]?)",  # More flexible pattern without colon
       r"^\\s*([A-C][+-]?)\\s*$",  # For cases where a line contains just the grade
       r"evaluation.*?([A-C][+-]?)",  # Looking for grades near evaluation-related words
       r"assessment.*?([A-C][+-]?)",  # Looking for grades near assessment-related words
       r"([A-C][+-]?)\\s*(?:overall|rating|score)"  # For "A- overall" or similar
       ```
    
    2. Consider adding the multi-pass strategy for cases with "Grade:" but no extracted grade
    
    3. Implement the contextual analysis for high-confidence patterns in conclusion sections
    """)


if __name__ == "__main__":
    run_enhancement_analysis()