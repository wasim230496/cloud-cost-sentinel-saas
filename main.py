from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.models import init_db

app = FastAPI(
    title="Cloud Cost & Resource Sentinel SaaS API",
    description="Automated multi-tenant resource optimization engine",
    version="1.0.0"
)

# Run table generation on startup trigger
@app.on_event("startup")
def startup_event():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

@app.get("/")
async def read_root():
    return {
        "status": "online",
        "service": "Cloud Cost & Resource Sentinel Backend",
        "version": "1.0.0"
    }
