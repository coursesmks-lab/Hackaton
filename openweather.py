# api_client/openweather.py
from dotenv import load_dotenv
load_dotenv()  # <-- add this here

import os
from requests_cache import CachedSession
import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")




import os
from requests_cache import CachedSession
import requests

# API_KEY = os.getenv("OPENWEATHER_API_KEY")
# API_KEY = '001c86e9a7d72a913a2a71c61f07fd5c'

session = CachedSession('cache/openweather_cache',expire_after = 300)

class OpenWeatherClient:
    BASE = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key=None, session_obj=None):
        self.api_key = api_key or API_KEY
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY requird. Set it in .env or env vars.")
        self.session = session_obj or session

        adapter = requests.adapters.HTTPAdapter(max_retries = 3)
        self.session.mount('https://',adapter)
    
    def get_current_by_city(self, city, units="metric"):
        if not city or not city.strip():
            raise ValueError("City cannot be empty")
        params = {"q" : city, "appid": self.api_key, "units":units}
        url = f"{self.BASE}/weather"
        resp = self.session.get(url, params = params, timeout =10)
        if resp.status_code == 200:
            return resp.json()
        try:
            js = resp.json()
            msg = js.get('message') or str(js)
        except Exception:
            msg = resp.text
        raise RuntimeError(f"Openweather error {resp.status_code}:{msg}")
    def onecall_by_coords(self, lat, lon, exclude = None, units = "metric"):
        if lat is None or lon is None:
            raise ValueError('lat and lon are required')
        params = {"lat" : lat , "lon":lon , "appid":self.api_key, "units":units}
        if exclude:
            params['exclude'] = ','.join(exclude)
        url = f"{self.BASE}/onecall"
        resp = self.session.get(url,params = params, timeout = 10)
        if resp.status_code == 200:
            return resp.json()
        try:
            js = resp.json()
            msg = js.get('message') or str(js)
        except Exception:
            msg = resp.text
        raise RuntimeError(f"Openweather onecall error {resp.status_code}:{msg}")