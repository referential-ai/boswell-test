#!/usr/bin/env python3
"""
LetterGrade.py - Utility for handling letter grade operations including median calculation
Provided by Peter L. for the Boswell Test project

This module provides functionality for converting between letter grades and numeric values,
and calculating statistical measures like median on letter grades.
"""

def medianOfList(lst):
    """Returns the middle sorted values for both even and odd n;
    for odd n, just take the middle sorted value; for even n,
    take the average of the two middle sorted values.
    
    Args:
        lst: A list of numeric values
        
    Returns:
        The median value as a float, or 0.0 if the list is empty
    """
    if not lst:
        return 0.0  # Handle empty list case
    n, srtlst = len(lst), sorted(lst)
    return (srtlst[n//2] + srtlst[(n-1)//2])/2

def getSingleGrade(g):
    """Get the base numeric value of a single letter grade.
    
    Args:
        g: Single letter grade character (a, b, c, d, f)
        
    Returns:
        The numeric value as a float: A=4.0, B=3.0, C=2.0, D=1.0, F=0.0
    """
    g = g.lower()
    if g == 'a':  
        return 4.0
    elif g == 'b':  
        return 3.0
    elif g == 'c':  
        return 2.0
    elif g == 'd':  
        return 1.0
    elif g == 'f':
        return 0.0
    return 0.0

def getPmGrade(g):
    """Get the adjustment value for a plus or minus grade modifier.
    
    Args:
        g: The modifier character (+ or -)
        
    Returns:
        Value to add/subtract: +0.25 for plus, -0.25 for minus
    """
    return 0.25 if g == '+' else -0.25 if g == '-' else 0.0

def cnvrt2Dgt(grdLst):
    """Convert a list of letter grades to numeric values, handling complex format.
    
    Supports formats like:
    - Simple: 'A+', 'B', 'C-'
    - Split: 'A/A-', 'B+/B'
    
    Args:
        grdLst: List of letter grades as strings
        
    Returns:
        List of converted numeric values
    """
    gd = []
    for g in grdLst:
        g = g.strip().lower()
        n, d, d2 = len(g), 0, 0
        
        # Basic single grade (e.g., 'a', 'b+', 'c-')
        if n >= 1:
            d += getSingleGrade(g[0])
            
        if n >= 2 and g[1] != '/':
            d += getPmGrade(g[1])
            
        # Handle split grades (e.g., 'a/a-', 'b+/b')
        if n > 2 and g[1] == '/':
            if n >= 3:
                d2 += getSingleGrade(g[2])
            if n > 3:
                d2 += getPmGrade(g[3])
            d = (d + d2) / 2
        elif n > 2 and g[2] == '/':
            if n >= 4:
                d2 += getSingleGrade(g[3])
            if n > 4:
                d2 += getPmGrade(g[-1])
            d = (d + d2) / 2
            
        gd.append(d)
        
    return gd

def medianOfLetterGrades(lst):
    """Calculate the median letter grade from a list of letter grades.
    
    Args:
        lst: List of letter grades as strings
        
    Returns:
        The median letter grade
    """
    # Convert the letter grades to numeric values
    dl = cnvrt2Dgt(lst)
    
    # Calculate the median of the numeric values
    g = medianOfList(dl)
    
    # Convert the median numeric value back to a letter grade
    if g >= 4.126:
        return "A+"
    elif g >= 4.01:
        return "A+/A"
    elif g >= 3.88:
        return "A"
    elif g >= 3.76:
        return "A/A-"
    elif g >= 3.51:
        return "A-"
    elif g >= 3.26:
        return "A-/B+"
    elif g >= 3.126:
        return "B+"
    elif g >= 3.01:
        return "B+/B"
    elif g >= 2.88:
        return "B"
    elif g >= 2.76:
        return "B/B-"
    elif g >= 2.51:
        return "B-"
    elif g >= 2.26:
        return "B-/C+"
    elif g >= 2.126:
        return "C+"
    elif g >= 2.01:
        return "C+/C"
    elif g >= 1.88:
        return "C"
    elif g >= 1.76:
        return "C/C-"
    elif g >= 1.51:
        return "C-"
    elif g >= 1.26:
        return "C-/D+"
    elif g >= 1.126:
        return "D+"
    elif g >= 1.01:
        return "D+/D"
    elif g >= 0.88:
        return "D"
    elif g >= 0.76:
        return "D/D-"
    elif g >= 0.51:
        return "D-"
    else:
        return "F"

# Example usage
if __name__ == "__main__":
    # Test cases
    test1 = ['A-', 'A-/B+', 'A+', 'B+/B', 'B-/C+']
    test2 = ['A-/B+', 'A+', 'B+/B', 'B-/C+', 'B', 'A']
    
    print(f"Test 1 Grades: {test1}")
    print(f"Numeric values: {cnvrt2Dgt(test1)}")
    print(f"Median: {medianOfLetterGrades(test1)}")
    
    print(f"\nTest 2 Grades: {test2}")
    print(f"Numeric values: {cnvrt2Dgt(test2)}")
    print(f"Median: {medianOfLetterGrades(test2)}")