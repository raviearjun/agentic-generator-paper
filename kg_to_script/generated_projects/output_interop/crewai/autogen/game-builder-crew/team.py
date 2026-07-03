"""
Auto-generated AutoGen Team: GameBuilderCrew
Goals:
  - : Create software as needed
  - : Create Perfect code, by analyzing the code that is given for errors
  - : Ensure that the code does the job that it is supposed to do
  - : Automate the creation of a Python-based game using autonomous agents orchestrated by the CrewAI framework.
Capabilities:
  - : Web search and retrieval capability (e.g., Serper).
  - : Access to OpenAI language model API.
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


def tool_serper_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_serper

    Description:
    Serper search API used for web search (mentioned in README).
    """
    return (
        "Tool 'tool_serper' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_serper = FunctionTool(
    tool_serper_impl,
    description="""Serper search API used for web search (mentioned in README). """
)


def tool_openai_api_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_openai_api

    Description:
    OpenAI API access used by CrewAI to call LLMs (configured via environment variables).
    """
    return (
        "Tool 'tool_openai_api' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_openai_api = FunctionTool(
    tool_openai_api_impl,
    description="""OpenAI API access used by CrewAI to call LLMs (configured via environment variables). """
)


# ==================================================
# Agents
# ==================================================


senior_engineer_agent = AssistantAgent(
    name="senior_engineer_agent",
    model_client=model_client,
    system_message="""
Role:
Senior Software Engineer

Goal:
Create software as needed

Background:
You are a Senior Software Engineer.
""",
)


qa_engineer_agent = AssistantAgent(
    name="qa_engineer_agent",
    model_client=model_client,
    system_message="""
Role:
Software Quality Control Engineer

Goal:
Create Perfect code, by analyzing the code that is given for errors

Background:
You are a Software Quality Control Engineer.
""",
)


chief_qa_engineer_agent = AssistantAgent(
    name="chief_qa_engineer_agent",
    model_client=model_client,
    system_message="""
Role:
Chief Software Quality Control Engineer

Goal:
Ensure that the code does the job that it is supposed to do

Background:
You are a Chief Software Quality Control Engineer.
""",
)



