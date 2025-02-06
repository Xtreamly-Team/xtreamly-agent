// Core styles
import '@mantine/core/styles.css'
// Package styles
// import '@mantine/dates/styles.css'
import '@mantine/notifications/styles.css'
// import '@mantine/dropzone/styles.css';
// import '@mantine/charts/styles.css';
import {generateColors} from '@mantine/colors-generator'

import {createTheme, Loader} from "@mantine/core";
import {RingLoader} from "./components/RingLoader.tsx";

export const brandColor = '#28ab99'
export const brand = generateColors(brandColor)
export const blueColor = '#1d2f86'
export const blue = generateColors(blueColor)
export const redColor = '#cc2332'
export const red = generateColors(redColor)
export const gradientColor = 'linear-gradient(90deg, rgba(29,47,134,1) 0%, rgba(226,226,226,1) 49%, rgba(204,35,50,1) 100%)'
export const gradient = {
    from: blueColor,
    to: redColor,
    deg: 141
};

export const theme = createTheme({
    black: '#040307',
    colors: {
        blue,
        red,
    },
    fontFamily: 'ABCDiatype-Medium, sans-serif',
    fontFamilyMonospace: 'ABCDiatypeSemi-Mono-Medium, monospace',
    headings: {fontFamily: 'ABCDiatype-Medium, sans-serif'},
    components: {
        Loader: Loader.extend({
            defaultProps: {
                loaders: { ...Loader.defaultLoaders, ring: RingLoader },
                color: brandColor,
                type: 'ring',
            },
        }),
        TextInput: {
            styles: () => ({
                label: {
                    display: 'block',
                    textAlign: 'left',
                },
            }),
        },
        Textarea: {
            styles: () => ({
                label: {
                    display: 'block',
                    textAlign: 'left',
                },
            }),
        },
        Select: {
            styles: () => ({
                label: {
                    display: 'block',
                    textAlign: 'left',
                },
            }),
        },
        Button: {
            styles: (_: any, {variant}: any) => {
                const baseStyles = {
                    root: {
                        borderRadius: 40,
                    },
                };

                const variants: any = {
                    filled: {
                        root: {
                            background: "linear-gradient(265.56deg, #246CF9 -0.27%, #1E68F6 -0.26%, #0047D0 98.59%)",
                            color: "#FFFFFF",
                            border: "none",
                            "&:hover": {
                                color: "red !important",
                            },
                        },
                    },
                    outline: {
                        root: {
                            background: "none",
                            color: "#fff",
                            border: "1px solid #fff",
                        },
                    },
                    light: {
                        root: {
                            backgroundColor: "transparent",
                            color: "#fff",
                            transition: "color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out",
                            "&:hover": {
                                color: "rgb(28.8, 86.4, 199.2)",
                            },
                        },
                    },
                    default: {
                        root: {
                            background: "linear-gradient(265.56deg, #246CF9 -0.27%, #1E68F6 -0.26%, #0047D0 98.59%)",
                            border: 0,
                            color: "#FFF",
                        },
                    }
                };

                return { ...baseStyles, ...(variants[variant] || variants.default) };
            },
        },
    },
})