from api_client.openweather import OpenWeatherClient
from requests_cache import CachedSession
import os

client = OpenWeatherClient()

def extract_weather_by_city(city, units = 'metric'):
    """Return dict containing current + onecall (hourly/daily) where possible."""
    current = client.get_current_by_city(city, units=units)
    coords = current.get('coord', {})
    lat = coords.get('lat')
    lon = coords.get('lon')
    onecall = None
    if lat is not None and lon is not None:
        onecall = client.onecall_by_coords(lat, lon, units=units)
    result = {
        'current':current,
        'onecall':onecall
    }
    return result