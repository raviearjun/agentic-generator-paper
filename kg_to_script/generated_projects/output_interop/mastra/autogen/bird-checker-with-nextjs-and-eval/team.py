"""
Auto-generated AutoGen Team: BirdCheckerSystem
Goals:
  - : System should determine whether a provided image contains a bird, identify its scientific name if present, and summarize location.
Capabilities:
  - : Fetch a random image from Unsplash matching the given query (wildlife | feathers | flying | birds).
Resources:
  - : Image object returned from Unsplash (urls, alt_description, user metadata).
  - : Structured classification output { bird: boolean, species: string, location: string }.
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


def get_random_image_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    get_random_image_tool

    Description:
    Gets a random image from unsplash based on the selected option
    """
    return (
        "Tool 'get_random_image_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


get_random_image_tool = FunctionTool(
    get_random_image_tool_impl,
    description="""Gets a random image from unsplash based on the selected option """
)


# ==================================================
# Agents
# ==================================================


bird_agent = AssistantAgent(
    name="bird_agent",
    model_client=model_client,
    system_message="""
Role:
bird classifier

Goal:
System should determine whether a provided image contains a bird, identify its scientific name if present, and summarize location.

Background:
You are a bird classifier.
""",
)



