"""
Auto-generated AutoGen Team: MatchToProposalCrew
Goals:
  - : Extract relevant information from the CV, such as skills, experience, and education.
  - : Match the CV to the job opportunities based on skills, experience, and key achievements.
  - : Overall objective for the crew: automate the matching of candidate CVs to job proposals.
Capabilities:
  - : Capability to read file contents from disk.
  - : Capability to search and query CSV-formatted job listings.
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


def tool_file_read_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_file_read

    Description:
    Tool to read file contents (used to read CV and other files).
    """
    return (
        "Tool 'tool_file_read' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_file_read = FunctionTool(
    tool_file_read_impl,
    description="""Tool to read file contents (used to read CV and other files). """
)


def tool_csv_search_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_csv_search

    Description:
    Tool to search and query CSV files for matching job opportunities.
    """
    return (
        "Tool 'tool_csv_search' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_csv_search = FunctionTool(
    tool_csv_search_impl,
    description="""Tool to search and query CSV files for matching job opportunities. """
)


# ==================================================
# Agents
# ==================================================


cv_reader = AssistantAgent(
    name="cv_reader",
    model_client=model_client,
    system_message="""
Role:
CV Reader

Goal:
Extract relevant information from the CV, such as skills, experience, and education.

Background:
You are a CV Reader.
""",
)


matcher = AssistantAgent(
    name="matcher",
    model_client=model_client,
    system_message="""
Role:
Matcher

Goal:
Match the CV to the job opportunities based on skills, experience, and key achievements.

Background:
You are a Matcher.
""",
)



