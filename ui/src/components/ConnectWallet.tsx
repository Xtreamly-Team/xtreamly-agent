import {Center, Stack, Text} from "@mantine/core";

export default function ConnectWallet() {
    return (
        <Stack>
            <Text ta='center'>Connect your wallet to view your transactions.</Text>
            <Center>
                <w3m-button/>
            </Center>
        </Stack>
    )
}
