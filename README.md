# 🤖 STAN Bot

A conversational AI backend built with **Python + FastAPI**, featuring:
- 🔌 Pluggable LLM providers (Dummy, OpenAI, HuggingFace)
- 🧠 Stateful memory with Redis (conversation recall)
- ⚡ REST API endpoints for health, chat, history, and reset
- 📦 Ready for integration with any frontend (web, mobile, chat UI)

---

## 🚀 Features
- **Phase 1**: FastAPI backend with health + chat endpoints
- **Phase 2**: Redis-based memory store (conversation history per user)
- **Phase 3 (Upcoming)**: Tone adaptation (empathetic / playful modes)
- **Phase 4 (Upcoming)**: Real LLM providers (OpenAI, HuggingFace, Mistral)

---

## 📂 Project Structure
```
stan-bot/
│── app/
│   ├── main.py          # FastAPI entrypoint
│   ├── config.py        # Environment + provider configs
│   ├── llm_providers.py # Dummy/OpenAI/HF provider integrations
│   ├── memory.py        # Redis-based memory store
│   └── schemas.py       # Pydantic models (request/response)
│
├── .env.example         # Example environment config
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## ⚙️ Installation

### 1. Clone repo
```bash
git clone https://github.com/your-username/stan-bot.git
cd stan-bot
```

### 2. Create venv
```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Create a `.env` file:

```env
# LLM Provider (dummy | openai | hf)
PROVIDER=dummy

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# OpenAI (if PROVIDER=openai)
OPENAI_API_KEY=sk-xxxx
OPENAI_MODEL=gpt-4o-mini

# HuggingFace (if PROVIDER=hf)
HF_API_KEY=hf_xxx
HF_MODEL=HuggingFaceH4/zephyr-7b-beta
```

---

## ▶️ Running the Server
```bash
python -m uvicorn app.main:app --reload --port 8000
```

- API available at → http://127.0.0.1:8000  
- Swagger docs → http://127.0.0.1:8000/docs  

---

## 🔌 API Endpoints

### 1. Health Check
```http
GET /health
```
**Response**
```json
{"status": "ok", "provider": "dummy"}
```

### 2. Chat
```http
POST /chat
```
**Request**
```json
{
  "user_id": "u1",
  "message": "Hello, my favorite color is blue"
}
```

**Response (dummy provider)**
```json
{
  "reply": "(stub) You said: Hello, my favorite color is blue",
  "model": "dummy-echo",
  "provider": "dummy",
  "tokens_estimate": null
}
```

### 3. Get History
```http
GET /chat/{user_id}/history?limit=5
```

### 4. Clear History
```http
DELETE /chat/{user_id}
```

---

## 🛠 Tech Stack
- **Backend**: FastAPI, Pydantic
- **LLM Providers**: OpenAI, HuggingFace, Dummy Echo
- **Memory**: Redis
- **Server**: Uvicorn
- **Config**: python-dotenv

---

## 📌 Roadmap
- ✅ Phase 1: Backend setup
- ✅ Phase 2: Redis memory
- 🔄 Phase 3: Emotional tone adaptation
- 🔄 Phase 4: Full LLM integration (OpenAI/HF/Mistral)
- 🔄 Phase 5: Deployment (Docker, Cloud Run, etc.)

---

## 👨‍💻 Contributing
1. Fork repo  
2. Create feature branch  
3. Submit PR 🚀  

---

## 📜 License
MIT License © 2025 [Your Name]
