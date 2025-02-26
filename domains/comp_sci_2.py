"""
Computer Science Domain 2 - Level 2 System Design
"""

# Prompts
ESSAY_PROMPT = """
**System/Role**: You are a senior software architect with expertise in distributed systems and scalable architecture.

**User Query**:
"Design a scalable, fault-tolerant backend system for a real-time collaborative document editing platform (similar to Google Docs). Your design should address:

1) Core architectural components and their interactions
2) Data consistency and conflict resolution mechanisms 
3) Scalability considerations for supporting millions of concurrent users
4) Fault tolerance and disaster recovery strategies
5) Performance optimizations for real-time collaboration

Include specific technology choices where relevant, justifying your selections based on the system requirements."

**Response Guidelines**:
- Provide a comprehensive system architecture that addresses all requirements
- Include technical details of data models, APIs, and communication protocols
- Discuss trade-offs in your design decisions with clear rationales
- Address both theoretical principles and practical implementation concerns
- Demonstrate understanding of distributed systems challenges (CAP theorem, eventual consistency, etc.)
- Limit response to around 800-900 words
"""

GRADING_PROMPT = """
**System/Role**: You are a principal systems engineer at a major tech company who evaluates system design proposals. You have decades of experience building large-scale distributed systems.

**User Query**:
"Conduct a rigorous technical review of the following system design proposal. Evaluate it based on:

1) Architectural soundness: Is the overall architecture appropriate for the requirements? Are components well-defined with clear responsibilities?

2) Scalability: Does the design handle increased load effectively? Are there potential bottlenecks?

3) Fault tolerance: How well does the system handle failures? Are redundancy and recovery mechanisms adequately addressed?

4) Consistency model: Is the data consistency approach appropriate for real-time collaboration? Are conflict resolution strategies viable?

5) Technical feasibility: Are the proposed technologies appropriate? Has the author demonstrated understanding of their capabilities and limitations?

6) Completeness: Are all critical aspects of the system addressed, or are there significant gaps?

Be exacting in your assessment. Identify specific strengths and weaknesses, evaluating both the theoretical understanding and practical implementation considerations.

Then, assign a letter grade (A+, A, A-, B+, B, B-, C+, C, or C-) on a separate line, following the exact format:

```
Grade: <LetterGrade>
```

Here is the system design proposal to evaluate:

{essay}

Use only the valid letter grades provided (no numeric or other scales). When in doubt between two grades, assign the lower one."
"""

DOMAIN_INFO = {
    "name": "Computer Science - Level 2: System Design",
    "description": "Level 2 evaluation of system architecture and distributed systems knowledge."
}