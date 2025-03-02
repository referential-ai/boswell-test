"""
Programming Domain 3 - Level 3 Competitive Programming Challenges
"""

# Prompts
ESSAY_PROMPT = """
**System/Role**: You are an elite competitive programmer with expertise in algorithm optimization and advanced data structures across TypeScript, Python, Rust, and C programming languages.

**User Query**:
"Implement the following three advanced competitive programming problems in all four languages: TypeScript, Python, Rust, and C.

1) Segment Tree with Lazy Propagation:
   - Implement a segment tree with lazy propagation to handle range updates and range queries efficiently
   - Support the following operations:
     * Range sum query: Find the sum of elements in a given range
     * Range update: Add a value to all elements in a given range
   - Time complexity should be O(log n) for both operations
   - Include a demonstration with at least 10 operations on an array of size 10^5

2) Suffix Array and LCP Array:
   - Implement a solution to build a suffix array and LCP (Longest Common Prefix) array for a given string
   - The suffix array should be constructed in O(n log n) time 
   - Implement a function that uses these arrays to find the longest repeated substring in the text
   - Include a demonstration with a string of at least 1000 characters

3) Maximum Flow with Dinic's Algorithm:
   - Implement Dinic's algorithm for finding maximum flow in a network
   - The algorithm should use a combination of level graphs and blocking flows for efficiency
   - Time complexity should be O(V²E) or better
   - Include a demonstration with a non-trivial graph (at least 50 vertices and 200 edges)
   - Show how the algorithm correctly handles a complex network with multiple source/sink paths

For each language implementation:
- Include complete, runnable code with proper encapsulation
- Optimize for both correctness and performance
- Use appropriate data structures for each language
- Include comprehensive error handling and edge case validation
- Add detailed comments explaining the algorithmic approach and optimization techniques

Present your solutions with each language's implementation in order: TypeScript, Python, Rust, then C."

**Response Guidelines**:
- Provide complete, working code with optimal time and space complexity
- Include necessary type definitions, helper functions, and data structures
- Focus on both algorithmic correctness and performance optimization
- Explain critical optimization techniques employed in each solution
- Ensure solutions handle edge cases and demonstrate correctness with examples
"""

GRADING_PROMPT = """
**System/Role**: You are a world-class competitive programming coach with experience judging international algorithm competitions.

**User Query**:
"Conduct a thorough evaluation of the following implementations of advanced algorithms: Segment Tree with Lazy Propagation, Suffix Array with LCP, and Dinic's Maximum Flow algorithm in TypeScript, Python, Rust, and C.

Your evaluation must comprehensively assess:

1) **Algorithmic Correctness**: Are the implementations mathematically sound? Do they handle all edge cases? Are there any subtle bugs that would fail on specific inputs?

2) **Algorithmic Efficiency**: Are the implementations optimized to the theoretical time complexity limits? Identify any sub-optimal operations or missed optimization opportunities.

3) **Language Optimization**: Does each implementation leverage language-specific optimizations and idioms? Are there missed opportunities to use specialized data structures or language features?

4) **Code Quality and Clarity**: Despite the complexity of these algorithms, is the code structured clearly? Would another competitive programmer be able to understand and modify the implementation?

5) **Error Handling and Robustness**: How well do the implementations handle unexpected inputs, edge cases, or potential runtime issues?

For each language implementation, provide a detailed analysis identifying specific strengths, weaknesses, optimizations, and theoretical or practical limitations. Compare the implementation against what would be expected in a high-level competitive programming contest.

Then, assign an overall letter grade (A+, A, A-, B+, B, B-, C+, C, or C-) on a separate line, following the exact format:

```
Grade: <LetterGrade>
```

where `<LetterGrade>` is one of the valid grades above.

Here is the code to evaluate:

{essay}

Use **only** the valid letter grades provided (no numeric or other scales). Be exceptionally strict in your evaluation - an A+ should only be given to implementations that would be competitive at the highest levels of programming contests."
"""

DOMAIN_INFO = {
    "name": "Programming - Level 3: Competitive Programming Challenges",
    "description": "Level 3 evaluation of elite algorithm implementation through Segment Trees with Lazy Propagation, Suffix Arrays, and Dinic's Maximum Flow in TypeScript, Python, Rust, and C."
}