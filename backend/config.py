import os

# Rate limiting
RATE_LIMIT = os.getenv("RATE_LIMIT", "50/minute")

# Retry settings for geocoding
GEOCODE_MAX_RETRIES = int(os.getenv("GEOCODE_MAX_RETRIES", 3))
GEOCODE_RETRY_DELAY = float(os.getenv("GEOCODE_RETRY_DELAY", 1.0))  # seconds

# Nominatim API URL
NOMINATIM_URL = os.getenv("NOMINATIM_URL", "https://nominatim.openstreetmap.org/search") 