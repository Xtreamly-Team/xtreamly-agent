import {createAppKit} from '@reown/appkit/react'

import {arbitrumSepolia} from '@reown/appkit/networks'
import {WagmiAdapter} from '@reown/appkit-adapter-wagmi'
import type {AppKitNetwork} from "@reown/appkit-common";

export const rpc = arbitrumSepolia.rpcUrls.default.http[0]

// 1. Get projectId from https://cloud.reown.com
const projectId = 'bc074c01e77d2f77b965dd15b994e5a5'

// 2. Create a metadata object - optional
const metadata = {
    name: 'xtreamly',
    description: 'AppKit Example',
    url: 'https://reown.com/appkit', // origin must match your domain & subdomain
    icons: ['https://assets.reown.com/reown-profile-pic.png']
}

// 3. Set the networks
const networks = [arbitrumSepolia] as [AppKitNetwork]

// 4. Create Wagmi Adapter
export const wagmiAdapter = new WagmiAdapter({
    networks,
    projectId,
    ssr: true
});

// 5. Create modal
createAppKit({
    adapters: [wagmiAdapter],
    networks,
    projectId,
    metadata,
    features: {
        analytics: true // Optional - defaults to your Cloud configuration
    },
    themeVariables: {
        '--w3m-accent': "#0047D0FF",
        '--w3m-color-mix-strength': 10,
    }
})