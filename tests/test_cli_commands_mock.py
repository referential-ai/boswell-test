"""
Mocked tests for Botwell CLI commands.

This module contains tests that heavily rely on mocking to test the CLI commands:
1. create_domain
2. generate_summary_report
"""

import os
import sys
import unittest
import tempfile
import json
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO
from pathlib import Path

# Import the modules we're testing
from botwell.cmd.create_domain import (
    create_domain_file, interactive_mode
)
from botwell.cmd.generate_summary_report import (
    find_result_directories, generate_reports
)


class TestCreateDomain(unittest.TestCase):
    """Tests for the create_domain.py module."""
    
    def setUp(self):
        """Set up temporary directory for domain creation tests."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up temporary directory after tests."""
        if os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
        
    @patch("os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_create_domain_file(self, mock_file, mock_makedirs):
        """Test creating a domain file."""
        # Call the function with test parameters
        file_path = create_domain_file(
            domain_id="test_1",
            domain_title="Test Domain",
            domain_description="A test domain",
            domain_expertise="Test Expert",
            essay_question="What is testing?",
            topic_short_name="testing",
            word_count=500
        )
        
        # Check that the directories were created
        mock_makedirs.assert_called_once()
        
        # Check that the file was opened for writing
        mock_file.assert_called_once()
        
        # Check file content
        file_handle = mock_file()
        written_content = file_handle.write.call_args[0][0]
        self.assertIn("Test Domain", written_content)
        self.assertIn("A test domain", written_content)
        self.assertIn("Test Expert", written_content)
        self.assertIn("What is testing?", written_content)
        self.assertIn("500", written_content)
        
    @patch("builtins.input")
    def test_interactive_mode(self, mock_input):
        """Test interactive mode for domain creation."""
        # Set up mock return values
        mock_input.side_effect = [
            "Test Domain",  # title
            "A test domain",  # description
            "Test Expert",  # expertise
            "What is testing?",  # question
            "testing"  # topic
        ]
        
        # Create mock args
        args = MagicMock()
        args.domain_id = "test_1"
        args.title = None
        args.description = None
        args.expertise = None
        args.question = None
        args.topic = None
        args.words = 500
        
        # Call interactive mode
        result = interactive_mode(args)
        
        # Verify result
        self.assertEqual(result["domain_id"], "test_1")
        self.assertEqual(result["domain_title"], "Test Domain")
        self.assertEqual(result["domain_description"], "A test domain")
        self.assertEqual(result["domain_expertise"], "Test Expert")
        self.assertEqual(result["essay_question"], "What is testing?")
        self.assertEqual(result["topic_short_name"], "testing")
        self.assertEqual(result["word_count"], 500)


class TestGenerateSummaryReport(unittest.TestCase):
    """Tests for the generate_summary_report.py module."""
    
    def setUp(self):
        """Set up temporary directory for report generation tests."""
        self.temp_dir = tempfile.mkdtemp()
        # Create a results directory structure
        self.results_dir = os.path.join(self.temp_dir, "results")
        os.makedirs(self.results_dir, exist_ok=True)
        
    def tearDown(self):
        """Clean up temporary directory after tests."""
        if os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
    
    @patch("os.path.exists")
    @patch("os.listdir")
    @patch("os.path.isdir")
    def test_find_result_directories(self, mock_isdir, mock_listdir, mock_exists):
        """Test finding result directories."""
        # Set up mocks
        mock_exists.return_value = True  # results base directory exists
        mock_listdir.return_value = [
            "20250227-152739-pol_sci_1",  # Valid format
            "20250227-155124-pol_sci_2",  # Valid format
            "20250227-aggregate",         # Should be excluded (contains "aggregate")
            "invalid_format"              # Should be excluded (invalid format)
        ]
        mock_isdir.return_value = True
        
        # The issue is that we need to handle multiple calls to os.path.exists
        # First call checks if results directory exists, which should return true
        # Later calls check if full_results.json files exist, and should return true for valid directories
        def exists_side_effect(path):
            if path == "results":  # Base results directory
                return True
            elif "full_results.json" in path:  # Check for results file
                # Return True if the path contains a valid directory name
                return "pol_sci_1" in path or "pol_sci_2" in path
            return False
        
        mock_exists.side_effect = exists_side_effect
        dirs = find_result_directories()
        
        # Verify results
        self.assertEqual(len(dirs), 2)
        self.assertTrue("pol_sci_1" in dirs[1])
        self.assertTrue("pol_sci_2" in dirs[0])
    
    @patch("botwell.cmd.generate_summary_report.create_summary_report_for_results")
    @patch("os.path.exists")
    @patch("sys.stdout", new_callable=StringIO)
    def test_generate_reports_specific_directory(self, mock_stdout, mock_exists, mock_create_report):
        """Test generating a report for a specific directory."""
        # Set up mocks
        mock_exists.return_value = True  # Directory exists
        mock_create_report.return_value = "/path/to/report.md"  # Return a report path
        
        # Call function with specific directory
        test_path = "/path/to/results"
        generate_reports(directory=test_path)
        
        # Verify create_summary_report_for_results was called with the correct path
        mock_create_report.assert_called_once_with(test_path)
        
        # Verify output message
        output = mock_stdout.getvalue()
        self.assertIn("Generating summary report", output)
        self.assertIn("Report saved to:", output)


if __name__ == "__main__":
    unittest.main()