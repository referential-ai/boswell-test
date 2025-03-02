# Architecture

This document describes the modular architecture of the Botwell framework.

## Package Structure

```
botwell/
├── __init__.py        # Package initialization
├── cli.py             # Command-line interface
├── core/              # Core functionality
│   ├── __init__.py
│   ├── files.py       # File operations
│   ├── grading.py     # Grading logic
│   ├── test.py        # Test execution
│   └── verification.py # Model verification
├── domains/           # Domain definitions
│   ├── __init__.py    # Domain loading
│   └── definitions/   # Individual domain files
│       └── ...
├── models/            # Model configurations
│   ├── __init__.py
│   ├── api.py         # API interaction
│   ├── config.py      # Model lists
│   └── management.py  # Model management
├── reporting/         # Report generation
│   ├── __init__.py
│   ├── aggregate.py   # Multi-domain aggregation
│   ├── boswell.py     # Boswell report generation
│   ├── cost.py        # Cost report
│   ├── quotient.py    # Boswell Quotient calculation
│   ├── summary.py     # Summary printing
│   ├── tables.py      # Table generation
│   ├── timing.py      # Timing report
│   └── visualizations.py # Chart generation
└── utils/             # Utilities
    ├── __init__.py
    └── tokenization.py # Token calculation
```

## Key Features

1. Modular code structure making it easier to:
   - Add new domains
   - Add new model providers
   - Customize report generation
   - Add more visualization options
   
2. Updated free models list with 12 additional models:
   - Moonshot AI: Moonlight 16b
   - Nous: DeepHermes 3 Llama 3 8B
   - Google: Gemini Flash Lite 2.0
   - Google: Gemini Pro 2.0 Experimental
   - Dolphin3.0 R1 Mistral 24B
   - DeepSeek: R1
   - Mistral: Mistral Small 3
   - Meta: Llama 3.1 8B Instruct
   - Meta: Llama 3.3 70B Instruct
   - NVIDIA: Llama 3.1 Nemotron 70B
   - Mistral: Mistral Nemo
   - Meta: Llama 3.2 1B Instruct

3. Added results directory tagging with `-free` when tests are run with only free models

4. Created proper importable package structure

5. Added performance optimization with caching:
   - Implemented response caching system to avoid redundant API calls
   - Added cache management tools to view statistics and clear entries
   - Automatic cache invalidation after configurable time periods

6. Enhanced reporting capabilities:
   - Added comprehensive summary report generation
   - Better visualization of results
   - Tools to generate reports for past test runs

7. Added domain creation utilities:
   - Interactive domain creation with guided prompts
   - Templates for consistent domain definitions
   - Command-line or interactive modes for flexibility

## Benefits of Modular Architecture

1. **Maintainability**: Smaller, focused modules are easier to maintain
2. **Testability**: Individual components can be tested separately  
3. **Reusability**: Components can be reused in other projects
4. **Extendability**: New features can be added without modifying existing code
5. **Organization**: Clear separation of concerns between different parts of the system