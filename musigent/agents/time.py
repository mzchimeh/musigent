# musigent/agents/time.py
# Time tool: deterministic function that returns real UTC time + timezone.
from datetime import datetime
import requests

def get_utc_time() -> dict:
    try:
        resp = requests.get("https://worldtimeapi.org/api/ip", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        utc_dt = datetime.fromisoformat(data["utc_datetime"].replace("Z", "+00:00"))
        return {
            "status": "success",
            "utc_time": utc_dt.isoformat(),
            "timezone": data.get("timezone"),
            "raw_offset": data.get("raw_offset"),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
