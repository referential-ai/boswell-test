# Boswell Test: LLM Comparative Analysis Framework

The Boswell Test is an automated tool for comparing Large Language Models (LLMs) through peer-review, where models grade each other's essays. This implementation is based on the methodology introduced by Peter Luh in his article ["Is AI Chatbot My Boswell?"](https://peterl168.substack.com/p/is-ai-chatbot-my-boswell) (February 2025).

## 🌟 Introduction: How It Works

This tool automates the process of running a Boswell Test across multiple LLMs. Here's how it works:

1. **Essay Generation**: The system prompts multiple LLMs with the same complex question in a specific domain (like political science or computer science)
2. **Peer Evaluation**: Each LLM grades the essays written by all other models, providing detailed feedback and assigning letter grades (A+, A, A-, etc.)
3. **Bias Analysis**: The system analyzes grading patterns to identify which models grade more strictly or leniently compared to the median
4. **Visualization**: The framework generates charts and graphs showing performance metrics, grading distributions, timing data, and cost analysis
5. **Comprehensive Reporting**: Results are organized in timestamped directories with easy-to-read tables in multiple formats (Markdown, ASCII, CSV, JSON)

The Boswell Test methodology offers several advantages over traditional benchmarks:
- It captures nuanced evaluation capabilities, not just raw performance
- It leverages LLMs' own analytical skills to provide detailed feedback
- It reveals biases in how different models evaluate the same work
- It creates a multidimensional view of model capabilities across different domains

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
   git clone https://github.com/yourusername/botwell.git
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

This will sequentially run tests on all domains with the same set of models, creating separate results directories for each domain.

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
│   │   └── ...
│   ├── charts/                    # Data visualizations
│   │   ├── grading_bias.png       # Bar chart of grading bias by model
│   │   ├── grade_distribution.png # Boxplot of grades received by each model
│   │   ├── essay_generation_time.png  # Time comparison for essay generation
│   │   ├── average_grading_time.png   # Time comparison for grading
│   │   ├── cost_breakdown.png     # Cost analysis per model
│   │   └── time_breakdown.png     # Pie chart of process timing
│   ├── grades_table.txt           # ASCII table of all grades
│   ├── grades_table.md            # Markdown table of all grades
│   ├── grades_table.csv           # CSV format for spreadsheet import
│   ├── grading_bias.txt           # ASCII table of grading bias analysis
│   ├── grading_bias.md            # Markdown table of grading bias analysis
│   ├── cost_report.md             # Detailed cost analysis report
│   ├── timing_report.md           # Detailed timing analysis report  
│   ├── grades.json                # Structured grade data in JSON
│   └── full_results.json          # Complete results with all data
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
```markdown
| Model | GPT-4o | Claude | Claude-S | Median Grade |
|-------|--------|--------|----------|--------------|
| GPT-4o | --- | A- | B+ | B+ |
| Claude | A | --- | A- | A- |
| Claude-S | B+ | A | --- | A- |
```

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
```markdown
| Model | Median Given | Grading Bias | Numeric Bias |
|-------|-------------|-------------|-------------|
| GPT-4o | B+ | Slightly Strict (-1/3 grade) | -0.33 |
| Claude | A | Lenient (+1 grade) | 0.35 |
| Claude-S | B+ | Neutral | -0.05 |
| **OVERALL** | B+ | **Baseline** | 0.00 |
```

This analysis helps identify potential biases in how different models evaluate the same content. For example, some models might consistently grade more strictly or leniently than others.

#### 4. Cost Analysis Report

The framework provides detailed cost tracking and analysis:

**Cost Summary Table** (console output):
```
=== COST SUMMARY ===
Total Cost: $2.8764
Total Tokens: 184,392
Total Duration: 45.28 seconds

Essay Generation: $0.8532 (29.7%)
Grading: $2.0232 (70.3%)
See cost_report.md for detailed breakdown
```

**Detailed Cost Report** (`cost_report.md`):
```markdown
# Boswell Test Cost Report

Run timestamp: 2024-06-27 15:43:21
Domain: Political Science - Level 1: AI Policy Analysis

## Summary
- **Total cost**: $2.8764
- **Total tokens**: 184,392
- **Total duration**: 45.28 seconds

## Essay Generation Costs
| Model | Tokens | Cost | Duration (s) |
|-------|--------|------|--------------|
| GPT-4o | 12,586 | $0.2517 | 3.21 |
| Claude-3-Opus | 11,328 | $0.2832 | 4.55 |
| Claude-3-Sonnet | 8,642 | $0.1037 | 2.88 |
| Claude-3.7-Sonnet | 7,924 | $0.0951 | 2.65 |
| GPT-4o-mini | 10,547 | $0.0843 | 2.10 |
| GPT-3.5-Turbo | 6,824 | $0.0352 | 1.93 |
| **TOTAL** | | **$0.8532** | |

## Grading Costs
| Grader | Essays Graded | Total Tokens | Total Cost | Avg. Cost per Essay |
|--------|---------------|--------------|------------|---------------------|
| GPT-4o | 6 | 28,634 | $0.5727 | $0.0954 |
| Claude-3-Opus | 6 | 29,128 | $0.7282 | $0.1214 |
| Claude-3-Sonnet | 6 | 24,715 | $0.2966 | $0.0494 |
| Claude-3.7-Sonnet | 6 | 22,982 | $0.2758 | $0.0460 |
| GPT-4o-mini | 6 | 18,452 | $0.1476 | $0.0246 |
| GPT-3.5-Turbo | 6 | 12,630 | $0.0023 | $0.0004 |
| **TOTAL** | | | **$2.0232** | |

## Cost Breakdown by Phase
| Phase | Cost | Percentage |
|-------|------|------------|
| Essay Generation | $0.8532 | 29.7% |
| Grading | $2.0232 | 70.3% |
| **TOTAL** | **$2.8764** | **100%** |
```

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

