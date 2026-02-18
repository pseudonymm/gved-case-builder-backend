from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import fill_in_service

router = APIRouter()

class FillInRequest(BaseModel):
    context: str
    type: str

# TODO: make this http streaming response so that the frontend can show suggestions as they come in instead of waiting for the entire response to be generated
@router.post("/fill-in", response_model=list[str])
async def fill_in(req: FillInRequest):
    return await fill_in_service(req.context, req.type)