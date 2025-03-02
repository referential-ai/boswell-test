# Code Style Guidelines

This document outlines the code style guidelines for the Botwell project.

## Python Formatting

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines for Python code
- Use 4 spaces for indentation (no tabs)
- Limit line length to 100 characters
- Use consistent whitespace around operators and after commas
- Include docstrings for all modules, classes, and functions

## Naming Conventions

- **Functions/Variables**: Use `snake_case` for function and variable names
  ```python
  def calculate_boswell_quotient():
      model_scores = {}
  ```

- **Classes**: Use `PascalCase` for class names
  ```python
  class GradeAnalyzer:
      def __init__(self):
          pass
  ```

- **Constants**: Use `UPPER_CASE` for constants
  ```python
  DEFAULT_TIMEOUT = 60
  MAX_RETRIES = 3
  ```

## Import Organization

Group imports in the following order, with a blank line between each group:

1. Standard library imports
2. Third-party library imports
3. Local application imports

Example:
```python
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

import matplotlib.pyplot as plt
import requests

from botwell.core.grading import calculate_grades
from botwell.utils.caching import cache_response
```

## Documentation

- Use docstrings for modules, classes, and functions
- Follow the [Google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for docstrings
- Include type hints where appropriate

Example:
```python
def calculate_grade_average(grades: list[float]) -> float:
    """Calculate the average of a list of grades.
    
    Args:
        grades: A list of numeric grade values
        
    Returns:
        The average grade value
        
    Raises:
        ValueError: If the grades list is empty
    """
    if not grades:
        raise ValueError("Grades list cannot be empty")
    return sum(grades) / len(grades)
```

## Error Handling

- Use specific exceptions rather than catching all exceptions
- Include descriptive error messages
- Use try/except blocks only around code that might raise the specific exception

Example:
```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
except requests.Timeout:
    logger.error(f"Request to {url} timed out after 5 seconds")
    return None
except requests.RequestException as e:
    logger.error(f"Request to {url} failed: {e}")
    return None
```

## Testing

- Write unit tests for core functionality
- Use descriptive test names that explain what's being tested
- Each test should cover a single aspect of functionality

## Concurrency Implementation

- Use `concurrent.futures.ThreadPoolExecutor` for concurrent operations:
  - Model verification (speeds up checking which models are available)
  - Essay generation (each model's essay is generated concurrently)
  - Essay grading (grading tasks run in parallel)
  - Model data processing (when updating available models)
- Add proper locks to prevent race conditions when accessing shared data
- Include error handling and retry logic for all concurrent operations
- Use appropriate concurrency limits to prevent overwhelming the API