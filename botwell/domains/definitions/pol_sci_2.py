"""
Political Science Domain 2 - Level 2 AI Governance Analysis
"""

# Prompts
ESSAY_PROMPT = """
**System/Role**: You are a world-class AI policy researcher with deep expertise in international relations, technology ethics, and governance.

**User Query**:
"Analyze the emerging tensions between national AI sovereignty and global governance frameworks. 
Consider specific policies from at least three major AI powers (e.g., US, EU, China), discussing:
1) How regulatory approaches reflect underlying philosophical and ethical assumptions
2) The implications for global AI development and deployment
3) Concrete examples where these tensions manifest in technical standards, data governance, or security policies

Support your analysis with references to specific policy documents, international agreements, and scholarly perspectives. 
Address potential future scenarios where these tensions might be resolved or exacerbated."

**Response Guidelines**:
- Demonstrate sophisticated understanding of both technical and policy dimensions
- Provide nuanced, non-obvious insights that go beyond superficial comparisons
- Maintain logical coherence while addressing complex, interconnected issues
- Ground analysis in specific examples and evidence rather than generalities
- Limit response to around 800-900 words
"""

GRADING_PROMPT = """
**System/Role**: You are a distinguished scholar in international technology policy with expertise across political science, computer science, and ethics. You have a reputation for maintaining exceptionally high standards in academic evaluation.

**User Query**:
"Conduct a rigorous evaluation of the following essay using a demanding intellectual framework. Focus your assessment on:

1) Analytical depth: Does the essay offer genuine insights beyond common knowledge? Does it demonstrate understanding of subtle distinctions and complex interactions between policy domains?

2) Evidentiary rigor: Does the essay ground claims in specific policies, documents or scholarly perspectives? Are examples precise and relevant rather than vague or generic?

3) Logical coherence: Does the argument flow consistently, avoiding contradictions or unwarranted leaps? Are connections between ideas clearly articulated?

4) Sophistication: Does the essay demonstrate nuanced understanding of competing values and perspectives in AI governance? Does it avoid simplistic characterizations?

5) Distinctive thought: Does the essay contain original observations or frameworks rather than merely restating conventional wisdom?

Be exacting in your evaluation. Reward genuine intellectual contribution while penalizing superficiality, vagueness, or reliance on generalities. Grade harshly but fairly.

Then, assign a letter grade (A+, A, A-, B+, B, B-, C+, C, or C-) on a separate line, following the exact format:

```
Grade: <LetterGrade>
```

Here is the essay to grade:

{essay}

Use only the valid letter grades provided (no numeric or other scales). When in doubt between two grades, assign the lower one."
"""

DOMAIN_INFO = {
    "name": "Political Science - Level 2 AI Governance Analysis",
    "description": "Level 2 test of sophisticated AI governance analysis with rigorous grading."
}