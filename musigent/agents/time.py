from google.adk.agents.llm_agent import Agent
from google.adk import tool
from datetime import datetime
import requests

@tool
def auto_time_utc() -> dict:
    ...
    
time_agent = Agent(
    model="gemini-3-pro-preview",
    name="time_agent",
    instruction="Auto-detect location and return UTC time.",
    tools=[auto_time_utc]
)
