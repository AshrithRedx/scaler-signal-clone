"use client";

import { useState } from "react";

interface Props {
    onSend: (message: string) => void;
}

export default function MessageInput({
    onSend,
}: Props) {

    const [text, setText] = useState("");

    const send = () => {

        if (!text.trim()) return;

        onSend(text);

        setText("");

    };

    return (

        <div className="flex gap-3 p-4 border-t border-gray-700 bg-[#202c33]">

            <input
                className="flex-1 rounded-lg bg-[#2a3942] text-white px-4 py-3 outline-none border border-transparent focus:border-[#00a884] transition-colors"
                placeholder="Type a message..."
                value={text}
                onChange={(e)=>setText(e.target.value)}
                onKeyDown={(e)=>{

                    if(e.key==="Enter")
                        send();

                }}
            />

            <button
                onClick={send}
                className="bg-[#00a884] hover:bg-[#01916f] transition-colors px-6 rounded-lg text-white font-semibold"
            >
                Send
            </button>

        </div>

    );

}