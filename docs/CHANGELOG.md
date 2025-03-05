# Changelog

All notable changes to the Botwell project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Command reference documentation with comprehensive list of all CLI commands
- CHANGELOG file to track project changes

### Changed
- Documentation alignment to ensure consistency between main README and docs directory
- Updated command formats across all documentation files to use modular CLI structure

### Fixed
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
  - Nous: DeepHermes 3 Llama 3 8B Preview
  - Google: Gemini models (Flash Lite 2.0 Preview, Pro 2.0 Experimental)

## [1.0.0] - 2025-02-15

### Added
- Initial release of Boswell Test framework
- Implementation of peer-review methodology for LLM evaluation
- Support for multiple testing domains
- Boswell Quotient calculation for comprehensive model ranking
- Visualization and reporting tools
- Support for major LLM providers through OpenRouter