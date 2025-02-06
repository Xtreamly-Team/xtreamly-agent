import {Stack, Text, Title} from "@mantine/core";

function NoMatch() {
  return (
      <Stack align="center" mt={150}>
          <Title>Page Not Found</Title>
          <Text>
              The specified file was not found on this website. Please check the URL
              for mistakes and try again.
          </Text>
      </Stack>
  );
}

export default NoMatch;
