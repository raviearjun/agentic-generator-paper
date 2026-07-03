"""
Auto-generated AutoGen Team: ProposedChangeUITeam
Goals:
  - : Facilitate safe review and application of code changes via an agent-mediated user workflow.
Human Agents:
  - human_user ()
Capabilities:
  - : Apply proposed file changes / update repository file contents.
  - : Capability enabling the agent to request file updates via external tool calls.
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


def tool_update_file_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_update_file

    Description:
    Tool used to apply an accepted proposed change to files (invoked via tool call messages).
    """
    return (
        "Tool 'tool_update_file' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_update_file = FunctionTool(
    tool_update_file_impl,
    description="""Tool used to apply an accepted proposed change to files (invoked via tool call messages). """
)


# ==================================================
# Agents
# ==================================================


langgraph_agent = AssistantAgent(
    name="langgraph_agent",
    model_client=model_client,
    system_message="""
Role:
assistant

Goal:
assistant

Background:
You are a assistant.
""",
)


# ==================================================
# Human Agents (UserProxy)
# ==================================================

human_user = UserProxyAgent(
    name="human_user",
    description=""" """,
)

