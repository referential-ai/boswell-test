"""
Programming Domain 1 - Level 1 Coding Fundamentals
"""

# Prompts
ESSAY_PROMPT = """
**System/Role**: You are an experienced software engineer with expertise in TypeScript, Python, Rust, and C programming languages.

**User Query**:
"Implement the following three classic programming problems in all four languages: TypeScript, Python, Rust, and C.

1) FizzBuzz:
   - Print numbers from 1 to 100
   - For multiples of 3, print 'Fizz' instead of the number
   - For multiples of 5, print 'Buzz' instead of the number
   - For multiples of both 3 and 5, print 'FizzBuzz'

2) Palindrome Checker:
   - Write a function that accepts a string and returns true/false depending on whether it reads the same backward as forward
   - Ignore case and non-alphanumeric characters
   - Example: 'A man, a plan, a canal: Panama' should return true

3) Binary Search:
   - Implement an iterative binary search function
   - The function should return the index of a target value in a sorted array, or -1 if not found
   - Example input: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], target = 7
   - Expected output: 6 (index of value 7)

For each language implementation:
- Include complete, runnable code
- Use proper syntax and follow language conventions
- Include basic error handling
- Organize your code with appropriate functions

Present your solution with each language's implementation in order: TypeScript, Python, Rust, then C."

**Response Guidelines**:
- Provide complete, working code that would run correctly without modification
- Include necessary imports and function declarations
- Follow language-specific idioms and best practices
- Keep solutions concise while ensuring correctness
"""

GRADING_PROMPT = """
**System/Role**: You are a technical interviewer with expertise in multiple programming languages and a focus on code correctness and quality.

**User Query**:
"Evaluate the following programming solutions for FizzBuzz, Palindrome Checker, and Binary Search implemented in TypeScript, Python, Rust, and C. 

Assess the solutions based on these criteria:
1) **Correctness**: Do the implementations work as expected? Are there any bugs or logic errors?

2) **Code Quality**: Does the code follow language conventions and best practices? Is it well-structured and readable?

3) **Completeness**: Are all three problems implemented in all four languages?

4) **Error Handling**: Does the code handle potential errors appropriately?

For each language implementation, identify any issues or areas for improvement. Be specific and thorough in your assessment.

Then, assign an overall letter grade (A+, A, A-, B+, B, B-, C+, C, or C-) on a separate line, following the exact format:

```
Grade: <LetterGrade>
```

where `<LetterGrade>` is one of the valid grades above.

Here is the code to evaluate:

{essay}

Use **only** the valid letter grades provided (no numeric or other scales)."
"""

DOMAIN_INFO = {
    "name": "Programming - Level 1: Coding Fundamentals",
    "description": "Level 1 evaluation of programming fundamentals through FizzBuzz, Palindrome Checker, and Binary Search implementations in TypeScript, Python, Rust, and C."
}