from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import counter
import os
from dotenv import load_dotenv

load_dotenv()
ALLOWED_ORIGIN = os.getenv("FRONTEND_URL", "http://localhost:3000")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["*"],
)

app.include_router(counter.router)