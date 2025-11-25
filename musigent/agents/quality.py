
class QualityAgent:
    def __init__(self, memory):
        self.memory = memory

    def evaluate(self, draft):
        notes = []
        approved = True
        originality_score = 0.92

        if not draft.get("audio_url"):
            approved = False
            notes.append("No audio URL generated.")

        if originality_score < 0.8:
            approved = False
            notes.append("Low originality score.")

        return {
            "approved": approved,
            "originality_score": originality_score,
            "notes": notes,
        }
