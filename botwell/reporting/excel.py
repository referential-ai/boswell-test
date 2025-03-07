"""
Excel cross-assessment table generation for Boswell Test results.

This module generates a color-coded Excel spreadsheet with the complete
cross-assessment matrix as seen in Table 1 of the research paper.
"""

import os
import sys
from typing import Dict, Any, List, Optional, Union, Tuple
from botwell.utils import median_of_list
from dataclasses import dataclass
import openpyxl 
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.styles.fonts import DEFAULT_FONT
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell import Cell

# Import grade conversion functions from core module
from botwell.core.grading import grade_to_numeric, median_of_letter_grades, grade_to_percentage, percentage_to_letter_grade

# Define common styles as module-level constants
THIN_BORDER = Border(
    left=Side(style='thin'), 
    right=Side(style='thin'),
    top=Side(style='thin'), 
    bottom=Side(style='thin')
)
CENTER_ALIGNMENT = Alignment(horizontal='center', vertical='center')
LEFT_ALIGNMENT = Alignment(horizontal='left', vertical='center')
MODEL_NAME_FILL = PatternFill(start_color="D0D0D0", end_color="D0D0D0", fill_type="solid")  # Light gray for row headers  # Light gray
HEADER_ROW_FILL = PatternFill(start_color="D0D0D0", end_color="D0D0D0", fill_type="solid")  # Same gray for column headers  # Same gray for headers
BIAS_ROW_FILL = PatternFill(start_color="FFCCCC", end_color="FFCCCC", fill_type="solid")  # Light red
HELVETICA_FONT = Font(name="Helvetica Neue", size=18)  # Data cells at 18pt
HELVETICA_TITLE = Font(name="Helvetica Neue", size=11)  # Title text at 11pt  # All text at 8pt
HELVETICA_BOLD = Font(name="Helvetica Neue", bold=True, size=11)  # Bold 11pt for header/footer rows  # Bold 5pt for header/footer rows
WRAP_ALIGNMENT = Alignment(horizontal='left', vertical='center', wrap_text=True)
CENTER_WRAP_ALIGNMENT = Alignment(horizontal='center', vertical='center', wrap_text=True)  # Use for all cells

# No fill colors for cells
NO_FILL = None

def apply_cell_style(
    cell: Cell, 
    value: Optional[str] = None, 
    alignment: Optional[Alignment] = None, 
    border: Optional[Border] = None,
    font: Optional[Font] = HELVETICA_FONT,
    fill: Optional[PatternFill] = None
) -> Cell:
    """
    Apply common styling to a cell.
    
    Args:
        cell: The cell to style
        value: Optional value to set
        alignment: Optional alignment style
        border: Optional border style (defaults to THIN_BORDER)
        font: Optional font style (defaults to HELVETICA_FONT)
        fill: Optional fill style
        
    Returns:
        The styled cell
    """
    if value is not None:
        cell.value = value
    if alignment is not None:
        cell.alignment = alignment
    if border is not None:
        cell.border = border
    if fill is not None:
        cell.fill = fill
    if font is not None:
        cell.font = font
    return cell

