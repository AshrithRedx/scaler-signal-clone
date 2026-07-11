"use client";

import { useEffect, useRef } from "react";

import { Message } from "@/types/message";
import MessageInput from "./MessageInput";

interface Props {
    messages: Message[];
    conversationName: string;
    currentUserId: string;
    onSend: (message: string) => void;
}

export default function ChatWindow({
    messages,
    conversationName,
    currentUserId,
    onSend,
}: Props) {

    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
        });

    }, [messages]);

    return (

        <div className="flex flex-col flex-1 h-screen bg-[#111b21]">

            {/* Header */}
            <div className="h-16 border-b border-[#2a3942] flex items-center px-6 bg-[#202c33]">

                <div className="w-10 h-10 rounded-full bg-[#00a884] flex items-center justify-center text-white font-bold text-lg mr-4">
                    {conversationName.charAt(0).toUpperCase()}
                </div>

                <div>
                    <div className="text-white text-lg font-semibold">
                        {conversationName}
                    </div>

                    <div className="text-sm text-[#00a884]">
                        ● Online
                    </div>
                </div>

            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-3">

                {messages.map((message) => {

                    const isMine =
                        message.sender_id === currentUserId;

                    return (

                        <div
                            key={message.id}
                            className={`flex ${
                                isMine
                                    ? "justify-end"
                                    : "justify-start"
                            }`}
                        >

                            <div
                                className={`max-w-[70%] rounded-2xl px-4 py-3 shadow-md break-words ${
                                    isMine
                                        ? "bg-[#005c4b] text-white"
                                        : "bg-[#202c33] text-white"
                                }`}
                            >

                                <div>
                                    {message.content}
                                </div>

                                <div className="text-[10px] text-gray-300 mt-1 text-right">
                                    {new Date(
                                        message.created_at
                                    ).toLocaleTimeString([], {
                                        hour: "2-digit",
                                        minute: "2-digit",
                                    })}
                                </div>

                            </div>

                        </div>

                    );

                })}

                <div ref={bottomRef} />

            </div>

            <MessageInput
                onSend={onSend}
            />

        </div>

    );

}