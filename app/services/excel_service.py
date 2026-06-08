from openpyxl import Workbook
from datetime import datetime
import os


def create_excel(ai_response, story_name):

    wb = Workbook()
    ws = wb.active
    ws.title = "Test Cases"

    headers = [
        "TC_ID",
        "Type",
        "Title",
        "Priority",
        "Preconditions",
        "Steps",
        "Expected Result"
    ]

    ws.append(headers)

    lines = ai_response.split("\n")

    tc_id = 1

    current_type = ""

    title = ""
    priority = ""
    preconditions = ""
    steps = ""
    expected_result = ""

    for line in lines:

        line = line.strip()

        if "Functional Test Cases" in line:
            current_type = "Functional"
            continue

        if "Negative Test Cases" in line:
            current_type = "Negative"
            continue

        if "Boundary Test Cases" in line:
            current_type = "Boundary"
            continue

        if line.startswith("Title:"):

            if title:
                ws.append([
                    f"TC{tc_id:03}",
                    current_type,
                    title,
                    priority,
                    preconditions,
                    steps,
                    expected_result
                ])

                tc_id += 1

            title = line.replace("Title:", "").strip()
            priority = ""
            preconditions = ""
            steps = ""
            expected_result = ""

        elif line.startswith("Priority:"):
            priority = line.replace("Priority:", "").strip()

        elif line.startswith("Preconditions:"):
            preconditions = line.replace("Preconditions:", "").strip()

        elif line.startswith("Expected Result:"):
            expected_result = line.replace(
                "Expected Result:",
                ""
            ).strip()

        elif line.startswith("Steps:"):
            steps = ""

        elif line.startswith("1.") or line.startswith("2.") \
                or line.startswith("3.") or line.startswith("4."):
            steps += line + "\n"

    if title:
        ws.append([
            f"TC{tc_id:03}",
            current_type,
            title,
            priority,
            preconditions,
            steps,
            expected_result
        ])

    os.makedirs("exports", exist_ok=True)

    from datetime import datetime

    safe_story_name = story_name.replace(" ", "_")

    filename = (
        f"exports/{safe_story_name}_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

    wb.save(filename)

    return filename