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

# from gcp.func import client_bq
# from gcp.func import *
# from settings.plot import tailwind, _style, _style_black, _style_white
# folder = 'plot_cookiedao'

pd.set_option('display.max_columns', None)
load_dotenv()

headers = {
    "x-api-key": os.environ.get("COOKIE_DAO_API"),
}

def get_agents(page):
    base_url = "https://api.cookie.fun/v2/"
    res = requests.get(base_url + "agents/agentsPaged", {
        "interval": "_7Days",
        "page": page,
        "pageSize": 25,
    }, headers=headers)
    res.raise_for_status()
    res = res.json()["ok"]
    return res["data"], res["currentPage"] == res["totalPages"]

def agent_record(a):
    return {
        "agentName": a["agentName"],
        "mindshare": a["mindshare"],
        "mindshareDeltaPercent": a["mindshareDeltaPercent"],
        "marketCap": a["marketCap"],
        "marketCapDeltaPercent": a["marketCapDeltaPercent"],
        "price": a["price"],
        "priceDeltaPercent": a["priceDeltaPercent"],
        "liquidity": a["liquidity"],
        "volume24Hours": a["volume24Hours"],
        "volume24HoursDeltaPercent": a["volume24HoursDeltaPercent"],
        "holdersCount": a["holdersCount"],
        "holdersCountDeltaPercent": a["holdersCountDeltaPercent"],
        "averageImpressionsCount": a["averageImpressionsCount"],
        "averageImpressionsCountDeltaPercent": a["averageImpressionsCountDeltaPercent"],
        "averageEngagementsCount": a["averageEngagementsCount"],
        "averageEngagementsCountDeltaPercent": a["averageEngagementsCountDeltaPercent"],
        "followersCount": a["followersCount"],
        "smartFollowersCount": a["smartFollowersCount"],
        "contracts": json.dumps(a["contracts"]),
        "twitterUsernames": ",".join(a["twitterUsernames"]),
    }   

def get_data_cookiedao():
    _time = datetime.utcnow().replace(tzinfo=pytz.utc).strftime("%Y-%m-%d %H:%M:%S")

    Agents = []
    page = 1
    done = False
    # while not done:
    agents, done = get_agents(page)
    Agents += agents
    # print("Ingested page", page)    
    page += 1
    time.sleep(.5)
    
    df_agents = pd.DataFrame([agent_record(a) for a in Agents])
    
    Tweets = []
    for a in Agents[:]: 
        if len(a['topTweets']):
            df_t = pd.DataFrame(a['topTweets'])
            df_t['agentName'] = a['agentName']
            Tweets += [df_t]
    df_tweets = pd.concat(Tweets) 
    
    Contracts = []
    for a in Agents[:]: 
        if len(a['contracts']):
            df_c = pd.DataFrame(a['contracts'])
            df_c['agentName'] = a['agentName']
            Contracts += [df_c]
    df_contracts = pd.concat(Contracts)
    
    df_agents['_time'] = _time
    df_tweets['_time'] = _time
    df_contracts['_time'] = _time    
    return df_agents, df_tweets, df_contracts


def load_data_cookiedao():
    df_agents, df_tweets, df_contracts = get_data_cookiedao()




# =============================================================================
# Time


# =============================================================================
# # =============================================================================
# # Upload BQ
# auth_file = os.path.join('..', 'gcp', f'xtreamly-ai-cc418ba37b0c.json')
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = auth_file
# from google.cloud import bigquery
# 
# tbl_agents = f"xtreamly-ai.xtreamly_cookiedao.agents"
# tbl_tweets = f"xtreamly-ai.xtreamly_cookiedao.tweets"
# tbl_contracts = f"xtreamly-ai.xtreamly_cookiedao.contracts"
# 
# def _convert(df):
#     for c,t in zip(df.columns, df.dtypes):
#         if c == "_time":  df["_time"] = pd.to_datetime(df["_time"])
#         elif str(t) == "object": df[c] = df[c].astype(str)
#         elif str(t) == "float64": df[c] = df[c].astype("Float64")
#         elif str(t) == "int64": df[c] = df[c].astype("Int64")
#         else: 0
#     return df
# job = client_bq.load_table_from_dataframe(_convert(df_agents), tbl_agents)
# job = client_bq.load_table_from_dataframe(_convert(df_tweets), tbl_tweets)
# job = client_bq.load_table_from_dataframe(_convert(df_contracts), tbl_contracts)
# =============================================================================


