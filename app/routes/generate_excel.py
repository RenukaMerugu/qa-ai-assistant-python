from fastapi import APIRouter
from app.services.ollama_service import generate_test_cases
from app.services.excel_service import create_excel

router = APIRouter()


@router.post("/generate-excel")
def generate_excel(payload: dict):

    ai_response = generate_test_cases(
        payload["story_name"],
        payload["description"]
    )

    excel_file = create_excel(
        ai_response,
        payload["story_name"]
    )

    return {
        "message": "Excel created successfully",
        "file": excel_file
    }