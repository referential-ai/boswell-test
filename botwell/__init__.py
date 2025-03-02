"""
Botwell - LLM Comparative Analysis Tool

A framework for evaluating and comparing large language models through essay generation,
peer grading, and comprehensive analysis.

This modular implementation:
1. Structures code into logical modules for maintainability
2. Supports concurrent processing for improved performance
3. Provides comprehensive visualization and reporting tools
4. Enables easy domain and model extension
"""

__version__ = "1.0.0"

# Provide convenient imports for users
from botwell.domains import AVAILABLE_DOMAINS
from botwell.models.config import MODELS, FREE_MODELS, PREMIUM_MODELS
from botwell.core.test import run_boswell_test

# Expose main entry point
from botwell.cli import main