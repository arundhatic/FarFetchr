from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from datetime import datetime

from database import get_db
from models import Query, Base
from schemas import DistanceRequest, DistanceResponse, QueryHistoryList, QueryRead
from utils import geocode_address, haversine

app = FastAPI()

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/distance", response_model=DistanceResponse)
async def calculate_distance(
    req: DistanceRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        src_lat, src_lon = await geocode_address(req.source)
        dest_lat, dest_lon = await geocode_address(req.destination)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    miles, kilometers = haversine(src_lat, src_lon, dest_lat, dest_lon)
    now = datetime.utcnow()
    query = Query(
        source=req.source,
        destination=req.destination,
        miles=miles,
        kilometers=kilometers,
        timestamp=now
    )
    try:
        db.add(query)
        await db.commit()
        await db.refresh(query)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    return DistanceResponse(
        miles=miles,
        kilometers=kilometers,
        source=req.source,
        destination=req.destination,
        timestamp=now
    )

@app.get("/history", response_model=QueryHistoryList)
async def get_history(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Query).order_by(Query.timestamp.desc()))
        queries: List[Query] = result.scalars().all()
        return QueryHistoryList(history=[QueryRead.model_validate(q, from_attributes=True) for q in queries])
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error") 