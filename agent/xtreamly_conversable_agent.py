import autogen
from agent.ui_pusher import push_message


class XtreamlyConversableAgent(autogen.ConversableAgent):
    def __init__(
            self,
            chat_id: str,
            name: str,
            llm_config: dict,
            human_input_mode: str,
            is_termination_msg=None,
            system_message: str = "You are a helpful AI Assistant.",
            max_consecutive_auto_reply: int = None,
            default_auto_reply: str = '',
            input_queue=None
    ):
        super().__init__(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            is_termination_msg=is_termination_msg,
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            human_input_mode=human_input_mode,
            default_auto_reply=default_auto_reply,
        )
        self.chat_id = chat_id
        self.input_queue = input_queue
        self.register_hook("process_message_before_send", self.persist_assistant_messages)

    def persist_assistant_messages(
            self,
            sender,
            message,
            recipient,
            silent
    ):
        m = self._message_to_dict(message)
        push_message(self.chat_id, self.name, m.get("content", None))

        return message

    async def a_get_human_input(self, prompt: str) -> str:
        """Get human input.

        Override this method to customize the way to get human input.

        Args:
            prompt (str): prompt for the human input.

        Returns:
            str: human input.
        """
        if self.input_queue is None:
            return prompt

        reply = await self.input_queue.get()
        self._human_input.append(reply)
        return reply
