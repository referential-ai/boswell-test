#!/usr/bin/env python3
"""
Script to analyze all grading responses to determine why there are no composite grades.
"""

import os
import json
import glob
import re
from typing import Dict, List, Any, Tuple

def analyze_grade_texts(results_dir: str) -> Dict[str, List[str]]:
    """
    Examine all grading responses and extract the exact text used to express grades.
    
    Args:
        results_dir: Path to the results directory
        
    Returns:
        Dictionary mapping grade patterns to examples of that pattern
    """
    pattern_examples = {
        "exact_grade_format": [],  # "Grade: A-"
        "grade_with_parentheses": [],  # "Grade: (A-)"
        "composite_grade_format": [],  # "Grade: A-/B+"
        "descriptive_grade": [],  # "Grade: Between A- and B+"
        "unusual_format": []  # Any other formats
    }
    
    grades_dir = os.path.join(results_dir, "grades")
    if not os.path.exists(grades_dir):
        print(f"No grades directory found at {grades_dir}")
        return pattern_examples
    
    # Scan through all grade files
    for author_dir in os.listdir(grades_dir):
        author_path = os.path.join(grades_dir, author_dir)
        if not os.path.isdir(author_path):
            continue
        
        for grader_file in os.listdir(author_path):
            if not grader_file.endswith(".json"):
                continue
            
            grade_file_path = os.path.join(author_path, grader_file)
            
            try:
                with open(grade_file_path, 'r') as f:
                    grade_data = json.load(f)
                
                feedback = grade_data.get("feedback", "")
                grade = grade_data.get("grade", "")
                
                # Extract the actual line containing the grade
                grade_line = None
                for line in feedback.split("\n"):
                    if re.search(r'grade\s*:.*', line, re.IGNORECASE):
                        grade_line = line.strip()
                        break
                
                if grade_line:
                    # Categorize the grade line
                    if re.search(r'grade\s*:\s*[A-C][+-]?/[A-C][+-]?', grade_line, re.IGNORECASE):
                        pattern_examples["composite_grade_format"].append({
                            "line": grade_line, 
                            "file": grade_file_path,
                            "extracted_grade": grade
                        })
                    elif re.search(r'grade\s*:\s*\([A-C][+-]?\)', grade_line, re.IGNORECASE):
                        pattern_examples["grade_with_parentheses"].append({
                            "line": grade_line, 
                            "file": grade_file_path,
                            "extracted_grade": grade
                        })
                    elif re.search(r'grade\s*:\s*[A-C][+-]?', grade_line, re.IGNORECASE):
                        pattern_examples["exact_grade_format"].append({
                            "line": grade_line, 
                            "file": grade_file_path,
                            "extracted_grade": grade
                        })
                    elif re.search(r'between\s+[A-C][+-]?\s+and\s+[A-C][+-]?', grade_line, re.IGNORECASE):
                        pattern_examples["descriptive_grade"].append({
                            "line": grade_line, 
                            "file": grade_file_path,
                            "extracted_grade": grade
                        })
                    else:
                        pattern_examples["unusual_format"].append({
                            "line": grade_line, 
                            "file": grade_file_path,
                            "extracted_grade": grade
                        })
                else:
                    # No grade line found, examine the whole feedback
                    for pattern, examples in [
                        (r'[A-C][+-]?/[A-C][+-]?', "composite_grade_format"),
                        (r'between\s+[A-C][+-]?\s+and\s+[A-C][+-]?', "descriptive_grade")
                    ]:
                        match = re.search(pattern, feedback, re.IGNORECASE)
                        if match:
                            pattern_examples[examples].append({
                                "context": feedback[max(0, match.start()-40):min(len(feedback), match.end()+40)], 
                                "file": grade_file_path,
                                "extracted_grade": grade
                            })
            except Exception as e:
                print(f"Error processing {grade_file_path}: {e}")
    
    return pattern_examples

def scan_for_patterns_in_prompts(results_dir: str) -> Dict[str, Any]:
    """
    Analyze the grading prompt to see if we're instructing models to use composite grades.
    """
    full_results_path = os.path.join(results_dir, "full_results.json")
    if not os.path.exists(full_results_path):
        print(f"No full_results.json found at {full_results_path}")
        return {}
    
    with open(full_results_path, 'r') as f:
        full_results = json.load(f)
    
    # Extract grading prompt
    grading_prompt = full_results.get("config", {}).get("grading_prompt", "")
    
    # Check if prompt mentions composite grades
    composite_mentions = []
    composite_patterns = [
        r'[A-C][+-]?/[A-C][+-]?',
        r'between\s+[A-C][+-]?\s+and\s+[A-C][+-]?',
        r'composite\s+grade',
        r'halfway',
        r'midpoint'
    ]
    
    for pattern in composite_patterns:
        for match in re.finditer(pattern, grading_prompt, re.IGNORECASE):
            start = max(0, match.start() - 40)
            end = min(len(grading_prompt), match.end() + 40)
            composite_mentions.append({
                "pattern": pattern,
                "context": grading_prompt[start:end]
            })
    
    return {
        "includes_composite_instructions": len(composite_mentions) > 0,
        "composite_mentions": composite_mentions,
        "full_prompt": grading_prompt
    }

def main():
    # Use the latest results directory
    results_dirs = sorted(glob.glob("results/*-pol_sci_1"), reverse=True)
    if not results_dirs:
        print("No results directories found")
        return
    
    latest_results_dir = results_dirs[0]
    print(f"Analyzing results in: {latest_results_dir}")
    
    # Check if prompt mentions composite grades
    prompt_analysis = scan_for_patterns_in_prompts(latest_results_dir)
    
    if prompt_analysis.get("includes_composite_instructions", False):
        print("\nGrading prompt includes composite grade instructions:")
        for mention in prompt_analysis.get("composite_mentions", []):
            print(f"- {mention['context']}")
    else:
        print("\nGrading prompt does NOT explicitly instruct models to use composite grades.")
        print("This is likely why we don't see composite grades in the responses.")
    
    # Analyze grade response patterns
    pattern_examples = analyze_grade_texts(latest_results_dir)
    
    print("\nAnalysis of grade formats in model responses:")
    for pattern_type, examples in pattern_examples.items():
        print(f"\n{pattern_type.replace('_', ' ').title()}: {len(examples)} instances")
        
        if examples:
            for i, example in enumerate(examples[:3]):  # Show first 3 examples
                if "line" in example:
                    print(f"  {i+1}. '{example['line']}' (extracted as '{example['extracted_grade']}')")
                elif "context" in example:
                    print(f"  {i+1}. '...{example['context']}...' (extracted as '{example['extracted_grade']}')")
    
    # Check if we found any composite formats
    if pattern_examples["composite_grade_format"] or pattern_examples["descriptive_grade"]:
        print("\nComposite grade formats WERE found, but they may not be in the exact 'X/Y' format expected by the system.")
    else:
        print("\nNo composite grade formats were found in any responses.")
        print("This suggests models are generally giving specific grades rather than composite grades.")
    
    print("\nConclusion:")
    print("1. The system supports composite grades technically (as seen in the code)")
    print("2. We don't see composite grades in the results because:")
    if not prompt_analysis.get("includes_composite_instructions", False):
        print("   - We don't explicitly ask models to use composite grades in our prompts")
    print("   - Models tend to provide specific grades rather than composite ones")
    print("   - The current extraction patterns might not capture all forms of composite grades")
    print("\nTo generate composite grades, we should:")
    print("1. Update the grading prompt to explicitly request composite grades when appropriate")
    print("2. Ensure our extraction patterns can identify different forms of composite grades")

if __name__ == "__main__":
    main()