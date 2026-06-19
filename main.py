from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize the core SaaS App engine instances
app = FastAPI(
    title="Cloud Cost & Resource Sentinel SaaS API",
    description="Automated multi-tenant resource optimization engine",
    version="1.0.0"
)

# Enable CORS parameters so frontends can securely bind later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

@app.get("/")
async def read_root():
    """
    Base landing diagnostic endpoint.
    """
    return {
        "status": "online",
        "service": "Cloud Cost & Resource Sentinel Backend",
        "version": "1.0.0"
    }

@app.get("/api/v1/health")
async def health_check():
    """
    SaaS System health matrix checker.
    """
    return {
        "status": "healthy",
        "database": "disconnected (pending configuration)",
        "redis_queue": "disconnected (pending configuration)"
    }