These visualizations provide at-a-glance insights into model performance, efficiency, and cost-effectiveness across the different test aspects.

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

## 📈 Sample Results

### Performance Grades

Below is a sample of results from a Boswell Test run, showing median grades and individual evaluations:

| Model              | Median Grade | Grades Received      |
|--------------------|--------------|----------------------|
| GPT-4o             | A-           | A, A-, B+, B+, B+, B+, A, A- |
| Claude-3-Opus      | B+           | B+, A, B+, A-, B+, N/A, B+, A- |
| Claude-3-Sonnet    | B+           | B+, A-, B+, B+, B+, B+, A-, A- |
| Claude-3.7-Sonnet  | A-           | A-, A-, A, B+, B+, A-, A-, A- |
| GPT-4o-mini        | B+           | A-, A, A-, B+, B+, B+, A, B+ |
| Llama-3-8B         | B+           | B, A-, A-, B-, B-, B+, A-, B |
| GPT-3.5-Turbo      | B+           | B+, A-, A-, B-, B, B, B+, B |
| o3-mini-high       | A-           | A, A, A, B+, B+, A-, B+, A- |

### Grading Bias Analysis

The analysis also identifies which models tend to grade more strictly or leniently:

| Model              | Median Given | Grading Bias       | Numeric Bias |
|--------------------|--------------|-------------------|-------------|
| GPT-4o             | B+           | Neutral           | -0.05 |
| Claude-3-Opus      | A-           | Slightly Lenient  | 0.20 |
| Claude-3-Sonnet    | B+           | Neutral           | 0.00 |
| Claude-3.7-Sonnet  | B            | Slightly Strict   | -0.27 |
| GPT-4o-mini        | A-           | Slightly Lenient  | 0.15 |
| Llama-3-8B         | B            | Slightly Strict   | -0.30 |
| GPT-3.5-Turbo      | A-           | Slightly Lenient  | 0.25 |
| o3-mini-high       | B+           | Neutral           | 0.02 |
| **OVERALL**        | B+           | **Baseline**      | 0.00 |

This bias analysis helps identify patterns in how different models evaluate their peers. For instance, in this sample, Claude-3.7-Sonnet and Llama-3-8B appear to be slightly stricter graders, while Claude-3-Opus, GPT-4o-mini, and GPT-3.5-Turbo tend to be slightly more lenient.

## 📊 Timing and Performance Metrics

The Boswell Test framework tracks detailed timing information throughout the testing process:

- **Total Runtime**: Precise tracking of the entire test duration in minutes and seconds
- **Phase Timing**: Breakdown of time spent in essay generation, grading, analysis, and file generation
- **Per-Model Timing**: Tracking how long each model takes to generate essays and grade others
- **Timing Visualizations**: Charts showing relative performance of different models
- **Timing Reports**: Detailed Markdown reports with all timing metrics

This timing information helps identify which models are more efficient and how overall test time is distributed across different phases.

## 🧰 Reliability Features

The Boswell Test framework includes several features to ensure reliable operation:

- **Model Verification**: Automatically tests models with a small prompt before starting the main test
- **Retry Logic**: Automatically retries failed API calls up to a configurable number of times
- **Error Handling**: Gracefully handles API errors and prevents script crashes
- **Flexible Grade Extraction**: Finds grades in different formats even if they don't follow the exact requested format
- **Comprehensive Logging**: Detailed console feedback throughout the testing process
- **Domain Independence**: Run tests across all domains with a single command
- **Robust Visualizations**: Charts adapt to missing or incomplete data

## 🧩 Extending the Framework

### Creating New Domains

To create a new test domain:

1. Create a new file in the `domains/` directory (e.g., `domains/my_domain.py`)
2. Define `ESSAY_PROMPT`, `GRADING_PROMPT`, and `DOMAIN_INFO` variables
3. Add the domain to the `AVAILABLE_DOMAINS` dictionary in `boswell_test.py`
4. The domain will automatically be available via the `--domain` flag

### Adding New Models

Edit the `MODELS` list in `boswell_test.py` to add or remove models from OpenRouter. The script is pre-configured with models known to work with OpenRouter. If you want to try additional models:

1. Check the available models on [OpenRouter](https://openrouter.ai/docs/models)
2. Add them to the `MODELS` list in the format `{"name": "Model-Name", "model_id": "provider/model-id"}`
3. The model verification step will automatically filter out any models that aren't available

## 📝 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- **Peter Luh** who created the [Boswell Test methodology](https://peterl168.substack.com/p/is-ai-chatbot-my-boswell) that this tool implements. His February 2025 research article, "Is AI Chatbot My Boswell?", introduced the concept of LLMs peer-reviewing each other and analyzing grading bias. This implementation automates and extends his pioneering methodology.
- [OpenRouter](https://openrouter.ai/) for providing unified API access to multiple LLMs
- All model providers for creating the amazing AI models that make this test possible