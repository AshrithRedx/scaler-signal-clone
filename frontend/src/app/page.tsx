"use client";

import { useEffect, useRef, useState } from "react";

import ConversationSidebar from "@/components/sidebar/ConversationSidebar";
import ChatWindow from "@/components/chat/ChatWindow";

import { ChatAPI } from "@/lib/chatApi";
import { ChatWebSocket } from "@/lib/websocket";

import { Conversation } from "@/types/conversation";
import { Message } from "@/types/message";

type DemoUser = {
    id: string;
    name: string;
};

const USERS = {
    kaelen: {
        id: "52445db9-3755-4dae-9d1d-899ffcba9b89",
        name: "Kaelen Frost",
    },

    lyra: {
        id: "4477b8f4-890f-4bee-918b-f50700b5d686",
        name: "Lyra Quinn",
    },
} as const;

export default function Home() {

    const socket = useRef<ChatWebSocket | null>(null);

    // Read user from URL
    const [currentUser, setCurrentUser] =
    useState<DemoUser>(USERS.kaelen);;

    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [selectedConversation, setSelectedConversation] =
        useState<Conversation | null>(null);

    const [messages, setMessages] = useState<Message[]>([]);

    // Read ?user=...
    useEffect(() => {

        const params = new URLSearchParams(window.location.search);

        const user =
            params.get("user")?.toLowerCase();

        if (user === "lyra") {

            setCurrentUser(USERS.lyra);

        } else {

            setCurrentUser(USERS.kaelen);

        }

    }, []);

    const USER_ID = currentUser.id;

    // Load conversations whenever user changes
    useEffect(() => {

        ChatAPI.getConversations(USER_ID)
            .then((data) => {

                setConversations(data);

                setSelectedConversation(null);

                setMessages([]);

            })
            .catch(console.error);

    }, [USER_ID]);

    // Load messages
    useEffect(() => {

        if (!selectedConversation) return;

        ChatAPI.getMessages(selectedConversation.id)
            .then((data) => {

                setMessages(data);

            })
            .catch(console.error);

    }, [selectedConversation]);

    // WebSocket
    useEffect(() => {

        if (!selectedConversation) return;

        socket.current?.disconnect();

        socket.current = new ChatWebSocket();

        socket.current.connect(

            selectedConversation.id,

            (message: Message) => {

                setMessages((prev) => [...prev, message]);

            }

        );

        return () => {

            socket.current?.disconnect();

        };

    }, [selectedConversation, USER_ID]);

    const sendMessage = (text: string) => {

        socket.current?.send(
            USER_ID,
            text,
        );

    };

    return (

        <div className="flex h-screen">

            <ConversationSidebar
                conversations={conversations}
                selectedConversation={selectedConversation}
                onSelect={setSelectedConversation}
                currentUserName={currentUser.name}
            />

            {selectedConversation ? (

                <ChatWindow
                    messages={messages}
                    conversationName={
                        selectedConversation.name ??
                        "Direct Message"
                    }
                    currentUserId={USER_ID}
                    onSend={sendMessage}
                />

            ) : (

                <div className="flex-1 flex items-center justify-center bg-[#111b21]">

                    <div className="text-center">

                        <div className="text-6xl mb-6">
                            💬
                        </div>

                        <h1 className="text-3xl font-semibold text-white">
                            Signal Clone
                        </h1>

                        <p className="text-gray-400 mt-4">
                            Select a conversation to start chatting.
                        </p>

                    </div>

                </div>

            )}

        </div>

    );

}