# Botwell Documentation

This directory contains documentation for the Botwell framework.

## Core Documentation

- [CHANGELOG.md](CHANGELOG.md) - History of all notable changes to the project
- [Project Restructuring Plan](project_restructuring_plan_TODO.md) - Plan and tracking for code reorganization

## Directory Structure

### Framework Components

- [functionality/](functionality/) - Documentation about framework functionality and features
  - [boswell_quotient.md](functionality/boswell_quotient.md) - Details on the Boswell Quotient calculation

- [technical/](technical/) - Technical documentation about implementation details
  - [architecture.md](technical/architecture.md) - Framework modular architecture
  - [caching.md](technical/caching.md) - Caching system implementation
  - [model_interaction.md](technical/model_interaction.md) - Mermaid diagrams of model interactions
  - [code_style.md](technical/code_style.md) - Code style guidelines
  - [development_guide.md](technical/development_guide.md) - Guide for developers
  - [median_calculation.md](technical/median_calculation.md) - Median calculation algorithm
  - [next_steps.md](technical/next_steps.md) - Planned features and improvements
  - [phase2_improvements.md](technical/phase2_improvements.md) - Phase 2 refactoring improvements
  - [evaluation_flowchart.md](technical/evaluation_flowchart.md) - Evaluation process flowchart
  - [na_grade_analysis.md](technical/na_grade_analysis.md) - Analysis of NA grade handling
  - [three_tier_extraction_system.md](technical/three_tier_extraction_system.md) - Grade extraction system

- [usage/](usage/) - Usage guides and examples
  - [quick_start.md](usage/quick_start.md) - Getting started guide
  - [advanced_usage.md](usage/advanced_usage.md) - Advanced usage scenarios
  - [domains.md](usage/domains.md) - Working with test domains

### Package Structure

- **botwell/core/** - Core functionality for the testing framework
- **botwell/models/** - Model management and API interactions
- **botwell/reporting/** - Report generation and visualization
- **botwell/domains/** - Domain definitions for different test scenarios
- **botwell/cmd/** - Command-line interface tools
- **botwell/utils/** - Utility functions and helpers
- **botwell/analysis/** - Grade extraction and response analysis tools
- **botwell/grading/** - Composite grade processing and analysis

## Reference Materials

- [command_reference.md](command_reference.md) - Comprehensive CLI command reference
- [cross_grading_table.md](cross_grading_table.md) - Cross grading table documentation
- [grading.md](grading.md) - Grading methodology documentation
- [model_name_standardization.md](model_name_standardization.md) - Model name standardization rules
- [release_steps.md](release_steps.md) - Release process guidelines

## Main Documentation

- [Project Overview](../README.md) - Main README file with project overview