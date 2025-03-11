"""
Utility for writing raw API responses to a file.

This module provides thread-safe functions for writing raw API responses to a text file.
"""

import time
import json
from threading import Lock
from typing import Dict, Any, Optional, TextIO

# Thread safety lock for file operations
_file_lock = Lock()
_output_file: Optional[TextIO] = None


def initialize_raw_output(filename: str) -> None:
    """Initialize the raw output file.
    
    Args:
        filename: The path to the file where raw responses will be written
    """
    global _output_file
    
    with _file_lock:
        if _output_file is not None:
            # File is already open, close it first
            _output_file.close()
        
        # Open file in write mode to clear any existing content
        _output_file = open(filename, 'w', encoding='utf-8')
        _output_file.write(f"==== BOSWELL TEST RAW API RESPONSES - STARTED AT {time.strftime('%Y-%m-%d %H:%M:%S')} ====\n\n")
        _output_file.flush()


def write_raw_response(
    request_type: str,
    model_name: str,
    prompt: str,
    response: Dict[str, Any],
    additional_info: Dict[str, Any] = None
) -> None:
    """Write a raw API response to the output file in a human-readable format.
    
    Args:
        request_type: The type of request (e.g., "Essay Generation", "Grading")
        model_name: The name of the model that generated the response
        prompt: The prompt that was sent to the model
        response: The raw API response
        additional_info: Optional additional information to include
    """
    global _output_file
    
    if _output_file is None:
        # No file has been initialized
        return
    
    with _file_lock:
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Format the response in a readable way
            _output_file.write(f"==== API CALL: {timestamp} ====\n")
            _output_file.write(f"MODEL: {model_name}\n")
            _output_file.write(f"TYPE: {request_type}\n")
            
            if additional_info:
                for key, value in additional_info.items():
                    _output_file.write(f"{key.upper()}: {value}\n")
            
            _output_file.write("\nPROMPT:\n")
            _output_file.write(prompt)
            _output_file.write("\n\nRESPONSE:\n")
            
            # Format the full response as pretty-printed JSON, then convert to string
            # This makes the raw output more readable
            response_str = json.dumps(response, indent=2)
            _output_file.write(response_str)
            
            _output_file.write("\n\n==== END OF RESPONSE ====\n\n")
            _output_file.flush()
        
        except Exception as e:
            # Log error but don't crash the program
            _output_file.write(f"\nERROR WRITING RAW RESPONSE: {str(e)}\n\n")
            _output_file.flush()


def close_raw_output() -> None:
    """Close the raw output file if it's open."""
    global _output_file
    
    with _file_lock:
        if _output_file is not None and not _output_file.closed:
            _output_file.write(f"\n==== BOSWELL TEST RAW API RESPONSES - ENDED AT {time.strftime('%Y-%m-%d %H:%M:%S')} ====\n")
            _output_file.close()
            _output_file = None