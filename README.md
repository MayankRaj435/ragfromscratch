## RAG Guardrails

The FastAPI app now serves a browser console at `/`. Start it from the repository root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` to:

- ask questions against the guarded RAG pipeline;
- inspect retrieved source chunks and similarity scores;
- see validation and service errors clearly; and
- run frontend smoke checks against the app's root, health, and validation endpoints.

The frontend is served from `app/static/` and uses the existing `POST /ask` response contract.