# Grading System Documentation

## Overview

The Boswell system uses a standardized grading system to evaluate AI model essays and calculate the Boswell Quotient. This document outlines the grading scale, conversion methods, and how N/A grades are handled.

## Grade Scale

The system uses a university standard letter grade scale with corresponding numeric values:

| Letter Grade | Numeric Value |
|--------------|---------------|
| A+           | 4.25          |
| A            | 4.0           |
| A-           | 3.75          |
| B+           | 3.5           |
| B            | 3.0           |
| B-           | 2.75          |
| C+           | 2.5           |
| C            | 2.0           |
| C-           | 1.75          |
| D+           | 1.5           |
| D            | 1.0           |
| D-           | 0.75          |
| F            | 0.0           |
| N/A          | 0.0           |

## Grade Conversion Methods

### Letter Grade to Numeric Value

The `grade_to_numeric()` function converts letter grades to their numeric equivalents based on the scale above.

```python
def grade_to_numeric(grade: str) -> float:
    """Convert letter grade to numeric value using university standard."""
    grade_map = {
        "A+": 4.25, "A": 4.0, "A-": 3.75,
        "B+": 3.5, "B": 3.0, "B-": 2.75,
        "C+": 2.5, "C": 2.0, "C-": 1.75,
        "D+": 1.5, "D": 1.0, "D-": 0.75,
        "F": 0.0,
        "N/A": 0.0
    }
    return grade_map.get(grade, 0.0)
```

### Numeric Value to Percentage

The `grade_to_percentage()` function maps numeric grades (0.0-4.25) to a percentage scale (0-100) to provide more granular visualization and comparison.

```python
def grade_to_percentage(numeric_grade: float) -> int:
    """Convert numeric grade to percentage (0-100 scale)."""
    if numeric_grade >= 4.25:  # A+
        return 100
    elif numeric_grade >= 4.0:  # A
        return 93 + int((numeric_grade - 4.0) / 0.25 * 4)
    # ... (other grade ranges)
    else:  # F
        return max(0, int(numeric_grade * 59 / 0.75))
```

### Percentage to Letter Grade

The `percentage_to_letter_grade()` function converts percentages back to letter grades:

```python
def percentage_to_letter_grade(percentage: int) -> str:
    """Convert percentage (0-100 scale) to letter grade."""
    if percentage >= 97:
        return "A+"
    elif percentage >= 93:
        return "A"
    # ... (other percentage ranges)
    else:
        return "F"
```

## Grade Extraction

Grades are extracted from feedback text using the `extract_grade()` function, which uses regular expressions to find letter grades in various formats.

```python
def extract_grade(feedback: str, model_name: str = "Unknown") -> str:
    """Extract letter grade from grading feedback."""
    # First try exact format: "Grade: A+"
    match = re.search(r"Grade:\s*([A-C][+-]?)", feedback)
    if match:
        return match.group(1).upper()
    
    # Fall back to more flexible patterns if needed
    # ...
    
    # If no grade found, log and return N/A
    log_failed_extraction(model_name, feedback)
    return "N/A"
```

## N/A Grade Handling

### When N/A Grades Occur

N/A grades can occur in several scenarios:
1. The grader model didn't explicitly state a grade
2. The extraction pattern failed to identify a grade in the feedback
3. The API call failed or timed out

### Logging of N/A Grades

Failed grade extractions are logged to help identify patterns and improve extraction:

```python
def log_failed_extraction(model_name: str, feedback: str, log_sample: bool = True) -> None:
    """Log failed grade extractions for analysis."""
    log_dir = "logs/grade_extraction"
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{log_dir}/{timestamp}_{model_name}_failed_extraction.txt"
    
    with open(filename, 'w') as f:
        f.write(f"Model: {model_name}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("Feedback content:\n")
        f.write(feedback)
```

### Standardized Display Format

To ensure consistency across all report types, N/A grades are displayed in a standardized format:

- **Standard Format**: `N/A (0.00)` 
- **In Percentage Fields**: `0.00`

This standardization applies to all report types:
- ASCII tables
- Markdown tables
- CSV exports
- Boswell Quotient reports

### Effect on Calculations

The system handles N/A grades in specific ways in different contexts:

1. **In Grade Tables**: 
   - Displayed as "N/A (0.00)" with a numeric equivalent of 0.00
   - N/A counts are tracked and displayed separately for analysis
   - Tables include an N/A count row when N/A grades are present

2. **In Bias Analysis**: 
   - Excluded from bias calculations to prevent skewing results
   - System includes fallback handling for empty datasets
   - Uses defensive programming to prevent crashes when all grades are N/A

3. **In Boswell Quotient Calculation**:
   - Models with N/A grades have fewer components in their Boswell Quotient
   - Component is marked as "N/A (0.00)" in reports with consistent formatting
   - The final Boswell Quotient is weighted based on available components only
   - Models with incomplete data show a component count indicator (e.g., "B+ (2/3)")

### Analysis Tools

The system includes an analysis script `analyze_na_handling.py` to examine N/A grade patterns and their effects on the Boswell Quotient calculations. This tool:

- Calculates N/A grade frequency across test runs
- Identifies models more prone to ungradeability
- Analyzes which graders have difficulty extracting grades
- Recommends improvements to grade extraction patterns
- Checks retry mechanisms and their effectiveness

## Grading Bias

The system calculates grading bias to identify models that are consistently lenient or strict:

```python
def calculate_grading_bias(results: Dict[str, Any], models: list) -> Dict[str, Any]:
    """Calculate grading bias for each model."""
    # ...
    # Positive bias means more lenient, negative means stricter
    median_bias = stats["median_given"] - overall_median
    
    # Convert numeric bias to descriptive label
    if abs(median_bias) < 0.15:
        letter_bias = "Neutral"
    elif median_bias > 0:
        if median_bias > 0.6:
            letter_bias = "Very Lenient (+2 grades)"
        # ...
    # ...
```

## Display Precision

All numeric grades and scores are displayed with two decimal places in reports and visualizations for precision.