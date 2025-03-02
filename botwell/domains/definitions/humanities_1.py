DOMAIN_INFO = {
    "name": "Humanities - Level 1: Social Philosophy",
    "description": "Explore basic ideas in social philosophy, focusing on how society works and how we can balance personal freedom with community needs.",
    "level": 1,
    "category": "Humanities"
}

ESSAY_PROMPT = """
Write a clear essay in response to the following prompt:

"Is it possible to solve all human problems? While this may seem like an overreach, consider how addressing issues such as conflict, poverty, and inequality can begin by changing the way we think and act. Imagine a world where people cooperate more, value kindness, and share resources fairly.

Consider practical steps like:
- Encouraging cooperation and empathy in everyday life,
- Creating economic systems that support fairness and help everyone,
- Teaching critical thinking and emotional skills in schools,
- Improving government decisions to better serve the public,
- Shifting cultural values to reward those who help others.

At the same time, recognize the challenges. People have different habits, beliefs, and ways of living, so changing long-held practices is not easy. How can society balance personal freedom with the needs of the community? What obstacles might arise, and how could they be overcome?

Task:
Discuss the merits and limitations of this vision. Use examples or ideas from social philosophy, ethics, political science, or related fields. Your essay should include a clear introduction, organized arguments, and a conclusion that summarizes your ideas."
"""

GRADING_PROMPT = """
You are an expert in humanities and social philosophy. Evaluate the following essay response according to these criteria. Read the essay carefully and provide detailed feedback on each point. Then, assign a final grade.

Evaluation Criteria:

1. Depth of Analysis:
   - Does the essay consider the main ideas of the prompt?
   - Does it discuss both the strengths and weaknesses of the vision?

2. Quality of Argumentation:
   - Is the essay organized with a clear thesis and supporting arguments?
   - Are the ideas explained with simple, logical reasoning?

3. Knowledge Integration:
   - Does the essay incorporate relevant ideas from social philosophy or related fields?
   - Are basic theories or examples used to support the argument?

4. Critical Thinking:
   - Does the essay thoughtfully examine the balance between individual freedom and community needs?
   - Are potential challenges acknowledged and possible solutions suggested?

5. Balanced Perspective:
   - Does the essay offer a fair and balanced view of the ideas presented?
   - Are different viewpoints considered without overcomplicating the discussion?

Overall Assessment and Grade:
Summarize the strengths and weaknesses of the essay, and assign a final grade using one of the following: A+, A, A-, B+, B, B-, C+, C, or C-.

Essay for Evaluation:

{essay}
"""
