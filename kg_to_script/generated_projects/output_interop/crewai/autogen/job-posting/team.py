"""
Auto-generated AutoGen Team: JobPostingCrew
Goals:
  - : Analyze the company website and provided description to extract insights on culture, values, and specific needs.
  - : Use insights from the Research Analyst to create a detailed, engaging, and enticing job posting.
  - : Review the job posting for clarity, engagement, grammatical accuracy, and alignment with the company's culture and values.
  - : Automate the creation of job postings using CrewAI to analyze company information and produce polished job descriptions and analyses.
Capabilities:
  - : Performs general website search and retrieval.
  - : Uses Serper.dev API for search and rich web results.
  - : Reads the contents of a local file for use by agents.
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


def website_search_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    website_search_tool

    Description:
    A generic website search tool used to look up pages and content.
    """
    return (
        "Tool 'website_search_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


website_search_tool = FunctionTool(
    website_search_tool_impl,
    description="""A generic website search tool used to look up pages and content. """
)


def serper_dev_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    serper_dev_tool

    Description:
    Serper.dev integration tool for advanced search queries.
    """
    return (
        "Tool 'serper_dev_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


serper_dev_tool = FunctionTool(
    serper_dev_tool_impl,
    description="""Serper.dev integration tool for advanced search queries. """
)


def file_read_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    file_read_tool

    Description:
    A tool to read a local job description example file.
    """
    return (
        "Tool 'file_read_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


file_read_tool = FunctionTool(
    file_read_tool_impl,
    description="""A tool to read a local job description example file. """
)


# ==================================================
# Agents
# ==================================================


research_agent = AssistantAgent(
    name="research_agent",
    model_client=model_client,
    system_message="""
Role:
Research Analyst

Goal:
Analyze the company website and provided description to extract insights on culture, values, and specific needs.

Background:
You are a Research Analyst.
""",
)


writer_agent = AssistantAgent(
    name="writer_agent",
    model_client=model_client,
    system_message="""
Role:
Job Description Writer

Goal:
Use insights from the Research Analyst to create a detailed, engaging, and enticing job posting.

Background:
You are a Job Description Writer.
""",
)


review_agent = AssistantAgent(
    name="review_agent",
    model_client=model_client,
    system_message="""
Role:
Review and Editing Specialist

Goal:
Review the job posting for clarity, engagement, grammatical accuracy, and alignment with the company's culture and values.

Background:
You are a Review and Editing Specialist.
""",
)



