#!/usr/bin/env python
"""
Check for composite grade values in the raw grade matrix.
"""

import json
import os
import sys

def check_for_composite_values(filepath):
    """Check for values that would trigger composite grade notation."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    composite_values = []
    
    # Define the ranges that would trigger composite grade notation
    # These are the exact midpoints between grade boundaries (with a small tolerance)
    ranges = [
        (3.49, 3.51),     # A-/B+ (3.5)
        (3.115, 3.135),   # B+/B (3.125)
        (2.865, 2.885),   # B/B- (2.875)
        (3.865, 3.885),   # A/A- (3.875)
        (2.115, 2.135),   # C+/C (2.125)
        (1.865, 1.885)    # C/C- (1.875)
    ]
    
    for model in data:
        for grader, info in data[model].items():
            value = info['numeric_grade']
            
            for lower, upper in ranges:
                if lower < value < upper:
                    composite_values.append((model, grader, value))
                    break
    
    if composite_values:
        print(f"Found {len(composite_values)} potential composite grade values:")
        for model, grader, value in composite_values:
            print(f"  Model: {model}, Grader: {grader}, Value: {value}")
            
        # Also check for median/average values that might be composite
        print("\nChecking for composite values in averages:")
        for model in data:
            model_values = []
            for grader, info in data[model].items():
                if info['numeric_grade'] > 0:
                    model_values.append(info['numeric_grade'])
            
            if model_values:
                avg = sum(model_values) / len(model_values)
                for lower, upper in ranges:
                    if lower < avg < upper:
                        print(f"  Model: {model}, Average: {avg}")
                        break
    else:
        print("No composite grade values found in the data.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "results/20250305-214416-pol_sci_1/raw_grade_matrix.json"
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
        
    check_for_composite_values(filepath)