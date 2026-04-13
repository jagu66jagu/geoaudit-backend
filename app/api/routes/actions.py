from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
from app.services.action_service import run_action

router = APIRouter()

class ActionRequest(BaseModel):
    action_type: str
    finding_id: str
    context_data: dict[str, Any]

@router.post("/actions/generate")
async def generate_action(request: ActionRequest):
    try:
        result = await run_action(
            action_type=request.action_type,
            finding_id=request.finding_id,
            context_data=request.context_data,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
