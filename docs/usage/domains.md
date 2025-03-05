# Domain Guide

The Botwell framework uses "domains" to define test scenarios. Each domain contains a specific prompt for essay generation and a corresponding grading prompt.

## Available Domains

The framework includes multiple testing domains, each with different difficulty levels:

### Political Science
- `pol_sci_1`: Level 1: AI policy analysis
- `pol_sci_2`: Level 2: AI governance analysis with rigorous grading

### Computer Science
- `comp_sci_1`: Level 1: Algorithm analysis and complexity
- `comp_sci_2`: Level 2: System design for distributed applications

### Programming
- `programming_1`: Level 1: Coding Fundamentals
- `programming_2`: Level 2: Advanced Algorithms
- `programming_3`: Level 3: Competitive Programming Challenges

### Humanities
- `humanities_1`: Level 1: Social Philosophy

## Listing Available Domains

To see all available domains:

```bash
botwell --list-domains
```

## Creating New Domains

You can create your own custom domains using the `create-domain` subcommand:

### Interactive Mode

```bash
botwell create-domain
```

This will guide you through the process of defining:
- Domain title
- Area of expertise required
- Essay question
- Other necessary parameters

The tool works in interactive mode, guiding you through the creation process.

## Domain Structure

Each domain is defined by a Python file that contains:

1. `ESSAY_PROMPT`: The prompt given to models to generate essays
2. `GRADING_PROMPT`: The prompt for peer-grading other essays
3. `DOMAIN_INFO`: Metadata about the domain (title, difficulty, etc.)

Example domain structure:

```python
ESSAY_PROMPT = """
You are an expert in [FIELD]. Answer the following question thoroughly:

[DETAILED QUESTION]

Provide a well-structured response with clear sections, evidence, and reasoning.
"""

GRADING_PROMPT = """
You are a professor of [FIELD]. Grade the following essay in response to this question:

[QUESTION]

Essay to grade:
[ESSAY]

Provide detailed feedback on:
1. Content accuracy and depth
2. Critical analysis
3. Structure and organization
4. Evidence and examples
5. Writing quality

Assign a letter grade (A+, A, A-, B+, B, B-, C+, C, C-, D, or F) and explain your reasoning.
Your response should follow this format:
[DETAILED FEEDBACK]

Letter Grade: [GRADE]
"""

DOMAIN_INFO = {
    "title": "Domain Title - Level X: Specific Focus",
    "description": "Level X evaluation of specific capabilities.",
    "difficulty": X,  # 1-5 scale
    "expertise": "Required expertise"
}
```

## Using Custom Domains

After creating a custom domain, it will automatically become available when using the `--domain` flag:

```bash
botwell --domain my_custom_domain
```