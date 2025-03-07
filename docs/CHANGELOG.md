# Changelog

All notable changes to the Botwell project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Implemented individual JSON files for each essay's grading responses
- Created `detailed_na_analysis.py` script for deep analysis of N/A grade patterns and causes
- Developed `grade_extraction_improved.py` with enhanced extraction algorithms (57.1% improvement)
- Created `evaluation_flowchart.md` with Mermaid diagram for visualization of the grading process
- Added `implementation_plan.md` with step-by-step integration guide for improved grade extraction
- Added `executive_summary.md` with comprehensive findings on N/A grade handling
- Added `response_to_peter.md` template for addressing reviewer comments
- Created `paper_update_recommendations.md` with specific text suggestions
- Added 8 new regex patterns for improved grade extraction including context-aware patterns
- Added multi-pass extraction strategy with fallback mechanisms for grade detection
- Added contextual analysis for high-confidence grade patterns in conclusion sections

### Changed
- Enhanced grading data storage with per-essay JSON files for easier analysis and offline iteration
- Enhanced grade extraction algorithm with more robust pattern matching
- Improved documentation for N/A grade handling procedures
- Updated implementation approach for grade extraction to use multi-pass strategy
- Refined grading flowchart to clearly indicate N/A assignment process

### Fixed
- Addressed N/A grade extraction issues with enhanced pattern matching
- Improved recovery of missing grades from feedback with ambiguous formats
- Fixed grade detection for models that omit explicit "Grade:" formatting

## [1.2.0] - 2025-03-05
### Added
- Command reference documentation with comprehensive list of all CLI commands
- CHANGELOG file to track project changes
- Added comprehensive grading system documentation in docs/grading.md
- Created analyze_na_handling.py script for analyzing N/A grade patterns
- Added enhanced logging system for failed grade extractions
- Implemented specialized retry mechanism for grade extraction
- Added detailed documentation about N/A grade handling procedures
- Added defensive fallback logic for empty datasets in bias calculations
- Added component count indicator (e.g. "B+ (2/3)") for incomplete Boswell Quotients
- Added detailed analysis in na_grade_analysis.md for diagnosing N/A patterns

### Changed
- Documentation alignment to ensure consistency between main README and docs directory
- Updated command formats across all documentation files to use modular CLI structure
- Updated grade scale to university standard (A+ = 4.25 instead of 4.3)
- Improved precision in Boswell Quotient display (two decimal places)
- Standardized N/A grade display format across all report types (consistent "N/A (0.00)" format)
- Enhanced grade extraction with more robust pattern matching
- Improved error reporting for grade extraction failures
- Added model_name parameter to extract_grade() for better logging

### Fixed
- Fixed handling of N/A values in Boswell Quotient component display
- Fixed handling of N/A grades throughout the system
- Corrected command structure discrepancies in documentation
- Fixed references to non-existent files in documentation
- Updated domain descriptions to match between README and domains.md

## [1.1.0] - 2025-03-01

### Added
- Modular architecture for better maintainability and extensibility
- Response caching system to improve performance and reduce redundant API calls
- Cache management utilities (`botwell cache` commands)
- Domain creation utilities (`botwell create-domain` command)
- Enhanced reporting capabilities
- Essay synthesis feature to combine top-performing essays
- Comprehensive command-line interface for all operations

### Changed
- Restructured package to follow proper Python package conventions
- Refactored code to separate concerns into distinct modules
- Improved documentation structure with categorized guides

### Added Models
- Expanded free model support with 12 additional LLMs:
  - Meta: Llama 3.1 8B Instruct
  - Meta: Llama 3.3 70B Instruct
  - Meta: Llama 3.2 1B Instruct
  - NVIDIA: Llama 3.1 Nemotron 70B Instruct
  - Mistral: Mistral Small 3
  - Mistral: Mistral Nemo
  - DeepSeek: R1
  - Moonshot AI: Moonlight 16b A3b Instruct
  - Nous: DeepHermes 3 Llama-3-8B Preview
  - Google: Gemini models (Flash Lite 2.0 Preview, Pro 2.0 Experimental)

## [1.0.0] - 2025-02-15

### Added
- Initial release of Botwell Test framework
- Implementation of peer-review methodology for LLM evaluation
- Support for multiple testing domains
- Boswell Quotient calculation for comprehensive model ranking
- Visualization and reporting tools
- Support for major LLM providers through OpenRouter