import os
import time
import requests


class SunoTool:
    def __init__(self, api_key: str | None = None,
                 model: str = "V4_5ALL",
                 callback_url: str = "https://example.com/callback"):
        # API key from arg or env (for Kaggle: use a secret named SUNO_API_KEY)
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
        Generate real music via Suno API.

        For jingles we use:
        - customMode = true
        - instrumental = true (no lyrics)
        - model = self.model
        - style = style from the plan
        - title = short version of prompt
        Duration is *hinted* in the prompt text (Suno doesn't take seconds directly).
        """
        # Build a short, safe title (required in customMode=true)
        safe_title = (prompt or "Brand Jingle")[:80]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "customMode": True,
            "instrumental": True,
            "model": self.model,
            "style": style,                # e.g. "high-energy, punchy, modern"
            "title": safe_title,
            # We don’t need lyrics since instrumental=True, but we hint duration in idea text:
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

            # Typical shape: {"code":200, "data":[{...},{...}], "msg":"success"}
            if data.get("code") != 200:
                # Return an error string so the rest of the pipeline still works
                return f"SUNO_ERROR: code={data.get('code')} msg={data.get('msg')}"

            tracks = data.get("data") or []
            if not tracks:
                return "SUNO_ERROR: no tracks returned"

            first = tracks[0]
            # Prefer stream URL; fallback to audioUrl
            url = first.get("streamUrl") or first.get("audioUrl")
            if not url:
                return "SUNO_ERROR: no URL in response"

            return url

        except Exception as e:
            # Fail gracefully but visibly
            return f"SUNO_EXCEPTION: {type(e).__name__}: {e}"


class SpotifyTool:
    def __init__(self, token=None):
        self.token = token

    def analyze_user(self, user_id):
        return {"favorite_genres": ["dark_rock", "electronic"], "energy": 0.7}
