# %reset -f
# =============================================================================
# https://docs.cookie.fun/#/
# https://cookiedao.notion.site/Cookie-DeFAI-Hackathon-17ddcd6f6625800dab49d8fb103ecc48
# https://discord.com/channels/994904272489680917/@home
# =============================================================================

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.insert(0, parent_dir)
from gcp.func import client_bq
import requests
import numpy as np
import pandas as pd
import math
import time
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.image as image
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm, to_hex, LinearSegmentedColormap, Normalize
import pytz
import json
import db_dtypes
from datetime import datetime, timedelta
from pprint import pprint
from dotenv import load_dotenv

from gcp.func import *
from settings.plot import tailwind, _style, _style_black, _style_white
pd.set_option('display.max_columns', None)
load_dotenv()
folder = 'plot_cookiedao'

chain_arbitrum = 42161

# Data BQ
## arbitrum
sql_arbitrum = f"""
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY agentName ORDER BY _time DESC) AS rn
    FROM `xtreamly-ai.xtreamly_cookiedao.contracts`
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
)
WHERE rn = 1
ORDER BY _time DESC;
"""
df_agents = client_bq.query(sql_agents).result().to_dataframe()
df = df_agents.copy()
#df = df[(df["marketCap"] > 10e5) & (df["volume24Hours"] > 0) & (df["holdersCount"] > 0)]
df = df[df['agentName'].isin(df_arbitrum['agentName'])]



# Tools - Cookie DAO
def _msg(out, metric, var):
    msg = f"Top {metric} agents (by {var}):\n\t"
    for i,r in out.iterrows():
        msg += f"{i+1}. {r['agentName']} ({np.round(r[var],4)}),\n\t"
    return msg[:-3]

def top10_agents_significant(df):
    out = df[
        (df["mindshareDeltaPercent"].abs() >= 10) |
        (df["marketCapDeltaPercent"].abs() >= 10) |
        (df["priceDeltaPercent"].abs() >= 10) |
        (df["volume24HoursDeltaPercent"].abs() >= 10)
    ].sort_values(by='followersCount', ascending=False).head(10).reset_index(drop=True)
    return _msg(out, "significant", "followersCount")

def top10_agents_popular(df):
    out = df[
        (df["followersCount"] >= 500) & 
        (df["averageEngagementsCountDeltaPercent"] >= 10)
    ].sort_values(by='followersCount', ascending=False).head(10).reset_index(drop=True)
    return _msg(out, "popular", "followersCount")

def top10_agents_performing(df):
    out = df.sort_values(by=["marketCap", "mindshare", "followersCount"], 
                         ascending=[False, False, False]).head(10).reset_index(drop=True)
    return _msg(out, "popular", "marketCap")

def top10_agents_volatile(df):
    out = df.assign(volatility_score=(
        df["priceDeltaPercent"].abs() +
        df["marketCapDeltaPercent"].abs() +
        df["volume24HoursDeltaPercent"].abs()
    )).sort_values(by="volatility_score", ascending=False).head(10).reset_index(drop=True)
    return _msg(out, "volatile", "volatility_score")

def top10_agents_stable(df):
    out = df.assign(volatility_score=(
        df["priceDeltaPercent"].abs() +
        df["marketCapDeltaPercent"].abs() +
        df["volume24HoursDeltaPercent"].abs()
    )).sort_values(by="volatility_score", ascending=True).head(10).reset_index(drop=True)
    return _msg(out, "stable", "volatility_score")

def top10_agents_undervalued(df):
    out = df[df["marketCap"] > 0].assign(undervalue_score=(
        df["averageEngagementsCount"] / df["marketCap"]
    )).sort_values(by="undervalue_score", ascending=False).head(10).reset_index(drop=True)
    return _msg(out, "undervalued", "undervalue_score")

def top10_agents_newly_active(df):
    out = df[
        (df["holdersCountDeltaPercent"] > 10) & 
        (df["volume24HoursDeltaPercent"] > 10)
    ].sort_values(by="holdersCountDeltaPercent", ascending=False).head(10).reset_index(drop=True)
    return _msg(out, "newly active", "holdersCountDeltaPercent")

print(top10_agents_significant(df))
print(top10_agents_popular(df))
print(top10_agents_volatile(df))
print(top10_agents_stable(df))
print(top10_agents_undervalued(df))
print(top10_agents_newly_active(df))

# to do - add tools that evaluate tweets as influencers - analyse tweets with openai

def xtreamly_volatility():
    threshold = 0.003897
    symbol = "ETH"  # Change this to any token symbol
    horizon = "60min"  # Options: "1min", "60min", etc.
    url = f"https://api.xtreamly.io/volatility_prediction?symbol={symbol}&horizon={horizon}"
    headers = {"accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for bad responses (4xx and 5xx)
        data = response.json()
        state = 'low' if data['volatility'] <= 0.003897 else 'high'
        return state
    except requests.exceptions.RequestException as e:
        return f"Error fetching volatility prediction: {e}"

# =============================================================================
# # =============================================================================
# # # Do every hour: 
# # =============================================================================
# state = xtreamly_volatility()
# # 0. Get list of agents with current exposure (from previous inference)
# if state=='low': 0
# # =============================================================================
# #     [LLM] Get agent to use these functions: # eventually we can get to hardcoded selection
# #         - top10_agents_significant
# #         - top10_agents_undervalued
# #         - top10_agents_stable
# #     Agent decides best 10 agents to follow
# #     Filter for new agents to follow 
# #     Close exposure on agents that are not in new new follow list
# #     Invest Long in these new agents equally with available funds
# # =============================================================================
# if state=='high': 0
# # =============================================================================
# #     [LLM] Get agent to use these functions: # eventually we can get to hardcoded selection
# #         - top10_agents_significant
# #         - top10_agents_popular
# #         - top10_agents_volatile
# #         - top10_agents_newly_active
# #     Agent decides best 10 agents to follow
# #     Filter for new agents to follow 
# #     Close exposure on agents that are not in new new follow list
# #     Invest Long in these new agents equally with available funds
# # =============================================================================
# =============================================================================

