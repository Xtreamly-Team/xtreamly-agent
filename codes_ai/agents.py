import os
import autogen

llm_config={
    "cache_seed": 44,
    "temperature": 0,
    "config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}],
    "timeout": 120,
    }

agent_planner = autogen.ConversableAgent(
        name="Planner",
        system_message = """
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
        """,
        llm_config=llm_config,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        max_consecutive_auto_reply=3,
        human_input_mode="NEVER",
    )

agent_researcher = autogen.ConversableAgent(
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

executor = autogen.ConversableAgent(
        name=f"tool_executor",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        default_auto_reply="TERMINATE",
        human_input_mode="NEVER",
    )

human_proxy = autogen.ConversableAgent(
    "human_proxy",
    llm_config=False,  # no LLM used for human proxy
    human_input_mode="ALWAYS",  # always ask for human input
)
