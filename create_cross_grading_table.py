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
        
        # Also generate the raw numeric table
        from botwell.reporting.raw_table import generate_raw_numeric_table
        raw_table_path = generate_raw_numeric_table(results, output_dir)
        print(f"Generated raw numeric table: {raw_table_path}")
        
        # Also generate the letter grade table
        from botwell.reporting.letter_table import generate_letter_grade_table
        letter_table_path = generate_letter_grade_table(results, output_dir)
        print(f"Generated letter grade table: {letter_table_path}")
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

            # Try to import raw_table if it exists
            raw_module_path = os.path.join(os.path.dirname(__file__), 'botwell', 'reporting', 'raw_table.py')
            if os.path.exists(raw_module_path):
                raw_spec = importlib.util.spec_from_file_location("raw_table_module", raw_module_path)
                raw_module = importlib.util.module_from_spec(raw_spec)
                raw_spec.loader.exec_module(raw_module)
                raw_table_path = raw_module.generate_raw_numeric_table(results, output_dir)
                if raw_table_path and not raw_table_path.endswith(".xlsx"):
                    print(f"Generated raw numeric table at: {raw_table_path}")
            
            # Try to import letter_table if it exists
            letter_module_path = os.path.join(os.path.dirname(__file__), 'botwell', 'reporting', 'letter_table.py')
            if os.path.exists(letter_module_path):
                letter_spec = importlib.util.spec_from_file_location("letter_table_module", letter_module_path)
                letter_module = importlib.util.module_from_spec(letter_spec)
                letter_spec.loader.exec_module(letter_module)
                letter_table_path = letter_module.generate_letter_grade_table(results, output_dir)
                print(f"Generated letter grade table: {letter_table_path}")
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
                            numeric_grade = results["grades"][graded_model][grader_model].get("numeric_grade", 0.0)
                            row_data[f"Score from {grader_model}"] = f"{grade} ({numeric_grade:.2f})" if grade != "N/A" else "N/A"
                        except KeyError:
                            row_data[f"Score from {grader_model}"] = "N/A"
                    
                    raw_grades = []
                    for grader_model in models:
                        try:
                            if "numeric_grade" in results["grades"][graded_model][grader_model]:
                                raw_grades.append(results["grades"][graded_model][grader_model]["numeric_grade"])
                        except KeyError:
                            pass
                    # Add raw average as a column
                    row_data["Overall Score (0-4.25 scale)"] = f"{sum(raw_grades) / len(raw_grades):.2f}" if raw_grades else "N/A"
                    data.append(row_data)
                
                # Create DataFrame
                # Handle duplicate model names for row indices
                display_models = models.copy()
                if len(set(models)) < len(models):
                    model_counts = {}
                    for i, model in enumerate(models):
                        if model in model_counts:
                            model_counts[model] += 1
                            display_models[i] = f"{model} (Run {model_counts[model]})"
                        else:
                            model_counts[model] = 1
                
                df = pd.DataFrame(data, index=display_models)
                
                # Save to Excel
                excel_file = os.path.join(output_dir, "cross_grading_table.xlsx")
                with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name="Cross Grading")
                    # Add a title row - not as fancy as the openpyxl version but still helpful
                    workbook = writer.book
                    worksheet = writer.sheets['Cross Grading']
                    worksheet.insert_rows(1)
                    worksheet.cell(row=1, column=1, value="Cross-Grading Table: Models Evaluating Each Other's Essays")
                    worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(models)+2)
                
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