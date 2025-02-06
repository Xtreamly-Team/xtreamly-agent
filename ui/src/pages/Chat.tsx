import ChatInput from "../components/chat/chatinput";
import LoadingDots from "../components/chat/loadingDots";
import {useState} from "react";
import {Avatar, Box, Button, Group, Stack, Text, Title} from "@mantine/core";
import Markdown from "react-markdown";
import {post} from "../services/api";

export const AGENTS: any = {
    "Researcher": {
        title: "Researcher",
        x: "17%",
    },
    "Planner": {
        title: "Planner",
        x: "51%",
    },
    "tool_executor": {
        title: "Executor",
        x: "83.5%",
    },
    "human_proxy": {
        title: "You",
        x: "38.5%",
        y: "20%",
        noArrow: true,
        size: "md"
    },
}

export function ChatPage({
    chatId,
    loading,
    messages
}: any) {
    const [textLoaded] = useState(true);

    const postMessage = async (msg: any) => {
        try {
            const response = await post('conversation', {}, {
                chatId,
                msg
            })
            if (!response.ok) {
                throw new Error('Failed to send message');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };
    
    const renderWelcome = () => (
        <Stack justify="center" ta="center" flex={1}>
            {/*<Center>*/}
            {/*    <Image src='logo_only.png' h={150} w={200}/>*/}
            {/*</Center>*/}
            <Text>the first <b>AI-trained</b> DeFi trading agent specializing in loop trading.</Text>
            <Button
                maw={500}
                m="auto"
                onClick={
                    () => postMessage("What are the top 5 cookie DAO agents to invest in?")
                }
            >
                What are the top 5 cookie DAO agents to invest in?
            </Button>
        </Stack>
    );

    const renderMessages = () => {
        return (
            <Stack
                h="100%"
                w="100%"
                style={{
                    flexGrow: 1,
                    overflowY: "auto",
                    // flexDirection: "column-reverse"
                }}
            >
                {
                    loading &&
                    <Group>
                        <Avatar src="logo_only.png"/>
                        <LoadingDots/>
                    </Group>
                }
                {
                    [...messages].reverse().map(renderMessage)
                }
            </Stack>
        );
    };

    const renderMessage = (m: any, i: number) => {
        return (
            <Group key={i}>
                <Group wrap="nowrap" align="flex-start">
                    <Avatar src={m.ai ? `${m.agent}.webp` : null}/>
                    {
                        // i === 0 && m.ai ?
                        //     <SlowText text={m.message} textLoaded={() => setTextLoaded(true)}/> :
                        <Stack>
                            <Title order={2}>{AGENTS[m.agent].title}</Title>
                            <Text><Markdown>{m.message?.trim()}</Markdown></Text>
                        </Stack>
                    }
                </Group>
                {
                    (textLoaded || i !== 0) &&
                    <Group>
                        <Box w={40}/>
                    </Group>
                }
            </Group>
        );
    };

    return (
        <Stack>
            <ChatInput onAsk={postMessage} disabled={loading}/>
            {!messages.length && renderWelcome()}
            {messages.length > 0 && renderMessages()}
        </Stack>
    );
}
