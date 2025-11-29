
from musigent.agents.planner import PlannerAgent
from musigent.agents.composer import ComposerAgent
from musigent.agents.quality import QualityAgent
from musigent.memory import MemoryStore
from musigent.agents.time import TimeAgent


class MusigentRunner:
    def __init__(self):
        self.memory = MemoryStore('memory_db.json')
        self.planner = PlannerAgent(self.memory)
        self.composer = ComposerAgent(self.memory)
        self.quality = QualityAgent(self.memory)
        self.time = TimeAgent(self.memory)

    def handle_request(self, mode, prompt, duration_sec=30):
        plan = self.planner.plan(mode, prompt, duration_sec)
        draft = self.composer.compose(plan)
        eval_ = self.quality.evaluate(draft)
        self.memory.save_interaction(plan, draft, eval_)
        time_info = self.time.get_time_info()
        return {"plan": plan,
                "draft": draft,
                "evaluation": eval_,
                "time_info": time_info
        }
