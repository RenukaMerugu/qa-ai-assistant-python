from ollama import chat
from app.prompts.testcase_prompts import build_testcase_prompt


def generate_test_cases(story_name, description):

    prompt = build_testcase_prompt(
        story_name,
        description
    )

    response = chat(
        model="qwen3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print(response["message"]["content"])

    return response["message"]["content"]