"""
Auto-generated AutoGen Team: BirdCheckerSystem
Goals:
  - : Identify if an image depicts a bird, provide the scientific name if it is a bird, and summarize the image location in one or two short sentences.
Capabilities:
  - : Fetch random image matching a query from the Unsplash API
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
Bird checker

Goal:
Identify if an image depicts a bird, provide the scientific name if it is a bird, and summarize the image location in one or two short sentences.

Background:
You are a Bird checker.
""",
)



