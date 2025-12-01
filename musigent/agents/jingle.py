# musigent/agents/jingle.py
from dataclasses import dataclass

@dataclass
class JingleInput:
    brand_name: str
    company_field: str
    customer_persona: str
    vibe: str  # "energetic" | "peaceful" | "standard"

class JingleAgent:
    def build_plan(self, data: JingleInput) -> dict:
        vibe = data.vibe.lower()
        if vibe == "energetic":
            style = "high-energy, punchy, modern"
            tempo_range = "140-160 BPM"
        elif vibe == "peaceful":
            style = "soft, calm, warm"
            tempo_range = "70-90 BPM"
        else:
            style = "balanced, catchy, neutral"
            tempo_range = "100-120 BPM"

        prompt = (
            f"Create a 5-second audio logo (jingle) for the brand '{data.brand_name}'. "
            f"The company works in {data.company_field}. "
            f"Target customers: {data.customer_persona}. "
            f"The jingle should be {style}, memorable, and copyright-safe, "
            "without vocals, only instruments and sound design, suitable as a brand audio logo."
        )

        return {
            "mode": "jingle",
            "prompt": prompt,
            "style": style,
            "tempo_range": tempo_range,
            "duration_sec": 5,  # internal jingle length
        }
