"""
Command-line interface for the Botwell test framework.
"""

import argparse
import os
import sys
import time
import json
from typing import List, Dict, Any

from botwell.domains import AVAILABLE_DOMAINS
from botwell.models.config import MODELS, FREE_MODELS, PREMIUM_MODELS
from botwell.cmd.list_resources import main as list_resources_main
from botwell.cmd.cache_manager import main as cache_manager_main
from botwell.cmd.create_domain import main as create_domain_main
from botwell.cmd.generate_summary_report import main as generate_summary_report_main
from botwell.core.test import run_boswell_test


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Boswell Test - LLM Comparative Analysis")
    
    # Main operation modes
    mode_group = parser.add_argument_group("Main operations")
    
    mode_group.add_argument("--all-domains", action="store_true",
                        help="Run tests on all available domains")
    
    mode_group.add_argument("--aggregate-results", action="store_true",
                        help="Generate aggregate statistics from existing results directories")
    
    mode_group.add_argument("--synthesize-essays", action="store_true",
                        help="Synthesize top essays from a domain into a combined essay")
    
    # Utility subcommands
    subparsers = parser.add_subparsers(dest="subcommand", help="Utility commands")
    
    # Cache management subcommand
    cache_parser = subparsers.add_parser("cache", help="Cache management utilities")
    cache_subparsers = cache_parser.add_subparsers(dest="cache_action", help="Cache action to perform")
    
    # Stats subcommand
    stats_parser = cache_subparsers.add_parser("stats", 
                             help="Display cache statistics")
    
    # Clear subcommand
    clear_parser = cache_subparsers.add_parser("clear", 
                              help="Clear the cache (all entries or expired only)")
    clear_parser.add_argument("--expired-only", "-e", action="store_true",
                             help="Clear only expired entries (with 'clear' action)")
    
    # Domain creation subcommand
    domain_parser = subparsers.add_parser("create-domain", help="Create a new domain definition")
    
    # Summary report generation subcommand
    report_parser = subparsers.add_parser("report", help="Generate summary reports for test results")
    report_group = report_parser.add_mutually_exclusive_group(required=True)
    report_group.add_argument("--directory", "-d", type=str,
                             help="Generate report for a specific results directory")
    report_group.add_argument("--all", "-a", action="store_true",
                             help="Generate reports for all results directories")
    report_group.add_argument("--latest", "-l", action="store_true",
                             help="Generate report for the most recent results directory")
    
    # Regular CLI arguments
    parser.add_argument("--domain", type=str, choices=AVAILABLE_DOMAINS.keys(),
                        default="pol_sci_1",
                        help="Domain to test or synthesize (default: pol_sci_1)")
    
    parser.add_argument("--results-dirs", type=str, nargs="+",
                        help="Specific results directories to include in aggregation (default: auto-detect)")
    
    parser.add_argument("--results-dir", type=str,
                        help="Specific results directory to use for essay synthesis")
    
    parser.add_argument("--num-essays", type=int, default=5,
                        help="Number of top essays to synthesize (default: 5)")
    
    parser.add_argument("--synthesis-model", type=str, default="openai/o1",
                        help="Model ID to use for essay synthesis (default: openai/o1). Examples: anthropic/claude-3-opus, openai/gpt-4o")
    
    parser.add_argument("--output", type=str, default="boswell_results.json",
                        help="Output file name (default: boswell_results.json)")
    
    parser.add_argument("--raw", type=str, metavar="FILE",
                        help="Save raw API responses to specified text file")
    
    parser.add_argument("--models", type=str, nargs="+",
                        help="Specific models to test (default: all models)")
    
    parser.add_argument("--free", action="store_true",
                        help="Use only free/widely accessible models, excluding premium models")
    
    parser.add_argument("--skip-verification", action="store_true",
                        help="Skip the model verification step (faster but less reliable)")
    
    parser.add_argument("--max-retries", type=int, default=3,
                        help="Maximum number of retries for API calls (default: 3)")
    
    # Information modes
    parser.add_argument("--list-domains", action="store_true",
                        help="List available domains and exit")
    
    parser.add_argument("--list-models", action="store_true",
                        help="List available models and exit")
    
    # Model management
    parser.add_argument("--update-models", action="store_true",
                        help="Update the local models file with currently available OpenRouter models and exit")
    
    parser.add_argument("--models-file", type=str, default="openrouter_models.json",
                        help="File to save/load OpenRouter models (default: openrouter_models.json)")
    
    return parser.parse_args()


def list_domains() -> None:
    """Display available domains."""
    # Use the modularized list_resources functionality
    from botwell.cmd.list_resources import main as list_resources_main
    list_resources_main()

