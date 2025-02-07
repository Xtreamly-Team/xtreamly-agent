import {useQuery} from '@tanstack/react-query'
import {VolatilityAPI} from "../utils/VolatilityAPI";

export function useCurrentVolatility() {
    const {data: currentVolatility, isLoading} = useQuery({
        queryKey: ["curren-volatility"],
        queryFn: async () => new VolatilityAPI().state(),
        staleTime: 60000, // 1 minute
    })

    return {
        currentVolatility,
        loading: isLoading
    }
}

export function useHistoricalVolatility() {
    const {data: historicalVolatility, isLoading} = useQuery({
        queryKey: ["historical-volatility"],
        queryFn: async () => {
            const now = Date.now()
            const from = now - (1000 * 60 * 60) // -1 hour
            return new VolatilityAPI().historicalState(new Date(from), new Date(now))
        },
        staleTime: 60000, // 1 minute
    })

    return {
        historicalVolatility,
        loading: isLoading
    }
}