# Cross-Grading Table Documentation

## Overview

The cross-grading table is a key output of the Boswell system that visualizes how each model evaluated every other model's essay. This document explains how this table is generated, its features, and the underlying implementation.

## Table Structure

The cross-grading table is organized as follows:

- **Rows**: Each row represents a model being graded (essay author)
- **Columns**: Each column represents a model doing the grading (evaluator)
- **Cells**: Each cell contains the grade that the column model gave to the row model
- **Diagonal**: Cells where row = column represent self-assessment (how a model graded its own essay)
- **Additional Columns**: Includes median grades and raw numeric averages

## Excel Generation Process

The cross-grading table is generated as a color-coded Excel spreadsheet through the `generate_cross_grading_excel()` function in `botwell/reporting/excel.py`. This function works as follows:

1. Creates a new Excel workbook with a "Cross Grading" worksheet
2. Sets up the header row with model names
3. Iterates through each model, creating a row for that model
4. For each cell, retrieves the grade that the column model gave to the row model
5. Calculates and adds median grades for each row
6. Calculates and adds raw numeric averages for each row
7. Adds a grading bias row showing tendencies of each grader
8. Adds column medians showing typical grades given by each model

```python
def generate_cross_grading_excel(results: Dict[str, Any], run_dir: str) -> None:
    """
    Generate Excel spreadsheet with color-coded cross-grading matrix.
    
    Args:
        results: The full results dictionary
        run_dir: Directory path where output files should be saved
    """
    # Get models list
    models = list(results["essays"].keys())
    
    # Create a new Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cross Grading"
    
    # Set up worksheet header and apply styling
    # ...
    
    # Fill in the grading matrix
    for i, graded_model in enumerate(models):
        # Create a row for each model
        # ...
        
        # Add grades for each grader
        for j, grader_model in enumerate(models):
            # Get and format the grade
            # ...
            
        # Calculate and add median grade and raw average
        # ...
    
    # Add grading bias and column median rows
    # ...
    
    # Save the Excel file
    excel_file = os.path.join(run_dir, "cross_grading_table.xlsx")
    wb.save(excel_file)
```

## Grade Display Format

Each grade in the table is displayed with both its letter grade and numeric equivalents:

- **Format**: `"A (4.00)"` or `"B+ (3.25)"`
- **N/A Grades**: Displayed as `"N/A"` or `"N/A (0.00)"`
- **Cell Styling**: Each cell is color-coded based on the letter grade
- **Self-Assessment**: Self-grading cells have a distinctive lavender background

## Raw Numeric Averages

A key feature of the cross-grading table is the raw numeric average column:

1. **Calculation**: Direct mathematical mean of all numeric grades for each model
2. **Precision**: Calculated with full floating-point precision
3. **Display**: Shown with 2 decimal places (e.g., `"3.75"`)
4. **Styling**: Displayed with blue background and bold formatting
5. **Purpose**: Provides a more precise measure than median letter grades

```python
# Calculate raw average
exact_raw_average = sum(raw_numeric_grades) / len(raw_numeric_grades) if raw_numeric_grades else 0.0

# Add to Excel cell with special formatting
apply_cell_style(
    ws.cell(row=row, column=raw_avg_col),
    value=f"{exact_raw_average:.2f}" if exact_raw_average > 0 else "N/A",
    alignment=CENTER_WRAP_ALIGNMENT,
    border=THIN_BORDER,
    font=Font(name="Helvetica Neue", bold=True, size=8),
    fill=PatternFill(start_color="E6F0FF", end_color="E6F0FF", fill_type="solid")
)
```

## Color Coding Scheme

The table uses a color-coding scheme to make grade patterns visually apparent:

| Grade | Color      | Hex Code |
|-------|------------|----------|
| A+    | Bright green | #00FF00 |
| A     | Light green  | #90EE90 |
| A-    | Pale green   | #98FB98 |
| B+    | Light blue   | #ADD8E6 |
| B     | Sky blue     | #87CEEB |
| B-    | Light steel blue | #B0C4DE |
| C+    | Light yellow | #FFFFE0 |
| C     | Yellow      | #FFFF99 |
| C-    | Gold        | #FFD700 |
| D+    | Light salmon | #FFA07A |
| D     | Coral       | #FF7F50 |
| D-    | Tomato      | #FF6347 |
| F     | Red         | #FF0000 |
| N/A   | Light gray  | #D3D3D3 |

