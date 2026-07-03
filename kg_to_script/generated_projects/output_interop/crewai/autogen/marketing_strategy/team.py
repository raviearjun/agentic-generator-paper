"""
Auto-generated AutoGen Team: MarketingPostsCrew
Goals:
  - : Create a comprehensive marketing strategy to showcase CrewAI's AI-driven solutions, emphasizing ease of use, scalability, and integration capabilities, targeting enterprise decision-makers.
  - : Conduct amazing analysis of the products and competitors, providing in-depth insights to guide marketing strategies.
  - : Synthesize amazing insights from product analysis to formulate incredible marketing strategies.
  - : Develop compelling and innovative content for social media campaigns, with a focus on creating high-impact ad copies.
Capabilities:
  - : Perform web search queries and return relevant search results.
  - : Retrieve and parse website content for analysis.
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


def tool_serper_dev_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_serper_dev_tool

    Description:
    Tool for performing web/search queries via Serper.dev (used to find up-to-date information).
    """
    return (
        "Tool 'tool_serper_dev_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_serper_dev_tool = FunctionTool(
    tool_serper_dev_tool_impl,
    description="""Tool for performing web/search queries via Serper.dev (used to find up-to-date information). """
)


def tool_scrape_website_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_scrape_website_tool

    Description:
    Tool to scrape website content for extracting information about customers and competitors.
    """
    return (
        "Tool 'tool_scrape_website_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_scrape_website_tool = FunctionTool(
    tool_scrape_website_tool_impl,
    description="""Tool to scrape website content for extracting information about customers and competitors. """
)


# ==================================================
# Agents
# ==================================================


lead_market_analyst = AssistantAgent(
    name="lead_market_analyst",
    model_client=model_client,
    system_message="""
Role:
Lead Market Analyst

Goal:
Conduct amazing analysis of the products and competitors, providing in-depth insights to guide marketing strategies.

Background:
You are a Lead Market Analyst.
""",
)


chief_marketing_strategist = AssistantAgent(
    name="chief_marketing_strategist",
    model_client=model_client,
    system_message="""
Role:
Chief Marketing Strategist

Goal:
Synthesize amazing insights from product analysis to formulate incredible marketing strategies.

Background:
You are a Chief Marketing Strategist.
""",
)


creative_content_creator = AssistantAgent(
    name="creative_content_creator",
    model_client=model_client,
    system_message="""
Role:
Creative Content Creator

Goal:
Develop compelling and innovative content for social media campaigns, with a focus on creating high-impact ad copies.

Background:
You are a Creative Content Creator.
""",
)



