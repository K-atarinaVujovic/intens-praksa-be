from fastapi import APIRouter
from app.services.counter_service import increase_counter, restart_counter, get_counter

router = APIRouter(prefix="/counter", tags=["counter"])

@router.get("/")
def read_counter():
    return {"count": get_counter()}

@router.post("/increase")
def increase():
    return {"count": increase_counter()}

@router.post("/restart")
def restart():
    return {"count": restart_counter()}