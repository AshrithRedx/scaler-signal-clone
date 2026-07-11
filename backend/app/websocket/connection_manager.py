from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(
        self,
        conversation_id: str,
        websocket: WebSocket,
    ):
        await websocket.accept()

        self.active_connections[conversation_id].append(websocket)

    def disconnect(
        self,
        conversation_id: str,
        websocket: WebSocket,
    ):
        if conversation_id in self.active_connections:

            if websocket in self.active_connections[conversation_id]:
                self.active_connections[conversation_id].remove(websocket)

            if not self.active_connections[conversation_id]:
                del self.active_connections[conversation_id]

    async def broadcast(
        self,
        conversation_id: str,
        message: dict,
    ):

        if conversation_id not in self.active_connections:
            return

        dead_connections = []

        for connection in self.active_connections[conversation_id]:

            try:
                await connection.send_json(message)

            except Exception:
                dead_connections.append(connection)

        for connection in dead_connections:
            self.disconnect(conversation_id, connection)


manager = ConnectionManager()