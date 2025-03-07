"""
Unit tests for the median_of_list function.
"""

import unittest
from botwell.utils import median_of_list

class TestMedianOfList(unittest.TestCase):
    """Test cases for the median_of_list function."""

    def test_odd_length_list(self):
        """Test that median_of_list returns the middle value for odd-length lists."""
        # Example from Peter's email
        result = median_of_list([2, 3, 4, 5, 6])
        self.assertEqual(result, 4.0)
        
        # Additional test case with unsorted list
        result = median_of_list([5, 2, 6, 3, 4])
        self.assertEqual(result, 4.0)
        
        # Test with a different odd-length list
        result = median_of_list([1, 3, 5, 7, 9, 11, 13])
        self.assertEqual(result, 7.0)

    def test_even_length_list(self):
        """Test that median_of_list returns the average of two middle values for even-length lists."""
        # Example from Peter's email
        result = median_of_list([1.2, 5.4, 7.5, 9.2, 6.3, 6.5])
        self.assertEqual(result, 6.4)
        
        # Additional test case with unsorted list
        result = median_of_list([9.2, 1.2, 6.5, 7.5, 6.3, 5.4])
        self.assertEqual(result, 6.4)
        
        # Test with a different even-length list
        result = median_of_list([2, 4, 6, 8])
        self.assertEqual(result, 5.0)

    def test_empty_list(self):
        """Test that median_of_list returns 0.0 for empty lists."""
        result = median_of_list([])
        self.assertEqual(result, 0.0)

    def test_single_element_list(self):
        """Test that median_of_list returns the element for single-element lists."""
        result = median_of_list([5])
        self.assertEqual(result, 5.0)

    def test_two_element_list(self):
        """Test that median_of_list returns the average for two-element lists."""
        result = median_of_list([1, 3])
        self.assertEqual(result, 2.0)

if __name__ == '__main__':
    unittest.main()