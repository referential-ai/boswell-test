#!/usr/bin/env python3
"""
Debug script to understand pattern matching issues with composite grades.
"""

import re
from botwell.core.grading import extract_grade

# The problematic test cases
test_cases = [
    # These are the ones that failed
    ("This essay deserves a grade of B+/B.", "B+/B"),
    ("The grade for this essay is B/B-.", "B/B-"),
    ("Grade: This essay is between two grades, so I'll give it an A-/B+", "A-/B+"),
]

# Define the pattern for composite grades
grade_pattern = r'[A-C][+-]?'
composite_pattern = f'({grade_pattern}(?:/{grade_pattern})?)'

# Define individual patterns to test
patterns_to_test = [
    f"grade\\s*(?:of|is|:)?\\s*{composite_pattern}",
    f"deserves\\s+a\\s+grade\\s+of\\s+({grade_pattern}(?:/{grade_pattern})?)",
    f"grade\\s+for\\s+this\\s+essay\\s+is\\s+({grade_pattern}(?:/{grade_pattern})?)",
    f"Grade:\\s*.*?({grade_pattern}(?:/{grade_pattern})?)",
    f"between\\s+two\\s+grades.*?({grade_pattern}(?:/{grade_pattern})?)",
    f"give\\s+it\\s+an?\\s+({grade_pattern}(?:/{grade_pattern})?)",
]

# Test each problematic case with each pattern
print("Debugging Pattern Matching for Composite Grades")
print("=" * 60)

for i, (feedback, expected) in enumerate(test_cases, 1):
    print(f"\nTest Case {i}: {feedback}")
    print(f"Expected: {expected}")
    print("Current result from extract_grade(): " + extract_grade(feedback))
    print("-" * 60)
    print("Testing individual patterns:")
    
    for pattern in patterns_to_test:
        match = re.search(pattern, feedback, re.IGNORECASE)
        if match:
            print(f"✓ Pattern '{pattern}' matches: {match.group(1)}")
        else:
            print(f"✗ Pattern '{pattern}' does not match")
    
    print("-" * 60)

# Custom fix attempt
def custom_extract_from_problematic_cases(feedback):
    """Try to extract composite grades from problematic text patterns."""
    
    # Case 1: "deserves a grade of X"
    match = re.search(r'deserves\s+a\s+grade\s+of\s+([A-C][+-]?/[A-C][+-]?)', feedback, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    # Case 2: "grade for this essay is X"
    match = re.search(r'grade\s+for\s+this\s+essay\s+is\s+([A-C][+-]?/[A-C][+-]?)', feedback, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    # Case 3: "between two grades... give it an X"
    match = re.search(r'between\s+two\s+grades.*?give\s+it\s+an?\s+([A-C][+-]?/[A-C][+-]?)', feedback, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    return "NOT FOUND"

print("\nTesting custom extraction function:")
for i, (feedback, expected) in enumerate(test_cases, 1):
    result = custom_extract_from_problematic_cases(feedback)
    print(f"Test {i}: {result} (Expected: {expected}) - {'✓' if result == expected else '✗'}")