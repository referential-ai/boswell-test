# Model Name Abbreviation

## Purpose

The Excel report uses abbreviated model names for better readability and more compact table display. Long model names are automatically shortened while preserving essential identifying information.

## How It Works

The `abbreviate_model_name()` function uses regex pattern matching to transform long model names into more concise versions:

```python
def abbreviate_model_name(model_name: str) -> str:
    """Create shortened version of model name for display."""
    # Common patterns to abbreviate
    patterns = [
        # DeepSeek models
        (r'DeepSeek-Distill-Qwen-(\d+b)', r'DeepSeek \1'),
        (r'DeepSeek-R1-Full', r'DeepSeek R1'),
        # Perplexity models
        (r'Perplexity: Llama 3.1 Sonar (\d+B)(?: Online)?', r'Perplexity \1'),
        # Claude models
        (r'Claude-(\d+(?:\.\d+)?)-(\w+)', r'Claude \1 \2'),
        # Gemini models
        (r'Gemini (Pro|Flash) (\d+\.\d+)', r'Gemini \1 \2'),
        # GPT models
        (r'GPT-(\d+)([a-z]?)(?:-mini)?', r'GPT-\1\2'),
        # Others 
        (r'grok(\d+)-(\d+)', r'Grok \1'),
        (r'o(\d+)(?:-mini)?(?:-high)?', r'o\1')
    ]
    
    # Apply patterns
    result = model_name
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result)
    
    return result
```

## Example Transformations

| Original Model Name | Abbreviated Version |
|---------------------|---------------------|
| DeepSeek-Distill-Qwen-32b | DeepSeek 32b |
| Perplexity: Llama 3.1 Sonar 70B | Perplexity 70B |
| Claude-3-Opus | Claude 3 Opus |
| Gemini Pro 1.5 | Gemini Pro 1.5 |
| GPT-4o-mini | GPT-4o |
| grok2-1212 | Grok 2 |
| o1-mini | o1 |

## Preservation of Full Names

To ensure traceability, the Excel report includes a "Model Name Reference" appendix at the bottom that maps the abbreviated names back to their full versions.

```python
# Add model name appendix
appendix_row = legend_row + 6
if model_name_mapping:
    apply_cell_style(
        ws.cell(row=appendix_row, column=1),
        value="Model Name Reference:",
        alignment=LEFT_ALIGNMENT,
        font=Font(name="Helvetica Neue", bold=True, size=8)
    )
    
    # Add mapping between abbreviated and full names
    for i, (abbrev, full_name) in enumerate(model_name_mapping.items()):
        if abbrev != full_name:  # Only add if there was an actual abbreviation
            apply_cell_style(
                ws.cell(row=appendix_row + i + 1, column=1),
                value=f"{abbrev} = {full_name}",
                alignment=LEFT_ALIGNMENT,
                font=HELVETICA_FONT
            )
```

This approach allows for concise column headers while maintaining the ability to trace back to the original model names.