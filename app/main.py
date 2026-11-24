# L10: required CORS setup; rate limiting is optional and ungraded.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import items

app = FastAPI(title="Security Basics API")

# TODO: Add CORS for http://localhost:8501, methods GET/POST, explicit headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins= [
        "http://localhost:8501", 
    ],
    allow_credentials=True, #allows to include sensitive user credentials ex.authentication headers
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# TODO: Import items and include its router with prefix="/items", tags=["items"].
app.include_router(items.router, prefix="/items", tags=["items"])