"""
Tests for CLI commands in the Botwell framework.

This module contains tests for:
1. cache_manager.py - Cache management utilities
2. create_domain.py - Domain creation utilities
3. list_resources.py - Resource listing utilities 
4. generate_summary_report.py - Report generation utilities
5. Main CLI entry point (cli.py)
"""

import os
import sys
import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock, mock_open, call
from io import StringIO
import shutil

# Import the modules we're testing
from botwell.cmd.cache_manager import (
    get_cache_stats, print_cache_stats, clear_cache, 
    format_size, format_age, main as cache_manager_main,
    parse_arguments as cache_parse_arguments
)
from botwell.cmd.create_domain import (
    create_domain_file, prompt_for_value, 
    interactive_mode, main as create_domain_main
)
from botwell.cmd.list_resources import main as list_resources_main
from botwell.cmd.generate_summary_report import (
    find_result_directories, generate_reports, 
    main as generate_summary_report_main
)
from botwell.domains import AVAILABLE_DOMAINS
from botwell.cli import (
    parse_arguments, list_domains, list_models, main as cli_main
)
from botwell.models.config import MODELS, FREE_MODELS, PREMIUM_MODELS
from botwell.core.test import run_boswell_test, run_all_domains

class TestCacheManager(unittest.TestCase):
    """Tests for the cache_manager.py module."""
    
    def setUp(self):
        """Set up temporary directory for cache tests."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up temporary directory after tests."""
        shutil.rmtree(self.temp_dir)
        
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

    def test_get_cache_stats_empty_dir(self):
        """Test getting stats from a non-existent cache directory."""
        nonexistent_dir = os.path.join(self.temp_dir, "nonexistent")
        stats = get_cache_stats(nonexistent_dir)
        self.assertFalse(stats["exists"])
        self.assertEqual(stats["entries"], 0)
        self.assertEqual(stats["size"], 0)
        
    def test_get_cache_stats_with_entries(self):
        """Test getting stats from a cache directory with entries."""
        # Create a mock cache directory with some entries
        cache_dir = os.path.join(self.temp_dir, "cache")
        os.makedirs(cache_dir, exist_ok=True)
        
        # Create a sample cache entry
        entry = {
            "model_id": "test-model",
            "response": {
                "usage": {
                    "prompt_tokens": 100
                }
            }
        }
        
        # Write sample cache entries
        with open(os.path.join(cache_dir, "entry1.json"), "w") as f:
            json.dump(entry, f)
            
        with open(os.path.join(cache_dir, "entry2.json"), "w") as f:
            json.dump(entry, f)
            
        # Get stats and verify
        stats = get_cache_stats(cache_dir)
        self.assertTrue(stats["exists"])
        self.assertEqual(stats["entries"], 2)
        self.assertGreater(stats["size"], 0)
        self.assertEqual(stats["models"].get("test-model", 0), 2)
        
    @patch("sys.stdout", new_callable=StringIO)
    def test_print_cache_stats(self, mock_stdout):
        """Test printing cache statistics."""
        # Create a mock cache directory
        cache_dir = os.path.join(self.temp_dir, "cache")
        os.makedirs(cache_dir, exist_ok=True)
        
        # Test with empty directory
        print_cache_stats(cache_dir)
        output = mock_stdout.getvalue()
        self.assertIn("exists but contains no entries", output)
        
        # Reset mock
        mock_stdout.truncate(0)
        mock_stdout.seek(0)
        
        # Create sample entry
        entry = {
            "model_id": "test-model",
            "response": {
                "usage": {
                    "prompt_tokens": 100
                }
            }
        }
        with open(os.path.join(cache_dir, "entry1.json"), "w") as f:
            json.dump(entry, f)
            
        # Test with populated directory
        print_cache_stats(cache_dir)
        output = mock_stdout.getvalue()
        self.assertIn("Cache Statistics", output)
        self.assertIn("test-model", output)
        
    @patch("botwell.utils.caching.ResponseCache")
    def test_clear_cache(self, mock_response_cache):
        """Test clearing the cache."""
        # Set up mock cache
        mock_cache_instance = MagicMock()
        mock_cache_instance.clear_all.return_value = 10
        mock_cache_instance.clear_expired.return_value = 5
        mock_response_cache.return_value = mock_cache_instance
        
        # Test clearing all
        with patch("sys.stdout", new_callable=StringIO):
            clear_cache(self.temp_dir, False)
            mock_cache_instance.clear_all.assert_called_once()
            
        # Test clearing expired only
        mock_cache_instance.reset_mock()
        with patch("sys.stdout", new_callable=StringIO):
            clear_cache(self.temp_dir, True)
            mock_cache_instance.clear_expired.assert_called_once()    

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_arguments(self, mock_parse_args):
        """Test the argument parsing for cache manager."""
        cache_parse_arguments()
        mock_parse_args.assert_called_once()
    @patch("botwell.cmd.cache_manager.print_cache_stats")
    def test_main_stats(self, mock_print_stats):
        """Test the main function with stats command."""
        cache_manager_main()
        mock_print_stats.assert_called_once()
        
    @patch("sys.argv", ["cache_manager", "clear"])
    @patch("botwell.cmd.cache_manager.clear_cache")
    def test_main_clear(self, mock_clear_cache):
        """Test the main function with clear command."""
        cache_manager_main()
        mock_clear_cache.assert_called_once_with(".cache", False)
        
    @patch("sys.argv", ["cache_manager", "clear", "--expired-only"])
    @patch("botwell.cmd.cache_manager.clear_cache")
    def test_main_clear_expired(self, mock_clear_cache):
        """Test the main function with clear --expired-only command."""
        cache_manager_main()
        mock_clear_cache.assert_called_once_with(".cache", True)


