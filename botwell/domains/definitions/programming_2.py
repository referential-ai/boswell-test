"""
Programming Domain 2 - Level 2 Advanced Algorithms
"""

# Prompts
ESSAY_PROMPT = """
**System/Role**: You are a senior software engineer with deep expertise in algorithm implementation across TypeScript, Python, Rust, and C programming languages.

**User Query**:
"Implement the following three algorithmic problems in all four languages: TypeScript, Python, Rust, and C.

1) N-Queens Problem:
   - Implement a solution to the 8-Queens problem (placing 8 queens on an 8×8 chessboard with no two queens threatening each other)
   - Use a backtracking approach
   - Return the count of all valid solutions and print one valid solution

2) Longest Common Subsequence:
   - Implement a function that finds the longest common subsequence of two strings
   - Example: LCS of "ABCBDAB" and "BDCABA" is "BCBA" (length 4)
   - Use dynamic programming for optimal performance
   - Return both the length and the actual subsequence

3) Graph Traversal - Shortest Path:
   - Implement Dijkstra's algorithm to find the shortest path between two vertices in a weighted graph
   - Represent the graph using an adjacency list
   - The function should return the shortest path and its total weight
   - Include a sample graph implementation with at least 6 vertices

For each language implementation:
- Include complete, runnable code
- Use proper data structures appropriate for each language
- Implement error handling and edge cases
- Focus on correctness first, then efficiency
- Include brief comments explaining your approach

Present your solutions with each language's implementation in order: TypeScript, Python, Rust, then C."

**Response Guidelines**:
- Provide complete, working code that would run correctly without modification
- Include necessary imports, type declarations, and helper functions
- Follow language-specific best practices and idioms
- Balance readability and performance
- Ensure your code handles edge cases appropriately
"""

GRADING_PROMPT = """
**System/Role**: You are a principal engineer who specializes in algorithm analysis, optimization, and multi-language implementation.

**User Query**:
"Rigorously evaluate the following implementations of the N-Queens problem, Longest Common Subsequence, and Dijkstra's shortest path algorithm in TypeScript, Python, Rust, and C.

Your evaluation should focus on:

1) **Algorithmic Correctness**: Do the implementations correctly solve each problem? Are there any logical errors or edge cases not handled properly?

2) **Algorithmic Efficiency**: Are the time and space complexity optimal for each problem? Are there any inefficient operations that could be improved?

3) **Language-Specific Implementation**: Does each implementation leverage the strengths and idioms of its language? Is the code idiomatic?

4) **Code Quality and Structure**: Is the code well-organized, readable, and maintainable? Are variables and functions named appropriately?

5) **Error Handling**: Are potential errors and edge cases handled gracefully?

For each language implementation, provide a detailed critique identifying specific strengths and weaknesses. Point out any bugs, inefficiencies, or improvements that could be made.

Then, assign an overall letter grade (A+, A, A-, B+, B, B-, C+, C, or C-) on a separate line, following the exact format:

```
Grade: <LetterGrade>
```

where `<LetterGrade>` is one of the valid grades above.

Here is the code to evaluate:

{essay}

Use **only** the valid letter grades provided (no numeric or other scales). When in doubt between two grades, assign the lower one."
"""

DOMAIN_INFO = {
    "name": "Programming - Level 2: Advanced Algorithms",
    "description": "Level 2 evaluation of advanced algorithm implementation through N-Queens, Longest Common Subsequence, and Dijkstra's algorithm in TypeScript, Python, Rust, and C."
}