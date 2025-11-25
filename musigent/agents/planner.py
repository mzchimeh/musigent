
class PlannerAgent:
    def __init__(self, memory):
        self.memory = memory

    def plan(self, mode, prompt, duration_sec):
        plan = {
            "mode": mode,
            "prompt": prompt,
            "duration_sec": duration_sec,
            "style": None,
            "tempo_range": None,
        }
        if mode == "jingle":
            plan["style"] = "short, catchy"
            plan["tempo_range"] = [100, 130]
        elif mode == "bgm":
            plan["style"] = "ambient, no-vocals"
            plan["tempo_range"] = [60, 90]
        elif mode == "persona":
            plan["style"] = "based-on-user-taste"
            plan["tempo_range"] = [70, 120]
        else:
            plan["style"] = "generic"
            plan["tempo_range"] = [60, 120]
        return plan
