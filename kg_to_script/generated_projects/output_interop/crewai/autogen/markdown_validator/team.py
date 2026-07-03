"""
Auto-generated AutoGen Team: MarkDownValidatorCrew
Goals:
  - : Provide a detailed list of the markdown linting results.
Give a summary with actionable tasks to address the validation results.
Write your response as if you were handing it to a developer to fix the issues.
DO NOT provide examples of how to fix the issues or recommend other tools to use.
Capabilities:
  - : Identify markdown syntax issues using pymarkdown, returning formatted scan failures (file, line, rule, description).
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


def markdown_validation_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    markdown_validation_tool

    Description:
    A tool to review files for markdown syntax errors. Uses PyMarkdownApi to scan a file path and returns formatted scan results.
    """
    return (
        "Tool 'markdown_validation_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


markdown_validation_tool = FunctionTool(
    markdown_validation_tool_impl,
    description="""A tool to review files for markdown syntax errors. Uses PyMarkdownApi to scan a file path and returns formatted scan results. """
)


# ==================================================
# Agents
# ==================================================


requirements_manager = AssistantAgent(
    name="requirements_manager",
    model_client=model_client,
    system_message="""
Role:
Requirements Manager

Goal:
Provide a detailed list of the markdown linting results.
Give a summary with actionable tasks to address the validation results.
Write your response as if you were handing it to a developer to fix the issues.
DO NOT provide examples of how to fix the issues or recommend other tools to use.

Background:
You are a Requirements Manager.
""",
)



