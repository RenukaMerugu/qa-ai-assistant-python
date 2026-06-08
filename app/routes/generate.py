from fastapi import APIRouter
from app.services.ollama_service import generate_test_cases

router = APIRouter()


@router.post("/generate")
def generate(payload: dict):

    result = generate_test_cases(
        payload["story_name"],
        payload["description"]
    )

    return {
        "raw_response": result
    }