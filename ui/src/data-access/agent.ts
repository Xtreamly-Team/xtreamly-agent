import {subscribeTo} from "../utils/firestore";
import {useQuery} from "@tanstack/react-query";
import {get} from "../services/api.ts";

function subscribes(chatId: string, onUpdate: (messages: any[]) => void) {
    console.log(`chats/${chatId}/messages`);
    return subscribeTo(`chats/${chatId}/messages`, (data    ) => {
        const d = Object.values(data).sort((a, b) => a.time - b.time);
        onUpdate(d)
    })
}

export function useAgent() {
    const {data: chatId, isLoading} = useQuery({
        queryKey: ["init-chat"],
        queryFn: async () => {
            const res = await get('init_chat')
            const body = await res.json()
            const chatId = body.chatId
            get("init_agent", {chatId})
            return chatId
        },
        staleTime: 60*60000, // 1 minute
    })

    return {
        chatId,
        loading: isLoading,
        subscribe: subscribes
    }
}
