#!/usr/bin/env python3
"""
Domain creation utility for Botwell.

This module helps create new domain definition files for the Boswell test.
"""

import os
import sys
import argparse
import re
from pathlib import Path
import time


DOMAIN_TEMPLATE = '''"""
{domain_title} Domain
"""

# Prompts
ESSAY_PROMPT = """
**System/Role**: You are an expert in {domain_expertise}.

**User Query**:
"{essay_question}"

**Response Guidelines**:
- {guideline_1}
- {guideline_2}
- {guideline_3}
- {guideline_4}
- Limit response to around {word_count} words if possible
"""

GRADING_PROMPT = """
**System/Role**: You are a senior professor specializing in {domain_expertise}.

**User Query**:
"Please evaluate the following essay on {topic_short_name}. Focus your assessment on:
1) {grading_focus_1}
2) {grading_focus_2}
3) {grading_focus_3}
4) {grading_focus_4}
5) {grading_focus_5}

Then, **assign a letter grade** (A+, A, A-, B+, B, B-, C+, C, or C-) on a separate line, following the exact format:

```
Grade: <LetterGrade>
```

where `<LetterGrade>` is one of the valid grades above.

Here is the essay to grade:

{{essay}}

Use **only** the valid letter grades provided (no numeric or other scales)."
"""

DOMAIN_INFO = {{
    "name": "{domain_title}",
    "description": "{domain_description}"
}}
'''


def create_domain_file(
    domain_id: str,
    domain_title: str,
    domain_description: str,
    domain_expertise: str, 
    essay_question: str,
    topic_short_name: str,
    word_count: int = 700
) -> str:
    """
    Create a new domain definition file.
    
    Args:
        domain_id: Short ID for the domain (e.g., "econ_1")
        domain_title: Full title of the domain
        domain_description: Description of the domain
        domain_expertise: Area of expertise for the system role
        essay_question: The main essay prompt question
        topic_short_name: Short name for the topic (used in grading prompt)
        word_count: Target word count for essays
        
    Returns:
        Path to the created file
    """
    # Validate domain ID (only allow letters, numbers, and underscores)
    if not re.match(r'^[a-z0-9_]+$', domain_id):
        raise ValueError("Domain ID should only contain lowercase letters, numbers, and underscores")
    
    # Set default guidelines if not provided
    guideline_1 = "Include precise analysis with supporting evidence"
    guideline_2 = "Support your analysis with clear reasoning"
    guideline_3 = "Consider practical implications, not just theoretical aspects"
    guideline_4 = "Present balanced coverage of different perspectives"
    
    # Set default grading focuses if not provided
    grading_focus_1 = "Accuracy and precision of information presented"
    grading_focus_2 = "Depth of analysis and critical thinking"
    grading_focus_3 = "Structure and organization of arguments"
    grading_focus_4 = "Use of relevant examples and supporting evidence"
    grading_focus_5 = "Clarity and coherence of explanations"
    
    # Format domain file content
    domain_content = DOMAIN_TEMPLATE.format(
        domain_title=domain_title,
        domain_description=domain_description,
        domain_expertise=domain_expertise,
        essay_question=essay_question,
        topic_short_name=topic_short_name,
        guideline_1=guideline_1,
        guideline_2=guideline_2,
        guideline_3=guideline_3,
        guideline_4=guideline_4,
        word_count=word_count,
        grading_focus_1=grading_focus_1,
        grading_focus_2=grading_focus_2,
        grading_focus_3=grading_focus_3,
        grading_focus_4=grading_focus_4,
        grading_focus_5=grading_focus_5
    )
    
    # Ensure definitions directory exists
    definitions_dir = "botwell/domains/definitions"
    os.makedirs(definitions_dir, exist_ok=True)
    
    # Create the file
    file_path = os.path.join(definitions_dir, f"{domain_id}.py")
    with open(file_path, 'w') as f:
        f.write(domain_content)
    
    # Add domain to __init__.py in the domains directory
    # NOTE: This is commented out for now, as modifying existing files like __init__.py
    # is typically not done automatically without explicit user confirmation
    # update_domains_init(domain_id, domain_title)
    
    return file_path


def update_domains_init(domain_id: str, domain_title: str) -> None:
    """
    Update the domains/__init__.py file to include the new domain.
    
    Args:
        domain_id: ID of the new domain
        domain_title: Title of the new domain
    """
    init_path = "botwell/domains/__init__.py"
    if not os.path.exists(init_path):
        print(f"Warning: Could not find {init_path} to update")
        return
    
    with open(init_path, 'r') as f:
        content = f.read()
    
    # Find the AVAILABLE_DOMAINS dictionary
    domains_match = re.search(r'AVAILABLE_DOMAINS\s*=\s*{([^}]*)}', content, re.DOTALL)
    if not domains_match:
        print(f"Warning: Could not find AVAILABLE_DOMAINS dictionary in {init_path}")
        return
    
    # Extract the dictionary content
    domains_content = domains_match.group(1)
    
    # Add the new domain to the end of the dictionary
    new_domain_entry = f'    "{domain_id}": "{domain_title}",'
    
    # Check if the domain already exists
    if f'"{domain_id}"' in domains_content:
        print(f"Warning: Domain {domain_id} already exists in AVAILABLE_DOMAINS")
        return
    
    # Add the new domain before the final closing brace
    updated_content = content.replace(
        domains_match.group(0),
        f'AVAILABLE_DOMAINS = {{{domains_content}\n{new_domain_entry}\n}}'
    )
    
    # Write back the updated content
    with open(init_path, 'w') as f:
        f.write(updated_content)


