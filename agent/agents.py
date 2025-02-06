import autogen
from agent.run_agents import *
from agent.xtreamly_conversable_agent import XtreamlyConversableAgent
import asyncio

llm_config = {
    "cache_seed": 44,
    "temperature": 0,
    "config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}],
    "timeout": 120,
}


class AutogenChat:
    def __init__(self, chat_id):
        self.websocket = asyncio.Queue()
        self.chat_id = chat_id
        self.client_sent_queue = asyncio.Queue()
        self.client_receive_queue = asyncio.Queue()

        self.agent_planner = XtreamlyConversableAgent(
            chat_id=chat_id,
            name="Planner",
            system_message="""
            # You are the Planner to progress of the task from human and discuss only about agents from Cookie DAO to invest in.
            Cookie DAO is crypto’s first AI agents index and a modular data layer for the agentic economy. 
    
            ### Responsibilities
            **1. Review Human Needs:**
            - Identify with human user needs of investing in agents from Cookie DAO
            - Query Researcher for more information
            **2. Propose to Human to invest with the rationale:**
            - Propose potenatial investment in agents from Cookie DAO with input: [agentName, Volume]
            - Ask for Human input to investment in agents from Cookie DAO
            **Execute Investment:**
            - Send request to Researcher to apply investment in agent from Cookie DAO
    
            ### Reply 'TERMINATE' when the whole task is completed.
            ### Do not reply when the user says says '!@#$^'.
            """,
            llm_config=llm_config,
            is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
            max_consecutive_auto_reply=3,
            human_input_mode="NEVER",
        )

        self.agent_researcher = XtreamlyConversableAgent(
            chat_id=chat_id,
            name=f"Researcher",
            system_message="""
            # You are the Researcher collecting information on agents from Cookie DAO.
            Cookie DAO is crypto’s first AI agents index and a modular data layer for the agentic economy. 
    
            ### Responsibilities
            - **Provide Tools Output:** Return results from executed tools to other conversation participants
            - **Deep dive:** Adjust research to gather missing information as needed
            - **Invest:** Request Human for confirmation and next ask Researcher to apply investment into agent from Cookie DAO
    
            ### Reply 'TERMINATE' when the whole task is completed.
            """,
            llm_config=llm_config,
            is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
            max_consecutive_auto_reply=5,
            human_input_mode="NEVER",
        )

        self.executor = XtreamlyConversableAgent(
            chat_id=chat_id,
            name=f"tool_executor",
            llm_config=False,
            is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
            default_auto_reply="TERMINATE",
            human_input_mode="NEVER",
        )

        self.human_proxy = XtreamlyConversableAgent(
            chat_id=chat_id,
            name="human_proxy",
            llm_config=False,  # no LLM used for human proxy
            human_input_mode="ALWAYS",  # always ask for human input
            input_queue=self.websocket
        )

        # =============================================================================
        # Dynamic tools registry
        autogen.register_function(xtreamly_volatility, caller=self.agent_researcher, executor=self.executor,
                                  name="xtreamly_volatility",
                                  description="""Checks current market volatility status"""
                                  )
        autogen.register_function(invest, caller=self.agent_researcher, executor=self.executor,
                                  name="invest",
                                  description="""Invests into cookie dao agents"""
                                  )

        if vol == 'low':
            autogen.register_function(agents_significant, caller=self.agent_researcher, executor=self.executor,
                                      name="agents_significant",
                                      description="""Identifies most significant agents"""
                                      )
            autogen.register_function(agents_popular, caller=self.agent_researcher, executor=self.executor,
                                      name="agents_popular",
                                      description="""Identifies most popular agents"""
                                      )
            autogen.register_function(agents_volatile, caller=self.agent_researcher, executor=self.executor,
                                      name="agents_volatile",
                                      description="""Identifies most volatile agents"""
                                      )
            autogen.register_function(agents_undervalued, caller=self.agent_researcher, executor=self.executor,
                                      name="agents_undervalued",
                                      description="""Identifies most undervalued agents"""
                                      )

        if vol == 'high':
            autogen.register_function(agents_significant, caller=self.agent_researcher, executor=self.executor,
                                      name="agents_significant",
                                      description="""Identifies most significant agents"""
                                      )
            autogen.register_function(agents_popular, caller=self.agent_researcher, executor=self.executor,
                                      name="agents_popular",
                                      description="""Identifies most popular agents"""
                                      )
            autogen.register_function(agents_stable, caller=self.agent_researcher, executor=self.executor,
                                      name="agents_stable",
                                      description="""Identifies most stable agents"""
                                      )
            autogen.register_function(agents_newly_active, caller=self.agent_researcher, executor=self.executor,
                                      name="agents_newly_active",
                                      description="""Identifies newly active agents"""
                                      )

        # =============================================================================
        group_chat = autogen.GroupChat(
            agents=[self.human_proxy, self.agent_planner, self.agent_researcher],
            messages=[],
            max_round=50,
        )
        self.group_chat_manager = autogen.GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}]},
        )
        self.agent_researcher.register_nested_chats(
            trigger=self.group_chat_manager,
            chat_queue=[
                {"recipient": self.agent_researcher, "sender": self.executor, "summary_method": "last_msg"},
                {"recipient": self.group_chat_manager, "sender": self.agent_researcher, "summary_method": "reflection_with_llm"},
                {"recipient": self.agent_planner, "sender": self.agent_researcher, "summary_method": "reflection_with_llm"},
                {"recipient": self.agent_planner, "sender": self.human_proxy, "summary_method": "reflection_with_llm"},
            ])

    async def start(self, message):
        await self.human_proxy.a_initiate_chats([{
            "chat_id": self.chat_id,
            "recipient": self.group_chat_manager,
            "message": "!@#$^",
            "max_turns": 20,
            "max_round": 48,
            "summary_method": "reflection_with_llm",
        }])
