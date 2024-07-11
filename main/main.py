from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import uvicorn
from LLM import llm

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    top_p: float = 0.8
    top_k: int = 2
    temp: float = 0.9

class ChatRequest(BaseModel):
    user_id: int
    chat_id: int = None
    prompt: str
    top_p: float = 0.8
    top_k: int = 2
    temp: float = 0.9

class ExtendedChatRequest(BaseModel):
    user_id: int
    chat_id: int = None
    prompt: str

@app.post("/get-prompt-response")
async def get_prompt_response(request: PromptRequest):
    try:
        response = llm.getPromptResponse(request.prompt, request.top_p, request.top_k, request.temp)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get-chat-response")
async def get_chat_response(request: ChatRequest):
    try:
        response = llm.chat(request.user_id, request.chat_id, request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get-extended-chat-response")
async def get_extended_chat_response(request: ExtendedChatRequest):
    try:
        response = llm.extendedChat(request.user_id, request.chat_id, request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
