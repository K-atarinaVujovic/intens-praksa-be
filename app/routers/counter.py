from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.counter_service import increase_counter, restart_counter, get_counter
import asyncpg
import asyncio
import os

router = APIRouter(prefix="/counter", tags=["counter"])

active_connections: list[WebSocket] = []

async def broadcast(count: int):
    for connection in active_connections:
        await connection.send_json({"count": count})

async def pg_listener():
    conn = await asyncpg.connect(os.environ["DATABASE_URL"])
    async def on_notify(connection, pid, channel, payload):
        await broadcast(int(payload))
    await conn.add_listener("counter_updates", on_notify)
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await conn.close()

@router.get("/")
def read_counter():
    return {"count": get_counter()}

@router.post("/increase")
async def increase():
    count = increase_counter()
    return {"count": count}

@router.post("/restart")
async def restart():
    count = restart_counter()
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