This visual scheme makes it easy to identify patterns such as lenient graders (more green/blue) or strict graders (more yellow/red).

## Median Calculation

The table includes median grades calculated for each model:

1. **Row Medians**: The median grade received by each model (shown in an additional column)
2. **Column Medians**: The median grade given by each model (shown in an additional row)

For row medians, the calculation prioritizes using the actual numeric grades:

```python
median_grade, _, median_value, raw_average = calculate_median_grade(
    grades_for_model, 
    results, 
    graded_model,
    grader_models_for_median
)
```

The `calculate_median_grade()` function handles various cases:
- Converts letter grades to numeric values for calculation
- Sorts the numeric values to find the median
- Handles even vs. odd number of grades appropriately
- Converts the numeric median back to a letter grade
- Detects if GPA scale (0-4) or percentage scale (0-100) is in use
- Returns both the letter grade and its numeric equivalent

## Grading Bias

The grading bias row shows whether each model tends to be lenient or strict compared to others:

- **Calculation**: The difference between a model's median given grade and the overall median
- **Display**: Descriptive labels like "Neutral", "Lenient (+1 grade)", or "Strict (-1 grade)"
- **Styling**: Displayed with light red background

```python
# Positive bias means more lenient, negative means stricter
median_bias = stats["median_given"] - overall_median

# Convert numeric bias to descriptive label
if abs(median_bias) < 0.15:
    letter_bias = "Neutral"
elif median_bias > 0:
    if median_bias > 0.6:
        letter_bias = "Very Lenient (+2 grades)"
    elif median_bias > 0.3:
        letter_bias = "Lenient (+1 grade)"
    else:
        letter_bias = "Slightly Lenient (+1/3 grade)"
else:
    if median_bias < -0.6:
        letter_bias = "Very Strict (-2 grades)"
    elif median_bias < -0.3:
        letter_bias = "Strict (-1 grade)"
    else:
        letter_bias = "Slightly Strict (-1/3 grade)"
```

## Fallback Implementation

The system includes a fallback implementation using pandas when the Excel module can't be imported:

```python
# Fall back to pandas if we can't find the Excel module
print("Excel module not found, using pandas directly...")
try:
    import pandas as pd
    
    # Create DataFrame
    df = pd.DataFrame(data, index=models)
    
    # Save to Excel
    excel_file = os.path.join(output_dir, "cross_grading_table.xlsx")
    df.to_excel(excel_file)
    print(f"Generated Excel cross-grading table: {excel_file}")
except ImportError:
    print("Error: pandas is required to generate Excel tables. Please install it with 'pip install pandas'")
    sys.exit(1)
```

This fallback produces a basic Excel table without the color coding and advanced formatting, but preserves the essential data structure.

## Usage Example

To generate a cross-grading table from command line:

```bash
python create_cross_grading_table.py path/to/full_results.json
```

This will create the Excel file in the same directory as the results file.

## Grade Scale Considerations

The Excel module uses two different grade scales:

1. **Percentage Scale** (GRADE_SCORES): Maps letter grades to percentages (A+ = 97.0, A = 93.0, etc.)
2. **GPA Scale** (GPA_GRADE_SCALE): Maps letter grades to GPA values (A+ = 4.0, A = 4.0, etc.)

Note that in the GPA scale, A+ and A both map to 4.0, which differs from the university standard in `grading.py` where A+ = 4.25.

```python
# GPA-style grades (0-4 scale) mapping
GPA_GRADE_SCALE = {
    "A+": 4.0,
    "A": 4.0,  # A+ and A are both 4.0 in GPA scale
    "A-": 3.7,
    "B+": 3.3,
    # ...
}
```

The system detects which scale to use based on the range of values in the data, providing appropriate conversions between letter grades and numeric values.