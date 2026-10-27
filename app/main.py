import logging
from google.genai.errors import APIError


from fastapi import FastAPI, HTTPException


from app.data import (
    load_employees,
    get_employee,
    search_employees,
)
from app.models import GenerateRequest, LearningPlanRequest
from app.services import generate_ai_response
from app.utils import build_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Employee Skills Assistant")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/employees")
def list_employees():
    try:
        return {"employees": load_employees()}
    except (OSError, ValueError):
        logger.exception("Could not load employee data")
        raise HTTPException(
            status_code=500,
            detail="Could not load employee data"
        )


@app.get("/employees/{employee_id}")
def employee_details(employee_id: int):
    employee = get_employee(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


@app.get("/employees/search")
def find_employees(skill: str):
    if not skill.strip():
        raise HTTPException(
            status_code=422,
            detail="Skill cannot be blank"
        )

    matches = search_employees(skill)

    return {
        "count": len(matches),
        "employees": matches
    }


@app.post("/generate")
def generate(request: GenerateRequest):
    try:
        logger.info("AI generation request received")

        result = generate_ai_response(
            request.prompt,
            request.temperature
        )

        logger.info("AI generation request completed")

        return {
            "prompt": request.prompt,
            **result
        }

    except APITimeoutError as exc:
        logger.exception("Gemini request timed out")
        raise HTTPException(
            status_code=504,
            detail="AI service timed out. Please try again."
        ) from exc

    except APIError as exc:
        logger.exception("Gemini API request failed")

        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Please try again."
        ) from exc

    except RuntimeError as exc:
        logger.exception("AI service configuration or response error")
        raise HTTPException(
            status_code=500,
            detail="AI service could not complete the request"
        ) from exc


@app.post("/employees/{employee_id}/learning-plan")
def create_learning_plan(
    employee_id: int,
    request: LearningPlanRequest
):
    employee = get_employee(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    prompt = build_prompt(
        employee_name=employee["name"],
        role=employee["role"],
        skills=employee["skills"],
        instructions=(
            f"Experience level: {request.experience_level}. "
            f"Learning goals: {', '.join(request.goals)}. "
            "Give a practical plan with weekly milestones."
        )
    )

    try:
        result = generate_ai_response(prompt)

        return {
            "employee": employee["name"],
            "goals": request.goals,
            **result
        }

    except APITimeoutError as exc:
        logger.exception("Learning plan request timed out")
        raise HTTPException(
            status_code=504,
            detail="AI service timed out. Please try again."
        ) from exc

    except APIError as exc:
        logger.exception("Learning plan generation failed")
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable"
        ) from exc

    except RuntimeError as exc:
        logger.exception("Learning plan configuration or response error")
        raise HTTPException(
            status_code=500,
            detail="Could not generate the learning plan"
        ) from exc