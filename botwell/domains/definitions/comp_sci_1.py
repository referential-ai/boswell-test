"""
Computer Science Domain 1 - Level 1 Algorithm Analysis
"""

# Prompts
ESSAY_PROMPT = """
**System/Role**: You are a computer science expert with deep knowledge of algorithms and data structures.

**User Query**:
"Compare and analyze the time and space complexity trade-offs between different sorting algorithms (e.g., quicksort, mergesort, heapsort, etc.).
Discuss the following aspects:
1) Best, average, and worst-case time complexities
2) Space complexity requirements
3) Real-world considerations beyond Big O analysis
4) Scenarios where each algorithm would be the optimal choice

Provide concrete examples to illustrate the practical implications of these theoretical differences."

**Response Guidelines**:
- Include precise mathematical analysis of complexity
- Support your analysis with clear reasoning
- Consider practical implementation details, not just theoretical aspects
- Present balanced coverage of multiple sorting algorithms
- Limit response to around 600-700 words if possible
"""

GRADING_PROMPT = """
**System/Role**: You are a senior computer science professor specializing in algorithms and computational complexity.

**User Query**:
"Please evaluate the following essay on sorting algorithm complexity. Focus your assessment on:
1) Technical accuracy of the complexity analysis
2) Depth of understanding of algorithm characteristics
3) Correctness of the comparative analysis
4) Balance between theoretical foundations and practical applications
5) Clarity of explanations for technical concepts

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
    "name": "Computer Science - Level 1: Algorithm Analysis",
    "description": "Level 1 evaluation of understanding and analysis of sorting algorithms and complexity."
}