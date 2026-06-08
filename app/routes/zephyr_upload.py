from fastapi import APIRouter

from app.services.zephyr_service import (
    create_test_case,
    update_test_script
)

router = APIRouter()


@router.post("/upload-to-zephyr")
async def upload_to_zephyr(
    payload: dict
):

    testcases = payload["test_cases"]

    created = []

    for tc in testcases:

        created_tc = create_test_case(
            tc["title"]
        )

        update_test_script(
            created_tc["id"],
            tc["steps"],
            tc["expectedResult"]
        )

        created.append(
            {
                "key": created_tc["key"],
                "id": created_tc["id"],
                "title": tc["title"]
            }
        )

    return {
        "message":
            f"{len(created)} test cases uploaded successfully",
        "created_testcases":
            created
    }