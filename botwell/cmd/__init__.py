"""
Command-line utilities for Botwell.

This module contains command-line utilities for various Botwell operations:
- cache_manager: Manage the cache (view stats, clear)
- create_domain: Create new domain definition files
- generate_summary_report: Generate summary reports for test results
- list_resources: List available models and domains
"""

from botwell.cmd.cache_manager import main as cache_manager_main
from botwell.cmd.create_domain import main as create_domain_main
from botwell.cmd.generate_summary_report import main as generate_summary_report_main
from botwell.cmd.list_resources import main as list_resources_main

# Export the main functions for easier importing
__all__ = [
    'cache_manager_main',
    'create_domain_main',
    'generate_summary_report_main',
    'list_resources_main',
]