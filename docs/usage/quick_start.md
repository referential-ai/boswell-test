# Quick Start Guide

Get up and running with the Botwell Test framework in minutes:

## Installation

```bash
# Clone the repository
git clone https://github.com/alanwilhelm/botwell.git
cd botwell

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Configuration

```bash
# Set your API key
export OPENROUTER_API_KEY="your_api_key_here"
```

## Running a Simple Test

```bash
# Run a simple test with free models
botwell --domain pol_sci_1 --free

# Generate a summary report
python generate_summary_report.py --latest
```

## Viewing Results

Results are stored in the `results/` directory in a timestamped folder:

```bash
# List results directories
ls -l results/

# View the Boswell Quotient report
cat results/TIMESTAMP-DOMAIN/boswell_report.md

# Explore the charts
ls -l results/TIMESTAMP-DOMAIN/charts/
```

## Next Steps

- See [advanced_usage.md](advanced_usage.md) for more complex usage scenarios
- Check [models.md](models.md) for information about available models
- Learn about [domains.md](domains.md) for test domains and how to create your own