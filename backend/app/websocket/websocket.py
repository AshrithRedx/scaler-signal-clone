from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.db.database import SessionLocal
from app.services.message_service import send_message
from app.websocket.connection_manager import manager

router = APIRouter()


@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    conversation_id: str,
):
    db = SessionLocal()

    await manager.connect(conversation_id, websocket)

    try:
        while True:

            data = await websocket.receive_json()

            if "sender_id" not in data or "content" not in data:
                await websocket.send_json({
                    "error": "Invalid payload"
                })
                continue

            message = send_message(
                db=db,
                conversation_id=conversation_id,
                sender_id=data["sender_id"],
                content=data["content"],
            )

            await manager.broadcast(
                conversation_id,
                {
                    "id": message.id,
                    "conversation_id": message.conversation_id,
                    "sender_id": message.sender_id,
                    "content": message.content,
                    "status": message.status,
                    "created_at": message.created_at.isoformat(),
                },
            )

    except WebSocketDisconnect:
        manager.disconnect(
            conversation_id,
            websocket,
        )

    finally:
        db.close()