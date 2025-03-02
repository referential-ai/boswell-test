"""
Domain definitions and loading for Boswell tests.
"""

import importlib
from typing import Tuple, Dict

# Available domains
AVAILABLE_DOMAINS = {
    "pol_sci_1": "Political Science - Level 1: AI Policy Analysis",
    "pol_sci_2": "Political Science - Level 2: AI Governance Analysis",
    "comp_sci_1": "Computer Science - Level 1: Algorithm Analysis",
    "comp_sci_2": "Computer Science - Level 2: System Design",
    "programming_1": "Programming - Level 1: Coding Fundamentals",
    "programming_2": "Programming - Level 2: Advanced Algorithms",
    "programming_3": "Programming - Level 3: Competitive Programming Challenges",
    "humanities_1": "Humanities - Level 1: Social Philosophy"
}


def load_domain(domain_name: str) -> Tuple[str, str, Dict[str, str]]:
    """Load the specified domain module and return its prompts."""
    try:
        domain_module = importlib.import_module(f"botwell.domains.definitions.{domain_name}")
        return (
            domain_module.ESSAY_PROMPT, 
            domain_module.GRADING_PROMPT,
            domain_module.DOMAIN_INFO
        )
    except (ImportError, AttributeError) as e:
        raise ImportError(f"Error loading domain '{domain_name}': {e}")