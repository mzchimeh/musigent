import uuid
from musigent.tools import SunoTool, SpotifyTool


class ComposerAgent:
    def __init__(self, memory):
        self.memory = memory
        self.suno = SunoTool()
        self.spotify = SpotifyTool()

    def compose(self, plan):
        track_id = str(uuid.uuid4())

        if plan["mode"] == "persona":
            taste = self.spotify.analyze_user("mock_user_id")
        else:
            taste = {}

        # ✅ enforce 5-second max for jingles
        duration = plan["duration_sec"]
        if plan["mode"] == "jingle":
            duration = min(5, duration)

        audio_url = self.suno.generate_music(
            plan["prompt"],
            plan["style"],
            duration,
        )

        draft = {
            "track_id": track_id,
            "audio_url": audio_url,
            "style": plan["style"],
            "tempo_range": plan["tempo_range"],
            "taste_profile": taste,
        }
        return draft
