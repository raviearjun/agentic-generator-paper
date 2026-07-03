"""
Auto-generated AutoGen Team: EmailAssistantTeamStateGraphsystem
Human Agents:
  - human_user ()
Capabilities:
  - : Produces an email object with subject, body, and recipient based on conversation history or user edits.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.agents import UserProxyAgent

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


def tool_write_email_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_write_email

    Description:
    Write an email based on the conversation history
    """
    return (
        "Tool 'tool_write_email' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_write_email = FunctionTool(
    tool_write_email_impl,
    description="""Write an email based on the conversation history """
)


# ==================================================
# Agents
# ==================================================


email_assistant_agent = AssistantAgent(
    name="email_assistant_agent",
    model_client=model_client,
    system_message="""
Role:
Email Assistant

Goal:
Email Assistant

Background:
You are a Email Assistant.
""",
)


# ==================================================
# Human Agents (UserProxy)
# ==================================================

human_user = UserProxyAgent(
    name="human_user",
    description=""" """,
)

