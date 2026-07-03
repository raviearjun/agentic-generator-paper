"""
Auto-generated AutoGen Team: StockAnalysisCrew
Goals:
  - : Automate the process of analyzing a stock to produce a detailed report and investment recommendation.
Capabilities:
  - : Performs arithmetic and mathematical calculations.
  - : Scrapes and summarizes web page content.
  - : Performs web searches and retrieves relevant results.
  - : Searches textual sources or indexes.
  - : Semantic search within a company's 10-K filing content.
  - : Semantic search within a company's 10-Q filing content.
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


def tool_calculator_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_calculator_tool

    Description:
    Performs safe mathematical expression evaluation (add, sub, mul, div, pow, mod).
    """
    return (
        "Tool 'tool_calculator_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_calculator_tool = FunctionTool(
    tool_calculator_tool_impl,
    description="""Performs safe mathematical expression evaluation (add, sub, mul, div, pow, mod). """
)


def tool_scrape_website_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_scrape_website_tool

    Description:
    Tool to scrape website content and convert to text for summarization.
    """
    return (
        "Tool 'tool_scrape_website_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_scrape_website_tool = FunctionTool(
    tool_scrape_website_tool_impl,
    description="""Tool to scrape website content and convert to text for summarization. """
)


def tool_website_search_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_website_search_tool

    Description:
    Tool to search the web for relevant pages and summaries.
    """
    return (
        "Tool 'tool_website_search_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_website_search_tool = FunctionTool(
    tool_website_search_tool_impl,
    description="""Tool to search the web for relevant pages and summaries. """
)


def tool_txt_search_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_txt_search_tool

    Description:
    Text search tool for searching indexed textual data.
    """
    return (
        "Tool 'tool_txt_search_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_txt_search_tool = FunctionTool(
    tool_txt_search_tool_impl,
    description="""Text search tool for searching indexed textual data. """
)


def tool_sec10_k_tool_generic_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_sec10_k_tool_generic

    Description:
    A tool to semantically search a company's latest 10-K SEC filing content.
    """
    return (
        "Tool 'tool_sec10_k_tool_generic' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_sec10_k_tool_generic = FunctionTool(
    tool_sec10_k_tool_generic_impl,
    description="""A tool to semantically search a company's latest 10-K SEC filing content. """
)


def tool_sec10_q_tool_generic_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_sec10_q_tool_generic

    Description:
    A tool to semantically search a company's latest 10-Q SEC filing content.
    """
    return (
        "Tool 'tool_sec10_q_tool_generic' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_sec10_q_tool_generic = FunctionTool(
    tool_sec10_q_tool_generic_impl,
    description="""A tool to semantically search a company's latest 10-Q SEC filing content. """
)


def tool_sec10_k_tool_amzn_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_sec10_k_tool_amzn

    Description:
    SEC10KTool initialized with stock_name=AMZN to pre-load AMZN latest 10-K content.
    """
    return (
        "Tool 'tool_sec10_k_tool_amzn' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_sec10_k_tool_amzn = FunctionTool(
    tool_sec10_k_tool_amzn_impl,
    description="""SEC10KTool initialized with stock_name=AMZN to pre-load AMZN latest 10-K content. """
)


def tool_sec10_q_tool_amzn_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_sec10_q_tool_amzn

    Description:
    SEC10QTool initialized with stock_name=AMZN to pre-load AMZN latest 10-Q content.
    """
    return (
        "Tool 'tool_sec10_q_tool_amzn' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_sec10_q_tool_amzn = FunctionTool(
    tool_sec10_q_tool_amzn_impl,
    description="""SEC10QTool initialized with stock_name=AMZN to pre-load AMZN latest 10-Q content. """
)


# ==================================================
# Agents
# ==================================================


financial_agent = AssistantAgent(
    name="financial_agent",
    model_client=model_client,
    system_message="""
Role:
The Best Financial Analyst

Goal:
The Best Financial Analyst

Background:
You are a The Best Financial Analyst.
""",
)


research_analyst_agent = AssistantAgent(
    name="research_analyst_agent",
    model_client=model_client,
    system_message="""
Role:
Staff Research Analyst

Goal:
Staff Research Analyst

Background:
You are a Staff Research Analyst.
""",
)


financial_analyst_agent = AssistantAgent(
    name="financial_analyst_agent",
    model_client=model_client,
    system_message="""
Role:
The Best Financial Analyst

Goal:
The Best Financial Analyst

Background:
You are a The Best Financial Analyst.
""",
)


investment_advisor_agent = AssistantAgent(
    name="investment_advisor_agent",
    model_client=model_client,
    system_message="""
Role:
Private Investment Advisor

Goal:
Private Investment Advisor

Background:
You are a Private Investment Advisor.
""",
)



