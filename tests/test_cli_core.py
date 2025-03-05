"""
Tests for core CLI command functionality in the Botwell framework.

This module contains focused tests for:
1. cache_manager.py - Cache management utilities
2. list_resources.py - Resource listing utilities 
3. Main CLI functionality (cli.py)
"""

import os
import sys
import unittest
import json
import time
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO

# Import the modules we're testing
from botwell.cmd.cache_manager import (
    format_size, format_age, get_cache_stats, 
    clear_cache
)
from botwell.cmd.list_resources import main as list_resources_main
from botwell.cli import list_models, list_domains


class TestFormatFunctions(unittest.TestCase):
    """Tests for utility formatting functions."""
    
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


class TestCacheManager(unittest.TestCase):
    """Tests for the cache_manager.py module."""
    
    @patch("os.path.exists")
    def test_get_cache_stats_empty_dir(self, mock_exists):
        """Test getting stats from a non-existent cache directory."""
        mock_exists.return_value = False
        stats = get_cache_stats("/nonexistent")
        self.assertFalse(stats["exists"])
        self.assertEqual(stats["entries"], 0)
        self.assertEqual(stats["size"], 0)
        
    @patch("os.path.exists")
    @patch("os.listdir")
    @patch("os.path.getsize")
    @patch("os.path.getmtime")
    @patch("builtins.open", new_callable=mock_open)
    def test_get_cache_stats_with_entries(self, mock_file, mock_mtime, mock_size, mock_listdir, mock_exists):
        """Test getting stats from a cache directory with entries."""
        # Set up mocks
        mock_exists.return_value = True
        mock_listdir.return_value = ["entry1.json", "entry2.json", "not_json.txt"]
        mock_size.return_value = 1024
        mock_mtime.return_value = time.time() - 3600  # 1 hour ago
        
        # Mock file content
        entry_content = {
            "model_id": "test-model",
            "response": {
                "usage": {
                    "prompt_tokens": 100
                }
            }
        }
        mock_file.return_value.read.return_value = json.dumps(entry_content)
        
        # Get stats and verify
        stats = get_cache_stats("/cache")
        self.assertTrue(stats["exists"])
        self.assertEqual(stats["entries"], 2)  # Should only count JSON files
        self.assertGreater(stats["size"], 0)
        self.assertEqual(stats["models"].get("test-model", 0), 2)
    
    @patch("sys.stdout", new_callable=StringIO)
    def test_clear_cache(self, mock_stdout):
        """Test clearing the cache."""
        temp_dir = "/tmp/cache_test"
        
        # Create a mock for ResponseCache
        mock_cache = MagicMock()
        mock_cache.clear_all.return_value = 10
        mock_cache.clear_expired.return_value = 5
        
        # Setup our test environment
        with patch("botwell.cmd.cache_manager.ResponseCache", return_value=mock_cache), \
                patch("os.path.exists", return_value=True), \
                patch("botwell.cmd.cache_manager.get_cache_stats") as mock_stats:
            
            # Mock the before and after stats 
            mock_stats.side_effect = [
                {"size": 1024, "entries": 10, "exists": True},  # before
                {"size": 0, "entries": 0, "exists": True}       # after
            ]
            
            # Call the function we're testing
            clear_cache(temp_dir, False)
            
            # Verify the right method was called
            mock_cache.clear_all.assert_called_once()


class TestListResources(unittest.TestCase):
    """Tests for the list_resources.py module."""
    
    @patch("botwell.cmd.list_resources.AVAILABLE_DOMAINS", {"test_1": "Test Domain"})
    @patch("botwell.cmd.list_resources.MODELS", [{"name": "model1", "model_id": "id1"}])
    @patch("botwell.cmd.list_resources.FREE_MODELS", ["model1"])
    @patch("botwell.cmd.list_resources.PREMIUM_MODELS", [])
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_resources(self, mock_stdout):
        """Test the main function displays domains and models."""
        list_resources_main()
        output = mock_stdout.getvalue()
        
        # Verify output contains expected information
        self.assertIn("Available domains", output)
        self.assertIn("test_1", output)
        self.assertIn("Test Domain", output)
        
        self.assertIn("Available models", output)
        self.assertIn("model1", output)
        self.assertIn("id1", output)
        self.assertIn("free", output)
        
        self.assertIn("Usage information", output)


class TestMainCLI(unittest.TestCase):
    """Tests for the main CLI interface in cli.py."""
    
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_models(self, mock_stdout):
        """Test the list_models function."""
        # Test listing all models
        with patch("botwell.cli.MODELS", [{"name": "model1", "model_id": "id1"}, 
                                         {"name": "model2", "model_id": "id2"}]), \
             patch("botwell.cli.FREE_MODELS", ["model1"]), \
             patch("botwell.cli.PREMIUM_MODELS", ["model2"]):
            list_models(False)
            output = mock_stdout.getvalue()
            self.assertIn("Available models", output)
            self.assertIn("model1", output)
            self.assertIn("model2", output)
    
        # Test listing only free models
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        with patch("botwell.cli.MODELS", [{"name": "model1", "model_id": "id1"}, 
                                         {"name": "model2", "model_id": "id2"}]), \
             patch("botwell.cli.FREE_MODELS", ["model1"]), \
             patch("botwell.cli.PREMIUM_MODELS", ["model2"]):
            list_models(True)
            output = mock_stdout.getvalue()
            self.assertIn("Available free models", output)
            self.assertIn("model1", output)
            self.assertNotIn("model2", output)
    
    @patch("botwell.cmd.list_resources.main")
    def test_list_domains(self, mock_list_resources):
        """Test the list_domains function."""
        # By examining the cli.py file, we can see that list_domains calls
        # list_resources_main from botwell.cmd.list_resources
        with patch("botwell.cli.list_resources_main", mock_list_resources):
            list_domains()
            mock_list_resources.assert_called_once()


if __name__ == "__main__":
    unittest.main()