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
import requests
import numpy as np
import pandas as pd
import math
import time
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm, to_hex, LinearSegmentedColormap, Normalize
import pytz
import json
import db_dtypes
from datetime import datetime, timedelta
from pprint import pprint
from dotenv import load_dotenv

def _msg(out, metric, var):
    msg = f"Top {metric} agents (by {var}):\n\t"
    if out.shape[0]:
        for i,r in out.iterrows():
            msg += f"{i+1}. {r['agentName']} ({np.round(r[var],4)}),\n\t"
    else:
        msg += " - None.\n\t"
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

# =============================================================================

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
