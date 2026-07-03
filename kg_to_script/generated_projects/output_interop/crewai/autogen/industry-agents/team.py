"""
Auto-generated AutoGen Team: blogcrew
Goals:
  - : Continuously track the latest biomedical advancements and identify how Weaviate’s features can support AI applications in biomedical research, diagnostics, and personalized medicine.
  - : Stay updated on healthcare policy shifts, digital health trends, and explore how Weaviate’s features can optimize workflows in hospital systems, EHR integration, and health communication.
  - : Monitor financial sector trends including AI in trading, compliance automation, and client advisory, and assess how Weaviate’s tools can enable cutting-edge financial applications.
Capabilities:
  - : Performs semantic vector search over document chunks in Weaviate.
  - : Performs web search via Serper.dev.
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


def tool_weaviate_vector_search_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_weaviate_vector_search_tool

    Description:
    Vector search tool using Weaviate for semantic retrieval from collection 'WeaviateBlogChunk'.
    """
    return (
        "Tool 'tool_weaviate_vector_search_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_weaviate_vector_search_tool = FunctionTool(
    tool_weaviate_vector_search_tool_impl,
    description="""Vector search tool using Weaviate for semantic retrieval from collection 'WeaviateBlogChunk'. """
)


def tool_serper_dev_tool_impl(
    query: str = ""
) -> str:
    """
    AgentO Tool:
    tool_serper_dev_tool

    Description:
    Web search tool backed by Serper.dev.
    """
    return (
        "Tool 'tool_serper_dev_tool' "
        "is a generated stub and "
        "has not been implemented yet."
    )


tool_serper_dev_tool = FunctionTool(
    tool_serper_dev_tool_impl,
    description="""Web search tool backed by Serper.dev. """
)


# ==================================================
# Agents
# ==================================================


biomedical_marketing_agent = AssistantAgent(
    name="biomedical_marketing_agent",
    model_client=model_client,
    system_message="""
Role:
Industry researcher focused on biomedical trends and their applications in AI

Goal:
Continuously track the latest biomedical advancements and identify how Weaviate’s features can support AI applications in biomedical research, diagnostics, and personalized medicine.

Background:
You are a Industry researcher focused on biomedical trends and their applications in AI.
""",
)


healthcare_marketing_agent = AssistantAgent(
    name="healthcare_marketing_agent",
    model_client=model_client,
    system_message="""
Role:
AI-savvy marketer specializing in healthcare systems, digital health, and patient engagement.

Goal:
Stay updated on healthcare policy shifts, digital health trends, and explore how Weaviate’s features can optimize workflows in hospital systems, EHR integration, and health communication.

Background:
You are a AI-savvy marketer specializing in healthcare systems, digital health, and patient engagement..
""",
)


financial_marketing_agent = AssistantAgent(
    name="financial_marketing_agent",
    model_client=model_client,
    system_message="""
Role:
Insight analyst exploring innovations in finance, wealth tech, and regulatory tech

Goal:
Monitor financial sector trends including AI in trading, compliance automation, and client advisory, and assess how Weaviate’s tools can enable cutting-edge financial applications.

Background:
You are a Insight analyst exploring innovations in finance, wealth tech, and regulatory tech.
""",
)



