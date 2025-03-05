# Documentation Update Summary

## Overview

This document summarizes the updates made to align the documentation across the Botwell project, ensuring consistency between the main README.md and the `/docs` directory.

## Identified Issues

1. **Command Structure Discrepancies**:
   - Report generation commands used different formats (`botwell report` vs `python generate_summary_report.py`)
   - Cache management commands used different formats (`botwell cache` vs `python cache_manager.py`)
   - Domain creation commands used different formats (`botwell create-domain` vs `python create_domain.py`)

2. **Content Issues**:
   - References to non-existent `models.md` file in the docs
   - Domain descriptions in `domains.md` didn't match the main README
   - Some documentation didn't reflect the modular architecture

## Updates Made

### 1. Quick Start Guide (`docs/usage/quick_start.md`)
- Updated report generation command to use `botwell report --latest`
- Fixed reference to non-existent models.md file, replacing it with `botwell --list-models` command

### 2. Advanced Usage Guide (`docs/usage/advanced_usage.md`)
- Updated cache management commands to use `botwell cache stats/clear`
- Updated domain creation commands to use `botwell create-domain`
- Updated report generation commands to use `botwell report` format

### 3. Domain Guide (`docs/usage/domains.md`)
- Updated domain descriptions to match the main README
- Updated domain creation section to use `botwell create-domain`
- Removed outdated command line mode for domain creation

### 4. Caching Documentation (`docs/technical/caching.md`)
- Updated cache management commands to use `botwell cache stats/clear`

### 5. Added Visual Documentation
- Created `docs/technical/model_interaction.md` with mermaid diagrams showing:
  - Boswell Test workflow process
  - Model interaction and peer review details
  - Boswell Quotient calculation method

### 6. Created New References
- Created `command_reference.md` with a comprehensive table of all CLI commands
- Added `CHANGELOG.md` to track all notable changes to the project

## Command Reference

The new `command_reference.md` file now provides a single source of truth for all Botwell commands, organized by category:

- Basic Usage
- Information Commands
- Domain Management
- Model Management
- Cache Management
- Report Generation
- Advanced Features
- Environment Variables

## Conclusion

With these updates, the documentation is now consistent across all files, accurately reflects the current CLI implementation, and provides clear guidance for users. The command structure aligns with the modular architecture of the framework.