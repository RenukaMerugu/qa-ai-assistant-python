import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("JIRA_BASE_URL")
PROJECT_ID = int(os.getenv("JIRA_PROJECT_ID"))
FOLDER_ID = int(os.getenv("JIRA_FOLDER_ID"))
STATUS_ID = int(os.getenv("JIRA_STATUS_ID"))
TOKEN = os.getenv("JIRA_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def create_test_case(title):

    payload = {
        "projectId": PROJECT_ID,
        "name": title,
        "folderId": FOLDER_ID,
        "statusId": STATUS_ID,
        "testData": [],
        "parameters": []
    }

    response = requests.post(
        f"{BASE_URL}/rest/tests/1.0/testcase",
        headers=HEADERS,
        json=payload
    )

    response.raise_for_status()

    return response.json()


def update_test_script(test_case_id, steps, expected_result):

    payload = {
        "id": test_case_id,
        "projectId": 23404,
        "testScript": {
            "stepByStepScript": {
                "steps": [
                    {
                        "index": 0,
                        "description": steps,
                        "expectedResult": expected_result,
                        "customFieldValueIndex": {},
                        "customFieldValues": []
                    }
                ]
            }
        },
        "testData": [],
        "parameters": []
    }

    response = requests.put(
        f"{BASE_URL}/rest/tests/1.0/testcase/{test_case_id}",
        headers=HEADERS,
        json=payload
    )

    print("STATUS =", response.status_code)
    print("BODY =")
    print(response.text)

    return response.text