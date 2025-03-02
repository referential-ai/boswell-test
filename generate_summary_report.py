#!/usr/bin/env python3
"""
Generate summary reports for existing Boswell Test results.

This script can:
1. Generate a summary report for a specified results directory
2. Generate summary reports for all results directories
3. Generate a summary report for the most recent results
"""

import os
import sys
import argparse
from pathlib import Path
import re
from typing import List

from botwell.reporting.summary_report import create_summary_report_for_results


def find_result_directories() -> List[str]:
    """Find all result directories from previous runs.
    
    Returns:
        List of result directory paths sorted by timestamp (newest first)
    """
    results_base = "results"
    if not os.path.exists(results_base):
        return []
        
    # Find directories that match the timestamp-domain pattern
    result_dirs = []
    for entry in os.listdir(results_base):
        entry_path = os.path.join(results_base, entry)
        
        # Skip aggregate directories
        if "aggregate" in entry:
            continue
            
        # Check if it's a directory with the right format (timestamp-domain)
        if os.path.isdir(entry_path) and re.match(r"^\d{8}-\d{6}-[a-z_]+\d*", entry):
            # Check if it has a full_results.json file (indicating it was a complete run)
            if os.path.exists(os.path.join(entry_path, "full_results.json")):
                result_dirs.append(entry_path)
    
    # Sort by timestamp (newest first)
    result_dirs.sort(reverse=True)
    return result_dirs


def generate_reports(directory: str = None, all_dirs: bool = False, latest: bool = False) -> None:
    """Generate summary reports for specified Boswell Test results.
    
    Args:
        directory: Specific results directory to process
        all_dirs: Process all results directories if True
        latest: Process only the most recent results directory if True
    """
    # Check for contradictory arguments
    if sum([bool(directory), all_dirs, latest]) != 1:
        print("Error: Please specify exactly one of: --directory, --all, or --latest")
        return
        
    if directory:
        # Generate report for the specified directory
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist")
            return
            
        print(f"Generating summary report for: {directory}")
        try:
            report_path = create_summary_report_for_results(directory)
            print(f"Report saved to: {report_path}")
        except Exception as e:
            print(f"Error generating report: {e}")
            
    elif all_dirs or latest:
        # Find result directories
        result_dirs = find_result_directories()
        
        if not result_dirs:
            print("No result directories found")
            return
            
        if latest:
            # Process only the most recent directory
            directory = result_dirs[0]
            print(f"Processing most recent results: {directory}")
            try:
                report_path = create_summary_report_for_results(directory)
                print(f"Report saved to: {report_path}")
            except Exception as e:
                print(f"Error generating report: {e}")
        else:
            # Process all directories
            print(f"Processing {len(result_dirs)} result directories...")
            
            success_count = 0
            for directory in result_dirs:
                print(f"  Processing: {directory}")
                try:
                    report_path = create_summary_report_for_results(directory)
                    print(f"  Report saved to: {report_path}")
                    success_count += 1
                except Exception as e:
                    print(f"  Error generating report: {e}")
                    
            print(f"\nGenerated {success_count} reports successfully")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Generate summary reports for Boswell Test results")
    
    # Set up mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--directory", "-d", type=str,
                      help="Generate report for a specific results directory")
    group.add_argument("--all", "-a", action="store_true",
                      help="Generate reports for all results directories")
    group.add_argument("--latest", "-l", action="store_true",
                      help="Generate report for the most recent results directory")
    
    args = parser.parse_args()
    
    generate_reports(
        directory=args.directory,
        all_dirs=args.all,
        latest=args.latest
    )


if __name__ == "__main__":
    main()