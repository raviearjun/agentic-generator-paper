
from autogen_agentchat.agents import AssistantAgent

from autogen_agentchat.teams import RoundRobinGroupChat

from autogen_agentchat.conditions import (

    MaxMessageTermination

)

from autogen_core.tools import FunctionTool

from autogen_ext.models.openai import (
    OpenAIChatCompletionClient
)

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)


# ==================================================
# Generated Tool Stubs
# ==================================================


def tool_weather_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_weather_tool

    Description:
    Tool to fetch current weather data for a specified location (current conditions: temperature, humidity, wind, precipitation).
    """
    return (
        "Tool 'tool_weather_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_weather_tool = FunctionTool(
    tool_weather_tool_impl,
    description="""Tool to fetch current weather data for a specified location (current conditions: temperature, humidity, wind, precipitation). """
)


# ==================================================
# Agents
# ==================================================


weather_agent = AssistantAgent(
    name="weather_agent",
    model_client=model_client,
    system_message="""
Role:
Weather Assistant

Goal:
Weather Assistant

Background:
You are a Weather Assistant.
""",
)



