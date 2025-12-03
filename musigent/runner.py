from musigent.utils.formatter import result_to_dataframe
from musigent.memory import MemoryStore
from musigent.agents.planner import PlannerAgent
from musigent.agents.composer import ComposerAgent
from musigent.agents.quality import QualityAgent
from musigent.agents.jingle import JingleAgent, JingleInput
from musigent.agents.time import get_utc_time


class MusigentRunner:
    def __init__(self):
        self.memory = MemoryStore("memory_db.json")
        self.planner = PlannerAgent(self.memory)
        self.composer = ComposerAgent(self.memory)
        self.quality = QualityAgent(self.memory)
        self.jingle = JingleAgent()

    def handle_request(self, mode, prompt, duration_sec: int = 30, username: str = "guest"):
        plan = self.planner.plan(mode, prompt, duration_sec)
        draft = self.composer.compose(plan)
        eval_ = self.quality.evaluate(draft)
        time_info = get_utc_time()

        self.memory.save_interaction(plan, draft, eval_, username, time_info)

        result = {
            "plan": plan,
            "draft": draft,
            "evaluation": eval_,
            "time_info": time_info,
        }
        result["table"] = result_to_dataframe(result)
        return result

    def handle_jingle_survey(
        self,
        brand_name: str,
        company_field: str,
        customer_persona: str,
        vibe: str,
        username: str = "guest",
    ):
        # short-term rate limit (max 5 requests per 60 seconds)
        if self.memory.get_user_recent_count(username, window_seconds=60) >= 5:
            return {
                "error": "Rate limit: max 5 jingle requests per minute per user. Please wait and try again."
            }

        # daily limit: max 5 jingles per user per day
        if self.memory.get_user_daily_count(username) >= 5:
            return {
                "error": "Daily limit reached. Max 5 jingles per user per day."
            }

        j_input = JingleInput(
            brand_name=brand_name,
            company_field=company_field,
            customer_persona=customer_persona,
            vibe=vibe,
        )

        plan = self.jingle.build_plan(j_input)
        draft = self.composer.compose(plan)
        eval_ = self.quality.evaluate(dr_
