# %reset -f
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.insert(0, parent_dir)
import requests
import numpy as np
import pandas as pd
import math
import time
import pytz
import json
import db_dtypes
import warnings
from datetime import datetime, timedelta
from pprint import pprint
from dotenv import load_dotenv
from typing import Annotated, Literal

# Suppress specific warnings
warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore")

from google.cloud import storage, bigquery  # , pubsub_v1
from google.oauth2 import service_account
from codes_ai.cookiedao_tools import *
from codes_ai.agents import *

auth_file = os.path.join(f'xtreamly-ai.json')
credentials = None
if os.path.isfile(auth_file):
    credentials = service_account.Credentials.from_service_account_file(auth_file)
client_bigquery = bigquery.Client(credentials=credentials, project="xtreamly-ai")
client_bq = client_bigquery

def load_agents():
    ## arbitrum
    sql_arbitrum = f"""
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY agentName ORDER BY _time DESC) AS rn
        FROM `xtreamly-ai.xtreamly_cookiedao.contracts`
        WHERE _time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)        
    )
    WHERE rn = 1 and chain = 42161
    ORDER BY _time DESC;
    """
    df_arbitrum = client_bq.query(sql_arbitrum).result().to_dataframe()
    
    ## agents
    sql_agents = f"""
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY agentName ORDER BY _time DESC) AS rn
        FROM `xtreamly-ai.xtreamly_cookiedao.agents`
        WHERE _time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
    )
    WHERE rn = 1
    ORDER BY _time DESC;
    """
    df_agents = client_bq.query(sql_agents).result().to_dataframe()
    df = df_agents.copy()
    #df = df[(df["marketCap"] > 10e5) & (df["volume24Hours"] > 0) & (df["holdersCount"] > 0)]
    df = df[df['agentName'].isin(df_arbitrum['agentName'])]
    return df

def invest(
        agentName: Annotated[str, "agentName"],
        volume: Annotated[float, "100.0"],
    ) -> str:
    # identify contract address        
    return f"""
    I have nvested in {agentName} in volumne: {volume}. 
    It was a pleasure talking to you!
    """

vol = xtreamly_volatility()
df = load_agents()
def agents_significant() -> str: return top_agents_significant(df)
def agents_popular() -> str: return top_agents_popular(df)
def agents_volatile() -> str: return top_agents_volatile(df)
def agents_stable() -> str: return top_agents_stable(df)
def agents_undervalued() -> str: return top_agents_undervalued(df)
def agents_newly_active() -> str: return top_agents_newly_active(df)

# =============================================================================
# Dynamic tools registry
autogen.register_function(xtreamly_volatility, caller=agent_researcher, executor=executor,
    name="xtreamly_volatility",
    description="""Checks current market volatility status"""
)
autogen.register_function(invest, caller=agent_researcher, executor=executor,
    name="invest",
    description="""Invests into agents"""
)

if vol =='low':
    autogen.register_function(agents_significant, caller=agent_researcher, executor=executor,
        name="agents_significant",
        description="""Identifies most significant agents"""
    )
    autogen.register_function(agents_popular, caller=agent_researcher, executor=executor,
        name="agents_popular",
        description="""Identifies most popular agents"""
    )    
    autogen.register_function(agents_volatile, caller=agent_researcher, executor=executor,
        name="agents_volatile",
        description="""Identifies most volatile agents"""
    )
    autogen.register_function(agents_undervalued, caller=agent_researcher, executor=executor,
        name="agents_undervalued",
        description="""Identifies most undervalued agents"""
    )

if vol =='high':
    autogen.register_function(agents_significant, caller=agent_researcher, executor=executor,
        name="agents_significant",
        description="""Identifies most significant agents"""
    )
    autogen.register_function(agents_popular, caller=agent_researcher, executor=executor,
        name="agents_popular",
        description="""Identifies most popular agents"""
    )    
    autogen.register_function(agents_stable, caller=agent_researcher, executor=executor,
        name="agents_stable",
        description="""Identifies most stable agents"""
    )
    autogen.register_function(agents_newly_active, caller=agent_researcher, executor=executor,
        name="agents_newly_active",
        description="""Identifies newly active agents"""
    )

# =============================================================================
group_chat = autogen.GroupChat(
    agents=[human_proxy, agent_planner, agent_researcher],
    messages=[],
    max_round=50,
)
group_chat_manager = autogen.GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}]},
)
agent_researcher.register_nested_chats(
    trigger=group_chat_manager,
    chat_queue=[
        {"recipient": agent_researcher, "sender": executor, "summary_method": "last_msg"},
        {"recipient": group_chat_manager, "sender": agent_researcher, "summary_method": "reflection_with_llm"},
        {"recipient": agent_planner, "sender": agent_researcher, "summary_method": "reflection_with_llm"},
        ],)  

def _conversation(msg):
    return human_proxy.initiate_chats([{
                "recipient": group_chat_manager,
                "message": f""" 
                {msg}
                """,
                "max_turns": 20,
                "max_round": 48,
                "summary_method": "reflection_with_llm",
            }])
    
_conversation("Find me best agents to invest now")