# =============================================================================
# Define BQ
# schema_agents = [
#     bigquery.SchemaField("_time", "TIMESTAMP"),
#     bigquery.SchemaField("agentName", "STRING"),
#     bigquery.SchemaField("mindshare", "FLOAT"),
#     bigquery.SchemaField("mindshareDeltaPercent", "FLOAT"),
#     bigquery.SchemaField("marketCap", "FLOAT"),
#     bigquery.SchemaField("marketCapDeltaPercent", "FLOAT"),
#     bigquery.SchemaField("price", "FLOAT"),
#     bigquery.SchemaField("priceDeltaPercent", "FLOAT"),
#     bigquery.SchemaField("liquidity", "FLOAT"),
#     bigquery.SchemaField("volume24Hours", "FLOAT"),
#     bigquery.SchemaField("volume24HoursDeltaPercent", "FLOAT"),
#     bigquery.SchemaField("holdersCount", "INTEGER"),
#     bigquery.SchemaField("holdersCountDeltaPercent", "FLOAT"),
#     bigquery.SchemaField("averageImpressionsCount", "FLOAT"),
#     bigquery.SchemaField("averageImpressionsCountDeltaPercent", "FLOAT"),
#     bigquery.SchemaField("averageEngagementsCount", "FLOAT"),
#     bigquery.SchemaField("averageEngagementsCountDeltaPercent", "FLOAT"),
#     bigquery.SchemaField("followersCount", "INTEGER"),
#     bigquery.SchemaField("smartFollowersCount", "INTEGER"),
#     bigquery.SchemaField("contracts", "STRING"),
#     bigquery.SchemaField("twitterUsernames", "STRING"),
#     ]
# table_agents = bigquery.Table(tbl_agents, schema=schema_agents)
# table_agents = client_bq.create_table(table_agents, exists_ok=True)
# 
# 
# schema_tweets = [
#     bigquery.SchemaField("_time", "TIMESTAMP"),
#     bigquery.SchemaField("tweetUrl", "STRING"),
#     bigquery.SchemaField("tweetAuthorProfileImageUrl", "STRING"),
#     bigquery.SchemaField("tweetAuthorDisplayName", "STRING"),
#     bigquery.SchemaField("smartEngagementPoints", "INTEGER"),
#     bigquery.SchemaField("impressionsCount", "INTEGER"),
#     bigquery.SchemaField("agentName", "STRING"),
# ]
# table_tweets = bigquery.Table(tbl_tweets, schema=schema_tweets)
# table_tweets = client_bq.create_table(table_tweets, exists_ok=True)
# 
# 
# schema_contracts = [
#     bigquery.SchemaField("_time", "TIMESTAMP"),
#     bigquery.SchemaField("agentName", "STRING"),
#     bigquery.SchemaField("chain", "INTEGER"),
#     bigquery.SchemaField("contractAddress", "STRING"),
# ]
# table_contracts = bigquery.Table(tbl_contracts, schema=schema_contracts)
# table_contracts = client_bq.create_table(table_contracts, exists_ok=True)
# =============================================================================


# =============================================================================
# class APIClient:
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.base_url = 'https://api.cookie.fun/v1'
#         
#     def get_kols(self, limit=50):
#         headers = {'x-api-key': self.api_key}
#         response = requests.get(
#             f'{self.base_url}/kols',
#             headers=headers,
#             params={'limit': limit}
#         )
#         return response.json()
# 
# 
# class CookieAPIClient:
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.base_url = "https://api.cookie.fun/v1"
#         self.headers = {"x-api-key": self.api_key}
#     
#     def check_connection(self):
#         """Check if the API key is valid and fetch quota details."""
#         url = f"{self.base_url}/authorization"
#         response = requests.get(url, headers=self.headers)
#         
#         if response.status_code == 200:
#             print("✅ Connection successful!")
#             return response.json()
#         elif response.status_code == 401:
#             print("❌ Invalid API Key! Please check your API credentials.")
#         elif response.status_code == 403:
#             print("❌ Access restricted! Your API plan may not allow this request.")
#         elif response.status_code == 429:
#             print("⚠️ Rate limit exceeded! Try again later.")
#         else:
#             print(f"❌ Connection failed! HTTP Status: {response.status_code}")
#         return response.json() if response.content else None  # ✅ Fixed return statement
# 
# api_key=os.getenv('COOKIE_DAO_API')
# client = CookieAPIClient(api_key)
# quota_info = client.check_connection()
# 
# if quota_info:
#     print("Quota Information:", quota_info)
# =============================================================================


    
    
    
    
    