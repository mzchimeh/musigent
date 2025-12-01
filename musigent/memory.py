import json, os
from datetime import datetime, timedelta 

class MemoryStore:
    def __init__(self, path="memory_db.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({"interactions": []}, f)
        # in-memory per-user daily counter (not persisted)
        self.user_daily = {}

    def _today_str(self) -> str:
        return datetime.utcnow().strftime("%Y-%m-%d")

    def get_user_daily_count(self, username: str) -> int:
        today = self._today_str()
        info = self.user_daily.get(username)
        if info and info["day"] == today:
            return info["count"]
        return 0

    def _increment_user_daily(self, username: str) -> None:
        today = self._today_str()
        info = self.user_daily.get(username)
        if not info or info["day"] != today:
            self.user_daily[username] = {"day": today, "count": 1}
        else:
            info["count"] += 1

    def save_interaction(self, plan, draft, evaluation, username="guest", time_info=None):
        """Append one interaction to the JSON log and update per-user daily count."""
        self._increment_user_daily(username)
        ts = datetime.utcnow().isoformat() + "Z"

        with open(self.path, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("interactions", []).append({
                "timestamp_utc": ts,
                "username": username,
                "plan": plan,
                "draft": draft,
                "evaluation": evaluation,
                "time_info": time_info,
            })
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    #This reads our JSON log (where we already save timestamp_utc and username) 
    #and counts how many events happened in the last 60 seconds for that user.       
    def get_user_recent_count(self, username: str, window_seconds: int = 60) -> int:
        """How many interactions this user had in the last window_seconds (UTC)."""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return 0

        now = datetime.utcnow()                      # naive UTC
        cutoff = now - timedelta(seconds=window_seconds)
        count = 0

        for item in data.get("interactions", []):
            if item.get("username") != username:
                continue

            ts = item.get("timestamp_utc") or item.get("timestamp")
            if not ts:
                continue

            try:
                # try to parse a few common formats
                s = ts.replace("Z", "+00:00").replace(" UTC", "")
                t = datetime.fromisoformat(s)
                # force naive UTC for safe comparison
                t = t.replace(tzinfo=None)
            except Exception:
                continue

            if t >= cutoff:
                count += 1

        return count
