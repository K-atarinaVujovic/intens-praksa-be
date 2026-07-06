from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.routers.counter import router as counter_router, pg_listener
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
ALLOWED_ORIGIN = os.getenv("FRONTEND_URL", "http://localhost:3000")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    listener_task = asyncio.create_task(pg_listener())
    yield
    # shutdown
    listener_task.cancel()
    try:
        await listener_task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

app.include_router(counter_router)

# comment!