import {AGENTS, ChatPage} from "./Chat";
import {AspectRatio, Box, Stack, Text, Title, Tooltip} from "@mantine/core";
import {useEffect, useState} from "react";
import {useAgent} from "../data-access/agent";
import Markdown from "react-markdown";

function Thought({
    text,
    agent
}: {
    text: string,
    agent: string
}) {
    const a = AGENTS[agent]
    return (
        <Tooltip
            arrowOffset={120}
            arrowSize={10}
            multiline
            label={
                <Text
                    size={a.size || "10px"}
                    mah={200}
                    style={{
                        overflow: "hidden"
                    }}
                >
                    <Markdown>{text?.trim()}</Markdown>
                </Text>
            }
            withArrow={a.noArrow ? false : true}
            opened
            position="top-start"
            mah={300}
            w={250}
            bg="rgba(0, 0, 0, 0.8)"
            c="white"
        >
            <Box
                style={{
                    position: "absolute",
                    top: a.y || "64.5%",
                    left: a.x
                }}
            >
            </Box>
        </Tooltip>
    )
}

function getLatestMessages(ms: any[]): any[] {
    const latestItemsMap = new Map<string, any>();

    for (const item of ms) {
        const existingItem = latestItemsMap.get(item.agent);

        if (!existingItem || item.time > existingItem.time) {
            latestItemsMap.set(item.agent, item);
        }
    }

    return Array.from(latestItemsMap.values());
}

function Agent() {
    const [messages, setMessages] = useState<any[]>([]);
    const { chatId, loading, subscribe } = useAgent()

    useEffect(() => {
        if (chatId) {
            subscribe(chatId, (data) => {
                setMessages([...data]);
            })
        }
    }, [chatId]);

    return (
        <Stack gap="sm">
            <Title ta="center">Welcome Trader</Title>
            <Title order={2} ta="center">I am the Xtreamly Trading Agent</Title>
            <AspectRatio
                ratio={8 / 4.5}
                style={{
                    position: "relative",
                }}
            >
                <img src="firm.webp"/>
                <Box
                    w="100%"
                    style={{
                        position: "absolute",
                        top: 0,
                    }}
                >
                {
                    getLatestMessages(messages).map((m, i) => <Thought key={i} text={m.message} agent={m.agent}/>)
                }
                </Box>
            </AspectRatio>
            {chatId && <ChatPage chatId={chatId} messages={messages} loading={loading}/> }
        </Stack>
    );
}

export default Agent;
