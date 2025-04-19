# FastAPI application for super intelligent admin system
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from .routers import chatbot, backend, frontend, infra, monitoring, ai, knowledge
from .utils.auth import verify_jwt
from .utils.logging import setup_logging
from .utils.metrics import setup_metrics

app = FastAPI(
    title="SuperIntelligentAdminSystem",
    description="Admin system for managing chat application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
setup_logging()

# Metrics middleware
setup_metrics()

# OAuth2 for Keycloak JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Include routers
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(backend.router, prefix="/backend", tags=["Backend"])
app.include_router(frontend.router, prefix="/frontend", tags=["Frontend"])
app.include_router(infra.router, prefix="/infra", tags=["Infrastructure"])
app.include_router(monitoring.router, prefix="/monitoring", tags=["Monitoring"])
app.include_router(ai.router, prefix="/ai", tags=["AI"])
app.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge"])

@app.get("/")
async def root():
    return {"message": "Welcome to SuperIntelligentAdminSystem"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"Internal Server Error: {str(exc)}"}
    )