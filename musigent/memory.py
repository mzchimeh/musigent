
import json, os

class MemoryStore:
    def __init__(self, path="memory_db.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({"interactions": []}, f)

    def save_interaction(self, plan, draft, evaluation):
        with open(self.path, "r+") as f:
            data = json.load(f)
            data.setdefault("interactions", []).append({
                "plan": plan,
                "draft": draft,
                "evaluation": evaluation,
            })
            f.seek(0)
            json.dump(data, f, indent=2)
