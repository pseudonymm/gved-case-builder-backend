from fastapi import HTTPException
from litellm import acompletion

async def fill_in_service(context: str, type: str):
    prompts = {
        "background": (
            "You are building an Asian Parliamentary debate case.\n"
            "Task: produce the BACKGROUND section.\n\n"
            "What BACKGROUND should contain: a concise setup that gives judges and teammates the historical, political, social, or economic context needed to understand the motion and the arguments that follow.\n"
            "Include: timeline of key events (if relevant), major actors, root causes, and any past policies or decisions that led to the current dispute. Keep it focused and directly relevant to the motion.\n\n"
            "Context: {context}"
        ),
        "status_quo": (
            "You are building an Asian Parliamentary debate case.\n"
            "Task: produce the STATUS QUO section.\n\n"
            "What STATUS QUO should contain: a clear description of the present state of affairs as it relates to the motion — what currently exists, how institutions or actors behave today, and what problems or advantages this state produces.\n"
            "Include: who benefits, who loses, current policies or norms, recent data or facts that demonstrate the current situation, and why change (or preservation) matters.\n\n"
            "Context: {context}"
        ),
        "definitions": (
            "You are building an Asian Parliamentary debate case.\n"
            "Task: produce the DEFINITIONS section.\n\n"
            "What DEFINITIONS should contain: precise, debate-ready definitions of key terms in the motion and in the case so judges and opponents share the same meanings. Aim for clarity, arguability, and relevance to the case.\n"
            "Include: a primary definition for the motion (if applicable), scope notes, any necessary clarifications to avoid unfair interpretations, and brief justifications for chosen definitions.\n\n"
            "Context: {context}"
        )
            ,
            "why_support": (
                "You are building an Asian Parliamentary debate case.\n"
                "Task: produce a concise 'WHY WE SUPPORT THIS MOTION' section.\n\n"
                "What this section should contain: clear, debate-ready reasons and advantages for supporting the motion.\n"
                "Include: the strongest impacts, solvency arguments, stakeholders who benefit, and strategic arguments teams can deploy. Keep it focused and actionable.\n\n"
                "Context: {context}"
            ),
            # oppose section removed — always generate support
    }
    
    if type not in prompts:
        raise HTTPException(status_code=400, detail="Invalid type. Must be one of: background, status_quo, definitions, why_support")
    
    prompt = prompts[type].format(context=context)
    
    response = await acompletion(
        model="cerebras/gpt-oss-120b",
        messages=[{
            "role": "system",
            "content": (
                "You are an assistant specialized in building Asian Parliamentary debate cases. "
                "For each requested section (BACKGROUND, STATUS QUO, or DEFINITIONS), produce a focused, debate-ready markdown section following the guidance for that section. "
                "Be concise, precise, and include only material directly useful to a debating team or adjudicator. Use headings, bullet points, and short paragraphs as appropriate. "
                "Do not add unrelated analysis or alternative sections."
            )
        }, {
            "role": "user",
            "content": prompt
        }],
        stream=True
    )
    
    async for chunk in response:  # type: ignore
        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content