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
from agent.cookiedao_tools import *
from agent.agents import *

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
    I have invested in {agentName} in volume: {volume}. 
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
