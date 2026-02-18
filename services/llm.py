from fastapi import HTTPException
from litellm import acompletion

async def fill_in_service(context: str, type: str) -> str:
    prompt = ""
    
    match type:
        case "background":
            # TODO: define prompt for each
        case "status_quo":
            # TODO: define prompt for each
        case "definitions":
            # TODO: define prompt for each
        case _:
            raise HTTPException(status_code=400, detail="Invalid type. Must be one of: background, status_quo, definitions")
        
    # TODO: call the api with the prompt and appropriate system instructions, return the suggestions (streaming response so that the frontend can show suggestions as they come in instead of waiting for the entire response to be generated)