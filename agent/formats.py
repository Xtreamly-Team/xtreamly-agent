from pydantic import BaseModel, Field
from typing import Optional, List

class details_ideas(BaseModel):
    Agent: str = Field(..., description="Agent name")
    Name: str = Field(..., description="Name of the token")

class details_overview(BaseModel):
    overview: str = Field(..., description="Short anwer for the user (1-2) sentences.")
