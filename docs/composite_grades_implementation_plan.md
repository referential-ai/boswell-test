# Composite Grades Implementation Plan

## Overview
This document outlines the implementation plan for supporting composite grade notation (e.g., "A-/B+" for a score of 3.5) in the Boswell grading system. This enhancement will provide more nuanced evaluation and better distinguish between models with similar performance.

## Background
In the current system, numeric grades are mapped to discrete letter grades (A+, A, A-, B+, etc.) without intermediate values. However, academic grading systems often use composite notation for scores that fall exactly between two standard grade points, such as:
- 3.5 (halfway between A- and B+) → "A-/B+"
- 3.125 (halfway between B+ and B) → "B+/B"

Peter has requested this enhancement for future papers to provide finer-grained distinctions between model performances.

## Implementation Details

### 1. New Function in `grading.py`
Add a new function to convert numeric grades to composite grade notation:

```python
def numeric_to_composite_grade(numeric_grade: float) -> str:
    """
    Convert a numeric grade to a composite letter grade notation when applicable.
    
    For grades that fall exactly between two standard grade points (e.g., 3.5),
    returns a composite notation (e.g., "A-/B+"). For grades that are closer to
    a standard grade point, returns the corresponding single letter grade.
    
    Examples:
    - 3.5 (halfway between A- and B+) → "A-/B+"
    - 3.125 (halfway between B+ and B) → "B+/B"
    - 3.8 (closer to A than A-) → "A"
    
    Args:
        numeric_grade: A float representing the numeric grade (0.0-4.25)
        
    Returns:
        A string representing the letter grade or composite grade notation
    """
    # Standard grade boundaries
    grade_boundaries = {
        4.25: "A+", 4.0: "A", 3.75: "A-",
        3.25: "B+", 3.0: "B", 2.75: "B-",
        2.25: "C+", 2.0: "C", 1.75: "C-",
        1.25: "D+", 1.0: "D", 0.75: "D-",
        0.0: "F"
    }
    
    # Check if the grade is exactly at a boundary
    if numeric_grade in grade_boundaries:
        return grade_boundaries[numeric_grade]
    
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
            
            # If closer to upper boundary
            elif numeric_grade > midpoint:
                return upper_grade
            
            # If closer to lower boundary
            else:
                return lower_grade
    
    # Default fallback for any values outside the range
    if numeric_grade > 4.25:
        return "A+"
    else:
        return "F"
```

### 2. Integration Points

The new function will be used in these areas:

1. **Tables and Reports**:
   - Update the cross-grading table generation to include composite grades where applicable
   - Modify the raw numeric average column to show composite grades when appropriate

2. **Visualization**:
   - Update label formatting for charts that display grades
   - Ensure tooltips and legends properly display composite grades

3. **API and Data Structures**:
   - Ensure the JSON output includes composite grade notation
   - Maintain backward compatibility with systems expecting single letter grades

### 3. Testing

1. **Unit Tests**:
   - Create unit tests for the new `numeric_to_composite_grade` function
   - Verify correct conversion of boundary cases (exact midpoints) and non-boundary cases

2. **Integration Tests**:
   - Verify the composite grades appear correctly in generated reports
   - Check that visualization components properly handle composite grades

### 4. Documentation

1. **Update `grading.md`**:
   - Explain the composite grade notation system
   - Provide examples of composite grades and their numeric equivalents

2. **Update Technical Documentation**:
   - Explain implementation details for developers
   - Document any backward compatibility considerations

## Timeline

1. Implementation of core function: 1 day
2. Integration with existing systems: 1-2 days
3. Testing and validation: 1 day
4. Documentation updates: 0.5 day

Total estimated time: 3-4 days

## Future Considerations

- Consider adding a configuration option to enable/disable composite grade notation
- Explore adding confidence intervals or uncertainty visualizations to complement the composite grades
- Investigate more granular scoring systems if additional precision is needed