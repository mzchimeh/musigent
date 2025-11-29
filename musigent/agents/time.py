# TimeAgent:
# Automatically detects the user's timezone via IP
# and returns the current time in UTC (timezone 0).
    
from google.adk.agents.llm_agent import Agent
from google.adk import tool
from datetime import datetime
import requests


@tool  # @tool registers this function as an ADK tool so the agent can call it.
def auto_time_utc() -> dict:
    """
    Automatically detects the user's timezone using IP
    and returns the current time in UTC (timezone 0).
    """
    try:
        # Detect timezone
        info = requests.get("https://ipapi.co/json/").json()
        tz = info.get("timezone", "Unknown")

        # UTC time
        utc_now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        return {
            "status": "success",
            "detected_timezone": tz,
            "utc_time": utc_now
        }

    except Exception:
        return {
            "status": "error",
            "utc_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }


class TimeAgent:
    """ADK-based agent that returns UTC time after auto-detecting location."""

    def __init__(self):
        self.agent = Agent(
            model="gemini-3-pro-preview",
            name="time_agent",
            instruction=(
                "Automatically detect user location via IP and return time in UTC "
                "using the auto_time_utc tool."
            ),
            tools=[auto_time_utc],
        )

    def get_time_info(self):
        """Call the ADK agent to retrieve UTC time."""
        return self.agent("What is the current time?")
