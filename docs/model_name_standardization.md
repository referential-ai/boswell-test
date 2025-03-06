# Model Name Standardization Guide

This document provides the official, standardized names for all models referenced in the paper. Use these exact formats to ensure consistency throughout.

## Definitive Model Name List

| Family | Official Full Name | Notes |
|--------|-------------------|-------|
| **OpenAI Models** |
| | GPT-4o | Not "GPT4o", "GPT4-o", or "GPT-4-o" |
| | GPT-4o-mini | Include hyphen and lowercase "mini" |
| | GPT-3.5-Turbo | Include both hyphens and "Turbo" capitalized |
| **Anthropic Models** |
| | Claude-3-Opus | Include hyphens, not "Claude 3 Opus" |
| | Claude-3-Sonnet | Include hyphens, not "Claude 3 Sonnet" |
| | Claude-3.7-Sonnet | Note the decimal in version number |
| | Claude-3.7-Sonnet-thinking | This is a distinct model from Claude-3.7-Sonnet |
| **Perplexity Models** |
| | Perplexity: Llama 3.1 Sonar 70B | Include colon, spaces, and full version numbers |
| | Perplexity: Llama 3.1 Sonar 8B Online | Note "Online" suffix is part of official name |
| **Meta Models** |
| | Llama-3-8B | Include hyphens, not "Llama 3 8B" |
| **Google Models** |
| | Gemini Flash 2.0 | Include space and version number |
| | Gemini Pro 1.5 | Include space and version number |
| **DeepSeek Models** |
| | DeepSeek-R1-Full | Include hyphens |
| | DeepSeek-Distill-Qwen-32b | Include hyphens and lowercase "b" in size |
| **Qwen Models** |
| | Qwen-Max | Include hyphen |
| | Qwen-Plus | Include hyphen |
| | Qwen-Turbo | Include hyphen |
| **Anthropic Models** |
| | o1 | Lowercase "o" followed by number without space |
| | o1-mini | Include hyphen and lowercase "mini" |
| | o3-mini-high | Include both hyphens, lowercase "mini" and "high" |
| **Misc Models** |
| | grok-beta | Lowercase "g", include hyphen |
| | grok2-1212 | Lowercase "g", include hyphen, include version number |

## Formatting Guidelines

1. **Capitalization**: Preserve the exact capitalization shown above
2. **Hyphens vs. Spaces**: Use the exact punctuation shown above
3. **Version Numbers**: Always include the full version number
4. **Abbreviations**: Don't abbreviate model names (e.g., don't use "Claude" instead of "Claude-3-Opus")

## Usage Examples

### Correct:
- "Claude-3.7-Sonnet-thinking achieved the highest score..."
- "Both GPT-4o and Perplexity: Llama 3.1 Sonar 70B performed well..."

### Incorrect:
- "Claude thinking achieved the highest score..." (incomplete name)
- "Both GPT4o and Perplexity performed well..." (improper formatting and incomplete name)

## Table References

When creating tables, ensure column headers use the exact name formats listed above. For space constraints in visualizations, you may create a mapping table that defines abbreviated names, but include this table in the paper for reference.

## Standardization Implementation

The system uses a comprehensive model name standardization utility to ensure consistent naming:

```python
def standardize_model_name(model_name: str) -> str:
    """
    Standardize a model name to ensure consistency throughout the system.
    
    Args:
        model_name: The model name to standardize
        
    Returns:
        The standardized model name
    """
    # Check if it's already a standard name
    if model_name in STANDARD_MODEL_NAMES:
        return model_name
        
    # Check if it's in our direct mapping
    if model_name in MODEL_NAME_MAPPING:
        return MODEL_NAME_MAPPING[model_name]
    
    # Apply heuristic rules for cases not explicitly mapped
    # ... (pattern matching logic) ...
```

The standardization process includes:

1. Direct mapping of known variant names to standard names
2. Pattern-based recognition for common model name variations
3. Fallback logic for handling edge cases
4. Verification against a set of approved standard names

This ensures that all model references maintain consistency across the system, regardless of how they were originally entered.