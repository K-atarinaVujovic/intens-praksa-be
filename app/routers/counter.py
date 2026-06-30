from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.counter_service import increase_counter, restart_counter, get_counter

router = APIRouter(prefix="/counter", tags=["counter"])

active_connections: list[WebSocket] = []

async def broadcast(count: int):
    for connection in active_connections:
        await connection.send_json({"count": count})

@router.get("/")
def read_counter():
    return {"count": get_counter()}

@router.post("/increase")
async def increase():
    count = increase_counter()
    await broadcast(count)
    return {"count": count}

@router.post("/restart")
async def restart():
    count = restart_counter()
    await broadcast(count)
    return {"count": count}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        # send current count immediately on connect
        await websocket.send_json({"count": get_counter()})
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)