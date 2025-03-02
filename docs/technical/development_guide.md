# Development Guide

This document provides guidelines and information for developers working on the Botwell project.

## Environment Setup & Commands
- **Setup environment**: `python -m venv venv && source venv/bin/activate`
- **Install dependencies**: `pip install -e .`
- **Run script**: `python -m botwell` or `botwell` (if installed with pip)

## Project Structure
- Modular package structure in `botwell/` directory
- Entry point via `main.py` and package CLI
- Utility scripts in project root
- Documentation in `docs/` directory
- Test files in `tests/` directory

## Environment Variables
- `OPENROUTER_API_KEY` - Required for API authentication

## Concurrency Implementation
- Uses `concurrent.futures.ThreadPoolExecutor` for:
  - Model verification (speeds up checking which models are available)
  - Essay generation (each model's essay is generated concurrently)
  - Essay grading (grading tasks run in parallel)
  - Model data processing (when updating available models)
- Thread safety with locks to prevent race conditions
- Implementation includes proper error handling and retry logic
- Default concurrency limits prevent overwhelming the API

## Command Line Scripts
The project includes several utility scripts:
- `cache_manager.py` - Manage the caching system
- `create_domain.py` - Create new domain definitions
- `generate_summary_report.py` - Generate summary reports
- `list_resources.py` - List available models and domains
- `run_simple_test.py` - Run a simple test with minimal setup

## Recommendations for Development
1. Always use virtual environment
2. Keep the modular structure clean
3. Add unit tests for new functionality
4. Follow the code style guidelines
5. Update documentation for significant changes