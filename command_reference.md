# Botwell Command Reference

This document provides a comprehensive reference of all available commands in the Botwell framework.

## Basic Usage

| Command | Description |
|---------|-------------|
| `botwell` | Run a test with default settings (pol_sci_1 domain with all verified models) |
| `botwell --domain <domain_name>` | Run a test with a specific domain |
| `botwell --free` | Run a test with only free models |
| `botwell --models "Model1" "Model2" ...` | Run a test with specific models |

## Information Commands

| Command | Description |
|---------|-------------|
| `botwell --list-domains` | List all available test domains |
| `botwell --list-models` | List all available models |
| `botwell --list-models --free` | List only free models |

## Domain Management

| Command | Description |
|---------|-------------|
| `botwell --all-domains` | Run tests on all available domains |
| `botwell create-domain` | Create a new domain definition with interactive prompts |

## Model Management

| Command | Description |
|---------|-------------|
| `botwell --update-models` | Update local models file with available OpenRouter models |
| `botwell --update-models --models-file <file>` | Specify custom models file for updating |
| `botwell --skip-verification` | Skip the model verification step (faster but less reliable) |

## Cache Management

| Command | Description |
|---------|-------------|
| `botwell cache stats` | View cache statistics |
| `botwell cache clear` | Clear all cache entries |
| `botwell cache clear --expired-only` | Clear only expired cache entries |

## Report Generation

| Command | Description |
|---------|-------------|
| `botwell report --latest` | Generate a report for the most recent test results |
| `botwell report --all` | Generate reports for all results directories |
| `botwell report --directory <path>` | Generate a report for a specific results directory |

## Advanced Features

| Command | Description |
|---------|-------------|
| `botwell --max-retries <number>` | Configure retry attempts for API calls |
| `botwell --output <file>` | Specify custom output file for results |
| `botwell --synthesize-essays` | Synthesize top essays into a combined essay |
| `botwell --aggregate-results` | Generate aggregate statistics from existing results |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `OPENROUTER_API_KEY` | Required API key for accessing models |
| `BOTWELL_CACHE_EXPIRATION` | Set cache expiration time in days (default: 7) |
| `BOTWELL_DISABLE_CACHE` | Set to 1 to disable caching entirely |