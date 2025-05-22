# schemas.py
# Pydantic schemas for FarFetchr backend

# TODO: Define request and response schemas for /distance and /history endpoints 

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DistanceRequest(BaseModel):
    source: str = Field(..., example="415 Mission St, San Francisco, CA")
    destination: str = Field(..., example="1600 Amphitheatre Parkway, Mountain View, CA")

class DistanceResponse(BaseModel):
    miles: float
    kilometers: float
    source: str
    destination: str
    timestamp: datetime

class QueryRead(BaseModel):
    id: int
    source: str
    destination: str
    miles: float
    kilometers: float
    timestamp: datetime

    class Config:
        orm_mode = True

class QueryHistoryList(BaseModel):
    history: List[QueryRead] 