from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.models import init_db

# FIXED: Separated 'async def' keywords correctly
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up server triggers...")
    try:
        init_db()
    except Exception as e:
        print(f"DATABASE INITIALIZATION CRASH: {e}")
    yield
    print("Shutting down server triggers...")

app = FastAPI(
    title="Cloud Cost & Resource Sentinel SaaS API",
    description="Automated multi-tenant resource optimization engine",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

# FIXED: Separated 'async def' keywords here too
@app.get("/")
async def read_root():
    return {
        "status": "online",
        "service": "Cloud Cost & Resource Sentinel Backend",
        "version": "1.0.0"
    }

