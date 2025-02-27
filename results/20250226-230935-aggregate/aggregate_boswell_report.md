# Aggregate Boswell Quotient Analysis Across Domains

This report aggregates model performance across 4 domains:
- **Political Science - Level 1: AI Policy Analysis**
- **Political Science - Level 2: AI Governance Analysis**
- **Computer Science - Level 1: Algorithm Analysis**
- **Computer Science - Level 2: System Design**

## Overall Model Rankings

The table below shows models ranked by their average Boswell Quotient across all domains:

| Rank | Model | Boswell Quotient | Grade | Domain Count | Consistency | Best Domain | Worst Domain |
|------|-------|-----------------|-------|--------------|-------------|------------|-------------|
| 1 | o1-mini | 92.9 | A- | 4 | 95.7 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 2 | Qwen-Turbo | 90.1 | A- | 4 | 89.5 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 3 | Claude-3-Opus | 88.8 | B+ | 4 | 95.0 | Computer Science - Level 1: Algorithm Analysis | Computer Science - Level 2: System Design |
| 4 | Qwen-Plus | 88.7 | B+ | 4 | 90.3 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 5 | DeepSeek-R1-Full | 88.5 | B+ | 4 | 94.4 | Political Science - Level 2: AI Governance Analysis | Computer Science - Level 2: System Design |
| 6 | grok2-1212 | 86.7 | B | 4 | 78.5 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 7 | GPT-4o-mini | 85.3 | B | 4 | 82.2 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 8 | o3-mini-high | 85.1 | B | 4 | 82.5 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 9 | grok-beta | 84.3 | B | 4 | 89.7 | Computer Science - Level 2: System Design | Political Science - Level 1: AI Policy Analysis |
| 10 | GPT-4o | 84.3 | B | 4 | 81.4 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 1: AI Policy Analysis |
| 11 | o1 | 84.2 | B | 4 | 79.3 | Computer Science - Level 1: Algorithm Analysis | Computer Science - Level 2: System Design |
| 12 | Llama-3-8B | 84.0 | B | 4 | 83.1 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 1: AI Policy Analysis |
| 13 | DeepSeek-Distill-Qwen-32b | 82.3 | B- | 4 | 78.5 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 1: AI Policy Analysis |
| 14 | Qwen-Max | 82.3 | B- | 4 | 91.5 | Computer Science - Level 2: System Design | Political Science - Level 2: AI Governance Analysis |
| 15 | Claude-3.7-Sonnet | 81.0 | B- | 4 | 85.3 | Computer Science - Level 2: System Design | Political Science - Level 2: AI Governance Analysis |
| 16 | GPT-3.5-Turbo | 80.0 | B- | 4 | 67.2 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 17 | Perplexity: Llama 3.1 Sonar 8B Online | 79.5 | C+ | 4 | 91.8 | Political Science - Level 2: AI Governance Analysis | Political Science - Level 1: AI Policy Analysis |
| 18 | Claude-3-Sonnet | 78.2 | C+ | 4 | 69.7 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 19 | Claude-3.7-Sonnet-thinking | 76.0 | C | 4 | 82.8 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 20 | Gemini Pro 1.5 | 74.6 | C | 4 | 82.1 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 21 | Perplexity: Llama 3.1 Sonar 405B Online | 74.0 | C | 4 | 74.4 | Political Science - Level 1: AI Policy Analysis | Political Science - Level 2: AI Governance Analysis |
| 22 | Gemini Flash 1.5 | 73.8 | C | 4 | 74.6 | Computer Science - Level 2: System Design | Political Science - Level 1: AI Policy Analysis |
| 23 | Perplexity: Llama 3.1 Sonar 70B | 71.5 | C- | 4 | 82.2 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |

## Top Performing Models

**o1-mini** achieved the highest average Boswell Quotient of **92.9** across 4 domains.
With a consistency score of 95.7, it demonstrated remarkably stable performance across all domains.

Other strong performers include **Qwen-Turbo** (90.1), **Claude-3-Opus** (88.8), **Qwen-Plus** (88.7).

## Domain-Specific Leaders

The table below shows which models performed best in each domain:

| Domain | Top Model | Boswell Quotient | Grade |
|--------|-----------|------------------|-------|
| Political Science - Level 1: AI Policy Analysis | o1-mini | 92.1 | A- |
| Political Science - Level 2: AI Governance Analysis | o1-mini | 91.5 | A- |
| Computer Science - Level 1: Algorithm Analysis | GPT-3.5-Turbo | 96.2 | A |
| Computer Science - Level 2: System Design | o1-mini | 92.2 | A- |

## Key Insights

### Most Consistent Performers
These models maintained the most consistent performance across different domains: **o1-mini** (consistency: 95.7), **Claude-3-Opus** (consistency: 95.0), **DeepSeek-R1-Full** (consistency: 94.4).
High consistency suggests these models have broad capabilities that transfer well between different subject areas.

### Domain Specialists
These models showed significantly stronger performance in specific domains:
- **Claude-3-Sonnet** excels in **Computer Science - Level 1: Algorithm Analysis** (score: 95.3, 22.8 points above its average in other domains)
- **GPT-3.5-Turbo** excels in **Computer Science - Level 1: Algorithm Analysis** (score: 96.2, 21.6 points above its average in other domains)
- **Gemini Flash 1.5** excels in **Computer Science - Level 2: System Design** (score: 87.9, 18.8 points above its average in other domains)

## Conclusion
The aggregated Boswell Quotient provides a comprehensive view of model capabilities across multiple domains, helping identify both generalist models that perform consistently well across diverse tasks and specialist models that excel in particular areas.

Based on this cross-domain analysis, **o1-mini** emerges as the most capable overall AI assistant, with strong performance across the tested domains.