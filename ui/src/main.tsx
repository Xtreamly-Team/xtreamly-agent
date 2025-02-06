import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import App from './App'
import './index.css'

import {WagmiProvider} from 'wagmi'
import {QueryClient, QueryClientProvider} from '@tanstack/react-query'
import {initializeGA} from './utils/ga'
import {wagmiAdapter} from './utils/wallet'
import {MantineProvider} from "@mantine/core";
import {Notifications} from "@mantine/notifications";
import {BrowserRouter} from "react-router-dom";
import {theme} from "./theme";

initializeGA()

const queryClient = new QueryClient();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <BrowserRouter>
          <MantineProvider theme={theme} defaultColorScheme="dark">
              <WagmiProvider config={wagmiAdapter.wagmiConfig}>
                  <QueryClientProvider client={queryClient}>
                      <Notifications/>
                      <App/>
                  </QueryClientProvider>
              </WagmiProvider>
          </MantineProvider>
      </BrowserRouter>
  </StrictMode>,
)
