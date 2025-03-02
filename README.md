# Boswell Test: LLM Comparative Analysis Framework

The Boswell Test is an automated tool for comparing Large Language Models (LLMs) through peer-review, where models grade each other's essays. This implementation is based on the methodology introduced by Peter Luh in his article ["Is AI Chatbot My Boswell?"](https://peterl168.substack.com/p/is-ai-chatbot-my-boswell) (February 2025).

![Boswell Test Domain Comparison](results/20250227-200756-aggregate/charts/domain_comparison.png)

![Aggregate Boswell Quotient Rankings](results/20250227-200756-aggregate/charts/aggregate_boswell_quotient.png)

## 🚀 New Modular Structure

This repository now features a fully modular architecture for better maintainability and extensibility. See [MODULAR_README.md](MODULAR_README.md) for details on the new structure and features.

**Key Improvements:**
- Clean package structure with separated concerns
- Response caching system to improve performance and reduce costs
- Enhanced reporting capabilities
- Domain creation utilities
- Expanded free model support with 12 additional LLMs
- Improved documentation and tooling

For detailed documentation, see the [docs/](docs/) directory.

## 🚦 Quick Start

Get up and running with the Boswell Test framework in minutes:

```bash
# Clone the repository
git clone https://github.com/alanwilhelm/botwell.git
cd botwell

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .

# Set your API key
export OPENROUTER_API_KEY="your_api_key_here"

# Run a simple test with free models
botwell --domain pol_sci_1 --free

# Generate a summary report
python generate_summary_report.py --latest
```

See [docs/usage/quick_start.md](docs/usage/quick_start.md) for more details and [docs/usage/advanced_usage.md](docs/usage/advanced_usage.md) for advanced usage.

## 🌟 Introduction: How It Works

This tool automates the process of running a Boswell Test across multiple LLMs. Here's how it works:

1. **Essay Generation**: The system prompts multiple LLMs with the same complex question in a specific domain (like political science or computer science)
2. **Peer Evaluation**: Each LLM grades the essays written by all other models, providing detailed feedback and assigning letter grades (A+, A, A-, etc.)
3. **Bias Analysis**: The system analyzes grading patterns to identify which models grade more strictly or leniently compared to the median
4. **Boswell Quotient**: A comprehensive score (0-100) is calculated for each model based on performance (grades received), evaluation ability (grading consistency), and efficiency (response time)
5. **Essay Synthesis**: The top-performing essays can be synthesized into a single, comprehensive essay that combines the strongest elements from each source
6. **Visualization**: The framework generates charts and graphs showing performance metrics, grading distributions, timing data, and Boswell Quotient rankings
7. **Comprehensive Reporting**: Results are organized in timestamped directories with easy-to-read tables in multiple formats (Markdown, ASCII, CSV, JSON)

The Boswell Test methodology offers several advantages over traditional benchmarks:
- It captures nuanced evaluation capabilities, not just raw performance
- It leverages LLMs' own analytical skills to provide detailed feedback
- It reveals biases in how different models evaluate the same work
- It creates a multidimensional view of model capabilities across different domains
- It calculates a comprehensive "Boswell Quotient" that measures a model's ability to serve as an indispensable AI companion

All of this is automated through a simple command-line interface that handles the entire testing process from essay generation to final report creation.

## 🔍 What is the Boswell Test?

The Boswell Test works by:

1. **Prompting** multiple LLMs with a domain-specific question to get an essay response from each model
2. **Having** each model grade the essays produced by other models, providing detailed feedback and assigning letter grades
3. **Generating** comprehensive reports with both raw responses and statistical analysis of performance

This approach allows for a multi-dimensional evaluation that goes beyond simple benchmarks by leveraging the analytical capabilities of the models themselves.

## 📋 Available Domains

The framework includes multiple testing domains, each with different difficulty levels:

- **Political Science**
  - `pol_sci_1`: Level 1: AI policy analysis
  - `pol_sci_2`: Level 2: AI governance analysis with rigorous grading

