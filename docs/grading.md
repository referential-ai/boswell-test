# Grading System Documentation

## Table of Contents

- [Overview](#overview)
- [Grade Scale](#grade-scale)
- [Grade Conversion Methods](#grade-conversion-methods)
  - [Letter Grade to Numeric Value](#letter-grade-to-numeric-value)
  - [Raw Numeric Scores](#raw-numeric-scores)
  - [Numeric Value to Percentage](#numeric-value-to-percentage)
  - [Percentage to Letter Grade](#percentage-to-letter-grade)
- [Grade Extraction](#grade-extraction)
  - [Primary Extraction Patterns](#primary-extraction-patterns)
  - [Multi-Pass Recovery Strategy](#multi-pass-recovery-strategy)
  - [Semantic Descriptor Matching](#semantic-descriptor-matching)
- [N/A Grade Handling](#na-grade-handling)
  - [When N/A Grades Occur](#when-na-grades-occur)
  - [Logging of N/A Grades](#logging-of-na-grades)
  - [Standardized Display Format](#standardized-display-format)
  - [Effect on Calculations](#effect-on-calculations)
  - [Analysis Tools](#analysis-tools)
- [Individual Grading Files](#individual-grading-files)
  - [File Structure and Location](#file-structure-and-location)
  - [Contents of Grading Files](#contents-of-grading-files)
  - [Benefits of Individual Grading Files](#benefits-of-individual-grading-files)
  - [References in Markdown Files](#references-in-markdown-files)
- [Grading Bias](#grading-bias)
  - [Bias Calculation](#bias-calculation)
  - [Bias Categorization](#bias-categorization)
- [Display Precision](#display-precision)
- [Grade Scale Variations](#grade-scale-variations)
- [Composite Grade Notation](#composite-grade-notation)
  - [Composite Grade Implementation](#composite-grade-implementation)
  - [Usage in Reports](#usage-in-reports)
  - [Grading Prompt Instructions](#grading-prompt-instructions)
- [Raw Numeric Averages](#raw-numeric-averages)
- [Cross-Grading Table Generation](#cross-grading-table-generation)
  - [Excel Table Features](#excel-table-features)
  - [Raw Average Calculation](#raw-average-calculation)

## Overview

The Boswell system uses a standardized grading system to evaluate AI model essays and calculate the Boswell Quotient. This document outlines the grading scale, conversion methods, how raw numeric grades are preserved, and how N/A grades are handled.

## Grade Scale

The system uses a university standard letter grade scale with corresponding numeric values:

| Letter Grade | Numeric Value |
|--------------|---------------|
| A+           | 4.25          |
| A            | 4.0           |
| A-           | 3.75          |
| B+           | 3.25          |
| B            | 3.0           |
| B-           | 2.75          |
| C+           | 2.25          |
| C            | 2.0           |
| C-           | 1.75          |
| D+           | 1.25          |
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
        "B+": 3.25, "B": 3.0, "B-": 2.75,
        "C+": 2.25, "C": 2.0, "C-": 1.75,
        "D+": 1.25, "D": 1.0, "D-": 0.75,
        "F": 0.0,
        "N/A": 0.0
    }
    return grade_map.get(grade, 0.0)
```

### Raw Numeric Scores

The system preserves and displays raw numeric scores with 4 decimal precision to prevent loss of precision when converting between grading systems. Raw scores are handled in several ways:

1. When a grade is extracted, its raw numeric equivalent is stored
2. Raw averages are calculated directly from these numeric values
3. All output formats preserve these raw values in a dedicated "Raw Numeric Average" column

```python
# Calculate raw average directly from numeric scores
raw_grades = [results["grades"][grader][author]["numeric_grade"] 
               for grader in models if grader in results["grades"] 
               and author in results["grades"][grader]]
raw_avg = sum(raw_grades) / len(raw_grades) if raw_grades else 0.0
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

Grades are extracted from feedback text using the `extract_grade()` function, which uses multiple regular expressions to find letter grades in various formats. The system uses a sophisticated approach with fallback mechanisms.

### Primary Extraction Patterns

The system uses 23 different regex patterns organized in order of specificity:

```python
def extract_grade(feedback: str, model_name: str = "Unknown") -> str:
    """Extract letter grade from grading feedback."""
    # First try to match the exact format we requested
    match = re.search(r"Grade:\s*([A-C][+-]?)", feedback)
    if match:
        return match.group(1)
    
    # Fall back to more flexible patterns if the exact format isn't found
    grade_patterns = [
        # Original patterns
        r"([A-C][+-]?)\s*grade",  # "A+ grade" or "B- grade"
        r"grade\s*(?:of|is|:)?\s*([A-C][+-]?)",  # "grade of A" or "grade: B+"
        r"grade\s*[\"']([A-C][+-]?)[\"']",  # grade "A-" or grade 'B'
        r"([A-C][+-]?)$",  # Just the grade at the end of a line
        r"final\s*grade\s*[:\-=]\s*([A-C][+-]?)",  # "final grade: A+"
        r"grade\s*for\s*this\s*essay\s*[:\-=]\s*([A-C][+-]?)",  # "grade for this essay: B"
        r"([A-C][+-]?)\s*grade\s*for\s*this\s*essay",  # "A grade for this essay"
        r"assign\s*a\s*grade\s*of\s*([A-C][+-]?)",  # "assign a grade of B+"
        r"assign\s*([A-C][+-]?)",  # "assign B+"
        r"grade\s*assignment\s*[:\-=]\s*([A-C][+-]?)",  # "grade assignment: A-"
        r"overall\s*grade\s*[:\-=]\s*([A-C][+-]?)",  # "overall grade: C+"
        
        # Enhanced patterns for better coverage
        r"Grade\s*([A-C][+-]?)\s*$",  # For cases ending with just "Grade A" with no punctuation
        r"([A-C][+-]?)\s*grade\s*$",  # For cases ending with "A grade" 
        r"grade[^A-Za-z0-9]*([A-C][+-]?)[^A-Za-z0-9]*$",  # For "grade: [A]" at the end
        r"grade[^:]*?([A-C][+-]?)",  # More flexible pattern without colon
        r"^\s*([A-C][+-]?)\s*$",  # For cases where a line contains just the grade
        r"evaluation.*?([A-C][+-]?)",  # Looking for grades near evaluation-related words
        r"assessment.*?([A-C][+-]?)",  # Looking for grades near assessment-related words
        r"([A-C][+-]?)\s*(?:overall|rating|score)",  # For "A- overall" or similar
        
        # Conclusion section patterns
        r"(?:in\s*conclusion|to\s*conclude|overall|summary|finally).*?([A-C][+-]?)",
        r"([A-C][+-]?)\s*(?:is\s*appropriate|would\s*be\s*fair|seems\s*fair|is\s*a\s*fair\s*assessment)",
        r"(?:deserve|earned|warrants|merits).*?([A-C][+-]?)",
        r"(?:final|overall|appropriate)\s*grade\s*(?:is|would\s*be).*?([A-C][+-]?)"
    ]
    
    # Try each pattern in order of specificity
    for pattern in sorted(grade_patterns, key=len, reverse=True):
        for line in feedback.split('\n'):
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1).upper()  # Normalize to uppercase
```

### Multi-Pass Recovery Strategy

When primary patterns fail, the system employs a multi-pass recovery strategy to extract grades:

```python
# Special multi-pass attempt to recover grade when primary patterns fail
# This is particularly helpful for cases with "Grade:" but no direct grade following
if "Grade:" in feedback or "grade:" in feedback:
    # Find the position of the last "Grade:" mention
    grade_idx = max(feedback.lower().rfind("grade:"), feedback.lower().rfind("grade :"))
    if grade_idx != -1:
        # Check what comes after "Grade:" (50 chars should be enough to find a grade)
        after_grade = feedback[grade_idx:grade_idx+50]
        
        # Look for any letter grade pattern after "Grade:"
        match = re.search(r'[A-C][+-]?', after_grade, re.IGNORECASE)
        if match:
            print(f"  Recovered grade using multi-pass strategy: {match.group(0).upper()}")
            return match.group(0).upper()
```

### Semantic Descriptor Matching

As a last resort, the system uses semantic descriptor matching to infer the grade based on the presence of grade-describing keywords:

```python
# As a last resort, look for grade descriptors to infer the grade
grade_descriptors = {
    "A+": ["exceptional", "outstanding", "excellent", "superb", "flawless", "perfect"],
    "A": ["excellent", "superior", "exceptional", "outstanding", "remarkable"],
    "A-": ["very good", "strong", "impressive", "solid", "thorough"],
    "B+": ["good", "above average", "commendable", "solid", "effective"],
    "B": ["good", "competent", "satisfactory", "acceptable", "adequate"],
    "B-": ["satisfactory", "acceptable", "adequate", "sufficient", "passable"],
    "C+": ["fair", "average", "passable", "moderate", "mediocre"],
    "C": ["average", "passable", "fair", "mediocre", "basic"],
    "C-": ["below average", "minimal", "basic", "weak", "limited"]
}

# Implement semantic descriptor approach
feedback_lower = feedback.lower()
grade_scores = {grade: 0 for grade in grade_descriptors}

for grade, descriptors in grade_descriptors.items():
    for descriptor in descriptors:
        count = feedback_lower.count(descriptor)
        grade_scores[grade] += count

# Find the grade with the highest descriptor count
max_score = max(grade_scores.values())
if max_score > 0:
    # Get all grades with the max score
    best_grades = [grade for grade, score in grade_scores.items() if score == max_score]
    best_grade = best_grades[0]  # Default to first if multiple
    return best_grade
```

This comprehensive approach ensures the highest possible grade extraction rate, significantly reducing N/A grades.

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

- **Letter Grade Format**: `N/A` 
- **Numeric Equivalent**: `0.00`
- **In Percentage Fields**: `0.00` (2 decimal places)

This standardization applies to all report types:
- ASCII tables
- Markdown tables
- CSV exports
- Excel spreadsheets
- Boswell Quotient reports

## Individual Grading Files

In addition to the consolidated JSON results file, the system stores each grading interaction in an individual JSON file. This provides a more granular and accessible way to analyze grading data.

### File Structure and Location

Each grading response is stored as a separate JSON file with the following structure:

```
results/[timestamp]-[domain]/grades/[author]/[grader].json
```

For example, if Claude-3.7-Sonnet grades an essay by Qwen-Max, the grading data will be available at:

```
results/20250306-142820-pol_sci_1/grades/Qwen-Max/Claude-3.7-Sonnet.json
```

### Contents of Grading Files

Each JSON file contains the complete grading interaction, including:

```json
{
  "author": "Qwen-Max",
  "grader": "Claude-3.7-Sonnet",
  "feedback": "# Feedback on 'Strengths and Weaknesses of Global AI Policies...",
  "grade": "A-",
  "numeric_grade": 3.75,
  "cost_info": {
    "input_tokens": 927,
    "output_tokens": 726,
    "input_cost": 0.00046350000000000004,
    "output_cost": 0.001089,
    "total_cost": 0.0015525,
    "duration": 21.27737593650818
  },
  "timestamp": "2025-03-06 14:39:54"
}
```

### Benefits of Individual Grading Files

This approach offers several advantages:

1. **Offline Analysis**: Researchers can analyze individual grading responses without having to parse the monolithic JSON file
2. **Iterative Improvements**: Facilitates iterating on grading prompt design by providing easy access to raw grading data
3. **Debugging**: Makes it easier to identify issues with specific grader/author combinations
4. **Model Comparison**: Enables direct comparison of how different models grade the same essay
5. **Extensibility**: Additional analysis tools can easily process individual files without modifying the core system

### References in Markdown Files

Essay feedback markdown files include references to the corresponding individual grading files:

```markdown
## Graded by: Claude-3.7-Sonnet

[feedback content...]

**Letter Grade:** A-
**Numeric Grade:** 3.75
**Complete grading data:** `grades/Qwen-Max/Claude-3.7-Sonnet.json`
```

This allows users to easily find the complete grading data for further analysis.

### Effect on Calculations

The system handles N/A grades in specific ways in different contexts:

1. **In Grade Tables**: 
   - Displayed as "N/A (0.00)" with a numeric equivalent of 0.00
   - Raw numeric grades preserved with 4 decimal places
   - N/A counts are tracked and displayed separately for analysis
   - Tables include an N/A count row when N/A grades are present

2. **In Bias Analysis**: 
   - Excluded from bias calculations to prevent skewing results
   - Raw numeric scores used for more precise bias calculations
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

The system calculates grading bias to identify models that are consistently lenient or strict. Positive bias values indicate leniency, while negative values indicate strictness.

### Bias Calculation

Bias is calculated as the difference between a model's median given grade and the overall median grade across all models:

- **Median Bias**: The difference between the median grade given by the model and the median of all grades
- **Mean Bias**: The difference between the mean grade given by the model and the mean of all grades

### Bias Categorization

Bias is converted to descriptive labels based on the magnitude of deviation:

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

The system uses multiple levels of precision for different types of data:

- **Letter Grades**: Displayed as-is (e.g., "A+", "B-")
- **Percentages**: Displayed with 2 decimal places (e.g., "93.00")
- **Raw Numeric Grades**: Displayed with 2 decimal places (e.g., "3.75") for consistency
- **Combined Format**: For clarity, some displays show both: "A- (3.75)"

## Grade Scale Variations

The system uses two different grade scales in different contexts:

1. **University Standard Scale** (used in grading.md and most calculations):
   - A+ = 4.25, A = 4.0, A- = 3.75, etc.

2. **GPA Scale** (used in Excel module for certain calculations):
   - A+ = 4.0 (same as A), A- = 3.7, B+ = 3.3, etc.

The GPA scale is used primarily for converting between letter grades and numeric values in the Excel cross-grading table 
generation, while the University Standard Scale is used for the core grading functions.

## Composite Grade Notation

The system now supports composite grade notation for scores that fall exactly between two standard grade points. This provides a more nuanced representation of model performance.

### Composite Grade Implementation

Composite grades are formed by combining two adjacent letter grades when a numeric score falls precisely at their midpoint:

| Numeric Value | Composite Notation | Description |
|---------------|-------------------|-------------|
| 3.875         | A/A-              | Exactly between A (4.0) and A- (3.75) |
| 3.5           | A-/B+             | Exactly between A- (3.75) and B+ (3.25) |
| 3.125         | B+/B              | Exactly between B+ (3.25) and B (3.0) |
| 2.875         | B/B-              | Exactly between B (3.0) and B- (2.75) |

The system uses a small tolerance (±0.01) to determine if a score should receive composite notation:

```python
def numeric_to_composite_grade(numeric_grade: float) -> str:
    """Convert a numeric grade to a composite letter grade notation when applicable."""
    # Standard grade boundaries
    grade_boundaries = {
        4.25: "A+", 4.0: "A", 3.75: "A-",
        3.25: "B+", 3.0: "B", 2.75: "B-",
        # ... other boundaries
    }
    
    # Find surrounding grades
    sorted_boundaries = sorted(grade_boundaries.items(), reverse=True)
    
    for i in range(len(sorted_boundaries) - 1):
        upper_bound, upper_grade = sorted_boundaries[i]
        lower_bound, lower_grade = sorted_boundaries[i + 1]
        
        # If grade falls between two standard boundaries
        if lower_bound < numeric_grade < upper_bound:
            # Calculate midpoint
            midpoint = (upper_bound + lower_bound) / 2
            
            # If the grade is very close to the midpoint (within 0.01)
            # Use composite notation
            if abs(numeric_grade - midpoint) <= 0.01:
                return f"{upper_grade}/{lower_grade}"
            
            # If closer to upper or lower boundary, return that grade
            # ...
```

### Usage in Reports

Composite grade notation is used in:

1. **Raw Numeric to Letter Grade Conversion**: When displaying letter grades derived from raw numeric averages
2. **Median Calculations**: When the median falls exactly between two grade points
3. **Aggregate Statistics**: When showing model performance across multiple domains

This enhanced notation provides more precise differentiation between models with similar performance.
|
| ### Grading Prompt Instructions
| 
| The system instructs LLMs to use composite grade notation for borderline cases through explicit instructions in the grading prompts. For example, the Political Science domain prompt now includes:
| 
| ```
| **Important**: If you believe the essay falls precisely between two grade levels, use a composite grade notation. For example:
| - "A-/B+" for an essay between A- and B+
| - "B+/B" for an essay between B+ and B
| - "A/A-" for an essay between A and A-
| 
| Use this composite notation when you're genuinely torn between two adjacent grades, as it provides more precise evaluation.
| ```
| 
| This explicit instruction accomplishes several goals:
| 
| 1. **Awareness**: Makes LLMs aware that composite grades are a valid option
| 2. **Examples**: Provides clear examples of the expected format (e.g., "A-/B+")
| 3. **Usage Guidance**: Explains when to use composite notation (when "genuinely torn between two adjacent grades")
| 4. **Rationale**: Explains why composite grades are valuable ("provides more precise evaluation")
| 
| Combined with the existing extraction and display capabilities, these prompt instructions ensure that the full precision of the LLMs' judgments is captured in all reports and visualizations.

## Raw Numeric Averages

The system now calculates and prominently displays raw numeric averages in all reports:

1. **Calculation**: Direct mathematical mean of all numeric grades, preserving full precision
2. **Display**: Shown with 2 decimal places in all output formats
3. **Excel Export**: Highlighted with blue background and bold formatting
4. **Column Label**: Clearly labeled as "Raw Numeric Average" 

Raw averages provide a more precise measure than median letter grades, especially when grades cluster near the boundaries between letter grade ranges.

```python
# Example: Excel display with both letter grade and raw numeric value
cell = ws.cell(row=row, column=col)
display_value = f"{grade_value} ({raw_numeric_grade:.2f})"
apply_cell_style(
    cell,
    value=display_value,
    alignment=CENTER_WRAP_ALIGNMENT,
    border=THIN_BORDER
)
```

This approach ensures that no precision is lost when converting between different grading scales and provides users with the most accurate representation of model performance.

## Cross-Grading Table Generation

The system generates cross-grading tables showing how each model graded every other model's essay:

### Excel Table Features

- **Color Coding**: Each cell is color-coded based on the letter grade (green for A+/A, blue for B+/B, etc.)
- **Raw Numeric Display**: Each grade is displayed with its raw numeric value for precision
- **Self-Assessment Highlighting**: Self-grading cells use a distinct background color
- **Median Calculation**: Each row includes the median grade received by that model
- **Raw Average Column**: A dedicated column shows the raw numeric average with 2 decimal precision
- **Grading Bias Row**: Shows each model's grading bias (Lenient, Strict, Neutral)
- **Column Medians**: The bottom row shows median grades given by each model

### Raw Average Calculation

Raw averages are calculated directly from numeric grades with full precision:

```python
exact_raw_average = sum(raw_numeric_grades) / len(raw_numeric_grades) if raw_numeric_grades else 0.0
display_value = f"{exact_raw_average:.2f}" if exact_raw_average > 0 else "N/A"