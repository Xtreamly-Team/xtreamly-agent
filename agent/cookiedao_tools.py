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