def setup_worksheet_header(
    ws: Worksheet, 
    models: List[str]
) -> Tuple[int, int]:
    """
    Set up the worksheet title and header row.
    
    Args:
        ws: The worksheet to modify
        models: List of model names
        
    Returns:
        Tuple of (median_column_index, header_row_index)
    """
    # Title row removed
    
    # Set column widths
    ws.column_dimensions['A'].width = 20  # Model column
    for i in range(len(models) + 1):  # +1 for median column
        ws.column_dimensions[get_column_letter(i+2)].width = 32/7  # 32px (Excel uses ~7px per unit)
    # Add column for raw numeric average
    ws.column_dimensions[get_column_letter(len(models) + 3)].width = 12  # Raw average column
    
    # Add "Model" header
    apply_cell_style(
       ws.cell(row=1, column=1),
       value="Model",
       alignment=CENTER_WRAP_ALIGNMENT,
       border=THIN_BORDER,
       fill=MODEL_NAME_FILL,
       font=HELVETICA_BOLD
    )
    
    # Add model headers
    for i, model in enumerate(models):
        apply_cell_style(
            ws.cell(row=1, column=i+2),
            value=model,
            alignment=CENTER_WRAP_ALIGNMENT, 
            border=THIN_BORDER,
            font=HELVETICA_BOLD,
            fill=HEADER_ROW_FILL
        )
    
    # Add Median Grade header
    median_col = len(models) + 2
    apply_cell_style(
        ws.cell(row=1, column=median_col),
        value="Median Grade",
        alignment=CENTER_WRAP_ALIGNMENT,
        border=THIN_BORDER,
        font=HELVETICA_BOLD,
        fill=HEADER_ROW_FILL
    )
    
    # Add Raw Average header
    raw_avg_col = len(models) + 3
    apply_cell_style(
        ws.cell(row=1, column=raw_avg_col),
        value="Raw Numeric Average",
        alignment=CENTER_WRAP_ALIGNMENT,
        border=THIN_BORDER,
        font=HELVETICA_BOLD,
        fill=PatternFill(start_color="D9EAF7", end_color="D9EAF7", fill_type="solid")  # Slightly different blue
        )
        
    return median_col, raw_avg_col, 1  # Return median column index, raw average column index, and header row index

def get_grade_with_score(
    results: Dict[str, Any],
    graded_model: str,
    grader_model: str
) -> Tuple[str, str]:
    """
    Get grade and formatted grade value with score.
    
    Args:
        results: Results dictionary
        graded_model: Model being graded
        grader_model: Model doing the grading
        
    Returns:
        Tuple of (grade, formatted_grade_value, raw_numeric_grade)
    """
    try:
        grade = results["grades"][graded_model][grader_model]["grade"]
        # Use the actual numeric grade from results if available, otherwise fall back to mapping
        if "numeric_grade" in results["grades"][graded_model][grader_model]:
            score = results["grades"][graded_model][grader_model]["numeric_grade"]
            raw_numeric_grade = score
        else:
            score = grade_to_numeric(grade)
            raw_numeric_grade = score
        grade_value = grade  # Display only the letter grade without numeric score
        return grade, grade_value, raw_numeric_grade
    except KeyError:
        return "N/A", "N/A", 0.0  # No numeric score

def calculate_median_grade(
    grades: List[str],
    results: Dict[str, Any] = None,
    graded_model: str = None,
    grader_models: List[str] = None
) -> Tuple[str, float, str]:
    """
    Calculate median grade from a list of grades.
    
    Args:
        grades: List of grade letters
        results: Optional results dictionary containing numeric grades
        graded_model: Optional model being graded
        grader_models: Optional list of models who gave the grades (aligned with grades list)
        
    Returns:
        Tuple of (median_grade_letter, median_score, formatted_median_value, raw_average)
    """
    # Track all raw numeric grades for computing mean
    raw_numeric_grades = []
    
    if not grades:
        return "N/A", 0, "N/A", 0.0  # No grades available
    
    # Convert letter grades to numeric scores, using actual numeric grades when available
    scores = []
    # If we have all the necessary information and grader models, get exact scores
    if results and graded_model and grader_models and len(grades) == len(grader_models):
        for i, grade in enumerate(grades):
            grader_model = grader_models[i]
            # Check if this grader has graded this model
            if (grader_model in results["grades"] and 
                graded_model in results["grades"][grader_model] and
                "grade" in results["grades"][grader_model][graded_model]):
                grade_data = results["grades"][grader_model][graded_model]
                if "numeric_grade" in grade_data:
                    scores.append(grade_data["numeric_grade"])
                    raw_numeric_grades.append(grade_data["numeric_grade"])
                else:
                    numeric_grade = grade_to_numeric(grade)
                    scores.append(numeric_grade)
                    raw_numeric_grades.append(numeric_grade)
    # If no scores were found via results (or results not provided), use the mapping
    if not scores:
        scores = [grade_to_numeric(grade) for grade in grades]
        raw_numeric_grades = scores.copy()
    
    scores.sort()
    
    # Calculate median score (could be a decimal if even number of elements)
    median_score = median_of_list(scores)
    
    # Find the closest letter grade for the median score
    median_grade = "N/A"
    
    # Convert the median numeric score to a letter grade using core functions
    if median_score > 0.001:  # Only convert if score is meaningful
        percentage = grade_to_percentage(median_score)
        median_grade = percentage_to_letter_grade(percentage)
    
    # Special case: if the score is very close to 0, it should be N/A
    if abs(median_score) < 0.0001:
        median_grade = "N/A"

    # Calculate raw average
    raw_average = sum(raw_numeric_grades) / len(raw_numeric_grades) if raw_numeric_grades else 0.0
    
    median_value = median_grade  # Display only the letter grade without numeric score  
    return median_grade, median_score, median_value, raw_average

