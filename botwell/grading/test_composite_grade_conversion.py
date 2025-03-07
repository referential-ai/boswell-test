#!/usr/bin/env python
"""
Test the conversion of composite letter grades to numeric values.
"""
import sys
import os

# Add the project root to the path so we can import from botwell
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botwell.core.grading import grade_to_numeric

def test_composite_grade_conversion():
    """Test the conversion of composite grades to numeric values."""
    test_cases = [
        # Regular grades
        ("A+", 4.25),
        ("A", 4.0),
        ("A-", 3.75),
        ("B+", 3.25),
        ("B", 3.0),
        ("B-", 2.75),
        ("C+", 2.25),
        ("C", 2.0),
        ("C-", 1.75),
        
        # Composite grades
        ("A/A-", 3.875),  # (4.0 + 3.75) / 2
        ("A-/B+", 3.5),   # (3.75 + 3.25) / 2
        ("B+/B", 3.125),  # (3.25 + 3.0) / 2
        ("B/B-", 2.875),  # (3.0 + 2.75) / 2
        ("B-/C+", 2.5),   # (2.75 + 2.25) / 2
        ("C+/C", 2.125),  # (2.25 + 2.0) / 2
        
        # Edge cases
        ("N/A", 0.0),
        ("F/D-", 0.375),  # (0.0 + 0.75) / 2
    ]
    
    print("Testing composite grade conversion:")
    for grade, expected in test_cases:
        actual = grade_to_numeric(grade)
        status = "✓" if abs(actual - expected) < 0.001 else "✗"
        print(f"{status} {grade} -> {actual:.3f} (expected {expected:.3f})")

if __name__ == "__main__":
    test_composite_grade_conversion()