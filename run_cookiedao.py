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
import pytz
import json
import db_dtypes
from datetime import datetime, timedelta
from pprint import pprint
from dotenv import load_dotenv


from google.cloud import storage, bigquery  # , pubsub_v1
from google.oauth2 import service_account
from codes_ai.cookiedao import *

auth_file = os.path.join('..', 'gcp', f'xtreamly-ai.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = auth_file
auth_file = os.path.join(f'xtreamly-ai.json')
credentials = None
if os.path.isfile(auth_file):
    credentials = service_account.Credentials.from_service_account_file(auth_file)
client_bigquery = bigquery.Client(credentials=credentials, project="xtreamly-ai")
client_bq = client_bigquery

def _convert(df):
    for c,t in zip(df.columns, df.dtypes):
        if c == "_time":  df["_time"] = pd.to_datetime(df["_time"])
        elif str(t) == "object": df[c] = df[c].astype(str)
        elif str(t) == "float64": df[c] = df[c].astype("Float64")
        elif str(t) == "int64": df[c] = df[c].astype("Int64")
        else: 0
    return df

def load_data_cookiedao():
    df_agents, df_tweets, df_contracts = get_data_cookiedao()

    tbl_agents = f"xtreamly-ai.xtreamly_cookiedao.agents"
    tbl_tweets = f"xtreamly-ai.xtreamly_cookiedao.tweets"
    tbl_contracts = f"xtreamly-ai.xtreamly_cookiedao.contracts"

    job = client_bq.load_table_from_dataframe(_convert(df_agents), tbl_agents)
    job = client_bq.load_table_from_dataframe(_convert(df_tweets), tbl_tweets)
    job = client_bq.load_table_from_dataframe(_convert(df_contracts), tbl_contracts)

    # print("df_agents ",df_agents.shape[0])