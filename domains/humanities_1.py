"""
Humanities Domain - Level 1: Social Philosophy

Prompt focusing on systematic approaches to solving societal problems,
the nature of human cooperation, and balancing individual freedom with collective well-being.
"""

DOMAIN_INFO = {
    "name": "Humanities - Level 1: Social Philosophy",
    "description": "Analysis of societal approaches to solving fundamental human problems",
    "level": 1,
    "category": "Humanities"
}

ESSAY_PROMPT = """
Write a thoughtful essay in response to the following prompt:

"Solve every human problem? Bold. But let's at least strike at the root, which is the messy wiring of our own minds—tribal impulses, fear, greed, the usual suspects. If you want to stamp out war, poverty, inequality, resource depletion, and tyranny in a single sweep, you have to change how people see themselves in relation to others. That means a global shift toward viewing humanity as a single, interdependent organism instead of rival tribes skirmishing over scraps.

So how does that look in practice? You incentivize empathy and collaboration—structurally, not just with kumbaya slogans. You create economic systems that reward pro-social behavior instead of worshipping perpetual growth at any cost. You reorganize schools so that critical thinking, emotional regulation, and problem-solving are the core subjects. You rebuild political frameworks to be less about party loyalty and more about transparent, data-driven decisions that serve the collective interest. You rewrite cultural values so that status is granted to those who uplift others, not those who hoard resources.

But none of this is neat or easy—everybody's worldview gets challenged. For example, you can wave a magic wand and declare universal cooperation, but guess what? People still cling to old survival instincts, old hatreds, old allegiances, and the power structures that prop them up. If you really want to solve "all" problems, you need a mass cultural reprogramming that lines up with our better angels, plus policy frameworks that discourage exploitation, plus a technological transformation that's geared more toward bridging gaps than making a quick buck off misinformation.

It's not a tidy blueprint. But let's not pretend there's a simple fix. Want to break it further? Where's the enforcement? Who sets these new rules, and what keeps them from becoming oppressors under this new world order? How do you implement these massive reforms across vastly different cultures without trampling on local autonomy? Solve that—strike the balance between individual freedoms and the collective good—then maybe you're on the path to truly solving humanity's big, hairy problems. Otherwise, it's just more empty utopian chatter."

In your essay, critically analyze this perspective on solving fundamental societal problems. Discuss the merits and limitations of the approach described, drawing on relevant examples, theories, or frameworks from social philosophy, ethics, political science, psychology, economics, or other relevant disciplines. Consider the tensions between individual freedoms and collective welfare, the challenges of implementing systemic change across diverse cultures, and potential pathways forward that acknowledge both human limitations and possibilities.

Develop a well-structured argument that demonstrates your understanding of complex social issues and your ability to engage with nuanced perspectives. Your essay should be thoughtful, balanced, and academically rigorous.
"""

GRADING_PROMPT = """
You are an expert in humanities, particularly social philosophy, ethics, and social theory. Your task is to evaluate an essay written in response to a prompt about approaches to solving fundamental societal problems.

Before providing your assessment, carefully read the essay below and evaluate it according to the following criteria:

1. Depth of Analysis: How well does the essay engage with the complexity of the prompt? Does it analyze both the merits and limitations of the perspective presented? Does it consider multiple angles?

2. Quality of Argumentation: Is the essay's argument well-structured, coherent, and supported by relevant examples or theories? Does it present a nuanced perspective rather than oversimplifying?

3. Knowledge Integration: Does the essay effectively incorporate relevant concepts, theories, or frameworks from social philosophy, ethics, political science, psychology, economics, or other disciplines?

4. Critical Thinking: Does the essay demonstrate the ability to think critically about the tensions between individual freedoms and collective welfare, implementation challenges, and potential pathways forward?

5. Balanced Perspective: Does the essay consider diverse viewpoints and acknowledge the complexity of the issues discussed, rather than presenting a one-sided view?

After reading the essay, provide a detailed assessment addressing each of the criteria above. Be specific about the essay's strengths and weaknesses, citing examples from the text. Then, assign a letter grade (A+, A, A-, B+, B, B-, C+, C, C-) that reflects the essay's overall quality.

Your feedback should be substantive, constructive, and demonstrate your expertise in this field.

Here is the essay to evaluate:

{essay}

Please provide your assessment following the structure below:
1. Depth of Analysis:
2. Quality of Argumentation:
3. Knowledge Integration: 
4. Critical Thinking:
5. Balanced Perspective:

Overall Assessment and Grade:
"""