from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import logging

from database import get_db
from models import Query, Base
from schemas import DistanceRequest, DistanceResponse, QueryHistoryList, QueryRead
from utils import geocode_address, haversine
from config import RATE_LIMIT, GEOCODE_MAX_RETRIES, GEOCODE_RETRY_DELAY, NOMINATIM_URL

# Set up logger
logger = logging.getLogger("farfetchr.api")
logging.basicConfig(level=logging.INFO)

# Create limiter instance with in-memory storage
limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMIT])
app = FastAPI()

# Add rate limiter middleware
app.add_middleware(SlowAPIMiddleware)
app.state.limiter = limiter

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"[CONFIG] RATE_LIMIT={RATE_LIMIT}")
print(f"[CONFIG] GEOCODE_MAX_RETRIES={GEOCODE_MAX_RETRIES}")
print(f"[CONFIG] GEOCODE_RETRY_DELAY={GEOCODE_RETRY_DELAY}")
print(f"[CONFIG] NOMINATIM_URL={NOMINATIM_URL}")

@app.post("/distance", response_model=DistanceResponse)
@limiter.limit(RATE_LIMIT)
async def calculate_distance(
    request: Request,
    req: DistanceRequest,
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"POST /distance - source: '{req.source}', destination: '{req.destination}'")
    try:
        src_lat, src_lon = await geocode_address(req.source)
        dest_lat, dest_lon = await geocode_address(req.destination)
    except Exception as e:
        logger.error(f"Geocoding failed: {e}")
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
        logger.info(f"Distance calculation saved to DB: {req.source} -> {req.destination} | {miles:.2f} mi, {kilometers:.2f} km")
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    logger.info(f"POST /distance - success: {req.source} -> {req.destination} | {miles:.2f} mi, {kilometers:.2f} km")
    return DistanceResponse(
        miles=miles,
        kilometers=kilometers,
        source=req.source,
        destination=req.destination,
        timestamp=now
    )

@app.get("/history", response_model=QueryHistoryList)
@limiter.limit(RATE_LIMIT)
async def get_history(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    logger.info("GET /history")
    try:
        result = await db.execute(select(Query).order_by(Query.timestamp.desc()))
        queries: List[Query] = result.scalars().all()
        logger.info(f"GET /history - returned {len(queries)} records")
        return QueryHistoryList(history=[QueryRead.model_validate(q, from_attributes=True) for q in queries])
    except SQLAlchemyError as e:
        logger.error(f"Database error on /history: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/")
def read_root():
    return {
        "message": "FarFetchr backend is running!",
        "docs": "Visit /docs for the interactive API documentation (Swagger UI)."
    } 