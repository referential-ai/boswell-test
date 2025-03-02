"""
Caching utilities for API responses and results.

This module provides functionality to cache API responses and other
expensive computations to improve performance and reduce costs.
"""

import os
import json
import hashlib
from typing import Dict, Any, Optional, Callable
import time
import functools


class ResponseCache:
    """Cache for API responses to avoid redundant calls."""
    
    def __init__(self, cache_dir: str = ".cache", expiration_days: int = 7):
        """
        Initialize the response cache.
        
        Args:
            cache_dir: Directory to store cache files
            expiration_days: Number of days after which cache entries expire
        """
        self.cache_dir = cache_dir
        self.expiration_seconds = expiration_days * 24 * 60 * 60
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, model_id: str, prompt: str) -> str:
        """
        Generate a unique cache key for a model and prompt.
        
        Args:
            model_id: The model identifier
            prompt: The prompt text
        
        Returns:
            A unique cache key based on the model and prompt
        """
        # Create a unique identifier from the model ID and prompt
        combined = f"{model_id}:{prompt}"
        return hashlib.md5(combined.encode('utf-8')).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """
        Get the file path for a cache entry.
        
        Args:
            cache_key: The cache key
            
        Returns:
            The file path for the cache entry
        """
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get(self, model_id: str, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Get a cached response if available and not expired.
        
        Args:
            model_id: The model identifier
            prompt: The prompt text
            
        Returns:
            The cached response or None if not available/expired
        """
        cache_key = self._get_cache_key(model_id, prompt)
        cache_path = self._get_cache_path(cache_key)
        
        # Check if cache file exists
        if not os.path.exists(cache_path):
            return None
            
        # Load cache entry
        try:
            with open(cache_path, 'r') as f:
                cache_entry = json.load(f)
                
            # Check if entry has expired
            if "timestamp" in cache_entry:
                age = time.time() - cache_entry["timestamp"]
                if age > self.expiration_seconds:
                    # Cache has expired
                    return None
                    
            # Return the cached response
            if "response" in cache_entry:
                return cache_entry["response"]
                
        except (json.JSONDecodeError, IOError):
            # If there's any error reading the cache, return None
            return None
            
        return None
    
    def save(self, model_id: str, prompt: str, response: Dict[str, Any]) -> None:
        """
        Save a response to the cache.
        
        Args:
            model_id: The model identifier
            prompt: The prompt text
            response: The response to cache
        """
        cache_key = self._get_cache_key(model_id, prompt)
        cache_path = self._get_cache_path(cache_key)
        
        # Create cache entry with timestamp
        cache_entry = {
            "timestamp": time.time(),
            "model_id": model_id,
            "prompt_hash": hashlib.md5(prompt.encode('utf-8')).hexdigest(),
            "response": response
        }
        
        # Save to cache file
        try:
            with open(cache_path, 'w') as f:
                json.dump(cache_entry, f)
        except IOError as e:
            print(f"Warning: Could not save to cache: {e}")
    
    def clear_expired(self) -> int:
        """
        Clear expired cache entries.
        
        Returns:
            Number of expired entries cleared
        """
        cleared_count = 0
        current_time = time.time()
        
        for filename in os.listdir(self.cache_dir):
            # Skip non-JSON files
            if not filename.endswith('.json'):
                continue
                
            file_path = os.path.join(self.cache_dir, filename)
            
            try:
                with open(file_path, 'r') as f:
                    cache_entry = json.load(f)
                
                # Check if entry has expired
                if "timestamp" in cache_entry:
                    age = current_time - cache_entry["timestamp"]
                    if age > self.expiration_seconds:
                        # Remove expired cache entry
                        os.remove(file_path)
                        cleared_count += 1
                        
            except (json.JSONDecodeError, IOError):
                # If there's any error reading the cache, skip this file
                continue
                
        return cleared_count
    
    def clear_all(self) -> int:
        """
        Clear all cache entries.
        
        Returns:
            Number of entries cleared
        """
        cleared_count = 0
        
        for filename in os.listdir(self.cache_dir):
            # Skip non-JSON files
            if not filename.endswith('.json'):
                continue
                
            file_path = os.path.join(self.cache_dir, filename)
            
            try:
                os.remove(file_path)
                cleared_count += 1
            except IOError:
                # If there's any error removing the file, skip it
                continue
                
        return cleared_count


# Create a global cache instance
response_cache = ResponseCache()


def cached_api_call(func: Callable) -> Callable:
    """
    Decorator to cache API calls.
    
    This decorator will check the cache before making an API call and
    return the cached response if available. Otherwise, it will make the
    API call and cache the response.
    
    Args:
        func: The API call function to decorate
        
    Returns:
        Decorated function that uses caching
    """
    @functools.wraps(func)
    def wrapper(model_id: str, prompt: str, *args, **kwargs):
        # Check if caching is disabled via kwargs
        if kwargs.get('disable_cache', False):
            # Remove disable_cache from kwargs before passing to func
            kwargs.pop('disable_cache', None)
            return func(model_id, prompt, *args, **kwargs)
            
        # Check cache for response
        cached_response = response_cache.get(model_id, prompt)
        if cached_response is not None:
            print(f"Using cached response for {model_id} ({len(prompt)} chars)")
            return cached_response
            
        # Call the original function
        response = func(model_id, prompt, *args, **kwargs)
        
        # Cache the response
        if "error" not in response:
            response_cache.save(model_id, prompt, response)
            
        return response
        
    return wrapper