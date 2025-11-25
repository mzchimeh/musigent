
from fastapi import FastAPI
from pydantic import BaseModel
from musigent.runner import MusigentRunner

app = FastAPI(title="Musigent - Starter API")
runner = MusigentRunner()

class GenerateRequest(BaseModel):
    mode: str  # jingle | bgm | persona
    prompt: str
    duration_sec: int = 30

@app.post("/generate")
async def generate(req: GenerateRequest):
    result = runner.handle_request(req.mode, req.prompt, req.duration_sec)
    return result
