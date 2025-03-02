"""
Test Domain 1 Domain
"""

# Prompts
ESSAY_PROMPT = """
**System/Role**: You are an expert in Test Domain.

**User Query**:
"What are the best practices for test-driven development?"

**Response Guidelines**:
- Include precise analysis with supporting evidence
- Support your analysis with clear reasoning
- Consider practical implications, not just theoretical aspects
- Present balanced coverage of different perspectives
- Limit response to around 700 words if possible
"""

GRADING_PROMPT = """
**System/Role**: You are a senior professor specializing in Test Domain.

**User Query**:
"Please evaluate the following essay on test domain. Focus your assessment on:
1) Accuracy and precision of information presented
2) Depth of analysis and critical thinking
3) Structure and organization of arguments
4) Use of relevant examples and supporting evidence
5) Clarity and coherence of explanations

Then, **assign a letter grade** (A+, A, A-, B+, B, B-, C+, C, or C-) on a separate line, following the exact format:

```
Grade: <LetterGrade>
```

where `<LetterGrade>` is one of the valid grades above.

Here is the essay to grade:

{essay}

Use **only** the valid letter grades provided (no numeric or other scales)."
"""

DOMAIN_INFO = {
    "name": "Test Domain 1",
    "description": "Level 1 evaluation of test_domain capabilities."
}
