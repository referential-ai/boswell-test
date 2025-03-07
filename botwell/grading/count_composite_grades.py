#!/usr/bin/env python
"""
Count how many composite grades were used by LLMs in the test results.
"""

import json
import os
import glob
import sys

def count_composite_grades(results_dir):
    """Count how many composite grades were used by LLMs in the given results directory."""
    composite_count = 0
    total_count = 0
    composite_examples = []
    
    pattern = f"{results_dir}/grades/*/*"
    
    for file in glob.glob(pattern):
        try:
            with open(file) as f:
                data = json.load(f)
                grade = data.get('grade', '')
                total_count += 1
                
                if '/' in grade:
                    composite_count += 1
                    author = os.path.basename(os.path.dirname(file))
                    grader = os.path.basename(file).replace('.json', '')
                    composite_examples.append((grader, author, grade))
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    # Print summary
    if total_count > 0:
        percentage = composite_count / total_count * 100
        print(f"Composite grades from LLMs: {composite_count}/{total_count} ({percentage:.1f}%)")
        
        if composite_examples:
            print("\nExamples of composite grades:")
            for grader, author, grade in composite_examples[:5]:  # Show first 5 examples
                print(f"  {grader} gave {author} a grade of {grade}")
    else:
        print("No grading files found.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        results_dir = sys.argv[1]
    else:
        # Use the latest results directory if none specified
        results_dirs = sorted(glob.glob("results/*-pol_sci_1"), reverse=True)
        if not results_dirs:
            print("No results directories found.")
            sys.exit(1)
        results_dir = results_dirs[0]
        print(f"Using latest results directory: {results_dir}")
    
    count_composite_grades(results_dir)