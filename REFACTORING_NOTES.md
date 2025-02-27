# Botwell Test Refactoring Notes

This document outlines a plan for refactoring the Botwell Test codebase to improve maintainability, testability, and extensibility.

## Proposed Module Structure

The main `boswell_test.py` file has grown quite large and should be split into multiple modules with clear responsibilities:

```
botwell/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── api.py             # API interaction (OpenRouter)
│   ├── models.py          # Data structures/classes
│   ├── prompts.py         # Default prompts and templates
│   └── config.py          # Configuration settings
├── analysis/
│   ├── __init__.py
│   ├── grading.py         # Grade extraction and processing
│   ├── boswell.py         # Boswell Quotient calculation
│   ├── aggregation.py     # Cross-domain aggregation
│   └── stats.py           # Statistical analysis
├── reporting/
│   ├── __init__.py
│   ├── tables.py          # Table generation (ASCII, Markdown, CSV)
│   ├── visualization.py   # Chart generation
│   ├── boswell_report.py  # Boswell Quotient reports
│   └── formatters.py      # Formatting utilities
├── domains/               # Domain definition modules
│   ├── __init__.py
│   ├── comp_sci_1.py
│   ├── comp_sci_2.py
│   ├── pol_sci_1.py
│   └── pol_sci_2.py
├── utils/
│   ├── __init__.py
│   ├── logging.py        # Logging utilities
│   └── concurrency.py    # Concurrency helpers
├── cli.py                # Command-line interface
└── main.py               # Main execution logic
```

## Refactoring Steps

1. **Extract API functionality**:
   - Move OpenRouter API calls to a dedicated module
   - Create model clients with proper error handling
   - Add support for additional API providers

2. **Implement Core Data Structures**:
   - Create Model, Essay, Grade, Domain classes
   - Implement proper validation and type hints
   - Improve serialization/deserialization

3. **Separate Analysis Logic**:
   - Extract grading bias calculations
   - Extract Boswell Quotient calculations
   - Create utility functions for statistics

4. **Improve Reporting**:
   - Create a proper Reporting class hierarchy
   - Support multiple output formats
   - Make visualizations more configurable

5. **Create a Proper CLI Interface**:
   - Use a more robust CLI library (e.g., Click or Typer)
   - Add better help documentation
   - Implement proper logging levels

## Testing Strategy

- **Unit Tests**: Test each component in isolation
  - API interaction (with mocks)
  - Data processing
  - Report generation

- **Integration Tests**: Test interactions between components
  - End-to-end test with small domains
  - Test data flow between components

- **Property-Based Tests**:
  - Test that Boswell Quotient maintains relative ordering
  - Test consistency across multiple runs

## Future Enhancements

1. **Domain Registry**:
   - Allow dynamic registration of domains
   - Support pluggable domain modules

2. **Result Database**:
   - Store results in a database for comparison
   - Track model performance over time

3. **Web Interface**:
   - Create a web dashboard for results
   - Interactive visualizations

4. **API Mode**:
   - Expose functionality through a REST API
   - Allow programmatic access to test results

5. **Advanced Analysis**:
   - Implement more sophisticated statistical analysis
   - Add confidence intervals for model comparisons
   - Detect anomalies in grading patterns