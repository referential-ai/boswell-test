#!/usr/bin/env python3
"""
Test script for the improved grade extraction in botwell/core/grading.py
This script tests the enhanced grade extraction on previously failed cases.
"""

import os
import sys
from botwell.core.grading import extract_grade

def test_improved_extraction():
    """Test the improved grade extraction on previously failed cases."""
    print("Testing improved grade extraction...")
    
    # Directory containing failed extraction logs
    logs_dir = "logs/grade_extraction"
    
    if not os.path.exists(logs_dir):
        print(f"Error: Directory {logs_dir} does not exist")
        return False
        
    log_files = [f for f in os.listdir(logs_dir) if f.endswith("_failed_extraction.txt")]
    
    if not log_files:
        print(f"No log files found in {logs_dir}")
        return False
        
    print(f"Found {len(log_files)} log files")
    success_count = 0
    
    for filename in log_files:
        filepath = os.path.join(logs_dir, filename)
        
        # Extract model name from filename
        model_name = filename.split("_", 1)[1].replace("_failed_extraction.txt", "")
        print(f"Testing: {model_name}")
        
        with open(filepath, 'r') as f:
            content = f.read()
            
            # Skip header lines to get to the actual feedback
            feedback_start = content.find("Feedback content:")
            if feedback_start >= 0:
                feedback = content[feedback_start + len("Feedback content:"):]
                
                # Test the extract_grade function
                grade = extract_grade(feedback, model_name)
                
                if grade != "N/A":
                    print(f"  ✓ SUCCESS: Extracted grade {grade}")
                    success_count += 1
                else:
                    print(f"  ✗ FAILED: Could not extract grade")
    
    # Print summary
    print("\nTest Summary:")
    print(f"Successfully extracted grades: {success_count}/{len(log_files)} ({success_count/len(log_files)*100:.1f}%)")
    
    return success_count == len(log_files)

if __name__ == "__main__":
    # Add project root to path (if not running from there)
    if not os.getcwd().endswith("boswell-test-v1"):
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    success = test_improved_extraction()
    
    if success:
        print("\nAll tests PASSED! The improved grade extraction is working correctly.")
        sys.exit(0)
    else:
        print("\nSome tests FAILED. The improved grade extraction needs further enhancement.")
        sys.exit(1)