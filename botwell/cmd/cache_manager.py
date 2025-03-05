#!/usr/bin/env python3
"""
Cache management utility for Botwell.

This module provides commands to manage the API response cache:
1. Clear the entire cache
2. Clear only expired cache entries
3. List cache statistics
"""

import os
import json
import argparse
import time
from pathlib import Path
from typing import Dict, Any, List
import sys

from botwell.utils.caching import ResponseCache


def format_size(size_bytes: int) -> str:
    """Format a byte size into a human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def get_cache_stats(cache_dir: str = ".cache") -> Dict[str, Any]:
    """Get statistics about the cache."""
    # Check if cache directory exists
    if not os.path.exists(cache_dir):
        return {
            "exists": False,
            "entries": 0,
            "size": 0,
            "formatted_size": "0 bytes",
            "oldest": None,
            "newest": None,
            "models": {},
            "prompt_lengths": {"min": 0, "max": 0, "avg": 0}
        }
    
    # Collect stats
    stats = {
        "exists": True,
        "entries": 0,
        "size": 0,
        "oldest": None,
        "newest": None,
        "models": {},
        "prompt_lengths": {"min": float('inf'), "max": 0, "total": 0}
    }
    
    for filename in os.listdir(cache_dir):
        # Skip non-JSON files
        if not filename.endswith('.json'):
            continue
            
        stats["entries"] += 1
        file_path = os.path.join(cache_dir, filename)
        file_size = os.path.getsize(file_path)
        stats["size"] += file_size
        
        # Get file timestamp
        file_time = os.path.getmtime(file_path)
        if stats["oldest"] is None or file_time < stats["oldest"]:
            stats["oldest"] = file_time
        if stats["newest"] is None or file_time > stats["newest"]:
            stats["newest"] = file_time
        
        # Try to load entry and gather model stats
        try:
            with open(file_path, 'r') as f:
                entry = json.load(f)
                
                # Count by model
                model_id = entry.get("model_id", "unknown")
                if model_id not in stats["models"]:
                    stats["models"][model_id] = 0
                stats["models"][model_id] += 1
                
                # Track prompt lengths (from response info)
                if "response" in entry and "usage" in entry["response"]:
                    prompt_tokens = entry["response"]["usage"].get("prompt_tokens", 0)
                    stats["prompt_lengths"]["total"] += prompt_tokens
                    stats["prompt_lengths"]["min"] = min(stats["prompt_lengths"]["min"], prompt_tokens)
                    stats["prompt_lengths"]["max"] = max(stats["prompt_lengths"]["max"], prompt_tokens)
                    
        except (json.JSONDecodeError, IOError):
            # If we can't read the file, just continue
            pass
    
    # Calculate average prompt length
    if stats["entries"] > 0:
        stats["prompt_lengths"]["avg"] = stats["prompt_lengths"]["total"] / stats["entries"]
    else:
        stats["prompt_lengths"]["min"] = 0
        stats["prompt_lengths"]["avg"] = 0
    
    # Format sizes and dates
    stats["formatted_size"] = format_size(stats["size"])
    
    if stats["oldest"]:
        stats["oldest_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stats["oldest"]))
        stats["oldest_age"] = time.time() - stats["oldest"]
    
    if stats["newest"]:
        stats["newest_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stats["newest"]))
        stats["newest_age"] = time.time() - stats["newest"]
    
    return stats


def print_cache_stats(cache_dir: str = ".cache") -> None:
    """Print statistics about the cache."""
    stats = get_cache_stats(cache_dir)
    
    if not stats["exists"]:
        print(f"Cache directory '{cache_dir}' does not exist.")
        return
    
    if stats["entries"] == 0:
        print(f"Cache directory '{cache_dir}' exists but contains no entries.")
        return
    
    print(f"Cache Statistics for '{cache_dir}':")
    print(f"  Entries: {stats['entries']}")
    print(f"  Total Size: {stats['formatted_size']}")
    print(f"  Oldest Entry: {stats.get('oldest_date', 'N/A')} ({format_age(stats.get('oldest_age', 0))} ago)")
    print(f"  Newest Entry: {stats.get('newest_date', 'N/A')} ({format_age(stats.get('newest_age', 0))} ago)")
    print(f"  Average Prompt Tokens: {stats['prompt_lengths']['avg']:.1f}")
    
    # Print model breakdown
    print("\nModel Distribution:")
    for model, count in sorted(stats["models"].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {model}: {count} entries ({count/stats['entries']*100:.1f}%)")


def format_age(seconds: float) -> str:
    """Format an age in seconds to a human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"
    else:
        return f"{seconds/86400:.1f} days"


def clear_cache(cache_dir: str = ".cache", expired_only: bool = False) -> None:
    """Clear the cache."""
    # Create cache manager
    cache = ResponseCache(cache_dir=cache_dir)
    
    # Check if cache directory exists
    if not os.path.exists(cache_dir):
        print(f"Cache directory '{cache_dir}' does not exist.")
        return
    
    # Get stats before clearing
    before_stats = get_cache_stats(cache_dir)
    
    # Clear cache
    if expired_only:
        cleared = cache.clear_expired()
        print(f"Cleared {cleared} expired entries from cache.")
    else:
        cleared = cache.clear_all()
        print(f"Cleared {cleared} entries from cache.")
    
    # Get stats after clearing
    after_stats = get_cache_stats(cache_dir)
    
    # Print change
    freed_space = before_stats["size"] - after_stats["size"]
    print(f"Freed {format_size(freed_space)} of space.")


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for the cache manager."""
    parser = argparse.ArgumentParser(description="Botwell Cache Management Utility")
    
    # Set up subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear the cache")
    clear_parser.add_argument("--expired-only", "-e", action="store_true",
                            help="Clear only expired entries")
    clear_parser.add_argument("--cache-dir", type=str, default=".cache",
                            help="Cache directory (default: .cache)")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show cache statistics")
    stats_parser.add_argument("--cache-dir", type=str, default=".cache",
                            help="Cache directory (default: .cache)")
    
    return parser.parse_args()


def main() -> None:
    """Command-line entry point."""
    args = parse_arguments()
    
    # Default to stats if no command specified
    if not args.command:
        print_cache_stats()
        return
    
    # Execute command
    if args.command == "clear":
        clear_cache(args.cache_dir, args.expired_only)
    elif args.command == "stats":
        print_cache_stats(args.cache_dir)


if __name__ == "__main__":
    main()