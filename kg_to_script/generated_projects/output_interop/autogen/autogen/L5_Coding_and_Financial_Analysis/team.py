"""
Auto-generated AutoGen Team: CodingandFinancialAnalysisCrew
Goals:
  - : Produce and save plots (e.g., ytd_stock_gains.png, stock_prices_YTD_plot.png) showing year-to-date gains for requested tickers (NVDA and TSLA/TLSA).
Capabilities:
  - : Ability to execute arbitrary code snippets in a sandboxed local environment.
  - : Download historical stock close prices for given symbols and date range.
  - : Render time series plots for stock price data and save to image files.
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


def tool_local_cli_executor_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_local_cli_executor

    Description:
    Executor used to run code locally with a working directory and timeout; can register functions to be callable during execution.
    """
    return (
        "Tool 'tool_local_cli_executor' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_local_cli_executor = FunctionTool(
    tool_local_cli_executor_impl,
    description="""Executor used to run code locally with a working directory and timeout; can register functions to be callable during execution. """
)


def tool_get_stock_prices_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_get_stock_prices

    Description:
    Function that downloads stock prices using yfinance and returns closing prices for given symbols between start and end dates.
    """
    return (
        "Tool 'tool_get_stock_prices' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_get_stock_prices = FunctionTool(
    tool_get_stock_prices_impl,
    description="""Function that downloads stock prices using yfinance and returns closing prices for given symbols between start and end dates. """
)


def tool_plot_stock_prices_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_plot_stock_prices

    Description:
    Function that plots provided stock prices dataframe and saves the figure to a specified filename using matplotlib.
    """
    return (
        "Tool 'tool_plot_stock_prices' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_plot_stock_prices = FunctionTool(
    tool_plot_stock_prices_impl,
    description="""Function that plots provided stock prices dataframe and saves the figure to a specified filename using matplotlib. """
)


# ==================================================
# Agents
# ==================================================


code_writer_agent = AssistantAgent(
    name="code_writer_agent",
    model_client=model_client,
    system_message="""
Role:
Assistant / Code Writer

Goal:
Assistant / Code Writer

Background:
You are a Assistant / Code Writer.
""",
)


code_executor_agent = AssistantAgent(
    name="code_executor_agent",
    model_client=model_client,
    system_message="""
Role:
Code Executor

Goal:
Code Executor

Background:
You are a Code Executor.
""",
)



