# Boswell Test Command Reference

## Excel Cross-Assessment Table Generation

The Boswell Test now automatically generates an Excel spreadsheet file (`cross_grading_table.xlsx`) as part of the standard output. This file contains the complete model cross-assessment matrix as seen in Table 1 of the research paper, with appropriate color highlighting and the median bias data included in the last row.

### Features

- Full cross-assessment matrix showing how each model grades every other model
- Color highlighting to visually indicate grade levels (A+, A, A-, B+, etc.)
- Median grade for each model shown in the rightmost column
- Grading bias statistics included in the bottom row
- Formatted for easy reading and analysis

### Default Behavior

This Excel table is generated automatically with every test run - no additional flags or commands needed. You'll find it in your results directory:

```
results/[timestamp]-[domain]/cross_grading_table.xlsx
```

### Usage Examples

Running any Boswell test automatically generates this Excel file:

```bash
# All of these commands will generate the Excel cross-assessment table
botwell --domain pol_sci_1
botwell --domain pol_sci_1 --free
botwell --domain pol_sci_1 --models "GPT-4o" "Claude-3.7-Sonnet" "Gemini Pro 1.5" "o1"
```

### Integration With Other Tools

The Excel file can be directly opened in Microsoft Excel, Google Sheets, LibreOffice Calc, or any other spreadsheet application for further analysis or presentation.

## Standalone Excel Table Generation

If you want to generate the cross-assessment Excel table separately after a test run has completed, you can use the standalone command:

```bash
# Generate cross-assessment Excel table with exact Table 1 styling from the paper
python create_cross_grading_table.py results/[timestamp]-[domain]/full_results.json
```

### Features

- Works with any existing result directory that contains a `full_results.json` file
- Generates the same Excel table format as the automatic process
- Preserves all formatting, colors, and layout exactly as shown in Table 1
- Uses the default system font for optimal readability in different spreadsheet apps 

### Example

```bash
python create_cross_grading_table.py results/20250305-184949-pol_sci_1/full_results.json