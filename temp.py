# %reset -f
import os
import autogen
import numpy as np
import random
import json
import shutil
import pandas as pd
import pytz
import openai
import warnings
import openai
from dotenv import load_dotenv
from typing import Annotated, Literal
from urllib.parse import unquote
from datetime import datetime
from copy import deepcopy
from pprint import pprint
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
client_openai = openai.OpenAI()
np.random.seed(123)
random.seed(123)
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the leaderboard page
from codes_ai.utils import *
from codes_ai.agents import *
from codes_ai.prompts import *
#from codes_ai.formats import details
from codes_ai.firecrawl import firecrawl_page_raw

from pydantic import BaseModel, Field
from typing import Optional, List
import re
import json
import time

from settings.gcp import client_bq

timestamp = datetime.utcnow().replace(tzinfo=pytz.utc)

