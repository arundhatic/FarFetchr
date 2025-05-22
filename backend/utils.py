# utils.py
# Utility functions for FarFetchr backend (geocoding, haversine, etc.)

import httpx
import math

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

async def geocode_address(address: str) -> tuple[float, float]:
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
    }
    headers = {"User-Agent": "FarFetchrApp/1.0 (your@email.com)"}
    async with httpx.AsyncClient() as client:
        response = await client.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError(f"Address not found: {address}")
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon

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