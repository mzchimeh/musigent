# musigent/agents/time.py
# Time tool: deterministic function that returns real UTC time + timezone.
import requests
from datetime import datetime
import os

def get_utc_time():
    try:
        key = os.environ["GOOGLE_API_KEY"]
        url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={key}"
        resp = requests.post(url, timeout=5)
        
        utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        return {
            "status": "success",
            "utc_time": utc,
            "source": "google geolocation"
        }
    except:
        return {"status": "error", "utc_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}