def generate_cross_grading_excel(results: Dict[str, Any], run_dir: str) -> None:
    # Define specific model order
    MODEL_ORDER = [
        "o1-mini",
        "GPT-4o-mini",
        "Claude-3.7-Sonnet",
        "Claude-3-Sonnet",
        "GPT-4o",
        "Gemini Flash 2.0",
        "DeepSeek-Distill-Qwen-32b",
        "Gemini Pro 1.5",
        "grok2-1212",
        "Perplexity: Llama 3.1 Sonar 8B Online",
        "Perplexity: Llama 3.1 Sonar 70B",
        "o1",
        "o3-mini-high",
        "Qwen-Max",
        "Claude-3-Opus",
        "Claude-3.7-Sonnet-thinking",
        "DeepSeek-R1-Full"
    ]
    """
    Generate Excel spreadsheet with color-coded cross-grading matrix.
    
    Args:
        results: The full results dictionary
        run_dir: Directory path where output files should be saved
    """
    try:
        # Validate inputs
        if not isinstance(results, dict) or "essays" not in results:
            raise ValueError("Results dictionary is invalid or missing essays")
        
        if not os.path.isdir(run_dir):
            os.makedirs(run_dir, exist_ok=True)
            
        # Get models list and order them according to MODEL_ORDER
        available_models = set(results["essays"].keys())
        
        # Filter MODEL_ORDER to only include available models
        models = [model for model in MODEL_ORDER if model in available_models]
        
        # Add any models that are in results but not in MODEL_ORDER at the end
        remaining_models = [model for model in available_models if model not in MODEL_ORDER]
        models.extend(sorted(remaining_models))
        
        if not models:
            raise ValueError("No models found in results")
        
        # Create a new Excel workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Cross Grading"
        
        # Set up worksheet header
        median_col, raw_avg_col, header_row = setup_worksheet_header(ws, models)
        
        # Apply Helvetica Neue font to all cells we'll be working with
        for row in range(1, len(models) + 5):  # Add a few extra rows 
            for col in range(1, len(models) + 4):  # Add columns including raw average column
                cell = ws.cell(row=row, column=col)
                if cell.font.name != "Helvetica Neue":  # Only set if not already set
                    cell.font = HELVETICA_FONT
        
        # Fill in the grading matrix
        for i, graded_model in enumerate(models):
            row = i + 2  # Start on row 2
            
            # Add model name in first column
            apply_cell_style(
                ws.cell(row=row, column=1),
                value=graded_model,
                alignment=WRAP_ALIGNMENT,
                border=THIN_BORDER,
                fill=NO_FILL,
                font=HELVETICA_BOLD
            )
            
            # Add grades for each grader
            grades_for_model = []
            grader_models_for_median = []  # Track which graders provided the grades
            raw_numeric_grades = []  # Track raw numeric grades for this model
            
            for j, grader_model in enumerate(models):
                col = j + 2
                
                # Get the grade that grader_model gave to graded_model (including self-assessment)
                grade, grade_value, raw_numeric_grade = get_grade_with_score(results, graded_model, grader_model)
                if grade != "N/A":
                    grades_for_model.append(grade)
                    grader_models_for_median.append(grader_model)
                    raw_numeric_grades.append(raw_numeric_grade)
                
                # Add the grade to the cell
                cell = ws.cell(row=row, column=col)
                # Show only the letter grade without numeric score
                display_value = grade_value
                
                apply_cell_style(
                    cell,
                    value=display_value,
                    alignment=CENTER_WRAP_ALIGNMENT,
                    border=THIN_BORDER,
                    fill=NO_FILL
                )
                
                # Set row height to accommodate text
                ws.row_dimensions[row].height = 32  # 32px height
            
            # Calculate and add median grade
            median_grade, _, median_value, raw_average = calculate_median_grade(
                grades_for_model, 
                results, 
                graded_model,
                grader_models_for_median  # Pass the collected grader models
            )
            
            # Calculate raw average directly to ensure maximum precision
            exact_raw_average = 0.0
            if raw_numeric_grades:
                exact_raw_average = sum(raw_numeric_grades) / len(raw_numeric_grades)
            
            # Add median grade with its numeric equivalent
            cell = ws.cell(row=row, column=median_col)
            # Only show the letter grade
            median_display = median_value
                
            apply_cell_style(
                cell,
                value=median_display,
                alignment=CENTER_WRAP_ALIGNMENT,
                border=THIN_BORDER,
                fill=NO_FILL
            )
            
            # Add the exact raw average to the raw average column with 2 decimal precision
            apply_cell_style(
                ws.cell(row=row, column=raw_avg_col),
                value=f"{exact_raw_average:.2f}" if exact_raw_average > 0 else "N/A",
                alignment=CENTER_WRAP_ALIGNMENT,
                border=THIN_BORDER,
                font=HELVETICA_FONT,  # Use standard 18pt font
                fill=NO_FILL
            )
            
        # Grading Bias row removed
        
        # Add Column Median row
        col_median_row = len(models) + 2
        apply_cell_style(
            ws.cell(row=col_median_row, column=1),
            value="Column Medians",
            alignment=WRAP_ALIGNMENT,
            border=THIN_BORDER,
            fill=HEADER_ROW_FILL,
            font=HELVETICA_BOLD
        )
        
        # Fill in column median data
        for j, grader_model in enumerate(models):
            col = j + 2
            
            # Calculate median for this column
            # Collect all grades given by this grader model
            grades_given = []
            for graded_model in models:
                try:
                    grade_info = results["grades"][graded_model][grader_model]
                    if isinstance(grade_info, dict) and "grade" in grade_info and grade_info["grade"] != "N/A":
                        grades_given.append(grade_info["grade"])
                except KeyError:
                    pass
            
            # Calculate median
            median_grade = "N/A"
            median_value = "N/A"
            descriptive_text = "N/A"
            
            if grades_given:
                median_grade, _, median_value, _ = calculate_median_grade(grades_given)
                
                # Get descriptive text based on median grade
                if median_grade == "A+":
                    descriptive_text = "Excellent"
                elif median_grade in ["A", "A-"]:
                    descriptive_text = "Very Good"
                elif median_grade in ["B+", "B"]:
                    descriptive_text = "Good"
                elif median_grade in ["B-", "C+"]:
                    descriptive_text = "Satisfactory"
                elif median_grade in ["C", "C-"]:
                    descriptive_text = "Average"
                elif median_grade.startswith("D"):
                    descriptive_text = "Below Average"
                elif median_grade == "F":
                    descriptive_text = "Poor"
            
            display_value = f"{median_grade}"
            
            apply_cell_style(
                ws.cell(row=col_median_row, column=col),
                value=display_value,
                alignment=CENTER_WRAP_ALIGNMENT,
                border=THIN_BORDER,
                fill=NO_FILL,
                font=HELVETICA_BOLD
            )
        
        # Add empty cells for median and raw average columns
        apply_cell_style(
            ws.cell(row=col_median_row, column=median_col),
            value="",
            border=THIN_BORDER,
            fill=HEADER_ROW_FILL
        )
        
        apply_cell_style(
            ws.cell(row=col_median_row, column=raw_avg_col),
            value="",
            border=THIN_BORDER,
            fill=HEADER_ROW_FILL
        )
        
        # Save the Excel file
        excel_file = os.path.join(run_dir, "cross_grading_table.xlsx")
        wb.save(excel_file)
        print(f"Generated Excel cross-grading table: {excel_file}")
        
    except Exception as e:
        print(f"Error generating Excel file: {str(e)}")
        if isinstance(e, (KeyError, IndexError, ValueError, TypeError)):
            # More specific error handling for common issues
            print(f"Details: {type(e).__name__} - Check the structure of your results dictionary")
        # Optionally re-raise the exception if needed
        # raise