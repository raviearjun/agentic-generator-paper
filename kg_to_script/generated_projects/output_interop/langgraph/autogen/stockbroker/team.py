"""
Auto-generated AutoGen Team: TradingSystem
Goals:
  - : Provide portfolio overview and enable executing trades via the UI.
Capabilities:
  - : Execute market buy orders for a specified ticker and quantity at the provided price.
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


def buy_stock_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    buy_stock_tool

    Description:
    Executes stock purchase orders when invoked by the UI. Expects a JSON content with purchaseDetails { ticker, quantity, price }.
    """
    return (
        "Tool 'buy_stock_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


buy_stock_tool = FunctionTool(
    buy_stock_tool_impl,
    description="""Executes stock purchase orders when invoked by the UI. Expects a JSON content with purchaseDetails { ticker, quantity, price }. """
)


# ==================================================
# Agents
# ==================================================


trade_agent = AssistantAgent(
    name="trade_agent",
    model_client=model_client,
    system_message="""
Role:
trading_assistant

Goal:
trading_assistant

Background:
You are a trading_assistant.
""",
)



