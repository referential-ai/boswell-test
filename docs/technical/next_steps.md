# Next Steps

This document outlines planned improvements and feature additions for the Botwell framework.

## 1. Model Support Expansion

### Add Grok 3 Support
- Research how to access Grok 3 via OpenRouter or alternative APIs
- Implement integration with appropriate configurations
- Test and verify functionality
- Add to the list of supported models
- Document usage details

## 2. Grading Statistics Improvements

### Calculate and Display Additional Median Values
- Implement calculation of median for the last column (grades received)
- Calculate median of diagonal elements (self-assessment patterns)
- Ensure proper statistical validity given these may differ from overall medians
- Update visualization and reporting tools to show these statistics
- Add explanatory notes about interpretation of these metrics

## 3. Grading Bias Analysis Enhancements

### Address Median Bias in Last Row
- Investigate and document the tendency of chatbots to be lenient graders
- Implement separate statistics for "grader leniency factor"
- Consider normalization methods to account for this bias
- Update reports to highlight this pattern and its implications
- Add configuration option to apply bias correction

## 4. Free vs. Paid Model Differentiation

### Identify and Separate Model Tiers
- Document which models are available in free tiers
- Research performance differences between free and paid models
- Consider adding tier indicators in reports and visualizations
- Implement option to generate separate reports for free vs. paid models
- Update CLI to support explicit tier-based filtering

Current free tier models include:
- GPT-3.5-Turbo
- Llama-3-8B
- Gemini Flash 1.5
- Mistral Small
- Qwen-Turbo
- DeepSeek-Lite
- And others as listed in the `FREE_MODELS` configuration

## 5. Algorithm Query Documentation

### Document Domain Question Details
- Create comprehensive documentation of existing algorithm queries
- Review and potentially enhance computer science domain questions
- Ensure consistent difficulty scaling across domains
- Add examples of strong answers for reference
- Consider creating a new domain specifically for algorithmic complexity analysis

## Implementation Priorities

1. **High Priority**:
   - Grading statistics improvements
   - Free vs. paid model differentiation documentation

2. **Medium Priority**:
   - Grok 3 support
   - Algorithm query documentation 

3. **Lower Priority**:
   - Grading bias analysis enhancements

## Timeline and Resources

- Estimated development time: 2-3 weeks
- Primary focus areas: statistical analysis components and reporting
- Required expertise: Python statistics libraries, API integration, documentation
- Testing approach: Unit tests for new statistical methods, integration tests for reporting

## How to Contribute

If you're interested in implementing any of these features:

1. Select a task from the priority list
2. Create a new branch with a descriptive name
3. Implement the feature following the code style guidelines
4. Add appropriate tests and documentation
5. Submit a pull request with a clear description of changes