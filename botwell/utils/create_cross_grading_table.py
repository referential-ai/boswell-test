#!/usr/bin/env python
"""
Create a cross-grading Excel table from Boswell Test results.

This script generates a color-coded Excel spreadsheet with the complete
cross-assessment matrix as seen in Table 1 of the research paper.
"""

import json
import os
import sys

def generate_cross_grading_excel(results_file: str) -> None:
    """
    Generate Excel spreadsheet with color-coded cross-grading matrix.
    
    Args:
        results_file: Path to the full_results.json file from Boswell test results
    """
    # Load results data
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    # Extract the output directory from the results file path
    output_dir = os.path.dirname(results_file)
    
    # Try to import the Excel generator
    try:
        # First try to import from the package
        from botwell.reporting.excel import generate_cross_grading_excel as excel_generator
        excel_generator(results, output_dir)
    except ImportError:
        # If we can't find it in the package, try to import it directly if it exists in the same directory
        module_path = os.path.join(os.path.dirname(__file__), 'botwell', 'reporting', 'excel.py')
        if os.path.exists(module_path):
            # We need to use importlib because the module isn't in the normal Python path
            import importlib.util
            spec = importlib.util.spec_from_file_location("excel_module", module_path)
            excel_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(excel_module)
            excel_module.generate_cross_grading_excel(results, output_dir)
        else:
            # Fall back to pandas if we can't find either module
            print("Excel module not found, using pandas directly...")
            try:
                import pandas as pd
                
                # Get models list
                models = list(results["essays"].keys())
                
                # Create grading matrix
                data = []
                for graded_model in models:
                    row_data = {}
                    for grader_model in models:
                        try:
                            grade = results["grades"][graded_model][grader_model]["grade"]
                            row_data[grader_model] = grade
                        except KeyError:
                            row_data[grader_model] = "N/A"
                    
                    # Calculate raw average of numeric grades
                    raw_grades = []
                    for grader_model in models:
                        try:
                            if "numeric_grade" in results["grades"][graded_model][grader_model]:
                                raw_grades.append(results["grades"][graded_model][grader_model]["numeric_grade"])
                        except KeyError:
                            pass
                    # Add raw average as a column
                    row_data["Raw Numeric Average"] = f"{sum(raw_grades) / len(raw_grades):.2f}" if raw_grades else "N/A"
                    data.append(row_data)
                
                # Create DataFrame
                df = pd.DataFrame(data, index=models)
                
                # Save to Excel
                excel_file = os.path.join(output_dir, "cross_grading_table.xlsx")
                df.to_excel(excel_file)
                print(f"Generated Excel cross-grading table: {excel_file}")
            except ImportError:
                print("Error: pandas is required to generate Excel tables. Please install it with 'pip install pandas'")
                sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_cross_grading_table.py <path_to_full_results.json>")
        sys.exit(1)
    
    results_file = sys.argv[1]
    generate_cross_grading_excel(results_file)