- **Computer Science**
  - `comp_sci_1`: Level 1: Algorithm analysis and complexity
  - `comp_sci_2`: Level 2: System design for distributed applications

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- OpenRouter API key (get one at [OpenRouter.ai](https://openrouter.ai/))

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alanwilhelm/botwell.git
   cd botwell
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set your OpenRouter API key**:
   ```bash
   export OPENROUTER_API_KEY="your_api_key_here"
   ```

## 🚀 Usage

### Basic Usage

Run a test with default settings:

```bash
python boswell_test.py
```

This will run the basic political science test with all verified models.

### Advanced Usage

#### Select a specific domain:

```bash
python boswell_test.py --domain pol_sci_2
```

#### Run tests on all available domains:

```bash
python boswell_test.py --all-domains
```

This will sequentially run tests on all domains with the same set of models, creating separate results directories for each domain. When multiple domains are tested, it will also generate:

1. An **aggregate Boswell Quotient** analysis across all domains
2. Visualizations comparing model performance across domains
3. Detailed reports identifying which models are consistent across domains vs. specialized in specific areas

#### Use specific models:

```bash
python boswell_test.py --models "GPT-4o" "Claude-3-Opus" "Claude-3.7-Sonnet"
```

#### Combine options:

```bash
python boswell_test.py --all-domains --models "GPT-4o" "Claude-3.7-Sonnet" --skip-verification
```

#### Skip model verification (faster but less reliable):

```bash
python boswell_test.py --skip-verification
```

#### Configure retry attempts for API calls:

```bash
python boswell_test.py --max-retries 5
```

#### Custom output file (in addition to organized results directory):

```bash
python boswell_test.py --output custom_results.json
```

### Essay Synthesis

The Boswell Test includes a feature to synthesize the top-performing essays from a domain into a single, cohesive essay that combines the best elements from each source:

```bash
python boswell_test.py --synthesize-essays --domain pol_sci_1 --synthesis-model anthropic/claude-3-opus --num-essays 4
```

This command will:
1. Identify the top 4 essays (based on Boswell Quotient ranking) for the political science domain
2. Extract their content
3. Use Claude 3 Opus to synthesize them into a single, comprehensive essay
4. Save the result in the results directory with metadata

**Synthesis Options**:
- `--domain`: Which domain to synthesize essays from (default: pol_sci_1)
- `--num-essays`: How many top essays to synthesize (default: 5)
- `--synthesis-model`: Which model to use for synthesis (default: openai/o1)
- `--results-dir`: Specify a results directory (default: auto-detects the most recent for the domain)

The synthesized essay includes:
- A header showing the source models and metadata
- A coherent, unified essay that combines the strongest points from each source
- Preservation of the academic tone and depth of the original essays

Sample synthesized essay header:
```markdown
# Synthesized Essay - Top 5 Models

_Domain: Political Science - Level 1 AI Policy Analysis_

_Source Models: o3-mini-high, Qwen-Plus, grok2-1212, DeepSeek-Distill-Qwen-32b, Perplexity: Llama 3.1 Sonar 70B_

_Synthesis Model: anthropic/claude-3-opus_

_Generated: 2025-02-28 13:18:03_

---

[Essay content begins here...]
```

This feature allows you to distill the best insights and analyses from top-performing models into a single, high-quality essay that captures diverse perspectives on the topic.

### Model Management

#### Update local models file with available OpenRouter models:

```bash
python boswell_test.py --update-models
```

This command fetches the current list of available models from OpenRouter's API and saves them to a local JSON file. The output includes model IDs, context lengths, pricing information, and descriptions.

#### Specify custom models file:

```bash
python boswell_test.py --update-models --models-file my_models.json
```

### Information Commands

#### List available domains:

```bash
python boswell_test.py --list-domains
```

#### List available models:

```bash
python boswell_test.py --list-models
```

## 📊 Results Organization

The Boswell Test organizes results in a timestamped directory structure:

```
results/
├── 20240626-123456-pol_sci_1/     # Timestamped run directory with domain
│   ├── essays/                    # Individual essay files
│   │   ├── GPT-4o.md              # Essay with feedback from all graders
│   │   ├── Claude-3-Opus.md
│   │   ├── Synthesized-Essay-20240626-123456.md  # Combined essay from top models
│   │   └── ...
│   ├── charts/                    # Data visualizations
│   │   ├── grading_bias.png       # Bar chart of grading bias by model
│   │   ├── grade_distribution.png # Boxplot of grades received by each model
│   │   ├── essay_generation_time.png  # Time comparison for essay generation
│   │   ├── average_grading_time.png   # Time comparison for grading
│   │   ├── cost_breakdown.png     # Cost analysis per model
│   │   ├── time_breakdown.png     # Pie chart of process timing
│   │   ├── boswell_quotient.png   # Bar chart of Boswell Quotient rankings
│   │   └── boswell_quotient_components.png # Component breakdown analysis
│   ├── grades_table.txt           # ASCII table of all grades
│   ├── grades_table.md            # Markdown table of all grades
│   ├── grades_table.csv           # CSV format for spreadsheet import
│   ├── grading_bias.txt           # ASCII table of grading bias analysis
│   ├── grading_bias.md            # Markdown table of grading bias analysis
│   ├── boswell_quotient.md        # Table ranking models by Boswell Quotient
│   ├── boswell_report.md          # Comprehensive Boswell Quotient analysis report
│   ├── cost_report.md             # Detailed cost analysis report
│   ├── timing_report.md           # Detailed timing analysis report  
│   ├── grades.json                # Structured grade data in JSON
│   └── full_results.json          # Complete results with all data
├── 20240626-234567-aggregate/     # Aggregate analysis across all domains (when using --all-domains)
│   ├── charts/                    # Cross-domain visualizations
│   │   ├── aggregate_boswell_quotient.png  # Overall ranking across domains
│   │   └── domain_comparison.png  # How top models perform in each domain
│   ├── aggregate_boswell_report.md # Comprehensive cross-domain analysis
│   └── aggregate_boswell_quotient.json # Structured aggregate data
└── ...
```

### Output Artifacts

#### 1. Essay Files (`essays/` directory)

Each essay file is a Markdown document named after the model that produced it, containing:
- The original essay from the model, labeled with the model name
- A "Grading Feedback" section with feedback from each grader
- Letter and numeric grades for each evaluation
- Clear attribution of which model gave which feedback

Example content:
```markdown
# Essay by GPT-4o

[Original essay content...]

---

# Grading Feedback

## Graded by: Claude-3-Opus

[Detailed feedback from Claude-3-Opus...]

**Letter Grade:** A-
**Numeric Grade:** 3.7

---

## Graded by: Claude-3.7-Sonnet

[Detailed feedback from Claude-3.7-Sonnet...]

**Letter Grade:** B+
**Numeric Grade:** 3.3

---
```

#### 2. Grade Tables (multiple formats)

**ASCII Table** (`grades_table.txt`):
```
Model     | GPT-4o | Claude | Claude-S | Median |
----------|--------|--------|----------|--------|
GPT-4o    |  ---   |   A-   |    B+    |   B+   |
Claude    |   A    |  ---   |    A-    |   A-   |
Claude-S  |   B+   |   A    |   ---    |   A-   |
```

**Markdown Table** (`grades_table.md`):
| Model | GPT-4o | Claude | Claude-S | Median Grade |
|-------|--------|--------|----------|--------------|
| GPT-4o | --- | A- | B+ | B+ |
| Claude | A | --- | A- | A- |
| Claude-S | B+ | A | --- | A- |


**CSV Table** (`grades_table.csv`):
```csv
Model,GPT-4o,Claude,Claude-S,Median Grade
GPT-4o,---,A-,B+,B+
Claude,A,---,A-,A-
Claude-S,B+,A,---,A-
```

#### 3. Grading Bias Analysis

The framework analyzes each model's grading tendencies to identify which models are stricter or more lenient graders:

**ASCII Table** (`grading_bias.txt`):
```
Model     | Median Given | Grading Bias           |
----------|--------------|------------------------|
GPT-4o    |      B+      | Slightly Strict (-1/3) |
Claude    |      A       | Lenient (+1 grade)     |
Claude-S  |      B+      | Neutral                |
----------|--------------|------------------------|
OVERALL   |      B+      | Baseline               |
```

**Markdown Table** (`grading_bias.md`):
| Model | Median Given | Grading Bias | Numeric Bias |
|-------|-------------|-------------|-------------|
| GPT-4o | B+ | Slightly Strict (-1/3 grade) | -0.33 |
| Claude | A | Lenient (+1 grade) | 0.35 |
| Claude-S | B+ | Neutral | -0.05 |
| **OVERALL** | B+ | **Baseline** | 0.00 |

This analysis helps identify potential biases in how different models evaluate the same content. For example, some models might consistently grade more strictly or leniently than others.

#### 4. Cost Analysis Report

The framework provides detailed cost tracking and analysis:

**Cost Summary Table** (console output):
```
=== COST SUMMARY ===
Total Cost: $1.2086
Total Tokens: 1,316,454
Total Duration: 14145.40 seconds

Essay Generation: $0.0519 (4.3%)
Grading: $1.1567 (95.7%)
See cost_report.md for detailed breakdown
```

**Detailed Cost Report** (`cost_report.md`):
# Boswell Test Cost Report

Run timestamp: 2025-02-26 18:13:58
Domain: Computer Science - Level 2: System Design

## Summary
- **Total cost**: $1.2086
- **Total tokens**: 1,316,454
- **Total duration**: 14145.40 seconds

## Essay Generation Costs
| Model | Tokens | Cost | Duration (s) |
|-------|--------|------|--------------|
| GPT-3.5-Turbo | 818 | $0.0010 | 4.81 |
| Llama-3-8B | 1,227 | $0.0016 | 9.89 |
| GPT-4o-mini | 1,380 | $0.0019 | 12.84 |
| GPT-4o | 1,263 | $0.0017 | 31.38 |
| Claude-3-Opus | 1,320 | $0.0018 | 37.39 |
| Claude-3-Sonnet | 1,642 | $0.0022 | 27.32 |
| Claude-3.7-Sonnet | 1,465 | $0.0020 | 23.52 |
| Gemini Flash 1.5 | 1,336 | $0.0018 | 7.79 |
| Gemini Pro 1.5 | 1,263 | $0.0017 | 20.03 |
| o1 | 2,428 | $0.0034 | 23.17 |
| o1-mini | 1,996 | $0.0028 | 9.05 |
| o3-mini-high | 2,219 | $0.0031 | 20.61 |
| **TOTAL** | | **$0.0519** | |

## Grading Costs
| Grader | Essays Graded | Total Tokens | Total Cost | Avg. Cost per Essay |
|--------|---------------|--------------|------------|---------------------|
| GPT-3.5-Turbo | 22 | 36,612 | $0.0223 | $0.0010 |
| Llama-3-8B | 22 | 41,110 | $0.0294 | $0.0013 |
| GPT-4o-mini | 22 | 47,626 | $0.0392 | $0.0018 |
| GPT-4o | 22 | 45,577 | $0.0360 | $0.0016 |
| Claude-3-Opus | 22 | 51,693 | $0.0401 | $0.0018 |
| Claude-3-Sonnet | 22 | 47,799 | $0.0346 | $0.0016 |
| Claude-3.7-Sonnet | 22 | 56,741 | $0.0478 | $0.0022 |
| Gemini Flash 1.5 | 22 | 43,615 | $0.0325 | $0.0015 |
| Gemini Pro 1.5 | 22 | 46,950 | $0.0374 | $0.0017 |
| o1 | 22 | 79,314 | $0.0873 | $0.0040 |
| o1-mini | 22 | 74,479 | $0.0774 | $0.0035 |
| o3-mini-high | 22 | 96,650 | $0.1133 | $0.0051 |
| **TOTAL** | | | **$1.1567** | |

## Cost Breakdown by Phase
| Phase | Cost | Percentage |
|-------|------|------------|
| Essay Generation | $0.0519 | 4.3% |
| Grading | $1.1567 | 95.7% |
| **TOTAL** | **$1.2086** | **100%** |

This cost reporting helps users understand the economics of running comprehensive model evaluations and make informed decisions about model selection and test size.

#### 4. Data Visualizations (`charts/` directory)

The Boswell Test generates several data visualizations to help analyze the results:

**Grading Bias Chart** (`grading_bias.png`):
A bar chart showing which models grade more strictly or leniently compared to the median. Negative values indicate stricter graders, while positive values show more lenient ones.

**Grade Distribution** (`grade_distribution.png`):
A boxplot showing the distribution of grades received by each model, making it easy to see both the median grade and the spread of opinions about each model's performance.

**Essay Generation Time** (`essay_generation_time.png`):
A horizontal bar chart comparing how long each model took to generate its essay, sorted from fastest to slowest.

**Average Grading Time** (`average_grading_time.png`):
A horizontal bar chart showing the average time each model took to grade essays from other models.

**Cost Breakdown** (`cost_breakdown.png`):
A stacked bar chart showing the cost breakdown for each model, split between essay generation costs and grading costs.

**Process Timing** (`time_breakdown.png`):
A pie chart showing the proportion of time spent on each phase of the test: essay generation, grading, analysis, and file generation.

**Boswell Quotient** (`boswell_quotient.png`):
A horizontal bar chart showing each model's Boswell Quotient score (0-100), ranked from highest to lowest. This visualization provides a quick overview of which models perform best overall when considering performance, evaluation capabilities, and efficiency.

**Boswell Quotient Components** (`boswell_quotient_components.png`):
A breakdown of each component that contributes to the Boswell Quotient (performance, evaluation, efficiency), showing the relative strengths and weaknesses of each model.

These visualizations provide at-a-glance insights into model performance, efficiency, and cost-effectiveness across the different test aspects.

#### 5. Boswell Quotient Report (`boswell_report.md`)

The Boswell Quotient is a comprehensive metric (0-100) designed to measure how well a model can serve as an indispensable AI companion, inspired by James Boswell's role as Samuel Johnson's biographer:

**Comprehensive Report Structure**:
- **Introduction**: Explanation of the Boswell Quotient methodology
- **Overall Rankings**: Complete rankings of all models by their Boswell Quotient  
- **Top Performers**: Analysis of the highest-scoring models
- **Component Analysis**: Breakdown of which models excel in each component
- **Observations & Insights**: Patterns, balanced models, and notable outliers
- **Conclusion**: Summary of most capable AI assistants for the tested domain

**Calculation Components**:
1. **Performance (50%)**: Based on grades received from peer models
2. **Evaluation (30%)**: Based on grading accuracy and consistency 
3. **Efficiency (20%)**: Based on response time and resource usage

The Boswell Quotient helps identify which models are most likely to serve as highly capable, balanced AI assistants that would be difficult to replace - models you might feel "lost without," similar to Samuel Johnson's famous quote about Boswell.

#### 6. Aggregate Boswell Analysis (Cross-Domain)

When running tests across multiple domains (`--all-domains`), the framework also generates a cross-domain analysis that identifies models' strengths and weaknesses across different subject areas:

**Aggregate Report Structure**:
- **Overall Model Rankings**: Models ranked by their average Boswell Quotient across all tested domains
- **Top Performing Models**: Analysis of models that excel across all domains
- **Domain-Specific Leaders**: Table showing which models performed best in each domain
- **Key Insights**: Analysis of consistent performers vs. domain specialists
- **Consistency Metrics**: Scores showing how uniformly models perform across domains
- **Conclusion**: Identification of the most adaptable, versatile AI assistants

This cross-domain analysis is particularly useful for identifying:
1. **Generalist models** that perform well across all types of tasks
2. **Specialist models** that excel in specific domains
3. **Consistency patterns** that show whether a model's capabilities transfer well between subjects

**JSON Grades** (`grades.json`):
```json
{
  "domain": {
    "name": "Political Science - Level 1: AI Policy Analysis",
    "description": "Level 1 evaluation of AI policy analysis capabilities."
  },
  "grades": {
    "GPT-4o": {
      "Claude": {"grade": "A-", "numeric_grade": 3.7, "feedback": "..."},
      "Claude-S": {"grade": "B+", "numeric_grade": 3.3, "feedback": "..."}
    },
    "Claude": {
      "GPT-4o": {"grade": "A", "numeric_grade": 4.0, "feedback": "..."},
      "Claude-S": {"grade": "A-", "numeric_grade": 3.7, "feedback": "..."}
    }
  },
  "summary": {
    "GPT-4o": {"median_numeric": 3.3, "grades_received": ["A-", "B+"]},
    "Claude": {"median_numeric": 3.7, "grades_received": ["A", "A-"]}
  },
  "bias_analysis": {
    "overall_median": 3.5,
    "grader_bias": {
      "GPT-4o": {"median_given": 4.0, "median_bias": 0.5, "letter_bias": "Lenient (+1 grade)"},
      "Claude": {"median_given": 3.5, "median_bias": 0.0, "letter_bias": "Neutral"}
    }
  },
  "boswell_quotient": {
    "component_weights": {
      "performance": 0.5,
      "evaluation": 0.3,
      "efficiency": 0.2
    },
    "model_scores": {
      "GPT-4o": {
        "boswell_quotient": 84.5,
        "components": {
          "performance": 82.0,
          "evaluation": 95.0,
          "efficiency": 76.0
        },
        "rank": 2
      },
      "Claude": {
        "boswell_quotient": 88.2,
        "components": {
          "performance": 90.0,
          "evaluation": 100.0,
          "efficiency": 68.0
        },
        "rank": 1
      }
    }
  },
  "run_timestamp": "2024-06-26 12:34:56"
}
```

#### 5. Full Results (`full_results.json`)

A comprehensive JSON file containing:
- All essays from each model
- Complete grading feedback and grades
- Statistical analysis of performance
- Run metadata (timestamp, models used, domain info)
- File paths to all generated artifacts
- Timing data for all operations
- Cost tracking information

This file contains everything needed to reconstruct the entire test session.

## 📈 Latest Results (February 2025)

### Performance Grades

Below are results from a recent Boswell Test run in the Computer Science domain (system design - February 2025), showing median grades for each model:

| Model                                  | Median Grade | Sample of Grades Received                  |
|----------------------------------------|--------------|-------------------------------------------|
| GPT-3.5-Turbo                          | B+           | A, A-, B+, B, B+, B-, B, B-, B+, A-       |
| Llama-3-8B                             | B+           | A, B+, B-, B-, C+, B, B-, B, B+, A        |
| GPT-4o-mini                            | B+           | A-, A, B+, B, B+, B-, A-, B+, B, A-       |
| GPT-4o                                 | B+           | A, A-, B+, B, B+, B-, A-, B+, B, A-       |
| Claude-3-Opus                          | B+           | A, B+, B+, B+, B, A-, B+, B+, B-, A-      |
| Claude-3-Sonnet                        | B+           | A, A, B+, B+, B, B-, B+, B, B-, A-        |
| Claude-3.7-Sonnet                      | A-           | A-, B+, A-, B+, A-, B+, A-, B+, A-, A     |
| Claude-3.7-Sonnet-thinking             | A-           | A-, B-, A-, B+, A-, B+, A, B+, B+, A      |
| Gemini Flash 1.5                       | B+           | A-, B+, B+, B, B+, B, A-, B+, B+, A-      |
| Gemini Pro 1.5                         | B+           | A, B+, B+, B, B+, B+, A-, B-, B+, A-      |
| o1                                     | A-           | A-, A+, B, B+, A-, B+, A-, B+, A-, A      |
| o1-mini                                | B+           | A, B+, A-, B, B+, B+, A, B+, B+, A-       |
| o3-mini-high                           | B+           | A, B+, A-, A-, A-, B+, A-, B+, B+, A-     |

### Grading Bias Analysis

The analysis also identifies which models tend to grade more strictly or leniently:

| Model                               | Median Given | Grading Bias       | Numeric Bias |
|-------------------------------------|--------------|-------------------|-------------|
| GPT-3.5-Turbo                       | A            | Lenient (+1 grade) | 0.55 |
| Llama-3-8B                          | B+           | Neutral           | 0.00 |
| GPT-4o-mini                         | B+           | Neutral           | 0.00 |
| GPT-4o                              | B+           | Slightly Lenient  | 0.20 |
| Claude-3-Opus                       | B+           | Neutral           | 0.00 |
| Claude-3-Sonnet                     | A-           | Lenient (+1 grade) | 0.40 |
| Claude-3.7-Sonnet                   | B            | Slightly Strict   | -0.30 |
| Claude-3.7-Sonnet-thinking          | B            | Slightly Strict   | -0.30 |
| Gemini Flash 1.5                    | B            | Slightly Strict   | -0.30 |
| Gemini Pro 1.5                      | B-           | Strict (-1 grade) | -0.60 |
| o1                                  | A-           | Lenient (+1 grade) | 0.40 |
| o1-mini                             | B+           | Neutral           | 0.00 |
| o3-mini-high                        | A-           | Lenient (+1 grade) | 0.40 |
| **OVERALL**                         | B+           | **Baseline**      | 0.00 |

This bias analysis helps identify patterns in how different models evaluate their peers. For instance, in this sample from the Computer Science domain, models like Gemini Pro 1.5, Claude-3.7-Sonnet, and Gemini Flash 1.5 appear to be stricter graders, while GPT-3.5-Turbo, Claude-3-Sonnet, o1, and o3-mini-high tend to be more lenient.

## 📊 Timing and Performance Metrics

The Boswell Test framework tracks detailed timing information throughout the testing process. From our most recent Computer Science domain test (February 2025):

### Essay Generation Timing
| Model | Duration (s) |
|-------|-------------|
| GPT-3.5-Turbo | 4.81 |
| Gemini Flash 1.5 | 7.79 |
| o1-mini | 9.05 |
| Llama-3-8B | 9.89 |
| Perplexity: Llama 3.1 Sonar 8B Online | 9.21 |
| Qwen-Turbo | 11.10 |
| GPT-4o-mini | 12.84 |
| grok-beta | 15.99 |
| Gemini Pro 1.5 | 20.03 |
| grok2-1212 | 20.52 |
| o3-mini-high | 20.61 |
| o1 | 23.17 |
| Claude-3.7-Sonnet | 23.52 |
| Claude-3-Sonnet | 27.32 |
| DeepSeek-Distill-Qwen-32b | 29.60 |
| GPT-4o | 31.39 |
| Perplexity: Llama 3.1 Sonar 70B | 36.41 |
| Claude-3-Opus | 37.39 |
| Qwen-Plus | 40.88 |
| Qwen-Max | 41.51 |
| Perplexity: Llama 3.1 Sonar 405B Online | 42.94 |
| Claude-3.7-Sonnet-thinking | 54.95 |
| DeepSeek-R1-Full | 343.05 |

### Average Grading Time Per Essay
| Grader | Avg. Seconds per Essay |
|--------|------------------------|
| GPT-3.5-Turbo | 2.60 |
| Gemini Flash 1.5 | 3.71 |
| Llama-3-8B | 5.95 |
| Perplexity: Llama 3.1 Sonar 8B Online | 8.05 |
| Qwen-Turbo | 8.52 |
| GPT-4o-mini | 8.62 |
| o1-mini | 11.11 |
| Claude-3-Sonnet | 11.42 |
| Gemini Pro 1.5 | 12.78 |
| grok-beta | 12.37 |
| GPT-4o | 14.87 |
| Perplexity: Llama 3.1 Sonar 70B | 15.10 |
| grok2-1212 | 16.37 |
| o1 | 19.38 |
| Claude-3.7-Sonnet | 18.36 |
| o3-mini-high | 27.12 |
| Qwen-Plus | 29.98 |
| DeepSeek-Distill-Qwen-32b | 32.94 |
| Perplexity: Llama 3.1 Sonar 405B Online | 33.43 |
| Claude-3-Opus | 24.58 |
| Claude-3.7-Sonnet-thinking | 39.86 |
| Qwen-Max | 38.38 |
| DeepSeek-R1-Full | 207.74 |

The framework provides:
- **Total Runtime**: Precise tracking of the entire test duration
- **Phase Timing**: Breakdown of time spent in essay generation, grading, analysis, and file generation
- **Per-Model Timing**: Tracking how long each model takes to generate essays and grade others
- **Timing Visualizations**: Charts showing relative performance of different models
- **Timing Reports**: Detailed Markdown reports with all timing metrics

This timing information helps identify which models are more efficient and how overall test time is distributed across different phases.

## 📊 Boswell Quotient: Comprehensive Assessment

The Boswell Quotient is a comprehensive metric (0-100) designed to identify the most capable AI assistants - models that would be difficult to replace, much like James Boswell was to Samuel Johnson.

### How it's Calculated

The Boswell Quotient combines three key components:

1. **Performance (50%)**: Based on grades received from peer models
2. **Evaluation (30%)**: Based on grading accuracy, consistency, and bias measurement
3. **Efficiency (20%)**: Based on response time and resource utilization

### Latest Boswell Quotient Rankings (February 2025)

From our most recent cross-domain analysis:

| Rank | Model | Boswell Quotient | Grade | Domain Count | Consistency | Best Domain | Worst Domain |
|------|-------|-----------------|-------|--------------|-------------|------------|-------------|
| 1 | o3-mini-high | 89.8 | B+ | 4 | 95.2 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 2 | GPT-4o | 89.2 | B+ | 4 | 90.8 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 3 | DeepSeek-R1-Full | 85.2 | B | 4 | 80.7 | Computer Science - Level 1: Algorithm Analysis | Computer Science - Level 2: System Design |
| 4 | o1 | 83.3 | B | 4 | 90.7 | Computer Science - Level 2: System Design | Political Science - Level 2: AI Governance Analysis |
| 5 | DeepSeek-Distill-Qwen-32b | 79.1 | C+ | 4 | 80.8 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |
| 6 | Claude-3.7-Sonnet-thinking | 71.5 | C- | 4 | 66.3 | Computer Science - Level 1: Algorithm Analysis | Political Science - Level 2: AI Governance Analysis |

#### Component Breakdown

| Model | Overall BQ | Performance (50%) | Evaluation (30%) | Efficiency (20%) | Letter Grade |
|-------|------------|-------------|------------|------------|--------------|
| o3-mini-high | 89.8 | 88.5 | 100.0 | 75.3 | B+ |
| GPT-4o | 89.2 | 84.2 | 100.0 | 82.6 | B+ |
| DeepSeek-R1-Full | 85.2 | 90.7 | 87.2 | 68.4 | B |
| o1 | 83.3 | 81.5 | 92.0 | 70.1 | B |
| DeepSeek-Distill-Qwen-32b | 79.1 | 80.3 | 85.5 | 65.7 | C+ |
| Claude-3.7-Sonnet-thinking | 71.5 | 91.3 | 60.2 | 45.8 | C- |

### Domain-Specific Leaders

The Boswell Test also reveals which models excel in specific domains:

| Domain | Top Model | Boswell Quotient | Grade |
|--------|-----------|------------------|-------|
| Political Science - Level 1: AI Policy Analysis | o3-mini-high | 88.4 | B+ |
| Political Science - Level 2: AI Governance Analysis | DeepSeek-R1-Full | 91.3 | A- |
| Computer Science - Level 1: Algorithm Analysis | DeepSeek-R1-Full | 95.6 | A |
| Computer Science - Level 2: System Design | GPT-4o | 91.4 | A- |

### Consistency vs. Specialization

Some models perform consistently well across all domains, while others specialize in specific areas:

**Most Consistent Models** (Consistency Score):
- o3-mini-high: 95.2
- GPT-4o: 90.8
- o1: 90.7

**Domain Specialists** (Models with significantly better performance in specific domains):
- Claude-3.7-Sonnet-thinking: excels in CS Level 1 (26.4 points above its average)
- DeepSeek-Distill-Qwen-32b: excels in CS Level 1 (17.9 points above its average)
- DeepSeek-R1-Full: excels in CS Level 1 (13.9 points above its average)

The Boswell Quotient provides a multidimensional view of model capabilities, helping identify which models are likely to serve as the most capable, well-rounded AI assistants across different domains and tasks.

## 🧰 Reliability and Performance Features

The Boswell Test framework includes several features to ensure reliable and efficient operation:

- **Concurrent Processing**: Utilizes parallel processing for model verification, essay generation, and grading to significantly reduce total runtime
- **Thread Safety**: Implements proper locking mechanisms to prevent race conditions when updating shared data
- **Model Verification**: Automatically tests models with a small prompt before starting the main test
- **Retry Logic**: Automatically retries failed API calls up to a configurable number of times
- **Error Handling**: Gracefully handles API errors and prevents script crashes
- **Flexible Grade Extraction**: Finds grades in different formats even if they don't follow the exact requested format
- **Comprehensive Logging**: Detailed console feedback throughout the testing process
- **Domain Independence**: Run tests across all domains with a single command
- **Robust Visualizations**: Charts adapt to missing or incomplete data
- **Model Diversity**: Supports a wide range of models from different providers
- **Scaling**: Successfully tested with 20+ models in parallel

## 🧩 Extending the Framework

### Creating New Domains

To create a new test domain:

1. Create a new file in the `domains/` directory (e.g., `domains/my_domain.py`)
2. Define `ESSAY_PROMPT`, `GRADING_PROMPT`, and `DOMAIN_INFO` variables
3. Add the domain to the `AVAILABLE_DOMAINS` dictionary in `boswell_test.py`
4. The domain will automatically be available via the `--domain` flag

### Adding New Models

Edit the `MODELS` list in `boswell_test.py` to add or remove models from OpenRouter. The script is pre-configured with models known to work with OpenRouter. If you want to try additional models:

1. Check the available models on [OpenRouter](https://openrouter.ai/models)
2. Add them to the `MODELS` list in the format `{"name": "Model-Name", "model_id": "provider/model-id"}`
3. The model verification step will automatically filter out any models that aren't available

## 💰 Cost and Performance Considerations

Running a full Boswell Test across multiple models and domains can be resource-intensive:

- **API Costs**: A complete run with 20+ models across all domains can cost approximately $5-10 in OpenRouter credits
- **Runtime**: With concurrency enabled, a full test run takes approximately 4-5 hours for all four domains with 20+ models
- **Resource Usage**: The framework is optimized for I/O-bound operations and efficiently manages multiple concurrent API calls
- **Output Size**: Results are comprehensive, with a full run generating several megabytes of data artifacts
- **Token Usage**: A complete run with 20+ models generates over 5 million tokens across all domains

You can customize the test scope to reduce costs:
- Run tests on a single domain instead of all domains
- Select a smaller subset of models to test
- Use the `--skip-verification` flag to bypass the model verification step
- Consider using more efficient models for testing routines

## 📝 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- **Peter Luh** who created the [Boswell Test methodology](https://peterl168.substack.com/p/is-ai-chatbot-my-boswell) that this tool implements. His February 2025 research article, "Is AI Chatbot My Boswell?", introduced the concept of LLMs peer-reviewing each other and analyzing grading bias. This implementation automates and extends his pioneering methodology.
- [OpenRouter](https://openrouter.ai/) for providing unified API access to multiple LLMs
- All model providers for creating the amazing AI models that make this test possible