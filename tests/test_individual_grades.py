#!/usr/bin/env python3
"""
Test script to verify the individual grading files functionality.
This script will run a small test on a subset of models and check
that individual grade JSON files are created correctly.
"""

import os
import json
import argparse
import time

def main():
    """Run a small test with a single domain and check the individual grade files."""
    # Set up args
    parser = argparse.ArgumentParser(description="Test individual grading files")
    parser.add_argument("--domain", type=str, default="pol_sci_1",
                       help="Domain to test (default: pol_sci_1)")
    parser.add_argument("--models", type=str, nargs="+", default=["Claude-3.7-Sonnet", "o1", "Qwen-Max"],
                       help="Models to test (default: Claude-3.7-Sonnet o1 Qwen-Max)")
    args = parser.parse_args()
    
    # Add timestamp to test output
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    print(f"Starting individual grades test at {timestamp}")
    print(f"Using domain: {args.domain}")
    print(f"Using models: {', '.join(args.models)}")
    
    # Run a small test
    from botwell.core.test import run_boswell_test
    results = run_boswell_test(
        domain_name=args.domain,
        output_file=f"test_individual_grades_{timestamp}.json",
        selected_models=args.models,
        max_retries=2
    )
    
    if not results or "results_dir" not in results:
        print("Error: Test failed to produce results")
        return 1
    
    # Check for individual grade files
    results_dir = results["results_dir"]
    grades_dir = f"{results_dir}/grades"
    
    if not os.path.exists(grades_dir):
        print(f"Error: Grades directory not found at {grades_dir}")
        return 1
    
    # Count expected and actual files
    expected_files = 0
    actual_files = 0
    
    # Count how many files we expect (models × models)
    for author in results["essays"]:
        for grader in results["grades"]:
            if author in results["grades"][grader]:
                expected_files += 1
    
    # Count actual files and verify structure
    for author_dir in os.listdir(grades_dir):
        author_path = os.path.join(grades_dir, author_dir)
        if os.path.isdir(author_path):
            print(f"Checking grades for author: {author_dir}")
            
            for grader_file in os.listdir(author_path):
                if grader_file.endswith(".json"):
                    actual_files += 1
                    grader_name = os.path.splitext(grader_file)[0]
                    grade_file = os.path.join(author_path, grader_file)
                    
                    # Verify file content
                    try:
                        with open(grade_file, 'r') as f:
                            grade_data = json.load(f)
                            
                        # Check required fields
                        required_fields = ["author", "grader", "feedback", "grade", "numeric_grade"]
                        missing_fields = [field for field in required_fields if field not in grade_data]
                        
                        if missing_fields:
                            print(f"  Warning: File {grade_file} is missing fields: {', '.join(missing_fields)}")
                        else:
                            print(f"  ✓ Verified grade from {grader_name}: {grade_data['grade']}")
                            
                    except Exception as e:
                        print(f"  Error reading {grade_file}: {e}")
    
    # Report results
    print(f"\nGrade file verification complete:")
    print(f"  Expected files: {expected_files}")
    print(f"  Actual files: {actual_files}")
    
    if actual_files < expected_files:
        print(f"  Warning: Some expected grade files were not found")
    elif actual_files > expected_files:
        print(f"  Warning: More grade files than expected were found")
    else:
        print(f"  Success: All expected grade files were found and verified")
    
    print(f"\nTest results saved to {results_dir}")
    return 0

if __name__ == "__main__":
    exit(main())