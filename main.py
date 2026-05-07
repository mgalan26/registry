from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

from routers import modules, errors

load_dotenv()

REGISTRY_API_KEY = os.getenv("REGISTRY_API_KEY", "")

app = FastAPI(title="Now Ecosystem Registry", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.url.path in ("/", "/health", "/docs", "/openapi.json", "/redoc"):
        return await call_next(request)

    key = request.headers.get("X-Registry-Key")
    if not key or key != REGISTRY_API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or missing X-Registry-Key"},
        )

    return await call_next(request)


app.include_router(modules.router, prefix="/modules", tags=["modules"])
app.include_router(errors.router, prefix="/errors", tags=["errors"])


@app.get("/health")
def health():
    return {"status": "ok"}