def list_models(free_only: bool = False) -> None:
    """Display available models.
    
    Args:
        free_only: If True, only list free models
    """
    if free_only:
        print("\nAvailable free models:")
        print("-" * 60)
        for model in MODELS:
            if model['name'] in FREE_MODELS:
                print(f"{model['name']:<25} | {model['model_id']}")
        print(f"\nTotal: {len(FREE_MODELS)} free models")
    else:
        print("\nAvailable models:")
        print("-" * 60)
        for model in MODELS:
            premium = " (premium)" if model['name'] in PREMIUM_MODELS else ""
            print(f"{model['name']:<25} | {model['model_id']}{premium}")
        print(f"\nTotal: {len(MODELS)} models ({len(FREE_MODELS)} free, {len(PREMIUM_MODELS)} premium)")


def main() -> None:
    """Main entry point for the script."""
    args = parse_arguments()
    
    # Check for API key
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY environment variable is not set.")
        print("Please set it with: export OPENROUTER_API_KEY='your-api-key'")
        sys.exit(1)
    
    # Handle information modes
    if args.list_domains:
        list_domains()
        return 0
    
    if args.list_models:
        list_models(args.free)
        return 0
    
    # Handle utility subcommands
    if args.subcommand == "cache":
        if args.cache_action == "stats":
            # Use a clean sys.argv to avoid conflicting arguments
            old_argv = sys.argv
            sys.argv = ["cache_manager", "stats"]
            try:
                cache_manager_main()
            finally:
                sys.argv = old_argv
        elif args.cache_action == "clear":
            # Override sys.argv to pass proper arguments to the cache manager
            old_argv = sys.argv
            sys.argv = ["cache_manager", "clear"]
            if args.expired_only:
                sys.argv.append("--expired-only")
            try:
                cache_manager_main()
            finally:
                sys.argv = old_argv
        return 0
    
    elif args.subcommand == "create-domain":
        # Use a clean sys.argv
        old_argv = sys.argv
        sys.argv = ["create_domain"]
        try:
            create_domain_main()
        finally:
            sys.argv = old_argv
        return 0
    
    elif args.subcommand == "report":
        # Override sys.argv to pass proper arguments to the report generator
        old_argv = sys.argv
        sys.argv = ["generate_summary_report"]
        if args.directory:
            sys.argv.extend(["--directory", args.directory])
        elif args.all:
            sys.argv.append("--all")
        elif args.latest:
            sys.argv.append("--latest")
        try:
            generate_summary_report_main()
        finally:
            sys.argv = old_argv
        return 0
    
    # Handle model management
    if args.update_models:
        from botwell.models.management import update_models_file
        update_models_file(args.models_file)
        return 0
        
    # Handle aggregating existing results
    if args.aggregate_results:
        from botwell.reporting.aggregate import aggregate_existing_results
        print("Aggregating results from previous runs...")
        aggregate_existing_results(args.results_dirs)
        return 0
        
    # Handle synthesizing top essays
    if args.synthesize_essays:
        from botwell.reporting.synthesis import synthesize_top_essays
        print(f"Synthesizing top essays for domain '{args.domain}'...")
        synthesize_top_essays(args.domain, args.results_dir, args.num_essays, args.synthesis_model)
        return 0
    
    # Determine which models to use
    models_to_use = None
    if args.models:
        print(f"Using {len(args.models)} specified models: {', '.join(args.models)}")
        models_to_use = args.models
    elif args.free:
        print(f"Using free models only: {', '.join(FREE_MODELS)}")
        models_to_use = FREE_MODELS
        print("Premium models will be excluded from the test.")
    else:
        print(f"Using all available models")
    
    # Run tests on all domains
    if args.all_domains:
        from botwell.core.test import run_all_domains
        run_all_domains(args)
        return 0
    
    # Run the test on a single domain
    print(f"Starting Boswell Test for domain '{args.domain}'...")
    
    # Run the test with all options
    results = run_boswell_test(
        domain_name=args.domain,
        output_file=args.output,
        selected_models=models_to_use,
        skip_verification=args.skip_verification,
        max_retries=args.max_retries,
        is_free_run=args.free,
        raw_output_file=args.raw
    )
    
    # Print summary
    from botwell.reporting.summary import print_summary
    print_summary(results)
    
    print(f"\nBoswell Test completed!")
    print(f"  - Full results directory: {results['results_dir']}")
    print(f"  - Tables directory: {results['results_dir']}/grades_table.*")
    print(f"  - Essays directory: {results['results_dir']}/essays/")
    print(f"  - Visualizations: {results['results_dir']}/charts/")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())