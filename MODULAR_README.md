# Botwell - Modular Version

## Overview
This is the modular version of the Boswell Test framework, which has been refactored from the original monolithic codebase (`boswell_test.py`). The refactored version follows a cleaner package structure and improved organization.

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

## Usage

### Installation
```bash
# Install in development mode
pip install -e .
```

### Environment Setup
This framework requires an OpenRouter API key to access the language models. Set your API key as an environment variable:

```bash
# Set API key in the terminal
export OPENROUTER_API_KEY="your_api_key_here"

# Or add to your .bashrc or .zshrc for persistence
echo 'export OPENROUTER_API_KEY="your_api_key_here"' >> ~/.bashrc
```

You can obtain an API key at [OpenRouter.ai](https://openrouter.ai/).

### Running the CLI
```bash
# Run directly
python -m botwell --help

# Run after installation
botwell --help
```

### Running Tests
```bash
# Run a simple test with a few free models
python run_simple_test.py

# Run a test with specific models
botwell --domain pol_sci_1 --models "GPT-4o" "Claude-3-Sonnet" "GPT-3.5-Turbo" "Llama-3-8B" "Gemini Pro 1.5"

# Run with free models only
botwell --domain comp_sci_1 --free

# Run tests on all domains with selected models
botwell --all-domains --models "GPT-4o" "Claude-3-Sonnet" "GPT-3.5-Turbo"
```

### List Available Resources
```bash
# List all available models and domains
python list_resources.py
```

### Generate Summary Reports
```bash
# Generate a summary report for the most recent test run
python generate_summary_report.py --latest

# Generate reports for all test runs
python generate_summary_report.py --all

# Generate a report for a specific results directory
python generate_summary_report.py --directory results/20250227-152739-pol_sci_1
```

### Cache Management
```bash
# View cache statistics
python cache_manager.py stats

# Clear expired cache entries
python cache_manager.py clear --expired-only

# Clear all cache entries
python cache_manager.py clear
```

### Create New Domains
```bash
# Create a new domain definition with interactive prompts
python create_domain.py new_domain_1 --interactive

# Create a domain with command-line parameters
python create_domain.py econ_1 --title "Economics - Level 1: Microeconomics" \
  --expertise "Economics" --question "Analyze the pros and cons of price controls..."
```

### Working with Results
After running tests, results are stored in a timestamped directory under `results/`. Here's how to access them:

```bash
# View all results directories
ls -l results/

# Generate a summary report for the most recent test
python generate_summary_report.py --latest

# Explore a specific results directory
cd results/20250227-152739-pol_sci_1/
```

Each results directory contains:
- `essays/` - Individual essay files with grading feedback
- `charts/` - Visualizations of performance, bias, and rankings
- `boswell_report.md` - Comprehensive analysis report
- `summary_report.md` - (If generated) Condensed overview of results
- Various data files (JSON, CSV, markdown tables)

## New Features

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

## Benefits Over Monolithic Version

1. **Maintainability**: Smaller, focused modules are easier to maintain
2. **Testability**: Individual components can be tested separately
3. **Reusability**: Components can be reused in other projects
4. **Extendability**: New features can be added without modifying existing code
5. **Organization**: Clear separation of concerns between different parts of the system