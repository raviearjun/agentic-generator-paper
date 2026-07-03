"""
Auto-generated AutoGen Team: TripPlannerCrew
Goals:
  - : Select the best city based on weather, season, and prices
  - : Provide the BEST insights about the selected city
  - : Create the most amazing travel itineraries with budget and packing suggestions for the city
  - : Automate the process of choosing among city options and producing a full trip itinerary based on traveler preferences.
Capabilities:
  - : Search the internet for relevant results using Serper API.
  - : Scrape and summarize website content using browserless and HTML partitioning.
  - : Perform safe mathematical calculations.
  - : Analyze travel data to select an optimal city based on weather, season, and prices.
  - : Provide deep local insights, attractions, cultural context, and practical tips.
  - : Create detailed itineraries, budgets, packing suggestions, and logistics.
"""

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


def tool_search_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_search

    Description:
    Search the internet using Serper (google.serper.dev) and return top results.
    """
    return (
        "Tool 'tool_search' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_search = FunctionTool(
    tool_search_impl,
    description="""Search the internet using Serper (google.serper.dev) and return top results. """
)


def tool_browser_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_browser

    Description:
    Scrape website content via browserless and summarize chunks using an internal Agent/Task.
    """
    return (
        "Tool 'tool_browser' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_browser = FunctionTool(
    tool_browser_impl,
    description="""Scrape website content via browserless and summarize chunks using an internal Agent/Task. """
)


def tool_calculator_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_calculator

    Description:
    Safe mathematical expression evaluator implemented with ast and restricted operators.
    """
    return (
        "Tool 'tool_calculator' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_calculator = FunctionTool(
    tool_calculator_impl,
    description="""Safe mathematical expression evaluator implemented with ast and restricted operators. """
)


# ==================================================
# Agents
# ==================================================


city_selection_agent = AssistantAgent(
    name="city_selection_agent",
    model_client=model_client,
    system_message="""
Role:
City Selection Expert

Goal:
Select the best city based on weather, season, and prices

Background:
You are a City Selection Expert.
""",
)


local_expert_agent = AssistantAgent(
    name="local_expert_agent",
    model_client=model_client,
    system_message="""
Role:
Local Expert at this city

Goal:
Provide the BEST insights about the selected city

Background:
You are a Local Expert at this city.
""",
)


travel_concierge_agent = AssistantAgent(
    name="travel_concierge_agent",
    model_client=model_client,
    system_message="""
Role:
Amazing Travel Concierge

Goal:
Create the most amazing travel itineraries with budget and packing suggestions for the city

Background:
You are a Amazing Travel Concierge.
""",
)



