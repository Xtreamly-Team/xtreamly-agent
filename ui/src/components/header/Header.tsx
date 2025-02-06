import {Anchor, Box, Burger, Button, Container, Drawer, Group, Loader, rem, ScrollArea, Stack} from '@mantine/core';
import {Link} from 'react-router-dom';
import styles from './Header.module.scss';
import {useAccount} from 'wagmi';
import {useDisclosure} from "@mantine/hooks";

const imageSize = 50;

function Logo() {
    return (
        <Anchor component={Link} to="/" className='dfa'>
            <img src="/logo.png" alt="Logo" width={imageSize * 2} height={imageSize}/>
        </Anchor>
    )
}

function WalletConnect() {
    const { isReconnecting, isDisconnected } = useAccount()

    if (!isDisconnected && isReconnecting) {
        return <Loader size={55}/>
    }

    return <w3m-button/>
}

function Header() {
    const [drawerOpened, { toggle: toggleDrawer, close: closeDrawer }] = useDisclosure(false);

    return (
        <Box component="header" className={styles.header}>
            <Container size="xl">
                <Group justify="space-between">
                    <Logo/>
                    <Group visibleFrom="md">
                        <WalletConnect/>
                    </Group>
                    <Burger
                        opened={drawerOpened}
                        onClick={toggleDrawer}
                        hiddenFrom="md"
                    />
                </Group>
            </Container>

            <Drawer
                title={<Logo/>}
                opened={drawerOpened}
                onClose={closeDrawer}
                padding="md"
                hiddenFrom="md"
                zIndex={100}
            >
                <ScrollArea h={`calc(100vh - ${rem(90)})`} mx="-md">
                    <Stack align="flex-start">
                        <Button component={Link} to="/" variant="light">Agent</Button>
                        <Box ml="md">
                            <WalletConnect/>
                        </Box>
                    </Stack>
                </ScrollArea>
            </Drawer>
        </Box>
    );
}

export default Header;