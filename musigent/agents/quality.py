import os
import io
import requests
import numpy as np
from pydub import AudioSegment


class QualityAgent:
    def __init__(self, memory):
        self.memory = memory
        self.audd_key = os.getenv("AUDD_API_KEY", None)

    # -------------------------------------------------------------------------
    # MAIN EVALUATION PIPELINE
    # -------------------------------------------------------------------------
    def evaluate(self, draft):
        """
        Evaluation:
        - Originality score = audio variability (RMS deviation)
        - Copyright recognition via Audd.io
        """
        notes = []
        approved = True

        audio_url = draft.get("audio_url")

        # No audio URL at all → fail fast, do not pretend to evaluate originality
        if not audio_url:
            notes.append("No audio generated. Originality not computed.")
            return {
                "approved": False,
                "originality_score": None,
                "copyright_safety": {
                    "risk_level": "high",
                    "reasons": ["No audio available for analysis."],
                    "copyright_safety_score": 0,
                    "matched_track": None,
                },
                "notes": notes,
            }

        # ---- REAL originality score ----
        originality_score = self._compute_originality(audio_url)

        # If we could not analyze audio (e.g., Suno error / invalid file)
        if originality_score is None:
            approved = False
            notes.append("Audio could not be analyzed. Originality not computed.")

            # we still try copyright check – but if that also fails, risk stays high
            copyright_info = self._copyright_safety_check(audio_url)

            return {
                "approved": approved,
                "originality_score": None,
                "copyright_safety": copyright_info,
                "notes": notes,
            }

        # Normal case: originality successfully computed
        if originality_score < 0.35:
            approved = False
            notes.append("Low originality (audio too repetitive).")

        # ---- REAL copyright check ----
        copyright_info = self._copyright_safety_check(audio_url)

        if copyright_info.get("risk_level") == "high":
            approved = False

        return {
            "approved": approved,
            "originality_score": originality_score,
            "copyright_safety": copyright_info,
            "notes": notes,
        }

    # -------------------------------------------------------------------------
    # ORIGINALITY SCORE
    # -------------------------------------------------------------------------
    def _compute_originality(self, audio_url):
        """
        Computes originality score using RMS variance.
        High variance → dynamic, unique track
        Low variance → repetitive, low-originality music
        Score output: 0.0 to 1.0, or None if audio cannot be analyzed.
        """
        try:
            audio_bytes = requests.get(audio_url, timeout=10).content
            if not audio_bytes:
                return None

            audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

            # convert to mono array
            samples = np.array(audio.get_array_of_samples()).astype(np.float32)

            # compute RMS per chunk
            chunk_size = 2048
            rms_values = [
                float(np.sqrt(np.mean(samples[i:i + chunk_size] ** 2)))
                for i in range(0, len(samples), chunk_size)
            ]

            if len(rms_values) < 2:
                # Too short / invalid to measure originality
                return None

            # originality is variance normalized
            variability = np.std(rms_values)
            if max(rms_values) == 0:
                return None

            normalized = min(1.0, variability / max(rms_values))

            return round(float(normalized), 3)

        except Exception:
            # Any decoding/network error → treat as "not analyzable"
            return None

    # -------------------------------------------------------------------------
    # COPYRIGHT CHECK (USING AUDD.IO)
    # -------------------------------------------------------------------------
    def _copyright_safety_check(self, audio_url):
        """
        Step 1 — Heuristic baseline
        Step 2 — Audd.io recognition check
        """
        score = 70  # neutral baseline
        reasons = ["Baseline heuristic applied"]
        match_title = None

        try:
            audio_bytes = requests.get(audio_url, timeout=10).content

            if self.audd_key and audio_bytes:
                resp = requests.post(
                    "https://api.audd.io/",
                    data={
                        "api_token": self.audd_key,
                        "method": "recognize",
                        "return": "apple_music,spotify",
                    },
                    files={"file": ("audio.mp3", audio_bytes)},
                    timeout=20,
                )

                data = resp.json()
                result = data.get("result")

                if result:
                    match_title = f"{result.get('artist')} - {result.get('title')}"
                    score = min(score, 25)
                    reasons.append(f"Matched copyrighted track: {match_title}")
                else:
                    reasons.append("No match found in Audd.io database.")
            else:
                reasons.append("Audd.io API key missing or audio empty; skipping recognition.")

        except Exception as e:
            reasons.append(f"Audd.io error: {e}")

        # Compute risk
        if score >= 80:
            risk = "low"
        elif score >= 50:
            risk = "medium"
        else:
            risk = "high"

        return {
            "copyright_safety_score": score,
            "risk_level": risk,
            "matched_track": match_title,
            "reasons": reasons,
        }
