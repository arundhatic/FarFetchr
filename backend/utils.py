# utils.py
# Utility functions for FarFetchr backend (geocoding, haversine, etc.)

import httpx
import math
import re
import asyncio
import logging
from config import NOMINATIM_URL, GEOCODE_MAX_RETRIES, GEOCODE_RETRY_DELAY

# Set up logger
logger = logging.getLogger("farfetchr.geocode")
logging.basicConfig(level=logging.INFO)

def clean_address(address: str) -> str:
    # Remove 'Suite' and anything after, extra commas, and trim whitespace
    cleaned = re.sub(r'suite.*$', '', address, flags=re.IGNORECASE)
    cleaned = re.sub(r',+', ',', cleaned)
    cleaned = re.sub(r'\s+,', ',', cleaned)
    cleaned = re.sub(r',+\s*$', '', cleaned)
    return cleaned.strip()

ACCEPTED_TYPES = {
    "house", "building", "road", "residential", "street", "tertiary", "secondary", "primary"
}

async def geocode_address(address: str) -> tuple[float, float]:
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
    }
    headers = {"User-Agent": "FarFetchrApp/1.0 (your@email.com)"}
    attempt = 0
    last_exception = None
    while attempt < GEOCODE_MAX_RETRIES:
        try:
            async with httpx.AsyncClient() as client:
                logger.info(f"Geocoding attempt {attempt+1} for address: {address}")
                response = await client.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Nominatim response for address '{address}': {data}")
                if data:
                    result = data[0]
                    importance = float(result.get("importance", 0))
                    result_type = result.get("type", "")
                    display_name = result.get("display_name", "").lower()
                    address_parts = [part.lower() for part in address.split() if part]
                    if sum(part in display_name for part in address_parts) < 1:
                        logger.warning(f"Geocoding result not matched: {address} -> {display_name}")
                        raise ValueError(f"Address not matched: {address}")
                    if importance < 0.1 or result_type not in {"building", "house", "residential"}:
                        logger.warning(f"Geocoding result for '{address}' is low importance ({importance}) or not a building/house/residential (type={result_type}): {display_name}")
                    lat = float(result["lat"])
                    lon = float(result["lon"])
                    logger.info(f"Geocoding success for address: {address} -> ({lat}, {lon})")
                    return lat, lon
                # Try again with cleaned address
                cleaned = clean_address(address)
                if cleaned != address:
                    logger.info(f"Retrying with cleaned address: {cleaned}")
                    params["q"] = cleaned
                    response = await client.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    logger.info(f"Nominatim response for cleaned address '{cleaned}': {data}")
                    if data:
                        result = data[0]
                        importance = float(result.get("importance", 0))
                        result_type = result.get("type", "")
                        display_name = result.get("display_name", "").lower()
                        address_parts = [part.lower() for part in cleaned.split() if part]
                        if sum(part in display_name for part in address_parts) < 1:
                            logger.warning(f"Geocoding result not matched: {cleaned} -> {display_name}")
                            raise ValueError(f"Address not matched: {cleaned}")
                        if importance < 0.1 or result_type not in {"building", "house", "residential"}:
                            logger.warning(f"Geocoding result for cleaned '{cleaned}' is low importance ({importance}) or not a building/house/residential (type={result_type}): {display_name}")
                        lat = float(result["lat"])
                        lon = float(result["lon"])
                        logger.info(f"Geocoding success for cleaned address: {cleaned} -> ({lat}, {lon})")
                        return lat, lon
            logger.warning(f"No geocoding result for address: {address} (attempt {attempt+1})")
        except (httpx.RequestError, httpx.HTTPStatusError, ValueError) as e:
            logger.error(f"Geocoding API error on attempt {attempt+1} for address '{address}': {e}")
            last_exception = e
        attempt += 1
        if attempt < GEOCODE_MAX_RETRIES:
            await asyncio.sleep(GEOCODE_RETRY_DELAY)
    logger.error(f"Geocoding failed after {GEOCODE_MAX_RETRIES} attempts for address: {address}")
    raise ValueError(f"Address not found after {GEOCODE_MAX_RETRIES} attempts: {address}")

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> tuple[float, float]:
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    km = R * c
    miles = km * 0.621371
    return miles, km

# TODO: Implement geocoding and haversine formula 