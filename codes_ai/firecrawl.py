import os
import re
import json
from codes_ai.utils import * 
from firecrawl import FirecrawlApp
import openai
from openai import OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
client_openai = OpenAI()
firecrawl = FirecrawlApp(api_key=os.environ['FIRECRAWL_API_KEY'])
from typing import Annotated, Literal

def firecrawl_page_raw(
        url: Annotated[str, "Url"],
    ) -> str:
    
    page_content = firecrawl.scrape_url(
        url=url,
        params={
            "pageOptions":{
                "onlyMainContent": True
            }
        })
    web_content = page_content['markdown']
    return web_content


def _scrap_url(url, context, details, Data_pages):
    page_content_raw = firecrawl_page_raw(url)
    Data_pages += [{"url": url, "page": page_content_raw}]

    if nr_tokens(page_content_raw) > 2500: 
        prompt_concise_details = "" 
        for f in details.__fields__:
            prompt_concise_details += f"\t- {f} ({details.__fields__[f].description})\n"
        propmpt_concise = f"""Concise page information into the report in a clear and organized manner.
        
        Focus on when available:
            - {context} 
        {prompt_concise_details}
        
        Page content: 
        {page_content_raw}
        """
        
        response = client_openai.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {
                "role": "user",
                "content": [{ "type": "text", "text": propmpt_concise,},],
            }
          ],
          max_tokens=4000,
          temperature=0.
        )
        page_content = response.choices[0].message.content
    else:
        page_content = page_content_raw
    return page_content