# Updated Requirements from Peter's Latest Email

## Key Points from Peter's Latest Email

> "Have you got just the raw data of letter grades per model matrix? I'm interested in the simplest output so Table looks clean and concise. As is, each cell's parenthesis is redundant since we already know A- is 3.75, etc., so those numerical grades are extraneous. Also, model names are so small to be legible. We need to ensure simple, brief but clear model names used as column header and row index, such as 'DeepSeek 32b' for 'DeepSeek-Distill-Qwen-32b' or 'Perplexity 70B' for 'Perplexity: Llama 3.1 Sonar 70B', etc. Those full names could be easily added in an Appendix. Note such changes could ensure column width to be of roughly the same size (provided, row header is double-spaced (but not more than triple-spaced) for any long model abbreviations).
>
> BTW, since you're refactoring in future, I'd humbly suggest to you to save, if not already, this raw grade matrix so they can be reused to tweak table or jpg displays.
>
> I think, however, we're kind of running out of time so let's just use as is, unless this is a simple change."

## Clarified Requirements

1. **Display Format Simplification**
   - ✅ Remove the numerical values from display (e.g., show just "A-" instead of "A- (3.75)")
   - ✅ Focus on letter grades only in the presented table

2. **Model Name Abbreviation**
   - ✅ Use abbreviated model names as column headers and row indices
   - ✅ Examples: "DeepSeek 32b" instead of "DeepSeek-Distill-Qwen-32b"
   - ✅ Include full names in an appendix

3. **Table Formatting**
   - ✅ Ensure columns have roughly the same width
   - ✅ Use double-spacing (or triple if needed) for long model abbreviations in row headers

4. **Data Persistence**
   - ✅ Save the raw grade matrix for future tweaks to table or visualizations
   - ✅ Enable easy regeneration of display formats without re-running tests

5. **Implementation Priority**
   - ✅ Only proceed if this is a "simple change" due to time constraints
   - ✅ Otherwise, use the current format

## Technical Implications

1. **Modified Display Logic**:
   - Update cell display to show only letter grades without numeric values
   - Retain numeric data internally for calculations

2. **Model Name Processing**:
   - Create a model name abbreviation function
   - Store mapping between abbreviated and full names

3. **Table Structure**:
   - Standardize column widths
   - Add formatting for multi-line row headers when needed

4. **Data Management**:
   - Extract and save raw grade matrix as JSON
   - Add utility to regenerate Excel from saved matrix