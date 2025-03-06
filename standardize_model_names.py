#!/usr/bin/env python3
"""
Model Name Standardization Script

This script scans the project for inconsistent model name references and standardizes them
according to the official name format defined in model_name_standardization.md.

It focuses on these common issues:
1. Perplexity models sometimes using hyphens instead of colons
2. Abbreviated model names 
3. Inconsistent formatting of version numbers and suffixes
"""

import os
import re
import glob
from typing import Dict, List, Tuple

# Define the standard model names based on model_name_standardization.md
STANDARD_MODEL_NAMES = {
    # OpenAI Models
    "GPT4o": "GPT-4o",
    "GPT4-o": "GPT-4o",
    "GPT-4-o": "GPT-4o",
    "GPT4o-mini": "GPT-4o-mini",
    "GPT-4-o-mini": "GPT-4o-mini",
    "GPT4-o-mini": "GPT-4o-mini",
    "GPT-4o mini": "GPT-4o-mini",
    "GPT-3.5 Turbo": "GPT-3.5-Turbo",
    
    # Anthropic Models
    "Claude 3 Opus": "Claude-3-Opus",
    "Claude-3 Opus": "Claude-3-Opus",
    "Claude 3-Opus": "Claude-3-Opus",
    "Claude 3 Sonnet": "Claude-3-Sonnet",
    "Claude-3 Sonnet": "Claude-3-Sonnet",
    "Claude 3-Sonnet": "Claude-3-Sonnet",
    "Claude 3.7 Sonnet": "Claude-3.7-Sonnet",
    "Claude-3.7 Sonnet": "Claude-3.7-Sonnet",
    "Claude 3.7-Sonnet": "Claude-3.7-Sonnet",
    "Claude-3.7-Sonnet thinking": "Claude-3.7-Sonnet-thinking",
    "Claude-3.7-Sonnet-thinking": "Claude-3.7-Sonnet-thinking",
    "Claude thinking": "Claude-3.7-Sonnet-thinking",
    "Claude-3.7 thinking": "Claude-3.7-Sonnet-thinking",
    
    # Perplexity Models (the most problematic)
    "Perplexity-Llama": "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity Llama": "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity": "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity-70B": "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity 70B": "Perplexity: Llama 3.1 Sonar 70B",
    "Sonar 70B": "Perplexity: Llama 3.1 Sonar 70B",
    "Llama Sonar": "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity-Llama 3.1 Sonar 70B": "Perplexity: Llama 3.1 Sonar 70B",
    "Perplexity-8B": "Perplexity: Llama 3.1 Sonar 8B Online",
    "Perplexity 8B": "Perplexity: Llama 3.1 Sonar 8B Online",
    "Perplexity-Llama 3.1 Sonar 8B": "Perplexity: Llama 3.1 Sonar 8B Online",
    "Perplexity: Llama 3.1 Sonar 8B": "Perplexity: Llama 3.1 Sonar 8B Online",
    "Perplexity: Llama 3.1 Sonar 405B Online": "Perplexity: Llama 3.1 Sonar 70B",  # This seems to be a typo
    
    # Meta Models
    "Llama 3 8B": "Llama-3-8B",
    "Llama3-8B": "Llama-3-8B",
    "Llama-3 8B": "Llama-3-8B",
    "Llama 3-8B": "Llama-3-8B",
    
    # Google Models
    "Gemini Flash 2": "Gemini Flash 2.0",
    "Gemini-Flash-2.0": "Gemini Flash 2.0",
    "Gemini-Flash 2.0": "Gemini Flash 2.0",
    "Gemini Pro 1.5": "Gemini Pro 1.5",
    "Gemini-Pro-1.5": "Gemini Pro 1.5",
    "Gemini-Pro 1.5": "Gemini Pro 1.5",
    
    # DeepSeek Models
    "DeepSeek R1 Full": "DeepSeek-R1-Full",
    "DeepSeek-R1 Full": "DeepSeek-R1-Full",
    "DeepSeek R1-Full": "DeepSeek-R1-Full",
    "DeepSeek Distill Qwen 32b": "DeepSeek-Distill-Qwen-32b",
    "DeepSeek-Distill Qwen 32b": "DeepSeek-Distill-Qwen-32b",
    "DeepSeek Distill-Qwen 32b": "DeepSeek-Distill-Qwen-32b",
    "DeepSeek-Distill Qwen-32b": "DeepSeek-Distill-Qwen-32b",
    "DeepSeek Distill Qwen-32b": "DeepSeek-Distill-Qwen-32b",
    
    # Qwen Models
    "Qwen Max": "Qwen-Max",
    "Qwen Plus": "Qwen-Plus",
    "Qwen Turbo": "Qwen-Turbo",
    
    # Anthropic o Models
    "o1 mini": "o1-mini",
    "o3 mini high": "o3-mini-high",
    "o3 mini-high": "o3-mini-high",
    "o3-mini high": "o3-mini-high",
    
    # Misc Models
    "grok beta": "grok-beta",
    "grok2 1212": "grok2-1212"
}

def find_markdown_files(root_dir: str) -> List[str]:
    """Find all markdown files in the project."""
    return glob.glob(f"{root_dir}/**/*.md", recursive=True)

def standardize_file(filepath: str, model_dict: Dict[str, str]) -> Tuple[int, List[Tuple[str, str]]]:
    """
    Standardize model names in a file.
    
    Returns:
        Tuple of (number of replacements, list of replacements made)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track replacements for reporting
    replacements = []
    replacement_count = 0
    
    # Replace model names, starting with the longest keys first to avoid partial replacements
    for old_name, new_name in sorted(model_dict.items(), key=lambda x: len(x[0]), reverse=True):
        # Use word boundaries to avoid partial replacements
        pattern = r'\b' + re.escape(old_name) + r'\b'
        
        # Count occurrences before replacement
        matches = re.findall(pattern, content)
        if matches:
            # Only add to replacements if we found matches
            replacements.append((old_name, new_name, len(matches)))
            replacement_count += len(matches)
            
            # Make the replacement
            content = re.sub(pattern, new_name, content)
    
    # Write back to file if changes were made
    if replacement_count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return replacement_count, replacements

def standardize_model_names(root_dir: str) -> Dict[str, List[Tuple[str, str, int]]]:
    """
    Standardize model names across all markdown files.
    
    Returns:
        Dict mapping file paths to lists of replacements made
    """
    markdown_files = find_markdown_files(root_dir)
    results = {}
    
    total_replacements = 0
    files_modified = 0
    
    print(f"Found {len(markdown_files)} markdown files to process")
    
    for file_path in markdown_files:
        print(f"Processing {file_path}...", end="")
        replacements_count, replacements = standardize_file(file_path, STANDARD_MODEL_NAMES)
        
        if replacements_count > 0:
            results[file_path] = replacements
            total_replacements += replacements_count
            files_modified += 1
            print(f" made {replacements_count} replacements")
        else:
            print(" no replacements needed")
    
    print(f"\nStandardization complete!")
    print(f"Modified {files_modified} files with {total_replacements} total replacements")
    
    return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        root_directory = sys.argv[1]
    else:
        root_directory = "."  # Default to current directory
    
    print(f"Standardizing model names in {os.path.abspath(root_directory)}")
    results = standardize_model_names(root_directory)
    
    # Print detailed report
    if results:
        print("\nDetailed Replacement Report:")
        for file_path, replacements in results.items():
            print(f"\n{file_path}:")
            for old, new, count in replacements:
                print(f"  '{old}' → '{new}' ({count} occurrences)")
    else:
        print("\nNo replacements were needed. All model names are already standardized.")