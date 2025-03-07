#!/usr/bin/env python3
"""
Unit tests for the composite grade notation functionality in the Boswell framework.
"""

import unittest
from botwell.core.grading import numeric_to_composite_grade

class TestCompositeGrades(unittest.TestCase):
    """Test cases for the composite grade notation functionality."""
    
    def test_standard_grade_boundaries(self):
        """Test that standard grade boundaries return single letter grades."""
        # Test exact boundary values
        self.assertEqual(numeric_to_composite_grade(4.25), "A+")
        self.assertEqual(numeric_to_composite_grade(4.0), "A")
        self.assertEqual(numeric_to_composite_grade(3.75), "A-")
        self.assertEqual(numeric_to_composite_grade(3.25), "B+")
        self.assertEqual(numeric_to_composite_grade(3.0), "B")
        self.assertEqual(numeric_to_composite_grade(2.75), "B-")
        self.assertEqual(numeric_to_composite_grade(2.25), "C+")
        self.assertEqual(numeric_to_composite_grade(2.0), "C")
        self.assertEqual(numeric_to_composite_grade(1.75), "C-")
        self.assertEqual(numeric_to_composite_grade(0.0), "F")
    
    def test_composite_grade_notation(self):
        """Test that exact midpoints between standard grades return composite notation."""
        # Midpoint between A and A- (4.0 and 3.75) = 3.875
        self.assertEqual(numeric_to_composite_grade(3.875), "A/A-")
        
        # Midpoint between A- and B+ (3.75 and 3.25) = 3.5
        self.assertEqual(numeric_to_composite_grade(3.5), "A-/B+")
        
        # Midpoint between B+ and B (3.25 and 3.0) = 3.125
        self.assertEqual(numeric_to_composite_grade(3.125), "B+/B")
        
        # Midpoint between B and B- (3.0 and 2.75) = 2.875
        self.assertEqual(numeric_to_composite_grade(2.875), "B/B-")
        
        # Midpoint between C+ and C (2.25 and 2.0) = 2.125
        self.assertEqual(numeric_to_composite_grade(2.125), "C+/C")
    
    def test_near_midpoints(self):
        """Test that values close to but not exactly at midpoints map to nearest standard grade."""
        # Slightly closer to A than to A- (3.89)
        self.assertEqual(numeric_to_composite_grade(3.89), "A")
        
        # Slightly closer to A- than to A (3.86)
        self.assertEqual(numeric_to_composite_grade(3.86), "A-")
        
        # Slightly closer to A- than to B+ (3.55)
        self.assertEqual(numeric_to_composite_grade(3.55), "A-")
        
        # Slightly closer to B+ than to A- (3.45)
        self.assertEqual(numeric_to_composite_grade(3.45), "B+")
    
    def test_composite_grade_tolerance(self):
        """Test the tolerance for determining composite grades."""
        # Just within tolerance of A/A- midpoint (3.875 ± 0.01)
        self.assertEqual(numeric_to_composite_grade(3.865), "A/A-")
        self.assertEqual(numeric_to_composite_grade(3.885), "A/A-")
        
        # Just outside tolerance
        self.assertEqual(numeric_to_composite_grade(3.864), "A-")
        self.assertEqual(numeric_to_composite_grade(3.886), "A")
    
    def test_edge_cases(self):
        """Test edge cases like values outside the normal range."""
        # Values above highest grade
        self.assertEqual(numeric_to_composite_grade(4.3), "A+")
        self.assertEqual(numeric_to_composite_grade(5.0), "A+")
        
        # Values below lowest grade
        self.assertEqual(numeric_to_composite_grade(-1.0), "F")

if __name__ == "__main__":
    unittest.main()