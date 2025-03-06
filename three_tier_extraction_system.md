# Three-Tier Grade Extraction System & N/A Handling

## Overview

The Boswell grading system now implements a sophisticated three-tier grade extraction approach to minimize N/A grades. This document explains how these methods work together, details their implementation in the code, and discusses the current state of N/A grades in the system.

## The Three Extraction Methods

### 1. Pattern Matching (Primary Method)

**Implementation**: Found in `botwell/core/grading.py` lines 13-60

```python
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
    # ... many more patterns
]

# Try each pattern in order of specificity
for pattern in sorted(grade_patterns, key=len, reverse=True):
    for line in feedback.split('\n'):
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            return match.group(1).upper()  # Normalize to uppercase
```

**Characteristics**:
- Most precise method with lowest false positive rate
- Uses 25+ regex patterns to match different grade formats
- Patterns are sorted by specificity and tried in order
- Works best when models follow explicit formatting guidelines
- Recovers grades from models like Qwen-Max, Claude-3-Sonnet, DeepSeek-R1-Full

### 2. Contextual Analysis (Secondary Method)

**Implementation**: Found in `botwell/core/grading.py` lines 66-79

```python
# Special multi-pass attempt to recover grade when primary patterns fail
if "Grade:" in feedback or "grade:" in feedback:
    # Find the position of the last "Grade:" mention
    grade_idx = max(feedback.lower().rfind("grade:"), feedback.lower().rfind("grade :"))
    if grade_idx != -1:
        # Check what comes after "Grade:" (50 chars should be enough)
        after_grade = feedback[grade_idx:grade_idx+50]
        
        # Look for any letter grade pattern after "Grade:"
        match = re.search(r'[A-C][+-]?', after_grade, re.IGNORECASE)
        if match:
            print(f"  Recovered grade using multi-pass strategy: {match.group(0).upper()}")
            return match.group(0).upper()
```

**Characteristics**:
- Activated only when pattern matching fails
- Locates "Grade:" keywords in the text and examines nearby content
- More flexible than strict pattern matching
- Searches a 50-character window after grading keywords
- Successfully recovers grades from models like Qwen-Plus and Llama-3-8B

### 3. Semantic Descriptor Matching (Final Method)

**Implementation**: Found in `botwell/core/grading.py` lines 81-111

```python
# As a last resort, look for grade descriptors to infer the grade
grade_descriptors = {
    "A+": ["exceptional", "outstanding", "excellent", "superb", "flawless"],
    "A": ["excellent", "superior", "exceptional", "outstanding"],
    "A-": ["very good", "strong", "impressive", "solid", "thorough"],
    "B+": ["good", "above average", "commendable", "solid"],
    # ... other grade descriptors
}

feedback_lower = feedback.lower()
grade_scores = {grade: 0 for grade in grade_descriptors}

for grade, descriptors in grade_descriptors.items():
    for descriptor in descriptors:
        count = feedback_lower.count(descriptor)
        grade_scores[grade] += count

# Find the grade with the highest descriptor count
max_score = max(grade_scores.values())
if max_score > 0:
    best_grades = [grade for grade, score in grade_scores.items() if score == max_score]
    best_grade = best_grades[0]  # Default to first if multiple
    
    print(f"  Recovered grade {best_grade} using semantic descriptor matching")
    return best_grade
```

**Characteristics**:
- Used as a last resort when both previous methods fail
- Maps descriptive words to letter grades
- Counts occurrence frequency of descriptive terms
- Assigns the grade with the most matching descriptors
- Handles cases with no explicit grade by analyzing evaluative language
- Successfully recovers grades from models like o1-mini

## How They Work Together

The extraction methods form a sequential fallback system:

1. Pattern Matching is tried first
2. If that fails, Contextual Analysis is attempted
3. If both fail, Semantic Descriptor Matching is used
4. Only if all three methods fail does the system return "N/A"

```python
# Pattern matching (multiple patterns)
# ... code from lines 13-60 ...

# If pattern matching fails:
if "Grade:" in feedback or "grade:" in feedback:
    # Contextual analysis
    # ... code from lines 66-79 ...

# If contextual analysis fails:
grade_descriptors = { ... }
# Semantic descriptor matching
# ... code from lines 81-111 ...

# Final fallback if all methods fail
return "N/A"
```

This cascading approach maximizes grade recovery with each step becoming more flexible but potentially less precise than the previous.

## N/A Grades in the System

Despite the improved extraction system, N/A grades still appear in result files. There are several reasons for this:

### 1. Empty Columns in Grade Tables

The N/A grades visible in `grades_table.md` (and other formats) appear in specific columns (typically columns 23-27), even though our extraction analysis shows a 0% N/A rate. This discrepancy occurs because:

- These columns represent specific models that might not have been included in the grading process
- The tables use a fixed set of columns for all models, filling empty cells with "N/A (0.00)"
- These are structural N/As rather than extraction failures

### 2. Component Indicators in Boswell Quotient

Several models in the Boswell Quotient reports show "(2/3)" notation, indicating missing components:

```
Google: Gemini Flash Lite 2.0 Preview (free) | 87.81 | B+ (2/3) | 88.24 | N/A (0.00) | 87.38
```

This indicates:
- Only 2 out of 3 Boswell Quotient components were calculated
- The N/A component (with 0.00 value) is included for transparency
- This typically happens when a model couldn't be evaluated across all dimensions

### 3. Code Still Maintains N/A Fallback

The extraction system still has a final fallback to "N/A" if all three methods fail:

```python
# After trying all three methods
return "N/A"  # Grade not found
```

This ensures the system gracefully handles edge cases where even the advanced extraction methods can't determine a grade.

## Implications for System Design

The three-tier extraction system effectively eliminates most N/A grades from the core grading process (as confirmed by the 0% N/A extraction rate). However, the system still maintains N/A as a concept for:

1. **Data Integrity**: Ensuring all models and columns have values in reports
2. **Graceful Failure**: Providing a fallback when extraction is truly impossible
3. **Transparency**: Clearly indicating when components are missing in calculations

Rather than completely removing N/A from the system, the approach has been to:
1. Minimize actual N/A grades through improved extraction
2. Standardize how remaining N/As are displayed and processed

This design provides both robustness in extraction and clarity in reporting.