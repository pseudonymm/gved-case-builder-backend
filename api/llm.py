from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.llm import fill_in_service

router = APIRouter(
    prefix="/llm",
    tags=["LLM"]
)

class FillInRequest(BaseModel):
    context: str
    type: str

@router.post("/fill-in")
async def fill_in(req: FillInRequest):
    return StreamingResponse(
        fill_in_service(req.context, req.type),
        media_type="text/plain"
    )