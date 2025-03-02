"""
Tokenization utilities for estimating token counts.
"""

def calculate_tokens(text: str) -> int:
    """Estimate the number of tokens in a text string.
    
    This is a rough estimation using a simple rule of thumb:
    - Approximately 4 characters per token for English text
    """
    return max(1, len(text) // 4)