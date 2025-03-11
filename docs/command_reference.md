# Boswell Test Command Reference

This document provides a reference for all command-line options in the Boswell Test tool.

## Basic Usage

```bash
python -m botwell [options]
```

## General Options

| Option | Description |
| ------ | ----------- |
| `--domain DOMAIN` | Domain to test (default: pol_sci_1) |
| `--output FILE` | Output file name (default: boswell_results.json) |
| `--raw FILE` | Save raw API responses to specified text file |
| `--models MODEL [MODEL ...]` | Specific models to test (default: all models) |
| `--free` | Use only free/widely accessible models |
| `--skip-verification` | Skip the model verification step |
| `--max-retries N` | Maximum number of retries for API calls (default: 3) |

## Main Operation Modes

| Option | Description |
| ------ | ----------- |
| `--all-domains` | Run tests on all available domains |
| `--aggregate-results` | Generate aggregate statistics from existing results directories |
| `--synthesize-essays` | Synthesize top essays from a domain into a combined essay |

## Information Modes

| Option | Description |
| ------ | ----------- |
| `--list-domains` | List available domains and exit |
| `--list-models` | List available models and exit |
| `--update-models` | Update the local models file with currently available OpenRouter models and exit |

## Cache Management

```bash
python -m botwell cache stats
```

```bash
python -m botwell cache clear [--expired-only]
```

## Domain Creation

```bash
python -m botwell create-domain
```

## Summary Report Generation

```bash
python -m botwell report [--directory DIR | --all | --latest]
```

## Examples

Run a test on the default domain with all models:
```bash
python -m botwell
```

Run a test on a specific domain with only free models:
```bash
python -m botwell --domain pol_sci_1 --free
```

Run a test with specific models:
```bash
python -m botwell --models "Claude-3.7-Sonnet" "GPT-4o" "Mistral-Large"
```

Run a test and save raw API responses:
```bash
python -m botwell --domain pol_sci_1 --raw raw_responses.txt
```

Generate a summary report for the latest test:
```bash
python -m botwell report --latest
```

Clear the API response cache:
```bash
python -m botwell cache clear