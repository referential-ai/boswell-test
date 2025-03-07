# Project Restructuring TODO List

This document outlines the specific steps needed to clean up the Boswell project structure by moving files from the root directory into appropriate modules.

## Phase 1: Create New Directories

- [ ] Create botwell/analysis directory
  ```bash
  mkdir -p botwell/analysis
  ```

- [ ] Create botwell/grading directory
  ```bash
  mkdir -p botwell/grading
  ```

- [ ] Create data directories
  ```bash
  mkdir -p data/test_results
  mkdir -p data/raw
  ```

## Phase 2: Move Grade Extraction & Analysis Scripts

- [ ] Move advanced_grade_extraction.py
  ```bash
  git mv advanced_grade_extraction.py botwell/analysis/
  ```

- [ ] Move analyze_grade_responses.py
  ```bash
  git mv analyze_grade_responses.py botwell/analysis/
  ```

- [ ] Move analyze_na_handling.py
  ```bash
  git mv analyze_na_handling.py botwell/analysis/
  ```

- [ ] Move grade_extraction_improved.py
  ```bash
  git mv grade_extraction_improved.py botwell/analysis/
  ```

## Phase 3: Move Composite Grade Scripts

- [ ] Move check_composite_values.py
  ```bash
  git mv check_composite_values.py botwell/grading/
  ```

- [ ] Move count_composite_grades.py
  ```bash
  git mv count_composite_grades.py botwell/grading/
  ```

- [ ] Move find_average_composite_grades.py
  ```bash
  git mv find_average_composite_grades.py botwell/grading/
  ```

- [ ] Move find_composite_grades.py
  ```bash
  git mv find_composite_grades.py botwell/grading/
  ```

- [ ] Move test_composite_grade_conversion.py
  ```bash
  git mv test_composite_grade_conversion.py botwell/grading/
  ```

## Phase 4: Move Test Scripts

- [ ] Move test_composite_extraction.py
  ```bash
  git mv test_composite_extraction.py tests/
  ```

- [ ] Move test_composite_extraction_debug.py
  ```bash
  git mv test_composite_extraction_debug.py tests/
  ```

- [ ] Move test_composite_extraction_verbose.py
  ```bash
  git mv test_composite_extraction_verbose.py tests/
  ```

- [ ] Move test_improved_grading.py
  ```bash
  git mv test_improved_grading.py tests/
  ```

- [ ] Move test_individual_grades.py
  ```bash
  git mv test_individual_grades.py tests/
  ```

## Phase 5: Move Utility Scripts

- [ ] Move standardize_model_names.py
  ```bash
  git mv standardize_model_names.py botwell/utils/
  ```

- [ ] Move create_cross_grading_table.py
  ```bash
  git mv create_cross_grading_table.py botwell/utils/
  ```

## Phase 6: Move JSON Data Files

- [ ] Move larger_test_results.json
  ```bash
  git mv larger_test_results.json data/test_results/
  ```

- [ ] Move simple_test_results.json
  ```bash
  git mv simple_test_results.json data/test_results/
  ```

- [ ] Move test_individual_grades_20250306-143935.json
  ```bash
  git mv test_individual_grades_20250306-143935.json data/test_results/
  ```

## Phase 7: Move Documentation Files

- [ ] Move command_reference.md
  ```bash
  git mv command_reference.md docs/
  ```

- [ ] Move evaluation_flowchart.md
  ```bash
  git mv evaluation_flowchart.md docs/technical/
  ```

- [ ] Move na_grade_analysis.md
  ```bash
  git mv na_grade_analysis.md docs/technical/
  ```

- [ ] Move release_steps.md
  ```bash
  git mv release_steps.md docs/
  ```

- [ ] Move three_tier_extraction_system.md
  ```bash
  git mv three_tier_extraction_system.md docs/technical/
  ```

## Phase 8: Update __init__.py Files

- [ ] Create/update botwell/analysis/__init__.py
  ```python
  # botwell/analysis/__init__.py
  from .advanced_grade_extraction import *
  from .analyze_grade_responses import *
  from .analyze_na_handling import *
  from .grade_extraction_improved import *
  ```

- [ ] Create/update botwell/grading/__init__.py
  ```python
  # botwell/grading/__init__.py
  from .check_composite_values import *
  from .count_composite_grades import *
  from .find_average_composite_grades import *
  from .find_composite_grades import *
  from .test_composite_grade_conversion import *
  ```

- [ ] Update botwell/utils/__init__.py to include new modules
  ```python
  # Add to existing imports in botwell/utils/__init__.py
  from .standardize_model_names import *
  from .create_cross_grading_table import *
  ```

## Phase 9: Update Import Statements

After moving files, we need to update import statements in the moved files:

- [ ] Update imports in botwell/analysis/*.py files
- [ ] Update imports in botwell/grading/*.py files
- [ ] Update imports in moved test files

Example changes:
```python
# Before
from utils import some_function

# After
from botwell.utils import some_function
```

```python
# Before
with open('larger_test_results.json', 'r') as f:
    # ...

# After
with open('data/test_results/larger_test_results.json', 'r') as f:
    # ...
```

## Phase 10: Update setup.py

- [ ] Update setup.py to include new packages
  ```python
  # Add these to the existing 'packages' list in setup.py
  'botwell.analysis',
  'botwell.grading',
  ```

## Phase 11: Testing and Verification

- [ ] Run unit tests
  ```bash
  source .venv/bin/activate
  python -m unittest discover tests
  ```

- [ ] Verify package installation
  ```bash
  pip install -e .
  ```

- [ ] Run a sample test to confirm functionality
  ```bash
  python run_simple_test.py