import asyncio
import os
from typing import Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from pydantic import BaseModel

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

_raw_origins = os.environ.get("ALLOWED_ORIGINS", "*")
ALLOWED_ORIGINS = ["*"] if _raw_origins.strip() == "*" else [o.strip() for o in _raw_origins.split(",")]

app = FastAPI(title="AI Code Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_client = None


def get_client() -> genai.Client:
    global _client
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not set. Add it to a .env file or your host's environment variables.",
        )
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


class CodeRequest(BaseModel):
    prompt: str
    language: str


class CodeOptimizeRequest(BaseModel):
    code: str


class CodeExplainRequest(BaseModel):
    code: str


class CodeDebugRequest(BaseModel):
    code: str


class CodeTestRequest(BaseModel):
    code: str


class ProjectSummaryRequest(BaseModel):
    activities: List[str]


async def get_ai_response(prompt: str) -> str:
    try:
        client = get_client()
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.models.generate_content(model=GEMINI_MODEL, contents=prompt),
        )
        return response.text
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating response: {e}")
        raise HTTPException(status_code=502, detail=f"Error generating response: {e}")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Code Assistant API!", "model": GEMINI_MODEL}


@app.get("/health")
async def health_check():
    return {"status": "ok", "gemini_configured": bool(GEMINI_API_KEY)}


@app.post("/generate_code/")
async def generate_code(request: CodeRequest):
    prompt = f"Write {request.language} code for the following prompt: {request.prompt}"
    return {"code": await get_ai_response(prompt)}


@app.post("/optimize_code/")
async def optimize_code(request: CodeOptimizeRequest):
    prompt = f"Optimize the following code for readability and performance:\n{request.code}"
    return {"optimized_code": await get_ai_response(prompt)}


@app.post("/explain_code/")
async def explain_code(request: CodeExplainRequest):
    prompt = f"Explain the following code in simple terms:\n{request.code}"
    return {"explanation": await get_ai_response(prompt)}


@app.post("/debug_code/")
async def debug_code(request: CodeDebugRequest):
    prompt = f"""Analyze the following code for issues and suggest improvements:

{request.code}

Please provide:
1. A list of identified issues
2. Suggestions for fixing each issue
3. An updated version of the code with key changes highlighted

Format your response exactly as follows:
ISSUES:
[List of issues]

SUGGESTIONS:
[Suggestions for each issue]

UPDATED CODE:
[Updated code with key changes highlighted]
"""
    return {"result": await get_ai_response(prompt)}


@app.post("/generate_unit_tests/")
async def generate_unit_tests(request: CodeTestRequest):
    prompt = f"Write unit tests for the following code:\n{request.code}"
    return {"unit_tests": await get_ai_response(prompt)}


@app.post("/project_summary/")
async def project_summary(request: ProjectSummaryRequest):
    activities_summary = "\n".join(request.activities)
    prompt = f"Provide a project summary for the following activities:\n{activities_summary}"
    return {"summary": await get_ai_response(prompt)}


active_connections: Dict[str, List[WebSocket]] = {}


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    active_connections.setdefault(session_id, []).append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await broadcast_message(session_id, data)
    except WebSocketDisconnect:
        active_connections[session_id].remove(websocket)
        if not active_connections[session_id]:
            del active_connections[session_id]
    except Exception as e:
        print(f"Error with WebSocket communication: {e}")
        await websocket.close()


async def broadcast_message(session_id: str, message: str):
    for connection in active_connections.get(session_id, []):
        try:
            await connection.send_text(message)
        except Exception as e:
            print(f"Error sending message: {e}")


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)