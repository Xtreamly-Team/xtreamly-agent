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

df = None


def load_agents():
    global df
    print("Loading agents...")
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
    df = df[(df["marketCap"] > 10e5) & (df["volume24Hours"] > 0) & (df["holdersCount"] > 0)]
    # df = df[df['agentName'].isin(df_arbitrum['agentName'])]
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


def _msg(out, metric, var):
    msg = f"Top {metric} agents (by {var}):\n\t"
    if out.shape[0]:
        for i, r in out.iterrows():
            msg += f"{i + 1}. {r['agentName']} ({np.round(r[var], 4)}),\n\t"
    else:
        msg += " - None (try different tool).\n\t"
    return msg[:-3]


def top_agents_significant() -> str:
    global df
    out = df[
        (df["mindshareDeltaPercent"].abs() >= 10) |
        (df["marketCapDeltaPercent"].abs() >= 10) |
        (df["priceDeltaPercent"].abs() >= 10) |
        (df["volume24HoursDeltaPercent"].abs() >= 10)
        ].sort_values(by='followersCount', ascending=False).head(10).reset_index(drop=True)
    return _msg(out, "significant", "followersCount")


def top_agents_popular() -> str:
    global df
    out = df[
        (df["followersCount"] >= 500) &
        (df["averageEngagementsCountDeltaPercent"] >= 10)
        ].sort_values(by='followersCount', ascending=False).head(10).reset_index(drop=True)
    return _msg(out, "popular", "followersCount")


def top_agents_performing() -> str:
    global df
    out = df.sort_values(by=["marketCap", "mindshare", "followersCount"],
                         ascending=[False, False, False]).head(10).reset_index(drop=True)
    return _msg(out, "popular", "marketCap")


def top_agents_volatile() -> str:
    global df
    out = df.assign(volatility_score=(
            df["priceDeltaPercent"].abs() +
            df["marketCapDeltaPercent"].abs() +
            df["volume24HoursDeltaPercent"].abs()
    )).sort_values(by="volatility_score", ascending=False).head(10).reset_index(drop=True)
    return _msg(out, "volatile", "volatility_score")


def top_agents_stable() -> str:
    global df
    out = df.assign(volatility_score=(
            df["priceDeltaPercent"].abs() +
            df["marketCapDeltaPercent"].abs() +
            df["volume24HoursDeltaPercent"].abs()
    )).sort_values(by="volatility_score", ascending=True).head(10).reset_index(drop=True)
    return _msg(out, "stable", "volatility_score")


def top_agents_undervalued() -> str:
    global df
    out = df[df["marketCap"] > 0].assign(undervalue_score=(
            df["averageEngagementsCount"] / df["marketCap"]
    )).sort_values(by="undervalue_score", ascending=False).head(10).reset_index(drop=True)
    return _msg(out, "undervalued", "undervalue_score")


def top_agents_newly_active() -> str:
    global df
    out = df[
        (df["holdersCountDeltaPercent"] > 10) &
        (df["volume24HoursDeltaPercent"] > 10)
        ].sort_values(by="holdersCountDeltaPercent", ascending=False).head(10).reset_index(drop=True)
    return _msg(out, "newly active", "holdersCountDeltaPercent")


# =============================================================================
def xtreamly_volatility() -> str:
    threshold = 0.003897
    symbol = "ETH"  # Change this to any token symbol
    horizon = "60min"  # Options: "1min", "60min", etc.
    url = f"https://api.xtreamly.io/volatility_prediction?symbol={symbol}&horizon={horizon}"
    headers = {
        "accept": "application/json",
        "x-api-key": os.environ.get("XTREAMLY_API"),
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for bad responses (4xx and 5xx)
        data = response.json()
        state = 'low' if data['volatility'] <= threshold else 'high'
        return state
    except requests.exceptions.RequestException as e:
        return f"Error fetching volatility prediction: {e}"


vol = xtreamly_volatility()
load_agents()


def agents_significant() -> str: return top_agents_significant()


def agents_popular() -> str: return top_agents_popular()


def agents_volatile() -> str: return top_agents_volatile()


def agents_stable() -> str: return top_agents_stable()


def agents_undervalued() -> str: return top_agents_undervalued()


def agents_newly_active() -> str: return top_agents_newly_active()
