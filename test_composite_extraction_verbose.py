#!/usr/bin/env python3
"""
Verbose test script for composite grade extraction with detailed debugging.
"""

import re
import sys

# Create a copy of the problematic cases with complete feedback content
test_cases = [
    ("This essay deserves a grade of B+/B.", "B+/B"),
    ("The grade for this essay is B/B-.", "B/B-"),
    ("Grade: This essay is between two grades, so I'll give it an A-/B+", "A-/B+"),
]

# Paste our implementation directly to enable step-by-step debugging
def extract_grade_debug(feedback: str) -> tuple:
    """Extract letter grade from grading feedback with debug info."""
    debug_info = []
    
    # First try to match the exact format we requested
    match = re.search(r"Grade:\s*([A-C][+-]?(?:/[A-C][+-]?)?)", feedback)
    if match:
        debug_info.append(f"Matched with primary 'Grade:' pattern: {match.group(1)}")
        return (match.group(1), debug_info)
    
    debug_info.append("Primary pattern did not match, trying grade_patterns...")
    
    # Fake the grade_patterns just focusing on main composite ones
    grade_patterns = [
        r"([A-C][+-]?(?:/[A-C][+-]?)?)\s*grade",
        r"grade\s*(?:of|is|:)?\s*([A-C][+-]?(?:/[A-C][+-]?)?)",
    ]
    
    # Try each pattern in order
    for pattern in grade_patterns:
        for line in feedback.split('\n'):
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                debug_info.append(f"Matched with pattern '{pattern}': {match.group(1)}")
                return (match.group(1).upper(), debug_info)
    
    debug_info.append("Grade patterns did not match, trying specialized patterns...")
    
    # Try specialized pattern matching for problematic cases
    specialized_patterns = [
        # Case 1: "deserves a grade of X"
        (r'deserves\s+a\s+grade\s+of\s+([A-C][+-]?/[A-C][+-]?)', "deserves a grade pattern"),
        
        # Case 2: "grade for this essay is X"
        (r'grade\s+for\s+this\s+essay\s+is\s+([A-C][+-]?/[A-C][+-]?)', "essay grade pattern"),
        
        # Case 3: "between two grades... give it an X"
        (r'between\s+two\s+grades.*?give\s+it\s+an?\s+([A-C][+-]?/[A-C][+-]?)', "between grades pattern"),
    ]
    
    for pattern, desc in specialized_patterns:
        match = re.search(pattern, feedback, re.IGNORECASE)
        if match:
            debug_info.append(f"Matched with {desc}: {match.group(1)}")
            return (match.group(1).upper(), debug_info)
    
    debug_info.append("Specialized patterns did not match, trying multi-pass...")
    
    # Generic Grade: pattern with more flexible matching
    if "Grade:" in feedback or "grade:" in feedback or "GRADE:" in feedback:
        debug_info.append("Found 'Grade:' text, trying multi-pass extraction...")
        for grade_format in ["Grade:", "grade:", "GRADE:"]:
            if grade_format in feedback:
                # Find the position of the "Grade:" mention
                grade_idx = feedback.rfind(grade_format)
                if grade_idx != -1:
                    # Get everything after the "Grade:" 
                    after_grade = feedback[grade_idx+len(grade_format):]
                    debug_info.append(f"Looking after '{grade_format}': '{after_grade[:50]}...'")
                    
                    # Look for composite grades first, then regular grades
                    match = re.search(r'([A-C][+-]?/[A-C][+-]?)', after_grade, re.IGNORECASE)
                    if match:
                        debug_info.append(f"Found composite grade in multi-pass: {match.group(1)}")
                        return (match.group(1).upper(), debug_info)
                    
                    # If no composite grade, try for regular grade
                    match = re.search(r'([A-C][+-]?)', after_grade, re.IGNORECASE)
                    if match:
                        debug_info.append(f"Found single grade in multi-pass: {match.group(0)}")
                        return (match.group(0).upper(), debug_info)
    
    return ("N/A", debug_info)

print("VERBOSE TESTING OF COMPOSITE GRADE EXTRACTION")
print("=" * 70)

for i, (feedback, expected) in enumerate(test_cases, 1):
    print(f"\nTEST CASE {i}: {feedback}")
    print(f"Expected grade: {expected}")
    
    grade, debug_info = extract_grade_debug(feedback)
    print(f"Extracted grade: {grade} " + ("✓" if grade == expected else "✗"))
    
    print("\nDebug information:")
    for j, info in enumerate(debug_info, 1):
        print(f"{j}. {info}")
    
    print("-" * 70)

# Test the problematic patterns directly
print("\nDIRECT PATTERN MATCHING TEST")
print("=" * 70)

for i, (feedback, expected) in enumerate(test_cases, 1):
    print(f"\nTest Case {i}: {feedback}")
    
    # Test pattern 1
    pattern = r'deserves\s+a\s+grade\s+of\s+([A-C][+-]?/[A-C][+-]?)'
    match = re.search(pattern, feedback, re.IGNORECASE)
    print(f"Pattern 'deserves a grade of': {'✓ ' + match.group(1) if match else '✗ No match'}")
    
    # Test pattern 2
    pattern = r'grade\s+for\s+this\s+essay\s+is\s+([A-C][+-]?/[A-C][+-]?)'
    match = re.search(pattern, feedback, re.IGNORECASE)
    print(f"Pattern 'grade for this essay is': {'✓ ' + match.group(1) if match else '✗ No match'}")
    
    # Test pattern 3
    pattern = r'between\s+two\s+grades.*?give\s+it\s+an?\s+([A-C][+-]?/[A-C][+-]?)'
    match = re.search(pattern, feedback, re.IGNORECASE)
    print(f"Pattern 'between grades...give it an': {'✓ ' + match.group(1) if match else '✗ No match'}")