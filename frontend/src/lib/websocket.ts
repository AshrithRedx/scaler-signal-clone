import { Message } from "@/types/message";
export class ChatWebSocket {

    private socket: WebSocket | null = null;

    connect(
    conversationId: string,
    onMessage: (data: Message) => void
) {
    const wsBase =
        process.env.NEXT_PUBLIC_WS_URL ??
        "ws://127.0.0.1:8000";

    this.socket = new WebSocket(
        `${wsBase}/ws/${conversationId}`
    );

    this.socket.onopen = () => {
        console.log("✅ WebSocket Connected");
    };

    this.socket.onmessage = (event) => {
        const message: Message = JSON.parse(event.data);
        onMessage(message);
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