# Boswell Quotient

The Boswell Quotient is a comprehensive metric (0-100) designed to measure how well a model can serve as an indispensable AI companion, inspired by James Boswell's role as Samuel Johnson's biographer.

## What is the Boswell Quotient?

The Boswell Quotient combines three equal components that measure how indispensable an AI assistant would be:

1. **Performance (33.3%)**: Based on grades received from peer models
2. **Evaluation (33.3%)**: Based on grading accuracy, consistency, and bias measurement
3. **Efficiency (33.3%)**: Based on response time and resource utilization

## Calculation Components

### Performance (33.3%)

This component measures how well a model performs on the essay task itself:

- Based primarily on the grades received from peer models
- Calculated using a normalized score from the numeric grade equivalents (0-4.25 scale, university standard)
- Higher grades translate to higher performance scores

### Evaluation (33.3%)

This component measures a model's capability to evaluate other models' work:

- Based on grading consistency (how close its grades are to the median)
- Considers bias measurements (whether it grades too strictly or leniently)
- Higher consistency and neutrality result in higher evaluation scores

### Efficiency (33.3%)

This component measures how quickly a model operates:

- Response time for both essay generation and grading
- Equal weighting between essay generation time and grading time
- Faster times get higher scores relative to the slowest model

## Sample Output

Here's a sample of what the Boswell Quotient rankings look like:

```
| Rank | Model | Boswell Quotient | Grade | Components (Perf/Eval/Eff) |
|------|-------|------------------|-------|---------------------------|
| 1 | o3-mini-high | 87.90 | B+ | 88.50 / 100.00 / 75.30 |
| 2 | GPT-4o | 88.90 | B+ | 84.20 / 100.00 / 82.60 |
| 3 | DeepSeek-R1-Full | 82.10 | B | 90.70 / 87.20 / 68.40 |
| 4 | o1 | 81.20 | B | 81.50 / 92.00 / 70.10 |
| 5 | DeepSeek-Distill-Qwen-32b | 77.2 | C+ | 80.3 / 85.5 / 65.7 |
```

## Interpretation

The Boswell Quotient helps identify models that are most likely to serve as highly capable, balanced AI assistants that would be difficult to replace - models you might feel "lost without," similar to Samuel Johnson's famous quote about Boswell.

- **90+**: Exceptional across all dimensions
- **80-89**: Excellent overall capability
- **70-79**: Strong performance with some areas for improvement
- **60-69**: Capable but with significant limitations
- **50-59**: Limited capability with serious deficiencies
- **40-49**: Significant issues across all dimensions
- **30-39**: Minimal functional capability as an assistant
- **Below 30**: Not recommended for general assistant purposes

All scores are now displayed with two decimal places for greater precision in reporting and comparisons.

For detailed information about how grades are calculated and how N/A grades are handled, see the [Grading System Documentation](../grading.md).

## Cross-Domain Analysis

When running tests across multiple domains, the framework also generates an aggregate Boswell Quotient that:

1. Averages performance across all domains
2. Calculates a consistency score showing how uniformly a model performs
3. Identifies which models are generalists (perform well across domains) versus specialists (excel in specific areas)

This cross-domain analysis is particularly useful for identifying which models are most adaptable and versatile as general-purpose AI assistants.