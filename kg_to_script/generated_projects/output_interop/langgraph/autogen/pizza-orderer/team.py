"""
Auto-generated AutoGen Team: OrderPizzaGraphTeam
Goals:
  - : High-level goal to find a pizza shop and place an order for the user.
Capabilities:
  - : Find nearby pizza shop and return contact details (address, phone).
  - : Place an order at the specified pizza shop and return order confirmation.
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


def find_pizza_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    find_pizza_tool

    Description:
    Tool invoked to search for a pizza shop and return address and phone number.
    """
    return (
        "Tool 'find_pizza_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


find_pizza_tool = FunctionTool(
    find_pizza_tool_impl,
    description="""Tool invoked to search for a pizza shop and return address and phone number. """
)


def place_order_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    place_order_tool

    Description:
    Tool invoked to place a pizza order and confirm success.
    """
    return (
        "Tool 'place_order_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


place_order_tool = FunctionTool(
    place_order_tool_impl,
    description="""Tool invoked to place a pizza order and confirm success. """
)


# ==================================================
# Agents
# ==================================================


langgraph_anthropic_agent = AssistantAgent(
    name="langgraph_anthropic_agent",
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



