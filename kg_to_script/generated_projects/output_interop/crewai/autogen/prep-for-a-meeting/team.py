"""
Auto-generated AutoGen Team: MeetingPreparationCrew
Goals:
  - : Conduct thorough research on people and companies involved in the meeting.
  - : Analyze the current industry trends, challenges, and opportunities.
  - : Develop talking points, questions, and strategic angles for the meeting.
  - : Compile all gathered information into a concise, informative briefing document.
Capabilities:
  - : Performs web searches and returns search result identifiers.
  - : Finds webpages similar to a given URL.
  - : Retrieves and returns contents of webpages by IDs.
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


def exa_search_tool_search_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    exa_search_tool_search

    Description:
    Search for a webpage based on the query (returns a list of result IDs).
    """
    return (
        "Tool 'exa_search_tool_search' "
        "is a generated stub and "
        "has not been implemented yet."
    )


exa_search_tool_search = FunctionTool(
    exa_search_tool_search_impl,
    description="""Search for a webpage based on the query (returns a list of result IDs). """
)


def exa_search_tool_find_similar_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    exa_search_tool_find_similar

    Description:
    Search for webpages similar to a given URL.
    """
    return (
        "Tool 'exa_search_tool_find_similar' "
        "is a generated stub and "
        "has not been implemented yet."
    )


exa_search_tool_find_similar = FunctionTool(
    exa_search_tool_find_similar_impl,
    description="""Search for webpages similar to a given URL. """
)


def exa_search_tool_get_contents_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    exa_search_tool_get_contents

    Description:
    Get the contents of webpages given a list of IDs.
    """
    return (
        "Tool 'exa_search_tool_get_contents' "
        "is a generated stub and "
        "has not been implemented yet."
    )


exa_search_tool_get_contents = FunctionTool(
    exa_search_tool_get_contents_impl,
    description="""Get the contents of webpages given a list of IDs. """
)


# ==================================================
# Agents
# ==================================================


researcher_agent = AssistantAgent(
    name="researcher_agent",
    model_client=model_client,
    system_message="""
Role:
Research Specialist

Goal:
Conduct thorough research on people and companies involved in the meeting.

Background:
You are a Research Specialist.
""",
)


industry_analyst_agent = AssistantAgent(
    name="industry_analyst_agent",
    model_client=model_client,
    system_message="""
Role:
Industry Analyst

Goal:
Analyze the current industry trends, challenges, and opportunities.

Background:
You are a Industry Analyst.
""",
)


meeting_strategy_agent = AssistantAgent(
    name="meeting_strategy_agent",
    model_client=model_client,
    system_message="""
Role:
Meeting Strategy Advisor

Goal:
Develop talking points, questions, and strategic angles for the meeting.

Background:
You are a Meeting Strategy Advisor.
""",
)


summary_and_briefing_agent = AssistantAgent(
    name="summary_and_briefing_agent",
    model_client=model_client,
    system_message="""
Role:
Briefing Coordinator

Goal:
Compile all gathered information into a concise, informative briefing document.

Background:
You are a Briefing Coordinator.
""",
)



