"""
Auto-generated AutoGen Team: AICrewforscreenwriting
Goals:
  - : Create a screenplay from a newsgroup post.
Capabilities:
  - : Access and call Mistral LLM endpoint.
  - : Access and call Together.ai LLM endpoint.
  - : Access and call Anyscale LLM endpoint.
Resources:
  - : Resulting formatted screenplay dialogue produced by the Crew.
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


def mistral_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    mistral_tool

    Description:
    Official Mistral LLM API endpoint (optional selection in script).
    """
    return (
        "Tool 'mistral_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


mistral_tool = FunctionTool(
    mistral_tool_impl,
    description="""Official Mistral LLM API endpoint (optional selection in script). """
)


def together_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    together_tool

    Description:
    Together.ai models endpoint (optional selection in script).
    """
    return (
        "Tool 'together_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


together_tool = FunctionTool(
    together_tool_impl,
    description="""Together.ai models endpoint (optional selection in script). """
)


def anyscale_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    anyscale_tool

    Description:
    Anyscale models endpoint (optional selection in script).
    """
    return (
        "Tool 'anyscale_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


anyscale_tool = FunctionTool(
    anyscale_tool_impl,
    description="""Anyscale models endpoint (optional selection in script). """
)


# ==================================================
# Agents
# ==================================================


spamfilter = AssistantAgent(
    name="spamfilter",
    model_client=model_client,
    system_message="""
Role:
spamfilter

Goal:
spamfilter

Background:
You are a spamfilter.
""",
)


analyst = AssistantAgent(
    name="analyst",
    model_client=model_client,
    system_message="""
Role:
analyse

Goal:
analyse

Background:
You are a analyse.
""",
)


scriptwriter = AssistantAgent(
    name="scriptwriter",
    model_client=model_client,
    system_message="""
Role:
scriptwriter

Goal:
scriptwriter

Background:
You are a scriptwriter.
""",
)


formatter = AssistantAgent(
    name="formatter",
    model_client=model_client,
    system_message="""
Role:
formatter

Goal:
formatter

Background:
You are a formatter.
""",
)


scorer = AssistantAgent(
    name="scorer",
    model_client=model_client,
    system_message="""
Role:
scorer

Goal:
scorer

Background:
You are a scorer.
""",
)



