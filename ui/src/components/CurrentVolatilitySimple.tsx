import {useCurrentVolatility, useHistoricalVolatility} from "../data-access/volatility.ts";
import {Card, Group, Text, Title} from "@mantine/core";
import {UiLoader} from "./loader.tsx";
import {IconArrowDown, IconArrowUp, IconCircleFilled} from "@tabler/icons-react";
import {LineChart} from "@mantine/charts";

export const VOL_MAP = {
    "highvol": {
        title: "HIGH",
        color: "green",
        icon: <IconArrowUp size="1.8vw" color="green"/>,
    },
    "midvol": {
        title: "MEDIUM",
        color: "blue",
        icon: <IconCircleFilled size="1.8vw" color="blue"/>,
    },
    "lowvol": {
        title: "LOW",
        color: "red",
        icon: <IconArrowDown size="1.8vw" color="red"/>,
    },
} as any

function mapToBars(vol: any) {
    const date = new Date(vol.timestamp).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
    let value = 0
    if (vol.classification === 'highvol') {
        value = 10
    }
    if (vol.classification === 'lowvol') {
        value = -10
    }
    return {
        date,
        value
    }
}

export default function CurrentVolatilitySimple() {
    const { currentVolatility, loading } = useCurrentVolatility();
    const { historicalVolatility } = useHistoricalVolatility();

    if (loading || !currentVolatility) {
        return <UiLoader/>
    }

    const vol = VOL_MAP[currentVolatility.classification];
    let data = historicalVolatility ? historicalVolatility.map(mapToBars) : []
    data = [
        {
            date: "",
            value: -10
        },
        ...data
    ]

    return (
        <Card
            shadow="sm"
            px={10}
            radius="lg"
            ta="center"
            w="28%"
            h="33%"
            bg="rgba(0,0,0, 0.9)"
            style={{
                position: 'absolute',
                top: "14%",
                left: "36%"
            }}
        >
            <Group justify="center" gap={5}>
                <Title size="1.3vw">Volatility Prediction:</Title>
                <Text
                    size="1.3vw"
                    c={vol.color}
                >
                    {vol.title}
                </Text>
                {vol.icon}
            </Group>
            <Group mt={5} mb={10} gap={5} justify="center">
                <IconCircleFilled color={VOL_MAP.highvol.color} size={15}/>
                <Text size="sm">High</Text>
                <IconCircleFilled color={VOL_MAP.midvol.color} size={15}/>
                <Text size="sm">Medium</Text>
                <IconCircleFilled color={VOL_MAP.lowvol.color} size={15}/>
                <Text size="sm">Low</Text>
            </Group>
            <LineChart
                h={210}
                p={10}
                data={data}
                dataKey="date"
                withYAxis={false}
                series={[{ name: 'value', label: 'Avg. Temperature' }]}
                type="gradient"
                gradientStops={[
                    { offset: 0, color: VOL_MAP.highvol.color },
                    { offset: 50, color: VOL_MAP.midvol.color },
                    { offset: 100, color: VOL_MAP.lowvol.color },
                ]}
                withDots={false}
                withTooltip={false}
            />
        </Card>
    )
}