"use client";

import { Conversation } from "@/types/conversation";

interface Props {
    conversations: Conversation[];
    selectedConversation: Conversation | null;
    onSelect: (conversation: Conversation) => void;
    currentUserName: string;
}

export default function ConversationSidebar({
    conversations,
    selectedConversation,
    onSelect,
    currentUserName,
}: Props) {

    return (

        <div className="w-80 h-screen bg-[#202c33] border-r border-[#2a3942] flex flex-col">

            {/* Header */}
            <div className="h-16 flex items-center px-6 border-b border-[#2a3942]">

                <div className="w-10 h-10 rounded-full bg-[#00a884] flex items-center justify-center text-white font-bold text-lg">
                    {currentUserName.charAt(0).toUpperCase()}
                </div>

                <div className="ml-3">

                    <div className="text-white font-semibold">
                        Signal For Scaler
                    </div>

                    <div className="text-xs text-gray-400">
                        {currentUserName}
                    </div>

                </div>

            </div>

            {/* Conversations */}
            <div className="flex-1 overflow-y-auto">

                {conversations.map((conversation) => {

                    const selected =
                        selectedConversation?.id === conversation.id;

                    const title =
                        conversation.name ?? "Direct Message";

                    const avatar =
                        title.charAt(0).toUpperCase();

                    return (

                        <div
                            key={conversation.id}
                            onClick={() => onSelect(conversation)}
                            className={`flex items-center px-4 py-4 cursor-pointer transition-all duration-150 border-b border-[#2a3942]
                                ${
                                    selected
                                        ? "bg-[#2a3942]"
                                        : "hover:bg-[#2a3942]"
                                }`}
                        >

                            {/* Avatar */}

                            <div className="w-12 h-12 rounded-full bg-[#00a884] flex items-center justify-center text-white font-bold text-lg">

                                {avatar}

                            </div>

                            {/* Conversation Info */}

                            <div className="ml-4 flex-1 overflow-hidden">

                                <div className="text-white font-medium truncate">

                                    {title}

                                </div>

                                <div className="text-sm text-gray-400 truncate">

                                    Tap to open conversation

                                </div>

                            </div>

                        </div>

                    );

                })}

            </div>

        </div>

    );

}