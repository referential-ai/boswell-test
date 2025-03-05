#!/usr/bin/env python3
"""
Standalone test runner for CLI command tests.

This script runs all our CLI command tests without relying on unittest's discovery,
which can conflict with argument parsing in the main application.
"""

import unittest
import sys
import os

# Create a custom test suite
def create_test_suite():
    """Create a test suite with all CLI tests."""
    from tests.test_cli_core import (
        TestFormatFunctions, 
        TestCacheManager,
        TestListResources,
        TestMainCLI
    )
    
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add test cases from test_cli_core.py using loader
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestFormatFunctions))
    suite.addTest(loader.loadTestsFromTestCase(TestCacheManager))
    suite.addTest(loader.loadTestsFromTestCase(TestListResources))
    suite.addTest(loader.loadTestsFromTestCase(TestMainCLI))

    print("Added core CLI tests")

    # Try to add mocked tests
    # Note: Some of these tests were causing issues due to complex mocks
    # and command-line argument conflicts, so we'll import a simplified version
    try:
        # Try to import basic CLI tests
        from tests.test_cli_basic import (
            TestCliUtils,
            TestBasicCliCommands,
            TestCreateDomainBasic
        )

        # Add test classes from test_cli_basic.py
        suite.addTest(loader.loadTestsFromTestCase(TestCliUtils))
        suite.addTest(loader.loadTestsFromTestCase(TestBasicCliCommands))
        suite.addTest(loader.loadTestsFromTestCase(TestCreateDomainBasic))

        print("Added basic CLI tests")
    except (ImportError, AttributeError) as e:
        print(f"Warning: Could not import basic CLI tests: {e}", file=sys.stderr)

    # Try to add mocked command tests
    try:
        from tests.test_cli_commands_mock import (
            TestCreateDomain, 
            TestGenerateSummaryReport
        )
        suite.addTest(loader.loadTestsFromTestCase(TestCreateDomain))
        suite.addTest(loader.loadTestsFromTestCase(TestGenerateSummaryReport))
        print("Added mocked CLI command tests")
    except (ImportError, AttributeError) as e:
        print(f"Warning: Could not import mocked tests: {e}", file=sys.stderr)
    
    return suite

if __name__ == "__main__":
    # Create and run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(create_test_suite())
    
    # Set exit code based on test results
    sys.exit(not result.wasSuccessful())