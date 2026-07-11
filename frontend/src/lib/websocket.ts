export class ChatWebSocket {

    private socket: WebSocket | null = null;

    connect(
        conversationId: string,
        onMessage: (data: any) => void
    ) {

        this.socket = new WebSocket(
            `ws://127.0.0.1:8000/ws/${conversationId}`
        );

        this.socket.onopen = () => {
            console.log("✅ WebSocket Connected");
        };

        this.socket.onmessage = (event) => {
            onMessage(JSON.parse(event.data));
        };

        this.socket.onclose = () => {
            console.log("❌ WebSocket Disconnected");
        };

        this.socket.onerror = (error) => {
            console.error("WebSocket Error:", error);
        };

    }

    send(senderId: string, content: string) {

        if (!this.socket) return;

        if (this.socket.readyState !== WebSocket.OPEN)
            return;

        this.socket.send(
            JSON.stringify({
                sender_id: senderId,
                content,
            })
        );

    }

    disconnect() {

        this.socket?.close();

    }

}