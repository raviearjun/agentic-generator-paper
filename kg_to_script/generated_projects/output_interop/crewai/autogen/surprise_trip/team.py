"""
Auto-generated AutoGen Team: SurpriseTravelCrew
Goals:
  - : Create a comprehensive surprise travel plan for the traveler covering activities, restaurants, and a day-by-day itinerary.
Capabilities:
  - : Performs web searches for information such as events, activities, and restaurant listings.
  - : Extracts structured information from web pages (addresses, ratings, descriptions).
  - : Research and recommend activities suitable to traveler preferences.
  - : Find and recommend restaurants and scenic dining locations.
  - : Compile research into a day-by-day itinerary document.
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


def tool_serper_dev_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_serper_dev_tool

    Description:
    Web search tool (Serper.dev) used to search the web for activities, restaurants, and general information.
    """
    return (
        "Tool 'tool_serper_dev_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_serper_dev_tool = FunctionTool(
    tool_serper_dev_tool_impl,
    description="""Web search tool (Serper.dev) used to search the web for activities, restaurants, and general information. """
)


def tool_scrape_website_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_scrape_website_tool

    Description:
    Tool used to scrape website content for details about venues, restaurants and events.
    """
    return (
        "Tool 'tool_scrape_website_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_scrape_website_tool = FunctionTool(
    tool_scrape_website_tool_impl,
    description="""Tool used to scrape website content for details about venues, restaurants and events. """
)


# ==================================================
# Agents
# ==================================================


personalized_activity_planner = AssistantAgent(
    name="personalized_activity_planner",
    model_client=model_client,
    system_message="""
Role:
Activity Planner

Goal:
Activity Planner

Background:
You are a Activity Planner.
""",
)


restaurant_scout = AssistantAgent(
    name="restaurant_scout",
    model_client=model_client,
    system_message="""
Role:
Restaurant Scout

Goal:
Restaurant Scout

Background:
You are a Restaurant Scout.
""",
)


itinerary_compiler = AssistantAgent(
    name="itinerary_compiler",
    model_client=model_client,
    system_message="""
Role:
Itinerary Compiler

Goal:
Itinerary Compiler

Background:
You are a Itinerary Compiler.
""",
)



