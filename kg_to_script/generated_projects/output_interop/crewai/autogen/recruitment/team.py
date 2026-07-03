"""
Auto-generated AutoGen Team: RecruitmentCrew
Goals:
  - : Agent goal: find potential candidates matching provided job requirements.
  - : Agent goal: evaluate and rank candidates against job requirements.
  - : Agent goal: create outreach templates and communication plans.
  - : Agent goal: compile findings and recommend top candidates.
  - : Team-level objective to orchestrate agent collaboration for recruitment.
Capabilities:
  - : Capability to query search APIs and return structured search results.
  - : Capability to extract information from web pages using DOM parsing.
  - : Capability to query LinkedIn search results and format profile summaries.
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


def tool_serperdev_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_serperdev

    Description:
    Search API tool for retrieving web search results.
    """
    return (
        "Tool 'tool_serperdev' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_serperdev = FunctionTool(
    tool_serperdev_impl,
    description="""Search API tool for retrieving web search results. """
)


def tool_scrape_website_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_scrape_website

    Description:
    Tool for scraping and extracting structured information from websites.
    """
    return (
        "Tool 'tool_scrape_website' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_scrape_website = FunctionTool(
    tool_scrape_website_impl,
    description="""Tool for scraping and extracting structured information from websites. """
)


def tool_linkedin_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_linkedin

    Description:
    Custom LinkedIn retrieval tool that uses an authenticated browser session to find candidate profiles.
    """
    return (
        "Tool 'tool_linkedin' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_linkedin = FunctionTool(
    tool_linkedin_impl,
    description="""Custom LinkedIn retrieval tool that uses an authenticated browser session to find candidate profiles. """
)


# ==================================================
# Agents
# ==================================================


researcher = AssistantAgent(
    name="researcher",
    model_client=model_client,
    system_message="""
Role:
Job Candidate Researcher

Goal:
Agent goal: find potential candidates matching provided job requirements.

Background:
You are a Job Candidate Researcher.
""",
)


matcher = AssistantAgent(
    name="matcher",
    model_client=model_client,
    system_message="""
Role:
Candidate Matcher and Scorer

Goal:
Agent goal: evaluate and rank candidates against job requirements.

Background:
You are a Candidate Matcher and Scorer.
""",
)


communicator = AssistantAgent(
    name="communicator",
    model_client=model_client,
    system_message="""
Role:
Candidate Outreach Strategist

Goal:
Agent goal: create outreach templates and communication plans.

Background:
You are a Candidate Outreach Strategist.
""",
)


reporter = AssistantAgent(
    name="reporter",
    model_client=model_client,
    system_message="""
Role:
Candidate Reporting Specialist

Goal:
Agent goal: compile findings and recommend top candidates.

Background:
You are a Candidate Reporting Specialist.
""",
)



