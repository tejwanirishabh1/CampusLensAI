
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="CampusLens AI",
    description="A source-grounded academic document assistant",
    version="0.1.0"
)


class HealthResponse(BaseModel):
    status: str
    project: str


@app.get("/", response_model=HealthResponse)
def health_check():
    """Check whether the CampusLens AI API is running."""
    return {
        "status": "running",
        "project": "CampusLens AI"
    }
