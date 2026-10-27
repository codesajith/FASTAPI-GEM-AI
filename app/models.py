from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)
    temperature: float = Field(default=1.0, ge=0, le=2)


class LearningPlanRequest(BaseModel):
    goals: list[str] = Field(min_length=1, max_length=5)
    experience_level: str = Field(
        min_length=2,
        max_length=30
    )