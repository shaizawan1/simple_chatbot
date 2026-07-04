from langchain.agents import create_agent
from tools import get_weather_by_location
from prompt import system_prompt

def create_new_agent(model):
    agent = create_agent(
        model=model,
        tools=[get_weather_by_location],
        system_prompt=system_prompt
    )
    return agent