def build_testcase_prompt(story_name, description):
    return f"""
Act as a Senior QA Engineer.

Generate at least:

- Functional Test Cases
- Negative Test Cases
- Boundary Test Cases

For every testcase provide:

Title
Priority
Preconditions
Steps
Expected Result

Return in plain text.

Story Name:
{story_name}

Description:
{description}
"""