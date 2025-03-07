#!/usr/bin/env python3
"""
Simple test script to verify the composite grade extraction functionality.
"""

from botwell.core.grading import extract_grade

# Sample feedback texts that might include composite grades
test_cases = [
    # Exact format examples
    ("The essay demonstrates good organization. Grade: A-/B+", "A-/B+"),
    ("Overall, the essay needs improvement. Grade: B+/B", "B+/B"),
    ("The analysis is inconsistent. Grade: B/B-", "B/B-"),
    ("The essay shows excellent work. Grade: A/A-", "A/A-"),
    
    # Variations in format
    ("I would give this essay an A-/B+ grade.", "A-/B+"),
    ("This essay deserves a grade of B+/B.", "B+/B"),
    ("The grade for this essay is B/B-.", "B/B-"),
    ("Final grade: A/A-", "A/A-"),
    
    # With additional context
    ("""
    The essay presents a well-structured argument, but lacks depth in analysis.
    The introduction is strong, but the conclusion needs more development.
    
    Grade: A-/B+
    
    I hope this feedback is helpful for improvement.
    """, "A-/B+"),
    
    # Test the multi-pass recovery
    ("Grade: This essay is between two grades, so I'll give it an A-/B+", "A-/B+"),
    ("Grade:    B+/B   ", "B+/B")
]

# Run the tests
print("Testing composite grade extraction:")
print("-" * 50)

for i, (feedback, expected) in enumerate(test_cases, 1):
    result = extract_grade(feedback)
    success = result == expected
    print(f"Test {i}: {'✓' if success else '✗'} Got: {result}, Expected: {expected}")
    if not success:
        print(f"  Feedback: {feedback[:50]}..." if len(feedback) > 50 else f"  Feedback: {feedback}")

print("-" * 50)