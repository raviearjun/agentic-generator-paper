"""
Auto-generated AutoGen Team: StandupDuo
Goals:
  - : Deliver a short comedic routine for the audience.
Capabilities:
  - : Provides LLM inference and chat functionality.
  - : Retrieves OpenAI API key from environment or secret store.
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


def tool_open_ai_api_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_open_ai_api

    Description:
    External LLM API used by ConversableAgent (via autogen/OpenAI client).
    """
    return (
        "Tool 'tool_open_ai_api' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_open_ai_api = FunctionTool(
    tool_open_ai_api_impl,
    description="""External LLM API used by ConversableAgent (via autogen/OpenAI client). """
)


def tool_get_openai_api_key_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_get_openai_api_key

    Description:
    Helper function used to retrieve the OpenAI API key from environment/config.
    """
    return (
        "Tool 'tool_get_openai_api_key' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_get_openai_api_key = FunctionTool(
    tool_get_openai_api_key_impl,
    description="""Helper function used to retrieve the OpenAI API key from environment/config. """
)


# ==================================================
# Agents
# ==================================================


chatbot = AssistantAgent(
    name="chatbot",
    model_client=model_client,
    system_message="""
Role:
conversable agent

Goal:
conversable agent

Background:
You are a conversable agent.
""",
)


unnamed = AssistantAgent(
    name="unnamed",
    model_client=model_client,
    system_message="""
Role:
逗哏 / stand-up comedian (performer)

Goal:
逗哏 / stand-up comedian (performer)

Background:
You are a 逗哏 / stand-up comedian (performer).
""",
)


unnamed = AssistantAgent(
    name="unnamed",
    model_client=model_client,
    system_message="""
Role:
捧哏 / stand-up partner (support)

Goal:
捧哏 / stand-up partner (support)

Background:
You are a 捧哏 / stand-up partner (support).
""",
)



