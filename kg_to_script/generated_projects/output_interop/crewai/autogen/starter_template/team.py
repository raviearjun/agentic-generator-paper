"""
Auto-generated AutoGen Team: CustomCrew
Goals:
  - : Define agent 1 goal here
  - : Define agent 2 goal here
Capabilities:
  - : Performs web searches and returns results
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


def tool_duck_duck_go_search_run_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_duck_duck_go_search_run

    Description:
    LangChain DuckDuckGo search tool used for web search
    """
    return (
        "Tool 'tool_duck_duck_go_search_run' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_duck_duck_go_search_run = FunctionTool(
    tool_duck_duck_go_search_run_impl,
    description="""LangChain DuckDuckGo search tool used for web search """
)


# ==================================================
# Agents
# ==================================================


agent_1_name = AssistantAgent(
    name="agent_1_name",
    model_client=model_client,
    system_message="""
Role:
Define agent 1 role here

Goal:
Define agent 1 goal here

Background:
You are a Define agent 1 role here.
""",
)


agent_2_name = AssistantAgent(
    name="agent_2_name",
    model_client=model_client,
    system_message="""
Role:
Define agent 2 role here

Goal:
Define agent 2 goal here

Background:
You are a Define agent 2 role here.
""",
)



