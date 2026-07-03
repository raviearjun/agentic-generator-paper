
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


def tool_a2_a_api_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_a2_a_api

    Description:
    A2A JSON-RPC HTTP API endpoints used to interact with remote agents (agent-card, message/send, message/stream, tasks/*, pushNotificationConfig/*).
    """
    return (
        "Tool 'tool_a2_a_api' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_a2_a_api = FunctionTool(
    tool_a2_a_api_impl,
    description="""A2A JSON-RPC HTTP API endpoints used to interact with remote agents (agent-card, message/send, message/stream, tasks/*, pushNotificationConfig/*). """
)


def tool_process_a2_a_stream_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_process_a2_a_stream

    Description:
    Utility to parse and yield typed A2A stream events (SSE -> typed Message/Task/TaskStatusUpdateEvent/TaskArtifactUpdateEvent).
    """
    return (
        "Tool 'tool_process_a2_a_stream' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_process_a2_a_stream = FunctionTool(
    tool_process_a2_a_stream_impl,
    description="""Utility to parse and yield typed A2A stream events (SSE -> typed Message/Task/TaskStatusUpdateEvent/TaskArtifactUpdateEvent). """
)


# ==================================================
# Agents
# ==================================================


agent_id_constructor_parameter = AssistantAgent(
    name="agent_id_constructor_parameter",
    model_client=model_client,
    system_message="""
Role:
A2A remote agent

Goal:
A2A remote agent

Background:
You are a A2A remote agent.
""",
)



