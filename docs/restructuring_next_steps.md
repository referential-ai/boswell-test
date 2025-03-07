# Project Restructuring: Next Steps

Based on the test results, the following issues need to be addressed to complete the project restructuring:

## 1. Update Import Statements

Many files need their import statements updated to reflect the new project structure:

### Imports in Moved Analysis Files

```python
# Before
from utils import median_of_list
import standardize_model_names

# After
from botwell.utils import median_of_list
from botwell.utils.standardize_model_names import standardize_model_name
```

### Imports in Moved Grading Files

```python
# Before
from find_composite_grades import extract_composite_grade
from check_composite_values import check_composite_values

# After
from botwell.grading.find_composite_grades import extract_composite_grade
from botwell.grading.check_composite_values import check_composite_values
```

## 2. Fix File Path References

Update any hardcoded file paths in the code to point to the new file locations:

```python
# Before
with open('simple_test_results.json', 'r') as f:
    # ...

# After
with open('data/test_results/simple_test_results.json', 'r') as f:
    # ...
```

## 3. Fix Test Failures

### Issue: Import Error in test_composite_grades.py

```
ImportError: cannot import name 'numeric_to_composite_grade' from 'botwell.core.grading'
```

Solution: 
- Create or move the `numeric_to_composite_grade` function to botwell/core/grading.py
- Or update the import in tests/test_composite_grades.py to import from the correct location

### Issue: ModuleNotFoundError for boswell_test

```
ModuleNotFoundError: No module named 'boswell_test'
```

Solution:
- Rename any references to the old module name 'boswell_test' to 'botwell'
- Update imports in tests/test_unit.py

### Issue: CLI command tests failing

Multiple command-line interface tests are failing, likely due to changes in paths and structure.

Solution:
- Update mock parameters in test_cli_commands.py to match new paths
- Ensure CLI commands use the correct paths for the restructured project

## 4. Missing Cross-Grading Utility

The test output mentioned running:
```
python create_cross_grading_table.py results/[timestamp]-[domain]/full_results.json
```

But this has been moved to:
```
botwell utils create-cross-grading-table results/[timestamp]-[domain]/full_results.json
```

Solution:
- Create a CLI entry point for the cross-grading table utility
- Update documentation to reflect new command syntax

## 5. Implementation Timeline

1. First fix import statements in core files
2. Next update file path references
3. Then address test failures one by one
4. Finally add any missing CLI commands

We should also update the setup.py file to include new packages and entry points as needed.

## 6. Testing the Changes

After each major change:

```bash
# Run specific tests to verify fixes
python -m unittest tests/test_composite_grades.py
python -m unittest tests/test_unit.py
python -m unittest tests/test_cli_commands.py

# Run all tests
python -m unittest discover tests