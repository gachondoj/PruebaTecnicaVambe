from fastapi import FastAPI, HTTPException
from crud import get_assistant, create_assistant, update_assistant
from pydantic import BaseModel

app = FastAPI()

class AssistantCreate(BaseModel):
    name: str
    instructions: str

class AssistantUpdate(BaseModel):
    instructions: str

@app.get("/assistants/{assistant_id}")
def read_assistant(assistant_id: str):
    assistant = get_assistant(assistant_id)
    if not assistant:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return assistant

@app.post("/assistants/")
def create_assistant_endpoint(assistant: AssistantCreate):
    return create_assistant(assistant.name, assistant.instructions)

@app.put("/assistants/{assistant_id}")
def update_assistant_endpoint(assistant_id: str, update_data: AssistantUpdate):
    return update_assistant(assistant_id, update_data.instructions)