def prompt_for_value(prompt: str, default: str = None) -> str:
    """Prompt the user for a value with an optional default."""
    if default:
        value = input(f"{prompt} [{default}]: ")
        return value or default
    else:
        while True:
            value = input(f"{prompt}: ")
            if value:
                return value
            print("This field is required. Please enter a value.")


def interactive_mode(args):
    """Prompt for missing values in interactive mode."""
    # Domain ID
    domain_id = args.domain_id
    
    # Domain title
    if args.title:
        domain_title = args.title
    else:
        domain_title = prompt_for_value(
            "Enter the full domain title",
            f"Domain {domain_id.replace('_', ' ').title()}"
        )
    
    # Domain description
    if args.description:
        domain_description = args.description
    else:
        domain_description = prompt_for_value(
            "Enter a domain description",
            f"Level {domain_id[-1]} evaluation of {domain_id[:-2]} capabilities."
        )
    
    # Domain expertise
    if args.expertise:
        domain_expertise = args.expertise
    else:
        domain_expertise = prompt_for_value(
            "Enter the area of expertise",
            domain_id[:-2].replace('_', ' ').title()
        )
    
    # Essay question
    if args.question:
        essay_question = args.question
    else:
        essay_question = prompt_for_value("Enter the main essay question")
    
    # Topic short name
    if args.topic:
        topic_short_name = args.topic
    else:
        topic_short_name = prompt_for_value(
            "Enter a short name for the topic",
            domain_expertise.lower()
        )
    
    # Word count
    word_count = args.words
    
    return {
        "domain_id": domain_id,
        "domain_title": domain_title,
        "domain_description": domain_description,
        "domain_expertise": domain_expertise,
        "essay_question": essay_question,
        "topic_short_name": topic_short_name,
        "word_count": word_count
    }


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Create a new domain definition file")
    
    parser.add_argument("domain_id", type=str,
                      help="Short ID for the domain (e.g., 'econ_1', 'physics_2')")
    parser.add_argument("--title", "-t", type=str,
                      help="Full title of the domain")
    parser.add_argument("--description", "-d", type=str,
                      help="Description of the domain")
    parser.add_argument("--expertise", "-e", type=str,
                      help="Area of expertise for the system role")
    parser.add_argument("--question", "-q", type=str,
                      help="The main essay prompt question")
    parser.add_argument("--topic", type=str,
                      help="Short name for the topic (used in grading prompt)")
    parser.add_argument("--words", "-w", type=int, default=700,
                      help="Target word count for essays (default: 700)")
    parser.add_argument("--interactive", "-i", action="store_true",
                      help="Use interactive mode to prompt for missing values")
    
    return parser.parse_args()


def main():
    """Main entry point for the script."""
    args = parse_args()
    
    # Check if we have all required values or should use interactive mode
    if args.interactive:
        print("Entering interactive mode to collect domain information...")
        domain_info = interactive_mode(args)
    else:
        # Use default values for missing arguments
        domain_title = args.title or f"{args.domain_id.replace('_', ' ').title()}"
        domain_description = args.description or f"Level {args.domain_id[-1]} evaluation of {args.domain_id[:-2]} capabilities."
        domain_expertise = args.expertise or args.domain_id[:-2].replace('_', ' ').title()
        essay_question = args.question
        topic_short_name = args.topic or domain_expertise.lower()
        
        # Check if we're missing required values
        if not essay_question:
            print("Error: --question is required. Please provide a question for the prompt or use --interactive.")
            sys.exit(1)
            
        domain_info = {
            "domain_id": args.domain_id,
            "domain_title": domain_title,
            "domain_description": domain_description,
            "domain_expertise": domain_expertise,
            "essay_question": essay_question,
            "topic_short_name": topic_short_name,
            "word_count": args.words
        }
    
    try:
        file_path = create_domain_file(**domain_info)
        print(f"Domain file created at: {file_path}")
        print("\nTo add this domain to AVAILABLE_DOMAINS, edit botwell/domains/__init__.py and add:")
        print(f'    "{domain_info["domain_id"]}": "{domain_info["domain_title"]}",')
    except Exception as e:
        print(f"Error creating domain file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()