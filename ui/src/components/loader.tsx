import {LoadingOverlay} from "@mantine/core";
import {brandColor} from "../theme.ts";

export function UiLoader() {
    return (
        <LoadingOverlay
            visible
            zIndex={1000}
            color={brandColor}
            overlayProps={{
                radius: "sm",
                blur: 1,
                backgroundOpacity: 0.1
            }}
        />
    );
}