"""
Auto-generated AutoGen Team: CopyCrewagentsforcopygeneration
Goals:
  - : Produce thorough product and competitor analysis to inform marketing strategy.
  - : Formulate marketing strategies and creative ideas based on product and competitor analysis.
  - : Produce multiple Instagram ad copy options aligned with campaign strategy.
  - : Generate three photographic concepts that best represent the campaign and product without showing the actual product.
  - : Ensure final creative outputs are aligned with product goals; review and approve imagery.
  - : Produce marketing analysis and 3 Instagram ad copy options for the product.
  - : Produce three photograph concepts and a reviewed final selection aligned with campaign copy.
Capabilities:
  - : Extract and summarize HTML content from websites.
  - : Query web search API and return ranked result snippets.
  - : Search Instagram content via web search for post examples and snippets.
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


def tool_scrape_website_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_scrape_website

    Description:
    Scrapes a webpage via Browserless API and summarizes chunks using an LLM.
    """
    return (
        "Tool 'tool_scrape_website' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_scrape_website = FunctionTool(
    tool_scrape_website_impl,
    description="""Scrapes a webpage via Browserless API and summarizes chunks using an LLM. """
)


def tool_search_internet_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_search_internet

    Description:
    Performs web searches using the Serper (google.serper.dev) API and returns top results.
    """
    return (
        "Tool 'tool_search_internet' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_search_internet = FunctionTool(
    tool_search_internet_impl,
    description="""Performs web searches using the Serper (google.serper.dev) API and returns top results. """
)


def tool_search_instagram_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_search_instagram

    Description:
    Performs targeted Instagram site searches (site:instagram.com ...) via Serper API.
    """
    return (
        "Tool 'tool_search_instagram' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_search_instagram = FunctionTool(
    tool_search_instagram_impl,
    description="""Performs targeted Instagram site searches (site:instagram.com ...) via Serper API. """
)


# ==================================================
# Agents
# ==================================================


product_competitor_agent = AssistantAgent(
    name="product_competitor_agent",
    model_client=model_client,
    system_message="""
Role:
Lead Market Analyst

Goal:
Produce thorough product and competitor analysis to inform marketing strategy.

Background:
You are a Lead Market Analyst.
""",
)


strategy_planner_agent = AssistantAgent(
    name="strategy_planner_agent",
    model_client=model_client,
    system_message="""
Role:
Chief Marketing Strategist

Goal:
Formulate marketing strategies and creative ideas based on product and competitor analysis.

Background:
You are a Chief Marketing Strategist.
""",
)


creative_content_creator_agent = AssistantAgent(
    name="creative_content_creator_agent",
    model_client=model_client,
    system_message="""
Role:
Creative Content Creator

Goal:
Produce multiple Instagram ad copy options aligned with campaign strategy.

Background:
You are a Creative Content Creator.
""",
)


senior_photographer_agent = AssistantAgent(
    name="senior_photographer_agent",
    model_client=model_client,
    system_message="""
Role:
Senior Photographer

Goal:
Generate three photographic concepts that best represent the campaign and product without showing the actual product.

Background:
You are a Senior Photographer.
""",
)


chief_creative_diretor_agent = AssistantAgent(
    name="chief_creative_diretor_agent",
    model_client=model_client,
    system_message="""
Role:
Chief Creative Director

Goal:
Ensure final creative outputs are aligned with product goals; review and approve imagery.

Background:
You are a Chief Creative Director.
""",
)



