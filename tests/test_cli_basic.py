"""
Simplified tests for Botwell CLI that avoid complex mocks and dependencies.

This module provides basic tests for CLI functionality that can be run reliably
without complex environment setup or command-line argument conflicts.
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO
import os
import sys

# Import the modules we're testing
from botwell.cli import list_models, list_domains
from botwell.cmd.cache_manager import format_size, format_age


class TestCliUtils(unittest.TestCase):
    """Tests for CLI utility functions."""
    
    def test_format_size(self):
        """Test the format_size function for various byte sizes."""
        self.assertEqual(format_size(512), "512 bytes")
        self.assertEqual(format_size(1536), "1.5 KB")
        self.assertEqual(format_size(2 * 1024 * 1024), "2.0 MB")
        self.assertEqual(format_size(3 * 1024 * 1024 * 1024), "3.0 GB")
        
    def test_format_age(self):
        """Test the format_age function for various time durations."""
        self.assertEqual(format_age(30), "30.0 seconds")
        self.assertEqual(format_age(90), "1.5 minutes")
        self.assertEqual(format_age(7200), "2.0 hours")
        self.assertEqual(format_age(172800), "2.0 days")


class TestBasicCliCommands(unittest.TestCase):
    """Tests for basic CLI commands that don't require complex setup."""
    
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_models_all(self, mock_stdout):
        """Test list_models with all models."""
        with patch("botwell.cli.MODELS", [
                {"name": "model1", "model_id": "id1"}, 
                {"name": "model2", "model_id": "id2"}
            ]), \
            patch("botwell.cli.FREE_MODELS", ["model1"]), \
            patch("botwell.cli.PREMIUM_MODELS", ["model2"]):
            list_models(False)
            
            output = mock_stdout.getvalue()
            self.assertIn("Available models", output)
            self.assertIn("model1", output)
            self.assertIn("id1", output)
            self.assertIn("model2", output)
    
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_models_free(self, mock_stdout):
        """Test list_models with only free models."""
        with patch("botwell.cli.MODELS", [
                {"name": "model1", "model_id": "id1"}, 
                {"name": "model2", "model_id": "id2"}
            ]), \
            patch("botwell.cli.FREE_MODELS", ["model1"]), \
            patch("botwell.cli.PREMIUM_MODELS", ["model2"]):
            list_models(True)
            
            output = mock_stdout.getvalue()
            self.assertIn("Available free models", output)
            self.assertIn("model1", output)
            self.assertNotIn("model2", output)
    
    @patch("botwell.cmd.list_resources.main")
    def test_list_domains(self, mock_list_resources_main):
        """Test list_domains command."""
        list_domains()
        mock_list_resources_main.assert_called_once()
    

class TestCreateDomainBasic(unittest.TestCase):
    """Basic tests for the create-domain command functionality."""
    
    @patch("os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_create_domain_file(self, mock_file, mock_makedirs):
        """Test creating a domain file."""
        from botwell.cmd.create_domain import create_domain_file
        
        # Call function with test parameters
        file_path = create_domain_file(
            domain_id="test_domain",
            domain_title="Test Domain",
            domain_description="A domain for testing",
            domain_expertise="Testing Expert",
            essay_question="What is testing?",
            topic_short_name="testing",
            word_count=500
        )
        
        # Verify dirs were created
        mock_makedirs.assert_called_once()
        
        # Verify file was written to
        mock_file.assert_called_once()
        
        # Check content
        file_handle = mock_file()
        written_content = file_handle.write.call_args[0][0]
        
        # Verify the JSON structure has the correct fields
        self.assertIn("Test Domain", written_content)
        self.assertIn("A domain for testing", written_content)
        self.assertIn("Testing Expert", written_content)
        self.assertIn("What is testing?", written_content)
        self.assertIn("500", written_content)


if __name__ == "__main__":
    unittest.main()