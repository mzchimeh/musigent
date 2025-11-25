
import time

class SunoTool:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def generate_music(self, prompt, style, duration_sec):
        time.sleep(0.1)
        safe = prompt.replace(" ", "_")[:40]
        return f"https://example.com/mock_suno/{safe}_{duration_sec}.mp3"

class SpotifyTool:
    def __init__(self, token=None):
        self.token = token

    def analyze_user(self, user_id):
        return {"favorite_genres": ["dark_rock", "electronic"], "energy": 0.7}
