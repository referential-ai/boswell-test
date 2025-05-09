# Advanced Usage Guide

This guide covers more advanced usage scenarios for the Botwell framework.

## Testing with Specific Models

```bash
# Run with specific models
botwell --domain pol_sci_1 --models "GPT-4o" "Claude-3-Opus" "Claude-3.7-Sonnet"
```

## Testing Across All Domains

```bash
# Run tests on all available domains
botwell --all-domains

# Combine with specific models
botwell --all-domains --models "GPT-4o" "Claude-3.7-Sonnet" "GPT-3.5-Turbo" "Llama-3-8B"
```

## Essay Synthesis

Botwell can synthesize the top-performing essays into a single, comprehensive essay:

```bash
# Synthesize essays from top performers
botwell --synthesize-essays --domain pol_sci_1 --synthesis-model anthropic/claude-3-opus --num-essays 4
```

## Model Management

```bash
# Update local models file with available OpenRouter models
botwell --update-models

# Specify custom models file
botwell --update-models --models-file my_models.json
```

## Information Commands

```bash
# List available domains
botwell --list-domains

# List available models
botwell --list-models
```

## Skipping Verification (Faster but Less Reliable)

```bash
# Skip model verification
botwell --skip-verification
```

## Configuring Retry Attempts

```bash
# Configure retry attempts for API calls
botwell --max-retries 5
```

## Output Customization

```bash
# Custom output file (in addition to organized results directory)
botwell --output custom_results.json
```

## Cache Management

```bash
# View cache statistics
botwell cache stats

# Clear expired cache entries
botwell cache clear --expired-only

# Clear all cache entries
botwell cache clear
```

## Creating New Domains

```bash
# Create a new domain definition with interactive prompts
botwell create-domain

# The tool will guide you through the interactive process
# of creating a new domain with appropriate prompts
```

## Working with Results

```bash
# Generate a summary report for the most recent test
botwell report --latest

# Generate reports for all test runs
botwell report --all

# Generate a report for a specific results directory
botwell report --directory results/20250227-152739-pol_sci_1
```