class TestCreateDomain(unittest.TestCase):
    """Tests for the create_domain.py module."""
    
    def setUp(self):
        """Set up temporary directory for domain creation tests."""
        self.temp_dir = tempfile.mkdtemp()
        # Create a domains/definitions directory structure
        self.definitions_dir = os.path.join(self.temp_dir, "botwell", "domains", "definitions")
        os.makedirs(self.definitions_dir, exist_ok=True)
        
    def tearDown(self):
        """Clean up temporary directory after tests."""
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
        
    def test_prompt_for_value(self):
        """Test prompting for values with and without defaults."""
        # Test with default value
        with patch("builtins.input", return_value=""):
            value = prompt_for_value("Test prompt", "default_value")
            self.assertEqual(value, "default_value")
            
        # Test with user input
        with patch("builtins.input", return_value="user_input"):
            value = prompt_for_value("Test prompt", "default_value")
            self.assertEqual(value, "user_input")
            
        # Test required input (first empty, then valid)
        with patch("builtins.input", side_effect=["", "user_input"]):
            with patch("builtins.print"):
                value = prompt_for_value("Test prompt")
                self.assertEqual(value, "user_input")
                
    @patch("botwell.cmd.create_domain.prompt_for_value")
    def test_interactive_mode(self, mock_prompt):
        """Test interactive mode for domain creation."""
        # Set up mock return values
        mock_prompt.side_effect = [
            "Test Domain",
            "A test domain",
            "Test Expert",
            "What is testing?",
            "testing"
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
        self.assertEqual(result["word_count"], 500)
        self.assertEqual(mock_prompt.call_count, 5)
        
    @patch("sys.argv", ["create_domain", "test_1", "--question", "What is testing?"])
    @patch("botwell.cmd.create_domain.create_domain_file")
    def test_main_with_args(self, mock_create_domain):
        """Test the main function with command line arguments."""
        mock_create_domain.return_value = "/path/to/domain.py"
        
        with patch("sys.stdout", new_callable=StringIO):
            create_domain_main()
            
        # Verify create_domain_file was called with correct args
        mock_create_domain.assert_called_once()
        args = mock_create_domain.call_args[1]
        self.assertEqual(args["domain_id"], "test_1")
        self.assertEqual(args["essay_question"], "What is testing?")
        
    @patch("sys.argv", ["create_domain", "test_1", "--interactive"])
    @patch("botwell.cmd.create_domain.interactive_mode")
    @patch("botwell.cmd.create_domain.create_domain_file")
    def test_main_interactive(self, mock_create_domain, mock_interactive):
        """Test the main function in interactive mode."""
        mock_interactive.return_value = {
            "domain_id": "test_1",
            "domain_title": "Test Domain",
            "domain_description": "A test domain",
            "domain_expertise": "Test Expert",
            "essay_question": "What is testing?",
            "topic_short_name": "testing",
            "word_count": 500
        }
        mock_create_domain.return_value = "/path/to/domain.py"
        
        with patch("sys.stdout", new_callable=StringIO):
            create_domain_main()
            
        # Verify interactive_mode and create_domain_file were called
        mock_interactive.assert_called_once()
        mock_create_domain.assert_called_once()


class TestListResources(unittest.TestCase):
    """Tests for the list_resources.py module."""
    
    @patch("botwell.cmd.list_resources.AVAILABLE_DOMAINS", {"test_1": "Test Domain"})
    @patch("botwell.cmd.list_resources.MODELS", [{"name": "model1", "model_id": "id1"}])
    @patch("botwell.cmd.list_resources.FREE_MODELS", ["model1"])
    @patch("botwell.cmd.list_resources.PREMIUM_MODELS", [])
    @patch("sys.stdout", new_callable=StringIO) 
    def test_main(self, mock_stdout):
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
        self.assertIn("(free)", output)
        
        self.assertIn("Usage information", output)


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
        shutil.rmtree(self.temp_dir)
        
    @patch("os.path.exists")
    @patch("os.listdir")
    @patch("os.path.isdir")
    def test_find_result_directories(self, mock_isdir, mock_listdir, mock_exists):
        """Test finding result directories."""
        # Set up mocks
        mock_exists.return_value = True
        mock_listdir.return_value = [
            "20250227-152739-pol_sci_1",
            "20250227-155124-pol_sci_2",
            "20250227-aggregate",  # Should be excluded
            "invalid_format"       # Should be excluded
        ]
        mock_isdir.return_value = True
        
        # Mock os.path.exists for full_results.json check
        def mock_path_exists(path):
            return "aggregate" not in path and "invalid" not in path
            
        with patch("os.path.exists", side_effect=mock_path_exists):
            dirs = find_result_directories()
            
        # Verify results are sorted correctly (newest first)
        self.assertEqual(len(dirs), 2)
        self.assertIn("20250227-155124-pol_sci_2", dirs[0])
        self.assertIn("20250227-152739-pol_sci_1", dirs[1])
        
    @patch("botwell.reporting.summary_report.create_summary_report_for_results")
    @patch("botwell.cmd.generate_summary_report.find_result_directories")
    @patch("os.path.exists")
    @patch("sys.stdout", new_callable=StringIO)
    def test_generate_reports_specific_directory(self, mock_stdout, mock_exists, 
                                              mock_find_dirs, mock_create_report):
        """Test generating a report for a specific directory."""
        # Set up mocks
        mock_exists.return_value = True
        mock_create_report.return_value = "/path/to/report.md"
        
        # Call function with specific directory
        generate_reports(directory="/path/to/results")
        
        # Verify correct function was called
        mock_create_report.assert_called_once_with("/path/to/results")
        mock_find_dirs.assert_not_called()
        
    @patch("botwell.reporting.summary_report.create_summary_report_for_results")
    @patch("botwell.cmd.generate_summary_report.find_result_directories")
    @patch("sys.stdout", new_callable=StringIO)
    def test_generate_reports_latest(self, mock_stdout, mock_find_dirs, mock_create_report):
        """Test generating a report for the latest directory."""
        # Set up mocks
        mock_find_dirs.return_value = ["/path/to/newest", "/path/to/older"]
        mock_create_report.return_value = "/path/to/report.md"
        
        # Call function with latest flag
        generate_reports(latest=True)
        
        # Verify correct function was called with the newest directory
        mock_create_report.assert_called_once_with("/path/to/newest")
        
    @patch("botwell.reporting.summary_report.create_summary_report_for_results")
    @patch("botwell.cmd.generate_summary_report.find_result_directories")
    @patch("sys.stdout", new_callable=StringIO)
    def test_generate_reports_all(self, mock_stdout, mock_find_dirs, mock_create_report):
        """Test generating reports for all directories."""
        # Set up mocks
        mock_find_dirs.return_value = ["/path/to/dir1", "/path/to/dir2"]
        mock_create_report.return_value = "/path/to/report.md"
        
        # Call function with all_dirs flag
        generate_reports(all_dirs=True)
        
        # Verify create_report was called for each directory
        self.assertEqual(mock_create_report.call_count, 2)
        
    @patch("sys.argv", ["generate_summary_report", "--latest"])
    @patch("botwell.cmd.generate_summary_report.generate_reports")
    def test_main_latest(self, mock_generate_reports):
        """Test the main function with --latest flag."""
        generate_summary_report_main()
        mock_generate_reports.assert_called_once_with(
            directory=None, all_dirs=False, latest=True
        )
        
    @patch("sys.argv", ["generate_summary_report", "--all"])
    @patch("botwell.cmd.generate_summary_report.generate_reports")
    def test_main_all(self, mock_generate_reports):
        """Test the main function with --all flag."""
        generate_summary_report_main()
        mock_generate_reports.assert_called_once_with(
            directory=None, all_dirs=True, latest=False
        )
        
    @patch("sys.argv", ["generate_summary_report", "--directory", "/path/to/results"])
    @patch("botwell.cmd.generate_summary_report.generate_reports")
    def test_main_directory(self, mock_generate_reports):
        """Test the main function with --directory flag."""
        generate_summary_report_main()
        mock_generate_reports.assert_called_once_with(
            directory="/path/to/results", all_dirs=False, latest=False
        )
 

class TestMainCLI(unittest.TestCase):
    """Tests for the main CLI interface in cli.py."""
    
    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_arguments(self, mock_parse_args):
        """Test the command-line argument parsing."""
        mock_args = MagicMock()
        mock_parse_args.return_value = mock_args
        args = parse_arguments()
        self.assertEqual(args, mock_args)

    @patch("sys.argv", ["botwell", "--list-domains"])
    @patch("botwell.cli.list_domains")
    def test_main_list_domains(self, mock_list_domains):
        """Test the main function with --list-domains flag."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            cli_main()
            mock_list_domains.assert_called_once()
            
    @patch("sys.argv", ["botwell", "--list-models"])
    @patch("botwell.cli.list_models")
    def test_main_list_models(self, mock_list_models):
        """Test the main function with --list-models flag."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            cli_main()
            mock_list_models.assert_called_once_with(False)
            
    @patch("sys.argv", ["botwell", "--list-models", "--free"])
    @patch("botwell.cli.list_models")
    def test_main_list_free_models(self, mock_list_models):
        """Test the main function with --list-models --free flags."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            cli_main()
            mock_list_models.assert_called_once_with(True)
            
    @patch("sys.argv", ["botwell", "cache", "stats"])
    @patch("botwell.cmd.cache_manager.main")
    def test_main_cache_stats(self, mock_cache_manager):
        """Test the main function with cache stats subcommand."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            cli_main()
            mock_cache_manager.assert_called_once()
            
    @patch("sys.argv", ["botwell", "cache", "clear", "--expired-only"])
    @patch("botwell.cmd.cache_manager.main")
    def test_main_cache_clear(self, mock_cache_manager):
        """Test the main function with cache clear subcommand."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            cli_main()
            mock_cache_manager.assert_called_once()
            
    @patch("sys.argv", ["botwell", "create-domain"])
    @patch("botwell.cmd.create_domain.main")
    def test_main_create_domain(self, mock_create_domain):
        """Test the main function with create-domain subcommand."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            cli_main()
            mock_create_domain.assert_called_once()
            
    @patch("sys.argv", ["botwell", "report", "--latest"])
    @patch("botwell.cmd.generate_summary_report.main")
    def test_main_report(self, mock_generate_report):
        """Test the main function with report subcommand."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            cli_main()
            mock_generate_report.assert_called_once()
            
    @patch("sys.argv", ["botwell", "--update-models"])
    @patch("botwell.models.management.update_models_file")
    def test_main_update_models(self, mock_update_models):
        """Test the main function with --update-models flag."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            cli_main()
            mock_update_models.assert_called_once()
            
    @patch("sys.argv", ["botwell", "--aggregate-results"])
    @patch("botwell.reporting.aggregate.aggregate_existing_results")
    def test_main_aggregate_results(self, mock_aggregate):
        """Test the main function with --aggregate-results flag."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            cli_main()
            mock_aggregate.assert_called_once()
            
    @patch("sys.argv", ["botwell", "--synthesize-essays"])
    @patch("botwell.reporting.synthesis.synthesize_top_essays")
    def test_main_synthesize_essays(self, mock_synthesize):
        """Test the main function with --synthesize-essays flag."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}): 
            cli_main()
            mock_synthesize.assert_called_once()
            
    @patch("sys.argv", ["botwell", "--domain", "test_domain", "--free"])
    @patch("botwell.core.test.run_boswell_test")
    @patch("botwell.reporting.summary.print_summary")
    def test_main_run_test_free(self, mock_print_summary, mock_run_test):
        """Test the main function with --free flag (running free models)."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            # Set up mock return value
            results = {
                "results_dir": "/path/to/results"
            }
            mock_run_test.return_value = results
            
            cli_main()

            # Verify run_boswell_test and print_summary were called with correct parameters
            mock_run_test.assert_called_once_with(
                domain_name="test_domain",
                output_file="boswell_results.json",
                selected_models=FREE_MODELS,
                skip_verification=False,
                max_retries=3,
                is_free_run=True
            )
            mock_print_summary.assert_called_once_with(results)
    
    @patch("sys.argv", ["botwell", "--domain", "test_domain", "--models", "model1", "model2"])
    @patch("botwell.core.test.run_boswell_test")
    @patch("botwell.reporting.summary.print_summary")
    def test_main_run_test_with_models(self, mock_print_summary, mock_run_test):
        """Test the main function with specific models."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            # Set up mock return value
            results = {
                "results_dir": "/path/to/results"
            }
            mock_run_test.return_value = results
            
            cli_main()

            # Verify run_boswell_test was called with correct parameters
            mock_run_test.assert_called_once_with(
                domain_name="test_domain",
                output_file="boswell_results.json",
                selected_models=["model1", "model2"],
                skip_verification=False,
                max_retries=3,
                is_free_run=False
            )
            mock_print_summary.assert_called_once_with(results)
    
    @patch("sys.argv", ["botwell", "--domain", "test_domain", "--skip-verification"])
    @patch("botwell.core.test.run_boswell_test") 
    @patch("botwell.reporting.summary.print_summary")
    def test_main_run_test_skip_verification(self, mock_print_summary, mock_run_test):
        """Test the main function with skip-verification flag."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            results = {"results_dir": "/path/to/results"}
            mock_run_test.return_value = results
            cli_main()
            mock_run_test.assert_called_once()
            args = mock_run_test.call_args[1]
            self.assertEqual(args["domain_name"], "pol_sci_1")
            self.assertTrue(args["is_free_run"])
            
    @patch("sys.argv", ["botwell", "--all-domains"])
    @patch("botwell.core.test.run_all_domains")
    def test_main_run_all_domains(self, mock_run_all):
        """Test the main function with --all-domains flag."""
        with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key"}):
            cli_main()
            mock_run_all.assert_called_once()
            
    def test_list_models(self):
        """Test the list_models function."""
        # Test listing all models
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            list_models(False)
            output = mock_stdout.getvalue()
            self.assertIn("Available models", output)
    
        # Test listing only free models
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            list_models(True)
            output = mock_stdout.getvalue()
            self.assertIn("Available free models", output)
            self.assertIn("Total:", output)
    
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_no_api_key(self, mock_stdout):
        """Test the main function with no API key."""
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(SystemExit):
                cli_main()
            
            output = mock_stdout.getvalue()
            self.assertIn("Error: OPENROUTER_API_KEY environment variable is not set", output)


if __name__ == "__main__":
    unittest.main()