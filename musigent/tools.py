import os
import requests


class SunoTool:
    def __init__(
        self,
        api_key: str | None = None,
        model: str = "V4_5ALL",
        callback_url: str = "https://example.com/callback",
    ):
        """
        Real Suno API client.

        API key is taken from:
        - explicit api_key argument, OR
        - SUNO_API_KEY environment variable (e.g. Kaggle secret)
        """
        self.api_key = api_key or os.getenv("SUNO_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Suno API key not set. "
                "Set SUNO_API_KEY env var or pass api_key=... to SunoTool()."
            )
        self.model = model
        self.callback_url = callback_url

    def generate_music(self, prompt: str, style: str, duration_sec: int):
        """
        Generate real music via Suno API and return a URL or an error string.
        """
        safe_title = (prompt or "Brand Jingle")[:80]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "customMode": True,
            "instrumental": True,
            "model": self.model,
            "style": style,
            "title": safe_title,
            "prompt": f"{prompt} (around {duration_sec} seconds jingle)",
            "callBackUrl": self.callback_url,
        }

        try:
            resp = requests.post(
                "https://api.sunoapi.org/api/v1/generate",
                headers=headers,
                json=payload,
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()

            # Some APIs wrap response, some don't – keep it flexible
            code = data.get("code", 200) if isinstance(data, dict) else 200

            # Specific handling for insufficient credits
            if code == 429:
                return "NO_CREDITS: Insufficient funds, please recharge your account."

            # Generic non-200 handling
            if code != 200:
                msg = data.get("msg") if isinstance(data, dict) else str(data)
                return f"SUNO_ERROR: code={code} msg={msg}"

            # Extract tracks
            if isinstance(data, dict):
                tracks = data.get("data")
            else:
                tracks = data

            if isinstance(tracks, dict):
                # e.g. {"0": {...}, "1": {...}}
                tracks = list(tracks.values())
            if tracks is None:
                tracks = []
            if not isinstance(tracks, list):
                tracks = [tracks]

            if not tracks:
                return f"SUNO_ERROR: no tracks returned, raw={data}"

            first = tracks[0] or {}
            url = first.get("streamUrl") or first.get("audioUrl")
            if not url:
                return f"SUNO_ERROR: no URL in first track, raw={first}"

            return url
                        # Specific handling for insufficient credits
            if code == 429:
                return (
                    "SUNO_NO_CREDITS: Insufficient funds, please recharge your Suno account.\n\n"
                    "<span style='color:red; font-weight:bold;'>❌ SUNO ERROR — INSUFFICIENT CREDITS</span><br>"
                    "Please recharge your Suno account to continue generating real audio."
                )
        except Exception as e:
            return f"SUNO_EXCEPTION: {type(e).__name__}: {e}"


class SpotifyTool:
    def __init__(self, token=None):
        self.token = token

    def analyze_user(self, user_id):
        # Still mocked – enough for persona mode and demos
        return {
            "favorite_genres": ["dark_rock", "electronic"],
            "energy": 0.7,
        }
