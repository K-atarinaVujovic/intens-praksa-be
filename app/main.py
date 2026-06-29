from fastapi import FastAPI
from app.routers import counter

app = FastAPI()

app.include_router(counter.router)