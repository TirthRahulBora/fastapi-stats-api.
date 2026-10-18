import os
import time
import uuid
from typing import Annotated

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

EMAIL = os.getenv("APP_EMAIL", "24f3002455@ds.study.iitm.ac.in")
ALLOWED_ORIGIN = "https://dash-rzuh37.example.com"

app = FastAPI(title="Descriptive Statistics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def request_metadata(request: Request, call_next):
    started = time.perf_counter()
    request_id = str(uuid.uuid4())
    try:
        response = await call_next(request)
    except Exception:
        response = JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
    elapsed = max(0.0, time.perf_counter() - started)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    return response

@app.get("/stats")
async def stats(values: Annotated[str, Query(description="Comma-separated integers")]):
    try:
        parts = [part.strip() for part in values.split(",")]
        if not parts or any(part == "" for part in parts):
            raise ValueError
        numbers = [int(part) for part in parts]
    except ValueError:
        return JSONResponse(status_code=400, content={"detail": "values must be comma-separated integers"})

    total = sum(numbers)
    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / len(numbers),
    }

@app.get("/")
async def root():
    return {"service": "stats-api", "health": "ok"}
