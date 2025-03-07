"""
File operations and result handling for Boswell tests.
"""

import os
import json
import time
from typing import Dict, Any, Tuple


def create_results_directory(domain_name: str, timestamp: str, is_free_run: bool = False) -> Tuple[str, str]:
    """Create a timestamped directory for results."""
    # Create base results directory if it doesn't exist
    if not os.path.exists("results"):
        os.makedirs("results")
    
    # Create timestamped directory for this run
    # Include "free" in the directory name if it's a free run
    free_tag = "-free" if is_free_run else ""
    run_dir = f"results/{timestamp}-{domain_name}{free_tag}"
    essays_dir = f"{run_dir}/essays"
    grades_dir = f"{run_dir}/grades"
    
    os.makedirs(run_dir, exist_ok=True)
    os.makedirs(essays_dir, exist_ok=True)
    os.makedirs(grades_dir, exist_ok=True)
    
    return run_dir, essays_dir


def save_essay_with_grades(author: str, essay: str, grades: Dict[str, Dict[str, Any]], essays_dir: str) -> str:
    """Save an essay to a text file with grading feedback appended."""
    filename = f"{essays_dir}/{author}.md"
    
    with open(filename, 'w') as f:
        # Write essay header
        f.write(f"# Essay by {author}\n\n")
        f.write(essay)
        
        # Write grading feedback
        f.write("\n\n---\n\n")
        f.write("# Grading Feedback\n\n")
        
        for grader_name, grade_info in grades.items():
            f.write(f"## Graded by: {grader_name}\n\n")
            f.write(grade_info["feedback"])
            f.write(f"\n\n**Letter Grade:** {grade_info['grade']}\n")
            f.write(f"**Numeric Grade:** {grade_info['numeric_grade']:.1f}\n")
            f.write(f"**Complete grading data:** `grades/{author}/{grader_name}.json`\n\n")
            f.write("---\n\n")
    
    return filename


def save_essay_grading_json(author: str, grader: str, grade_data: Dict[str, Any], run_dir: str) -> str:
    """Save individual grading responses as JSON files.
    
    Args:
        author: The essay author (model name)
        grader: The grader model name
        grade_data: The complete grading data including feedback, grade, and raw response
        run_dir: The results directory for this run
        
    Returns:
        The path to the saved JSON file
    """
    # Create author directory if it doesn't exist
    author_dir = f"{run_dir}/grades/{author}"
    os.makedirs(author_dir, exist_ok=True)
    
    # Save individual grade JSON file
    filename = f"{author_dir}/{grader}.json"
    with open(filename, 'w') as f:
        json.dump(grade_data, f, indent=2)
    
    return filename


def save_results(results: Dict[str, Any], filename: str) -> None:
    """Save results to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {filename}")


def find_result_directories() -> list:
    """Find all result directories from previous runs.
    
    Returns:
        List of result directory paths sorted by timestamp (newest first)
    """
    import re
    
    if not os.path.exists("results"):
        return []
        
    # Find directories that match the timestamp-domain pattern
    result_dirs = []
    for entry in os.listdir("results"):
        entry_path = os.path.join("results", entry)
        # Skip aggregate directories
        if "aggregate" in entry:
            continue
            
        # Check if it's a directory with the right format
        if os.path.isdir(entry_path) and re.match(r"^\d{8}-\d{6}-[a-z_]+\d*(-free)?$", entry):
            # Check if it has a full_results.json file (indicating it was a complete run)
            if os.path.exists(os.path.join(entry_path, "full_results.json")):
                result_dirs.append(entry_path)
    
    # Sort by timestamp (newest first)
    result_dirs.sort(reverse=True)
    return result_dirs