from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import ChatRequest, ChatResponse
from .llm_providers import make_client
from .config import settings
from .memory import MemoryStore

app = FastAPI(title="STAN Bot", version="0.2.0")

# Allow CORS (so you can connect later from a frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = make_client()
memory = MemoryStore()

@app.get("/health")
def health():
    return {"status": "ok", "provider": settings.PROVIDER}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        # Save user input to memory
        memory.save_message(req.user_id, "user", req.message)

        # Get recent history (last 5 exchanges)
        history = memory.get_history(req.user_id, limit=5)
        context_text = "\n".join([f"{h['role']}: {h['message']}" for h in history])

        # Generate response using LLM + history context
        reply, model = await llm.generate(req.user_id, context_text)

        # Save assistant reply to memory
        memory.save_message(req.user_id, "assistant", reply)

        return ChatResponse(
            reply=reply,
            model=model,
            provider=settings.PROVIDER,
            tokens_estimate=None
        )

    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
